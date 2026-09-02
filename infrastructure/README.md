# infrastructure/

Terraform and deployment mechanics; derives deployed permission-set names
`ialab-<key>` (ADR-0003; T04 #6 decision 5; T15 #10 decision 8). The R5 #30
surfaces, authored with zero Terraform execution (no `terraform init`, `plan`,
or `apply` has ever run against them; the provider-execution condition of
specification §8.3 stays open):

- [`bootstrap/`](bootstrap/README.md) — the one-time AWS-side bootstrap root:
  the T15 #10 d6/d7 plan/apply pipeline roles, exact environment-bound OIDC
  trust, access-model policies, and explicit denies; applied only under the
  separately authorized R7 #32 owner-executed bootstrap.
- [`identity-center/`](identity-center/README.md) — the slice-A Identity
  Center resource model derived from the governed `access/` surface; planned
  post-merge by the merged `lab-plan` workflow and applied only as the one
  approved saved plan by the `lab` environment.
- [`keys/`](keys/README.md) — the plan-encryption public-key seam (T15 #10
  d9); the key material itself lands only with the separately authorized
  R6 #31 activation.

State keys `aws-identity-access/lab/<root>/terraform.tfstate` with native
lockfiles and the evidence prefix `aws-identity-access/evidence/` in the
existing state bucket (T15 #10 d16). No Terraform execution occurs before the
R6/14a control set is active (T15 d15). Static verification lives in
`tests/test_infrastructure_roots.py`.
