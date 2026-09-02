"""R3 #28 row-9 external checks - the two-layer deterministic plan-effect
classifier and its CLS-* codes (T20 #22 d1/d2/d5; T14 #19 catalogue).

Layer 1 classifies every recognized plan-JSON action list (T21 F8: no-op,
read, create, update, delete, both replace orders, forget) and fails closed
on anything else. The aggregate operates over the complete normalized vector.
Layer 2's contract classes (imports-only, state-removal-only,
guard-removal-no-live-change) require their configuration markers AND their
aggregate condition; every inconsistency fails closed. The pinned-provider
`forget` representation is unverified (spec 8.3): `state-removal-only`
cannot activate and a well-formed pattern fails closed as CLS-REPRESENTATION
without advancing the condition.

PR classes derive from changed paths per the T20 d2 table (CLS-UNCOVERED-PATH,
CLS-COMBINATION at validation and plan); permitted plan effects follow the
d5 matrix and composition rule (CLS-EFFECT, CLS-UNATTRIBUTABLE,
CLS-PROTECTED, CLS-REVOCATION-ACK). All inputs are synthetic and
clock-controlled; no fixture is ever planned against AWS.
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import classifier, runner  # noqa: E402

from tests.test_validator_plan_stage import PlanCase  # noqa: E402

PS_TYPE = "aws_ssoadmin_permission_set"
ATT_TYPE = "aws_ssoadmin_managed_policy_attachment"
ASN_TYPE = "aws_ssoadmin_account_assignment"

GRANT_PATH = ("access/identity-center/account-assignments/lab-workload-a/"
              "lab-readers--read-only.yml")
DEFINITION_PATH = "access/identity-center/permission-sets/read-only.yml"


def rc(address, type_, actions, after=None, before=None, importing=None,
       after_unknown=None, target_alias=None, protected=False):
    change = {"actions": list(actions)}
    if after is not None:
        change["after"] = after
    if before is not None:
        change["before"] = before
    if importing is not None:
        change["importing"] = importing
    if after_unknown is not None:
        change["after_unknown"] = after_unknown
    row = {"address": address, "type": type_, "change": change}
    if target_alias is not None:
        row["target_alias"] = target_alias
    if protected:
        row["protected"] = True
    return row


def ps_create(name="ialab-read-only", address="aws_ssoadmin_permission_set.read_only"):
    return rc(address, PS_TYPE, ["create"], after={"name": name})


def asn_create(alias="lab-workload-a",
               address="aws_ssoadmin_account_assignment.a"):
    return rc(address, ASN_TYPE, ["create"],
              after={"target_id": "111100000003"}, target_alias=alias)


class ClassifierCase(PlanCase):
    """PlanCase plus the row-9 plan section and changed-path input."""

    def with_plan(self, rows, changed_paths=None, removed_blocks=(),
                  import_blocks=(), guard_removed=False, overlay=None,
                  acknowledgements=()):
        self.context["plan"] = {
            "resource_changes": list(rows),
            "configuration": {
                "removed_blocks": list(removed_blocks),
                "import_blocks": list(import_blocks),
                "guard_removed": guard_removed,
            },
        }
        self.context["changed_paths"] = (
            [GRANT_PATH, DEFINITION_PATH] if changed_paths is None
            else list(changed_paths)
        )
        if overlay is not None:
            self.context["overlay"] = overlay
        if acknowledgements:
            self.context["revocation_acknowledgements"] = list(acknowledgements)

    def cls_codes(self, stage="plan"):
        return [c for c in self.plan_codes(stage) if c.startswith("CLS-")]


class LayerOneTable(unittest.TestCase):
    def test_every_recognized_action_class(self) -> None:
        # T21 F8 plus T20 d5: both replace orders are one class.
        self.assertEqual("no-op", classifier.action_class(["no-op"]))
        self.assertEqual("read", classifier.action_class(["read"]))
        self.assertEqual("create", classifier.action_class(["create"]))
        self.assertEqual("update", classifier.action_class(["update"]))
        self.assertEqual("delete", classifier.action_class(["delete"]))
        self.assertEqual("replace", classifier.action_class(["delete", "create"]))
        self.assertEqual("replace", classifier.action_class(["create", "delete"]))
        self.assertEqual("forget", classifier.action_class(["forget"]))

    def test_unknown_action_list_is_none(self) -> None:
        self.assertIsNone(classifier.action_class(["destroy"]))
        self.assertIsNone(classifier.action_class([]))
        self.assertIsNone(classifier.action_class(["create", "update"]))

    def test_aggregate_classes(self) -> None:
        agg = classifier.aggregate_class
        self.assertEqual("empty", agg([]))
        self.assertEqual("creates-only", agg(["create", "create"]))
        self.assertEqual("updates-only", agg(["update"]))
        self.assertEqual("deletes-only", agg(["delete"]))
        self.assertEqual("mixed", agg(["create", "delete"]))
        self.assertEqual("mixed", agg(["replace"]))

    def test_path_classification_is_the_d2_table(self) -> None:
        c = classifier.path_class
        self.assertEqual("access-grant", c(GRANT_PATH))
        self.assertEqual("access-definition", c(DEFINITION_PATH))
        self.assertEqual("access-definition",
                         c("access/identity-center/groups/lab-readers.yml"))
        self.assertEqual("verification-update",
                         c("access/identity-center/configuration/instance.yml"))
        self.assertEqual("exceptional-change",
                         c("governance/change-declarations/replace-read-only.yml"))
        self.assertEqual("platform-change", c("src/validator/runner.py"))
        self.assertEqual("platform-change", c("governance/ownership/routing.yml"))
        self.assertEqual("platform-change", c(".github/CODEOWNERS"))
        self.assertEqual("platform-change", c("docs/adr/0001-x.md"))
        self.assertEqual("platform-change", c("CLAUDE.md"))
        self.assertEqual("documentation", c("docs/guides/onboarding.md"))
        self.assertEqual("documentation", c("README.md"))
        self.assertIsNone(c("mystery/file.txt"))

    def test_root_control_paths_per_the_classification_amendment(self) -> None:
        # The accepted root-control-path classification amendment: exactly
        # these four T06 #8 d3-governed root files classify platform-change,
        # by exact path - never a root wildcard. Any other root path stays
        # fail-closed (CLS-UNCOVERED-PATH), and the pre-existing exact and
        # prefix rows are unchanged.
        c = classifier.path_class
        for path in (".gitignore", ".gitattributes", "LICENSE",
                     "aws-identity-access-poc-prompt.md"):
            self.assertEqual("platform-change", c(path), path)
        for uncovered in ("NOTICE", ".editorconfig", "LICENSE.txt",
                          "gitignore", "some.gitignore"):
            self.assertIsNone(c(uncovered), uncovered)
        classes, uncovered = classifier.classify_paths(
            [".gitignore", "NOTICE"])
        self.assertEqual({"platform-change"}, classes)
        self.assertEqual(["NOTICE"], uncovered)
        # Pre-existing behavior unchanged.
        self.assertEqual("platform-change", c("CLAUDE.md"))
        self.assertEqual("documentation", c("README.md"))
        self.assertEqual("documentation", c("CONTEXT.md"))
        self.assertEqual("access-grant", c(GRANT_PATH))


class PathArms(ClassifierCase):
    def test_uncovered_path_fires_at_validation(self) -> None:
        config = runner.RunConfig(
            inventory_fixture=self.fixture,
            changed_paths=["mystery/file.txt"],
        )
        result = runner.run("validation", self.target, config)
        self.assertIn("CLS-UNCOVERED-PATH", [f.code for f in result])

    def test_covered_paths_are_clean_at_validation(self) -> None:
        config = runner.RunConfig(
            inventory_fixture=self.fixture,
            changed_paths=[GRANT_PATH, DEFINITION_PATH],
        )
        result = runner.run("validation", self.target, config)
        self.assertEqual([], [f.code for f in result
                              if f.code.startswith("CLS-")])

    def test_declaration_combined_with_access_surface_fires(self) -> None:
        # d1: a PR must not introduce a declaration and execute its
        # exceptional change simultaneously.
        config = runner.RunConfig(
            inventory_fixture=self.fixture,
            changed_paths=[
                "governance/change-declarations/replace-read-only.yml",
                GRANT_PATH,
            ],
        )
        result = runner.run("validation", self.target, config)
        self.assertIn("CLS-COMBINATION", [f.code for f in result])

    def test_uncovered_path_fires_at_plan_too(self) -> None:
        self.with_plan([], changed_paths=["mystery/file.txt"])
        self.assertEqual(["CLS-UNCOVERED-PATH"], self.cls_codes())


class GreenPaths(ClassifierCase):
    def test_composed_grant_and_definition_creates_plan_is_clean(self) -> None:
        self.with_plan([
            ps_create(),
            rc("aws_ssoadmin_managed_policy_attachment.read_only", ATT_TYPE,
               ["create"]),
            asn_create(),
        ])
        self.assertEqual([], self.cls_codes())

    def test_empty_plan_is_clean_for_any_matched_class(self) -> None:
        self.with_plan(
            [], changed_paths=["access/identity-center/configuration/instance.yml"]
        )
        self.assertEqual([], self.cls_codes())

    def test_read_rows_are_separated_never_mutation(self) -> None:
        # d5: read/data-source refresh actions are excluded from the mutation
        # aggregate under an explicit deterministic rule - listed, not dropped.
        self.with_plan([
            rc("data.aws_ssoadmin_instances.this", "aws_ssoadmin_instances",
               ["read"]),
        ], changed_paths=["access/identity-center/configuration/instance.yml"])
        self.assertEqual([], self.cls_codes())

    def test_acknowledged_assignment_removal_is_clean(self) -> None:
        self.with_plan(
            [rc("aws_ssoadmin_account_assignment.a", ASN_TYPE, ["delete"],
                before={"target_id": "111100000003"},
                target_alias="lab-workload-a")],
            changed_paths=[GRANT_PATH],
            acknowledgements=[{
                "address": "aws_ssoadmin_account_assignment.a",
                "account": "lab-workload-a",
                "group": "lab-readers",
                "permission_set": "read-only",
            }],
        )
        self.assertEqual([], self.cls_codes())


class FailClosedRows(ClassifierCase):
    def test_unknown_action_list_fails_closed(self) -> None:
        self.with_plan([rc("aws_ssoadmin_permission_set.x", PS_TYPE,
                           ["provision"])])
        self.assertEqual(["CLS-UNKNOWN-ACTION"], self.cls_codes())

    def test_unresolved_required_value_fails_closed(self) -> None:
        # The deployed Name is required for the protected-resource check;
        # unknown-at-plan means classification cannot be established.
        row = rc("aws_ssoadmin_permission_set.x", PS_TYPE, ["create"],
                 after={}, after_unknown={"name": True})
        self.with_plan([row], changed_paths=[DEFINITION_PATH])
        self.assertEqual(["CLS-UNRESOLVED-VALUE"], self.cls_codes())

    def test_protected_prefix_violation(self) -> None:
        self.with_plan([ps_create(name="legacy-admin")],
                       changed_paths=[DEFINITION_PATH])
        self.assertEqual(["CLS-PROTECTED"], self.cls_codes())

    def test_protected_preexisting_marker(self) -> None:
        row = ps_create()
        row["protected"] = True
        self.with_plan([row], changed_paths=[DEFINITION_PATH])
        self.assertEqual(["CLS-PROTECTED"], self.cls_codes())

    def test_effect_targeting_a_deferred_alias(self) -> None:
        self.with_plan([asn_create(alias="lab-requested")],
                       changed_paths=[GRANT_PATH])
        self.assertEqual(["CLS-EFFECT"], self.cls_codes())

    def test_unattributable_resource_type(self) -> None:
        self.with_plan([rc("aws_iam_role.x", "aws_iam_role", ["create"],
                           after={"name": "ialab-x"})])
        self.assertEqual(["CLS-UNATTRIBUTABLE"], self.cls_codes())

    def test_row_outside_the_matched_classes(self) -> None:
        # An assignment create with only access-definition matched.
        self.with_plan([asn_create()], changed_paths=[DEFINITION_PATH])
        self.assertEqual(["CLS-UNATTRIBUTABLE"], self.cls_codes())

    def test_forbidden_action_for_the_matched_class(self) -> None:
        # d5 matrix: access-definition never deletes outside the overlay.
        self.with_plan(
            [rc("aws_ssoadmin_permission_set.read_only", PS_TYPE, ["delete"],
                before={"name": "ialab-read-only"})],
            changed_paths=[DEFINITION_PATH],
        )
        self.assertEqual(["CLS-EFFECT"], self.cls_codes())

    def test_replace_is_never_permitted_for_slice_classes(self) -> None:
        self.with_plan(
            [rc("aws_ssoadmin_permission_set.read_only", PS_TYPE,
                ["delete", "create"], after={"name": "ialab-read-only"},
                before={"name": "ialab-read-only"})],
            changed_paths=[DEFINITION_PATH],
        )
        self.assertEqual(["CLS-EFFECT"], self.cls_codes())

    def test_unacknowledged_assignment_delete(self) -> None:
        self.with_plan(
            [rc("aws_ssoadmin_account_assignment.a", ASN_TYPE, ["delete"],
                before={"target_id": "111100000003"},
                target_alias="lab-workload-a")],
            changed_paths=[GRANT_PATH],
        )
        self.assertEqual(["CLS-REVOCATION-ACK"], self.cls_codes())


class ForgetAndMarkers(ClassifierCase):
    def forget_row(self, address="aws_ssoadmin_permission_set.old"):
        return rc(address, PS_TYPE, ["forget"],
                  before={"name": "ialab-old"})

    def test_well_formed_state_removal_cannot_activate(self) -> None:
        # Ticket row 9: state-removal-only cannot activate and
        # CLS-REPRESENTATION fails closed without advancing the condition.
        self.with_plan([self.forget_row()],
                       removed_blocks=["aws_ssoadmin_permission_set.old"],
                       changed_paths=[DEFINITION_PATH])
        self.assertEqual(["CLS-REPRESENTATION"], self.cls_codes())

    def test_forget_combined_with_live_mutation(self) -> None:
        self.with_plan([self.forget_row(), ps_create()],
                       removed_blocks=["aws_ssoadmin_permission_set.old"])
        self.assertEqual(["CLS-FORGET-PATTERN"], self.cls_codes())

    def test_forget_without_its_removed_block(self) -> None:
        self.with_plan([self.forget_row()], changed_paths=[DEFINITION_PATH])
        self.assertEqual(["CLS-FORGET-PATTERN"], self.cls_codes())

    def test_removed_block_with_a_different_representation(self) -> None:
        # A removed-block resource planning anything but ["forget"] is a
        # representation the pinned toolchain must not emit - fail closed.
        self.with_plan(
            [rc("aws_ssoadmin_permission_set.old", PS_TYPE, ["delete"],
                before={"name": "ialab-old"})],
            removed_blocks=["aws_ssoadmin_permission_set.old"],
            changed_paths=[DEFINITION_PATH],
        )
        self.assertEqual(["CLS-REPRESENTATION"], self.cls_codes())

    def test_import_markers_with_live_mutation_mismatch(self) -> None:
        marked = rc("aws_ssoadmin_permission_set.x", PS_TYPE, ["no-op"],
                    after={"name": "ialab-x"}, importing={"id": "[omitted]"})
        self.with_plan([marked, ps_create()],
                       import_blocks=["aws_ssoadmin_permission_set.x"])
        self.assertEqual(["CLS-MARKER-MISMATCH"], self.cls_codes())

    def test_clean_imports_only_is_a_dormant_class(self) -> None:
        # imports-only computes, but the T19 rehearsal family is dormant:
        # no slice-A PR class permits it (T20 d5 matrix).
        marked = rc("aws_ssoadmin_permission_set.x", PS_TYPE, ["no-op"],
                    after={"name": "ialab-x"}, importing={"id": "[omitted]"})
        self.with_plan([marked],
                       import_blocks=["aws_ssoadmin_permission_set.x"],
                       changed_paths=[DEFINITION_PATH])
        self.assertEqual(["CLS-EFFECT"], self.cls_codes())

    def test_guard_removed_with_live_mutation_mismatch(self) -> None:
        self.with_plan([ps_create()], guard_removed=True,
                       changed_paths=[DEFINITION_PATH])
        self.assertEqual(["CLS-MARKER-MISMATCH"], self.cls_codes())


class OverlayMatrix(ClassifierCase):
    def test_retire_overlay_permits_the_declared_deletes(self) -> None:
        # exceptional-change declared retire: deletes-only with the T06
        # destroy acknowledgement travels through GOV-DECL-MATCH; the CLS
        # matrix accepts the declared kind's fixed class.
        self.with_plan(
            [rc("aws_ssoadmin_permission_set.old", PS_TYPE, ["delete"],
                before={"name": "ialab-old"})],
            changed_paths=[DEFINITION_PATH],
            overlay={"kind": "permission-set-key-replacement",
                     "phase": "retire"},
        )
        self.assertEqual([], self.cls_codes())

    def test_introduce_overlay_still_rejects_deletes(self) -> None:
        self.with_plan(
            [rc("aws_ssoadmin_permission_set.old", PS_TYPE, ["delete"],
                before={"name": "ialab-old"})],
            changed_paths=[DEFINITION_PATH],
            overlay={"kind": "permission-set-key-replacement",
                     "phase": "introduce"},
        )
        self.assertEqual(["CLS-EFFECT"], self.cls_codes())


if __name__ == "__main__":
    unittest.main()
