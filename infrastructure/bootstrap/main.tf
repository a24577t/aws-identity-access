# The one-time AWS-side bootstrap root (T15 #10 d15): the two
# repository-specific pipeline roles of the d6 access model, authored here
# and applied only under the separately authorized R7 #32 owner-executed
# bootstrap. Pipeline roles can never modify any role, trust policy, or
# OIDC provider (d6/d7) - including the resources this root manages.

provider "aws" {
  region = "us-east-1" # T15 #10 d3 - the single lab Region
}

data "aws_partition" "current" {}

# T15 #10 d6: the existing GitHub OIDC provider in role-host is
# referenced, never managed (one per account; owned by the substrate).
data "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
}

locals {
  # T15 #10 d8: the single point of deployed-name derivation.
  resource_name_prefix = "ialab-"
  plan_role_name       = "${local.resource_name_prefix}lab-plan"
  apply_role_name      = "${local.resource_name_prefix}lab-apply"

  # T15 #10 d8: the four coexistence tags (markers, never
  # reconciliation-ownership authority - ADR-0001, ADR-0009).
  tags = {
    project     = "aws-identity-access"
    environment = "lab"
    managed-by  = "aws-identity-access-terraform"
    owner       = "identity-platform"
  }

  # T15 #10 d16 object layout inside the existing state bucket. Every ARN
  # is composed from the partition data source and the sensitive inputs,
  # so no committed byte carries an identifier-shaped literal (T14 #19
  # d4b leak rule) and no live identifier is committed (T15 #10 d12).
  state_bucket_arn     = "arn:${data.aws_partition.current.partition}:s3:::${var.state_bucket}"
  state_prefix         = "aws-identity-access/lab/identity-center/*"
  state_object_arn     = "${local.state_bucket_arn}/aws-identity-access/lab/identity-center/terraform.tfstate"
  state_lock_arn       = "${local.state_object_arn}.tflock"
  state_objects_arn    = "${local.state_bucket_arn}/${local.state_prefix}"
  evidence_objects_arn = "${local.state_bucket_arn}/aws-identity-access/evidence/*"

  policy_inputs = {
    state_bucket_arn     = local.state_bucket_arn
    state_prefix         = local.state_prefix
    state_object_arn     = local.state_object_arn
    state_lock_arn       = local.state_lock_arn
    state_objects_arn    = local.state_objects_arn
    evidence_objects_arn = local.evidence_objects_arn
    kms_key_arn          = var.state_kms_key_arn
  }
}

# --- plan role (T15 #10 d6: read-only saved-plan producer) ---

resource "aws_iam_role" "lab_plan" {
  name        = local.plan_role_name
  description = "aws-identity-access read-only plan role; assumable only by the lab-plan environment subject (T15 #10 d6)."
  assume_role_policy = templatefile(
    "${path.module}/policies/trust-github-environment.json.tpl",
    {
      oidc_provider_arn = data.aws_iam_openid_connect_provider.github.arn
      environment       = "lab-plan"
    }
  )
  tags = local.tags

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_iam_role_policy" "lab_plan_access" {
  name   = "access-model"
  role   = aws_iam_role.lab_plan.id
  policy = templatefile("${path.module}/policies/plan-role.json.tpl", local.policy_inputs)
}

resource "aws_iam_role_policy" "lab_plan_denies" {
  name   = "explicit-denies"
  role   = aws_iam_role.lab_plan.id
  policy = templatefile("${path.module}/policies/explicit-denies.json.tpl", local.policy_inputs)
}

# --- apply role (T15 #10 d6: slice-A mutations of the approved plan only) ---

resource "aws_iam_role" "lab_apply" {
  name        = local.apply_role_name
  description = "aws-identity-access apply role; assumable only by the lab environment subject (T15 #10 d6)."
  assume_role_policy = templatefile(
    "${path.module}/policies/trust-github-environment.json.tpl",
    {
      oidc_provider_arn = data.aws_iam_openid_connect_provider.github.arn
      environment       = "lab"
    }
  )
  tags = local.tags

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_iam_role_policy" "lab_apply_access" {
  name   = "access-model"
  role   = aws_iam_role.lab_apply.id
  policy = templatefile("${path.module}/policies/apply-role.json.tpl", local.policy_inputs)
}

resource "aws_iam_role_policy" "lab_apply_denies" {
  name   = "explicit-denies"
  role   = aws_iam_role.lab_apply.id
  policy = templatefile("${path.module}/policies/explicit-denies.json.tpl", local.policy_inputs)
}
