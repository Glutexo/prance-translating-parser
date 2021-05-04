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

    @staticmethod
    def _assert_ref(schema, ref):
        assert "$ref" in schema
        assert schema["$ref"] == f"#/components/schemas/{ref}"

    def __init__(self, file):
        self.specification = self._parse_spec(file)

    def assert_schemas(self, keys):
        assert self.specification["components"]["schemas"].keys() == keys

    def assert_path_ref(self, ref):
        responses = self.specification["paths"]["/hosts"]["get"]["responses"]
        schema = responses["default"]["content"]["application/json"]["schema"]
        self._assert_ref(schema, ref)

    def assert_schema_ref(self, key, ref):
        schemas = self.specification["components"]["schemas"]
        assert key in schemas
        self._assert_ref(schemas[key], ref)


def test_local_reference_from_root():
    tester = SpecificationTester("local_root_ref.spec.yaml")
    tester.assert_path_ref("PlainObject")
    tester.assert_schemas({"PlainObject"})


def test_file_reference_from_root():
    tester = SpecificationTester("file_ref.spec.yaml")
    tester.assert_path_ref("plain_obj.spec.yaml_PlainObject")
    tester.assert_schemas({"plain_obj.spec.yaml_PlainObject"})


def test_local_reference_from_file():
    tester = SpecificationTester("local_file_ref.spec.yaml")
    tester.assert_path_ref("more_objs.spec.yaml_RefObject")
    tester.assert_schemas({"more_objs.spec.yaml_RefObject", "more_objs.spec.yaml_PlainObject"})
    tester.assert_schema_ref("more_objs.spec.yaml_RefObject", "more_objs.spec.yaml_PlainObject")


@mark.skip
def test_same_file_reference_from_file():
    pass


@mark.skip
def test_different_file_reference_from_file():
    pass


@mark.skip
def test_root_file_reference_from_file():
    pass
