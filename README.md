# Translating Parser for Prance #

This is a Translating parser for [Prance], a library processing and validating [OpenAPI] specification files. It targets use cases when a specification spans across multiple files that need to be compiled to a single document, but inlining of the references objects is not desired or event possible.

Frameworks like [Connexion] unfortunately do not support file references in the specification and [Prance] can be used to alleviate this missing features. Inlining can result in excessive memory usage and also can make code generators not work properly if they rely on properly reused component schema definitions. If the specification contains a recursive object definition, inlining would result in an infinite loop.

The original motivation is to make [Red Hat Insights Host Inventory](https://github.com/RedHatInsights/insights-host-inventory) work with recursive objects [defined](https://github.com/RedHatInsights/inventory-schemas/blob/master/schemas/system_profile/v1.yaml#L5) in a schema that is incorporated to the OpenAPI specification of the application.

## Examples ##

Imagine having an OpenAPI specification file that references an object from an external file. The current Resolving Parser would inline all of those, even if they were pointing to the same object, using a lot of memory. If the target object would recursively reference itself, such inlining wouldn’t be even possible.

_openapi.spec.yaml_
```yaml
---
openapi: 3.0.3
info:
  title: Example specification for the translating parser
  version: 0.0.0
paths:
  /hosts:
    get:
      responses:
        default:
          description: >-
            An operation with a referenced schema.
          content:
            application/json:
              schema:
                $ref: 'schemas.yaml#/$defs/Response'
```

_schemas.spec.yaml_
```yaml
---
$defs:
  Response:
    type: object
    properties:
      simple:
        $ref: "#/$defs/Simple"
      nested:
        $ref: "#/$defs/Nested"
  Simple:
    type: object
  Nested:
    type: object
    additionalProperties:
      $ref: "#/$defs/Nested"
```

### Resolving Parser result ###

```yaml
---
openapi: 3.0.3
info:
  title: Example specification for the translating parser
  version: 0.0.0
paths:
  /hosts:
    get:
      responses:
        default:
          description: >-
            An operation with a referenced schema.
          content:
            application/json:
              schema:
                type: object
                properties:
                  simple:
                    type: object
                  nested:
                    type: object
                    additionalProperties:
                      <RECURSION!>
```

All references are removed and replaces with the referenced content. If a single object is referenced multiple times, the whole schema is inlined in place of each reference. In case of the recursive reference, this causes an infinite loop unless a custom Recursion Handler is provided. 

### Translating Parser result ###

```yaml
---
openapi: 3.0.3
info:
  title: Example specification for the translating parser
  version: 0.0.0
paths:
  /hosts:
    get:
      responses:
        default:
          description: >-
            An operation with a referenced schema.
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/schemas.spec.yaml_Response"
components:
  schemas:
    schemas.spec.yaml_Response:
      type: object
      properties:
        simple:
          $ref: "#/components/schemas/schemas.spec.yaml_Simple"
        nested:
          $ref: "#/components/schemas/schemas.spec.yaml_Nested"
  Simple:
    type: object
  Nested:
    type: object
    additionalProperties:
      $ref: "#/components/schemas/schemas.spec.yaml_Nested"
```

Here, the schemas from the external files are carried over to the original specification document. References remain references, just pointing to the Schemas collection. This applies to the recursive object too that is still recursive, only referencing itself in its new location.

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