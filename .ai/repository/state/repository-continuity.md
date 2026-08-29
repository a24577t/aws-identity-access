# Repository Continuity Artifact — narrow ⟦G-Accept⟧: declaration-vocabulary amendment

**Type:** transient continuity artifact (lifecycle model, continuity mechanism 2).
Present only while the narrow ⟦G-Accept⟧ acceptance transaction for the
declaration-vocabulary amendment is in flight. Carries only uncommitted in-flight
intent and pointers; committed repository state prevails on any conflict
(MADR-0001 D3). Consumed once by the next session bootstrap; deleted on the
acceptance branch before merge.

## Transaction

One narrow ⟦G-Accept⟧ accepting, as a single net diff against stable base
`0f03e3d274986041d41f60e712a0fb16a62ec7f2`:

1. `docs/specifications/slice-a-declaration-vocabulary-amendment.md` (new) — the
   E1 declaration-vocabulary correction record from R1 #26's S8 validate halt.
2. `.ai/repository/methodology/skill-execution-map.md` (replaced) — one added
   sentence in Excursion E1: Pre-Baseline E1 decisions ratify at a narrow
   ⟦G-Accept⟧ with no Architecture Version advance; ⟦G-Refine⟧ with version
   advance applies from the first baseline onward (owner decision Q-AV2, 2026-08-29).
3. `.ai/repository/state/STATUS.md` (replaced) — accepted-set and objective
   reconciliation; Architecture Baseline / Baseline Version / Architecture Version
   remain `none`.

Authoritative payload bytes: `.ai/repository/state/transition-payloads/
g-accept-declaration-vocabulary/` at the transition-start commit — record under
`record/`, map successor under `methodology/`, STATUS successor under `status/`,
with `MANIFEST.sha256` binding every payload byte. The payload, not this artifact,
is the transport of truth.

## Position and resume rule (repository-only, P4)

Resume from the repository alone; do not rely on any conversation. Determine the
current step by inspection and continue at the first incomplete step of the
publication plan (`publication-plan.md` in the payload):

- **Transition-start commit present on `main`** (this artifact + payload) but no
  `acceptance/declaration-vocabulary` branch → create the acceptance branch from
  the transition-start commit and continue at plan step P2.
- **Acceptance branch exists, no PR** → verify its tree against the payload
  manifest; continue at plan step P3 (PR creation).
- **PR open, unmerged** → the owner gate is pending. Only Eric merges (P4 stop).
- **PR merged** → run plan step P5 closeout verification; this artifact and the
  payload must be absent from `main`; if closeout verification has not been
  recorded, perform and record it.
- **Any verification failure** → stop, surface the discrepancy, apply the plan's
  failure/abort rules; never force-push, never rewrite `main` history.

## In-flight work item

R1 #26 (assigned `a24577t`) remains In Implementation, halted at S8 pending this
acceptance; branch `ticket/r1-foundation-and-contracts` @
`b23d2b9c363e72316d2dc5602cc2cdc8a3623c74` is untouched by this transaction. After
merge: S7 D1–D3 correction pass → narrow S8 revalidation → S9 (amendment §5). The
ticket, its branch, and all schemas are outside this transaction's diff.

## Authorization boundary

Prepared under Eric's decision approvals (Q1–Q3, 2026-08-28; Q-AV1–Q-AV3,
2026-08-29). Publication executes only under Eric's hash-bound narrow ⟦G-Accept⟧
authorization; the merge is Eric's owner-only act. No AWS contact, Terraform,
GitHub configuration, or tracker write occurs in this transaction.
