from os.path import join

from pytest import mark

from translating_parser.parser import TranslatingParser


def _parse_spec(file):
    path = join("tests", "specs", file)
    parser = TranslatingParser(path)
    parser.parse()
    return parser.specification


def _assert_path_ref(specification, ref):
    responses = specification["paths"]["/hosts"]["get"]["responses"]
    expected_schema = responses["default"]["content"]["application/json"]["schema"]
    assert "$ref" in expected_schema
    assert expected_schema["$ref"] == ref


def _assert_schemas(specification, keys):
    assert specification["components"]["schemas"].keys() == keys


def test_local_reference_from_root():
    specification = _parse_spec("local_ref.spec.yaml")
    _assert_path_ref(specification, "#/components/schemas/PlainObject")
    _assert_schemas(specification, {"PlainObject"})


def test_file_reference_from_root():
    specification = _parse_spec("file_ref.spec.yaml")
    _assert_path_ref(specification, "#/components/schemas/plain_obj.spec.yaml_PlainObject")
    _assert_schemas(specification, {"plain_obj.spec.yaml_PlainObject"})


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
