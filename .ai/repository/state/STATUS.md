# STATUS — aws-identity-access

**Type:** Status Artifact. Concise last-stable-state view of the repository (see the
[lifecycle model](../methodology/lifecycle-model.md), *Status Artifact: last-stable-state
semantics*). Subordinate to accepted decisions
([MADR-0001](../methodology/adr/0001-repository-authoritative-continuity.md)); reconciled
only through Repository Gates. Not an architecture document.

## Repository

- **Repository Version:** `none — untagged`
- **Completed Phase:** none
- **Current Phase:** Pre-Baseline

## Architecture

- **Architecture Baseline:** none (first baseline publishes at the phase gate,
  operator-guide S4/S5)
- **Baseline Version:** none
- **Architecture Version:** none
- **Accepted decision set:** the slice-A architecture accepted at ⟦G-Accept⟧ — the domain
  decision register ([`docs/adr/`](../../../docs/adr/README.md), ADR-0001…0009) and the
  two normative architecture documents (each `status: accepted` per its T23 header),
  together with the gate-approved slice-A engineering specification and brownfield
  implementation plan, whose authority derives from the approved ⟦G-Accept⟧ record and
  their repository placement (they carry no T23 header). Three later records, each
  accepted at a narrow ⟦G-Accept⟧: the
  [execution-grouping amendment](../../../docs/specifications/slice-a-execution-grouping-amendment.md)
  supersedes only §10's ticket-consumption mapping (the specification remains
  byte-unchanged), and the
  [repository byte-identity amendment](../../../docs/specifications/repository-byte-identity-amendment.md)
  fixes hash authority on canonical Git-blob bytes and governs the root
  `.gitattributes` (LF text; exact-byte JSON), and the
  [declaration-vocabulary amendment](../../../docs/specifications/slice-a-declaration-vocabulary-amendment.md)
  — ratified through the Pre-Baseline E1 route (Skill Execution Map, Excursion
  E1) — fixes the executable field table of the change-declaration records
  (executable renderings of T06 #8 decision 5; plan-effect classes per T20 #22
  decision 5), the cited records prevailing on any divergence. The Architecture
  Baseline, Baseline Version, and Architecture Version remain `none`.

## Objective

- **S6 complete:** the eight grouped implementation tickets of the
  [execution-grouping amendment](../../../docs/specifications/slice-a-execution-grouping-amendment.md)
  are published with the amendment §4 seven-edge native dependency set:
  R1 #26, R2 #27, R3 #28, R4 #29, R5 #30, R6 #31,
  R7 #32, R8 #33.
- **R1 complete:** R1 #26 (Foundation and contracts — §10 rows 1, 2, 8) passed the
  full verify chain (S8 PASS; S9 evidence on the ticket; S10 three-axis PASS; S11
  PASS WITH CONDITIONS) and merged at ⟦G-Merge⟧ via PR #35, merge commit
  `dfe76edde39c8ee0af87a7fa286c3d5e25bf048d`; #26 is closed as completed. The two
  non-blocking S11 conditions travel with R2 #27: C1 (correct both
  `permission-set-key-replacement` schema descriptions' "impossible by schema"
  overclaim, preserving authored/wired byte identity) and C2 (update
  `tests/README.md`'s test enumeration when `tests/` is next edited).
- **R2 complete:** R2 #27 (Validation and catalog system — §10 rows 3–7) passed
  the full verify chain (S8 PASS; S9 evidence and correction addendum on the
  ticket; S10 three-axis PASS; S11 PASS WITH CONDITIONS) and merged at
  ⟦G-Merge⟧ via PR #37, merge commit
  `441c0d103b477309358750ccf0a90a52be2f614c`; #27 is closed as completed.
  Its two non-blocking S11 conditions travel with R3 #28: C1 (remove or
  disposition the four identified vestigial constructs during R3's authorized
  `src/validator` work) and C2 (document the ADM rule-2/4 condition-gating
  boundary; any behavior change routes through E1). The recorded allocation
  note for `ADO-PHASE` and the CLS/GEN fixtures also travels with R3.
- **Current Objective:** run Skill Step S7 (`implement`) against the next frontier
  ticket R3 (#28, Plan analysis and generated governance — §10 rows 9, 10, 12) with fresh context,
  through the decision-gated lifecycle S7–S11 (Standards + Spec + Conformance axes and
  the independent Quality Gate) to ⟦G-Merge⟧. R5 #30 is also unblocked; R3 #28 is
  next in the amendment/map order and neither ticket is claimed.
- **Next Milestone:** R3 verified and merged at ⟦G-Merge⟧; the frontier then advances
  per the amendment's native edges (R4 unblocks). R6, R7, and R8 remain
  separately authorized beyond ticket creation; no Terraform apply before the R6/14a
  control set is active. The three empirical conditions (provider execution; `forget`
  representation; import redaction) remain open and gate what their records say they
  gate.

## Repository Version sentinel

`none — untagged` is the Repository Version recorded while the repository has never
produced a Project Release. It corresponds to the **absence of any Git tag**: session
bootstrap's Repository-Version check (Status Artifact version = latest Git tag)
reconciles because both sides are "none". The sentinel is replaced by the first released
Semantic Version when Project Release (operator-guide S7/S8) reconciles this artifact
together with the tag and release metadata.
