# aws-identity-access

<!-- STUB — T04 layout prototype (throwaway). Shows the two README sections decisions T04-d2 and T04-d6 require; final wording lands with the accepted architecture (S5+). -->

## Repository shape

`access/` contains governed desired access. Routine access-request pull requests modify this
directory. It contains no implementation code, credentials, generated AWS identifiers, or
runtime requests, grants, and sessions.

| Root | Holds | Ordinary requester edits? |
|---|---|---|
| `access/` | governed desired access (slice A: `identity-center/`) | **yes — only here** |
| `governance/` | declarations that are not routine access grants | no |
| `docs/` | `architecture/` (authoritative) · `guides/` (informative) · `generated/` (non-authoritative, generated) · `agents/` · `research/` — not of equal authority | no |
| `schemas/` | RD-04 schemas validating every governed file | no |
| `infrastructure/` | Terraform and deployment mechanics | no |
| `src/` · `tests/` | validation / effective-plan code and executable tests (T14) | no |
| `.github/` | CI, CODEOWNERS, repository automation — strictest owner set | no |

## Absent for slice A

The first POC slice (T03 #4) deliberately contains none of the following surfaces. Each is
owned by this repository under aws_ami document 01 and may be introduced by a later slice
through a governed decision; their absence is a scope boundary, not a domain prohibition. The
selected-slice validation profile rejects files under these paths with a stable out-of-slice
code (T14).

| Absent surface | Scoped out by |
|---|---|
| `access/iam/` (roles, customer-managed policies, permission boundaries, users, groups) | T03 #4 decision 1; T11 #16, T12 #17 closed Out of scope |
| `access/deployments/fleet-roles/` | T03 #4 decision 1; T13 #18 closed Out of scope |
| `access/identity-center/identity-source/` (desired configuration) | T03 #4 decision 2 — the identity source is an evidenced prerequisite (T22) |
| `access/identity-center/bootstrap/` | T03 #4 decision 2 — procedures are not in the slice; prerequisite evidence is T22's |
| `governance/exceptions/` | T03 #4 decision 5 — no USER-principal or IAM exceptions in the slice |
| `governance/runtime-mutations/` | convention inherited (OD-16); no runtime-mutation contract in slice A (T04 #6 decision 6) |
