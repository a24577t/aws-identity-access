"""R4 #29 row-11 static verification of the committed workflow files.

The executable form of the ticket's static evidence: every action pin
checked against the specification 8.1 table (full 40-hex SHA, tag as
trailing comment; the pinned action set is closed), the pinned validator
container as the only toolchain image, the T15 #10 d15 check names, stage
ordering, and environment shape, the T20 #22 / T15 #10 d12 output
boundaries (no plaintext plan published; no secret value; no live
identifier shape), and the spec 8.2 identical-commands rule. Orchestration
shape only - behavior stays in src/validator and is tested there.
"""

import re
import sys
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import leak  # noqa: E402

WORKFLOWS = REPO / ".github" / "workflows"

EXPECTED_FILES = {
    "validate.yml", "plan-preview.yml", "lab-plan.yml", "lab-apply.yml",
}

# Specification 8.1 - the closed pinned action set (adding an action is a
# platform-change PR).
PINNED_ACTIONS = {
    "actions/checkout": (
        "fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09", "v5.1.0"),
    "actions/upload-artifact": (
        "330a01c490aca151604b8cf639adc76d48f6c5d4", "v5.0.0"),
    "actions/download-artifact": (
        "634f93cb2916e3fdff6788551b99b062d0335ce0", "v5.0.0"),
    "aws-actions/configure-aws-credentials": (
        "61815dcd50bd041e203e49132bacad1fd04d2708", "v5.1.1"),
}

CONTAINER = ("python:3.12.7-slim@sha256:60d9996b6a8a3689d36db740b49f4327"
             "be3be09a21122bd02fb8895abb38b50d")
RUNNER = "ubuntu-24.04"
TERRAFORM_VERSION = "1.15.7"
# terraform_1.15.7_linux_amd64.zip per the official release SHA256SUMS
# (https://releases.hashicorp.com/terraform/1.15.7/), retrieved 2026-09-02.
TERRAFORM_ZIP_SHA256 = (
    "73bbb8f5188ad75d4fb853fd100ae4d7e146ef7af7db18776109642fdb7759d2")

_USES_RE = re.compile(r"^\s*(?:-\s+)?uses:\s*(\S+)\s*(?:#\s*(\S+))?\s*$")
_SECRET_RE = re.compile(r"\$\{\{\s*secrets\.([A-Za-z0-9_]+)\s*\}\}")


def text_of(name):
    return (WORKFLOWS / name).read_text(encoding="utf-8")


def doc_of(name):
    return yaml.safe_load(text_of(name))


def on_block(doc):
    # YAML 1.1 parses the bare key `on` as boolean True.
    return doc.get("on", doc.get(True))


def jobs_of(doc):
    return doc["jobs"]


class WorkflowInventory(unittest.TestCase):
    def test_exactly_the_four_row_11_workflow_files(self) -> None:
        self.assertTrue(WORKFLOWS.is_dir(), "no .github/workflows directory")
        found = {p.name for p in WORKFLOWS.iterdir() if p.is_file()}
        self.assertEqual(EXPECTED_FILES, found)


class PinDiscipline(unittest.TestCase):
    def test_every_action_is_pinned_by_full_sha_with_tag_comment(self) -> None:
        for name in sorted(EXPECTED_FILES):
            for line in text_of(name).splitlines():
                if "uses:" not in line:
                    continue
                match = _USES_RE.match(line)
                self.assertIsNotNone(match, f"{name}: unparseable {line!r}")
                ref, tag = match.groups()
                action, sep, sha = ref.partition("@")
                self.assertTrue(sep, f"{name}: unpinned action {ref}")
                self.assertIn(action, PINNED_ACTIONS,
                              f"{name}: action outside the 8.1 set")
                expected_sha, expected_tag = PINNED_ACTIONS[action]
                self.assertEqual(expected_sha, sha, f"{name}: {action}")
                self.assertEqual(expected_tag, tag,
                                 f"{name}: {action} tag comment")

    def test_runner_is_transport_and_container_is_the_pin(self) -> None:
        for name in sorted(EXPECTED_FILES):
            doc = doc_of(name)
            for job_id, job in jobs_of(doc).items():
                self.assertEqual(RUNNER, job.get("runs-on"),
                                 f"{name}:{job_id}")
            text = text_of(name)
            self.assertIn(CONTAINER, text, f"{name}: pinned container absent")
            for match in re.finditer(r"python:\S+", text):
                self.assertTrue(
                    CONTAINER.startswith(match.group(0))
                    or match.group(0).startswith("python:3.12.7-slim@sha256"),
                    f"{name}: unpinned python image {match.group(0)!r}")

    def test_terraform_pin_and_checksum(self) -> None:
        for name in ("lab-plan.yml", "lab-apply.yml"):
            self.assertIn(TERRAFORM_VERSION, text_of(name), name)
        self.assertIn(TERRAFORM_ZIP_SHA256, text_of("lab-plan.yml"))


class PrChecks(unittest.TestCase):
    """validate and plan-preview run for reviewed PRs, sanitized and
    credential-free; the job names are the T15 #10 d15 required checks."""

    def check_shape(self, name, job_id):
        doc = doc_of(name)
        self.assertEqual({"pull_request": None}, on_block(doc), name)
        self.assertEqual([job_id], list(jobs_of(doc)), name)
        job = jobs_of(doc)[job_id]
        self.assertNotIn("environment", job, name)
        self.assertEqual({"contents": "read"}, doc.get("permissions"), name)
        text = text_of(name)
        self.assertNotIn("aws-actions/", text, name)
        self.assertNotIn("id-token", text, name)
        self.assertNotIn("${{ secrets.", text, name)

    def test_validate_check(self) -> None:
        self.check_shape("validate.yml", "validate")

    def test_plan_preview_check(self) -> None:
        self.check_shape("plan-preview.yml", "plan-preview")


class LabPlanShape(unittest.TestCase):
    def test_post_merge_environment_job_from_exact_main(self) -> None:
        doc = doc_of("lab-plan.yml")
        self.assertEqual({"push": {"branches": ["main"]}}, on_block(doc))
        (job_id,) = list(jobs_of(doc))
        self.assertEqual("lab-plan", job_id)
        job = jobs_of(doc)[job_id]
        self.assertEqual("lab-plan", job.get("environment"))
        self.assertEqual({"contents": "read", "id-token": "write"},
                         doc.get("permissions"))
        concurrency = doc.get("concurrency") or job.get("concurrency")
        self.assertIsNotNone(concurrency, "deployment concurrency missing")
        self.assertIs(False, concurrency.get("cancel-in-progress"))

    def test_tf_log_disabled_and_plan_bytes_never_published(self) -> None:
        text = text_of("lab-plan.yml")
        self.assertIn('TF_LOG: ""', text)
        doc = doc_of("lab-plan.yml")
        (job,) = jobs_of(doc).values()
        upload_paths = [
            step.get("with", {}).get("path", "")
            for step in job["steps"]
            if str(step.get("uses", "")).startswith("actions/upload-artifact")
        ]
        self.assertTrue(upload_paths, "no evidence upload step")
        for paths in upload_paths:
            self.assertNotIn("plan.json", paths)
            for line in paths.splitlines():
                self.assertFalse(line.strip().endswith("/tfplan"),
                                 "plaintext saved plan published")
        self.assertTrue(any("tfplan.enc" in p for p in upload_paths),
                        "encrypted saved plan not published as evidence")


class LabConsumptionShape(unittest.TestCase):
    def test_dispatch_inputs_bind_the_exact_artifacts(self) -> None:
        doc = doc_of("lab-apply.yml")
        dispatch = on_block(doc)["workflow_dispatch"]
        for required in ("artifact_id", "source_commit", "summary_sha256"):
            self.assertIn(required, dispatch["inputs"])
            self.assertTrue(dispatch["inputs"][required].get("required"))

    def test_environment_order_and_secret_name_boundary(self) -> None:
        doc = doc_of("lab-apply.yml")
        (job_id,) = list(jobs_of(doc))
        job = jobs_of(doc)[job_id]
        self.assertEqual("lab", job.get("environment"))
        steps = job["steps"]

        def index_where(predicate, label):
            for index, step in enumerate(steps):
                if predicate(step):
                    return index
            self.fail(f"missing step: {label}")

        download = index_where(
            lambda s: str(s.get("uses", "")).startswith(
                "actions/download-artifact"), "download by artifact id")
        self.assertIn("artifact-ids", steps[download].get("with", {}))
        verify = index_where(
            lambda s: "verify-binding" in str(s.get("run", "")),
            "verify-binding")
        credentials = index_where(
            lambda s: str(s.get("uses", "")).startswith(
                "aws-actions/configure-aws-credentials"), "credentials")
        apply_step = index_where(
            lambda s: "apply -input=false" in str(s.get("run", "")), "apply")
        self.assertLess(download, verify)
        self.assertLess(verify, credentials,
                        "credentials must follow complete verification")
        self.assertLess(credentials, apply_step)
        self.assertEqual({"LAB_PLAN_DECRYPTION_KEY"},
                         set(_SECRET_RE.findall(text_of("lab-apply.yml"))))
        self.assertIn('TF_LOG: ""', text_of("lab-apply.yml"))


class OutputBoundary(unittest.TestCase):
    def test_no_live_identifier_shape_in_any_workflow(self) -> None:
        for name in sorted(EXPECTED_FILES):
            hits = list(leak.scan_text(text_of(name)))
            self.assertEqual([], hits, f"{name}: identifier-shaped content")

    def test_identical_commands_local_and_ci(self) -> None:
        text = text_of("validate.yml")
        for command in ("python -m unittest discover -s tests",
                        "python -m validator.ci validate",
                        "python -m validator.ci generated-check"):
            self.assertIn(command, text)
        self.assertIn("python -m validator.ci plan-preview",
                      text_of("plan-preview.yml"))
        self.assertIn("python -m validator.ci lab-plan",
                      text_of("lab-plan.yml"))
        self.assertIn("python -m validator.ci verify-binding",
                      text_of("lab-apply.yml"))
        for name in ("validate.yml", "plan-preview.yml"):
            self.assertIn("--require-hashes", text_of(name))
            self.assertIn("--network none", text_of(name))
