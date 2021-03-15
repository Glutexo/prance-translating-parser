from logging import basicConfig, DEBUG, getLogger

from prance import ResolvingParser
from yaml import dump

from parser import TranslatingParser
from cli import parse_args


def _configure_logging():
    basicConfig(level=DEBUG)


def _main(args):
    # parser = ResolvingParser(args.file)
    parser = TranslatingParser(args.file)
    parser.parse()
    output = dump(parser.specification)
    print(output)


if __name__ == "__main__":
    _configure_logging()

    args = parse_args()
    _main(args)
