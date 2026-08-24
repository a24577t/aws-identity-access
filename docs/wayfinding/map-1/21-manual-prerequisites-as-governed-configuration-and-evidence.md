---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 21
title: "T22 — Manual prerequisites as governed configuration and evidence: instance.yml, identity source, group references"
url: https://github.com/a24577t/aws-identity-access/issues/21
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-24
sources:
  decision_batch: "consolidated 8-question HITL batch (2026-08-24); collaborator-recommended selections 1A–7A with corrections 1–6 and 8B, approved by Eric and applied throughout"
  inherited_inputs:
    - https://github.com/a24577t/aws-identity-access/issues/21 (five comments: T05 group prerequisite evidence, T15 prerequisite evidence inputs, T16 prerequisite inputs, T09 prerequisite evidence inputs, T10 coordination)
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
---

# T22 — Manual prerequisites as governed configuration and evidence

> Proposed discovery record — the complete durable result of T22 #21. Decisions approved by Eric
> as the human project owner and decision authority after collaborator review; executed by Claude
> in the repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`, using the
> batch-question directive (governing invariant 3 in the
> [repository-owner operating guide](../../../.ai/repository-owner/operating-guide.md)).
> **Nothing here is accepted architecture: every decision is a proposal until ⟦G-Verdict⟧ and
> ⟦G-Accept⟧.** GitHub issue #21 is the workflow/index surface and links to this record.

## Authorization scope of this record

Approving publication of this T22 result records the **proposed manual-prerequisite model
only** — the `instance.yml` field set, the prerequisite classes and their evidencing, the
freshness rule, and the OD-08 proposal text. It does **not** authorize any AWS call or
mutation, Identity Center enablement, group creation, delegated-administrator registration
(each remains a separately authorized T16 decision-11 stage), S3 write, evidence or snapshot
creation, GitHub configuration, Terraform execution, implementation, or backfill. **No
`instance.yml` file is committed now**: the layout is Pre-Baseline, and the file lands at S6
under the accepted layout (the T16 decision-15 rule applied to this artifact). Everything
remains proposed pending ⟦G-Verdict⟧ and ⟦G-Accept⟧.

## Governing documents and evidence

Cited at the `aws_ami` revision pinned by T01 (#2): `07-identity-center-platform.md`
(manageable vs. manual boundary; "Manual does not mean unmanaged"; `configuration/instance.yml`),
`09-tier0-execution.md` (documented-bootstrap rule; apply from reviewed artifact),
`02-configuration-model.md` / RD-04, RD-03, `11-decision-register.md` (OD-08 — open). Inherited
map decisions: T03 #4 (d2/d3 — declaration-and-verification data; evidenced prerequisites gate
plan/apply; groups are references, never created here), T04 #6 (07's subtree with
`configuration/instance.yml` inherited unamended), T05 #7 (group identity and `GetGroupId`
resolution contract), T06 #8 (principal keys; review routing), T15 #10 (d3/d4 regional values
and instance consumption; d12 evidence tiers; d15 reduced-assurance honesty), T16 #11 (d5/d6
prerequisites; d11 staged separate authorizations), T09 #12 (snapshot envelope; `current`
pointer; 90-day backstop; `snapshot_id` public-safe; verification-record digest in the
authorization binding), T10 #15 (assignment files carry only `principal.group`), T21 #20
(domain-vs-profile code separation). Evidence (never authority): the 2026-08-23 T16 sanitized
discovery (all prerequisites absent).

## Settled inputs (fixed by prior decisions; recorded, not re-decided)

- Path: `access/identity-center/configuration/instance.yml` (T04; document 07 subtree).
- Regional values: `primary_region: us-east-1`, `additional_regions: []` (T15 d3);
  `instance.yml` is the sole regional authority; the snapshot's `identity_center.region` is a
  projection that must equal it (T09 d5).
- Instance ARN, identity-store ID, and GroupIds are never committed; they live only in the
  non-public binding snapshot and evidence (T15 d4, T09, T05 d2).
- Group declaration: `groups/<group-key>.yml` with `key`, required `identity_store_name`,
  optional informational `source:` (T05 d2); resolution via Identity Store `GetGroupId` with
  exact-DisplayName verification; failure is a plan error, never deferred, never created.
- Prerequisite set: organization instance in `us-east-1`; Identity Center default identity
  store; the hand-created first workforce group (T16 Stage 5.2); `lab-tooling` registered as
  delegated administrator scoped to `sso.amazonaws.com` (T15 d2/d4, T16 d5/d6, T09 d5). All
  were absent on 2026-08-23; every enablement is separately authorized S6 remediation
  (T16 d11 Stages 0–6).
- Freshness machinery: live re-verification at every plan and apply plus the 90-day backstop
  from the snapshot's `discovered_at`; validation runs with no AWS identity and never reads
  the snapshot (T09 d10/d15, T15 d6).

## Claim-resolution record (grill-with-docs)

| # | Claim | Authority | Result | Upstream amendment / refinement |
|---|---|---|---|---|
| 1 | `instance.yml` is declaration-and-verification data — intended instance characteristics, primary Region, enablement evidence, verification timestamp/cadence, responsible owner — and never a claim that this repository creates or owns the instance lifecycle | `07` ("Manual does not mean unmanaged"; `configuration/instance.yml`), RD-03, T03 d2, T15 d3/d4 | **inherited** — T22 fixes only the exact committed field set and verification-block structure (decisions 1–2) | none new |
| 2 | The lab identity source and every referenced workforce group are evidenced prerequisites; missing or stale prerequisite evidence blocks plan and apply | `07` (evidence + periodic verification), T03 d2/d3, T05 d2, T16 d5, T09 d10/d15 | **inherited** for the gating rule; the freshness definition, the API-verifiable vs. human-attested split, and the enforcement-stage assignment are this repository's **compatible** refinement (decisions 3–5) | none new |
| 3 | The evidence form, location, and cadence constitute an OD-08 proposal to carry upstream, not a local invention | OD-08 (open at the pin), `09` (documented-bootstrap rule), README staging-workspace notice | **compatible** — the lab instantiation is generalized into the OD-08 proposal of decision 7, carried by Eric; aws_ami is never edited by this repository | OD-08 proposal (decision 7) |

## Decisions

Eric approved the collaborator-recommended selections 1A–7A with corrections 1–6 and 8B,
applied throughout.

### Decision 1 — `instance.yml` committed field set and verification-block structure

Exact field set; unknown fields rejected; no additional properties. Schema illustration —
angle-bracket tokens are **placeholders, not values**; no verified prerequisite evidence
exists today:

```yaml
# access/identity-center/configuration/instance.yml — schema illustration
instance_type: organization
primary_region: us-east-1
additional_regions: []
identity_source:
  type: identity-center-default
delegated_administrator: lab-tooling
owner: identity-platform
verification:                      # optional; all-or-nothing; absent = unverified
  verified_at: "<exact RFC 3339 UTC body.discovered_at string from the referenced snapshot>"
  snapshot_id: "<64 lowercase hexadecimal — the snapshot content digest>"
```

- `instance_type` — closed vocabulary `organization`; an account instance is rejected
  (T16 d5's rejected alternative made structural).
- `primary_region` / `additional_regions` — must equal the T15 d3 values; `instance.yml`
  remains the sole regional authority (T09 d5).
- `identity_source.type` — decision 2.
- `delegated_administrator` — an inventory alias in the established alias grammar; a declared
  prerequisite only: designation authority stays with the organization mechanism, and this
  repository never performs registration (T16 d6; map Out-of-scope).
- `owner` — a T06 principal key; the responsible owner of the manual prerequisites
  (`identity-platform`).
- `verification` — **optional and structurally all-or-nothing**: when absent, prerequisite
  evidence is **unverified**; when present, both fields are required. `snapshot_id` is exactly
  64 lowercase hexadecimal characters and is the **binding reference** to the current binding
  snapshot. `verified_at` is the exact RFC 3339 UTC `body.discovered_at` string of the
  referenced snapshot — an **informational projection of that authoritative value**, never an
  independently authored freshness clock. The schema accepts the complete RFC 3339 UTC
  representation T09 permits for `body.discovered_at`, including a valid fractional-seconds
  component when present; no independent normalization, truncation, rounding, or second
  timestamp authority is introduced. Projection rule, enforced at plan/apply: byte-for-byte
  equality with the referenced snapshot's `body.discovered_at`. The 90-day calculation uses the
  snapshot's `discovered_at` only.

All values are alias-form and public-safe; no ARN, ID, or live identifier field exists in the
schema. Classification: **inherited** (T03 d2's enumeration made exact; `07`); the
all-or-nothing block and projection rule **compatible** (absent upstream). Rejected: a separate
committed `verification.yml` (splits what T03 d2 assigns to `instance.yml`); verification only
in non-public evidence (loses the committed reviewable surface `07` requires).

### Decision 2 — Identity-source representation in slice A

`identity_source.type` inside `instance.yml` is the complete slice-A identity-source
declaration. The `identity-source/` subtree (document 07's `desired-configuration` and
`verification`) is **absent for slice A** and recorded as an absent surface (the T04
absent-surfaces pattern); `okta.yml`, SCIM configuration, and identity-source procedures remain
outside the map (T03). The domain schema defines `type` as a governed vocabulary extensible by
a future governed decision; the selected-slice profile requires exactly
`identity-center-default`, rejecting any other value as out-of-slice under the `P-OOS-*`
profile family (naming input to T14). Classification: **compatible** (`07` requires desired
configuration for manual controls; the one-field fold satisfies it at slice scale). Rejected:
a minimal `identity-source/verification.yml` now (reintroduces a surface T03 ruled out);
no committed declaration (prerequisite invisible in the requester surface).

### Decision 3 — Prerequisite classes: API-verifiable vs. human-attested; group evidencing

Prerequisites divide into two classes with different verification semantics:

- **API-verifiable prerequisites** — instance presence and type where the authorized APIs
  expose it, the identity-store binding, the delegated-administrator registration scoped to
  `sso.amazonaws.com`, and **every referenced workforce group's resolution** (`GetGroupId`
  with exact-DisplayName verification, T05 d2) — are **reverified live at every plan and
  apply**.
- **Non-API-verifiable characteristics** — including any console-observed identity-source
  property — are recorded as **human attestations** in the Prerequisite Verification Record
  (decision 5). Plan and apply verify the attestation's **binding, integrity, referenced
  snapshot, and freshness**; they do **not** claim to re-observe the characteristic through
  AWS APIs. Missing, expired, mismatched, or integrity-invalid attestation evidence fails
  closed.

Group references carry **no committed per-group verification stamps**: live resolution at
every run is strictly fresher than any stamp, and the group file itself (T05 d2) plus the
committed `verification` block are the complete committed surface. The T09 snapshot envelope
and field-authority table are **not amended**. Classification: **inherited** (T05 d2, T03 d3)
with the two-class split **compatible** (absent upstream; honesty rule). Rejected: extending
the T09 snapshot with a groups section (reopens a resolved contract; couples group churn to
the account-fixture digest); committed per-group stamps (public churn, a second staleness
surface, no gate improvement).

### Decision 4 — Freshness rule: fresh, stale, enforcement stages, severity, diagnostics

**Fresh** ⇔ all of:

1. the committed `verification` block is present;
2. its `snapshot_id` equals the `current` pointer's snapshot and that snapshot passes the T09
   digest-integrity checks;
3. the snapshot is within the **90-day backstop** from its `body.discovered_at` — the one
   backstop constant, defined by T09 d10 and cited, never a second number;
4. live re-verification succeeds for **every API-verifiable prerequisite**, and **every
   non-API observation** has valid evidence bound to the current authorized verification
   record and snapshot.

**Stale** = any failure of 2–4. **Missing** = 1 absent. Enforcement stages: **validation is
hermetic and deterministic** — schema, formats (64-hex, RFC 3339 UTC), internal consistency,
and deterministic diagnostics only; it holds no clock, reads no snapshot, and makes no AWS
call (T15 d6, T09 d15, T05 d5). **Plan and apply own the clock, snapshot, evidence, and AWS
checks** and fail closed. Severity: **error** — never a warning, never deferred (deferral
remains reserved for `status: requested` inventory references, RD-08). T03 d2's "blocks plan
and apply" lands verbatim.

Diagnostics — proposed **`PRQ-*` domain family as input to T14** (final codes, severities,
and harmonization with `INV-*`/`E-*` are T14's; this record confers no code ownership),
distinguishing at minimum:

| Proposed code | Condition |
|---|---|
| `PRQ-MISSING` | committed `verification` block absent (unverified prerequisites) |
| `PRQ-SNAPSHOT` | referenced snapshot mismatch with `current`, expiry beyond the backstop, or digest/integrity failure (T14 harmonizes overlap with `INV-STALE`/`INV-DIGEST`/`INV-MISSING`) |
| `PRQ-INSTANCE` / `PRQ-IDENTITY-STORE` / `PRQ-DELEGATED-ADMIN` | an API-verifiable prerequisite failure — instance presence/type where exposed; the Identity Store binding; the `sso.amazonaws.com`-scoped delegated-administrator registration |
| `PRQ-ATTESTATION` | missing, stale, mismatched, integrity-invalid, or otherwise invalid human attestation about a non-API-verifiable characteristic (including console-observed identity-source characteristics) |
| `PRQ-GROUP` | referenced-group resolution failure (the T05 d2 plan error given a stable prerequisite code) |

Classification: **compatible** (refines T03 d2 with T09's already-proposed machinery).
Rejected: calendar checks at validation (time-dependent validation breaks deterministic
diagnostics); an approaching-expiry warning (excess ceremony; the fail-closed error already
forces action); calendar-only trust without live re-verification (rejected by T09 d10).

### Decision 5 — The Prerequisite Verification Record and evidence-tier classification

One **Prerequisite Verification Record** per Stage 6.1 re-discovery: a non-public record under
the run-scoped evidence path (`aws-identity-access/evidence/`), containing the
prerequisite-by-prerequisite results with **method** (`api` or `human-attestation`), the API
evidence or the attestation content and actor, timestamps, and the associated `snapshot_id`
and fixture digest. Live identifiers are permitted there. Its digest is bound into the
saved-plan authorization **as T09 decision 16 already requires**; `instance.yml` does **not**
duplicate that digest (no second authority location was demonstrated).

Evidence-tier classification (T15 decision 12), stated explicitly:

- committed alias-only `instance.yml` declaration and verification reference = **tier 3
  prerequisite evidence**;
- the non-public Prerequisite Verification Record (methods, observations, live identifiers)
  = **tier 2 lab-run evidence**;
- public artifacts may expose only the permitted aliases, digests, `snapshot_id`, and
  verification state.

No record, snapshot, or S3 write is created now; the first Prerequisite Verification Record
exists only after the separately authorized Stage 6.1/6.3 sequence. Classification:
**inherited** (T15 d12, T09 d16/d20) with the record's content definition **compatible**
(absent upstream). Rejected: a public committed verification record (duplicates the committed
block; leak-by-edit risk); relying on the snapshot alone (no home for group results or human
observations without amending T09).

### Decision 6 — Actors: performer, attestation, discovery transport, pipeline checks

- **Eric performs each separately authorized manual/console step** (T16 decision-11 Stages
  0–6; reaffirmed, not re-decided).
- A **console-only observation made by Eric is recorded as Eric's attestation**, together
  with the lab's reduced-assurance condition (one physical identity, T15 d15); it is never
  implied to be independent repository-owner verification.
- **Stage 6.1 repository-owner read-only discovery** (named lab profile) verifies only what
  its authorized APIs can establish, and **transports and binds** the human observations into
  the Prerequisite Verification Record without upgrading them to API-verified fact.
- **Plan and apply roles** perform the API-verifiable checks and the evidence
  integrity/freshness checks of decisions 3–4 under their decision-6/decision-14 read sets
  (T15, T09).
- The responsible owner recorded in `instance.yml` is `identity-platform` (T06 principal
  key). **Verification updates** (a new `verified_at`/`snapshot_id` after re-discovery) land
  only as governed PRs; T22 assigns no PR class — the class assignment is T20's.

Classification: **compatible** (OD-08's triad instantiated honestly; `09`
documented-bootstrap rule). Rejected: pipeline-automated bumps of the committed block
(automation authoring its own gate input inverts the governed-PR surface); scheduled human
attestation without live re-verification (calendar trust, rejected by T09 d10).

### Decision 7 — OD-08 upstream proposal and document-07 disposition

Proposal text carried by Eric, associated with OD-08 in `11-decision-register.md`
(aws_ami is never edited by this repository):

> **OD-08 proposal:** Manual/console-oriented Identity Center configuration is performed by
> the identity-platform owner under separate, explicit per-step authorization. It is
> represented as declaration-and-verification data in `configuration/instance.yml` (declared
> characteristics, identity-source type, delegated administrator, responsible owner,
> verification reference); evidence lives in two tiers — a committed, alias-only declaration
> referencing the evidence snapshot by content digest, and non-public encrypted evidence
> holding live identifiers. API-verifiable prerequisites are reverified live at every plan
> and apply. Characteristics not exposed to the authorized APIs are carried as explicitly
> human-verified observations in the bound non-public verification record. Both are subject
> to the snapshot-based maximum-age backstop of 90 days from `discovered_at`; missing, stale,
> mismatched, or invalid evidence blocks plan and apply.

Document-07 disposition: the extended `instance.yml` field set is a **compatible
instantiation** of 07's "manual does not mean unmanaged" pattern; **no new document-07
amendment** is carried, and the existing carried document-07 proposal (T04, extended by T10)
is unchanged. The upstream-proposals index (due no later than the S5 acceptance branch,
T08 d8) gains one OD-08 entry sourced to this record. Classification: **compatible**.
Rejected: an ownership-only proposal (leaves two of OD-08's three named questions
unanswered); deferring until after lab execution (the map already carries proposals
pre-execution — OD-21 precedent; T08 d8's index deadline).

### Decision 8 — Durable record and publication sequence (review-then-publish)

This record at
`docs/wayfinding/map-1/21-manual-prerequisites-as-governed-configuration-and-evidence.md`
with a `docs/wayfinding/README.md` index line. Under the selected review-then-publish form,
publication executes only after Eric reviews the exact drafted bytes — the record, the whole
`docs/wayfinding/README.md` successor, the tracker-payload bundle (resolution comment, close
comment, map line, three handoffs, and the substitution instructions), and the continuity
template, each bound by SHA-256 in the review package — and gives consolidated approval; the
fail-closed sequence below then runs unchanged. Rejected: publish-on-selection without byte review (the prior default; Eric chose
the added review round); resolving in-comment only without a durable record (breaks the
established record-first pattern).

## Glossary candidates (S5 `domain-modeling`)

**Manual prerequisite** — a condition established outside this repository by separately
authorized human action, consumed here only as declaration plus evidence.
**Declaration-and-verification data** — governed configuration stating intended manual state
and referencing its evidence, never asserting lifecycle ownership. **API-verifiable
prerequisite** — a manual prerequisite whose satisfaction the pipeline's authorized read APIs
can establish live at plan/apply. **Human attestation** — a recorded, named-actor observation
of a characteristic not exposed to the authorized APIs, bound into the verification record
and never upgraded to API-verified fact. **Prerequisite Verification Record** — the
non-public per-re-discovery record of prerequisite-by-prerequisite results and methods,
digest-bound into the saved-plan authorization. **Prerequisite evidence** — the tier-3
committed alias-form declaration plus its tier-2 non-public verification artifacts.
**Fresh / stale** — per decision 4: fresh requires the committed block, the current intact
unexpired snapshot, live API checks, and validly bound attestations; anything less is stale
or missing and blocks plan and apply.

## Downstream handoffs (proposals; posted after publication)

- **T14 #19:** `instance.yml` schema checks (closed vocabularies; regional equality with
  T15 d3; alias grammar; all-or-nothing `verification` block; the 64-lowercase-hex format and
  the complete RFC 3339 UTC representation T09 permits for `body.discovered_at`, fractional
  seconds included when present; unknown-field rejection); the hermetic-validation boundary
  (schema, formats, internal consistency, deterministic diagnostics at validation — clock,
  snapshot, evidence, and AWS checks at plan/apply); the `PRQ-*` family as input
  (`PRQ-MISSING`, `PRQ-SNAPSHOT`, `PRQ-INSTANCE`, `PRQ-IDENTITY-STORE`,
  `PRQ-DELEGATED-ADMIN`, `PRQ-ATTESTATION`, `PRQ-GROUP`) with the five required
  distinctions; the `P-OOS-*` identity-source profile input.
- **T20 #22:** the prerequisite gate at plan and apply; public-safe prerequisite reporting in
  the plan summary (aliases, digests, `snapshot_id`, verification state only); the
  verification-update governed PR needing a T20 class; the verification-record digest already
  bound per T09 d16.
- **T23 #23:** `instance.yml` is governed configuration (tier 3), not documentation — the
  documentation-set header rule need not apply to it; the configuration-contract document
  covers the decision-1 field set by citation; the identity-source subtree is an absent
  surface; non-public evidence is referenced from documentation only by `snapshot_id`/digests.

## Dependency effects and frontier

#21 has native edges blocked-by 0 (all three blockers closed), blocking 2 (#22, #19). Closing
#21 reduces T20 #22 to **zero** open blockers (**unblocked**) and T14 #19 to **one** (#22).
Live frontier after closure, in map order: **T23 #23 (next claimable)** · T20 #22. T14 #19
remains scheduled after T23 #23 and T20 #22 under the current map order. One HITL ticket per
session — nothing is claimed at publication.

## Publication sequence (fail-closed; record before close)

Executed only under Eric's consolidated publication approval of the exact reviewed bytes. A
failure at any step through 8 leaves #21 open, with all later normal publication steps
unperformed; completed remote writes are not automatically undone. The exact partial state is
preserved through a Repository Continuity Artifact where necessary and reported.

1. Create this record at
   `docs/wayfinding/map-1/21-manual-prerequisites-as-governed-configuration-and-evidence.md`
   and the `docs/wayfinding/README.md` index line in the working tree, byte-identical to the
   approved package (SHA-256 verified).
2. Validate them on the final bytes: frontmatter parses, internal links resolve, the
   mechanical checks pass; no live identifier, no acceptance claim.
3. Commit both on `main`; push (authorized as part of the consolidated approval).
4. Verify the immutable record URL at the pushed commit resolves and is byte-equivalent to
   the local file.
5. Post the exact #21 resolution comment from the hash-bound tracker-payload bundle, with
   the record commit SHA filled in.
6. Post the exact informational handoff comments from the same bundle to T14 #19, T20 #22,
   and T23 #23; no dependency edges.
7. Update map #1: append exactly the one T22 Decisions-so-far line from the bundle. No fog
   edit and no map-order change (T22 graduates nothing and creates no ticket).
8. Round-trip verify: the #21 resolution comment, all three handoff comments, and the
   complete map #1 diff (exactly the one addition).
9. If any step through 8 fails: leave #21 open, perform no later normal publication step,
   preserve the exact partial state through continuity if necessary, and report it.
10. Close #21 as completed, retaining assignee `a24577t`, with the exact close comment from
    the bundle.
11. Round-trip verify the close; verify T20 #22 now shows zero open blockers (unblocked) and
    T14 #19 one (#22).
12. Recompute all dependency effects and the live frontier (expected state above) without
    claiming anything.
13. Replace the Repository Continuity Artifact (position after T22; frontier at T23 #23; the
    OD-08 proposal added to the carried set; the CV-07 split disposition and open
    import-redaction verification carried unchanged), substituting the actual record commit
    SHA. The template hash binds the pre-substitution bytes; the committed bytes differ only
    by deterministic replacement of `<RECORD-COMMIT-SHA>` with the 40-hex record commit SHA.
    Commit and push.
14. Verify `HEAD == origin/main`, a clean working tree, and the final tracker invariants
    (#21 closed with assignee retained; map body as verified; no other issue state changed).

Post-close failure rule: if a failure occurs after step 10, do not reopen #21 and do not
duplicate earlier writes; record the precise partial state in continuity where possible,
report it, and stop.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Verdict⟧ and ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub
mutation, any enablement or registration, any S3 write, or any implementation.
