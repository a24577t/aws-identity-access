"""R3 #28 row-10 external checks - the effective-access generator (one
generator, two renderings; T20 #22 d3/d4) and the GEN-* checks (T20 #22 d6).

The sanitized plan-preview is fixture-alias-only and snapshot-blind; the
digest-bound summary derives from the same generator plus the explicit plan
context. Identical inputs produce identical bytes (spec 5, 8.2); every
public rendering enforces the decision-3 identifier boundary by omission or
replacement BEFORE serialization - the single permitted ARN-shaped public
vocabulary is the partition-qualified AWS-managed-policy pattern.
"""

import hashlib
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import effective_access, runner  # noqa: E402

from tests.test_validator_classifier import ClassifierCase, ps_create  # noqa: E402
from tests.test_validator_governance_families import GovTreeCase  # noqa: E402

MANIFEST = "docs/generated/generated-artifacts.yml"

ENVELOPE = (
    "---\n"
    "authority: generated\n"
    "do_not_edit: true\n"
    "generator:\n"
    "  path: src/validator/governance_generator.py\n"
    "  version: \"1\"\n"
    "sources:\n"
    "  - path: governance/ownership/routing.yml\n"
    "    revision: " + "a" * 40 + "\n"
    "target:\n"
    "  path: docs/generated/views/requester.md\n"
    "---\n\n# Requester view\n\nbody\n"
)


def manifest_for(*entries):
    lines = []
    for path, sha in sorted(entries):
        lines.extend([
            f"- target:\n    path: {path}\n    sha256: \"{sha}\"\n",
            "  generator:\n    path: src/validator/governance_generator.py\n"
            "    version: \"1\"\n",
            "  sources:\n    - path: governance/ownership/routing.yml\n"
            "      revision: " + "a" * 40 + "\n",
        ])
    return "".join(lines)


class PreviewRendering(GovTreeCase):
    def preview(self):
        return effective_access.render_preview(
            self.target,
            runner.RunConfig(inventory_fixture=self.fixture),
        )

    def test_preview_is_byte_deterministic(self) -> None:
        self.assertEqual(self.preview(), self.preview())
        self.assertIsInstance(self.preview(), bytes)

    def test_preview_carries_the_ten_field_shape(self) -> None:
        text = self.preview().decode("utf-8")
        for field in ("action", "principal", "permission", "target account",
                      "session duration", "permission boundary",
                      "persistence", "portal effect", "required reviewers",
                      "deferred targets"):
            self.assertIn(field, text.lower())

    def test_preview_boundary_constant_is_recorded(self) -> None:
        # d3 field 6: the field is kept so the ten-field shape stays honest.
        self.assertIn(b"absent for slice A", self.preview())

    def test_preview_reports_deferral_never_invalid(self) -> None:
        self.write(
            "access/identity-center/account-assignments/lab-requested/"
            "lab-readers--read-only.yml",
            "account: lab-requested\nprincipal:\n  type: GROUP\n"
            "  group: lab-readers\npermission_set: read-only\n",
        )
        text = self.preview().decode("utf-8")
        self.assertIn("deferred", text)
        self.assertNotIn("invalid", text)

    def test_preview_never_requires_a_snapshot(self) -> None:
        # Snapshot-blind by construction: no plan context exists here at all.
        self.assertIn(b"ialab-read-only", self.preview())

    def test_exempt_managed_policy_vocabulary_is_public(self) -> None:
        self.assertIn(b"arn:aws:iam::aws:policy/ReadOnlyAccess",
                      self.preview())


class SummaryRendering(ClassifierCase):
    def summary(self):
        self.with_plan([ps_create()],
                       changed_paths=["access/identity-center/"
                                      "permission-sets/read-only.yml"])
        return effective_access.render_summary(
            self.target,
            runner.RunConfig(inventory_fixture=self.fixture,
                             plan_context=self.context),
        )

    def test_summary_is_byte_deterministic_and_digestable(self) -> None:
        one, two = self.summary(), self.summary()
        self.assertEqual(one, two)
        self.assertEqual(
            hashlib.sha256(one).hexdigest(),
            effective_access.summary_digest(one),
        )

    def test_summary_carries_the_binding_fields(self) -> None:
        text = self.summary().decode("utf-8")
        self.assertIn(self.context["current_pointer"], text)  # snapshot_id
        self.assertIn("fixture", text.lower())
        self.assertIn("1.15.7", text)     # Terraform pin (T15 d13)
        self.assertIn("6.53.0", text)     # provider pin
        self.assertIn("enforcement", text.lower())

    def test_summary_redacts_every_live_identifier_shape(self) -> None:
        # The synthetic plan context carries account IDs, an instance ARN,
        # and an identity-store id; none may survive public serialization.
        blob = self.summary()
        self.assertNotIn(b"111100000003", blob)
        self.assertNotIn(b"arn:aws:sso", blob)
        self.assertNotIn(b"d-0000000000", blob)

    def test_sanitizer_replaces_before_serialization(self) -> None:
        line = effective_access.sanitize_public_text(
            "role arn:aws:iam::111122223333:role/x and 444455556666 leak"
        )
        self.assertNotIn("111122223333", line)
        self.assertNotIn("444455556666", line)
        self.assertIn("[omitted]", line)

    def test_sanitizer_keeps_the_exempt_vocabulary(self) -> None:
        line = effective_access.sanitize_public_text(
            "managed arn:aws:iam::aws:policy/ReadOnlyAccess stays"
        )
        self.assertIn("arn:aws:iam::aws:policy/ReadOnlyAccess", line)


class GenChecks(GovTreeCase):
    """GEN-MANIFEST / GEN-ENVELOPE / GEN-CODEOWNERS at validation;
    GEN-DRIFT at generated-ci."""

    def gen_codes(self, stage="validation", **config):
        config.setdefault("inventory_fixture", self.fixture)
        result = runner.run(stage, self.target, runner.RunConfig(**config))
        return sorted(f.code for f in result if f.code.startswith("GEN-"))

    def digest_of(self, rel):
        return hashlib.sha256((self.target / rel).read_bytes()).hexdigest()

    def write_generated_pair(self):
        self.write("docs/generated/views/requester.md", ENVELOPE)
        self.write(MANIFEST, manifest_for(
            ("docs/generated/views/requester.md",
             self.digest_of("docs/generated/views/requester.md")),
        ))

    def test_tree_without_generated_artifacts_is_clean(self) -> None:
        self.assertEqual([], self.gen_codes())

    def test_wellformed_manifest_and_envelope_are_clean(self) -> None:
        self.write_generated_pair()
        self.assertEqual([], self.gen_codes())

    def test_manifest_digest_mismatch(self) -> None:
        self.write_generated_pair()
        self.write(MANIFEST, manifest_for(
            ("docs/generated/views/requester.md", "0" * 64),
        ))
        self.assertEqual(["GEN-MANIFEST"], self.gen_codes())

    def test_generated_artifact_absent_from_manifest(self) -> None:
        self.write_generated_pair()
        self.write("docs/generated/views/orphan.md", ENVELOPE.replace(
            "path: docs/generated/views/requester.md",
            "path: docs/generated/views/orphan.md",
        ))
        self.assertEqual(["GEN-MANIFEST"], self.gen_codes())

    def test_generated_artifacts_without_any_manifest(self) -> None:
        self.write("docs/generated/views/requester.md", ENVELOPE)
        self.assertEqual(["GEN-MANIFEST"], self.gen_codes())

    def test_misordered_manifest(self) -> None:
        self.write("docs/generated/views/a.md", ENVELOPE.replace(
            "path: docs/generated/views/requester.md",
            "path: docs/generated/views/a.md",
        ))
        self.write("docs/generated/views/b.md", ENVELOPE.replace(
            "path: docs/generated/views/requester.md",
            "path: docs/generated/views/b.md",
        ))
        a = ("docs/generated/views/a.md", self.digest_of("docs/generated/views/a.md"))
        b = ("docs/generated/views/b.md", self.digest_of("docs/generated/views/b.md"))
        ordered = manifest_for(a, b)
        reversed_entries = manifest_for(b, a).replace(
            "- target:\n    path: docs/generated/views/a.md", "MARK-A"
        )
        # Build a reversed manifest by swapping the two entry blocks.
        blocks = ordered.split("- target:")
        swapped = "- target:" + blocks[2] + "- target:" + blocks[1]
        self.write(MANIFEST, swapped)
        self.assertEqual(["GEN-MANIFEST"], self.gen_codes())

    def test_envelope_missing_from_generated_markdown(self) -> None:
        self.write("docs/generated/views/requester.md", "# no envelope\n")
        self.write(MANIFEST, manifest_for(
            ("docs/generated/views/requester.md",
             self.digest_of("docs/generated/views/requester.md")),
        ))
        self.assertEqual(["GEN-ENVELOPE"], self.gen_codes())

    def test_envelope_with_whole_target_self_digest(self) -> None:
        tampered = ENVELOPE.replace(
            "target:\n  path: docs/generated/views/requester.md",
            "target:\n  path: docs/generated/views/requester.md\n"
            "  sha256: " + "0" * 64,
        )
        self.write("docs/generated/views/requester.md", tampered)
        self.write(MANIFEST, manifest_for(
            ("docs/generated/views/requester.md",
             self.digest_of("docs/generated/views/requester.md")),
        ))
        self.assertEqual(["GEN-ENVELOPE"], self.gen_codes())

    def test_codeowners_invalid_syntax(self) -> None:
        self.write(".github/CODEOWNERS", "/access/**\n")  # no owner handle
        self.write(MANIFEST, manifest_for(
            (".github/CODEOWNERS", self.digest_of(".github/CODEOWNERS")),
        ))
        self.assertEqual(["GEN-CODEOWNERS"], self.gen_codes())

    def test_codeowners_with_an_embedded_envelope(self) -> None:
        self.write(".github/CODEOWNERS",
                   "---\nauthority: generated\n---\n/access/** @a24577t\n")
        self.write(MANIFEST, manifest_for(
            (".github/CODEOWNERS", self.digest_of(".github/CODEOWNERS")),
        ))
        self.assertEqual(["GEN-CODEOWNERS"], self.gen_codes())

    def test_codeowners_absent_from_the_manifest(self) -> None:
        self.write(".github/CODEOWNERS", "/access/** @a24577t\n")
        self.write_generated_pair()
        self.assertEqual(["GEN-CODEOWNERS"], self.gen_codes())

    def test_gen_drift_fires_on_differing_regeneration(self) -> None:
        self.write_generated_pair()
        self.assertEqual(
            ["GEN-DRIFT"],
            self.gen_codes(
                stage="generated-ci",
                regenerated={"docs/generated/views/requester.md":
                             b"different regenerated bytes\n"},
            ),
        )

    def test_gen_drift_clean_on_identical_regeneration(self) -> None:
        self.write_generated_pair()
        committed = (self.target / "docs/generated/views/requester.md").read_bytes()
        self.assertEqual(
            [],
            self.gen_codes(
                stage="generated-ci",
                regenerated={"docs/generated/views/requester.md": committed},
            ),
        )


if __name__ == "__main__":
    unittest.main()
