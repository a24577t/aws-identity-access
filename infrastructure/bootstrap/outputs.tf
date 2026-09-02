# Role ARNs are live lab identifiers (T15 #10 d12): sensitive outputs,
# read only at the separately authorized bootstrap and carried into the
# GitHub deployment variables (LAB_PLAN_ROLE_ARN, LAB_APPLY_ROLE_ARN) by
# the R6 #31 / R7 #32 activation acts - never committed anywhere.

output "plan_role_arn" {
  description = "ARN of the read-only plan role the lab-plan environment assumes."
  value       = aws_iam_role.lab_plan.arn
  sensitive   = true
}

output "apply_role_arn" {
  description = "ARN of the apply role the lab environment assumes."
  value       = aws_iam_role.lab_apply.arn
  sensitive   = true
}
