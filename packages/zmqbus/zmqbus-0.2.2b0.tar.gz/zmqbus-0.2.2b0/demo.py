# mypy: disable-error-code="no-untyped-def,no-untyped-call,import"
import sys
import argparse
import logging
import pickle
import random
import time
from threading import Thread, current_thread, enumerate as t_enumerate

from zmqbus import Bus, Connection, halt, Message
from zmqbus.device import (Device, Pulse, Scheduler, ScheduledMessage,
                           Clock, PerfMeter, Dispatcher, Random, Echo)
from zmqbus.debug import Sniffer, ControlSniffer, PulseTracker

try:
    import chromalog
    chromalog.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(threadName)s: %(message)s')
except ModuleNotFoundError:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname).1s %(threadName)s: %(message)s')

logger = logging.getLogger(__name__)


TOPIC_ECHO = 'ECHO'


class DemoDispatcher(Dispatcher):
    def __init__(self):
        super().__init__('DemoDispatcher')
        self._busy_workers = set()

    def _busy_worker_logger(self, conn: Connection, msg: Message):
        logger.info('%r has gone busy for %.1f seconds',
                    msg.sender, msg.payload)
        self._busy_workers.add(msg.sender)

    def _free_worker_logger(self, conn: Connection, msg: Message):
        logger.info('%r has finished its %.1f seconds job',
                    msg.sender, msg.payload)
        self._busy_workers.discard(msg.sender)

    def _perf_meter_logger(self, conn: Connection, msg: Message):
        logger.info('Average latency %.2f ms measured by %r from '
                    '%r from the last %d messages',
                    msg.payload.avg_ms, msg.sender, msg.payload.clock,
                    msg.payload.samples)

    def _random_logger(self, conn: Connection, msg: Message):
        logger.info('Got a random number: %f', msg.payload)
        if msg.payload < 0.03:
            logger.warning('Got a low random number -- removing random logger')
            self.remove_callback('random', self._random_logger)

    def _init_callbacks(self):
        self.add_callback('PerfMeter', self._perf_meter_logger)
        self.add_callback('worker.busy', self._busy_worker_logger)
        self.add_callback('worker.free', self._free_worker_logger)
        self.add_callback('random', self._random_logger)

    def init(self, conn):
        super().init(conn)
        self._busy_workers.clear()

    def done(self, conn):
        super().done(conn)
        logger.info('Finished')
        if self._busy_workers:
            logger.warning('The following workers are still busy: %s',
                           ', '.join([repr(w) for w in self._busy_workers]))


def worker_main(address, authkey, me, delay_secs, workers):
    prng = random.Random()

    conn = Connection(address, authkey=authkey, name=f'Worker{me}')
    conn.subscribe('workers')

    def do_something(lengthy):
        if lengthy:
            secs = delay_secs + (prng.random() * delay_secs)
            conn.send('worker.busy', payload=secs)
            logger.info('Going very busy for %.1f seconds', secs)
        else:
            secs = 0.5 + prng.random()
        # Note: we don't call conn.sleep(), because we hant to
        # simulate a busy task that does not check connection traffic.
        time.sleep(secs)
        if lengthy:
            conn.send('worker.free', payload=secs)
            logger.info('Back to work after being busy for %d seconds',
                        secs)

    prob = 0.1 / workers

    logger.info('Starting with %.2f probability of something happening', prob)

    try:
        while conn.is_alive():
            try:
                msg = conn.recv(delay_secs * 0.5)
            except TimeoutError:
                msg = None

            if msg:
                if msg.to is None:
                    to = 'all workers'
                elif msg.to == conn.name:
                    to = 'me'
                else:
                    to = repr(msg.to)

                if msg.topic == TOPIC_ECHO:
                    logger.info('Got echo response for request sent %.1fs ago',
                                time.time() - msg.payload)
                else:
                    logger.info('Got %r from %r sent to %s',
                                msg.payload, msg.sender, to)

            if workers > 1 and prng.random() < prob:
                logger.info('Sending message to all workers')
                conn.send('workers', "Let's work")

            if prng.random() < prob:
                logger.info('Sending echo request')
                conn.send(TOPIC_ECHO, time.time())

            do_something(lengthy=prng.random() < prob)

            if workers > 1 and prng.random() < prob:
                while True:
                    peer = prng.randint(0, workers - 1)
                    if peer != me:
                        break
                logger.info('Saying hello to Worker%d', peer)
                conn.send('workers', 'hello', to=f'Worker{peer}')

            conn.sleep(1 + (prng.random() * 2))
    except BrokenPipeError:
        pass
    finally:
        conn.shutdown()

    logger.info('Finished')


def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    group = parser.add_argument_group('bus options')
    group.add_argument('-a', '--address',
                       help='the bus address')
    group.add_argument('-l', '--load',
                       metavar='FILE',
                       help='load pickled (address, authkey) from %(metavar)s')
    group.add_argument('--ping-interval',
                       type=int,
                       default=10,
                       help='bus ping interval in seconds')
    group.add_argument('--ping-timeout',
                       type=int,
                       default=10,
                       help='bus ping timeout in seconds')

    group = parser.add_argument_group('pulse threads options')
    group.add_argument('-P', '--pulses',
                       type=int,
                       default=3,
                       help='number of pulse threads')
    group.add_argument('--pulse-wait',
                       type=int,
                       default=20,
                       help='wait time between pulses')
    group.add_argument('--pulse-jitter',
                       type=float,
                       default=0.20,
                       help='pulse jitter')

    group = parser.add_argument_group('worker threads options')
    group.add_argument('-w', '--workers',
                       type=int,
                       default=3,
                       help='number of worker threads')

    group = parser.add_argument_group('scheduler threads options')
    group.add_argument('-S', '--schedulers',
                       type=int,
                       default=3,
                       help='number of messages to schedule')
    group.add_argument('--scheduler-messages',
                       type=int,
                       default=20,
                       help='number of messages to schedule')

    group = parser.add_argument_group('demo options')
    group.add_argument('-s', '--speed',
                       default='auto',
                       choices=('auto', 'slower', 'slow',
                                'normal', 'fast', 'faster'),
                       help='demo speed')
    group.add_argument('--no-clock',
                       action='store_true',
                       help='do not start a clock thread')
    group.add_argument('--no-random',
                       action='store_true',
                       help='do not start a random thread')

    return parser.parse_args()


def get_random_workers(workers):
    return random.sample([f'Worker{i}' for i in range(workers)],
                         random.randint(1, workers))


def wait_all_threads(timeout):
    while True:
        active = set(t for t in t_enumerate() if t is not current_thread())
        for t in active.copy():
            t.join(timeout=timeout)
            if not t.is_alive():
                active.remove(t)
        if not active:
            break
        logger.warning('The following threads are still alive: %s',
                       ', '.join([repr(a.name) for a in active]))


def main():
    args = get_args()

    speed_mult: float
    if args.speed == 'slower':
        speed_mult = 10
    elif args.speed == 'slow':
        speed_mult = 4
    elif args.speed == 'normal':
        speed_mult = 1
    elif args.speed == 'fast':
        speed_mult = 0.2
    elif args.speed == 'faster':
        speed_mult = 0.05
    else:
        assert args.speed == 'auto'
        speed_mult = (args.workers / 3) * (args.pulses / 3)

    threads = []

    if args.load and args.address:
        sys.exit('Cannot use --load and --address at the same time')

    if args.load:
        with open(args.load, 'rb') as fd:
            (address, authkey) = pickle.load(fd)
    else:
        # Create the bus in the main thread so we can get its address.
        bus = Bus(args.address or 'tcp://127.0.0.1:*',
                  ping_interval_secs=args.ping_interval,
                  ping_timeout_secs=args.ping_timeout)
        threads.append(Thread(name='Bus', target=bus.run))
        address = bus.address
        authkey = bus.authkey

    dev: Device

    dev = DemoDispatcher()
    threads.append(Thread(name=dev.name, target=dev, args=(address, authkey)))

    if not args.no_random:
        dev = Random(name='Random', topic='random', wait_secs=10 * speed_mult)
        threads.append(Thread(name=dev.name, target=dev,
                              args=(address, authkey)))

    if not args.no_clock:
        dev = Clock(name='Clock')
        threads.append(Thread(name=dev.name, target=dev,
                              args=(address, authkey)))

        dev = PerfMeter(name='PerfMeter', sender='Clock', )
        threads.append(Thread(name=dev.name, target=dev,
                              args=(address, authkey)))

    dev = Sniffer(name='Sniffer')
    threads.append(Thread(name=dev.name, target=dev,
                          args=(address, authkey)))

    dev = ControlSniffer(name='ControlSniffer')
    threads.append(Thread(name=dev.name, target=dev,
                          args=(address, authkey)))

    dev = Echo(name='Echo', topic=TOPIC_ECHO)
    threads.append(Thread(name=dev.name, target=dev,
                          args=(address, authkey)))

    if args.pulses:
        dev = PulseTracker(name='PulseTracker', topic='Pulse')
        threads.append(Thread(name=dev.name, target=dev,
                              args=(address, authkey)))

        for i in range(args.pulses):
            dev = Pulse(name=f'Pulse{i}',
                        wait_secs=args.pulse_wait * speed_mult,
                        jitter=args.pulse_jitter)
            threads.append(Thread(name=dev.name, target=dev,
                                  args=(address, authkey)))

    for i in range(args.schedulers):
        messages = []

        # We want to stop after roughly 2 minutes.
        delay = 120 / args.scheduler_messages

        # Probability to send a message to some worker.
        try:
            prob = 0.5 / (args.workers - 1)
        except ZeroDivisionError:
            prob = 0
        for j in range(args.scheduler_messages):
            messages.append(
                ScheduledMessage(secs=(delay
                                       * (0.5 + random.random())),
                                 topic='scheduler',
                                 payload=f'Scheduled message #{j}'))
            if random.random() < prob:
                messages.append(
                    ScheduledMessage(secs=(delay * random.random()),
                                     topic='workers',
                                     payload='Hi there',
                                     to=get_random_workers(args.workers)))

        if i == 0:
            # First schedule will have one extra message, and halt the
            # bus.
            messages.append(
                ScheduledMessage(secs=delay,
                                 topic='schedule',
                                 payload='Halting the bus'))
            after = lambda conn: halt(conn.address, authkey)  # noqa: E731
        else:
            after = None

        dev = Scheduler(
            name=f'Scheduler{i}',
            before=lambda conn: conn.send('scheduler', f'Before scheduler{i}'),
            messages=messages.copy(),
            after=after
        )
        threads.append(Thread(name=f'Scheduler{i}',
                              target=dev, args=(address, authkey)))

    for i in range(args.workers):
        threads.append(Thread(name=f'Worker{i}',
                              target=worker_main,
                              args=(address,
                                    authkey,
                                    i,
                                    args.ping_timeout,
                                    args.workers)))

    for t in threads:
        t.start()
        if args.speed != 'faster':
            time.sleep(1 * speed_mult)

    conn = Connection(address, name='demo', authkey=authkey)
    try:
        while conn.is_alive():
            conn.poll(None)
    except BrokenPipeError:
        pass
    except KeyboardInterrupt:
        halt(address, authkey, timeout_ms=args.ping_timeout * 2 * 1_000)
    finally:
        wait_all_threads(args.ping_timeout * 2)

    logger.info('Demo finished')


if __name__ == '__main__':
    sys.exit(main())
