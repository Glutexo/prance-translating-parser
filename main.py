from yaml import dump

from translating_parser import TranslatingParser

SPECIFICATION_FILE = "openapi.yaml"


def main():
    parser = TranslatingParser(SPECIFICATION_FILE)
    parser.parse()
    output = dump(parser.specification)
    print(output)


if __name__ == "__main__":
    main()
