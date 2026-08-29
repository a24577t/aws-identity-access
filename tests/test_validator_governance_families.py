"""R2 #27 row-4 external checks - FIX / GOV / DOC families and the INV
validation arms over the fixture surface, on the row-3 core.

The baseline extends the access-family baseline with the governance registry,
review classes, and routing table (mirroring the accepted R1 content), so the
canonical layers of T14 #19 d2 are exercised on committed-shape trees.
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import runner  # noqa: E402

from tests.test_validator_access_families import FIXTURE, TreeCase  # noqa: E402

PRINCIPAL = (
    "key: identity-platform\nkind: role\n"
    "description: The identity-platform owner role.\n"
)
REVIEW_CLASS = (
    "key: identity-platform\n"
    "description: Independent identity-platform review.\n"
    "satisfied_by:\n  - identity-platform\n"
)
ROUTING = (
    "unrouted: fail-closed\n"
    "routes:\n"
    "  - path: access/**\n"
    "    review_classes: [identity-platform]\n"
    "  - path: governance/**\n"
    "    review_classes: [identity-platform]\n"
    "  - path: docs/**\n"
    "    review_classes: [identity-platform]\n"
    "  - path: access/identity-center/account-assignments/*/**\n"
    "    resolution: account-delegation\n"
)
DECLARATION = (
    "schema_version: 1\n"
    "key: rename-lab-readers\n"
    "kind: group-key-rename\n"
    "owner: identity-platform\n"
    "justification: Declared exceptional change.\n"
    "change_reference: https://github.com/a24577t/aws-identity-access/issues/27\n"
    "deployment_scope: lab\n"
    "valid_from: \"2026-08-01T00:00:00Z\"\n"
    "valid_until: \"2026-10-01T00:00:00Z\"\n"
    "affected_paths:\n  - access/identity-center/groups/lab-readers.yml\n"
    "expected_plan_effect_class: empty\n"
    "from_key: lab-readers\n"
    "to_key: lab-viewers\n"
)
NORMATIVE_DOC = (
    "---\n"
    "status: accepted\n"
    "decided: 2026-08-28\n"
    "authority: normative\n"
    "scope: test scope\n"
    "decision_owner: \"Eric - human project owner and decision authority\"\n"
    "---\n\n# Doc\n"
)
INFORMATIVE_DOC = (
    "---\n"
    "authority: informative\n"
    "derives_from:\n"
    "  - https://example.invalid/pinned\n"
    "---\n\n# Guide\n"
)


class GovTreeCase(TreeCase):
    def setUp(self) -> None:
        super().setUp()
        self.write("governance/ownership/principals/identity-platform.yml",
                   PRINCIPAL)
        self.write("governance/ownership/review-classes/identity-platform.yml",
                   REVIEW_CLASS)
        self.write("governance/ownership/routing.yml", ROUTING)


class Baseline(GovTreeCase):
    def test_governance_baseline_is_clean(self) -> None:
        self.assertCodes([])


class FixFamily(GovTreeCase):
    def test_fix_fields_missing_field(self) -> None:
        # A defective extra entry isolates the code while the baseline
        # references stay satisfied by the five governed entries.
        self.write(
            "governance/inventory/lab-inventory-fixture.yml",
            FIXTURE
            + "  - { alias: lab-extra, class: role-host, status: active }\n",
        )
        self.assertCodes(["FIX-FIELDS"])

    def test_fix_fields_missing_label(self) -> None:
        self.write(
            "governance/inventory/lab-inventory-fixture.yml",
            FIXTURE.replace("source: lab-fixture\n", ""),
        )
        self.assertCodes(["FIX-FIELDS"])

    def test_fix_class_outside_vocabulary(self) -> None:
        self.write(
            "governance/inventory/lab-inventory-fixture.yml",
            FIXTURE
            + "  - { alias: lab-extra, class: sandbox, status: active,"
            " intended_classification: none }\n",
        )
        self.assertCodes(["FIX-CLASS"])

    def test_fix_alias_grammar(self) -> None:
        self.write(
            "governance/inventory/lab-inventory-fixture.yml",
            FIXTURE
            + "  - { alias: lab_extra, class: role-host, status: active,"
            " intended_classification: none }\n",
        )
        self.assertCodes(["FIX-ALIAS"])

    def test_fix_live_identifier(self) -> None:
        # FIX-LIVE canonically owns the fixture's leak semantics; the generic
        # public-content scan does not double-fire on the fixture surface.
        self.write(
            "governance/inventory/lab-inventory-fixture.yml",
            "source: lab-fixture\naccounts:\n"
            "  - { alias: lab-tooling, class: role-host, status: active,"
            " intended_classification: none, account_id: \"111122223333\" }\n",
        )
        codes = self.codes()
        self.assertIn("FIX-LIVE", codes)
        self.assertNotIn("INV-PUBLIC-LEAK", codes)

    def test_inv_dup_duplicate_alias_entry(self) -> None:
        self.write(
            "governance/inventory/lab-inventory-fixture.yml",
            FIXTURE
            + "  - { alias: lab-tooling,    class: role-host,         "
            "status: active,    intended_classification: none }\n",
        )
        self.assertCodes(["INV-DUP"])


class GovRegistry(GovTreeCase):
    def test_gov_principal_provider_handle_rejected(self) -> None:
        self.write(
            "governance/ownership/principals/identity-platform.yml",
            PRINCIPAL + "github: a24577t\n",
        )
        self.assertCodes(["GOV-PRINCIPAL"])

    def test_gov_class_unresolved_principal(self) -> None:
        self.write(
            "governance/ownership/review-classes/identity-platform.yml",
            "key: identity-platform\ndescription: d\n"
            "satisfied_by:\n  - ghost-principal\n",
        )
        self.assertCodes(["GOV-CLASS"])

    def test_gov_class_authored_enforcement_rejected(self) -> None:
        self.write(
            "governance/ownership/review-classes/identity-platform.yml",
            REVIEW_CLASS + "enforced: true\n",
        )
        self.assertCodes(["GOV-CLASS"])

    def test_gov_owner_unresolvable(self) -> None:
        self.write(
            "access/identity-center/configuration/instance.yml",
            "instance_type: organization\nprimary_region: us-east-1\n"
            "additional_regions: []\nidentity_source:\n"
            "  type: identity-center-default\n"
            "delegated_administrator: lab-tooling\nowner: ghost-owner\n",
        )
        self.assertCodes(["GOV-OWNER"])


class GovRouting(GovTreeCase):
    def test_gov_route_uncovered_path(self) -> None:
        self.write("stray/unrouted.txt", "x\n")
        self.assertCodes(["GOV-ROUTE"])

    def test_gov_route_never_a_target_account(self) -> None:
        # lab-management carries intended_classification none (T16 #11 d7).
        self.write(
            "access/identity-center/account-assignments/lab-management/"
            "lab-readers--read-only.yml",
            "account: lab-management\nprincipal:\n  type: GROUP\n"
            "  group: lab-readers\npermission_set: read-only\n",
        )
        self.assertCodes(["GOV-ROUTE"])

    def test_gov_route_unknown_review_class(self) -> None:
        self.write(
            "governance/inventory/lab-inventory-fixture.yml",
            FIXTURE.replace(
                "lab-workload-a, class: lab-workload,      status: active,    "
                "intended_classification: identity-platform",
                "lab-workload-a, class: lab-workload,      status: active,    "
                "intended_classification: ghost-class",
            ),
        )
        self.assertCodes(["GOV-ROUTE"])


class GovDeclarations(GovTreeCase):
    def test_gov_declaration_baseline_declaration_is_clean(self) -> None:
        self.write(
            "governance/change-declarations/rename-lab-readers.yml", DECLARATION
        )
        self.assertCodes([])

    def test_gov_declaration_missing_valid_until(self) -> None:
        self.write(
            "governance/change-declarations/rename-lab-readers.yml",
            DECLARATION.replace(
                "valid_until: \"2026-10-01T00:00:00Z\"\n", ""
            ),
        )
        self.assertCodes(["GOV-DECLARATION"])

    def test_gov_declaration_prohibited_field(self) -> None:
        self.write(
            "governance/change-declarations/rename-lab-readers.yml",
            DECLARATION + "approved_by: someone\n",
        )
        self.assertCodes(["GOV-DECLARATION"])

    def test_gov_declaration_calendar_invalid_timestamp(self) -> None:
        # Amendment 4: calendar-validity parsing is the R2 validator's
        # clock-free duty; the schema pattern cannot reject 2026-02-30.
        self.write(
            "governance/change-declarations/rename-lab-readers.yml",
            DECLARATION.replace("2026-08-01T00:00:00Z", "2026-02-30T00:00:00Z"),
        )
        self.assertCodes(["GOV-DECLARATION"])

    def test_gov_declaration_stem_key_mismatch(self) -> None:
        self.write(
            "governance/change-declarations/other-stem.yml", DECLARATION
        )
        self.assertCodes(["GOV-DECLARATION"])

    def test_gov_declaration_unknown_kind(self) -> None:
        self.write(
            "governance/change-declarations/rename-lab-readers.yml",
            DECLARATION.replace("kind: group-key-rename", "kind: mystery-kind"),
        )
        self.assertCodes(["GOV-DECLARATION"])


class DocFamily(GovTreeCase):
    def test_doc_normative_accepted_without_decided(self) -> None:
        self.write(
            "docs/architecture/overview.md",
            NORMATIVE_DOC.replace("decided: 2026-08-28\n", ""),
        )
        self.assertCodes(["DOC-NORMATIVE"])

    def test_doc_normative_unknown_field(self) -> None:
        self.write(
            "docs/architecture/overview.md",
            NORMATIVE_DOC.replace("---\n\n# Doc\n", "extra: field\n---\n\n# Doc\n"),
        )
        self.assertCodes(["DOC-NORMATIVE"])

    def test_doc_informative_empty_derives_from(self) -> None:
        self.write(
            "docs/guides/guide.md",
            "---\nauthority: informative\nderives_from: []\n---\n\n# G\n",
        )
        self.assertCodes(["DOC-INFORMATIVE"])

    def test_doc_informative_unresolvable_source(self) -> None:
        self.write(
            "docs/guides/guide.md",
            "---\nauthority: informative\nderives_from:\n"
            "  - docs/architecture/missing.md\n---\n\n# G\n",
        )
        self.assertCodes(["DOC-INFORMATIVE"])

    def test_doc_informative_resolvable_sources_pass(self) -> None:
        self.write("docs/architecture/overview.md", NORMATIVE_DOC)
        self.write(
            "docs/guides/guide.md",
            "---\nauthority: informative\nderives_from:\n"
            "  - docs/architecture/overview.md\n"
            "  - ADR-0001\n---\n\n# G\n",
        )
        self.write("docs/adr/0001-a-decision.md", "# ADR-0001\n")
        self.assertCodes([])

    def test_doc_scope_missing_header(self) -> None:
        self.write("docs/architecture/overview.md", "# No header\n")
        self.assertCodes(["DOC-SCOPE"])

    def test_doc_scope_supersedes_on_document(self) -> None:
        self.write(
            "docs/architecture/overview.md",
            NORMATIVE_DOC.replace(
                "---\n\n# Doc\n", "supersedes: ADR-0001\n---\n\n# Doc\n"
            ),
        )
        self.assertCodes(["DOC-SCOPE"])

    def test_doc_boundary_excludes_other_docs(self) -> None:
        self.write("docs/research/notes.md", "# No header, no finding\n")
        self.assertCodes([])


class GovCodeowners(GovTreeCase):
    HANDLES = {"identity-platform": "@a24577t"}

    def derived(self):
        return (
            "/access/** @a24577t\n"
            "/governance/** @a24577t\n"
            "/docs/** @a24577t\n"
            "/access/identity-center/account-assignments/lab-requested/** @a24577t\n"
            "/access/identity-center/account-assignments/lab-workload-a/** @a24577t\n"
            "/access/identity-center/account-assignments/lab-workload-b/** @a24577t\n"
        )

    def test_agreeing_codeowners_passes(self) -> None:
        result = runner.run(
            "generated-ci",
            self.target,
            runner.RunConfig(
                inventory_fixture=self.fixture,
                handle_mapping=self.HANDLES,
                codeowners=self.derived(),
            ),
        )
        self.assertEqual([], [f.code for f in result])

    def test_disagreeing_codeowners_fires(self) -> None:
        tampered = self.derived().replace(
            "/governance/** @a24577t", "/governance/** @someone-else"
        )
        result = runner.run(
            "generated-ci",
            self.target,
            runner.RunConfig(
                inventory_fixture=self.fixture,
                handle_mapping=self.HANDLES,
                codeowners=tampered,
            ),
        )
        self.assertEqual(
            ["GOV-CODEOWNERS"], sorted(f.code for f in result)
        )


if __name__ == "__main__":
    unittest.main()
