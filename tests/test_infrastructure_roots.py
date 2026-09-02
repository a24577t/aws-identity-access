"""R5 #30 row-13 static verification of the committed Terraform roots.

The executable form of the ticket's static evidence, with zero Terraform
execution (the provider-execution condition stays open - spec 8.3): root
inventory and pins (spec 8.1; T15 #10 d13; T21 #20 F2), the T15 #10 d16
state-key/evidence-prefix layout, the d8 deployed-name derivation
`ialab-<key>` over the committed slice keys, the d6/d7 role and deny model
through deterministic rendering of the committed policy templates (spec 5:
deterministic rendering tests; no fixture is ever planned against AWS),
the ADR-0009 protected-resource boundary, the T20 #22 d7 output rules,
and the seams the merged R4 #29 workflow files consume. Static HCL
inspection only - no `terraform` command runs anywhere in this suite.
"""

import json
import re
import sys
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import leak  # noqa: E402

INFRA = REPO / "infrastructure"
ROOTS = ("bootstrap", "identity-center")
WORKFLOWS = REPO / ".github" / "workflows"
PERMISSION_SETS = REPO / "access" / "identity-center" / "permission-sets"

TERRAFORM_VERSION = "1.15.7"  # T15 #10 d13 - exact
PROVIDER_VERSION = "6.53.0"  # spec 8.1 - hashicorp/aws = 6.53.0
PROVIDER_ADDRESS = "registry.terraform.io/hashicorp/aws"
# T21 #20 F2 - the recorded lock hash the committed entry must carry.
PROVIDER_H1 = "h1:eD0xCJQCp+iQQKpU/SpMk/pGRrkF16UUJAEMCXvWCWo="

PREFIX = "ialab-"  # T15 #10 d8
STATE_KEYS = {  # T15 #10 d16
    "bootstrap": "aws-identity-access/lab/bootstrap/terraform.tfstate",
    "identity-center":
        "aws-identity-access/lab/identity-center/terraform.tfstate",
}
EVIDENCE_PREFIX = "aws-identity-access/evidence/"  # T15 #10 d16
MANAGED_BY_TAG = "aws-identity-access-terraform"  # T15 #10 d8

# T15 #10 d6 - the exact environment-bound OIDC subjects.
SUBJECTS = {
    "lab-plan": "repo:a24577t/aws-identity-access:environment:lab-plan",
    "lab": "repo:a24577t/aws-identity-access:environment:lab",
}

# The apply role's slice-A mutation surface (T15 #10 d7: only the slice-A
# sso-admin write actions; ADR-0009 resource set).
APPLY_SSO_MUTATIONS = {
    "sso:CreatePermissionSet",
    "sso:UpdatePermissionSet",
    "sso:DeletePermissionSet",
    "sso:AttachManagedPolicyToPermissionSet",
    "sso:DetachManagedPolicyFromPermissionSet",
    "sso:PutInlinePolicyToPermissionSet",
    "sso:DeleteInlinePolicyFromPermissionSet",
    "sso:CreateAccountAssignment",
    "sso:DeleteAccountAssignment",
    "sso:ProvisionPermissionSet",
    "sso:TagResource",
    "sso:UntagResource",
}

_READ_ONLY_RE = re.compile(
    r"^(organizations|sso|identitystore):(Describe|Get|List)")
_VAR_RE = re.compile(r"\$\{([a-z_]+)\}")

# Synthetic rendering inputs (spec 5: deterministic rendering; plain tokens,
# never identifier-shaped).
SYNTH = {
    "oidc_provider_arn": "OIDC-PROVIDER-TOKEN",
    "environment": "lab-plan",
    "state_bucket_arn": "STATE-BUCKET-TOKEN",
    "state_object_arn": "STATE-OBJECT-TOKEN",
    "state_lock_arn": "STATE-LOCK-TOKEN",
    "state_objects_arn": "STATE-OBJECTS-TOKEN",
    "evidence_objects_arn": "EVIDENCE-OBJECTS-TOKEN",
    "kms_key_arn": "KMS-KEY-TOKEN",
    "state_prefix": "STATE-PREFIX-TOKEN",
}


def tf_files(root):
    return sorted((INFRA / root).glob("*.tf"))


def tf_text(root):
    return "\n".join(
        p.read_text(encoding="utf-8") for p in tf_files(root))


def root_text(root):
    """Every committed text byte of one root (HCL, lock, docs, templates)."""
    parts = []
    for p in sorted((INFRA / root).rglob("*")):
        if p.is_file():
            parts.append(p.read_text(encoding="utf-8"))
    return "\n".join(parts)


def render(template_name, mapping):
    """Deterministic stand-in for templatefile(): every `${name}` must
    resolve; an unknown placeholder fails the test (fail closed)."""
    text = (INFRA / "bootstrap" / "policies" / template_name).read_text(
        encoding="utf-8")

    def substitute(match):
        key = match.group(1)
        if key not in mapping:
            raise AssertionError(
                f"{template_name}: unknown placeholder {key!r}")
        return mapping[key]

    return json.loads(_VAR_RE.sub(substitute, text))


def statements(document):
    body = document["Statement"]
    return body if isinstance(body, list) else [body]


def actions_of(statement):
    value = statement.get("Action", [])
    return [value] if isinstance(value, str) else list(value)


def resources_of(statement):
    value = statement.get("Resource", [])
    return [value] if isinstance(value, str) else list(value)


def allow_statements(document):
    return [s for s in statements(document) if s.get("Effect") == "Allow"]


def deny_statements(document):
    return [s for s in statements(document) if s.get("Effect") == "Deny"]


class RootInventory(unittest.TestCase):
    def test_exactly_the_two_roots(self) -> None:
        # Ticket #30 acceptance: both roots exist; no other roots.
        found = sorted(
            p.parent.relative_to(INFRA).parts[0]
            for p in INFRA.rglob("*.tf"))
        self.assertEqual(sorted(set(found)), sorted(ROOTS))

    def test_each_root_carries_versions_lock_and_readme(self) -> None:
        for root in ROOTS:
            base = INFRA / root
            for name in ("versions.tf", ".terraform.lock.hcl", "README.md"):
                self.assertTrue((base / name).is_file(), f"{root}/{name}")

    def test_no_execution_artifacts_committed(self) -> None:
        # Ticket #30 acceptance: no init/plan/apply output, state file, or
        # provider binary is committed.
        for p in INFRA.rglob("*"):
            rel = p.relative_to(INFRA).as_posix()
            self.assertNotIn(".terraform/", rel + "/",
                             f"execution artifact committed: {rel}")
            if p.is_file():
                self.assertFalse(
                    rel.endswith((".tfstate", ".tfplan", ".backup")),
                    f"state or plan artifact committed: {rel}")

    def test_keys_seam_holds_no_key_material(self) -> None:
        # T15 #10 d9: the public key lands only with the separately
        # authorized act that registers its private half; R5 documents the
        # seam and commits no key material of either kind.
        readme = INFRA / "keys" / "README.md"
        self.assertTrue(readme.is_file(), "infrastructure/keys/README.md")
        self.assertIn("lab-plan-encryption.pub",
                      readme.read_text(encoding="utf-8"))
        for p in INFRA.rglob("*"):
            if not p.is_file():
                continue
            self.assertFalse(
                p.suffix in (".pem", ".key", ".pub"),
                f"key material committed: {p.relative_to(INFRA)}")
            self.assertNotIn("PRIVATE KEY",
                             p.read_text(encoding="utf-8", errors="ignore"))


class PinDiscipline(unittest.TestCase):
    def test_terraform_required_version_exact(self) -> None:
        for root in ROOTS:
            versions = (INFRA / root / "versions.tf").read_text(
                encoding="utf-8")
            self.assertIn(
                f'required_version = "{TERRAFORM_VERSION}"', versions, root)

    def test_provider_pin_exact(self) -> None:
        for root in ROOTS:
            versions = (INFRA / root / "versions.tf").read_text(
                encoding="utf-8")
            self.assertIn('source  = "hashicorp/aws"', versions, root)
            self.assertIn(f'version = "= {PROVIDER_VERSION}"', versions, root)

    def test_lock_carries_exactly_the_pinned_provider_entry(self) -> None:
        for root in ROOTS:
            lock = (INFRA / root / ".terraform.lock.hcl").read_text(
                encoding="utf-8")
            providers = re.findall(r'provider "([^"]+)"', lock)
            self.assertEqual([PROVIDER_ADDRESS], providers, root)
            versions = re.findall(r'version\s*=\s*"([^"]+)"', lock)
            self.assertEqual([PROVIDER_VERSION], versions, root)
            self.assertIn(PROVIDER_H1, lock, root)


class StateAndEvidenceLayout(unittest.TestCase):
    def test_backend_is_partial_s3(self) -> None:
        # T15 #10 d16 keys with d12's boundary: the bucket is a live lab
        # identifier and never appears in committed content - the backend
        # block stays partial and the pipeline (or the documented one-time
        # local init) supplies it.
        for root in ROOTS:
            text = tf_text(root)
            self.assertRegex(text, r'backend\s+"s3"\s*\{', root)
            self.assertNotRegex(text, r'\bbucket\s*=', root)

    def test_state_key_contract_recorded(self) -> None:
        for root in ROOTS:
            text = root_text(root)
            self.assertIn(STATE_KEYS[root], text, root)
            self.assertIn("use_lockfile", text, root)

    def test_evidence_prefix_scoped_in_bootstrap(self) -> None:
        self.assertIn(EVIDENCE_PREFIX, tf_text("bootstrap"))


class DeployedNameDerivation(unittest.TestCase):
    def test_single_point_of_derivation_per_root(self) -> None:
        # T15 #10 d8 via one local per root; every use interpolates it.
        for root in ROOTS:
            occurrences = tf_text(root).count(PREFIX)
            self.assertEqual(
                1, occurrences,
                f"{root}: expected exactly one literal {PREFIX!r} "
                f"(the resource_name_prefix local), found {occurrences}")

    def test_name_expression_derives_from_the_prefix_local(self) -> None:
        self.assertRegex(
            tf_text("identity-center"),
            r'name\s*=\s*"\$\{local\.resource_name_prefix\}\$\{')

    def test_derived_names_for_the_committed_slice_keys(self) -> None:
        keys = sorted(
            yaml.safe_load(p.read_text(encoding="utf-8"))["key"]
            for p in PERMISSION_SETS.glob("*.yml"))
        self.assertEqual(["inventory-reader", "read-only"], keys)
        for key in keys:
            composed = f"{PREFIX}{key}"
            self.assertLessEqual(len(composed), 30)  # T15 #10 d8 budget
            self.assertLessEqual(len(composed), 32)  # AWS bound
            self.assertRegex(composed, r"^[\w+=,.@-]+$")


class OpenConditionsStayOpen(unittest.TestCase):
    def test_no_import_or_removed_blocks(self) -> None:
        # Spec 8.3: the `forget` representation and import-redaction
        # conditions stay unadvanced; no adoption-shaped configuration
        # (T19 #14 d2 / ADO-PHASE).
        for root in ROOTS:
            text = tf_text(root)
            self.assertNotRegex(text, r"(?m)^\s*import\s*\{", root)
            self.assertNotRegex(text, r"(?m)^\s*removed\s*\{", root)


class LeakBoundary(unittest.TestCase):
    def test_leak_scan_clean_over_infrastructure(self) -> None:
        # T15 #10 d12 / T14 #19 d4b: no live-identifier shape anywhere in
        # the committed roots; the accepted rule itself is the check.
        for p in sorted(INFRA.rglob("*")):
            if not p.is_file():
                continue
            found = list(leak.scan_text(p.read_text(encoding="utf-8")))
            self.assertEqual(
                [], found, f"leak-shaped token in {p.relative_to(REPO)}")


class RoleAndDenyModel(unittest.TestCase):
    """T15 #10 d6/d7 through deterministic rendering of the committed
    policy templates with synthetic inputs (spec 5)."""

    def test_trust_binds_the_exact_environment_subject(self) -> None:
        for environment, subject in SUBJECTS.items():
            doc = render("trust-github-environment.json.tpl",
                         dict(SYNTH, environment=environment))
            (statement,) = statements(doc)
            self.assertEqual("Allow", statement["Effect"])
            self.assertEqual("sts:AssumeRoleWithWebIdentity",
                             statement["Action"])
            self.assertEqual(SYNTH["oidc_provider_arn"],
                             statement["Principal"]["Federated"])
            equals = statement["Condition"]["StringEquals"]
            self.assertEqual(
                "sts.amazonaws.com",
                equals["token.actions.githubusercontent.com:aud"])
            self.assertEqual(
                subject, equals["token.actions.githubusercontent.com:sub"])
            self.assertNotIn("*", json.dumps(statement["Condition"]))

    def test_plan_role_allows_reads_only(self) -> None:
        doc = render("plan-role.json.tpl", SYNTH)
        permitted_exact = {
            "s3:GetObject", "s3:PutObject", "s3:DeleteObject",
            "s3:ListBucket", "kms:Decrypt", "kms:Encrypt",
            "kms:GenerateDataKey", "kms:DescribeKey",
            "sts:GetCallerIdentity",
        }
        for statement in allow_statements(doc):
            for action in actions_of(statement):
                self.assertTrue(
                    _READ_ONLY_RE.match(action) or action in permitted_exact,
                    f"plan role allows a mutation: {action}")

    def test_plan_role_state_object_is_read_only(self) -> None:
        # d6: read the state object; manage only its native lockfile; no
        # state-object Put/Delete.
        doc = render("plan-role.json.tpl", SYNTH)
        for statement in allow_statements(doc):
            actions = set(actions_of(statement))
            resources = set(resources_of(statement))
            if SYNTH["state_object_arn"] in resources:
                self.assertEqual({"s3:GetObject"}, actions,
                                 "state object must be read-only")
            if actions & {"s3:PutObject", "s3:DeleteObject"}:
                self.assertLessEqual(
                    resources,
                    {SYNTH["state_lock_arn"], SYNTH["evidence_objects_arn"]},
                    "plan-role writes outside lockfile/evidence")
            if SYNTH["evidence_objects_arn"] in resources:
                self.assertLessEqual(
                    actions, {"s3:GetObject", "s3:PutObject"},
                    "evidence objects are Get/Put only (d6)")

    def test_apply_role_mutations_are_slice_a_only(self) -> None:
        doc = render("apply-role.json.tpl", SYNTH)
        permitted_exact = APPLY_SSO_MUTATIONS | {
            "s3:GetObject", "s3:PutObject", "s3:DeleteObject",
            "s3:ListBucket", "kms:Decrypt", "kms:Encrypt",
            "kms:GenerateDataKey", "kms:DescribeKey",
            "sts:GetCallerIdentity",
        }
        seen = set()
        for statement in allow_statements(doc):
            for action in actions_of(statement):
                self.assertTrue(
                    _READ_ONLY_RE.match(action) or action in permitted_exact,
                    f"apply role allows outside the slice-A model: {action}")
                seen.add(action)
        self.assertLessEqual(APPLY_SSO_MUTATIONS, seen,
                             "slice-A mutation surface incomplete")

    def test_apply_role_tag_conditions_guard_protected_resources(self) -> None:
        # ADR-0009: pre-existing (untagged) resources stay outside every
        # allow - creates require the managed-by request tag, mutations the
        # managed-by resource tag; the plan gate remains primary (T15 d7).
        doc = render("apply-role.json.tpl", SYNTH)
        create_guard = mutate_guard = False
        for statement in allow_statements(doc):
            actions = set(actions_of(statement))
            condition = json.dumps(statement.get("Condition", {}))
            if "sso:CreatePermissionSet" in actions:
                self.assertIn("aws:RequestTag/managed-by", condition)
                self.assertIn(MANAGED_BY_TAG, condition)
                create_guard = True
            if actions & (APPLY_SSO_MUTATIONS
                          - {"sso:CreatePermissionSet"}):
                self.assertIn("aws:ResourceTag/managed-by", condition)
                self.assertIn(MANAGED_BY_TAG, condition)
                mutate_guard = True
        self.assertTrue(create_guard and mutate_guard)

    def test_apply_role_state_and_evidence_scope(self) -> None:
        doc = render("apply-role.json.tpl", SYNTH)
        for statement in allow_statements(doc):
            actions = set(actions_of(statement))
            resources = set(resources_of(statement))
            if actions & {"s3:GetObject", "s3:PutObject", "s3:DeleteObject"}:
                self.assertLessEqual(
                    resources,
                    {SYNTH["state_objects_arn"],
                     SYNTH["evidence_objects_arn"]},
                    "apply-role object access outside lab/evidence prefixes")
            if SYNTH["evidence_objects_arn"] in resources:
                self.assertLessEqual(
                    actions, {"s3:GetObject", "s3:PutObject"},
                    "evidence objects are Get/Put only (d6)")

    def test_kms_data_plane_scoped_to_the_state_key(self) -> None:
        for template in ("plan-role.json.tpl", "apply-role.json.tpl"):
            doc = render(template, SYNTH)
            for statement in allow_statements(doc):
                kms = [a for a in actions_of(statement)
                       if a.startswith("kms:")]
                if not kms:
                    continue
                self.assertEqual([SYNTH["kms_key_arn"]],
                                 resources_of(statement), template)
                self.assertIn("kms:ViaService",
                              json.dumps(statement.get("Condition", {})),
                              template)

    def test_explicit_denies_cover_the_d7_classes(self) -> None:
        doc = render("explicit-denies.json.tpl", SYNTH)
        denied = set()
        for statement in deny_statements(doc):
            denied.update(actions_of(statement))
        expected = {
            "iam:*",  # role/trust and OIDC-provider mutation (total)
            "organizations:Create*", "organizations:Delete*",
            "organizations:Update*", "organizations:Invite*",
            "organizations:Move*", "organizations:Register*",
            "organizations:Deregister*", "organizations:Close*",
            "organizations:Tag*", "organizations:Untag*",
            "organizations:Attach*", "organizations:Detach*",
            "organizations:Enable*", "organizations:Disable*",
            "organizations:Leave*", "organizations:Remove*",
            "s3:CreateBucket", "s3:DeleteBucket", "s3:PutBucketPolicy",
            "s3:DeleteBucketPolicy", "s3:PutEncryptionConfiguration",
            "kms:PutKeyPolicy", "kms:ScheduleKeyDeletion",
            "kms:CreateGrant", "kms:Create*", "kms:Delete*",
            "sso:CreateInstance", "sso:DeleteInstance",
            "sso:CreateApplication", "sso:DeleteApplication",
            "identitystore:Create*", "identitystore:Delete*",
            "identitystore:Update*", "sso-directory:*",
        }
        self.assertLessEqual(
            expected, denied,
            f"missing denies: {sorted(expected - denied)}")

    def test_s3_deny_confines_both_roles_to_their_prefixes(self) -> None:
        doc = render("explicit-denies.json.tpl", SYNTH)
        confining = [
            s for s in deny_statements(doc)
            if actions_of(s) == ["s3:*"] and "NotResource" in s
        ]
        (statement,) = confining
        not_resources = statement["NotResource"]
        for token in ("state_bucket_arn", "state_objects_arn",
                      "evidence_objects_arn"):
            self.assertIn(SYNTH[token], not_resources)

    def test_both_roles_exist_with_trust_and_denies_attached(self) -> None:
        text = tf_text("bootstrap")
        self.assertIn('resource "aws_iam_role" "lab_plan"', text)
        self.assertIn('resource "aws_iam_role" "lab_apply"', text)
        self.assertIn("trust-github-environment.json.tpl", text)
        self.assertIn("explicit-denies.json.tpl", text)
        self.assertIn('environment = "lab-plan"', text)
        self.assertIn('environment = "lab"', text)
        # The OIDC provider is referenced, never managed (d6).
        self.assertIn('data "aws_iam_openid_connect_provider"', text)
        self.assertNotIn('resource "aws_iam_openid_connect_provider"', text)


class R4Integration(unittest.TestCase):
    """The seams the merged R4 #29 workflow files consume."""

    def workflow(self, name):
        return yaml.safe_load(
            (WORKFLOWS / name).read_text(encoding="utf-8"))

    def test_workflow_terraform_root_exists_with_lock(self) -> None:
        for name in ("lab-plan.yml", "lab-apply.yml"):
            doc = self.workflow(name)
            root = REPO / doc["env"]["TERRAFORM_ROOT"]
            self.assertEqual(
                "infrastructure/identity-center",
                doc["env"]["TERRAFORM_ROOT"], name)
            self.assertTrue(root.is_dir(), name)
            self.assertTrue((root / ".terraform.lock.hcl").is_file(), name)
            self.assertEqual(
                STATE_KEYS["identity-center"], doc["env"]["STATE_KEY"], name)

    def test_keys_seam_matches_the_workflow_reference(self) -> None:
        doc = self.workflow("lab-plan.yml")
        self.assertEqual("infrastructure/keys/lab-plan-encryption.pub",
                         doc["env"]["PLAN_ENCRYPTION_PUBLIC_KEY"])

    def test_lab_plan_hands_the_retrieved_context_to_terraform(self) -> None:
        # The T09 #12 binding evidence the job already retrieves is the one
        # ratified alias-to-account source (T15 #10 d5); without it the root
        # fails closed, so the plan command must hand the retrieved file to
        # Terraform.
        doc = self.workflow("lab-plan.yml")
        (job,) = doc["jobs"].values()
        plan_runs = [s.get("run", "") for s in job["steps"]
                     if "plan -input=false" in str(s.get("run", ""))]
        (run,) = plan_runs
        self.assertIn("plan_context_file=", run)
        self.assertIn("plan-context.json", run)
        variables = (INFRA / "identity-center" / "variables.tf").read_text(
            encoding="utf-8")
        self.assertIn('variable "plan_context_file"', variables)

    def test_apply_consumes_the_saved_plan_without_variables(self) -> None:
        # T20 #22 d4: apply never re-plans; the saved plan already carries
        # every resolved value, so no -var reaches the apply command.
        text = (WORKFLOWS / "lab-apply.yml").read_text(encoding="utf-8")
        self.assertNotIn("-var", text)


class GovernedSourceConsumption(unittest.TestCase):
    def test_identity_center_reads_the_governed_surfaces(self) -> None:
        text = tf_text("identity-center")
        for rel in (
            "access/identity-center/permission-sets",
            "access/identity-center/groups",
            "access/identity-center/account-assignments",
            "governance/inventory/lab-inventory-fixture.yml",
        ):
            self.assertIn(rel, text, rel)

    def test_fail_closed_contract_strings(self) -> None:
        text = tf_text("identity-center")
        # Assignments reach lab-workload accounts only (T15 #10 d7);
        # requested aliases defer and are omitted from the plan (T16 #11
        # d8); the decoded context is marked sensitive (T20 #22 d7).
        self.assertIn('"lab-workload"', text)
        self.assertIn('"requested"', text)
        self.assertIn("sensitive(", text)
        self.assertIn("precondition", text)

    def test_group_resolution_boundary(self) -> None:
        # ADR-0007: groups are references - resolved by exact DisplayName
        # through the Identity Store data source, never created here.
        text = tf_text("identity-center")
        self.assertIn('data "aws_identitystore_group"', text)
        self.assertIn('"DisplayName"', text)
        self.assertNotIn('resource "aws_identitystore_group"', text)

    def test_permission_sets_guarded_against_destroy(self) -> None:
        self.assertIn("prevent_destroy = true", tf_text("identity-center"))


if __name__ == "__main__":
    unittest.main()
