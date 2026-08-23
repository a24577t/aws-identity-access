---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 10
title: "T15 — Lab-environment test and deployment contract"
url: https://github.com/a24577t/aws-identity-access/issues/10
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-23
sources:
  inherited_inputs:
    - https://github.com/a24577t/aws-identity-access/issues/10#issuecomment-5382170417
    - https://github.com/a24577t/aws-identity-access/issues/10#issuecomment-5382919382
    - https://github.com/a24577t/aws-identity-access/issues/10#issuecomment-5383471026
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  lab_evidence: mcp_gateway01 (read-only; ADR-0001, 0003, 0007, 0008; live roots' lock files)
---

# T15 — Lab-environment test and deployment contract

> Proposed discovery record — the complete durable result of T15 #10. Decisions approved by Eric
> as the human project owner and decision authority after collaborator review; executed by Claude
> in the repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`, using the
> batch-question interaction rule recorded in
> [`.ai/repository-owner/operating-guide.md`](../../../.ai/repository-owner/operating-guide.md).
> **Nothing here is accepted architecture: every decision is a proposal until ⟦G-Verdict⟧ and
> ⟦G-Accept⟧.** GitHub issue #10 is the workflow/index surface and links to this record.

## Authorization scope of this record

Accepting T15 authorizes the **architecture contract only**. It does **not** authorize AWS
account creation or invitation, any AWS Organizations change, IAM Identity Center enablement or
identity-source change, delegated-administrator registration, IAM role / trust-policy / GitHub
OIDC bootstrap, GitHub rulesets, environments, secrets, variables, or workflows, Terraform plan,
apply, cleanup, or any other infrastructure mutation. Each remains separately authorized
implementation work (S6 tickets or later) requiring explicit Eric authorization.

## Governing documents and evidence

Cited at the `aws_ami` revision pinned by T01 (#2): `01-repository-boundaries.md`,
`03-region-model.md`, `05-runtime-mutation-contracts.md`, `06-account-lifecycle.md`,
`07-identity-center-platform.md`, `08-management-account.md`, `09-tier0-execution.md`,
`12-capability-validation.md` (CV-07), `11-decision-register.md` (RD-03, RD-06, RD-08; OD-03,
OD-04, OD-08, OD-09, OD-21 open), I-4, root `CONTEXT.md`. Inherited map decisions: T02 #3, T03
#4, T04 #6, T05 #7, T06 #8, T07 #9. Evidence (not authority): the `mcp_gateway01` lab
substrate, read-only; the GitHub repository state observed 2026-08-23 (public; owner type User;
one collaborator `a24577t`, admin; no rulesets, branch protection, environments, secrets,
variables, workflows, or CODEOWNERS). No AWS call was made.

## Claim-resolution record (grill-with-docs)

| # | Claim | Authority | Result | Upstream amendment / refinement |
|---|---|---|---|---|
| 1 | A lab deployment role / pipeline principal stands in for the Tier-0 principal without contradicting 09 | `09` (pipeline principals are Tier-0, provisioned/guarded by `aws-organization-governance`; apply from reviewed artifact); OD-03/OD-04 open | **compatible under a lab-only exception**: org-governance provisioning/guarding is absent in the lab; compatibility preserved by the no-self-escalation rule (decisions 6, 7, 15 — pipeline roles cannot modify any role, trust policy, or OIDC provider) | none new; T02's proposed document-09 refinement (controlled non-production POC exception) reaffirmed, carried by Eric |
| 2 | The lab inventory source satisfies I-4 / RD-06 for this consumer, or is a labeled fixture per T09 | I-4; RD-06 (names only; binding in exactly one place; IDs resolved at execution time); RD-08; `06`; the brief's "local inventory only as an explicitly labeled test fixture" | **compatible**: decision 5 — labeled alias fixture plus exactly one non-public binding record; identifiers resolved at execution time, never committed | none; T09 fixes the snapshot/transport form inside decision 5 |
| 3 | The lab Identity Center instance and Regions are consumed as instance properties | RD-03; `07`; `03` | **inherited**: decisions 3–4 | none |
| 4 | The permitted-mutation and protected-resource rules are consistent with 05's drift policy | `05` (detect → alert → preserve evidence → governed reconciliation; never auto-overwrite); I-6 | **compatible**: decision 7 — the POC never initiates divergence; divergence detected in POC-managed resources is alerted, evidenced, and reconciled only through a governed PR; pre-existing resources are never reconciled | none; "POC-managed resource set" recorded as a lab/POC domain refinement (T08 form) |

## Decisions (approved option A, with collaborator corrections integrated)

### Decision 1 — Authorized account classes and the naming rule
Four account classes, recorded as an inventory `class` field and never encoded in a name:
`management` (hosts the Identity Center organization instance; never a slice-A assignment
target); `lab-workload` (assignment targets; exactly the explicitly aliased active accounts);
`role-host` (hosts this repository's OIDC roles and its isolated state/evidence prefixes — the
T02 lab exception; may coincide with a `lab-workload` account); `requested-fixture`
(`status: requested`; never created). Logical aliases follow the T05 grammar
`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`, are immutable once bound, and carry no live identifier.
Classification: absent upstream; compatible with `01`, `06`/RD-08, T03 d5, T05. Rejected: three
classes (Tier-0 roles in the management account conflict with `08`); OU-derived classes
(conflict with T03/T04).

### Decision 2 — Target contract topology (not an assertion about current AWS state)
The contract **targets**: an AWS Organization whose management account is distinct from the
`role-host` account; `role-host` is a member account; an Identity Center organization instance
in the primary Region (decision 3) with the Identity Center default identity store as the lab
identity source; at least two usable active `lab-workload` member accounts; one
`requested-fixture` alias never created; the delegated-administrator prerequisite of decision 4.
**T16 performs read-only discovery before implementation** and records which elements are
present. If the distinct management account, `role-host`, two usable workload accounts, the
organization instance, the default identity store, or the delegated-administrator prerequisite
is absent, **T16 stops and produces remediation**. Account creation or invitation, Identity
Center enablement, delegation registration, and any other AWS mutation require **separate Eric
authorization**. Options B (`role-host` is the management account) and C (no Organization;
plan-only per T02) are **never selected by inference** — only by Eric's explicit decision.
Classification: absent upstream; compatible with `01`, `07`, `08`, T02, T03.

### Decision 3 — Regions
Single Region `us-east-1` (the substrate's Region). `instance.yml` declares
`primary_region: us-east-1` and `additional_regions: []`. All regional IAM Identity Center and
Identity Store operations use us-east-1. AWS Organizations is a global service; its inventory is
not represented as Region-owned. Classification: inherited (RD-03, `03`, `07`; T02 minimum
Region scope).

### Decision 4 — Identity Center instance consumption and deployment-role residency
**Conditional on T16 verifying decision 2A.** The instance ARN and identity-store ID are
resolved at plan time by data source and appear only in non-public evidence; `instance.yml`
holds Region, identity-source type, owner, and verification fields (T22 fixes the set). The
`role-host` account is registered as Identity Center **delegated administrator** through the
lab's organization mechanism as an **evidenced prerequisite** (T22 form) under its own separate
Eric authorization; deployment roles never reside in the management account. Recorded
limitation: **the delegated administrator must not manage permission sets provisioned in the
management account or assignments targeting the management account** — consistent with
decision 1 (the management account is never a slice-A target). If T16 does not verify 2A, this
decision stops for remediation; there is no silent fallback. Classification: inherited for the
instance as a manual prerequisite (`07`, T03 d2); delegated-administrator placement absent
upstream, compatible with `01` (designation is organization authority) and `08`.

### Decision 5 — Inventory source for this consumer
A **committed, explicitly labeled lab inventory fixture** contains only stable **logical account
aliases**, `class`, `status`, and intended classification. It contains **no actual AWS account
names, account IDs, root e-mails, ARNs, or live OU paths**. **Exactly one non-public evidence
record** holds the alias-to-account binding (live name, ID, OU placement) and the digest of the
fixture it binds. At execution time the pipeline verifies the exact live name/ID/OU binding,
uniqueness of each resolved account, `ACTIVE` state, and the fixture digest; `requested` aliases
resolve to deferred (RD-08), never invalid. **Public summaries use aliases only.** T09 owns the
snapshot and transport form within this rule. Classification: compatible with I-4, RD-06, RD-08,
the brief's labeled-fixture rule, and the owner sensitive-values constraint. Rejected: live
identifiers as GitHub environment variables (second binding location); live identifiers in the
fixture (violates the owner constraint).

### Decision 6 — Authentication, deployment roles, and the access model
Two **distinct** repository-specific IAM roles in `role-host` — a **plan role** and an **apply
role** — with validation running under no AWS identity. Each trust policy binds to the **exact
audience `sts.amazonaws.com`, the exact repository, and the exact environment subject**: plan
role ← `repo:a24577t/aws-identity-access:environment:lab-plan`; apply role ←
`repo:a24577t/aws-identity-access:environment:lab`. **Workflow definitions are protected
through governed workflow files, strict ownership routing (T06 strictest set on `.github/**`),
and the `main` ruleset**; the contract does **not** claim that AWS enforces workflow identity
through `job_workflow_ref` unless the implemented trust policy actually adds that condition, in
which case the implementation records it. The existing GitHub OIDC provider in `role-host` is
**referenced, never managed** (one per account; owned by `mcp_gateway01`). Roles are created by
the one-time bootstrap (decision 15) under separate authorization; pipeline roles cannot modify
any role, trust policy, or OIDC provider.

**Access model (authoritative for decisions 6, 7, and 16):**

Validation:
- No AWS identity.

Plan role:
- Read-only Organizations, IAM Identity Center, and Identity Store discovery.
- Read the Terraform state object.
- Get/Put/Delete only the native lockfile associated with that state.
- Get/Put only encrypted saved-plan and plan-evidence objects inside a run-scoped path under
  `aws-identity-access/evidence/`.
- No Terraform state-object Put/Delete.
- No IAM, OIDC-provider, Organizations, Identity Center, S3 control-plane, or KMS control-plane
  mutation.

Apply role:
- Only the slice-A IAM Identity Center mutations permitted by Decision 7.
- State-object and native-lockfile Get/Put/Delete only under `aws-identity-access/lab/<root>/`.
- Encrypted evidence Get/Put only under `aws-identity-access/evidence/`.
- No IAM-role/trust, OIDC-provider, Organizations, S3 bucket/configuration/policy, or KMS
  key/policy mutation.

KMS:
- Any required KMS data-plane use is restricted to encryption/decryption for objects in the
  authorized prefixes.
- KMS key and key-policy administration is prohibited.

The plan gate remains the primary protected-resource control.

Classification: compatible with `09` under the lab exception; inherited from T02 and T06 d4.
Rejected: a deploy → execution role chain (no added assurance); a single role (conflicts with
T06 d4).

### Decision 7 — Permitted mutations and protected resources
*Permitted Identity Center mutations (apply role):* create/update/delete of **POC-managed**
resources only — permission sets whose deployed Name carries the decision-8 prefix and tags,
their AWS-managed-policy attachment or embedded inline policy, and GROUP account assignments of
those sets to `lab-workload` accounts. Every S3, lockfile, evidence, and KMS data-plane operation
of either role is governed by the decision-6 access model; nothing beyond it is permitted.
*Explicitly denied* for both pipeline roles: IAM role and trust-policy mutation, GitHub OIDC
provider mutation, S3 bucket creation/configuration/policy mutation, KMS key and key-policy
administration, any AWS Organizations mutation, and Identity Center instance, identity-source,
application, user, and group mutation. *Protected resources:* every pre-existing Identity Center
object (instance, identity source, users, groups, non-prefixed permission sets and their
assignments, applications), the OIDC provider, `mcp_gateway01` roles and state keys, the
Organizations structure, and the state bucket and its CMK configuration. *Enforcement:* the
**plan gate remains the primary protected-resource control** — any create, import, update, or
delete outside the derived POC-managed set rejects the plan; the role policies are
defense-in-depth (allow only the slice-A sso-admin write actions on the apply role; explicit
Deny on the classes above). The pre-existing bucket-wide state access of the `mcp_gateway01`
roles is recorded as a lab-exception finding, not remediated (remediation would modify
`mcp_gateway01` resources). *Drift:* divergence detected in POC-managed resources is alerted,
evidenced, and reconciled only through a governed PR; pre-existing resources are never
reconciled. Classification: compatible with `05`, I-6, T03 d6, T04 d5, T05, T06 d4/d5.

### Decision 8 — Naming prefix and tags
`resource_name_prefix = "ialab-"` (6 characters including the delimiter; composed deployed Name
≤ 30, within AWS's 32). Tags on POC-managed permission sets: `project=aws-identity-access`,
`environment=lab`, `managed-by=aws-identity-access-terraform`, `owner=identity-platform` (T06
principal key). T16 discovery verifies that no pre-existing permission set begins with `ialab-`;
a collision is a protected-resource plan error. Prefix and tags are coexistence markers, never
reconciliation-ownership authority. Classification: compatible with T05 d1, T04 d5; T21 verifies
tag support at the pin.

### Decision 9 — Credential handling
No long-lived AWS credentials anywhere; OIDC only. The plan-encryption public key is committed
under `infrastructure/`; the private key is held as the `lab` environment secret referenced by
name only (`LAB_PLAN_DECRYPTION_KEY`) — the name is registered here, the value appears nowhere.
Local bootstrap uses a named AWS CLI profile; only the profile name is recorded. Live
identifiers are sensitive and appear only in non-public evidence (decision 12). Classification:
compatible with the owner rule and T06 d4 transport. Rejected: SSM-held private key (requires
credentials before decryption/verification, inverting T06's order).

### Decision 10 — Cost-limit mechanism
In the payer account, one zero-spend AWS Budget (no budget actions; free) and Free Tier usage
alerts, established and evidenced before the first apply (their creation is a separately
authorized mutation). "Separately billed service" = any service line absent from the pre-POC
bill; any plan introducing one is rejected unless Eric separately approves it (T02). CloudTrail
evidence via the free 90-day event history; no new trail. Each apply's public summary lists the
services touched, using aliases only. Classification: inherited (T02 cost boundary);
implementation choice only.

### Decision 11 — Cleanup and rollback
Rollback and cleanup are **governed changes**: a revert/retire PR → a post-merge saved plan that
may destroy only POC-managed resources (explicit destroy acknowledgement; protected set
untouched) → `lab` approval → apply, each under separate authorization. Partial-mutation
recovery receives a recorded disposition and new authorization. After terminal cleanup,
verification compares live Identity Center against T16's discovery snapshot. **Retiring a state
prefix prevents further use (apply-role permission removed; prefix marked retired in evidence)
and follows an explicit retention/disposition decision by Eric; it never automatically deletes
Terraform state, lock history, authorization evidence, or verification evidence.**
Classification: compatible with T02 step 6, T06 d4, `09`, T05 retire semantics. Rejected: local
`terraform destroy` (breaks apply-from-reviewed-artifact; recordable only as a documented
emergency path if Eric so decides).

### Decision 12 — Retained evidence and the architecture-evidence / lab-result boundary
Three tiers. **(1) Architecture evidence — committed, public:** result records, validation
specimens, CV-07 records, tool/provider pins, digests, and sanitized summaries referencing
**logical aliases only** — public artifacts contain only aliases, sanitized summaries, pins, and
digests, and **no live lab-specific identifiers**. **(2) Lab run evidence — encrypted and
non-public:** Terraform state and native lockfiles reside only under
`aws-identity-access/lab/<root>/`; encrypted saved plans, authorization records, enforcement
records, verification results, and other non-public run evidence (full alias bindings, actual
account IDs and names, role ARNs, OIDC details, CloudTrail references) reside under
`aws-identity-access/evidence/`; **Terraform state is never copied into the evidence prefix**;
both prefixes are in the existing CMK-encrypted state bucket (zero new recurring spend); public
workflow artifacts carry digests only. **(3) Prerequisite evidence (T22)** — committed in alias
form; any live identifier is redacted to the non-public tier. Boundary rule: everything under
`docs/` must be reproducible without the lab; a live lab identifier anywhere public is a
validation error (T14 code). Classification: absent upstream; compatible with T06 d3/d4, `07`,
T02 backend reuse. Rejected: a separate private repository for tier 2 (identifiers enter git
history).

### Decision 13 — Exact Terraform and AWS-provider pins (added duty from T03 revalidation)
Terraform `1.15.7` exact; `hashicorp/aws` `= 6.53.0` with the dependency lock file committed.
Selection basis: both already exercised in the lab's live roots and installed locally; current
provider major; `use_lockfile` requires ≥ 1.11. Upgrade rule: any pin change is a
platform-change PR (strictest review set), requires CV-07 re-verification by T21 and a new saved
plan; never auto-bumped. OD-09 remains open platform-wide. Classification: compatible with T02
and `09`. Rejected: newest-available (unproven in the lab); `5.100.0` (previous major).

### Decision 14 — S5 requirement wording (fixed)
"The S5 brownfield implementation plan must include: (1) a staged lab rollout (bootstrap →
validation → post-merge saved plan → approval → apply → verification → cleanup), each stage
under its own separate authorization, targeting aliased lab accounts only; (2) verification
criteria per stage; (3) a rollback procedure executed as a governed change; (4) an explicit
boundary between architecture evidence and lab-specific results, with live lab identifiers
confined to encrypted non-public evidence; (5) brownfield discovery, import/reconciliation
sequencing, destroy blocking, and migration planning per document 09."

### Decision 15 — Lab-only review exception, planning lifecycle, and the minimum bootstrap control set
*Basis (observed 2026-08-23):* public repository; owner type User; one collaborator
(`a24577t`, admin); no rulesets; `main` unprotected; no environments, secrets, variables,
workflows, or CODEOWNERS. *Exception record (T06 d3 content):* repository
`a24577t/aws-identity-access`, branch `main`, lab deployment scope = decisions 1–2 aliases,
visibility public / plan free, reviewer topology single collaborator; each unavailable or
unenforced control enumerated separately with server-enforced vs procedural/detective
distinguished; no control claimed enforced without live evidence; PR/merge records and
validation evidence required procedurally where server enforcement is unavailable; code-owner
review requested but not independently enforceable; identity-platform, security, and
architecture classes recorded as technically unenforced and never as independently satisfied
while one physical identity reviews; target/production use prohibited; never satisfies a
target-state assurance claim; never authorizes an apply. *Expiry:* the earliest of the POC phase
gate (⟦G-Phase⟧) or any change of visibility, plan, collaborator topology, branch rules, or
deployment scope (re-evaluation mandatory; private visibility removes free environment
protection and triggers it).

*Planning lifecycle and minimum server-enforced set (configured at S6 bootstrap under separate
authorization before any apply):*
- The `main` ruleset requires pull requests, blocks direct push, force-push, and deletion, has an
  empty bypass list, and requires the status checks `validate` and `plan-preview`.
- `plan-preview` runs for the reviewed pull request, is sanitized and non-authoritative, and is
  never eligible for apply.
- After merge, a `lab-plan` environment job runs from the exact `main` source commit, requires
  `a24577t` environment approval, and produces the encrypted applicable saved plan and its
  digest.
- The `lab` environment requires `a24577t` approval and may consume only that exact saved plan,
  source commit, inventory snapshot, and digest.
- Any source, input, pin, inventory, enforcement-evidence, or plan change invalidates the
  authorization and requires a new saved plan.
- Both environments disallow protection-rule bypass; `lab-plan` is restricted to the `main`
  workflow path and `lab` to `main` only; deployment concurrency remains one.
- Self-review prevention remains disabled and is recorded as reduced lab assurance; it is
  enabled as soon as an independent reviewer exists.

*AWS-side bootstrap:* a one-time `infrastructure/bootstrap/lab` root applied locally by Eric
under separate authorization, its outputs imported and evidenced (document 09's
documented-bootstrap rule); pipeline roles cannot alter it. Classification: absent upstream;
compatible with T06 d3/d4/(5) and `09`. Rejected: date-bound expiry; reusing the
`mcp_gateway01` bootstrap role (conflicts with T02).

### Decision 16 — State-key and evidence-prefix convention
State keys `aws-identity-access/lab/<root>/terraform.tfstate` (roots `bootstrap`,
`identity-center`) with their native lockfiles, and the evidence prefix
`aws-identity-access/evidence/` with run-scoped paths beneath it, in the existing state bucket;
`use_lockfile = true`. Object access per prefix is exactly the decision-6 access model: the
plan role reads state, manages only the lockfile, and writes encrypted plan/evidence objects in
its run-scoped evidence path; the apply role manages state and lockfile objects under
`aws-identity-access/lab/<root>/` and encrypted evidence under `aws-identity-access/evidence/`;
Terraform state is never written under the evidence prefix. Classification: compatible with
T02 (isolated prefix). Rejected: adopting `mcp_gateway01`'s account-slug path convention.

## The lab contract (consolidated)

| Element (from #10) | Contract | Decision |
|---|---|---|
| Authorized account classes, naming rule | `management`, `lab-workload`, `role-host`, `requested-fixture`; aliases per T05 grammar; T16 instantiates | 1 |
| Organization | target topology; T16 read-only discovery; stop-with-remediation; no mutation without separate authorization; Organizations is global, not Region-owned | 2, 3 |
| Regions | `us-east-1` for all regional Identity Center / Identity Store operations; instance properties | 3 |
| IAM Identity Center instance | prerequisite, never created here; delegated administration in `role-host` (conditional on 2A); management-account sets/assignments out of reach | 4 |
| Inventory source | labeled alias fixture + one non-public binding record; execution-time verification; T09 form | 5 |
| Authentication / deployment roles | distinct plan and apply roles; exact audience/repository/environment subjects; OIDC provider referenced only; decision-6 access model | 6 |
| Permitted mutations / protected resources | POC-managed Identity Center set only; explicit denies; plan gate primary | 7 |
| Naming / tagging | `ialab-`; four tags; collision = plan error | 8 |
| Credential handling | OIDC only; one named environment secret; no live identifier in public content | 9 |
| Cost limits | T02 boundary; zero-spend budget + Free Tier alerts; no new trail | 10 |
| Cleanup / rollback | governed destroy-class changes via post-merge saved plans; retirement ≠ deletion | 11 |
| Retained evidence / boundary | state only under `lab/<root>/`; run evidence only under `evidence/`; aliases public, bindings non-public | 12 |
| Pins | Terraform 1.15.7; aws 6.53.0; upgrade rule | 13 |
| S5 requirement wording | fixed text | 14 |
| Review exception / planning lifecycle / bootstrap controls | `validate` + `plan-preview` checks; post-merge `lab-plan` saved plan bound to the exact `main` commit; `lab` consumes only that plan; both environments reviewer-gated, no bypass; self-review prevention disabled (recorded) | 15 |
| State / evidence prefixes | isolated keys; S3-native locking; access per decision 6 | 16 |

## Downstream handoffs (proposals; posted after publication)

- **T16 #11:** read-only discovery against decision 2A (distinct management account, `role-host`,
  two usable workload accounts, organization instance, default identity store,
  delegated-administrator prerequisite); alias fixture and the single non-public binding record
  (d5); `ialab-` collision check (d8); any missing prerequisite = stop with remediation; no
  creation/invitation/enablement/registration without separate Eric authorization.
- **T21 #20:** CV-07 verification at `hashicorp/aws = 6.53.0` / Terraform `1.15.7` (d13);
  tag-support verification for the d8 tags; a failed CV-07 blocks until the pin is revised or
  Eric approves a dated exception.
- **T22 #21:** `instance.yml` field set for d3/d4; delegated-administrator registration and
  identity-source evidence as prerequisites; committed evidence in alias form (d12 tier 3).
- **T20 #22:** plan-summary fields use aliases only (d12); the `plan-preview` PR check is
  sanitized and non-authoritative; the applicable saved plan is produced post-merge by the
  `lab-plan` job from the exact `main` commit and consumed only by `lab` (d15); environment
  names and OIDC subjects (d6); pins (d13); deferred target reported as "deferred".
- **T14 #19:** validation code for a live lab identifier in public content (d12 boundary rule);
  prefix/composed-name checks at `ialab-` (d8); fixture-schema checks for d5 (aliases, class,
  status, classification only).
- **T19 #14:** target-estate naming and import sequencing start from the d14 S5 wording.

## Interaction directive (durable)

The batch-question rule used for this ticket is recorded in
[`.ai/repository-owner/operating-guide.md`](../../../.ai/repository-owner/operating-guide.md)
under "Governing invariants": "For HITL decision work, present all currently knowable questions
as one numbered batch; use additional rounds only for materially dependent, contradictory, or
newly surfaced decisions."

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Verdict⟧ and ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub mutation.
