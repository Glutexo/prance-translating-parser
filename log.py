from logging import basicConfig
from logging import DEBUG
from logging import getLogger
from logging import INFO

__all__ = ("configure_logging", "get_logger")


def configure_logging(verbose):
    level = DEBUG if verbose else INFO
    basicConfig(level=level)


def get_logger(name):
    return getLogger(name)
