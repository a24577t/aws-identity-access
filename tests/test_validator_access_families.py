"""R2 #27 row-4 external checks - requester-surface families KEY / ASN /
P-OOS / CFG on the row-3 core. Each test drives the public run seam over a
small committed-shape tree and asserts exact expected finding sets (T14 #19
d6 expectation-set pattern; spec 5: external behavior only).

The baseline tree mirrors the accepted R1 slice files; every negative case is
a minimal mutation of it, so each code's canonical layer is exercised at the
exact surface T14 #19 d2 assigns it.
"""

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import runner  # noqa: E402

GROUP = "key: lab-readers\nidentity_store_name: Lab Readers\n"
PS_MANAGED = (
    "key: read-only\n"
    "description: Read-only access via the AWS-managed ReadOnlyAccess policy.\n"
    "session_duration: PT8H\n"
    "managed_policies:\n"
    "  - arn:aws:iam::aws:policy/ReadOnlyAccess\n"
)
PS_INLINE = (
    "key: inventory-reader\n"
    "description: Narrow read access to basic IAM account and identity inventory.\n"
    "session_duration: PT1H\n"
    "inline_policy:\n"
    "  Version: \"2012-10-17\"\n"
    "  Statement:\n"
    "    - Sid: ReadIdentityInventory\n"
    "      Effect: Allow\n"
    "      Action:\n"
    "        - iam:GetAccountSummary\n"
    "        - iam:ListAccountAliases\n"
    "      Resource: \"*\"\n"
)
ASSIGNMENT = (
    "account: lab-workload-a\n"
    "principal:\n"
    "  type: GROUP\n"
    "  group: lab-readers\n"
    "permission_set: read-only\n"
)
INSTANCE = (
    "instance_type: organization\n"
    "primary_region: us-east-1\n"
    "additional_regions: []\n"
    "identity_source:\n"
    "  type: identity-center-default\n"
    "delegated_administrator: lab-tooling\n"
    "owner: identity-platform\n"
)
FIXTURE = (
    "source: lab-fixture\n"
    "accounts:\n"
    "  - { alias: lab-management, class: management,        status: active,    intended_classification: none }\n"
    "  - { alias: lab-tooling,    class: role-host,         status: active,    intended_classification: none }\n"
    "  - { alias: lab-workload-a, class: lab-workload,      status: active,    intended_classification: identity-platform }\n"
    "  - { alias: lab-workload-b, class: lab-workload,      status: active,    intended_classification: identity-platform }\n"
    "  - { alias: lab-requested,  class: requested-fixture, status: requested, intended_classification: identity-platform }\n"
)


class TreeCase(unittest.TestCase):
    """Build a baseline valid access/ tree in a temp dir and mutate it."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.target = Path(self.tmp.name)
        self.fixture = self.target / "governance" / "inventory" / "lab-inventory-fixture.yml"
        self.write("access/identity-center/groups/lab-readers.yml", GROUP)
        self.write("access/identity-center/permission-sets/read-only.yml", PS_MANAGED)
        self.write(
            "access/identity-center/permission-sets/inventory-reader.yml", PS_INLINE
        )
        self.write(
            "access/identity-center/account-assignments/lab-workload-a/"
            "lab-readers--read-only.yml",
            ASSIGNMENT,
        )
        self.write(
            "access/identity-center/configuration/instance.yml", INSTANCE
        )
        self.write("governance/inventory/lab-inventory-fixture.yml", FIXTURE)

    def write(self, rel, text) -> None:
        path = self.target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def remove(self, rel) -> None:
        (self.target / rel).unlink()

    def codes(self, **config):
        config.setdefault("inventory_fixture", self.fixture)
        result = runner.run("validation", self.target, runner.RunConfig(**config))
        return sorted(f.code for f in result)

    def assertCodes(self, expected, **config) -> None:
        self.assertEqual(sorted(expected), self.codes(**config))


class Baseline(TreeCase):
    def test_baseline_tree_is_clean_except_nothing(self) -> None:
        self.assertCodes([])


class KeyFamily(TreeCase):
    def test_key_grammar_uppercase(self) -> None:
        # Distinct stem (Windows checkouts are case-insensitive): the
        # uppercase defect lives in the key value.
        self.write(
            "access/identity-center/groups/uppercase-key.yml",
            "key: Upper-Case\nidentity_store_name: X\n",
        )
        self.assertCodes(["KEY-GRAMMAR"])

    def test_key_grammar_permission_set_length_bound(self) -> None:
        long_key = "a" * 25
        self.write(
            f"access/identity-center/permission-sets/{long_key}.yml",
            f"key: {long_key}\ndescription: d\nsession_duration: PT1H\n"
            "managed_policies:\n  - arn:aws:iam::aws:policy/ReadOnlyAccess\n",
        )
        self.assertCodes(["KEY-GRAMMAR"])

    def test_key_filename_stem_mismatch(self) -> None:
        self.write(
            "access/identity-center/groups/other-name.yml",
            "key: lab-readers2\nidentity_store_name: Other\n",
        )
        self.assertCodes(["KEY-FILENAME"])

    def test_key_composed_prefix_budget(self) -> None:
        # T05 d1: prefix budget over 8 including the delimiter returns to the
        # decision - checkable through the run configuration's prefix.
        self.assertCodes(
            ["KEY-COMPOSED", "KEY-COMPOSED"], resource_name_prefix="identity-lab-"
        )

    def test_key_description_bounds(self) -> None:
        self.write(
            "access/identity-center/permission-sets/read-only.yml",
            "key: read-only\ndescription: \"\"\nsession_duration: PT8H\n"
            "managed_policies:\n  - arn:aws:iam::aws:policy/ReadOnlyAccess\n",
        )
        self.assertCodes(["KEY-DESCRIPTION"])

    def test_key_idstore_name_trailing_whitespace(self) -> None:
        self.write(
            "access/identity-center/groups/lab-readers.yml",
            "key: lab-readers\nidentity_store_name: \"Lab Readers \"\n",
        )
        self.assertCodes(["KEY-IDSTORE-NAME"])

    def test_key_dup_two_files_one_identity_store_name(self) -> None:
        self.write(
            "access/identity-center/groups/lab-viewers.yml",
            "key: lab-viewers\nidentity_store_name: Lab Readers\n",
        )
        self.assertCodes(["KEY-DUP"])

    def test_key_dangling_assignment_references(self) -> None:
        self.write(
            "access/identity-center/account-assignments/lab-workload-a/"
            "ghost-group--read-only.yml",
            "account: lab-workload-a\nprincipal:\n  type: GROUP\n"
            "  group: ghost-group\npermission_set: read-only\n",
        )
        self.assertCodes(["KEY-DANGLING"])


class AsnFamily(TreeCase):
    def test_asn_shape_wrong_segment_count(self) -> None:
        self.write(
            "access/identity-center/account-assignments/lab-workload-a/"
            "lab-readers.yml",
            ASSIGNMENT,
        )
        self.assertCodes(["ASN-SHAPE"])

    def test_asn_shape_unrecognized_body_field(self) -> None:
        self.write(
            "access/identity-center/account-assignments/lab-workload-a/"
            "lab-readers--read-only.yml",
            ASSIGNMENT + "status: active\n",
        )
        self.assertCodes(["ASN-SHAPE"])

    def test_asn_user_fires_the_approved_pair(self) -> None:
        # The one intentional dual-family exception (T10 d7): USER principal
        # triggers exactly {ASN-SHAPE, P-OOS-USER}.
        self.write(
            "access/identity-center/account-assignments/lab-workload-a/"
            "lab-readers--read-only.yml",
            "account: lab-workload-a\nprincipal:\n  type: USER\n"
            "  group: lab-readers\npermission_set: read-only\n",
        )
        self.assertCodes(["ASN-SHAPE", "P-OOS-USER"])

    def test_asn_account_alias_directory_grammar(self) -> None:
        # Underscores violate the alias grammar (a distinct directory name:
        # Windows checkouts are case-insensitive, so no case variant).
        self.write(
            "access/identity-center/account-assignments/lab_workload_x/"
            "lab-readers--read-only.yml",
            "account: lab_workload_x\nprincipal:\n  type: GROUP\n"
            "  group: lab-readers\npermission_set: read-only\n",
        )
        self.assertCodes(["ASN-ACCOUNT-ALIAS"])

    def test_asn_agreement_directory_vs_account(self) -> None:
        self.write(
            "access/identity-center/account-assignments/lab-workload-b/"
            "lab-readers--read-only.yml",
            ASSIGNMENT,  # account: lab-workload-a inside lab-workload-b/
        )
        self.assertCodes(["ASN-AGREEMENT"])


class ProfileFamily(TreeCase):
    def test_poos_path_all_six_surfaces(self) -> None:
        surfaces = [
            "access/iam/users/someone.yml",
            "access/deployments/fleet-roles/role.yml",
            "access/identity-center/identity-source/okta.yml",
            "access/identity-center/bootstrap/step.md",
            "governance/exceptions/e.yml",
            "governance/runtime-mutations/m.yml",
        ]
        for rel in surfaces:
            self.write(rel, "x: 1\n")
        self.assertCodes(["P-OOS-PATH"] * 6)

    def test_poos_cmp_customer_managed_reference(self) -> None:
        self.write(
            "access/identity-center/permission-sets/read-only.yml",
            "key: read-only\ndescription: d\nsession_duration: PT8H\n"
            "customer_managed_policies:\n  - name: my-policy\n    path: /\n",
        )
        self.assertCodes(["P-OOS-CMP"])

    def test_poos_boundary_content(self) -> None:
        self.write(
            "access/identity-center/permission-sets/read-only.yml",
            PS_MANAGED + "permissions_boundary:\n  managed_policy_arn: x\n",
        )
        self.assertCodes(["P-OOS-BOUNDARY"])

    def test_poos_policy_form_two_managed_entries(self) -> None:
        self.write(
            "access/identity-center/permission-sets/read-only.yml",
            "key: read-only\ndescription: d\nsession_duration: PT8H\n"
            "managed_policies:\n"
            "  - arn:aws:iam::aws:policy/ReadOnlyAccess\n"
            "  - arn:aws:iam::aws:policy/ViewOnlyAccess\n",
        )
        self.assertCodes(["P-OOS-POLICY-FORM"])

    def test_poos_policy_form_both_forms(self) -> None:
        self.write(
            "access/identity-center/permission-sets/read-only.yml",
            PS_MANAGED
            + "inline_policy:\n  Version: \"2012-10-17\"\n  Statement:\n"
            "    - Effect: Allow\n      Action: [\"iam:GetAccountSummary\"]\n"
            "      Resource: \"*\"\n",
        )
        self.assertCodes(["P-OOS-POLICY-FORM"])

    def test_poos_identity_source(self) -> None:
        self.write(
            "access/identity-center/configuration/instance.yml",
            INSTANCE.replace("identity-center-default", "okta"),
        )
        self.assertCodes(["P-OOS-IDENTITY-SOURCE"])

    def test_out_of_slice_wording_is_fixed(self) -> None:
        self.write("access/iam/users/someone.yml", "x: 1\n")
        result = runner.run(
            "validation",
            self.target,
            runner.RunConfig(inventory_fixture=self.fixture),
        )
        (finding,) = [f for f in result if f.code == "P-OOS-PATH"]
        self.assertIn(
            "out of slice A \u2014 not prohibited by the domain architecture",
            finding.message,
        )


class CfgFamily(TreeCase):
    def test_cfg_fields_unknown_field(self) -> None:
        self.write(
            "access/identity-center/configuration/instance.yml",
            INSTANCE + "region_note: extra\n",
        )
        self.assertCodes(["CFG-FIELDS"])

    def test_cfg_vocab_account_instance(self) -> None:
        self.write(
            "access/identity-center/configuration/instance.yml",
            INSTANCE.replace("organization", "account"),
        )
        self.assertCodes(["CFG-VOCAB"])

    def test_cfg_region(self) -> None:
        self.write(
            "access/identity-center/configuration/instance.yml",
            INSTANCE.replace("us-east-1", "us-west-2"),
        )
        self.assertCodes(["CFG-REGION"])

    def test_cfg_verification_partial_block(self) -> None:
        self.write(
            "access/identity-center/configuration/instance.yml",
            INSTANCE + "verification:\n  snapshot_id: \"" + "a" * 64 + "\"\n",
        )
        self.assertCodes(["CFG-VERIFICATION"])

    def test_cfg_verification_bad_hex(self) -> None:
        self.write(
            "access/identity-center/configuration/instance.yml",
            INSTANCE
            + "verification:\n"
            + "  verified_at: \"2026-08-28T00:00:00Z\"\n"
            + "  snapshot_id: \"ZZ" + "a" * 62 + "\"\n",
        )
        self.assertCodes(["CFG-VERIFICATION"])

    def test_cfg_verification_calendar_validity(self) -> None:
        # Amendment 4: pattern-valid but calendar-impossible timestamps are
        # the validator's clock-free duty.
        self.write(
            "access/identity-center/configuration/instance.yml",
            INSTANCE
            + "verification:\n"
            + "  verified_at: \"2026-02-30T00:00:00Z\"\n"
            + "  snapshot_id: \"" + "a" * 64 + "\"\n",
        )
        self.assertCodes(["CFG-VERIFICATION"])


if __name__ == "__main__":
    unittest.main()
