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
  decision 5), the cited records prevailing on any divergence; and the
  [root-control-path classification amendment](../../../docs/specifications/slice-a-root-control-path-classification-amendment.md)
  — ratified through the same Pre-Baseline E1 route — closes the single
  T20 #22 decision-2 omission for the four T06-governed root control files
  (`.gitignore`, `.gitattributes`, `LICENSE`,
  `aws-identity-access-poc-prompt.md` → `platform-change`, exact paths, no
  wildcard; every other row and the fail-closed uncovered-path rule
  unchanged). The Architecture
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
- **R3 complete:** R3 #28 (Plan analysis and generated governance — §10 rows
  9, 10, 12, with R2's C1/C2 discharged and the `ADO-PHASE`/fixture
  allocation reconciled) passed the full verify chain (S8 PASS; S9 evidence
  on the ticket, including the honestly recorded row-12 chronology
  deviation; S10 three-axis PASS; S11 PASS with no conditions) and merged at
  ⟦G-Merge⟧ via PR #38, merge commit
  `0bd35caaaebf7c7dd983a1f37d449d8491ea952f`; #28 is closed as completed.
  IR-1/IR-2 from the S10/S11 records (private-name promotions in
  `src/validator`) remain non-blocking implementation recommendations only —
  no owner assigned — for the next authorized `src/validator` touch. The
  committed lab inventory fixture (`governance/inventory/lab-inventory-fixture.yml`,
  content fixed to the ratified T16 #11 d7 five-entry set) travels with
  R4 #29 as a recorded prerequisite input (#29 grooming comment).
- **R4 complete:** R4 #29 (CI workflows — §10 row 11, with the recorded
  lab-inventory-fixture prerequisite landed first) passed the full verify chain
  (S8 PASS; S9 evidence on the ticket; S10 three-axis PASS; S11 PASS with no
  conditions) and merged at ⟦G-Merge⟧ via PR #39, merge commit
  `213da223281688d725a5f45d6f5e29a89d003ac6`; #29 is closed as completed. The
  first live PR runs of the authored `validate` and `plan-preview` checks both
  passed on PR #39 (run links in the #29 resolution comment); the checks are not
  yet server-side-required — that activation is R6/14a. IR-R4-1…4 from the
  S10/S11 records remain non-blocking implementation recommendations only — no
  owner assigned — for their natural owners (the next authorized `validator.ci`
  touch; the R6 #31 activation pass). Nothing in R4 contacted AWS, executed
  Terraform, changed GitHub configuration, or advanced any empirical condition.
- **R5 complete:** R5 #30 (Terraform roots and resource model — §10 row 13)
  passed the full verify chain — S8 PASS, S9 evidence, S10 three-axis PASS,
  and S11 PASS WITH CONDITIONS on `680e5151…`; was halted at excursion E1 by
  the first live `plan-preview` failure (`CLS-UNCOVERED-PATH` on
  `.gitignore`), resumed through the accepted
  [root-control-path classification amendment](../../../docs/specifications/slice-a-root-control-path-classification-amendment.md)
  (PR #41, merge `bd43ca77…`) and its focused exact-path classifier
  correction — that omission and correction are resolved; delta-revalidated
  with S7/S9/S10 addenda and an independent S11 delta attestation on head
  `112d69c…` (original verdict valid, no added condition), with both
  current-head automatic PR checks (`validate`, `plan-preview`) passing —
  and merged at ⟦G-Merge⟧ via PR #40, true merge commit
  `18e5ca0904cbde9cccf6d60796b3515a5add588f`; #30 is closed as completed.
  The single non-blocking condition C1 (verify saved-plan `file()` re-read
  semantics at the first authorized rehearsal; stage the retrieved plan
  context at the identical path if apply re-reads) travels with R7 #32
  (handoff comment on the ticket). IR-R5-2 and IR-R4-1…4 remain
  non-blocking recommendations only — no owner assigned. Zero Terraform
  execution, zero AWS contact, zero GitHub-configuration change; no lab
  verification or production readiness is claimed.
- **Current Objective:** preparation and owner review of the proposed narrow
  post-R5 portable-development checkpoint amendment before either R6 #31 or
  R7 #32 begins. The checkpoint remains a proposal only: it does not yet
  alter accepted architecture, ticket state, or any completion claim.
- **Next Milestone:** the checkpoint proposal decided at its own gate, then
  the live frontier — R6 #31 (repository-side control activation) and R7 #32
  (AWS-side OIDC/bootstrap), both open, unassigned, and unblocked — each
  requiring its own separate authorization beyond ticket creation; R8 #33
  remains blocked by open #32. No Terraform apply before the R6/14a control
  set is active. The three empirical conditions (provider execution; `forget`
  representation; import redaction) remain open and gate what their records
  say they gate.

## Repository Version sentinel

`none — untagged` is the Repository Version recorded while the repository has never
produced a Project Release. It corresponds to the **absence of any Git tag**: session
bootstrap's Repository-Version check (Status Artifact version = latest Git tag)
reconciles because both sides are "none". The sentinel is replaced by the first released
Semantic Version when Project Release (operator-guide S7/S8) reconciles this artifact
together with the tag and release metadata.
