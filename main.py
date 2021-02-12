from prance import ResolvingParser
from yaml import dump

from parser import TranslatingParser

SPECIFICATION_FILE = "openapi.yaml"


def main():
    # parser = ResolvingParser(SPECIFICATION_FILE)
    parser = TranslatingParser(SPECIFICATION_FILE)
    parser.parse()
    output = dump(parser.specification)
    print(output)


if __name__ == "__main__":
    main()
