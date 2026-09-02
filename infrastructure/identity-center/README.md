# infrastructure/identity-center

The slice-A Identity Center root (spec 3 W8; spec 10 row 13): the
permission-set, AWS-managed-policy-attachment, inline-policy, and GROUP
account-assignment resource model, derived entirely from the governed
requester surface — planned post-merge by the merged `lab-plan` workflow
from the exact `main` commit and applied only as the one approved,
encrypted saved plan by the `lab` environment (T15 #10 d15; T20 #22 d4).

**Authored, never executed here.** R5 #30 authors this source with zero
Terraform execution; no `init`, `plan`, or `apply` has run against it,
and provider execution remains unverified until the designated lab-CI
boundary (spec 8.3 — the open provider-execution condition). No apply
may occur before the R6/14a control set is active (T15 d15).

## Derivation (governed sources only)

- **Permission sets** from `access/identity-center/permission-sets/*.yml`
  — deployed Name `ialab-<key>` through the single
  `resource_name_prefix` local (T15 #10 d8), explicit
  `session_duration`, and the four coexistence tags; exactly one of the
  two policy forms becomes an `aws_ssoadmin_managed_policy_attachment`
  or an embedded `aws_ssoadmin_permission_set_inline_policy`
  (`jsonencode` at plan time — T21 #20 d5/F6).
- **Groups** from `access/identity-center/groups/*.yml` — references
  only (ADR-0007): resolved by exact Identity Store DisplayName through
  the `aws_identitystore_group` data source; a missing or ambiguous name
  fails the plan (PRQ-GROUP semantics — never creation, never deferral);
  no GroupId is ever committed.
- **Assignments** from
  `access/identity-center/account-assignments/<account>/*.yml` — GROUP
  form only, to `lab-workload` accounts only (T15 #10 d7; ADR-0009),
  asserted by fail-closed preconditions. An account whose fixture entry
  is `status: requested` defers: it is omitted from the applicable saved
  plan and reported as deferred by the effective-access summary
  (T16 #11 d8; RD-08).
- **Instance** — resolved at plan time by `aws_ssoadmin_instances`
  (exactly one organization instance, `us-east-1`); its identifiers
  appear only in non-public evidence (T15 #10 d4/d12).
- **Alias-to-account binding** — the `plan_context_file` variable names
  the retrieved T09 #12 plan-context evidence (the snapshot envelope);
  it is the sole binding source (T15 #10 d5), decoded under
  `sensitive()` (T20 #22 d7). The `lab-plan` workflow hands the path to
  `terraform plan`; the saved plan carries every resolved value, so
  apply never re-reads it (one plan, one attempt — T20 #22 d4).

## Guard rails

The plan gate (the validator's plan-stage battery over the saved plan)
remains the primary protected-resource control (T15 #10 d7; ADR-0009).
In-root defense-in-depth: `prevent_destroy` on every permission set (a
replace or delete never rides an ordinary plan — T20 #22 d5), the
assignment preconditions above, and `depends_on` serialization of
assignments behind both policy children (T21 #20 F5).

## State (T15 #10 d16)

State object `aws-identity-access/lab/identity-center/terraform.tfstate`
with its native lockfile (`use_lockfile=true`) in the existing
CMK-encrypted state bucket, `us-east-1`. The backend block is partial by
design: the merged workflows supply every value at `init` (the bucket
name is a live lab identifier and never enters committed content —
T15 #10 d12).
