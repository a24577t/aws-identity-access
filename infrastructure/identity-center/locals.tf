# Governed-source consumption (spec 3 W8): the entire resource model is
# derived from the committed requester surface under access/ and the
# labeled lab inventory fixture - never from hand-authored resource
# literals. Validation of those sources is the validator's (the merged
# `validate` check gates every PR before this root can consume it); the
# preconditions in main.tf re-assert only the mutation boundary this root
# itself must never cross.

locals {
  repo_root = "${path.module}/../.."

  # T20 #22 d7: the decoded plan-context evidence and everything derived
  # from it is sensitive - it reaches no public artifact. jsondecode of a
  # missing or malformed document fails the plan (fail closed).
  plan_context = sensitive(jsondecode(file(var.plan_context_file)))

  # T09 #12 snapshot body: accounts carry the alias-to-account binding;
  # an unbound (requested) entry carries no account id (T16 #11 d8). A
  # referenced alias with no binding fails the plan at derivation below.
  snapshot_accounts = try(
  local.plan_context.snapshot.envelope.body.accounts, [])
  account_bindings = {
    for entry in local.snapshot_accounts :
    entry.alias => entry.account_id
    if try(entry.binding, "") != "unbound"
  }

  fixture = yamldecode(file(
  "${local.repo_root}/governance/inventory/lab-inventory-fixture.yml"))
  fixture_accounts = { for entry in local.fixture.accounts : entry.alias => entry }

  permission_set_dir = "${local.repo_root}/access/identity-center/permission-sets"
  permission_sets = {
    for name in fileset(local.permission_set_dir, "*.yml") :
    trimsuffix(name, ".yml") =>
    yamldecode(file("${local.permission_set_dir}/${name}"))
  }

  group_dir = "${local.repo_root}/access/identity-center/groups"
  groups = {
    for name in fileset(local.group_dir, "*.yml") :
    trimsuffix(name, ".yml") =>
    yamldecode(file("${local.group_dir}/${name}"))
  }

  assignment_dir = "${local.repo_root}/access/identity-center/account-assignments"
  assignment_docs = {
    for name in fileset(local.assignment_dir, "*/*.yml") :
    trimsuffix(name, ".yml") => merge(
      yamldecode(file("${local.assignment_dir}/${name}")),
      { account_dir = dirname(name) },
    )
  }

  # T16 #11 d8 / RD-08: a requested alias defers - it is omitted from the
  # applicable saved plan (the effective-access summary reports it as
  # deferred). Every other boundary defect fails the plan through the
  # main.tf preconditions, never silently.
  active_assignments = {
    for key, doc in local.assignment_docs :
    key => doc
    if try(local.fixture_accounts[doc.account].status, "") != "requested"
  }

  # T15 #10 d8: the single point of deployed-name derivation.
  resource_name_prefix = "ialab-"

  # T15 #10 d8: the four coexistence tags on POC-managed permission sets
  # (markers, never reconciliation-ownership authority - ADR-0009).
  permission_set_tags = {
    project     = "aws-identity-access"
    environment = "lab"
    managed-by  = "aws-identity-access-terraform"
    owner       = "identity-platform"
  }

  # One attachment resource per (permission set, AWS-managed policy ARN)
  # pair; the map key uses the policy's terminal name segment, which is
  # part of the T21 #20 d2 partition-qualified configuration vocabulary.
  managed_policy_attachments = merge([
    for key, ps in local.permission_sets : {
      for policy_arn in try(ps.managed_policies, []) :
      "${key}:${element(split("/", policy_arn), length(split("/", policy_arn)) - 1)}" =>
      { set = key, policy_arn = policy_arn }
    }
  ]...)

  inline_policies = {
    for key, ps in local.permission_sets :
    key => ps if try(ps.inline_policy, null) != null
  }
}
