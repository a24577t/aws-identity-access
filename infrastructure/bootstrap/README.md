# infrastructure/bootstrap

The one-time AWS-side bootstrap root (T15 #10 d15): the two
repository-specific pipeline IAM roles of the T15 #10 d6 access model —
the read-only **plan role** (assumed by the `lab-plan` environment
subject) and the mutation-capable **apply role** (assumed by the `lab`
environment subject) — with their trust policies, access-model policies,
and shared explicit denies. Applied **locally by the owner under the
separately authorized R7 #32 bootstrap only**; its sensitive outputs
(the role ARNs) are carried into the GitHub deployment variables by the
R6 #31 / R7 #32 activation acts and appear nowhere in committed content.

**Authored, never executed here.** R5 #30 authors this source with zero
Terraform execution; no `init`, `plan`, or `apply` has run against it,
and provider execution remains unverified until the designated lab-CI
boundary (spec 8.3 — the open provider-execution condition). No apply of
any root may occur before the R6/14a control set is active (T15 d15).

## Access model (T15 #10 d6/d7; ADR-0009)

Policy documents live as reviewable templates under
[`policies/`](policies/):

- [`trust-github-environment.json.tpl`](policies/trust-github-environment.json.tpl)
  — one trust form, bound to the exact audience `sts.amazonaws.com`, the
  exact repository, and the exact environment subject; the existing
  GitHub OIDC provider is referenced by data source, never managed.
- [`plan-role.json.tpl`](policies/plan-role.json.tpl) — read-only
  Organizations / Identity Center / Identity Store discovery; state
  object read-only; native lockfile Get/Put/Delete only; encrypted
  plan/evidence objects Get/Put under the evidence prefix; KMS
  data-plane on exactly the state key via S3.
- [`apply-role.json.tpl`](policies/apply-role.json.tpl) — the slice-A
  `sso` write actions only, guarded so creates require and mutations
  match the `managed-by` coexistence tag (pre-existing, untagged
  resources stay outside every allow — ADR-0009); state and lockfile
  objects only under the identity-center state prefix; encrypted
  evidence Get/Put; the same scoped KMS data-plane.
- [`explicit-denies.json.tpl`](policies/explicit-denies.json.tpl) —
  attached to **both** roles: all of IAM (covering role, trust-policy,
  and OIDC-provider mutation), Organizations mutation, S3 control plane
  plus an `s3:*` deny outside the authorized prefixes, KMS control
  plane, and Identity Center instance / identity-source / application /
  user / group mutation (`sso-directory` in full).

The plan gate remains the primary protected-resource control; these
role policies are defense-in-depth (T15 #10 d7). The templates are
rendered deterministically by `tests/test_infrastructure_roots.py` with
synthetic inputs, so the model is reviewable and testable without any
provider execution (spec 5).

## State (T15 #10 d16)

State object `aws-identity-access/lab/bootstrap/terraform.tfstate` with
its native lockfile (`use_lockfile=true`) in the existing CMK-encrypted
state bucket, `us-east-1`. The backend block is partial because the
bucket name is a live lab identifier (T15 #10 d12); the one-time,
separately authorized local init supplies it:

```
terraform init \
  -backend-config="bucket=<state-bucket>" \
  -backend-config="key=aws-identity-access/lab/bootstrap/terraform.tfstate" \
  -backend-config="region=us-east-1" \
  -backend-config="use_lockfile=true"
```

Credentials for that one-time apply come from the owner's named AWS CLI
profile (T15 #10 d9 — the profile name only; nothing is recorded here).
The two sensitive inputs (`state_bucket`, `state_kms_key_arn`) are
supplied at that apply and never committed; `.gitignore` excludes
`*.tfvars` and every Terraform working artifact.
