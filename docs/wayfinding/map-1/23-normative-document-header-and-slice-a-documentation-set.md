---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 23
title: "T23 — Normative-document header and slice-A documentation set"
url: https://github.com/a24577t/aws-identity-access/issues/23
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-24
sources:
  decision_batch: "consolidated 8-question HITL batch (2026-08-24); collaborator-recommended selections 1A–8A with corrections 1–8, approved by Eric and applied throughout"
  inherited_inputs:
    - https://github.com/a24577t/aws-identity-access/issues/23 (three comments: T19 migration-note content input, T21 canonical-example input, T22 documentation-set coordination)
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
---

# T23 — Normative-document header and slice-A documentation set

> Proposed discovery record — the complete durable result of T23 #23. Decisions approved by Eric
> as the human project owner and decision authority after collaborator review; executed by Claude
> in the repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`, using the
> batch-question directive (governing invariant 3 in the
> [repository-owner operating guide](../../../.ai/repository-owner/operating-guide.md)).
> **Nothing here is accepted architecture: every decision is a proposal until ⟦G-Verdict⟧ and
> ⟦G-Accept⟧.** GitHub issue #23 is the workflow/index surface and links to this record.

## Authorization scope of this record

Approving publication of this T23 result records the **proposed header schemas,
authority-class vocabulary, and slice-A documentation-set composition only**. It does **not**
authorize authoring any document of that set — the normative documents, guides, and index are
S5 activities performed on the acceptance branch under the gate; generated content arrives
only with the S6 tooling. It authorizes no file under `docs/architecture/`, `docs/guides/`,
`docs/adr/`, or `docs/generated/`, no implementation, backfill, AWS activity, S3 or evidence
creation, GitHub configuration, tagging, release work, or aws_ami edit. Everything remains
proposed pending ⟦G-Verdict⟧ and ⟦G-Accept⟧.

## Governing documents and evidence

Cited at the `aws_ami` revision pinned by T01 (#2): `docs/architecture/README.md` (document
status values `normative` / `register` / `checklist`; the `status` / `destination` / `decided`
frontmatter convention; staging-workspace notice; RD-09 restatement), `11-decision-register.md`
(RD-09), `01-repository-boundaries.md` (boundary counterexample content), root platform
`CONTEXT.md` (glossary precedent — no frontmatter). Repository authority: MADR-0002
(immutable baselines, append-only refinement), the lifecycle model, T08 #13 (d1–d6 register
form and header precedent; d8 upstream-proposals index; d11 S6 CI frontmatter requirement).
Intake proposal (not authority): the brief's authority-hierarchy metadata rules (normative /
informative + authority, scope, decision owner; guides cite their normative sources; generated
documents carry `do_not_edit` and named sources; the root README is navigation, not normative
architecture) and its documentation-deliverables list. Inherited map decisions: T03 #4 (slice
boundary), T04 #6 (d1 layout; d6 absent-surfaces pattern), T19 #14 (migration-note content
input), T20 #22 (owns PR classes and generated-document metadata — coordination only), T21 #20
(canonical-example input), T22 #21 (configuration-vs-documentation boundary; evidence
references by `snapshot_id`/digest only).

## Settled inputs (fixed by prior decisions; recorded, not re-decided)

- `docs/` subdivides into `architecture/` (authoritative), `guides/` (explanatory,
  non-authoritative), and a visibly non-authoritative `generated/`; documents under `docs/` do
  not share equal authority; absences are recorded in the root README, the slice profile, and
  the register (T04 d1/d6).
- The domain decision register is ADR-primary at `docs/adr/NNNN-slug.md` with the T08
  decision-5 header; acceptance only at ⟦G-Accept⟧/⟦G-Refine⟧; superseded ADRs stay
  byte-unchanged (T08 d1–d6, d9; MADR-0002).
- `docs/architecture/upstream-proposals.md` is required no later than the S5 acceptance branch
  as an informative index (T08 d8).
- Slice A contains no IAM users, roles, or fleet content (T03); the exceptional-IAM-user
  material is out of slice.
- Migration-note content is T19's (decision 1 retire rows with cited bases; the nine rejected
  conventions; the pinned scaffold and exploratory trees retired as implementation sources
  while the pinned platform documents and register remain governing authority).
- The T21 specimens `read-only` and `identity-inventory-reader` are **owner-approved proposed
  canonical examples** (proposals until ⟦G-Accept⟧), to be presented with both policy forms,
  the explicit `session_duration` requirement, the partition-qualified AWS-managed reference
  rule, and the `P-OOS-*`-vs-domain-prohibition distinction.
- `access/identity-center/configuration/instance.yml` is governed configuration (T15 d12
  tier 3), never documentation; the configuration-contract document covers the T22 decision-1
  field set and verification-block semantics **by citation**; the identity-source subtree is an
  absent surface; non-public evidence is referenced from documentation only by
  `snapshot_id`/digests (T22).

## Claim-resolution record (grill-with-docs)

| # | Claim | Authority | Result | Upstream amendment / refinement |
|---|---|---|---|---|
| 1 | The T08 decision-5 register header extends to the whole normative document set | aws_ami `docs/architecture/README.md` frontmatter convention at the pin; T08 d5/d6; MADR-0002 | **compatible with adaptation** — the header extends **minus `supersedes`**: `supersedes` expresses decision-record supersession and remains exclusive to register records; accepted architectural decisions evolve through append-only ADR refinements under MADR-0002, and later immutable baselines consolidate them; T23 introduces no separate in-place mutation rule for accepted normative documents (decision 1). The lifecycle `status` field is **absent** upstream and is a domain addition consistent with T08 d6 | none |
| 2 | Guides and walkthroughs are `informative` and must cite the normative sources they derive from | brief (a proposal, not authority); aws_ami vocabulary at the pin (no informative class) | **absent** upstream; **compatible** — adopted as the domain informative class with a mandatory non-empty, deduplicated, resolvable `derives_from` citation (decision 2); precedent already set by T08 d8's `authority: informative` index | none |
| 3 | The documentation-set composition holds against the slice-A scope with each piece's owning ticket respected | T03 d1/d5; T04 d1/d6; the T19/T20/T21/T22 handoffs | **compatible scoping** — the brief's list narrows: exceptional-IAM-user material falls to the absent-surfaces record; migration-note content stays T19's, PR classes and generated metadata stay T20's, canonical examples are T21's, `instance.yml` coverage is by citation of T22; T23 decides only composition, authority class, placement, and citation duties (decisions 5–7) | none |

## Decisions

Eric approved the collaborator-recommended selections 1A–8A with corrections 1–8, applied
throughout.

### Decision 1 — Normative-document header

Every normative domain document (`docs/architecture/`, normative class) carries:

```yaml
status: proposed          # closed set: proposed | accepted; flipped only at ⟦G-Accept⟧/⟦G-Refine⟧
authority: normative
scope: <what the document binds>
decision_owner: "Eric — human project owner and decision authority"
```

**Conditional field and enforcement timing.** While `status: proposed`, `decided` is absent.
When the gate changes `status` to `accepted`, `decided: <YYYY-MM-DD>` is **required and added
atomically in the same acceptance-gate merge**. Unknown fields are **prohibited by this
contract immediately**; the S6 CI frontmatter check (T08 d11) later **automates** enforcement —
it does not create the rule.

**Why no `supersedes`.** `supersedes` remains exclusive to ADR/register records because it
expresses decision-record supersession. Accepted architectural decisions evolve through
append-only ADR refinements under MADR-0002, and later immutable baselines consolidate those
refinements. T23 does **not** introduce a separate in-place mutation rule for accepted
normative architecture documents; the exact publication and versioning form of the normative
documents must conform to the existing baseline lifecycle when S5 authors them — nothing here
decides that accepted normative bytes may be rewritten.

Classification: **compatible with adaptation** (claim 1); the lifecycle `status` field is
absent upstream and consistent with T08 d5/d6. Rejected: the full T08 header including
`supersedes` on documents (imports decision-record supersession semantics documents do not
carry); the aws_ami three-field form verbatim (loses the established lifecycle and
reintroduces the N/A `destination`).

### Decision 2 — Informative-document header

Every informative domain document carries a deliberately minimal header:

```yaml
authority: informative
derives_from:             # non-empty; deduplicated; every entry resolvable
  - <repository normative-document path>
  - <domain ADR identifier or path>
  - <immutable pinned platform identifier or URL>
```

`derives_from` must be **non-empty, deduplicated, and resolvable**: each entry is a repository
normative-document path, a domain ADR identifier/path, or an immutable pinned platform
identifier/URL. An informative document may **summarize** its sources but cannot create or
override normative rules. No `status`, `scope`, or `decision_owner`: informative documents
bind nothing and decide nothing. Unknown header fields are prohibited by the applicable schema
immediately; the S6 CI check later automates this. Classification: **absent** upstream,
**compatible** (claim 2; T08 d8 precedent). Rejected: the full decision-1 header on
informative documents (implies decision authority where none exists); a prose citation footer
(mechanically unverifiable).

### Decision 3 — Authority-class vocabulary and the aws_ami mapping

The domain authority-class vocabulary is the closed set **`normative | informative |
generated`**. The aws_ami `register` kind is realized in this repository as the `docs/adr/`
records (T08 d1, decision-5 header); `checklist` is unused in slice A — a future
validation-checklist document adds the value only by governed decision. Recorded mapping:
domain `authority` ≈ aws_ami `status` (document kind); domain `decided` ≈ aws_ami `decided`;
aws_ami `destination` — N/A here (nothing migrates out), per the T08 d5 precedent; the domain
lifecycle `status` is an addition absent upstream.

**Generated-document ownership boundary.** Generated documents use **T20's full metadata
schema**; T23 contributes **only the required authority-class value `authority: generated`**.
`do_not_edit`, named-source fields, provenance, and every other generated-metadata concern
remain **T20-owned**. `docs/generated/**` is **excluded from the decision-1/decision-2 header
schemas, not exempt from metadata**. No generated file is authored at S5.

**Migrated-in rule.** If a platform document whose `destination` is this repository (document
07) ever migrates in, it arrives with its platform frontmatter unmodified and is adopted under
the domain header only by a separate governed decision.

Classification: **compatible** (the vocabulary instantiates the pin's kind convention for a
domain repository). Rejected: aws_ami's exact vocabulary as header values (leaves guides and
generated material unclassifiable); a two-class set with generated material marked solely by
T20 metadata (loses the one-field authority answer).

### Decision 4 — Header applicability boundary

The header rule applies to **`docs/architecture/` and `docs/guides/`** (and any future
informative document wherever a governed decision designates it). Named exclusions, each with
its own established form: `docs/adr/` (T08 decision-5 header); `docs/wayfinding/` (established
record frontmatter; proposed discovery, never accepted architecture); `docs/research/`
(research-note convention); `docs/agents/` (agent-configuration domain); `docs/generated/**`
— excluded from the decision-1/decision-2 header schemas but **not exempt from metadata**: it
carries T20's full generated-metadata schema plus the decision-3 authority-class value; the
**root README** — exempt as navigation (the brief's rule); the **root `CONTEXT.md`** glossary
— exempt, following the platform precedent (the pinned platform `CONTEXT.md` carries no
frontmatter); `.ai/**` (methodology domain); the intake brief (historical input); everything
under `access/` (governed configuration, per T22 — never documentation).

**Exemption is not authority.** Exemption from frontmatter does not make the root README or
`CONTEXT.md` independent authority: they summarize and navigate **only by citation**; accepted
decisions and normative architecture prevail on any conflict; and the README's absent/pending
documentation section must **cite the decisions establishing each absence**. Classification:
**compatible** (enumerable, CI-checkable boundary; nothing committed needs retrofitting).
Rejected: headers on every `.md` under `docs/` (retrofits committed proposed records for no
authority gain); headers on the README and `CONTEXT.md` (contradicts the brief's navigation
rule and the platform glossary precedent).

### Decision 5 — Slice-A normative document set

Exactly **two normative documents** at S5, with stable descriptive filenames (no numeric
prefixes; reading order lives in the root README's documentation section; no separate
`docs/architecture/README.md` index):

1. `docs/architecture/domain-overview.md` — the slice-A domain architecture: requester
   surface, the federated identity chain as instantiated here, the manual-prerequisite model,
   the profile-vs-domain distinction, and a **repository-boundary counterexamples section**
   (what deliberately lives elsewhere per document 01 — temporary elevation, runtime grants,
   workload roles, inventory authority) folded here rather than a separate document at slice
   scale.
2. `docs/architecture/configuration-contract.md` — the governed file forms (`groups/`,
   `permission-sets/`, `account-assignments/`, `configuration/instance.yml`) with their
   identity, grammar, and validation semantics **by citation** of the T05/T10/T21/T22
   decisions and `schemas/` pointers.

The filenames are **logical S5 authoring targets subject to the repository's immutable
baseline/publication structure**; T23 does not authorize overwriting an accepted version
later. The documents **synthesize and explain accepted architecture with precise citations**;
they must not duplicate decision authority or restate pinned platform rules as independently
owned decisions. `docs/architecture/upstream-proposals.md` remains **explicitly informative**
(decision-2 header) even though it resides under `docs/architecture/` (T08 d8).
Classification: **compatible scoping** (claim 3). Rejected: configuration-contract only
(leaves the domain-architecture deliverable and the counterexamples record homeless); the
brief's full numbered list with out-of-slice placeholders (manufactures empty normative
surface for content T03 scoped out).

### Decision 6 — Slice-A informative set

Five informative documents under `docs/guides/`:

1. `requester-guide.md`
2. `reviewer-guide.md`
3. `federated-access-walkthrough.md`
4. `pr-scenarios.md`
5. `migration-note.md`

Guides 1–2 are built on the two T21 **owner-approved proposed canonical examples**
(`read-only`, `identity-inventory-reader` — proposals until ⟦G-Accept⟧), presenting both
policy forms, the explicit `session_duration` requirement, the partition-qualified AWS-managed
reference rule, and the `P-OOS-*`-vs-domain-prohibition distinction, citing the normative
sources. Guide 3 instantiates the federated chain for slice A, with the lab caveat that the
identity source is the Identity Center default store; the exceptional-IAM-user walkthrough is
out of slice (absent-surfaces record). Guide 4 contains **three end-to-end PR scenarios** — an
access-grant PR (the T10 assignment pair plus the deferred `lab-requested` target), an
access-definition PR (a new permission set per T21), and a verification-update PR (the T22
`verified_at`/`snapshot_id` bump) — with PR classes referenced by citation of T20's future
definitions, never defined here. Guide 5 is the migration/reference note whose **content is
T19's** (decision 1 retire rows with cited bases; the nine rejected conventions; the pinned
scaffold and exploratory trees retired as implementation sources while the pinned platform
documents and register remain governing authority); T23 fixes only its place and class.

At S5 the guides derive from the **accepted normative sources and ADRs produced by the gate**.
Ownership boundaries preserved: T19 owns migration-note content; T20 owns PR classes and
generated metadata; T21 supplies the two example forms and the profile/domain distinction;
T22 supplies the `instance.yml` and evidence-reference semantics; **T23 decides only
composition, authority class, placement, and citation duties**. Non-public evidence appears in
every guide only as `snapshot_id`/digest references. Classification: **compatible scoping**
(claim 3). Rejected: one combined handbook (merges audiences the CODEOWNERS model separates);
swapped scenario subjects (the key-rename flow is a two-PR migration — a poor introductory
scenario; verification-update exercises the model the slice ships).

### Decision 7 — Generated effective-access examples

`docs/generated/` holds the effective-access examples under **T20's full generated-metadata
schema plus the decision-3 `authority: generated` value**; T23 contributes only that
authority-class value, and `do_not_edit`, named sources, provenance, and all other generated
metadata remain T20-owned. **No generated file is authored at S5** — generation requires the
S6 tooling; the root README's absent/pending documentation section records this, citing the
establishing decisions. Generated material is never hand-edited and never authoritative.
Coordination statements (no new dependency edges): to **T20** — the authority-class value
joins its metadata schema; to **T14** — the decision-1/decision-2 header schemas, the
conditional-`decided` rule, the unknown-field prohibitions, and the `derives_from`
presence/deduplication/resolvability checks join the S6 CI frontmatter requirement (T08 d11),
which **automates** these contracts and does not create them. Classification: **compatible**
(T04 d1 instantiated). Rejected: hand-authored placeholder outputs (exactly what
`do_not_edit` exists to prevent); dropping `docs/generated/` (contradicts T04 d1).

### Decision 8 — Durable record and publication sequence (hash-bound review-then-publish)

This record at
`docs/wayfinding/map-1/23-normative-document-header-and-slice-a-documentation-set.md`
with a `docs/wayfinding/README.md` index line. Publication executes only after Eric reviews
the exact drafted bytes — the record, the whole `docs/wayfinding/README.md` successor, the
tracker-payload bundle (resolution comment, close comment, map line, the T14 and T20
handoffs, and the substitution instructions), and the continuity template, each bound by
SHA-256 in the review package — and gives consolidated approval; the fail-closed sequence
below then runs unchanged. Handoffs go **only to the open tickets T14 #19 and T20 #22** —
none to the closed T19 #14, T21 #20, or T22 #21 — and add no dependency edges. Closing #23
changes **no blocker count** (it blocks nothing); the frontier becomes **T20 #22, then
T14 #19**; nothing else is claimed. Rejected: publish-on-selection without byte review;
in-comment resolution without a durable record.

## Glossary candidates (S5 `domain-modeling`)

**Authority class** — the one-field answer to what binds a domain document: `normative`,
`informative`, or `generated`. **Derives-from citation** — the mandatory non-empty,
deduplicated, resolvable list of normative sources an informative document derives from.
**Documentation set** — the accepted list of slice-A domain documents with their authority
classes and owning tickets. **Navigation exemption** — the root README and glossary carry no
authority header, hold no independent authority, and summarize or navigate only by citation,
with accepted decisions prevailing on any conflict.

## Downstream handoffs (proposals; posted after publication — open tickets only)

- **T14 #19:** the decision-1 normative header schema (closed sets; `decided` absent while
  proposed and required atomically at acceptance; unknown fields prohibited by the contract
  now, automated by the S6 CI check later); the decision-2 informative schema (`derives_from`
  non-empty, deduplicated, resolvable to a repository normative-document path, a domain ADR
  identifier/path, or an immutable pinned platform identifier/URL); the decision-4
  applicability boundary as an enumerable check surface; `docs/generated/**` excluded from
  these header schemas because T20's generated-metadata schema governs there.
- **T20 #22:** `authority: generated` is T23's authority-class value joining T20's full
  generated-metadata schema — `do_not_edit`, named sources, provenance, and the rest remain
  T20-owned; `pr-scenarios.md` cites T20's PR-class definitions (including the
  verification-update scenario subject); generated effective-access examples arrive only with
  the S6 tooling, never at S5.

## Dependency effects and frontier

#23 has native edges blocked-by 0 (its one blocker, T08 #13, is closed) and **blocking 0**.
Closing #23 changes **no blocker count**: T20 #22 remains at zero open blockers (already
unblocked) and T14 #19 remains at one (#22). Closing #23 satisfies its "required before S5
consolidation" condition. Live frontier after closure, in map order: **T20 #22 (next
claimable)** · T14 #19 (claimable only after #22 closes). One HITL ticket per session —
nothing is claimed at publication.

## Publication sequence (fail-closed; record before close)

Executed only under Eric's consolidated publication approval of the exact reviewed bytes. A
failure at any step through 8 leaves #23 open, with all later normal publication steps
unperformed; completed remote writes are not automatically undone. The exact partial state is
preserved through a Repository Continuity Artifact where necessary and reported.

1. Create this record at
   `docs/wayfinding/map-1/23-normative-document-header-and-slice-a-documentation-set.md`
   and the `docs/wayfinding/README.md` index line in the working tree, byte-identical to the
   approved package (SHA-256 verified).
2. Validate them on the final bytes: frontmatter parses, internal links resolve, the
   mechanical checks pass; no live identifier, no acceptance claim.
3. Commit both on `main`; push (authorized as part of the consolidated approval).
4. Verify the immutable record URL at the pushed commit resolves and is byte-equivalent to
   the local file.
5. Post the exact #23 resolution comment from the hash-bound tracker-payload bundle, with
   the record commit SHA filled in.
6. Post the exact informational handoff comments from the same bundle to T14 #19 and
   T20 #22 only; no dependency edges; no comment to any closed ticket.
7. Update map #1: append exactly the one T23 Decisions-so-far line from the bundle. No fog
   edit and no map-order change (T23 graduates nothing and creates no ticket).
8. Round-trip verify: the #23 resolution comment, both handoff comments, and the complete
   map #1 diff (exactly the one addition).
9. If any step through 8 fails: leave #23 open, perform no later normal publication step,
   preserve the exact partial state through continuity if necessary, and report it.
10. Close #23 as completed, retaining assignee `a24577t`, with the exact close comment from
    the bundle.
11. Round-trip verify the close; verify that closing #23 changed no blocker count — T20 #22
    still shows zero open blockers and T14 #19 one (#22).
12. Recompute all dependency effects and the live frontier (expected state above) without
    claiming anything.
13. Replace the Repository Continuity Artifact (position after T23; frontier at T20 #22; the
    carried items unchanged), substituting the actual record commit SHA. The template hash
    binds the pre-substitution bytes; the committed bytes differ only by deterministic
    replacement of `<RECORD-COMMIT-SHA>` with the 40-hex record commit SHA. Commit and push.
14. Verify `HEAD == origin/main`, a clean working tree, and the final tracker invariants
    (#23 closed with assignee retained; map body as verified; no other issue state changed).

Post-close failure rule: if a failure occurs after step 10, do not reopen #23 and do not
duplicate earlier writes; record the precise partial state in continuity where possible,
report it, and stop.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Verdict⟧ and ⟦G-Accept⟧; nothing in it authorizes authoring any document of
the set, any AWS or GitHub mutation, any S3 or evidence creation, or any implementation.
