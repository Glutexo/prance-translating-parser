from argparse import ArgumentParser
from importlib import import_module


__all__ = ("parse_args",)

_parser = ArgumentParser()
_parser.add_argument("file", nargs="?", default="openapi.yaml")


def _get_parser(name):
    module_name, class_name = name.split(".")
    module = import_module(module_name)
    return getattr(module, class_name)


_parser.add_argument("--parser", type=_get_parser, default="parser.TranslatingParser")


def parse_args():
    return _parser.parse_args()
