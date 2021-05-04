from os.path import join

from pytest import mark

from translating_parser.parser import TranslatingParser


def _parse_spec(file):
    path = join("tests", "specs", file)
    parser = TranslatingParser(path)
    parser.parse()
    return parser.specification


def test_local_reference_from_root():
    specification = _parse_spec("local_ref.spec.yaml")
    parsed_responses = specification["paths"]["/hosts"]["get"]["responses"]
    expected_schema = parsed_responses["default"]["content"]["application/json"]["schema"]
    assert "$ref" in expected_schema
    assert expected_schema["$ref"] == "#/components/schemas/PlainObject"
    assert specification["components"]["schemas"].keys() == {"PlainObject"}


def test_file_reference_from_root():
    specification = _parse_spec("file_ref.spec.yaml")
    parsed_responses = specification["paths"]["/hosts"]["get"]["responses"]
    expected_schema = parsed_responses["default"]["content"]["application/json"]["schema"]
    assert "$ref" in expected_schema
    assert expected_schema["$ref"] == "#/components/schemas/plain_obj.spec.yaml_PlainObject"
    assert specification["components"]["schemas"].keys() == {"plain_obj.spec.yaml_PlainObject"}


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
