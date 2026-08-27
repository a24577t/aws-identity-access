---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 6
title: "T04 — Top-level layout and the requester surface"
url: https://github.com/a24577t/aws-identity-access/issues/6
type: prototype
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with prototype + grill-with-docs"
recorded: 2026-08-27
sources:
  backfill: "T08 #13 decision 13 result-record backfill, reconstructed 2026-08-27 from the ticket's complete comment history; traceability, not authority"
  revalidation_comment: https://github.com/a24577t/aws-identity-access/issues/6#issuecomment-5382170023
  resolution_comment: https://github.com/a24577t/aws-identity-access/issues/6#issuecomment-5382598602
  close_comment: https://github.com/a24577t/aws-identity-access/issues/6#issuecomment-5382599851
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  prototype: throwaway stub tree, branch prototype/t04-layout @ 1d1c625fdc287f14c8510b4684ed2cd95788192c (21 files, marker PROTOTYPE-T04.md; never merged to main)
  resolved: 2026-08-22
---

# T04 — Top-level layout and the requester surface (slice A)

> **Backfilled discovery record** — produced 2026-08-27 under the separately authorized T08
> #13 decision-13 result-record backfill, reconstructing the complete durable result of
> T04 #6 from the ticket's comment history. Backfill preserves provenance and traceability
> only: it confers no new authority, changes no decision, and does not alter the approved S4
> Architecture Grill verdict. **Nothing here is accepted architecture: every decision is a
> proposal until ⟦G-Accept⟧.** GitHub issue #6 is the workflow/index surface and links to
> this record.

Prototype grill completed and approved by Eric as the human project owner and decision
authority, 2026-08-22, under `wayfinder-repo-owner` with `prototype` + `grill-with-docs`;
six decisions taken one at a time. Governing documents cited at the aws_ami revision pinned
by T01 (#2); the T18 inventory (`docs/research/brownfield-inventory.md`, then at commit
`5e02113`) was used as implementation evidence only.

**T03 revalidation (slice A), recorded on the ticket before resolution:** the stub tree
covers `access/identity-center/{instance.yml, groups/, permission-sets/,
account-assignments/<account>/}` plus `governance/`, `docs/`, `schemas/`,
`infrastructure/`. No `iam/`, no `deployments/fleet-roles/`, no `identity-source/` desired
configuration (the identity source is an evidenced prerequisite — T22). Claim (5) was
reduced to where `instance.yml` lives relative to 07's `configuration/`. Added: the stable
naming/prefix convention for POC-created Identity Center resources so they are
distinguishable from pre-existing lab resources (#4 decision 6).

**Prototype (throwaway):** branch `prototype/t04-layout`, 21 stub files, marker
`PROTOTYPE-T04.md` — immutable commit
[`1d1c625`](https://github.com/a24577t/aws-identity-access/tree/1d1c625fdc287f14c8510b4684ed2cd95788192c)
on branch `prototype/t04-layout`; never merged to `main`. Every file marks a location only
and names the ticket that decides its content. (The stub assignment files were later
superseded by the T10 #15 record specimens.)

## Decisions

1. **Top-level separation (approved as shown).** `access/` — ordinary requester
   configuration · `governance/` — declarations that are not routine access grants ·
   `docs/` — architecture, guides, research, agents, and clearly separated generated
   material · `schemas/` — RD-04 schemas · `infrastructure/` — Terraform and deployment
   mechanics · `src/` — validation and effective-plan implementation code · `tests/` —
   executable validation tests and specimens · `.github/` — CI, CODEOWNERS, repository
   automation. Ordinary requester PRs are confined to `access/`. Qualifications: `src/` and
   `tests/` are structural stubs (T14 owns contents); generated documentation occupies a
   visibly non-authoritative subdirectory and will carry T20's source and `do_not_edit`
   metadata; documents under `docs/` do not share equal authority; `.github/`,
   `governance/`, `schemas/`, `infrastructure/`, and authoritative documentation use the
   strictest applicable owner set.
2. **Requester root.** `access/identity-center/` carries 07's `identity-center/` subtree
   re-rooted under the named requester surface; the root README defines `access/` as
   governed desired access containing no code, credentials, generated AWS identifiers, or
   runtime state.
3. **`instance.yml`.** `access/identity-center/configuration/instance.yml` — the 07/03
   shape, inherited, **no amendment**. Responsibility (T03-d2):
   declaration-and-verification data only — intended characteristics, primary Region,
   enablement evidence, verification timestamp/cadence, responsible owner; never a claim
   that this repository creates or owns the instance lifecycle. T22 owns the field set and
   evidence details.
4. **Conventions.** `access/identity-center/groups/<group-key>.yml` ·
   `access/identity-center/permission-sets/<permission-set-key>.yml` ·
   `access/identity-center/account-assignments/<account-name>/<group-key>--<permission-set-key>.yml`.
   Boundaries: groups are references only and never created by this repository; permission
   sets are repository-managed desired state; each assignment file is exactly one
   group-to-permission-set grant in one account; `<account-name>` is the stable
   organization-inventory name, never an AWS account ID; OU membership never appears in the
   natural key or directory path. The `--` separator is a T04 prototype convention only —
   T05 defines key grammar and must reserve or reject it; T10 makes the final filename
   decision. Renaming 07's `assignments/` to `account-assignments/` and adding `groups/`
   form **one proposed upstream document-07 refinement** for Eric to carry; aws_ami is not
   edited.
5. **Naming/prefix boundary (modified recommendation).** Stable keys under `access/` are
   never environment-prefixed. `infrastructure/terraform` derives deployed permission-set
   names as `<resource_name_prefix><permission-set-key>`; T15/T16 select the exact non-empty
   lab/POC prefix; the target-estate prefix is **not** decided by T04 — T19 decides target
   naming during brownfield discovery, import/reconciliation, and migration planning.
   POC-created permission sets also carry a managed-by/project marker when the selected
   provider pin supports the tagging operation (T21 verifies). Prefix and tags are
   defense-in-depth coexistence markers, not reconciliation-ownership authority. Account
   assignments are not assumed taggable: their protected scope is the governed assignment
   tuple, association with POC-managed permission sets, and isolated Terraform state. The
   protected-resource plan guard rejects any create/import/update/delete outside the
   explicitly derived POC-managed resource and assignment set; pre-existing lab resources
   are never imported, modified, or destroyed by the first slice. Adopted as a lab/POC
   domain refinement without editing aws_ami.
6. **Deliberate absences.** `access/iam/`, `access/deployments/fleet-roles/`,
   `access/identity-center/identity-source/`, `access/identity-center/bootstrap/`,
   `governance/exceptions/`, `governance/runtime-mutations/` (the OD-16 convention remains
   inherited; this slice contains no runtime-mutation contract). Recorded in three layers:
   (1) the root README's "Absent for slice A" section, each surface linked to the T03/T04
   decision or closed ticket that scoped it out, stating that later slices may introduce it
   through a governed decision; (2) the selected-slice validation profile rejecting files
   under absent paths with a stable out-of-slice error code — a POC profile rule, not a
   permanent domain-schema prohibition (T14); (3) the domain decision register preserving
   the T03/T04 slice boundary, with physical form and placement deferred to T08 and no
   parallel decision artifact invented now. No placeholder directories or marker files; the
   validator must still detect and reject those paths if files appear. Classification:
   compatible scoping, not a domain-boundary change.

## Claim-resolution record (grill-with-docs)

Per claim: governing document + identifier · claim · result · upstream amendment/refinement.

**1. The brief's `access/` root and its prohibition of `configuration/`.**
- Authority: `01-repository-boundaries.md` (boundaries follow authority and lifecycle;
  Atomicity), `10-codeowners-model.md` (path-level overrides; pipeline strictest),
  `02-configuration-model.md` (path rule), `07-identity-center-platform.md` (names only the
  `identity-center/` subtree).
- Result: **absent** — no governing document names the directory above `identity-center/`
  or prohibits any root name; a named requester surface is **compatible** with 01/10.
- Refinement: adopt `access/` as a domain decision (decisions 1–2). Upstream amendment:
  none.
- T18 evidence: the separation of schemas/governance/tools/docs/CI is reusable (X01, S01);
  the `configuration/` root is the brief's rejected name, not a governing-document
  rejection.

**2. `account-assignments/` vs 07's `assignments/`.**
- Authority: `07-identity-center-platform.md` Directory shape (`assignments/`);
  `02-configuration-model.md` path rule ("Stable AWS vocabulary identifiers that are
  themselves the human-recognized name MAY be used directly").
- Result: **conflicting** with 07's directory name; the AWS vocabulary is "account
  assignment" and Identity Center also has application assignments, so the name
  disambiguates.
- Refinement: proposed upstream document-07 refinement (one proposal with claim 3): rename
  `assignments/` → `account-assignments/`. Carried by Eric; aws_ami not edited.
- T18 evidence: per-account files (X33–X36, S18) are the partial shape; aggregated lists
  and the OU directory level are rejected for the slice.

**3. A `groups/` registry.**
- Authority: `07-identity-center-platform.md` (shape omits a workforce-group construct);
  RD-05 (group principals are the standard); I-1 (path → configuration → authoritative key).
- Result: **absent** from 07 (REVIEW I-a, Conflict 4); **compatible** with RD-05/I-1.
- Refinement: `access/identity-center/groups/<group-key>.yml` as references only (T03-d3);
  proposed upstream document-07 refinement: add `groups/` to the directory shape (same
  proposal as claim 2).
- T18 evidence: X18–X23 and X55 are reusable shape; no immutability rule (REVIEW Q3 → T05).

**4. `governance/{runtime-mutations,exceptions,ownership}` and
`docs/{architecture,guides,generated}`.**
- Authority: OD-16 / `05-runtime-mutation-contracts.md`
  (`governance/runtime-mutations/<contract>.yml`), `10-codeowners-model.md` (contract files
  approved by the resource owner's CODEOWNERS), RD-09 / `11-decision-register.md`
  (decision-register authority — T08).
- Result: `governance/runtime-mutations/` **inherited** (convention retained; no contract
  in slice A); `governance/exceptions/` and `governance/ownership/` **absent** upstream,
  **compatible** (T06 decides the ownership registry); `docs/` subdivision **absent**,
  **compatible**, with unequal authority recorded (decision 1) and the register form
  deferred to T08.
- Refinement: none upstream. Domain: decisions 1 and 6.
- T18 evidence: X13/S19 evidence the contract field set; X37's `pa-*` namespace is rejected
  as an ownership mechanism (REVIEW Q4 → T06).

**5. `identity-source/` file naming (`okta.yml` vs 07's
`desired-configuration`/`verification`) — reduced by T03 to where `instance.yml` lives.**
- Authority: `07-identity-center-platform.md` L62-64 and `03-region-model.md` L37-43
  (`identity-center/configuration/instance.yml`); RD-03.
- Result: **inherited** — `access/identity-center/configuration/instance.yml`; no
  amendment. Identity-source desired configuration is Out of scope (T03-d2); the
  prerequisite evidence record is T22's.
- T18 evidence: X14/S14 reusable location (Regions only); X16/X63 reusable evidence-record
  shape.

## Upstream proposals carried by the owner (aws_ami not edited)

- **Document 07 refinement (one proposal):** add `groups/` to the Identity Center directory
  shape; rename `assignments/` → `account-assignments/`. (Later extended by T10 #15
  decision 7 with the per-account-identity sentence.)

## Carried forward (as recorded at resolution)

- T05: key grammar; reserve or reject the `--` separator. T10: final assignment filename
  rule.
- T06: ownership registry form; CODEOWNERS mechanism for account-name paths (OU informs
  reviewer selection via the inventory only).
- T14: selected-slice validation profile — out-of-slice path rejection code; profile, never
  domain schema.
- T15/T16: lab prefix value; protected-resource plan guard. T21: tagging-operation support
  at the provider pin. T19: target-estate naming/prefix strategy. T22: `instance.yml` field
  set and prerequisite evidence. T08: decision-register form for the T03/T04 slice
  boundary. T20: generated-documentation metadata.

## Glossary candidates (S5 `domain-modeling`)

**Requester surface** — the `access/` tree; the only directory ordinary access-request PRs
modify. **Deployment-scope prefix** — a non-empty lab/POC string prepended to deployed
permission-set names by `infrastructure/`, never part of a stable key.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub mutation. This backfill
record changes nothing decided by T04.
