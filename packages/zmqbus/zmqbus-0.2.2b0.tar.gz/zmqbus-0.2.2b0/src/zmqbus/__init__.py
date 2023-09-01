"""A data bus for ZeroMQ"""
import sys
import time
import tempfile
import logging
import secrets
import warnings
from collections import deque
from threading import Thread, get_ident
from typing import (Any, Optional, Dict, Deque, Sequence, Tuple,
                    NamedTuple, Callable, Union)

import zmq
from zmq.auth.thread import ThreadAuthenticator

__all__ = [
    'Message',
    'MESSAGE_FACTORY',
    'Bus',
    'Connection',
    'TOPIC_HELO',
    'TOPIC_PING',
    'TOPIC_DEAD',
    'TOPIC_LIVE',
    'TOPIC_QUIT',
    'TOPIC_HALT',
]

__version__ = '0.2.2b'

logger = logging.getLogger(__name__)

TOPIC_HELO = '_HELO'
TOPIC_PING = '_PING'
TOPIC_DEAD = '_DEAD'
TOPIC_LIVE = '_LIVE'
TOPIC_QUIT = '_QUIT'
TOPIC_HALT = '_HALT'

_CONTROL_ADDRESS = 'inproc://zmqbus.control'

_DEFAULT_TCP_ADDRESS = 'tcp://127.0.0.1:*'


def _is_control_topic(topic: str) -> bool:
    return topic in {TOPIC_HELO, TOPIC_PING, TOPIC_DEAD,
                     TOPIC_LIVE, TOPIC_QUIT, TOPIC_HALT}


def _assert_valid_user_topic(topic: str) -> None:
    if '\n' in topic:
        raise ValueError(f"Invalid topic {topic!r}: cannot contain newlines")


def _assert_valid_control_topic(topic: str) -> None:
    if not _is_control_topic(topic):
        raise ValueError(f'Invalid control topic: {topic!r}')


def _assert_connected(socket: Optional[zmq.Socket[Any]]) -> None:
    if socket is None or socket.closed:
        raise BrokenPipeError()


def _assert_valid_connection_name(name: str) -> None:
    if '\n' in name:
        raise ValueError('Invalid connection name {name!r}')


def _proxy_capture(ctx: zmq.Context[Any], address: str) -> None:
    sock = ctx.socket(zmq.PULL)
    sock.connect(address)
    try:
        while True:
            msg = sock.recv_multipart()
            if msg == [b'']:
                break
            if msg[0][0] in b'_*!<>':
                logger.debug('%s > topic=%r %r',
                             f'{msg[1]!r}' if msg[1] else '*BUS*',
                             msg[0], msg[2:])
            else:
                logger.debug('<! %r', msg)
    finally:
        sock.close()
    logger.debug('Capture thread stopped')


def _proxy(ctx: zmq.Context[Any],
           xpub: zmq.Socket[Any],
           xsub: zmq.Socket[Any],
           control_address: str,
           debug: bool) -> None:
    logger.debug('Proxy thread started')

    control = ctx.socket(zmq.PULL)
    control.connect(control_address)

    capture_t: Optional[Thread]
    capture: Optional[zmq.Socket[Any]]

    if debug:
        address = f'inproc://zmqbus.capture.{get_ident()}'
        capture = ctx.socket(zmq.PUSH)
        assert capture
        capture.bind(address)
        capture_t = Thread(name=f'bus-capture-{hex(get_ident())}',
                           target=_proxy_capture,
                           args=(ctx, address))
        capture_t.start()
    else:
        capture_t = capture = None

    try:
        # Dear pylint,
        #
        # I'm pretty sure that the member exists.
        #
        # pylint: disable-next=no-member
        zmq.proxy_steerable(xpub, xsub, capture, control)
    finally:
        if capture_t and capture_t.is_alive():
            assert capture
            capture.send(b'')  # Signal capture thread to exit.
            capture_t.join()
            capture.close()
        control.close()
        xpub.close()
        xsub.close()

    logger.debug('Proxy thread stopped')


def halt(address: str,
         authkey: Optional[bytes] = None,
         context: Optional[zmq.Context[Any]] = None,
         timeout_ms: float = 60_000) -> None:
    if not context:
        context = zmq.Context.instance()
    if authkey is None:
        authkey = get_authkey()
    with context.socket(zmq.REQ) as sock:
        sock.linger = 1
        sock.set_string(zmq.PLAIN_USERNAME, __name__)
        sock.set_string(zmq.PLAIN_PASSWORD, authkey.hex())
        sock.connect(address)
        if not sock.poll(timeout_ms, zmq.POLLOUT):
            raise TimeoutError()
        sock.send_string('stop')
        if not sock.poll(timeout_ms, zmq.POLLIN):
            raise TimeoutError()
        sock.recv()  # 'ok'.


class Message(NamedTuple):
    sender: Optional[str]
    to: Union[str, Sequence[str], None]
    topic: str
    payload: Any

    @property
    def is_unicast(self) -> bool:
        return self.to is not None

    @property
    def is_broadcast(self) -> bool:
        return self.to is None


MESSAGE_FACTORY = Message  # pylint: disable=invalid-name

_authkey: Optional[bytes] = None


def get_authkey() -> bytes:
    global _authkey  # pylint: disable=global-statement,invalid-name
    if not _authkey:
        _authkey = secrets.token_bytes()
    return _authkey


class Bus:  # pylint: disable=too-many-instance-attributes

    def __init__(self,  # pylint: disable=too-many-arguments
                 address: str,
                 authkey: Optional[bytes] = None,
                 context: Optional[zmq.Context[Any]] = None,
                 ping_interval_secs: float = 30,
                 ping_timeout_secs: float = 30,
                 xpub_address: Optional[str] = None,
                 xsub_address: Optional[str] = None,
                 halt_wait_secs: float = 0.05):

        if ping_interval_secs < 0:
            raise ValueError('Ping interval must be greater or equal to zero, '
                             f'got {ping_interval_secs}')

        if ping_timeout_secs < 0:
            raise ValueError('Ping timeout must be greater or equal to zero, '
                             f'got {ping_timeout_secs}')

        self._ctx = context or zmq.Context.instance()

        self._authkey = (get_authkey() if authkey is None else authkey)

        # Use a child logger with level set to INFO to avoid the
        # authkey being exposed in log files.
        auth_logger = logger.getChild('auth')
        auth_logger.setLevel(logging.INFO)

        self._auth = ThreadAuthenticator(context, log=auth_logger)
        self._auth.start()
        self._auth.configure_plain(domain='*',
                                   passwords={__name__: self._authkey.hex()})

        # Set up bus client (REP) socket.
        self._rep = self._ctx.socket(zmq.REP)
        self._rep.plain_server = True
        try:
            self._rep.bind(address)
        except zmq.ZMQError as ex:
            if ex.errno == zmq.EADDRINUSE:
                raise ConnectionAbortedError('Address already in '
                                             f'use: {address}') from ex
            raise

        self._halt_wait_secs = halt_wait_secs

        self._pub: Optional[zmq.Socket[Any]] = None

        self._tmpdir: Optional[tempfile.TemporaryDirectory[str]] = None

        self._ping_interval_secs = ping_interval_secs
        self._ping_timeout_secs = ping_interval_secs + ping_timeout_secs

        self._connections: Dict[str, float] = {}

        self._xpub_address: str
        self._xsub_address: str

        if xpub_address and xsub_address:
            self._xpub_address = xpub_address
            self._xsub_address = xsub_address
        else:
            self.__setup_xaddress(xpub_address, xsub_address)

    def __setup_xaddress(self,
                         xpub_address: Optional[str],
                         xsub_address: Optional[str]) -> None:
        import socket  # pylint: disable=import-outside-toplevel

        assert not (xpub_address and xsub_address)

        if hasattr(socket, 'AF_UNIX'):
            # pylint: disable-next=consider-using-with
            self._tmpdir = tempfile.TemporaryDirectory(prefix='zmqbus-')
            if not xpub_address:
                self._xpub_address = f'ipc://{self._tmpdir.name}/pub.sock'
            if not xsub_address:
                self._xsub_address = f'ipc://{self._tmpdir.name}/sub.sock'
        else:
            if not xpub_address:
                self._xpub_address = _DEFAULT_TCP_ADDRESS
            if not xsub_address:
                self._xsub_address = _DEFAULT_TCP_ADDRESS

    @property
    def underlying(self) -> zmq.Socket[Any]:
        return self._rep

    @property
    def address(self) -> str:
        return self._rep.get_string(zmq.LAST_ENDPOINT)

    @property
    def authkey(self) -> bytes:
        return self._authkey

    def _publish(self, topic: str, payload: Any = None) -> None:
        assert self._pub is not None
        self._pub.send_string(topic, flags=zmq.SNDMORE)
        self._pub.send_string('', flags=zmq.SNDMORE)
        self._pub.send_pyobj(payload)

    def _get_proxy_thread(self, control_address: str) -> Thread:
        xpub = self._ctx.socket(zmq.XPUB)
        xpub.plain_server = True
        xpub.bind(self._xpub_address)
        self._xpub_address = xpub.get_string(zmq.LAST_ENDPOINT)

        xsub = self._ctx.socket(zmq.XSUB)
        xsub.plain_server = True
        xsub.bind(self._xsub_address)
        self._xsub_address = xsub.get_string(zmq.LAST_ENDPOINT)

        logger.debug('Starting proxy XPUB+XSUB at %r and %r',
                     self._xpub_address, self._xsub_address)

        return Thread(target=_proxy,
                      name=f'bus-proxy-{hex(id(self))}',
                      args=(self._ctx, xpub, xsub, control_address,
                            sys.flags.dev_mode))

    def run(self) -> None:
        control = self._ctx.socket(zmq.PUSH)
        control.bind(f'inproc://zmqbus.control.{id(self)}')

        proxy_t = self._get_proxy_thread(control.get_string(zmq.LAST_ENDPOINT))
        proxy_t.start()

        try:
            self._run()
        finally:
            self._auth.stop()

            self._publish(TOPIC_HALT)

            if self._halt_wait_secs:
                time.sleep(self._halt_wait_secs)

            control.send(b'TERMINATE')

            if proxy_t.is_alive():
                proxy_t.join()

            control.close(self._rep.LINGER)

            if self._pub:
                self._pub.close(self._rep.LINGER)
                self._pub = None

            if self._tmpdir:
                self._tmpdir.cleanup()
                self._tmpdir = None

            self._connections.clear()

    def _run(self) -> None:
        self._pub = self._ctx.socket(zmq.PUB)
        self._pub.set_string(zmq.PLAIN_USERNAME, __name__)
        self._pub.set_string(zmq.PLAIN_PASSWORD, self._authkey.hex())
        self._pub.connect(self._xsub_address)

        timeout = self._ping_interval_secs * 1_000
        last_ping = 0.0

        while True:
            poll_start = time.perf_counter()

            if self._rep.poll(timeout, zmq.POLLIN):
                if not self._handle_request():
                    break

            if not self._ping_interval_secs:
                continue

            now = time.perf_counter()

            if (now - last_ping) > self._ping_interval_secs:
                if self._ping_interval_secs:
                    self._check_connections(now)

                # Broadcast ping.
                self._publish(TOPIC_PING)

                last_ping = now

            timeout -= (now - poll_start) * 1_000
            if timeout < 0:
                timeout = self._ping_interval_secs * 1_000

    def _check_connections(self, now: float) -> None:
        # Check and report stale connections.
        cutoff = now - self._ping_timeout_secs

        for (name, last) in self._connections.copy().items():
            if last < cutoff:
                del self._connections[name]
                self._publish(TOPIC_DEAD, name)
            else:
                self._connections[name] = last

    def _handle_request(self) -> bool:
        assert self._rep is not None
        assert self._pub is not None

        req = self._rep.recv_string()

        if req == 'stop':
            # Stop the bus.
            logger.info('Received bus stop request')
            self._rep.send_string('ok')
            if self._halt_wait_secs:
                time.sleep(self._halt_wait_secs)
            return False

        if req == 'hello':
            self._handle_request_hello()
        elif req == 'pong':
            self._handle_request_pong()
        elif req == 'ping':
            # Bus ping via control connection.
            self._rep.send_string('pong')
        elif req == 'quit':
            self._handle_request_quit()
        else:
            self._handle_unknown_request(req)

        return True

    def _handle_request_hello(self) -> None:
        name = self._rep.recv_string()

        if name in self._connections:
            logger.warning('Duplicate connection %r rejected', name)
            self._rep.send_string('oops', flags=zmq.SNDMORE)
            self._rep.send_string(f'Name {name!r} already taken')
        else:
            self._connections[name] = (time.perf_counter()
                                       + self._ping_interval_secs)

            self._rep.send_string(name, flags=zmq.SNDMORE)
            self._rep.send_string(self._xpub_address, flags=zmq.SNDMORE)
            self._rep.send_string(self._xsub_address)

            self._publish(TOPIC_HELO, name)

    def _handle_request_pong(self) -> None:
        name = self._rep.recv_string()
        if name not in self._connections:
            self._publish(TOPIC_LIVE, name)
        self._connections[name] = time.perf_counter()
        self._rep.send_string('ok')

    def _handle_request_quit(self) -> None:
        name = self._rep.recv_string()
        try:
            del self._connections[name]
        except KeyError:
            logger.error('QUIT from unknown connection %r', name)
            self._rep.send_string('oops')
        else:
            self._publish(TOPIC_QUIT, name)
            self._rep.send_string('ok')

    def _handle_unknown_request(self, req: str) -> None:
        args = []
        while self._rep.rcvmore:
            args.append(self._rep.recv())
        self._rep.send_string('oops')
        logger.error('Unknown request %r %r', req, args)

    def __del__(self) -> None:
        self._auth.stop()
        if self._tmpdir:
            self._tmpdir.cleanup()
            self._tmpdir = None
        self._rep.close()


class Connection:  # pylint: disable=too-many-instance-attributes
    def __init__(self,  # pylint: disable=too-many-arguments
                 address: str,
                 authkey: Optional[bytes] = None,
                 name: Optional[str] = None,
                 context: Optional[zmq.Context[Any]] = None,
                 timeout: float = 5_000,
                 keepalive_secs: float = 0,
                 on_halt: Optional[Callable[['Connection',
                                             Optional[str]], None]] = None):
        if name:
            _assert_valid_connection_name(name)
            self._name = name
        else:
            import uuid  # pylint: disable=import-outside-toplevel
            self._name = f'.{uuid.uuid4()}'

        if keepalive_secs < 0:
            raise ValueError('Keep-alive timeout must be greater than '
                             f'or equal to zero, got {keepalive_secs}')

        self._timeout = timeout

        self._ctx = context or zmq.Context.instance()

        self._authkey_str = (get_authkey() if authkey
                             is None else authkey).hex()

        self._sub: Optional[zmq.Socket[Any]] = None
        self._pub: Optional[zmq.Socket[Any]] = None

        self._on_halt = on_halt

        self._pending: Deque[MESSAGE_FACTORY] = deque()

        self.keepalive_secs = keepalive_secs
        self._last_keepalive: float

        self._subscribe_control = False

        self._req = self._ctx.socket(zmq.REQ)
        self._req.set_string(zmq.PLAIN_USERNAME, __name__)
        self._req.set_string(zmq.PLAIN_PASSWORD, self._authkey_str)

        self._address: Optional[str] = None

        try:
            self.__init_connections(address)
        except (TimeoutError, ConnectionError):
            self.shutdown()
            raise

    def __init_connections(self, address: str) -> None:
        self._req.connect(address)
        self._address = self._req.getsockopt_string(zmq.LAST_ENDPOINT)
        if self._req.poll(timeout=self._timeout, flags=zmq.POLLOUT) == 0:
            raise TimeoutError()
        self._req.send_string('hello', flags=zmq.SNDMORE)
        self._req.send_string(self._name)

        if self._req.poll(timeout=self._timeout, flags=zmq.POLLIN) == 0:
            self._req.close()
            raise ConnectionRefusedError()

        reply = self._req.recv_string()

        if reply == 'oops':
            message = self._req.recv_string()
            self._req.close()
            raise ConnectionAbortedError(message)

        if reply != self._name:
            self._req.close()
            raise ConnectionAbortedError(f'Unexpected hello: {reply!r}')

        # pylint: disable-next=unbalanced-tuple-unpacking
        pub_address = self._req.recv_string()
        assert isinstance(pub_address, str)

        sub_address = self._req.recv_string()
        assert isinstance(sub_address, str)

        # NB: pub connects to XSUB address.
        self._pub = self._ctx.socket(zmq.PUB)
        self._pub.set_string(zmq.PLAIN_USERNAME, __name__)
        self._pub.set_string(zmq.PLAIN_PASSWORD, self._authkey_str)
        assert self._pub is not None
        self._pub.connect(sub_address)

        # NB: sub connects to XPUB address.
        self._sub = self._ctx.socket(zmq.SUB)
        self._sub.set_string(zmq.PLAIN_USERNAME, __name__)
        self._sub.set_string(zmq.PLAIN_PASSWORD, self._authkey_str)
        assert self._sub is not None
        self._sub.connect(pub_address)

        logger.debug('Connected to pub/sub address at [%r, %r]',
                     pub_address, sub_address)

        self._sub.setsockopt_string(zmq.SUBSCRIBE, TOPIC_PING)
        self._sub.setsockopt_string(zmq.SUBSCRIBE, TOPIC_HALT)
        self._sub.setsockopt_string(zmq.SUBSCRIBE, f'@{self._name}\n')

        self._last_keepalive = time.perf_counter()

        self._endpoints: Dict[str, Callable[['Connection'], None]] = {}
        self._cli_responses: Dict[int, Any] = {}
        self._cli_requests: Dict[int, Tuple[str, str]] = {}
        self._req_id = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def address(self) -> Optional[str]:
        return self._address

    @property
    def underlying(self) -> zmq.Socket[Any]:
        return self._req

    def set_on_halt(self,
                    callback: Optional[Callable[['Connection', Optional[str]],
                                                None]]) -> None:
        self._on_halt = callback

    def is_alive(self) -> bool:
        if not self._pub:
            return False

        if not self.keepalive_secs:
            return True

        now = time.perf_counter()
        if (now - self._last_keepalive) <= self.keepalive_secs:
            return True

        if self._req.poll(timeout=self._timeout, flags=zmq.POLLOUT) == 0:
            return False

        self._req.send_string('ping')
        is_alive = self._req.recv_string() == 'pong'

        if is_alive:
            self._last_keepalive = now

        return is_alive

    def subscribe(self, topic: str) -> None:
        _assert_connected(self._sub)
        _assert_valid_user_topic(topic)
        assert self._sub
        self._sub.setsockopt_string(zmq.SUBSCRIBE, f'*{topic}')

    def unsubscribe(self, topic: str) -> None:
        _assert_connected(self._sub)
        _assert_valid_user_topic(topic)
        assert self._sub
        self._sub.setsockopt_string(zmq.UNSUBSCRIBE, f'*{topic}')

    def subscribe_control(self, enable: bool) -> None:
        _assert_connected(self._sub)
        assert self._sub
        self._subscribe_control = enable
        if enable:
            self._sub.setsockopt_string(zmq.SUBSCRIBE, '_')
        else:
            self._sub.setsockopt_string(zmq.UNSUBSCRIBE, '_')

    def send(self, topic: str,
             payload: Any = None,
             timeout: Optional[float] = None,
             to: Union[str, Sequence[str], None] = None) -> None:
        _assert_valid_user_topic(topic)
        self._send(topic, payload, timeout, to)

    def _send(self, topic: str,
              payload: Any = None,
              timeout: Optional[float] = None,
              to: Union[str, Sequence[str], None] = None) -> None:
        _assert_connected(self._pub)
        assert self._pub

        if (timeout is not None
                and self._pub.poll(timeout=timeout, flags=zmq.POLLOUT) == 0):
            raise TimeoutError()

        if to is None:
            self._pub.send_string(f'*{topic}', flags=zmq.SNDMORE)
            self._pub.send_string(self._name, flags=zmq.SNDMORE)
            self._pub.send_pyobj(payload)
        else:
            if isinstance(to, str):
                to = (to,)
            for rcpt in to:
                self._pub.send_string(f'@{rcpt}\n{topic}', flags=zmq.SNDMORE)
                self._pub.send_string(self._name, flags=zmq.SNDMORE)
                self._pub.send_pyobj(payload)
        try:
            self.poll(0)
        except TimeoutError:
            pass

    def recv(self, timeout: Optional[float] = None) -> Message:
        try:
            return self._pending.popleft()
        except IndexError:
            pass
        self.poll(timeout)
        return self._pending.popleft()

    def _enqueue(self,
                 sender: Optional[str],
                 to: Union[str, Sequence[str], None],
                 topic: str,
                 payload: Any) -> None:
        self._pending.append(MESSAGE_FACTORY(sender=sender,
                                             to=to,
                                             topic=topic,
                                             payload=payload))

    def _send_response(self,
                       endpoint: str,
                       sender: str,
                       payload: Tuple[int,
                                      Tuple[int, ...],
                                      Dict[str, Any]]) -> None:
        try:
            callback = self._endpoints[endpoint]
        except KeyError:
            logger.error('No such endpoint %r', endpoint)
            return

        (req_id, args, kwargs) = payload

        try:
            res = callback(self, *args, **kwargs)
        except Exception:  # pylint: disable=broad-exception-caught
            logger.exception("Failed '%s.%s' call", self._name, endpoint)
            return

        self._send(f'<\n{endpoint}', (req_id, res), to=sender)

    def _register_response(self,
                           endpoint: str,
                           sender: str,
                           payload: Tuple[int, Any]) -> None:
        (req_id, res) = payload

        if req_id not in self._cli_requests:
            logger.error("Invalid request #%d for '%s.%s' from %r",
                         req_id, sender, endpoint, self._name)
            return

        if self._cli_requests[req_id] != (sender, endpoint):
            logger.error("Unexpected response for '%s.%s' #%d from %r",
                         self._name, endpoint, req_id, sender)
            return

        self._cli_responses[req_id] = res

        del self._cli_requests[req_id]

    # pylint: disable-next=too-many-branches, too-many-statements
    def poll(self,
             timeout: Optional[float] = None,
             messages: bool = True,
             responses: bool = False) -> None:

        if timeout is None and not (messages or responses):
            raise RuntimeError('Infinite timeout needs to '
                               'pull messages or responses')

        while True:
            _assert_connected(self._sub)
            assert self._sub

            poll_start_time = time.perf_counter()
            if self._sub.poll(timeout=timeout) == 0:
                raise TimeoutError()

            topic = self._sub.recv_string()
            sender = self._sub.recv_string() or None
            payload = self._sub.recv_pyobj()

            self._last_keepalive = time.perf_counter()

            if topic[0] == '*' and sender != self._name:
                self._enqueue(sender, None, topic[1:], payload)
                break

            if topic[0] == '@':
                assert sender is not None, 'Unicast message must have a sender'
                (to, topic) = topic[1:].split(sep='\n', maxsplit=1)
                if topic[0] == '>':
                    # A request.
                    assert topic[1] == '\n'
                    if to == self._name:
                        self._send_response(topic[2:], sender, payload)
                elif topic[0] == '<':
                    # A response.
                    assert topic[1] == '\n'
                    if to == self._name:
                        self._register_response(topic[2:], sender, payload)
                        if responses:
                            break
                else:
                    self._enqueue(sender, to, topic, payload)
                    if messages:
                        break
                    topic = '*'  # Fake message to self to avoid extra
                                 # processing (see below).

            if topic == TOPIC_PING:
                self._send_pong()
                if self._subscribe_control:
                    self._enqueue(sender, None, topic, payload)
                    break
            elif topic == TOPIC_HALT:
                self._cleanup()
                self._req.close()
                if self._on_halt:
                    self._on_halt(self, sender)
            elif topic[0] == '_':
                if not _is_control_topic(topic):
                    logger.error('Got an invalid control topic: %r', topic)
                elif self._subscribe_control:
                    self._enqueue(sender, None, topic, payload)
                    break
            elif topic[0] not in '*<>':  # Check needed due to message to self.
                logger.error('Invalid bus topic %r', topic)

            if timeout is not None:
                timeout = timeout - int(1_000
                                        * (time.perf_counter()
                                           - poll_start_time))
                if timeout < 0:
                    raise TimeoutError()

    def _send_pong(self) -> None:
        self._req.send_string('pong', flags=zmq.SNDMORE)
        self._req.send_string(self._name)
        res = self._req.recv_string()
        assert res == 'ok', f"Expecting 'ok', got {res!r}"

    def sleep(self, secs: float) -> None:
        if secs < 0:
            raise ValueError('Sleep time must be greater or equal to zero, '
                             f'got {secs!r}')

        while secs > 0:
            poll_start = time.perf_counter()
            try:
                self.poll(secs * 1_000)
            except TimeoutError:
                break
            secs -= time.perf_counter() - poll_start

    def add_endpoint(self, name: str,
                     callback: Callable[..., Any]) -> None:
        self._endpoints[name] = callback

    def remove_endpoint(self, name: str) -> None:
        del self._endpoints[name]

    def request(self, name: str, endpoint: str,
                *args: Any, **kwargs: Any) -> int:
        self._req_id += 1
        self._send(f'>\n{endpoint}', (self._req_id, args, kwargs), to=name)
        self._cli_requests[self._req_id] = (name, endpoint)
        return self._req_id

    def _response(self, req_id: int) -> Any:
        res = self._cli_responses[req_id]
        del self._cli_responses[req_id]
        return res

    def response(self, req_id: int,
                 timeout: Union[float, Any, None] = ...) -> Any:
        if req_id not in self._cli_requests:
            raise LookupError(f'No such request #{req_id}')

        try:
            return self._response(req_id)
        except KeyError:
            pass

        if timeout == ...:
            timeout = self._timeout

        while True:
            poll_start_time = time.perf_counter()

            self.poll(timeout, messages=False, responses=True)
            try:
                return self._response(req_id)
            except KeyError:
                pass

            if timeout is not None:
                timeout = timeout - int(1_000
                                        * (time.perf_counter()
                                           - poll_start_time))
                if timeout < 0:
                    raise TimeoutError()

    def _cleanup(self) -> None:
        assert self._pub
        assert self._sub
        self._pending.clear()
        self._pub.close(self._req.LINGER)
        self._sub.close(self._req.LINGER)
        self._pub = self._sub = None

    def __enter__(self) -> 'Connection':
        return self

    def __exit__(self,  # type: ignore[no-untyped-def]
                 exc_type, exc_value, traceback) -> None:
        self.shutdown()

    def shutdown(self) -> None:
        if not self._req.closed:
            if self._pub:
                if self._req.poll(timeout=self._timeout, flags=zmq.POLLOUT):
                    self._req.send_string('quit', flags=zmq.SNDMORE)
                    self._req.send_string(self._name)
                    if self._req.poll(timeout=self._timeout, flags=zmq.POLLIN):
                        self._req.recv_string()
                self._cleanup()
            self._req.close()

    def __repr__(self) -> str:
        return (f'<{self.__module__}.{self.__class__.__name__}'
                f'({self._name!r}) '
                f'at {hex(id(self))}>')

    def __del__(self) -> None:
        if not self._req.closed:
            warnings.warn(f'Orphaned connection {self}',
                          ResourceWarning, stacklevel=2)
            self.shutdown()
