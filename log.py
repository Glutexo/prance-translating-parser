from logging import basicConfig, DEBUG, getLogger

__all__ = ("configure_logging", "get_logger")


def configure_logging(args):
    basicConfig(level=args.verbose)


def get_logger(name):
    return getLogger(name)
