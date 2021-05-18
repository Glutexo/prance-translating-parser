# Translating Parser for Prance #

This is a Translating parser for [Prance], a library processing and validating [OpenAPI] specification files. It targets use cases when a specification spans across multiple files that need to be compiled to a single document, but inlining of the references objects is not desired or event possible.

Frameworks like [Connexion] unfortunately do not support file references in the specification and [Prance] can be used to alleviate this missing features. Inlining can result in excessive memory usage and also can make code generators not work properly if they rely on properly reused component schema definitions. If the specification contains a recursive object definition, inlining would result in an infinite loop.

The original motivation is to make [Red Hat Insights Host Inventory](https://github.com/RedHatInsights/insights-host-inventory) work with recursive objects [defined](https://github.com/RedHatInsights/inventory-schemas/blob/master/schemas/system_profile/v1.yaml#L5) in a schema that is incorporated to the OpenAPI specification of the application.

## Development environment ##

1. Get [Pipenv].
  ```sh
  $ pip install pipenv
  ```
2. Install requirements.
  ```sh
  $ pipenv sync
  ```
3. ???
4. Profit.

## Usage ##

The core here is the [TranslatingParser](translating_parser/parser.py#L6) that can be used instead of Prance’s _ResolvingParser_ to process the specification.

```python
from translating_parser.parser import TranslatingParser
parser = TranslatingParser("openapi.spec.yaml")
parser.parse()
print(parser.specification)
```

There is a companion CLI script [main.py](main.py) that can be used to test and debug the parser.

```
usage: main.py [-h] [--parser PARSER] [--output-format OUTPUT_FORMAT]
               [--verbose]
               [file]

positional arguments:
  file                  OpenAPI specification file. Default:
                        specs/openapi.spec.yaml

optional arguments:
  -h, --help            show this help message and exit
  --parser PARSER, -p PARSER
                        Parser class. Default:
                        translating_parser.parser.TranslatingParser
  --output-format OUTPUT_FORMAT, -f OUTPUT_FORMAT
                        Output format: json or yaml. Default: json
  --verbose, -v         Verbose output
```

To use the original Resolving Parser, use `-p prance.ResolvingParser`.

## Testing ##

```sh
$ PYTHONPATH=. pipenv run pytest
```

## License ##

[MIT](LICENSE.txt), to be compatible with [Prance].

[Prance]: https://github.com/RonnyPfannschmidt/prance/
[OpenAPI]: https://www.openapis.org/
[Connexion]: https://github.com/zalando/connexion
[Pipenv]: https://github.com/pypa/pipenv