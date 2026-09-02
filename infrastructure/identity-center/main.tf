# The identity-center root (spec 3 W8; spec 10 row 13): the slice-A
# Identity Center resource model over the remediated T16 #11 topology,
# planned post-merge by the lab-plan workflow and applied only as the one
# approved saved plan (T20 #22 d4). The plan gate remains the primary
# protected-resource control (T15 #10 d7; ADR-0009); everything here is
# defense-in-depth behind it.

provider "aws" {
  region = "us-east-1" # T15 #10 d3 - the single lab Region
}

# T15 #10 d4: the Identity Center organization instance is resolved at
# plan time by data source; its identifiers appear only in non-public
# evidence. one() fails closed unless exactly one instance exists.
data "aws_ssoadmin_instances" "this" {}

locals {
  instance_arn      = one(data.aws_ssoadmin_instances.this.arns)
  identity_store_id = one(data.aws_ssoadmin_instances.this.identity_store_ids)
}

# ADR-0007: workforce groups are references. Resolution is by exact
# Identity Store DisplayName; a missing or ambiguous name fails the plan
# (PRQ-GROUP semantics) - this root never creates, renames, or adopts a
# group, and no GroupId is ever committed.
data "aws_identitystore_group" "this" {
  for_each          = local.groups
  identity_store_id = local.identity_store_id

  alternate_identifier {
    unique_attribute {
      attribute_path  = "DisplayName"
      attribute_value = each.value.identity_store_name
    }
  }
}

resource "aws_ssoadmin_permission_set" "this" {
  for_each = local.permission_sets

  instance_arn     = local.instance_arn
  name             = "${local.resource_name_prefix}${each.value.key}"
  description      = each.value.description
  session_duration = each.value.session_duration
  tags             = local.permission_set_tags

  lifecycle {
    # T20 #22 d5: access-definition changes never plan a replace or
    # delete outside the governed exceptional workflow; retirement
    # removes this block through that workflow first (T15 #10 d11).
    prevent_destroy = true
  }
}

resource "aws_ssoadmin_managed_policy_attachment" "this" {
  for_each = local.managed_policy_attachments

  instance_arn       = local.instance_arn
  permission_set_arn = aws_ssoadmin_permission_set.this[each.value.set].arn
  managed_policy_arn = each.value.policy_arn
}

resource "aws_ssoadmin_permission_set_inline_policy" "this" {
  for_each = local.inline_policies

  instance_arn       = local.instance_arn
  permission_set_arn = aws_ssoadmin_permission_set.this[each.key].arn
  inline_policy      = jsonencode(each.value.inline_policy)
}

# GROUP assignments of POC-managed permission sets to lab-workload
# accounts only (T15 #10 d7; ADR-0009). depends_on serializes assignment
# lifecycle against both policy children (T21 #20 F5 deletion ordering).
resource "aws_ssoadmin_account_assignment" "this" {
  for_each = local.active_assignments

  instance_arn       = local.instance_arn
  permission_set_arn = aws_ssoadmin_permission_set.this[each.value.permission_set].arn
  principal_type     = "GROUP"
  principal_id       = data.aws_identitystore_group.this[each.value.principal.group].group_id
  target_type        = "AWS_ACCOUNT"
  target_id          = local.account_bindings[each.value.account]

  depends_on = [
    aws_ssoadmin_managed_policy_attachment.this,
    aws_ssoadmin_permission_set_inline_policy.this,
  ]

  lifecycle {
    precondition {
      condition     = contains(keys(local.fixture_accounts), each.value.account)
      error_message = "fail closed: the assignment account is absent from the labeled lab inventory fixture (T15 #10 d5)."
    }
    precondition {
      condition     = try(local.fixture_accounts[each.value.account].class, "") == "lab-workload"
      error_message = "fail closed: assignments may target only lab-workload accounts (T15 #10 d7; ADR-0009)."
    }
    precondition {
      condition     = try(local.fixture_accounts[each.value.account].status, "") == "active"
      error_message = "fail closed: the assignment target is not an active fixture account (T15 #10 d5)."
    }
    precondition {
      condition     = try(each.value.principal.type, "") == "GROUP"
      error_message = "fail closed: only the two-segment GROUP assignment form is deployable in slice A (T10 #15)."
    }
  }
}
