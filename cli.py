from argparse import ArgumentParser

__all__ = ("parse_args",)

_parser = ArgumentParser()
_parser.add_argument("file", nargs="?", default="openapi.yaml")


def parse_args():
    return _parser.parse_args()
