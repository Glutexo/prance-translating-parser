from logging import basicConfig, DEBUG, getLogger

from prance import ResolvingParser
from yaml import dump

from parser import TranslatingParser

SPECIFICATION_FILE = "openapi.yaml"


def _configure_logging():
    basicConfig(level=DEBUG)


def _main():
    # parser = ResolvingParser(SPECIFICATION_FILE)
    parser = TranslatingParser(SPECIFICATION_FILE)
    parser.parse()
    output = dump(parser.specification)
    print(output)


if __name__ == "__main__":
    _configure_logging()
    _main()
