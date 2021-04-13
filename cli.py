from argparse import ArgumentParser
from importlib import import_module
from json import dumps as json_dumps
from logging import DEBUG
from logging import INFO
from yaml import dump as yaml_dump

__all__ = ("parse_args",)

_parser = ArgumentParser()
_parser.add_argument(
    "file", nargs="?", default="specs/openapi.spec.yaml", help="OpenAPI specification file. Default: %(default)s"
)


_FORMATTERS = {"json": json_dumps, "yaml": yaml_dump}


def _get_parser(name):
    module_name, class_name = name.split(".")
    module = import_module(module_name)
    return getattr(module, class_name)


def _get_formatter(name):
    try:
        return _FORMATTERS[name]
    except KeyError:
        raise ValueError()


_parser.add_argument(
    "--parser", "-p", type=_get_parser, default="parser.TranslatingParser", help="Parser class. Default: %(default)s"
)
_parser.add_argument(
    "--output-format",
    "-f",
    type=_get_formatter,
    default="json",
    help="Output format: json or yaml. Default: %(default)s",
)
_parser.add_argument(
    "--verbose",
    "-v",
    action="store_const",
    const=DEBUG,
    default=INFO,
    help="Verbose output",
)


def parse_args():
    return _parser.parse_args()
