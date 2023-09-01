import sys
import argparse
import logging
import pickle

from zmqbus import Bus


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--no-clobber',
                        action='store_true',
                        help='do overwrite output file')
    parser.add_argument('-i', '--ping-interval',
                        default=60,
                        type=int,
                        help='ping interval in seconds')
    parser.add_argument('-T', '--ping-timeout',
                        default=30,
                        type=int,
                        help='ping timeout in seconds')
    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help='verbose logging')
    parser.add_argument('-a', '--address',
                        default='tcp://127.0.0.1:*',
                        help='bus address to bind to (default: %(default)s)')
    parser.add_argument('output',
                        help='file to save pickled (address, authkey) tuple')
    return parser.parse_args()


def init_logging(level: int) -> None:
    try:
        # pylint: disable=import-outside-toplevel
        import chromalog  # type: ignore[import]
        chromalog.basicConfig(
            level=level,
            format='%(asctime)s [%(name)s]: %(message)s')
    except ModuleNotFoundError:
        logging.basicConfig(
            level=level,
            format='%(asctime)s %(levelname).1s [%(name)s]: %(message)s')


def main() -> None:
    args = get_args()

    if args.verbose > 1:
        init_logging(logging.DEBUG)
    elif args.verbose:
        init_logging(logging.INFO)
    else:
        init_logging(logging.WARNING)

    bus = Bus(args.address,
              ping_interval_secs=args.ping_interval,
              ping_timeout_secs=args.ping_timeout)

    try:
        with open(args.output, 'xb' if args.no_clobber else 'wb') as fd:
            pickle.dump((bus.address, bus.authkey), fd)
    except FileExistsError:
        sys.exit(f'{sys.argv[0]}: File already exists: {args.output}')

    try:
        bus.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
