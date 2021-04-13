from logging import basicConfig
from logging import getLogger

__all__ = ("configure_logging", "get_logger")


def configure_logging(level):
    basicConfig(level=level)


def get_logger(name):
    return getLogger(name)
