from os.path import join

from pytest import mark

from translating_parser.parser import TranslatingParser


class SpecificationTester:
    @staticmethod
    def _parse_spec(file):
        path = join("tests", "specs", file)
        parser = TranslatingParser(path)
        parser.parse()
        return parser.specification

    def __init__(self, file):
        self.specification = self._parse_spec(file)

    def assert_path_ref(self, ref):
        responses = self.specification["paths"]["/hosts"]["get"]["responses"]
        schema = responses["default"]["content"]["application/json"]["schema"]
        assert "$ref" in schema
        assert schema["$ref"] == ref

    def assert_schemas(self, keys):
        assert self.specification["components"]["schemas"].keys() == keys


def test_local_reference_from_root():
    tester = SpecificationTester("local_ref.spec.yaml")
    tester.assert_path_ref("#/components/schemas/PlainObject")
    tester.assert_schemas({"PlainObject"})


def test_file_reference_from_root():
    tester = SpecificationTester("file_ref.spec.yaml")
    tester.assert_path_ref("#/components/schemas/plain_obj.spec.yaml_PlainObject")
    tester.assert_schemas({"plain_obj.spec.yaml_PlainObject"})


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
