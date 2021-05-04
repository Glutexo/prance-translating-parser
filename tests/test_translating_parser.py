from yaml import dump

from pytest import mark

from translating_parser.parser import TranslatingParser


def test_local_reference_from_root():
    schema_obj = {
        "openapi": "3.0.3",
        "info": {
            "title": "Sample specification for the translating parser",
            "version": "0.0.0",
        },
        "paths": {
            "/hosts": {
                "get": {
                    "responses": {
                        "default": {
                            "description": "A local reference",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/PlainObject",
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {
                "PlainObject": {
                    "type": "object",
                },
            },
        },
    }
    schema_yaml = dump(schema_obj)
    parser = TranslatingParser(spec_string=schema_yaml)
    parser.parse()

    parsed_responses = parser.specification["paths"]["/hosts"]["get"]["responses"]
    expected_schema = parsed_responses["default"]["content"]["application/json"]["schema"]
    assert "$ref" in expected_schema
    assert expected_schema["$ref"] == "#/components/schemas/PlainObject"
    assert parser.specification["components"]["schemas"].keys() == {"PlainObject"}


@mark.skip
def test_file_reference_from_root():
    pass


@mark.skip
def test_local_reference_from_file():
    pass


@mark.skip
def test_same_file_reference_from_file():
    pass


@mark.skip
def test_different_file_reference_from_file():
    pass


@mark.skip
def test_root_file_reference_from_file():
    pass
