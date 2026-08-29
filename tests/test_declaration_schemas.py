"""R1 #26 S7 correction-pass checks (D1-D3): the change-declaration schemas
enforce the declaration-vocabulary amendment's plan-effect-class constraints —
the T20 #22 d5 closed vocabulary and fixed per-kind classes.

Covers, per the amendment's correction ledger:
- D1: group-key-rename fixes expected_plan_effect_class to `empty`; the
  superseded `zero-aws-mutations` token is rejected.
- D2: permission-set-key-replacement fixes creates-only for phase introduce and
  deletes-only for phase retire via schema conditionals; the retire-specific
  fields are NOT prohibited during introduce (deliberately unratified).
- D3: principal-replacement constrains expected_plan_effect_class to the closed
  vocabulary; every member is accepted, everything else rejected.
"""

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parent.parent
AUTHORED = REPO / "schemas" / "governance" / "change-declaration"

VOCABULARY = [
    "empty",
    "creates-only",
    "updates-only",
    "deletes-only",
    "mixed",
    "imports-only",
    "state-removal-only",
    "guard-removal-no-live-change",
]


def load(kind: str) -> Draft202012Validator:
    with open(AUTHORED / f"{kind}.schema.json", encoding="utf-8") as fh:
        return Draft202012Validator(json.load(fh))


def common(kind: str, key: str) -> dict:
    return {
        "schema_version": 1,
        "key": key,
        "kind": kind,
        "owner": "identity-platform",
        "justification": "Declared exceptional change for test coverage.",
        "change_reference": "https://github.com/a24577t/aws-identity-access/issues/26",
        "deployment_scope": "lab",
        "valid_from": "2026-08-29T00:00:00Z",
        "valid_until": "2026-09-29T00:00:00Z",
        "affected_paths": ["access/identity-center/groups/lab-readers.yml"],
    }


def rename_decl(effect: str = "empty") -> dict:
    d = common("group-key-rename", "rename-lab-readers")
    d.update(
        expected_plan_effect_class=effect,
        from_key="lab-readers",
        to_key="lab-viewers",
    )
    return d


def replacement_decl(phase: str, effect: str, retire_fields: bool) -> dict:
    d = common("permission-set-key-replacement", "replace-read-only")
    d.update(
        expected_plan_effect_class=effect,
        from_key="read-only",
        to_key="read-only-v2",
        phase=phase,
    )
    if retire_fields:
        d["introduce_completion_evidence"] = (
            "https://github.com/a24577t/aws-identity-access/issues/26"
        )
        d["destroy_acknowledgement"] = True
    return d


def principal_decl(effect: str) -> dict:
    d = common("principal-replacement", "replace-lab-readers-principal")
    d.update(
        expected_plan_effect_class=effect,
        group_key="lab-readers",
        reason="The external principal behind the group is replaced.",
        group_id_change_expected=True,
    )
    return d


def valid(validator: Draft202012Validator, instance: dict) -> bool:
    return not list(validator.iter_errors(instance))


class D1GroupKeyRename(unittest.TestCase):
    def setUp(self) -> None:
        self.v = load("group-key-rename")

    def test_empty_accepted(self) -> None:
        self.assertTrue(valid(self.v, rename_decl("empty")))

    def test_old_token_rejected(self) -> None:
        self.assertFalse(valid(self.v, rename_decl("zero-aws-mutations")))

    def test_every_other_vocabulary_value_rejected(self) -> None:
        for effect in VOCABULARY:
            if effect == "empty":
                continue
            with self.subTest(effect=effect):
                self.assertFalse(valid(self.v, rename_decl(effect)))


class D2PermissionSetKeyReplacement(unittest.TestCase):
    def setUp(self) -> None:
        self.v = load("permission-set-key-replacement")

    def test_introduce_creates_only_accepted(self) -> None:
        self.assertTrue(
            valid(self.v, replacement_decl("introduce", "creates-only", False))
        )

    def test_introduce_other_classes_rejected(self) -> None:
        for effect in VOCABULARY + ["zero-aws-mutations"]:
            if effect == "creates-only":
                continue
            with self.subTest(effect=effect):
                self.assertFalse(
                    valid(self.v, replacement_decl("introduce", effect, False))
                )

    def test_retire_deletes_only_accepted(self) -> None:
        self.assertTrue(
            valid(self.v, replacement_decl("retire", "deletes-only", True))
        )

    def test_retire_other_classes_rejected(self) -> None:
        for effect in VOCABULARY + ["zero-aws-mutations"]:
            if effect == "deletes-only":
                continue
            with self.subTest(effect=effect):
                self.assertFalse(
                    valid(self.v, replacement_decl("retire", effect, True))
                )

    def test_retire_without_evidence_or_ack_rejected(self) -> None:
        self.assertFalse(
            valid(self.v, replacement_decl("retire", "deletes-only", False))
        )

    def test_introduce_with_retire_fields_not_prohibited(self) -> None:
        # The amendment deliberately does not ratify structural absence of the
        # retire-specific fields during introduce (Q3-A "as rendered").
        self.assertTrue(
            valid(self.v, replacement_decl("introduce", "creates-only", True))
        )


class D3PrincipalReplacement(unittest.TestCase):
    def setUp(self) -> None:
        self.v = load("principal-replacement")

    def test_every_vocabulary_value_accepted(self) -> None:
        for effect in VOCABULARY:
            with self.subTest(effect=effect):
                self.assertTrue(valid(self.v, principal_decl(effect)))

    def test_values_outside_vocabulary_rejected(self) -> None:
        for effect in [
            "zero-aws-mutations",
            "replace",
            "creates_only",
            "EMPTY",
            "",
            "no-op",
        ]:
            with self.subTest(effect=effect):
                self.assertFalse(valid(self.v, principal_decl(effect)))


if __name__ == "__main__":
    unittest.main()
