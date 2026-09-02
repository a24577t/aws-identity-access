"""R2 #27 row-7 external checks - the governed fixture tree (T14 #19 d6;
spec 3 W4, 5).

tests/fixtures/valid/** mirrors the access/ and governance/ layouts and
passes with zero error findings; the one deferral it inherently carries -
the lab-requested assignment - is reported as exactly one INV-DEFERRED
finding of severity deferred, never invalid (RD-08; T14 #19 d1: `deferred`
is the non-blocking severity, so the valid tree blocks on nothing).

tests/fixtures/invalid/<CODE>/ holds one deterministic negative fixture per
active code of the ten R2 families - a run.json declaring the stage, run
inputs, and the exact expected finding set, and a tree/ holding the
committed synthetic inputs (plan/apply fixtures carry their clock-controlled
plan-context.json; no fixture depends on wall-clock time, AWS, live
identifiers, or credentials). Expectation sets are verified externally -
expected finding sets, never internals. The two approved multi-code
expectations are {ASN-SHAPE, P-OOS-USER} (T10 d7) and
{ADM-CAPABLE, ADM-STANDING} (T07 d2).

CLS-*, GEN-*, and ADO-* fixtures land with their implementing ticket
(R3 #28); their codes are outside R2's rows (execution-grouping amendment).
"""

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import catalogue, findings, runner  # noqa: E402

FIXTURES = REPO / "tests" / "fixtures"
VALID = FIXTURES / "valid"
INVALID = FIXTURES / "invalid"

# The ten R2 families plus the three landed by R3 #28 (CLS/GEN/ADO - the
# recorded allocation note reconciled): every ACTIVE code carries exactly
# one deterministic negative fixture; dormant ADO-MANIFEST carries none.
FAMILIES = {"INV", "PRQ", "P-OOS", "KEY", "ASN", "ADM", "GOV", "FIX",
            "CFG", "DOC", "CLS", "GEN", "ADO"}

VERIFIED_INSTANCE = (
    "instance_type: organization\n"
    "primary_region: us-east-1\n"
    "additional_regions: []\n"
    "identity_source:\n"
    "  type: identity-center-default\n"
    "delegated_administrator: lab-tooling\n"
    "owner: identity-platform\n"
    "verification:\n"
    "  verified_at: \"2026-08-28T00:46:16Z\"\n"
    "  snapshot_id: \"" + "a" * 64 + "\"\n"
)


def load_config(directory, tree_root):
    run = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    kwargs = {}
    if run.get("inventory_fixture"):
        kwargs["inventory_fixture"] = directory / run["inventory_fixture"]
    if run.get("plan_context"):
        kwargs["plan_context"] = directory / run["plan_context"]
    if run.get("resource_name_prefix"):
        kwargs["resource_name_prefix"] = run["resource_name_prefix"]
    if run.get("handle_mapping"):
        kwargs["handle_mapping"] = run["handle_mapping"]
    if run.get("codeowners_file"):
        kwargs["codeowners"] = (directory / run["codeowners_file"]).read_text(
            encoding="utf-8")
    if run.get("changed_paths"):
        kwargs["changed_paths"] = run["changed_paths"]
    if run.get("regenerated"):
        kwargs["regenerated"] = {
            path: text.encode("utf-8")
            for path, text in run["regenerated"].items()
        }
    return run, runner.RunConfig(**kwargs)


class ValidTree(unittest.TestCase):
    def run_valid(self):
        config = runner.RunConfig(
            inventory_fixture=VALID
            / "governance" / "inventory" / "lab-inventory-fixture.yml",
        )
        return runner.run("validation", VALID, config)

    def test_valid_tree_zero_errors_one_deferral(self) -> None:
        result = self.run_valid()
        errors = [f for f in result if f.severity == "error"]
        deferred = [f for f in result if f.severity == "deferred"]
        self.assertEqual([], [(f.code, f.file_path, f.message)
                              for f in errors])
        self.assertEqual(["INV-DEFERRED"], [f.code for f in deferred])
        self.assertIn("lab-requested", deferred[0].file_path)

    def test_valid_tree_is_deterministic(self) -> None:
        one = findings.serialize(self.run_valid())
        two = findings.serialize(self.run_valid())
        self.assertEqual(one, two)

    def test_valid_tree_verified_instance_form_also_passes(self) -> None:
        # T14 #19 d6 valid basis: instance.yml in BOTH forms - the second
        # (synthetic format-valid verification block) via overlay.
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "valid"
            shutil.copytree(VALID, target)
            (target / "access" / "identity-center" / "configuration"
             / "instance.yml").write_text(
                VERIFIED_INSTANCE, encoding="utf-8", newline="\n")
            config = runner.RunConfig(
                inventory_fixture=target
                / "governance" / "inventory" / "lab-inventory-fixture.yml",
            )
            result = runner.run("validation", target, config)
            self.assertEqual(
                [], [f.code for f in result if f.severity == "error"]
            )


class InvalidTree(unittest.TestCase):
    def test_every_active_r2_code_has_its_fixture_directory(self) -> None:
        expected = {
            code for code, entry in catalogue.CATALOGUE.items()
            if entry.family in FAMILIES and entry.state == "active"
        }
        present = {p.name for p in INVALID.iterdir() if p.is_dir()}
        self.assertEqual(expected, present)

    def test_every_fixture_meets_its_declared_expectation_set(self) -> None:
        for directory in sorted(INVALID.iterdir()):
            if not directory.is_dir():
                continue
            with self.subTest(code=directory.name):
                run, config = load_config(directory, directory / "tree")
                result = runner.run(run["stage"], directory / "tree", config)
                self.assertEqual(
                    sorted(run["expected"]),
                    sorted(f.code for f in result),
                    f"{directory.name}: expectation set mismatch",
                )

    def test_the_two_approved_multi_code_expectations(self) -> None:
        user = json.loads(
            (INVALID / "P-OOS-USER" / "run.json").read_text(encoding="utf-8")
        )
        self.assertEqual(["ASN-SHAPE", "P-OOS-USER"], sorted(user["expected"]))
        pair = json.loads(
            (INVALID / "ADM-STANDING" / "run.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            ["ADM-CAPABLE", "ADM-STANDING"], sorted(pair["expected"])
        )
        for directory in sorted(INVALID.iterdir()):
            if not directory.is_dir() or directory.name in (
                    "P-OOS-USER", "ADM-STANDING"):
                continue
            run = json.loads(
                (directory / "run.json").read_text(encoding="utf-8"))
            with self.subTest(code=directory.name):
                self.assertEqual(
                    [directory.name], run["expected"],
                    "only the two approved multi-code expectations exist",
                )

    def test_plan_fixtures_carry_their_controlled_clock(self) -> None:
        for directory in sorted(INVALID.iterdir()):
            if not directory.is_dir():
                continue
            run = json.loads(
                (directory / "run.json").read_text(encoding="utf-8"))
            if run["stage"] not in ("plan", "apply"):
                continue
            with self.subTest(code=directory.name):
                context = json.loads(
                    (directory / run["plan_context"]).read_text(
                        encoding="utf-8"))
                self.assertIn("clock", context)


if __name__ == "__main__":
    unittest.main()
