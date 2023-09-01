A bus implementation for Python using ZeroMQ
============================================

_zmqbus_ is package for Python that allows for communication between
collaborative processes in a bus fashion on the same machine. The bus
allows connected parties to subscribe and publish messages, with the
ability to direct messages to specific connections. It also supports
request/response messages for remote procedure calls (RPC), where
connections can send request and receive responses from well-known
addresses registered in the bus.

**IMPORTANT**: _zmqbus_ is still beta software. Use in production is
strongly discouraged.


Requirements
------------

- Python 3.7 or above
- pyzmq


Installation
------------

You can install _zmqbus_ using pip:

    pip install zmqbus


Usage
-----

See [demo.py](demo.py) for usage examples.


License
-------

See the [LICENSE.txt file](LICENSE.txt) for details.


Bug? Critics? Suggestions?
--------------------------

Go to https://github.com/flaviovs/zmqbus
