from argparse import ArgumentParser
from importlib import import_module
from logging import DEBUG
from logging import INFO

__all__ = ("parse_args",)

_parser = ArgumentParser()
_parser.add_argument(
    "file", nargs="?", default="specs/openapi.spec.yaml", help="OpenAPI specification file. Default: %(default)s"
)


_FORMATTERS = {"json": ("json", "dumps"), "yaml": ("yaml", "dump")}


def _get_parser(name):
    module_name, class_name = name.rsplit(".", 1)
    module = import_module(module_name)
    return getattr(module, class_name)


def _get_formatter(name):
    try:
        module_name, function_name = _FORMATTERS[name]
    except KeyError:
        raise ValueError()

    module = import_module(module_name)
    return getattr(module, function_name)


_parser.add_argument(
    "--parser", "-p", type=_get_parser, default="translating_parser.parser.TranslatingParser", help="Parser class. Default: %(default)s"
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
