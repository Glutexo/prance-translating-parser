from translating_parser.parser import TranslatingParser
from yaml import dump


def test_plain_object():
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

    expected_schema = parser.specification \
        ["paths"]["/hosts"]["get"]["responses"]["default"]["content"]["application/json"]["schema"]
    assert "$ref" in expected_schema
    assert expected_schema["$ref"] == "#/components/schemas/PlainObject"
    assert parser.specification["components"]["schemas"].keys() == {"PlainObject"}
