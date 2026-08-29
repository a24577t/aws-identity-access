"""R2 #27 row-3 external check: the finding-record contract of T14 #19 d9/C14
- canonical total ordering over the seven serialized distinguishing fields,
deterministic duplicate collapse before serialization, the fixed [omitted]
sentinel, the global-finding representation, severity derived from the
catalogue (never an ordering key), and byte-deterministic serialization.
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import findings  # noqa: E402


def f(**kw):
    base = dict(
        code="KEY-GRAMMAR",
        stage="validation",
        file_path="access/identity-center/groups/lab-readers.yml",
        field_path="/key",
        rule_ids=("T05 #7 d1/d5",),
        value=None,
        message="key violates the grammar",
    )
    base.update(kw)
    return findings.Finding(**base)


class OrderingAndCollapse(unittest.TestCase):
    def test_severity_comes_from_the_catalogue(self) -> None:
        # No silent downgrade surface: severity is not authorable per finding.
        self.assertEqual("error", f().severity)
        self.assertEqual("deferred", f(code="INV-DEFERRED").severity)

    def test_unknown_code_rejected(self) -> None:
        with self.assertRaises(findings.ContractViolation):
            f(code="KEY-INVENTED")

    def test_stage_outside_enumeration_rejected(self) -> None:
        # T14 #19 d3: a finding raised at a stage the code does not enumerate
        # is a contract violation.
        with self.assertRaises(findings.ContractViolation):
            f(code="PRQ-MISSING", stage="validation")

    def test_canonical_order_is_the_seven_key_order(self) -> None:
        # C14 key order: file_path, code, field_path, stage, rule_ids,
        # value (with sentinel), message.
        a = f(file_path="access/a.yml")
        b = f(file_path="access/b.yml", code="ASN-SHAPE")
        c = f(file_path="access/b.yml", code="KEY-GRAMMAR")
        d = f(file_path="access/b.yml", code="KEY-GRAMMAR", field_path="/z")
        ordered = findings.canonical(
            [d, c, b, a]
        )
        self.assertEqual([a, b, c, d], ordered)

    def test_value_sentinel_orders_omitted_values(self) -> None:
        omitted = f(value=None)
        present = f(value="Z")
        # "[omitted]" < "Z" is false ("[" is 0x5B > "Z" 0x5A): the sentinel
        # participates in ordering as the literal string.
        self.assertEqual([present, omitted], findings.canonical([omitted, present]))

    def test_identical_findings_collapse(self) -> None:
        self.assertEqual(1, len(findings.canonical([f(), f(), f()])))

    def test_distinct_locations_do_not_collapse(self) -> None:
        self.assertEqual(
            2, len(findings.canonical([f(field_path="/key"), f(field_path="/x")]))
        )

    def test_global_finding_representation(self) -> None:
        g = findings.Finding(
            code="GOV-ROUTE",
            stage="validation",
            file_path=None,
            field_path=None,
            rule_ids=("T06 #8 d3",),
            value=None,
            message="uncovered governed path",
        )
        self.assertEqual("-", g.file_path)
        self.assertEqual("-", g.field_path)


class Serialization(unittest.TestCase):
    def test_serialization_is_byte_deterministic_and_canonical(self) -> None:
        one = findings.serialize([f(field_path="/x"), f(), f()])
        two = findings.serialize([f(), f(field_path="/x")])
        self.assertEqual(one, two)
        self.assertIsInstance(one, bytes)
        self.assertNotIn(b"\r", one)

    def test_serialized_record_carries_the_contract_fields(self) -> None:
        import json

        doc = json.loads(findings.serialize([f(value=None)]))
        (rec,) = doc["findings"]
        self.assertEqual(
            ["code", "severity", "stage", "file_path", "field_path",
             "rule_ids", "value", "message"],
            list(rec),
        )
        self.assertEqual("[omitted]", rec["value"])
        self.assertEqual("error", rec["severity"])

    def test_control_characters_never_serialized_raw(self) -> None:
        # T05 #7 d5 / T14 d9: offending values are rendered escaped and
        # unambiguous, never raw control characters.
        blob = findings.serialize([f(value="bad\x07value", message="m")])
        self.assertNotIn(b"\x07", blob)


if __name__ == "__main__":
    unittest.main()
