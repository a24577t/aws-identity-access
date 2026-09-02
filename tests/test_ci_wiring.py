"""R4 #29 row-11 external checks on the CI wiring seam (validator.ci).

The wiring stages committed-byte inputs, feeds the explicit run inputs the
R2/R3 seams already accept (changed_paths, regenerated, plan_context,
inventory_fixture), serializes findings, and maps severities to exit codes
(error -> 1; deferred reports and never fails - RD-08). Behavior under test
is the wiring contract only: every deterministic validation/generation
behavior it invokes is an existing public seam with its own suite.
"""

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import ci  # noqa: E402

from tests.test_validator_plan_stage import PlanCase  # noqa: E402

HAS_GIT = shutil.which("git") is not None

DUMMY_REV = "1" * 40


def build_export(export_dir, tree_src):
    """An export directory in the transport format `ci export` produces:
    tree/ carrying committed bytes, revisions.tsv carrying last-touch
    revisions (dummy revisions suffice where no manifest is compared)."""
    export = Path(export_dir)
    shutil.copytree(tree_src, export / "tree")
    lines = []
    for path in sorted((export / "tree").rglob("*")):
        if path.is_file():
            rel = path.relative_to(export / "tree").as_posix()
            lines.append(f"{rel}\t{DUMMY_REV}")
    (export / "revisions.tsv").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return export


class ContractConstants(unittest.TestCase):
    def test_wiring_literals_equal_the_owning_constants(self) -> None:
        # ci keeps import-free literals so `export` stays stdlib-only on
        # the transport runner; they must track the owning modules exactly.
        from validator import governance_generator as gen

        self.assertEqual(gen.FIXTURE_PATH, ci.FIXTURE_REL)
        self.assertEqual(gen.CODEOWNERS_PATH, ci.CODEOWNERS_REL)
        self.assertEqual(gen.HANDLES_PATH, ci.HANDLES_REL)


class ExportedSourcesContract(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.export = build_export(
            Path(self.tmp.name) / "export", REPO / "tests" / "fixtures" / "valid")

    def test_read_ls_revision_contract(self) -> None:
        sources = ci.ExportedSources(self.export)
        rel = "governance/inventory/lab-inventory-fixture.yml"
        self.assertEqual(
            (self.export / "tree" / rel).read_bytes(), sources.read(rel))
        listing = sources.ls("access/identity-center/groups/")
        self.assertEqual(
            ["access/identity-center/groups/lab-readers.yml"], listing)
        self.assertEqual(DUMMY_REV, sources.revision(rel))
        self.assertIsNone(sources.read("no/such/path.yml"))
        self.assertIsNone(sources.revision("no/such/path.yml"))


class ValidateCommand(unittest.TestCase):
    """The `validate` check gate over the staged governed domain."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.export = build_export(
            self.base / "export", REPO / "tests" / "fixtures" / "valid")
        self.findings = self.base / "findings.json"

    def run_validate(self, *extra):
        return ci.main([
            "validate", "--export", str(self.export),
            "--findings", str(self.findings), *extra,
        ])

    def test_valid_domain_passes_with_exactly_the_deferral(self) -> None:
        self.assertEqual(0, self.run_validate())
        doc = json.loads(self.findings.read_text(encoding="utf-8"))
        codes = [(f["code"], f["severity"]) for f in doc["findings"]]
        self.assertEqual([("INV-DEFERRED", "deferred")], codes)

    def test_error_finding_fails_closed(self) -> None:
        leaky = (self.export / "tree" / "access" / "leak.md")
        leaky.write_bytes(b"role arn:aws:iam::111122223333:role/x\n")
        (self.export / "revisions.tsv").open("a", encoding="utf-8").write(
            f"access/leak.md\t{DUMMY_REV}\n")
        self.assertEqual(1, self.run_validate())
        doc = json.loads(self.findings.read_text(encoding="utf-8"))
        self.assertIn("INV-PUBLIC-LEAK", [f["code"] for f in doc["findings"]])


class PlanPreviewCommand(unittest.TestCase):
    """The `plan-preview` check: classification arms + sanitized preview."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.export = build_export(
            self.base / "export", REPO / "tests" / "fixtures" / "valid")
        self.preview = self.base / "plan-preview.md"
        self.findings = self.base / "findings.json"

    def run_preview(self, changed):
        changed_file = self.base / "changed-paths.txt"
        changed_file.write_text(
            "\n".join(changed) + "\n", encoding="utf-8", newline="\n")
        return ci.main([
            "plan-preview", "--export", str(self.export),
            "--changed-paths", str(changed_file),
            "--out", str(self.preview), "--findings", str(self.findings),
        ])

    def test_classified_change_renders_the_sanitized_preview(self) -> None:
        code = self.run_preview([
            "access/identity-center/account-assignments/lab-workload-a/"
            "lab-readers--read-only.yml",
        ])
        self.assertEqual(0, code)
        text = self.preview.read_text(encoding="utf-8")
        self.assertIn("never apply-eligible", text)
        self.assertIn("Deferred targets", text)

    def test_uncovered_changed_path_fails_closed(self) -> None:
        self.assertEqual(1, self.run_preview(["mystery.bin"]))
        doc = json.loads(self.findings.read_text(encoding="utf-8"))
        self.assertIn(
            "CLS-UNCOVERED-PATH", [f["code"] for f in doc["findings"]])


@unittest.skipUnless(HAS_GIT, "committed-byte staging reads HEAD blobs "
                              "through git (byte-identity amendment)")
class RealTreeValidate(unittest.TestCase):
    """The executable form of the R4 prerequisite: the committed governed
    domain at HEAD - including the lab inventory fixture - validates clean,
    with exactly the one recorded deferral."""

    def test_head_domain_validates_with_exactly_the_deferral(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            findings = Path(tmp) / "findings.json"
            code = ci.main(["validate", "--findings", str(findings)])
            doc = json.loads(findings.read_text(encoding="utf-8"))
            codes = [(f["code"], f["severity"]) for f in doc["findings"]]
            self.assertEqual([("INV-DEFERRED", "deferred")], codes)
            self.assertEqual(0, code)


@unittest.skipUnless(HAS_GIT, "regeneration sources are HEAD blobs and "
                              "last-touch revisions (byte-identity amendment)")
class GeneratedCheckCommand(unittest.TestCase):
    def test_head_generated_set_is_drift_free(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            findings = Path(tmp) / "findings.json"
            self.assertEqual(
                0, ci.main(["generated-check", "--findings", str(findings)]))

    def test_tampered_committed_codeowners_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            export = Path(tmp) / "export"
            self.assertEqual(0, ci.main(["export", "--out", str(export)]))
            codeowners = export / "tree" / ".github" / "CODEOWNERS"
            codeowners.write_bytes(
                codeowners.read_bytes() + b"# hand edit\n")
            findings = Path(tmp) / "findings.json"
            self.assertEqual(1, ci.main([
                "generated-check", "--export", str(export),
                "--findings", str(findings),
            ]))
            doc = json.loads(findings.read_text(encoding="utf-8"))
            self.assertIn("GEN-DRIFT", [f["code"] for f in doc["findings"]])


class LabPlanCommand(PlanCase):
    """The post-merge lab-plan derivation: plan-stage gate, authoritative
    summary, digests, and the T06 #8 d4 authorization-binding record."""

    def lab_plan(self, out_dir, mutate=None):
        context = dict(self.context)
        if mutate:
            mutate(context)
        context_file = self.target / "plan-context.json"
        context_file.write_text(
            json.dumps(context), encoding="utf-8", newline="\n")
        plan_file = self.target / "plan.bin"
        plan_file.write_bytes(b"synthetic saved plan bytes")
        return ci.main([
            "lab-plan", "--target", str(self.target),
            "--context", str(context_file), "--plan-file", str(plan_file),
            "--source-commit", "ab" * 20,
            "--expires", "2026-09-03T00:00:00Z",
            "--out-dir", str(out_dir),
        ]), plan_file

    def test_clean_context_emits_summary_digest_and_binding(self) -> None:
        out = self.target / "out"
        code, plan_file = self.lab_plan(out)
        self.assertEqual(0, code)
        summary = (out / "effective-access-summary.md").read_bytes()
        self.assertIn(b"digest of these exact bytes", summary)
        binding = json.loads(
            (out / "authorization-binding.json").read_text(encoding="utf-8"))
        self.assertEqual(
            hashlib.sha256(plan_file.read_bytes()).hexdigest(),
            binding["plan_sha256"])
        self.assertEqual(
            hashlib.sha256(summary).hexdigest(), binding["summary_sha256"])
        self.assertEqual("ab" * 20, binding["source_commit"])
        self.assertEqual(
            self.context["current_pointer"], binding["snapshot_id"])
        self.assertEqual(
            hashlib.sha256(self.fixture.read_bytes()).hexdigest(),
            binding["fixture_sha256"])
        self.assertEqual("lab", binding["deployment_scope"])
        self.assertEqual("2026-09-03T00:00:00Z", binding["expires"])
        self.assertTrue(binding["pins"])

    def test_plan_stage_error_fails_closed_without_binding(self) -> None:
        out = self.target / "out"

        def poison(context):
            context["current_pointer"] = "poisoned-pointer"

        code, _plan = self.lab_plan(out, mutate=poison)
        self.assertEqual(1, code)
        self.assertFalse((out / "authorization-binding.json").exists())


class VerifyBindingCommand(PlanCase):
    """The lab consumption rule's fail-closed verification: every bound
    input re-verified before anything else; any change invalidates."""

    def setUp(self) -> None:
        super().setUp()
        self.out = self.target / "out"
        context_file = self.target / "plan-context.json"
        context_file.write_text(
            json.dumps(self.context), encoding="utf-8", newline="\n")
        self.plan_file = self.target / "plan.bin"
        self.plan_file.write_bytes(b"synthetic saved plan bytes")
        code = ci.main([
            "lab-plan", "--target", str(self.target),
            "--context", str(context_file), "--plan-file", str(self.plan_file),
            "--source-commit", "ab" * 20,
            "--expires", "2026-09-03T00:00:00Z",
            "--out-dir", str(self.out),
        ])
        self.assertEqual(0, code)

    def verify(self, source_commit="ab" * 20, now="2026-09-02T12:00:00Z"):
        return ci.main([
            "verify-binding",
            "--binding", str(self.out / "authorization-binding.json"),
            "--plan-file", str(self.plan_file),
            "--summary", str(self.out / "effective-access-summary.md"),
            "--source-commit", source_commit,
            "--now", now,
        ])

    def test_unchanged_inputs_verify(self) -> None:
        self.assertEqual(0, self.verify())

    def test_changed_plan_bytes_invalidate(self) -> None:
        self.plan_file.write_bytes(b"different plan bytes")
        self.assertEqual(1, self.verify())

    def test_changed_summary_bytes_invalidate(self) -> None:
        summary = self.out / "effective-access-summary.md"
        summary.write_bytes(summary.read_bytes() + b"tail\n")
        self.assertEqual(1, self.verify())

    def test_different_source_commit_invalidates(self) -> None:
        self.assertEqual(1, self.verify(source_commit="cd" * 20))

    def test_expiry_fails_closed(self) -> None:
        self.assertEqual(1, self.verify(now="2026-09-04T00:00:00Z"))
