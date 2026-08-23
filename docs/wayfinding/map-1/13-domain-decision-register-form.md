---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 13
title: "T08 — Domain decision-register form vs aws_ami RD-09 and this repository's ADR methodology"
url: https://github.com/a24577t/aws-identity-access/issues/13
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-23
sources:
  decision_batch: "consolidated 15-question HITL batch (2026-08-23); Eric selected all 15 recommendations with three owner corrections, applied throughout"
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
---

# T08 — Domain decision-register form vs aws_ami RD-09 and this repository's ADR methodology

> Proposed discovery record — the complete durable result of T08 #13. Decisions approved by Eric
> as the human project owner and decision authority; the session was executed by Claude in the
> repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`. **Nothing here is
> accepted architecture: every decision is a proposal until ⟦G-Verdict⟧ and ⟦G-Accept⟧.** GitHub
> issue #13 is the workflow/index surface and links to this record.

Governing documents cited at the `aws_ami` revision pinned by `T01` (#2),
`5f3cb7163f468730fd2ceb5d565c90b0bfda6099`: `docs/architecture/11-decision-register.md` (RD-09;
register preamble — stable IDs, never reused), `docs/architecture/README.md` (lines 44–47,
document status values; staging-workspace notice; `status` / `destination` / `decided`
frontmatter convention). Repository authority: MADR-0001, MADR-0002, MADR-0004, P1, P5, the
lifecycle model, the Skill Execution Map (S5, ⟦G-Accept⟧, ⟦G-Refine⟧, E1), `to-spec-repo-owner`.
Intake proposal (not authority — map #1 Notes): the brief's authority hierarchy and documentation
metadata (lines 133–140) and its "a domain decision register" deliverable (line 430). Prior map
decisions carrying content "in the T08 form": T02 #3 (one reconciliation owner), T04 #6
(decisions 1, 6 — slice boundary; register form and placement deferred here), T07 #9 (decision 1
— no standing administrator), T15 #10 (decision 7 — POC-managed resource set). T09 #12 decision
24 handed off no content (T08 decides the register form, not content).

## Decisions

Each decision was selected by Eric from the recommended option of the consolidated batch;
corrections 1 (status vocabulary and supersession), 2 (decision-owner attribution), and
3 (backfill rationale and authorization boundary) are applied throughout.

### Decision 1 — Form: ADR-primary

The domain decision register is the set of per-decision, append-only domain ADR records together
with a subordinate index (decision 11). This mirrors the repository methodology's own register
pattern (`.ai/repository/methodology/adr/` + README index). Alternatives not taken: a single
register document in the aws_ami form (its in-place entry mutation for accepted content is
incompatible with MADR-0002 D3, and it collides with the S5 skill chain's "ADR texts"); a hybrid
register-plus-ADR split (two authoritative surfaces per decision — the duplication RD-09's own
rationale warns against, made internal).

### Decision 2 — Location: `docs/adr/NNNN-slug.md`

Sequential numbering per the house ADR format (scan highest, increment). This ratifies the
provisional layout already assumed by `CLAUDE.md`, `docs/agents/domain.md`, and
`to-spec-repo-owner` (precondition 4). Domain *architecture documents* (a separate brief
deliverable) live in `docs/architecture/` and cite ADR IDs; they are not decision records.
Alternatives not taken: `docs/architecture/decisions/` (mixes owned decisions with the future
migrated platform document 07, whose `destination` is this repository); a new `docs/decisions/`
root (no benefit over the ratified layout).

### Decision 3 — Scope: owned decisions only, exclusions explicit

The register holds only decisions this repository owns (domain model, layout, conventions, slice
boundaries, lab/POC domain refinements). `docs/adr/README.md` names the exclusions: platform
architecture (cited as `I-n` / `RD-nn` / `OD-nn` / document at the pin, never restated);
methodology decisions (MADRs); the glossary (root `CONTEXT.md`); process state (tracker, STATUS);
wayfinding records (proposed discovery, never accepted architecture); specifications
(`docs/specifications/`); operational and lab records in the homes prior decisions gave them
(T09/T15 binding and evidence artifacts — referenced, never duplicated). Under the adopted scope
interpretation, and provided upstream platform decisions are cited rather than restated, this
register creates no parallel platform-architecture authority. RD-09's domain-repository scope
remains unstated at the pinned revision; that ambiguity is carried by decision 14's upstream
clarification proposal.

### Decision 4 — Record format: house ADR format plus required frontmatter

Title + one-to-three-sentence decision; optional Considered options / Consequences sections when
they add value; required frontmatter per decision 5. Rigor scales per record via the optional
sections. Alternatives not taken: MADR-style mandatory sections (excess weight for one-sentence
domain rules; any individual record may still adopt them); the aws_ami entry style (the form not
taken in decision 1).

### Decision 5 — Metadata schema (register-record frontmatter)

```yaml
status: proposed          # closed set: proposed | accepted (decision 6)
authority: normative
scope: <what the decision binds>
decision_owner: "Eric — human project owner and decision authority"
decided: <YYYY-MM-DD>     # set when status becomes accepted, in the same gate merge; absent while proposed
supersedes: ADR-NNNN      # only on a superseding record (decision 9); otherwise absent
```

Recorded mapping to the aws_ami three-field convention at the pin: aws_ami `status`
(document kind) ≈ `authority` here; aws_ami `decided` ≈ `decided` here; aws_ami `destination` —
not applicable in this repository (nothing migrates out); recorded as N/A. The brief's four
concerns (normative/informative, authority, scope, decision owner) are all covered. This schema
is the worked precedent for the graduated documentation-metadata ticket (decision 15).

### Decision 6 — Lifecycle vocabulary (correction 1)

The committed domain-ADR `status` vocabulary is the closed set: proposed | accepted. A proposed
ADR becomes accepted only through ⟦G-Accept⟧ or ⟦G-Refine⟧, flipped in the gate's acceptance
merge with STATUS reconciled atomically. A proposal rejected or withheld at a gate does not
land on `main` as a register record; its disposition remains in the gate/tracker record. Open
questions are tracker artifacts (map, tickets), never register entries. There is no other status
value; supersession is expressed only per decision 9, never as a status.

### Decision 7 — Ownership and attribution (correction 2)

Every register record carries exactly
`decision_owner: "Eric — human project owner and decision authority"`. Acceptance authority is
Eric's, exercised only at Repository Gates. Assistants prepare texts; an assistant never appears
as decision owner and receives no attribution in accepted authoritative artifacts (P1). The field
is extensible to team owners in the target estate by a later decision.

### Decision 8 — Links to upstream architecture decisions

Upstream decisions are cited by stable identifier at the pinned revision using the immutable URL
form recorded by T01 — never restated. Requirement: an informative upstream-proposals index at
`docs/architecture/upstream-proposals.md` (`authority: informative`; proposal tracking, not a
decision artifact), listing every amendment/refinement proposal carried by Eric with its source
record — produced no later than the S5 acceptance branch. Carried set at this record's date:
document 09 and document 05 (T02 #3), document 02 (T05 #7), document 07 (T04 #6), documents
01/11 (T07 #9), OD-21 (T09 #12), and the RD-09 clarification (decision 14, this record).

### Decision 9 — Supersession (correction 1)

An accepted ADR is never edited: the superseded record remains byte-unchanged with
`status: accepted`. A superseding ADR carries `supersedes: ADR-NNNN`. No forward pointer of any
kind is ever added to the superseded record. The subordinate index may show the derived
supersession relationship, but it is never authoritative over either ADR. Grounded in MADR-0002
D3 and P5: an accepted record cannot point forward; navigation is carried by later artifacts —
the subordinate index immediately, the next baseline authoritatively.

### Decision 10 — Generated ADR-shaped views

Permitted only as generated artifacts in the visibly non-authoritative generated subdirectory
(T04 decision 1), carrying `do_not_edit: true` and named source inputs (T20's generated-document
metadata), regenerated and never hand-edited. ADR-shaped renderings of platform register content,
if ever produced, are generated from the aws_ami register (RD-09, sentence 4). None are produced
in slice A; the constraint is recorded for the future.

### Decision 11 — Index, validation, traceability

`docs/adr/README.md` holds one line per record (ID, title, status, link; derived supersession
relationships may be shown) — a subordinate summary that never overrides a record. Every record
cites its provenance: the source wayfinding record at its commit plus the ticket URL. Non-obvious
validator and schema rules cite register IDs (brief). Frontmatter/ID/index-consistency checking
in CI is recorded as an S6 tooling requirement; it is not built now.

### Decision 12 — Graduation through ⟦G-Verdict⟧ and ⟦G-Accept⟧

The register is populated at S5 and accepted at ⟦G-Accept⟧. Until S5, proposed decisions live
solely in wayfinding records and tickets. At S5, `to-spec-repo-owner` + `domain-modeling` draft
the founding records (`status: proposed`) on the acceptance branch from the grill-approved
results; the ⟦G-Accept⟧ merge lands them accepted with STATUS reconciled atomically. Founding
entries include at minimum the carried decisions: one reconciliation owner (T02 #3), the `access/`
requester surface (T04 decisions 1–2), the T03/T04 slice boundary (T04 decision 6), no standing
administrator (T07 decision 1), the POC-managed resource set (T15 decision 7). Post-baseline
refinements enter through E1 and ⟦G-Refine⟧.

### Decision 13 — Result-record backfill sequencing (correction 3)

Sequencing rule: before S5 consolidation, separately authorize and complete the result-record
backfill for T01–T06 and T11–T13, so S5 has complete repository-owned provenance and
traceability inputs (full durable reasoning preserved; T11–T13 as thin scope-closure records).
Once accepted, a register ADR is authoritative in itself; backfill preserves durable reasoning
and traceability — it does not confer authority on any future ADR. This decision records the
prerequisite only: no backfill file is created until Eric separately authorizes that activity.

### Decision 14 — RD-09 upstream clarification (carried by Eric; aws_ami never edited here)

Proposed clarification, associated with the RD-09 entry in
`docs/architecture/11-decision-register.md`: "RD-09's sole-authority scope covers platform
architecture decisions; a domain repository may maintain a decision register for decisions it
owns, which references and never restates entries of this register." The local decisions above
proceed regardless of when or whether it lands.

### Decision 15 — Fog graduation

The "Documentation metadata and set" patch graduates into a new `grilling` ticket, T23
(specification in this record's Fog graduation section), created before #13 closes as a
sub-issue of map #1 with a native blocked-by dependency on #13 — its successful creation and
wiring are preconditions of T08 closeout, and the close of #13 releases it. The patch is removed
from the map's Not yet specified in the same map edit. Decision 5's schema is its precedent
input. The "Schema versioning and test-environment pinning" patch remains in the fog
(trigger: T14).

## Claim-resolution record (grill-with-docs)

Per claim: governing document + identifier · claim · result · upstream amendment/refinement.

**Claim 1 — RD-09 binds domain repositories, not only aws_ami.**
- Authority: RD-09 at the pin (sentence 2, "sole architecture-decision authority"; sentence 4,
  ADR-shaped files "migrated or generated from this register, never maintained alongside it");
  `11-decision-register.md` frontmatter `destination: all`; README lines 44–47; T01 research
  §5.2 (scope survey).
- Result: **inherited** for platform architecture decisions — the register binds this repository,
  and no parallel artifact for its content is created (decisions 3, 8). **Absent** for a domain
  repository's own decisions — no sentence at the pin extends sole authority to them; resolved
  locally by decisions 1 and 3.
- Upstream: RD-09 clarification proposal (decision 14), carried by Eric.

**Claim 2 — this repository's S5 `domain-modeling` ADR texts under `docs/adr/` are compatible
with RD-09.**
- Authority: RD-09; `docs/agents/domain.md`; `to-spec-repo-owner` precondition 4; `CLAUDE.md`
  provisional-layout note.
- Result: **compatible**, conditioned on decision 3's exclusions — records hold only decisions
  owned here and cite, never restate, register entries. Without that scope the layout would be
  **conflicting**; the condition is part of the proposed decision set.
- Upstream: none beyond decision 14.

**Claim 3 — the brief's "domain decision register" and four-field metadata scheme are compatible
with aws_ami's `status` / `destination` / `decided`.**
- Authority: brief lines 133–140 and 430 (a proposal, not a decision — map #1 Notes); aws_ami
  README frontmatter convention at the pin.
- Result: register deliverable **compatible** — treated locally as compatible under decision 3's
  scope and citation rules (upstream platform decisions cited, never restated), while RD-09's
  domain-repository scope remains unstated at the pinned revision and that ambiguity is
  explicitly carried by decision 14's upstream clarification proposal. Four-field scheme
  **absent** upstream; adopted as the domain scheme with the decision 5 mapping (`destination`
  recorded N/A). The document-set-wide header is graduated to the decision 15 ticket.
- Upstream: none.

**House-conflict note.** Importing the aws_ami register *form* (in-place entry mutation) for
accepted domain content would conflict with MADR-0002 D3 and P5. RD-09 does not require that
form, and it is not adopted (decisions 1, 6, 9). After decision 3's scope separation, no conflict
remains between RD-09 and this repository's methodology; no methodology amendment is required.

## Upstream proposals carried by the owner (aws_ami not edited)

- **RD-09 clarification (decision 14):** "RD-09's sole-authority scope covers platform
  architecture decisions; a domain repository may maintain a decision register for decisions it
  owns, which references and never restates entries of this register."

## Proposed handoffs (proposals; nothing accepted)

- **S5 (`to-spec-repo-owner` + `domain-modeling`):** draft the founding register records per
  decision 12 in decision 4/5 form under `docs/adr/`, with the `docs/adr/README.md` index and
  scope exclusions (decisions 3, 11); produce `docs/architecture/upstream-proposals.md`
  (decision 8). Glossary candidate for root `CONTEXT.md` at S5: **Domain decision register** —
  the set of accepted domain ADRs under `docs/adr/` together with their subordinate index; the
  authoritative record of decisions this repository owns.
- **Backfill prerequisite (decision 13):** separately authorized activity, to complete before S5
  consolidation; recorded here and pointable from continuity; not begun by T08.
- **New documentation-metadata ticket T23 (decision 15):** created at publication, before #13
  closes, blocked by #13; specification below.
- **T20 #22 (informational handoff comment, no dependency edge):** decision 10 places any
  generated ADR-shaped view under T20's generated-document metadata regime; the exact comment is
  posted at publication step 7.
- **T14 #19 (informational handoff comment, no dependency edge):** decision 11's
  stable-decision-ID citation rule applies to the validation contract's rule documentation, and
  the S6 frontmatter/numbering/index CI requirement is recorded; the exact comment is posted at
  publication step 7.

## Fog graduation — proposed ticket (created at publication; number assigned then)

- **Title:** `T23 — Normative-document header and slice-A documentation set`
- **Label:** `wayfinder:grilling` · **Sub-issue of:** map #1
- **Native dependency edges:** blocked by T08 #13 — added at creation, before #13 closes, so
  T23's successful creation and wiring are preconditions of T08 closeout; the close of #13
  releases T23 (zero open blockers). T23 blocks nothing and must close before S5 consolidation.
- **Map order placement:** after T22 #21, before T20 #22.
- **Body:**

```markdown
- **Type:** `grilling` (HITL)
- **Blocked by:** T08 #13 · **Blocks:** none
- **Required before S5 consolidation.**
- **Document-governed:** yes — at the pinned aws_ami revision
  `5f3cb7163f468730fd2ceb5d565c90b0bfda6099` (T01): `docs/architecture/README.md` document
  status values (`normative` / `register` / `checklist`) and the `status` / `destination` /
  `decided` frontmatter convention; the brief's lines 133–140 header proposal
  (normative/informative + authority, scope, decision owner); the T08 #13 record's decision 5
  (register-record header precedent). Coordination, not blocking: T20 #22 owns
  generated-document metadata (`do_not_edit`, named sources); T19 #14 owns the
  migration/rejected-conventions note content.

## Question

What header must every normative and informative domain document in this repository carry, how
does it map onto aws_ami's three-field frontmatter at the pinned revision, and what is the
slice-A documentation set (root README, domain architecture documents, configuration-contract
document, requester and reviewer guides, walkthroughs, counterexamples, PR scenarios, generated
effective-access examples, migration note) with each artifact's authority class? Claims to
test: (1) the T08 decision 5 register header extends to the whole normative document set;
(2) guides and walkthroughs are `informative` and must cite the normative sources they derive
from (brief) — absent upstream, compatibility to establish; (3) the documentation-set
composition against the slice-A scope (T03/T04) and each piece's owning ticket (T19 migration
note; T20 generated metadata).

## Resolution record

Per claim: governing document + identifier · claim · result · upstream amendment/refinement.
```

## Dependency effects and frontier

T08 #13 enters closeout with blocked-by 0 (T01 #2 closed). During the publication sequence, T23
is created with a native blocked-by edge on #13, making #13's blocking count 1. Closing #13
releases exactly T23 (its open blockers go 1 → 0); it changes no other blocker counts — T20 #22
remains blocked (three open blockers: #15, #20, #21) and T14 #19 remains blocked (four: #15,
#20, #21, #22). Live frontier after closure, in map order: T19 #14 (next claimable — T23 occurs
later in map order) · T10 #15 · T21 #20 · T22 #21 · T23. T23, like T08, must close before S5
consolidation and blocks nothing.

## Publication sequence (fail-closed; record before close)

Executed only under Eric's consolidated publication approval. A failure at any step through 9
leaves #13 open, with all later normal publication steps unperformed; completed remote writes
are not automatically undone. The exact partial state is preserved through a Repository
Continuity Artifact where necessary and reported.

1. Create the T08 record at `docs/wayfinding/map-1/13-domain-decision-register-form.md` and the
   `docs/wayfinding/README.md` index line in the working tree.
2. Validate them: frontmatter parses, internal links resolve, and the mechanical correction
   checks pass on the final bytes.
3. Commit both on `main`; push (authorized as part of the consolidated approval).
4. Verify the immutable record URL at the pushed commit resolves and its content is
   byte-equivalent to the local file.
5. Post the exact #13 resolution comment, with the record commit SHA filled in.
6. Create T23: exact title, body, and `wayfinder:grilling` label; attach it as a sub-issue of
   map #1; add the native blocked-by dependency on #13; verify its complete body, label,
   sub-issue linkage, and dependency.
7. Post the exact informational handoff comments to T20 #22 and T14 #19; no dependency edges.
8. Update map #1: append exactly one T08 Decisions-so-far line; remove only the graduated
   "Documentation metadata and set" fog bullet; retain the "Schema versioning and
   test-environment pinning" fog bullet; insert T23 after T22 #21 and before T20 #22 in the
   map-order line.
9. Round-trip verify: the #13 resolution comment, T23 title/body/label/sub-issue/dependency,
   both handoff comments, and the complete map #1 diff (exactly the three edits).
10. If any step through 9 fails: leave #13 open, perform no later normal publication step,
    preserve the exact partial state through continuity if necessary, and report it.
11. Close #13 as completed, retaining assignee `a24577t`, with the close comment.
12. Round-trip verify the close; verify T23's #13 blocker is now closed and T23 has zero open
    blockers (released).
13. Recompute all dependency effects and the live frontier (expected state above) without
    claiming anything.
14. Replace the Repository Continuity Artifact (position after T08; T23 created and released;
    backfill prerequisite pointer; frontier); commit and push.
15. Verify `HEAD == origin/main`, a clean working tree, and the final tracker invariants
    (#13 closed with assignee retained; T23 open, unassigned, zero open blockers; map body as
    verified).

Post-close failure rule: if a failure occurs after step 11, do not reopen #13 and do not
duplicate earlier writes; record the precise partial state in continuity where possible, report
it, and stop.
