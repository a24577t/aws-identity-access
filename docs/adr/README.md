# Domain decision register — index

Subordinate index of the domain decision register (ADR-primary form, T08 #13 decisions
1–11). One line per record; this index is derived and never overrides a record. Records
hold only decisions this repository owns.

**Scope exclusions (T08 #13 decision 3):** platform architecture — cited as
`I-n` / `RD-nn` / `OD-nn` / document number at the pinned aws_ami revision
`5f3cb7163f468730fd2ceb5d565c90b0bfda6099`, never restated; methodology decisions
(MADRs under `.ai/repository/methodology/adr/`); the glossary (root `CONTEXT.md`);
process state (tracker, STATUS); wayfinding records (`docs/wayfinding/` — proposed
discovery, never accepted architecture); specifications (`docs/specifications/`);
operational and lab records in the homes prior decisions gave them (referenced, never
duplicated).

Acceptance occurs only at ⟦G-Accept⟧/⟦G-Refine⟧; a proposed record's `status` flips to
`accepted` with `decided` added atomically in the gate's acceptance merge. Superseded
records stay byte-unchanged; a superseding record carries `supersedes:`; derived
supersession relationships may be shown here non-authoritatively.

## Records

| ID | Title | Status |
|---|---|---|
| [ADR-0001](0001-one-reconciliation-owner-per-resource.md) | One reconciliation owner per resource | accepted |
| [ADR-0002](0002-no-silent-account-expansion.md) | No silent account expansion of ordinary access grants | accepted |
| [ADR-0003](0003-requester-surface-and-top-level-layout.md) | The `access/` requester surface and the top-level layout | accepted |
| [ADR-0004](0004-slice-a-boundary-and-absent-surfaces.md) | The slice-A boundary and its absent surfaces | accepted |
| [ADR-0005](0005-instance-yml-declaration-and-verification-data.md) | `instance.yml` is declaration-and-verification data | accepted |
| [ADR-0006](0006-prerequisite-evidence-freshness-gates-plan-and-apply.md) | Prerequisite-evidence freshness gates plan and apply | accepted |
| [ADR-0007](0007-workforce-groups-are-references.md) | Workforce groups are references, never created here | accepted |
| [ADR-0008](0008-no-standing-administrator-access.md) | No standing administrator access | accepted |
| [ADR-0009](0009-poc-managed-resource-set.md) | The POC-managed resource set and protected resources | accepted |
