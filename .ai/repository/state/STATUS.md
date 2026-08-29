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
  their repository placement (they carry no T23 header). Two later records, each
  accepted at a narrow ⟦G-Accept⟧: the
  [execution-grouping amendment](../../../docs/specifications/slice-a-execution-grouping-amendment.md)
  supersedes only §10's ticket-consumption mapping (the specification remains
  byte-unchanged), and the
  [repository byte-identity amendment](../../../docs/specifications/repository-byte-identity-amendment.md)
  fixes hash authority on canonical Git-blob bytes and governs the root
  `.gitattributes` (LF text; exact-byte JSON).

## Objective

- **S6 complete:** the eight grouped implementation tickets of the
  [execution-grouping amendment](../../../docs/specifications/slice-a-execution-grouping-amendment.md)
  are published with the amendment §4 seven-edge native dependency set:
  R1 #26, R2 #27, R3 #28, R4 #29, R5 #30, R6 #31,
  R7 #32, R8 #33.
- **Current Objective:** run Skill Step S7 (`implement`) against the first frontier
  ticket R1 (#26, Foundation and contracts — §10 rows 1, 2, 8) with fresh context,
  through the decision-gated lifecycle S7–S11 (Standards + Spec + Conformance axes and
  the independent Quality Gate) to ⟦G-Merge⟧.
- **Next Milestone:** R1 verified and merged at ⟦G-Merge⟧; the frontier then advances
  per the amendment's native edges (R2 and R5 unblock). R6, R7, and R8 remain
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
