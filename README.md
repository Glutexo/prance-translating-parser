# Translating Parser for Prance #

This is a Translating parser for [Prance], a library processing and validating [OpenAPI] specification files. It targets use cases when a specification spans across multiple files that need to be compiled to a single document, but inlining of the references objects is not desired or event possible.

Frameworks like [Connexion] unfortunately do not support file references in the specification and [Prance] can be used to alleviate this missing features. Inlining can result in excessive memory usage and also can make code generators not work properly if they rely on properly reused component schema definitions. If the specification contains a recursive object definition, inlining would result in an infinite loop. 

## Requirements ##

* pipenv
  ```sh
  $ pip install pipenv
  ```

## Development environment ##

```sh
$ pipenv sync
```

## Testing ##

```sh
$ PYTHONPATH=. pipenv run pytest
```

## License ##

[MIT](LICENSE.txt), to be compatible with [Prance].

[Prance]: https://github.com/RonnyPfannschmidt/prance/
[OpenAPI]: https://www.openapis.org/
[Connexion]: https://github.com/zalando/connexion