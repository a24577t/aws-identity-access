## Narrow ⟦G-Accept⟧ — declaration-vocabulary amendment and Pre-Baseline E1 routing correction

One acceptance transaction from the R1 #26 S8 `codebase-design` validate halt
(halt-don't-decide excursion E1). Decision direction approved by Eric: Q1-A/Q2-A/Q3-A
(2026-08-28) and Q-AV1-A/Q-AV2-A/Q-AV3-A (2026-08-29). Publication executes under
Eric's hash-bound narrow ⟦G-Accept⟧ authorization; **merge is Eric's owner-only gate
act** — the executor never merges.

### Net authoritative diff vs stable base `0f03e3d274986041d41f60e712a0fb16a62ec7f2`

1. **New:** `docs/specifications/slice-a-declaration-vocabulary-amendment.md` — the
   append-only correction record ratifying the executable field table of the
   change-declaration records (executable renderings of T06 #8 decision 5;
   plan-effect classes per T20 #22 decision 5; the cited records prevail on any
   divergence). No Architecture Version is created or advanced.
2. **Replaced:** `.ai/repository/methodology/skill-execution-map.md` — exactly one
   added sentence in Excursion E1: before the first Architecture Baseline, an E1
   decision is ratified through a narrow ⟦G-Accept⟧ and no Architecture Version
   advances; from the first baseline onward, E1 uses ⟦G-Refine⟧ and advances the
   Architecture Version.
3. **Replaced:** `.ai/repository/state/STATUS.md` — accepted-set lists the amendment
   as the third narrowly accepted correction record; objective records the resume
   route (S7 D1–D3 correction pass → narrow S8 revalidation → S9); Architecture
   Baseline, Baseline Version, and Architecture Version remain `none`.

The branch also deletes the two transient transaction paths committed at transition
start (`.ai/repository/state/repository-continuity.md`,
`.ai/repository/state/transition-payloads/g-accept-declaration-vocabulary/`), so the
post-merge net diff is exactly the three artifacts above.

### Out of scope

No schema edit, no change to #26 or its branch, no S7/S8/S9 execution, no AWS
contact, no Terraform, no GitHub configuration, no advancement of the three
empirical conditions.

### Verification (executor, recorded before requesting merge)

- Acceptance-branch blobs byte-identical to the transition payload
  (`MANIFEST.sha256`); payload blobs equal the owner-authorized hashes.
- Net diff vs `0f03e3d` contains exactly the three paths above plus the two
  transient-path deletions relative to the transition-start commit.
- No live AWS identifier anywhere in the diff; all text canonical LF under the
  repository byte-identity amendment.
