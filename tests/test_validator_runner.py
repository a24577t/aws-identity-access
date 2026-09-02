"""R2 #27 row-3 external checks on the validator run seam: the closed stage
vocabulary, the hermetic validation boundary (no clock, no snapshot, no plan
context - T22 #21 d4; T09 #12 d15; T15 #10 d6), deterministic output, and the
INV-PUBLIC-LEAK rule with exactly its single ARN exemption (T14 #19 d4b).
"""

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import findings, runner  # noqa: E402


def run_codes(stage, target, **config):
    return [f.code for f in runner.run(stage, target, runner.RunConfig(**config))]


class StageDiscipline(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.target = Path(self.tmp.name)

    def test_unknown_stage_rejected(self) -> None:
        with self.assertRaises(findings.ContractViolation):
            runner.run("compile", self.target, runner.RunConfig())

    def test_validation_refuses_plan_context(self) -> None:
        # Hermetic boundary: validation holds no clock and reads no snapshot.
        with self.assertRaises(findings.ContractViolation):
            runner.run(
                "validation",
                self.target,
                runner.RunConfig(plan_context={"clock": "2026-08-29T00:00:00Z"}),
            )

    def test_plan_requires_plan_context(self) -> None:
        with self.assertRaises(findings.ContractViolation):
            runner.run("plan", self.target, runner.RunConfig())

    def test_empty_tree_validates_clean_and_deterministically(self) -> None:
        one = runner.run("validation", self.target, runner.RunConfig())
        two = runner.run("validation", self.target, runner.RunConfig())
        self.assertEqual([], one)
        self.assertEqual(findings.serialize(one), findings.serialize(two))


class PublicLeakRule(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.target = Path(self.tmp.name)

    def write(self, rel, text) -> None:
        path = self.target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def test_exempt_aws_managed_policy_arn_passes(self) -> None:
        self.write(
            "permission-sets/read-only.yml",
            "managed_policies:\n  - arn:aws:iam::aws:policy/ReadOnlyAccess\n",
        )
        self.assertEqual([], run_codes("validation", self.target))

    def test_admin_access_arn_is_exempt_too(self) -> None:
        # The exemption is the vocabulary, not one policy name (T21 #20 d2).
        self.write(
            "x.yml",
            "arn:aws:iam::aws:policy/AdministratorAccess\n",
        )
        self.assertEqual([], run_codes("validation", self.target))

    def test_markup_quoted_exempt_vocabulary_citation_passes(self) -> None:
        # The accepted configuration contract cites the sole permitted
        # vocabulary inside Markdown backticks (`arn:aws:iam::aws:policy/...`);
        # prose may also close a parenthesis directly after it. The exemption
        # covers the vocabulary with a trailing markup delimiter glued to the
        # scanned token (T20 #22 d3; T21 #20 d2) - R4 #29 correction.
        self.write(
            "doc.md",
            "use the `arn:aws:iam::aws:policy/...` form - the sole\n"
            "exemption (arn:aws:iam::aws:policy/ReadOnlyAccess)\n",
        )
        self.assertEqual([], run_codes("validation", self.target))

    def test_markup_quoted_live_arn_still_fires(self) -> None:
        # The trailing-delimiter allowance affects only the exemption test:
        # a non-exempt ARN inside the same markup still fires (fail closed).
        self.write("doc.md", "see `arn:aws:iam::111122223333:role/some-role`\n")
        self.assertEqual(["INV-PUBLIC-LEAK"], run_codes("validation", self.target))

    def test_account_local_arn_fires(self) -> None:
        self.write("x.yml", "role: arn:aws:iam::111122223333:role/some-role\n")
        self.assertEqual(["INV-PUBLIC-LEAK"], run_codes("validation", self.target))

    def test_generated_sso_arn_fires(self) -> None:
        self.write(
            "x.yml",
            "arn: arn:aws:sso:::permissionSet/ssoins-abc123/ps-abc123\n",
        )
        self.assertEqual(["INV-PUBLIC-LEAK"], run_codes("validation", self.target))

    def test_twelve_digit_account_id_fires_with_locator(self) -> None:
        self.write("a/x.yml", "alias: fine\naccount_id: '111122223333'\n")
        result = runner.run("validation", self.target, runner.RunConfig())
        (leak,) = result
        self.assertEqual("INV-PUBLIC-LEAK", leak.code)
        self.assertEqual("a/x.yml", leak.file_path)
        self.assertEqual("L2", leak.field_path)

    def test_identity_store_id_and_reserved_role_fire(self) -> None:
        self.write("x.md", "store d-9067abc123 and AWSReservedSSO_read_only_abc\n")
        codes = run_codes("validation", self.target)
        self.assertEqual({"INV-PUBLIC-LEAK"}, set(codes))
        self.assertEqual(2, len(codes))

    def test_leaked_value_is_never_serialized(self) -> None:
        # Redaction by omission before public serialization (T14 #19 d4b).
        self.write("x.yml", "account_id: '111122223333'\n")
        (leak,) = runner.run("validation", self.target, runner.RunConfig())
        blob = findings.serialize([leak])
        self.assertNotIn(b"111122223333", blob)
        self.assertIn(b"[omitted]", blob)


if __name__ == "__main__":
    unittest.main()
