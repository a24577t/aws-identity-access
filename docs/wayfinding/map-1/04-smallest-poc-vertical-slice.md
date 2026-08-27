---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 4
title: "T03 — Smallest POC vertical slice"
url: https://github.com/a24577t/aws-identity-access/issues/4
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-27
sources:
  backfill: "T08 #13 decision 13 result-record backfill, reconstructed 2026-08-27 from the ticket's complete comment history; traceability, not authority"
  resolution_comment: https://github.com/a24577t/aws-identity-access/issues/4#issuecomment-5382184394
  close_comment: https://github.com/a24577t/aws-identity-access/issues/4#issuecomment-5382187455
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  resolved: 2026-08-22
---

# T03 — Smallest POC vertical slice: slice A, Identity Center only

> **Backfilled discovery record** — produced 2026-08-27 under the separately authorized T08
> #13 decision-13 result-record backfill, reconstructing the complete durable result of
> T03 #4 from the ticket's comment history. Backfill preserves provenance and traceability
> only: it confers no new authority, changes no decision, and does not alter the approved S4
> Architecture Grill verdict. **Nothing here is accepted architecture: every decision is a
> proposal until ⟦G-Accept⟧.** GitHub issue #4 is the workflow/index surface and links to
> this record.

Grill completed and approved by Eric as the human project owner and decision authority,
2026-08-22, under `wayfinder-repo-owner` with `grill-with-docs` on the document-governed
claims; seven decisions taken one at a time. Governing documents cited at the aws_ami
revision pinned by T01 (#2). Nothing below accepted architecture or authorized an AWS
mutation. Candidates considered: (A) Identity Center only; (B) A + one exceptional IAM user;
(C) A + one enterprise IAM role with trust; (D) the brief's full example set.

## The slice (decisions 1–6)

1. **Candidate A — Identity Center only.** No IAM users, roles, trust policies, fleet roles,
   or StackSets in the first slice.
2. **Identity Center instance and identity source (07 boundary).** `instance.yml` is in the
   slice as governed *declaration-and-verification data* — intended instance
   characteristics, primary Region, enablement evidence, verification timestamp/cadence,
   responsible owner — and never a claim that this repository creates or owns the instance
   lifecycle. The lab's existing identity source is an **evidenced prerequisite**; missing or
   stale prerequisite evidence blocks plan/apply. `okta.yml`, SCIM desired configuration,
   and identity-source procedures are outside the slice; OD-08 and the narrowed
   prerequisite/evidence question are carried forward explicitly (T22).
3. **Workforce groups are references, never created here.** `groups/<key>.yml` declares the
   stable key, source metadata, and the identity-store lookup name; validation and plan
   resolve it (data source) and fail — never silently create — if absent. Group lifecycle
   stays with the identity source (SCIM in the target; the lab's existing source in the
   lab), preserving the T02 single-reconciliation-owner rule. The same model applies in lab
   and target.
4. **Exactly two permission sets:** (1) a read-only set using an AWS-managed policy
   attachment; (2) a narrowly scoped set using an embedded inline policy document. No
   customer-managed policy references (rejected as out-of-slice by the selected-slice
   validation profile, not prohibited by the domain architecture), no `PowerUserAccess` (its
   breadth would pre-decide T07), no administrator set.
5. **Targeting — GROUP only; 2 active named lab accounts + 1 deferred.** The same
   group→permission-set grant is represented as two separate assignment files targeting two
   explicitly named active lab accounts; the saved Terraform plan must show two distinct
   account assignments. One additional assignment references a `status: requested` inventory
   account: it validates as **deferred** (RD-08), is omitted from the executable plan, and
   that account is **never provisioned** for this fixture. USER-principal exceptions and
   OU-expansion authoring input stay outside the slice (USER principals are rejected by the
   selected-slice validation profile; RD-05's governed exception class remains defined). T16
   names the accounts within T15's contract; lab-account provisioning remains an S6
   implementation ticket.
6. **Greenfield-only; pre-existing lab resources protected.** The slice creates only new,
   repository-named permission sets and assignments in its isolated state and takes no
   authority over anything pre-existing in the lab: a saved plan that creates, modifies,
   imports, or destroys a pre-existing Identity Center resource is rejected. **This is a
   first-slice boundary, not an implementation stance: the overall implementation remains
   brownfield.** T19 plans a brownfield lab import rehearsal after the greenfield POC is
   accepted (discovery, 09 import/reconciliation sequencing, destroy blocking, rollback, the
   point at which Terraform becomes authoritative), followed by target-estate migration.

**End-to-end proof the slice must demonstrate (T02 target):** validation passes → Terraform
produces a saved plan from reviewed code showing two distinct assignments, the deferred
target, and prerequisite-evidence status → the saved plan is reviewed and explicitly
approved → that exact plan is applied only to the explicitly named lab accounts →
verification → removal of temporary test resources. AWS apply requires later, separate owner
authorization.

## Claim-resolution record (grill-with-docs)

Per claim: governing document + identifier · claim · result · upstream amendment/refinement.

**1. "Each candidate slice keeps role + policy + assignment sharing one authority boundary
expressible as one PR."**
- Authority: `00-governing-principles.md` I-8; `01-repository-boundaries.md` *Atomicity* and
  the `aws-identity-access` membership list (permission sets, standing assignments,
  enterprise roles, exceptional users all inside the durable-access boundary).
- Result: **inherited** — for every candidate A–D; I-8 does not discriminate between them.
  Slice A's content (groups as references, permission sets, assignments, `instance.yml`) is
  one authority boundary and one PR.
- Amendment: none.

**2. "'End-to-end' for the slice stays within the API/Terraform-manageable boundary 07
defines, with manual items represented as desired configuration + procedure + evidence."**
- Authority: `07-identity-center-platform.md` (*Manageable vs. manual boundary*; *Manual
  does not mean unmanaged*; `configuration/instance.yml`), RD-03, CV-07
  (`12-capability-validation.md`), OD-08 (open).
- Result: **inherited** for slice A's reconciled content (permission sets, assignments —
  manageable, to be verified at the provider pin T15 selects); **inherited** for
  `instance.yml` as declaration/verification data; the identity source and groups as
  *evidenced prerequisites* that gate plan/apply is **compatible** (07 requires evidence and
  periodic verification; the gating rule is this repository's refinement). Reconciling the
  instance or identity source via Terraform would be **conflicting** and is not done.
- Refinement: adopt as domain decisions — (a) `instance.yml` is
  declaration-and-verification data, never lifecycle ownership; (b) prerequisite evidence
  freshness gates plan/apply; (c) workforce groups are references resolved in the identity
  store, never created by this repository. Upstream: the OD-08 proposal (who performs manual
  steps, where evidence lives, revalidation cadence) is prepared by T22 and carried by the
  owner. T08 determined the durable domain decision-register form.

## Map revalidation (decision 7 — Slice-first rule)

- **Closed Out of scope:** T11 #16 (no IAM users), T12 #17 (no IAM roles/trust), T13 #18
  (no fleet roles/StackSets) — one line each on the map.
- **Narrowed or extended by comment:** T18 #5, T04 #6, T05 #7, T07 #9, T15 #10 (extended:
  selects the exact Terraform and AWS-provider versions for the lab POC without resolving
  OD-09 platform-wide; protected resources; prerequisite gating; S5 wording), T16 #11,
  T19 #14, T10 #15.
- **Fog graduated:** T21 #20 (permission-set policy representation; verifies CV-07 against
  the T15 pin; a failed CV-07 blocks until the pin is revised and reverified or Eric
  approves a temporary, dated exception), T22 #21 (manual prerequisites as governed
  configuration and evidence; OD-08 proposal), T20 #22 (CI plan contract and PR classes).
  **Transferred:** brownfield import → T19. **Ruled out:** identity-source desired
  configuration, customer-managed permission-set references, permission boundaries /
  elevation-ceiling residency.
- **T14 #19 rewired:** blocked by T04, T05, T06, T07, T09, T10, T20, T21, T22.
- **Map order:** … T10 #15 · ~~T11~~ · ~~T12~~ · ~~T13~~ · T21 #20 · T22 #21 · T20 #22 ·
  T14 #19.

## Durable owner constraints (reconfirmed at resolution)

Brownfield overall with a greenfield-only first slice; S5 must include discovery,
import/reconciliation sequencing, destroy blocking, rollback, and migration planning; zero
incremental recurring spend beyond the `mcp_gateway01` lab baseline; named lab accounts
only, no production; no AWS mutation during Wayfinder. T02 selected no version values —
exact pins and CV-07 verification are required; T15 selects the lab pins; OD-03/04/09 stay
open platform-wide.

## Glossary candidate (S5 `domain-modeling`)

**Selected-slice validation profile** — the POC's validation profile for the selected
slice, which rejects out-of-slice forms (USER principals, customer-managed permission-set
references) without prohibiting them in the domain architecture.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub mutation. This backfill
record changes nothing decided by T03.
