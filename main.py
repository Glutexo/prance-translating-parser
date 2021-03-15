from prance import ResolvingParser
from yaml import dump

from cli import parse_args
from log import configure_logging
from log import get_logger
from parser import TranslatingParser


logger = get_logger(__name__)


def _main(args):
    logger.info("Parsing file %s", args.file)

    # parser = ResolvingParser(args.file)
    parser = TranslatingParser(args.file)
    parser.parse()
    output = dump(parser.specification)
    print(output)


if __name__ == "__main__":
    configure_logging()

    args = parse_args()
    logger.debug("Arguments: %s", vars(args))
    _main(args)
