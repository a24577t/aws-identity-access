"""R1 #26 row-2 mechanical check: every committed governed file validates against
its schema, hermetically (no network retrieval of meta-schemas), with the pinned
toolchain (jsonschema == 4.23.0, PyYAML == 6.0.2; specification §8.1).

The schema is the configuration contract's executable form; the contract prevails
on any divergence. This is not the T14 #19 validator (R2 #27) — schema conformance
only.
"""

import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parent.parent
SCHEMAS = REPO / "schemas"

ALL_SCHEMAS = sorted(SCHEMAS.rglob("*.schema.json"))

# Committed governed file -> governing schema.
GOVERNED = {
    "access/identity-center/groups/lab-readers.yml": "access/group.schema.json",
    "access/identity-center/permission-sets/read-only.yml": "access/permission-set.schema.json",
    "access/identity-center/permission-sets/inventory-reader.yml": "access/permission-set.schema.json",
    "access/identity-center/account-assignments/lab-workload-a/lab-readers--read-only.yml": "access/account-assignment.schema.json",
    "access/identity-center/account-assignments/lab-workload-b/lab-readers--read-only.yml": "access/account-assignment.schema.json",
    "access/identity-center/account-assignments/lab-requested/lab-readers--read-only.yml": "access/account-assignment.schema.json",
    "access/identity-center/configuration/instance.yml": "access/instance.schema.json",
    "governance/ownership/principals/identity-platform.yml": "governance/principal.schema.json",
    "governance/ownership/principals/security.yml": "governance/principal.schema.json",
    "governance/ownership/principals/architecture.yml": "governance/principal.schema.json",
    "governance/ownership/principals/deployment-authority.yml": "governance/principal.schema.json",
    "governance/ownership/review-classes/identity-platform.yml": "governance/review-class.schema.json",
    "governance/ownership/review-classes/security.yml": "governance/review-class.schema.json",
    "governance/ownership/review-classes/architecture.yml": "governance/review-class.schema.json",
    "governance/ownership/review-classes/deployment-authority.yml": "governance/review-class.schema.json",
    "governance/ownership/routing.yml": "governance/routing-table.schema.json",
}


def load_schema(rel: str) -> dict:
    with open(SCHEMAS / rel, encoding="utf-8") as fh:
        return json.load(fh)


class SchemaFilesAreValid(unittest.TestCase):
    def test_every_schema_is_valid_draft_2020_12(self) -> None:
        self.assertTrue(ALL_SCHEMAS, "no schema files found")
        for path in ALL_SCHEMAS:
            with self.subTest(schema=path.relative_to(REPO).as_posix()):
                with open(path, encoding="utf-8") as fh:
                    schema = json.load(fh)
                self.assertEqual(
                    schema.get("$schema"),
                    "https://json-schema.org/draft/2020-12/schema",
                )
                Draft202012Validator.check_schema(schema)

    def test_schemas_are_self_contained(self) -> None:
        # Hermetic rule: no cross-file or remote $ref anywhere.
        for path in ALL_SCHEMAS:
            with self.subTest(schema=path.relative_to(REPO).as_posix()):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn('"$ref"', text)


class GovernedFilesValidate(unittest.TestCase):
    def test_every_governed_file_validates(self) -> None:
        for rel_file, rel_schema in GOVERNED.items():
            with self.subTest(file=rel_file):
                target = REPO / rel_file
                self.assertTrue(target.is_file(), f"missing governed file {rel_file}")
                with open(target, encoding="utf-8") as fh:
                    instance = yaml.safe_load(fh)
                validator = Draft202012Validator(load_schema(rel_schema))
                errors = sorted(validator.iter_errors(instance), key=str)
                self.assertEqual(
                    [], [e.message for e in errors], f"{rel_file} vs {rel_schema}"
                )

    def test_filename_stem_equals_key(self) -> None:
        # 02 validation requirement 1 (T05 d1): filename stem = key exactly,
        # for every keyed governed record committed in R1.
        keyed = [
            "access/identity-center/groups/lab-readers.yml",
            "access/identity-center/permission-sets/read-only.yml",
            "access/identity-center/permission-sets/inventory-reader.yml",
            "governance/ownership/principals/identity-platform.yml",
            "governance/ownership/principals/security.yml",
            "governance/ownership/principals/architecture.yml",
            "governance/ownership/principals/deployment-authority.yml",
            "governance/ownership/review-classes/identity-platform.yml",
            "governance/ownership/review-classes/security.yml",
            "governance/ownership/review-classes/architecture.yml",
            "governance/ownership/review-classes/deployment-authority.yml",
        ]
        for rel_file in keyed:
            with self.subTest(file=rel_file):
                path = REPO / rel_file
                with open(path, encoding="utf-8") as fh:
                    data = yaml.safe_load(fh)
                self.assertEqual(path.name.removesuffix(".yml"), data["key"])

    def test_assignment_three_way_agreement(self) -> None:
        # T10 d3: directory <-> account; filename segment 1 <-> principal.group;
        # segment 2 <-> permission_set.
        base = REPO / "access/identity-center/account-assignments"
        files = sorted(base.rglob("*.yml"))
        self.assertEqual(3, len(files))
        for path in files:
            with self.subTest(file=path.relative_to(REPO).as_posix()):
                with open(path, encoding="utf-8") as fh:
                    data = yaml.safe_load(fh)
                group_seg, ps_seg = path.name.removesuffix(".yml").split("--")
                self.assertEqual(path.parent.name, data["account"])
                self.assertEqual(group_seg, data["principal"]["group"])
                self.assertEqual(ps_seg, data["permission_set"])

    def test_instance_has_no_verification_block(self) -> None:
        # T22 d1: no verification block until first verification.
        with open(
            REPO / "access/identity-center/configuration/instance.yml",
            encoding="utf-8",
        ) as fh:
            data = yaml.safe_load(fh)
        self.assertNotIn("verification", data)

    def test_schema_rejects_unknown_fields(self) -> None:
        # Spot-check the closed field sets: an added field must fail.
        validator = Draft202012Validator(
            load_schema("access/account-assignment.schema.json")
        )
        bad = {
            "account": "lab-workload-a",
            "principal": {"type": "GROUP", "group": "lab-readers"},
            "permission_set": "read-only",
            "status": "active",
        }
        self.assertTrue(list(validator.iter_errors(bad)))

    def test_schema_rejects_user_principal(self) -> None:
        # T10 d2: only the two-segment GROUP form is recognized.
        validator = Draft202012Validator(
            load_schema("access/account-assignment.schema.json")
        )
        bad = {
            "account": "lab-workload-a",
            "principal": {"type": "USER", "group": "lab-readers"},
            "permission_set": "read-only",
        }
        self.assertTrue(list(validator.iter_errors(bad)))


if __name__ == "__main__":
    unittest.main()
