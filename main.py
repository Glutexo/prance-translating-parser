from cli import parse_args
from log import configure_logging
from log import get_logger


logger = get_logger(__name__)


def _main(args):
    logger.info("Parsing file %s", args.file)

    parser = args.parser(args.file)
    parser.parse()
    output = args.output_format(parser.specification)
    print(output)


if __name__ == "__main__":
    args = parse_args()

    configure_logging(args.verbose)
    logger.debug("Arguments: %s", vars(args))
    _main(args)
