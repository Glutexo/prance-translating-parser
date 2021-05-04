from os.path import join

from pytest import mark

from translating_parser.parser import TranslatingParser


def test_local_reference_from_root():
    path = join("tests", "specs", "local_ref.spec.yaml")
    parser = TranslatingParser(path)
    parser.parse()

    parsed_responses = parser.specification["paths"]["/hosts"]["get"]["responses"]
    expected_schema = parsed_responses["default"]["content"]["application/json"]["schema"]
    assert "$ref" in expected_schema
    assert expected_schema["$ref"] == "#/components/schemas/PlainObject"
    assert parser.specification["components"]["schemas"].keys() == {"PlainObject"}


def test_file_reference_from_root():
    path = join("tests", "specs", "file_ref.spec.yaml")
    parser = TranslatingParser(path)
    parser.parse()

    parsed_responses = parser.specification["paths"]["/hosts"]["get"]["responses"]
    expected_schema = parsed_responses["default"]["content"]["application/json"]["schema"]
    assert "$ref" in expected_schema
    assert expected_schema["$ref"] == "#/components/schemas/plain_obj.spec.yaml_PlainObject"
    assert parser.specification["components"]["schemas"].keys() == {"plain_obj.spec.yaml_PlainObject"}


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
