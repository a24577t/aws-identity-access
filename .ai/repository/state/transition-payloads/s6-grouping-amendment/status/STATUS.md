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
  their repository placement (they carry no T23 header). The
  [execution-grouping amendment](../../../docs/specifications/slice-a-execution-grouping-amendment.md),
  accepted at a narrow ⟦G-Accept⟧, supersedes only §10's ticket-consumption mapping;
  the specification remains byte-unchanged.

## Objective

- **Current Objective:** run Skill Step S6 (`to-tickets`) against the accepted
  [slice-A engineering specification](../../../docs/specifications/slice-a-engineering-specification.md)
  §10 breakdown as consumed through the accepted
  [execution-grouping amendment](../../../docs/specifications/slice-a-execution-grouping-amendment.md)
  (eight grouped tickets R1–R8, one per amendment row; native edges per its §4
  seven-edge transitive reduction; §10 rows carried as traced sub-items).
- **Next Milestone:** the eight grouped implementation tickets published with edges;
  S7–S11 implement and verify the first frontier ticket (R1) under the decision-gated
  lifecycle. The three empirical conditions (provider execution; `forget`
  representation; import redaction) remain open and gate what their records say they
  gate.

## Repository Version sentinel

`none — untagged` is the Repository Version recorded while the repository has never
produced a Project Release. It corresponds to the **absence of any Git tag**: session
bootstrap's Repository-Version check (Status Artifact version = latest Git tag)
reconciles because both sides are "none". The sentinel is replaced by the first released
Semantic Version when Project Release (operator-guide S7/S8) reconciles this artifact
together with the tag and release metadata.
