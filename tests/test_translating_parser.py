from os.path import join

from pytest import mark

from translating_parser.parser import TranslatingParser


class SpecificationTester:
    @staticmethod
    def _parse_spec(name):
        file = f"{name}.spec.yaml"
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

    def assert_schema_ref(self, key, ref, sub=None):
        schemas = self.specification["components"]["schemas"]
        assert key in schemas
        schema = schemas[key][sub] if sub else schemas[key]
        self._assert_ref(schema, ref)


def test_local_reference_from_root():
    tester = SpecificationTester("local_reference_from_root")
    tester.assert_path_ref("PlainObject")
    tester.assert_schemas({"PlainObject"})


def test_file_reference_from_root():
    tester = SpecificationTester("file_reference_from_root")
    tester.assert_path_ref("file_reference_from_root_schemas.spec.yaml_PlainObject")
    tester.assert_schemas({"file_reference_from_root_schemas.spec.yaml_PlainObject"})


def test_local_reference_from_file():
    tester = SpecificationTester("local_reference_from_file")
    tester.assert_path_ref("local_reference_from_file_schemas.spec.yaml_RefObject")
    tester.assert_schemas(
        {
            "local_reference_from_file_schemas.spec.yaml_RefObject",
            "local_reference_from_file_schemas.spec.yaml_PlainObject",
        }
    )
    tester.assert_schema_ref(
        "local_reference_from_file_schemas.spec.yaml_RefObject",
        "local_reference_from_file_schemas.spec.yaml_PlainObject",
    )


def test_same_file_reference_from_file():
    tester = SpecificationTester("same_file_reference_from_file")
    tester.assert_path_ref("same_file_reference_from_file_schemas.spec.yaml_RefObject")
    tester.assert_schemas(
        {
            "same_file_reference_from_file_schemas.spec.yaml_RefObject",
            "same_file_reference_from_file_schemas.spec.yaml_PlainObject",
        }
    )
    tester.assert_schema_ref(
        "same_file_reference_from_file_schemas.spec.yaml_RefObject",
        "same_file_reference_from_file_schemas.spec.yaml_PlainObject",
    )


def test_different_file_reference_from_file():
    tester = SpecificationTester("different_file_reference_from_file")
    tester.assert_path_ref("different_file_reference_from_file_schemas1.spec.yaml_RefObject")
    tester.assert_schemas(
        {
            "different_file_reference_from_file_schemas1.spec.yaml_RefObject",
            "different_file_reference_from_file_schemas2.spec.yaml_PlainObject",
        }
    )
    tester.assert_schema_ref(
        "different_file_reference_from_file_schemas1.spec.yaml_RefObject",
        "different_file_reference_from_file_schemas2.spec.yaml_PlainObject",
    )


def test_root_file_reference_from_file():
    tester = SpecificationTester("root_file_reference_from_file")
    tester.assert_path_ref("root_file_reference_from_file_schemas.spec.yaml_RefObject")
    tester.assert_schemas({"PlainObject", "root_file_reference_from_file_schemas.spec.yaml_RefObject"})
    tester.assert_schema_ref("root_file_reference_from_file_schemas.spec.yaml_RefObject", "PlainObject")


def test_root_file_reference_from_root():
    tester = SpecificationTester("root_file_reference_from_root")
    tester.assert_path_ref("PlainObject")
    tester.assert_schemas({"PlainObject"})


def test_recursive_reference_in_root():
    tester = SpecificationTester("recursive_reference_in_root")
    tester.assert_schema_ref("RecursiveObject", "RecursiveObject", "additionalProperties")


def test_recursive_reference_in_file():
    tester = SpecificationTester("recursive_reference_in_file")
    tester.assert_path_ref("recursive_reference_in_file_schemas.spec.yaml_RecursiveObject")
    tester.assert_schemas({"recursive_reference_in_file_schemas.spec.yaml_RecursiveObject"})
    tester.assert_schema_ref(
        "recursive_reference_in_file_schemas.spec.yaml_RecursiveObject",
        "recursive_reference_in_file_schemas.spec.yaml_RecursiveObject",
        "additionalProperties"
    )
