import logging
from typing import Optional, Dict

import zmqbus
from zmqbus.device import Device, Pulse, DeviceParams

logger = logging.getLogger(__name__)


class Sniffer(Device):
    def run(self, conn: zmqbus.Connection) -> None:
        conn.subscribe('')
        while conn.is_alive():
            try:
                msg = conn.recv()
            except BrokenPipeError:
                break
            logger.info('< sender=%r topic=%r payload=%r',
                        msg.sender, msg.topic, msg.payload)
        logger.debug('%r exiting', self.name)


class ControlSniffer(Device):

    def _on_halt(self, _conn: zmqbus.Connection,
                 _sender: Optional[str]) -> None:
        logger.warning('Bus HALTED')

    def run(self, conn: zmqbus.Connection) -> None:
        conn.set_on_halt(self._on_halt)
        conn.subscribe_control(True)

        while conn.is_alive():
            try:
                msg = conn.recv()
            except BrokenPipeError:
                break

            if msg.topic == zmqbus.TOPIC_HELO:
                logger.info('%r connected to the bus', msg.payload)
            elif msg.topic == zmqbus.TOPIC_DEAD:
                logger.warning('%r is dead', msg.payload)
            elif msg.topic == zmqbus.TOPIC_LIVE:
                logger.info('%r is alive', msg.payload)
            elif msg.topic == zmqbus.TOPIC_QUIT:
                logger.warning('%r left the bus', msg.payload)
            elif msg.topic == zmqbus.TOPIC_PING:
                logger.info('PING')
            else:
                logger.error('Unexpected message: %r', msg)

        logger.debug('%r exiting', self.name)


class PulseTracker(Device):
    def __init__(self,
                 name: Optional[str] = None,
                 topic: Optional[str] = None,
                 params: Optional[DeviceParams] = None):
        super().__init__(name, params)
        self._topic = topic or Pulse.get_default_name()

    def run(self, conn: zmqbus.Connection) -> None:
        conn.subscribe(self._topic)

        last: Dict[str, float] = {}

        while conn.is_alive():
            try:
                msg = conn.recv()
            except BrokenPipeError:
                break

            if not msg.sender:
                continue

            if msg.sender in last:
                delta = msg.payload - last[msg.sender]
                if delta != 1:
                    logger.error('Expecting %d, from %r got %r',
                                 last[msg.sender] + 1, msg.sender, msg.payload)
            last[msg.sender] = msg.payload
