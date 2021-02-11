from yaml import dump

from prance import ResolvingParser

SPECIFICATION_FILE = "openapi.yaml"


def main():
    parser = ResolvingParser(SPECIFICATION_FILE)
    parser.parse()
    output = dump(parser.specification)
    print(output)


if __name__ == "__main__":
    main()
