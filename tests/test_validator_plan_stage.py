"""R2 #27 row-4 external checks - the plan/apply-stage battery: the INV
snapshot/live verification classes (T09 #12 d10/d11/d18/d19), the PRQ
prerequisite gate (T22 #21 d3/d4), the KEY-PROTECTED pre-existing arm
(T05 #7 d5; T15 #10 d8), and the plan-side GOV codes (T06 #8 d3/d5).

Plan and apply own the clock, snapshot, evidence, and AWS-derived facts;
this validator core consumes them as the explicit plan-context input
(synthetic, clock-controlled - T14 #19 d6/C10). Identifiers below are
synthetic and format-valid, never live.
"""

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import runner  # noqa: E402

from tests.test_validator_governance_families import GovTreeCase  # noqa: E402

CLOCK = "2026-09-01T12:00:00Z"
DISCOVERED = "2026-08-28T00:46:16Z"


def canonical_id(body):
    # RFC 8785 for this body shape (sorted keys, no whitespace, UTF-8).
    blob = json.dumps(
        body, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def make_body(fixture_digest):
    return {
        "schema_version": 1,
        "kind": "lab-binding-snapshot",
        "supersedes": None,
        "fixture": {
            "path": "governance/inventory/lab-inventory-fixture.yml",
            "digest": fixture_digest,
            "source_commit": "0" * 40,
        },
        "discovered_at": DISCOVERED,
        "producer": {"identity_type": "iam-user", "account_alias": "lab-tooling"},
        "organization": {
            "organization_id": "o-synth000abc",
            "feature_set": "ALL",
            "root_id": "r-syn0",
            "management_account_alias": "lab-management",
        },
        "identity_center": {
            "instance_arn": "arn:aws:sso:::instance/ssoins-0000000000000000",
            "identity_store_id": "d-0000000000",
            "region": "us-east-1",
            "delegated_admin_alias": "lab-tooling",
        },
        "accounts": [
            {"alias": "lab-management", "live_name": "synth-management",
             "account_id": "111100000001", "state": "ACTIVE",
             "joined_method": "CREATED", "joined_timestamp": DISCOVERED,
             "ou": {"ou_id": "r-syn0", "logical_class": "root"},
             "tags_verified": True},
            {"alias": "lab-tooling", "live_name": "synth-tooling",
             "account_id": "111100000002", "state": "ACTIVE",
             "joined_method": "INVITED", "joined_timestamp": DISCOVERED,
             "ou": {"ou_id": "ou-syn0-lab00000", "logical_class": "lab"},
             "tags_verified": True},
            {"alias": "lab-workload-a", "live_name": "synth-workload-a",
             "account_id": "111100000003", "state": "ACTIVE",
             "joined_method": "CREATED", "joined_timestamp": DISCOVERED,
             "ou": {"ou_id": "ou-syn0-lab00000", "logical_class": "lab"},
             "tags_verified": True},
            {"alias": "lab-workload-b", "live_name": "synth-workload-b",
             "account_id": "111100000004", "state": "ACTIVE",
             "joined_method": "CREATED", "joined_timestamp": DISCOVERED,
             "ou": {"ou_id": "ou-syn0-lab00000", "logical_class": "lab"},
             "tags_verified": True},
            {"alias": "lab-requested", "binding": "unbound"},
        ],
    }


def live_for(body):
    return {
        "accounts": [
            {"Id": e["account_id"], "Name": e["live_name"], "State": "ACTIVE",
             "ParentOuId": e["ou"]["ou_id"]}
            for e in body["accounts"]
            if e.get("binding") != "unbound"
        ],
        "pagination_complete": True,
        "api_error": None,
        "lab_ou_account_ids": ["111100000002", "111100000003", "111100000004"],
        "organization": {
            "organization_id": "o-synth000abc",
            "root_id": "r-syn0",
            "management_account_id": "111100000001",
        },
        "identity_center": {
            "instance_arn": "arn:aws:sso:::instance/ssoins-0000000000000000",
            "identity_store_id": "d-0000000000",
            "delegated_admin_account_id": "111100000002",
            "delegated_admin_service": "sso.amazonaws.com",
        },
        "permission_set_names": [],
        "groups": {
            "Lab Readers": {
                "resolved": True, "multiple": False, "display_name_exact": True,
            }
        },
        "prerequisites": {
            "instance": "pass", "identity_store": "pass",
            "delegated_admin": "pass",
        },
    }


class PlanCase(GovTreeCase):
    def setUp(self) -> None:
        super().setUp()
        fixture_digest = hashlib.sha256(self.fixture.read_bytes()).hexdigest()
        self.body = make_body(fixture_digest)
        snapshot_id = canonical_id(self.body)
        self.context = {
            "clock": CLOCK,
            "snapshot": {
                "envelope": {"snapshot_id": snapshot_id, "body": self.body},
                "object_key_id": snapshot_id,
                "metadata_id": snapshot_id,
                "sidecar_id": snapshot_id,
            },
            "current_pointer": snapshot_id,
            "pointer_changed": False,
            "live": live_for(self.body),
            "attestations": [],
            "enforcement": [],
            "review_events": [],
            "co_satisfaction_rule": False,
            "operation": None,
        }
        self.write(
            "access/identity-center/configuration/instance.yml",
            "instance_type: organization\nprimary_region: us-east-1\n"
            "additional_regions: []\nidentity_source:\n"
            "  type: identity-center-default\n"
            "delegated_administrator: lab-tooling\nowner: identity-platform\n"
            "verification:\n"
            f"  verified_at: \"{DISCOVERED}\"\n"
            f"  snapshot_id: \"{snapshot_id}\"\n",
        )

    def rebind(self) -> None:
        """Recompute every digest location after mutating the body, and keep
        the committed verification reference pointing at the new current
        snapshot (the reference is a separate surface - T14 #19 d4a)."""
        snapshot_id = canonical_id(self.body)
        snap = self.context["snapshot"]
        snap["envelope"]["snapshot_id"] = snapshot_id
        snap["object_key_id"] = snapshot_id
        snap["metadata_id"] = snapshot_id
        snap["sidecar_id"] = snapshot_id
        self.context["current_pointer"] = snapshot_id
        self.write(
            "access/identity-center/configuration/instance.yml",
            "instance_type: organization\nprimary_region: us-east-1\n"
            "additional_regions: []\nidentity_source:\n"
            "  type: identity-center-default\n"
            "delegated_administrator: lab-tooling\nowner: identity-platform\n"
            "verification:\n"
            f"  verified_at: \"{self.body['discovered_at']}\"\n"
            f"  snapshot_id: \"{snapshot_id}\"\n",
        )

    def plan_codes(self, stage="plan"):
        result = runner.run(
            stage,
            self.target,
            runner.RunConfig(
                inventory_fixture=self.fixture, plan_context=self.context
            ),
        )
        return sorted(f.code for f in result)


class GreenPath(PlanCase):
    def test_consistent_context_yields_only_the_deferral(self) -> None:
        # The requested alias is referenced by no assignment here; a fully
        # consistent context is clean at plan and at apply.
        self.assertEqual([], self.plan_codes("plan"))
        self.assertEqual([], self.plan_codes("apply"))


class InvPlanBattery(PlanCase):
    def test_inv_missing_no_snapshot(self) -> None:
        self.context["snapshot"] = None
        self.assertIn("INV-MISSING", self.plan_codes())

    def test_inv_missing_no_pointer(self) -> None:
        self.context["current_pointer"] = None
        self.assertIn("INV-MISSING", self.plan_codes())

    def test_inv_stale_pointer_changed(self) -> None:
        self.context["pointer_changed"] = True
        self.assertEqual(["INV-STALE"], self.plan_codes())

    def test_inv_stale_backstop_expired(self) -> None:
        self.context["clock"] = "2026-11-27T00:46:17Z"  # past 90 days
        self.assertEqual(["INV-STALE"], self.plan_codes())

    def test_inv_digest_sidecar_mismatch(self) -> None:
        self.context["snapshot"]["sidecar_id"] = "f" * 64
        self.assertEqual(["INV-DIGEST"], self.plan_codes())

    def test_inv_digest_fixture_bytes_mismatch(self) -> None:
        self.body["fixture"]["digest"] = "e" * 64
        self.rebind()
        self.assertEqual(["INV-DIGEST"], self.plan_codes())

    def test_inv_boundary_schema_version(self) -> None:
        self.body["schema_version"] = 2
        self.rebind()
        self.assertEqual(["INV-BOUNDARY"], self.plan_codes())

    def test_inv_boundary_region_projection(self) -> None:
        self.body["identity_center"]["region"] = "us-west-2"
        self.rebind()
        self.assertEqual(["INV-BOUNDARY"], self.plan_codes())

    def test_inv_unbound_active_alias(self) -> None:
        self.body["accounts"] = [
            e for e in self.body["accounts"] if e["alias"] != "lab-workload-b"
        ]
        self.rebind()
        self.context["live"] = live_for(self.body)
        self.assertEqual(["INV-UNBOUND"], self.plan_codes())

    def test_inv_state_not_active(self) -> None:
        self.context["live"]["accounts"][3]["State"] = "SUSPENDED"
        self.assertEqual(["INV-STATE"], self.plan_codes())

    def test_inv_rename_live_name(self) -> None:
        self.context["live"]["accounts"][2]["Name"] = "renamed-elsewhere"
        self.assertEqual(["INV-RENAME"], self.plan_codes())

    def test_inv_ou_moved(self) -> None:
        self.context["live"]["accounts"][2]["ParentOuId"] = "ou-syn0-other000"
        self.assertEqual(["INV-OU"], self.plan_codes())

    def test_inv_dup_duplicate_binding(self) -> None:
        dup = copy.deepcopy(self.body["accounts"][2])
        dup["alias"] = "lab-workload-b"
        self.body["accounts"][3] = dup
        self.rebind()
        self.assertIn("INV-DUP", self.plan_codes())

    def test_inv_unaliased_lab_ou_account(self) -> None:
        self.context["live"]["accounts"].append(
            {"Id": "111100000009", "Name": "synth-stray", "State": "ACTIVE",
             "ParentOuId": "ou-syn0-lab00000"}
        )
        self.context["live"]["lab_ou_account_ids"].append("111100000009")
        self.assertEqual(["INV-UNALIASED"], self.plan_codes())

    def test_inv_partial_pagination(self) -> None:
        self.context["live"]["pagination_complete"] = False
        self.assertEqual(["INV-PARTIAL"], self.plan_codes())

    def test_inv_prohibited_field_status_key(self) -> None:
        self.body["accounts"][2]["Status"] = "ACTIVE"
        self.rebind()
        self.assertEqual(["INV-PROHIBITED-FIELD"], self.plan_codes())

    def test_inv_prohibited_field_requested_bound(self) -> None:
        self.body["accounts"][4] = {
            "alias": "lab-requested", "binding": "unbound",
            "live_name": "synth-leaked",
        }
        self.rebind()
        self.assertEqual(["INV-PROHIBITED-FIELD"], self.plan_codes())

    def test_inv_deferred_referenced_requested_alias(self) -> None:
        self.write(
            "access/identity-center/account-assignments/lab-requested/"
            "lab-readers--read-only.yml",
            "account: lab-requested\nprincipal:\n  type: GROUP\n"
            "  group: lab-readers\npermission_set: read-only\n",
        )
        codes = self.plan_codes()
        self.assertEqual(["INV-DEFERRED"], codes)


class PrqBattery(PlanCase):
    def test_prq_missing_block(self) -> None:
        self.write(
            "access/identity-center/configuration/instance.yml",
            "instance_type: organization\nprimary_region: us-east-1\n"
            "additional_regions: []\nidentity_source:\n"
            "  type: identity-center-default\n"
            "delegated_administrator: lab-tooling\nowner: identity-platform\n",
        )
        self.assertEqual(["PRQ-MISSING"], self.plan_codes())

    def test_prq_snapshot_reference_not_current(self) -> None:
        self.write(
            "access/identity-center/configuration/instance.yml",
            "instance_type: organization\nprimary_region: us-east-1\n"
            "additional_regions: []\nidentity_source:\n"
            "  type: identity-center-default\n"
            "delegated_administrator: lab-tooling\nowner: identity-platform\n"
            "verification:\n"
            f"  verified_at: \"{DISCOVERED}\"\n"
            f"  snapshot_id: \"{'b' * 64}\"\n",
        )
        result = runner.run(
            "plan", self.target,
            runner.RunConfig(inventory_fixture=self.fixture,
                             plan_context=self.context),
        )
        (finding,) = result
        self.assertEqual("PRQ-SNAPSHOT", finding.code)
        self.assertIn("related_inv: INV-STALE", finding.message)

    def test_prq_snapshot_verified_at_not_byte_equal(self) -> None:
        self.write(
            "access/identity-center/configuration/instance.yml",
            "instance_type: organization\nprimary_region: us-east-1\n"
            "additional_regions: []\nidentity_source:\n"
            "  type: identity-center-default\n"
            "delegated_administrator: lab-tooling\nowner: identity-platform\n"
            "verification:\n"
            "  verified_at: \"2026-08-28T00:46:16.000Z\"\n"
            f"  snapshot_id: \"{self.context['current_pointer']}\"\n",
        )
        self.assertEqual(["PRQ-SNAPSHOT"], self.plan_codes())

    def test_prq_missing_suppressed_when_snapshot_missing(self) -> None:
        # One root cause: the absent snapshot is INV-MISSING's surface; the
        # verification reference is not additionally failed (T14 #19 d4a).
        self.context["snapshot"] = None
        self.context["current_pointer"] = None
        codes = self.plan_codes()
        self.assertIn("INV-MISSING", codes)
        self.assertNotIn("PRQ-SNAPSHOT", codes)

    def test_prq_instance_and_store_and_admin(self) -> None:
        self.context["live"]["prerequisites"] = {
            "instance": "fail", "identity_store": "fail",
            "delegated_admin": "fail",
        }
        self.assertEqual(
            ["PRQ-DELEGATED-ADMIN", "PRQ-IDENTITY-STORE", "PRQ-INSTANCE"],
            self.plan_codes(),
        )

    def test_prq_delegated_admin_wrong_service_scope(self) -> None:
        self.context["live"]["identity_center"]["delegated_admin_service"] = (
            "other.amazonaws.com"
        )
        self.assertEqual(["PRQ-DELEGATED-ADMIN"], self.plan_codes())

    def test_prq_attestation_invalid(self) -> None:
        self.context["attestations"] = [
            {"characteristic": "identity-source-console",
             "snapshot_id": self.context["current_pointer"], "valid": False}
        ]
        self.assertEqual(["PRQ-ATTESTATION"], self.plan_codes())

    def test_prq_attestation_stale_binding(self) -> None:
        self.context["attestations"] = [
            {"characteristic": "identity-source-console",
             "snapshot_id": "c" * 64, "valid": True}
        ]
        self.assertEqual(["PRQ-ATTESTATION"], self.plan_codes())

    def test_prq_group_resolution_failure(self) -> None:
        self.context["live"]["groups"]["Lab Readers"]["resolved"] = False
        self.assertEqual(["PRQ-GROUP"], self.plan_codes())

    def test_prq_group_missing_result(self) -> None:
        self.context["live"]["groups"] = {}
        self.assertEqual(["PRQ-GROUP"], self.plan_codes())


class KeyProtectedPlanArm(PlanCase):
    def test_pre_existing_deployed_name_collision(self) -> None:
        self.context["live"]["permission_set_names"] = ["ialab-read-only"]
        self.assertEqual(["KEY-PROTECTED"], self.plan_codes())


class GovPlanCodes(PlanCase):
    def test_gov_enforcement_unenforced_without_exception(self) -> None:
        self.context["enforcement"] = [
            {"control": "required-pr-review", "result": "unenforced",
             "lab_exception_current": False}
        ]
        self.assertEqual(["GOV-ENFORCEMENT"], self.plan_codes())

    def test_gov_enforcement_covered_by_current_exception(self) -> None:
        self.context["enforcement"] = [
            {"control": "required-pr-review", "result": "unenforced",
             "lab_exception_current": True}
        ]
        self.assertEqual([], self.plan_codes())

    def test_gov_approval_class_double_counted_identity(self) -> None:
        self.context["review_events"] = [
            {"event": "review-1", "identity": "a24577t",
             "class": "identity-platform"},
            {"event": "review-2", "identity": "a24577t", "class": "security"},
        ]
        self.assertEqual(["GOV-APPROVAL-CLASS"], self.plan_codes())

    def test_gov_decl_match_no_trusted_declaration(self) -> None:
        self.context["operation"] = {
            "kind": "group-key-rename", "phase": None,
            "keys": ["lab-readers", "lab-viewers"], "paths": [],
            "environment": "lab", "effect_class": "empty",
            "group_id_changed": False, "aws_mutation_rows": 0,
            "delete_rows": 0, "introduce_completion_verified": False,
        }
        self.assertEqual(["GOV-DECL-MATCH"], self.plan_codes())

    def _declare_rename(self, trusted=True) -> None:
        from tests.test_validator_governance_families import DECLARATION

        self.write(
            "governance/change-declarations/rename-lab-readers.yml", DECLARATION
        )
        self.context["trusted_base_declarations"] = (
            ["rename-lab-readers"] if trusted else []
        )

    def test_gov_decl_match_trusted_rename_passes(self) -> None:
        self._declare_rename()
        self.context["operation"] = {
            "kind": "group-key-rename", "phase": None,
            "keys": ["lab-readers", "lab-viewers"],
            "paths": ["access/identity-center/groups/lab-readers.yml"],
            "environment": "lab", "effect_class": "empty",
            "group_id_changed": False, "aws_mutation_rows": 0,
            "delete_rows": 0, "introduce_completion_verified": False,
        }
        self.assertEqual([], self.plan_codes())

    def test_gov_decl_match_branch_only_declaration(self) -> None:
        self._declare_rename(trusted=False)
        self.context["operation"] = {
            "kind": "group-key-rename", "phase": None,
            "keys": ["lab-readers", "lab-viewers"],
            "paths": ["access/identity-center/groups/lab-readers.yml"],
            "environment": "lab", "effect_class": "empty",
            "group_id_changed": False, "aws_mutation_rows": 0,
            "delete_rows": 0, "introduce_completion_verified": False,
        }
        self.assertEqual(["GOV-DECL-MATCH"], self.plan_codes())

    def test_gov_decl_match_expired(self) -> None:
        self._declare_rename()
        self.context["clock"] = "2026-10-02T00:00:00Z"
        self.context["operation"] = {
            "kind": "group-key-rename", "phase": None,
            "keys": ["lab-readers", "lab-viewers"],
            "paths": ["access/identity-center/groups/lab-readers.yml"],
            "environment": "lab", "effect_class": "empty",
            "group_id_changed": False, "aws_mutation_rows": 0,
            "delete_rows": 0, "introduce_completion_verified": False,
        }
        self.assertEqual(["GOV-DECL-MATCH"], self.plan_codes())

    def test_gov_decl_match_rename_with_aws_mutation(self) -> None:
        self._declare_rename()
        self.context["operation"] = {
            "kind": "group-key-rename", "phase": None,
            "keys": ["lab-readers", "lab-viewers"],
            "paths": ["access/identity-center/groups/lab-readers.yml"],
            "environment": "lab", "effect_class": "empty",
            "group_id_changed": False, "aws_mutation_rows": 1,
            "delete_rows": 0, "introduce_completion_verified": False,
        }
        self.assertEqual(["GOV-DECL-MATCH"], self.plan_codes())

    def test_gov_decl_match_group_id_change_wrong_kind(self) -> None:
        self._declare_rename()
        self.context["operation"] = {
            "kind": "group-key-rename", "phase": None,
            "keys": ["lab-readers", "lab-viewers"],
            "paths": ["access/identity-center/groups/lab-readers.yml"],
            "environment": "lab", "effect_class": "empty",
            "group_id_changed": True, "aws_mutation_rows": 0,
            "delete_rows": 0, "introduce_completion_verified": False,
        }
        self.assertEqual(["GOV-DECL-MATCH"], self.plan_codes())


if __name__ == "__main__":
    unittest.main()
