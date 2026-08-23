---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 9
title: "T07 — Standing administrator access (three separated decisions)"
url: https://github.com/a24577t/aws-identity-access/issues/9
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-23
sources:
  narrowing_comment: https://github.com/a24577t/aws-identity-access/issues/9#issuecomment-5382170270
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
---

# T07 — Standing administrator access (three separated decisions)

> Proposed discovery record — the complete durable result of T07 #9. Decisions approved by Eric
> as the human project owner and decision authority; the session was executed by Claude in the
> repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`. **Nothing here is
> accepted architecture: every decision is a proposal until ⟦G-Verdict⟧ and ⟦G-Accept⟧.** GitHub
> issue #9 is the workflow/index surface and links to this record.

Governing documents cited at the `aws_ami` revision pinned by `T01` (#2): `11-decision-register.md`
(no entry decides the question; `OD-05` open), root `CONTEXT.md` (Durable access, Elevation,
Break-glass), `01-repository-boundaries.md`, `05-runtime-mutation-contracts.md`, `RD-05`. Evidence
(not authority): T18 inventory `docs/research/brownfield-inventory.md` (X27, X31, X36, X39; REVIEW Q14).

## Decision 1 — Durable-access prohibition

Approved: option A. A standing account assignment granting `AdministratorAccess`-equivalent
authority to a workforce principal is prohibited in durable access. T07 selects that the rule be
carried into the proposed domain-decision register using the `T08` form and into the proposed
upstream refinement to documents `01`/`11`; neither is accepted yet.

Clarifications recorded as part of the decision:
- The prohibition applies to all environments, including the lab. There is no Free Tier, POC,
  single-collaborator, or other lab exception permitting a standing `AdministratorAccess`-equivalent
  workforce assignment.
- The prohibited object is a standing account assignment granting `AdministratorAccess`-equivalent
  authority to a workforce principal.
- An admin-capable permission-set definition may exist only as a durable construct supporting the
  future governed elevation service. Its existence does not authorize either a standing or manually
  maintained assignment.
- Any future use must follow the governed request → grant → expire lifecycle, with automatic expiry
  and reconciliation defined by the elevation work.
- T07 decision 1 proposes the durable prohibition; `T21` and `T14` will define the exact
  equivalence-detection and validation rules if the proposal passes ⟦G-Verdict⟧ and ⟦G-Accept⟧.
  Equivalence includes at minimum the AWS-managed `AdministratorAccess` policy, an unrestricted
  `Allow */*` without a boundary, and unbounded identity-mutation authority.
- The proposed one-sentence refinement to upstream documents `01`/`11` is prepared for Eric to
  carry through the governing acceptance process; `aws_ami` is not modified; the refinement is
  proposed, not accepted.
- `T03`'s exclusion of an administrator permission set from slice A is preserved.

Classification (proposed): prohibition **absent** upstream; **compatible** with `CONTEXT.md`
(durable access vs elevation), `01`, and `05` (durable constructs vs individual use); a prohibition
on the admin-capable *definition* would conflict with `05` and is not selected.

## Decision 2 — POC demonstration

Approved: option A. Slice A demonstrates no valid administrator path. The demonstration is negative
proof only: an intentionally invalid permission-set and standing GROUP-assignment specimen pair
under the `T14`-selected test-fixture path.

Clarifications recorded as part of the decision:
- The specimens exist only under the `T14`-selected test-fixture path, never under `access/`.
- They contain no real AWS account IDs, GroupIds, ARNs, credentials, or other runtime identifiers.
- They are never included in a Terraform plan, uploaded as an artifact for deployment, or applied.
- The validator must deterministically reject the pair with a stable `T14` error code identifying
  the standing `AdministratorAccess`-equivalent assignment.
- `T21` owns the complete equivalence-detection rule. The initial counterexample may exercise
  managed `AdministratorAccess`, but it must not narrow the proposed prohibition to that one policy
  form.
- The test must demonstrate the cross-file condition: an admin-capable permission-set definition
  combined with a standing workforce GROUP assignment.
- This does not change `T03`'s exactly-two-permission-set slice or introduce an administrator
  permission set into requester configuration.
- Option C (a valid bounded production-operator set in the slice) remains conflicting with `T03`
  and is not selected.

Classification (proposed): invalid specimen outside `access/` **compatible** with `02`, `T04`
decision 1, and decision 1; a valid admin-capable set in the slice **conflicting** with `T03` #4
decision 4.

## Decision 3 — Elevation dependency and the interim administrative path

Approved: **no interim administrator assignment exists in slice A.** Conclusions recorded exactly:
- Slice A and the POC contain no valid administrator assignment or administrator-access
  demonstration beyond the approved negative validator proof.
- The POC does not depend on implementing the future elevation service and may complete without
  exercising administrator elevation.
- Any future workforce assignment of `AdministratorAccess`-equivalent authority is blocked until a
  governed elevation service has been accepted and implemented with request → grant → automatic
  expiry → reconciliation.
- Existing AWS Organizations management-account, root-user, account-recovery, or lab-operator
  access is an external operational prerequisite. It is not represented under `access/`, not
  reconciled by this repository, not part of the POC demonstration, and not evidence that standing
  administrator access is permitted.
- Break-glass/account-recovery access is an emergency operational path, not a routine
  governed-access or change path. T07 does not design or implement it.
- No manual, temporary, lab-only, or single-collaborator exception may create a standing
  `AdministratorAccess`-equivalent workforce assignment.
- T07 does not create an elevation-service implementation ticket unless one already exists in the
  approved Wayfinder map. It records the future dependency and lets map closure/S5 disposition it.

Classification (proposed): **compatible** with the durable-access/elevation separation in
`CONTEXT.md`, documents `01` and `05`, and T07 decisions 1–2; exact future elevation behavior
remains deferred (`OD-05` open upstream).

## Proposed handoffs (proposals; nothing accepted)

- **`T08` form (domain decision register):** carry decision 1 as a domain decision — "No standing
  account assignment grants `AdministratorAccess`-equivalent authority to a workforce principal in
  durable access; administrative authority is obtained only through the governed elevation
  lifecycle (request → grant → automatic expiry → reconciliation)."
- **Upstream refinement to documents `01`/`11` (one sentence, carried by Eric; `aws_ami` not
  edited):** proposed wording — "Standing account assignments granting AdministratorAccess-equivalent
  authority to workforce principals are prohibited in durable access; such authority is obtained only
  through the governed elevation lifecycle owned by `aws-privileged-access`." Proposed as a new
  resolved register entry in `11` referenced from the `aws-identity-access` section of `01`.

## Downstream constraints (inherited by existing tickets)

- **`T14` #19:** the negative specimen pair under the test-fixture path; a stable error code that
  deterministically rejects the standing `AdministratorAccess`-equivalent assignment; the cross-file
  check (admin-capable definition + standing workforce GROUP assignment); no specimen under
  `access/`; no runtime identifiers in specimens; specimens never planned or applied.
- **`T21` #20:** owns the complete equivalence-detection rule (at minimum managed
  `AdministratorAccess`, unrestricted `Allow */*` without a boundary, unbounded identity-mutation
  authority); the counterexample may exercise managed `AdministratorAccess` but must not narrow the
  proposed prohibition; the slice's two permission sets remain read-only and narrowly scoped.
- **Existing elevation work (platform; `OD-05`):** the future dependency is recorded here for map
  closure/S5 disposition; no elevation-service ticket is created by T07.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is accepted
until ⟦G-Verdict⟧ and ⟦G-Accept⟧.
