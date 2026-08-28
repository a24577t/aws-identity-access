# aws-identity-access

Durable AWS access — IAM Identity Center workforce-group references, permission sets, and
standing account assignments — governed as configuration in this repository. Access
persists until removed through a governed PR. This README is navigation only: it holds no
independent authority, cites rather than decides, and accepted decisions prevail on any
conflict (T23 #23 decision 4).

Governing platform architecture is the pinned aws_ami revision
`5f3cb7163f468730fd2ceb5d565c90b0bfda6099` (ADR-0004 provenance; T01 #2): cited by stable
identifier, never restated. The domain glossary is [`CONTEXT.md`](CONTEXT.md); the domain
decision register is [`docs/adr/`](docs/adr/README.md); repository governance and
methodology live under [`.ai/`](.ai/README.md) (see [`CLAUDE.md`](CLAUDE.md)).

## Layout (slice A)

| Root | Purpose |
|---|---|
| `access/` | the requester surface — ordinary access-request PRs modify only this tree (ADR-0003); content lands at S6 under the accepted layout |
| `governance/` | declarations that are not routine access grants: ownership registry, review classes, change declarations, catalog data (T06 #8; S6) |
| `docs/` | documentation with unequal authority: `architecture/` (normative), `guides/` (informative), `adr/` (register), `wayfinding/`·`research/` (records/evidence), `generated/` (S6; visibly non-authoritative), `specifications/` |
| `schemas/` | JSON Schemas validating governed configuration (RD-04; S6) |
| `infrastructure/` | Terraform and deployment mechanics; derives deployed names (S6) |
| `src/` | validation and effective-plan implementation code (S6) |
| `tests/` | executable validation tests and per-code fixtures (T14 #19; S6) |
| `.github/` | CI, generated CODEOWNERS, repository automation (S6) |

## Documentation (reading order — T23 #23 decision 5)

1. [`docs/architecture/domain-overview.md`](docs/architecture/domain-overview.md) —
   the slice-A domain architecture (normative).
2. [`docs/architecture/configuration-contract.md`](docs/architecture/configuration-contract.md)
   — the governed file forms and validation semantics, by citation (normative).
3. [`docs/adr/README.md`](docs/adr/README.md) — the domain decision register index.
4. [`docs/guides/requester-guide.md`](docs/guides/requester-guide.md) ·
   [`docs/guides/reviewer-guide.md`](docs/guides/reviewer-guide.md) ·
   [`docs/guides/federated-access-walkthrough.md`](docs/guides/federated-access-walkthrough.md)
   · [`docs/guides/pr-scenarios.md`](docs/guides/pr-scenarios.md) ·
   [`docs/guides/migration-note.md`](docs/guides/migration-note.md) — informative guides.
5. [`docs/architecture/upstream-proposals.md`](docs/architecture/upstream-proposals.md) —
   informative index of upstream proposals carried by the owner.
6. [`docs/specifications/`](docs/specifications/) — the slice-A engineering specification
   and the brownfield implementation plan (S6 consumes them after acceptance).

## Absent for slice A (T04 #6 decision 6; ADR-0004)

Each surface below is deliberately absent from the selected slice. The selected-slice
validation profile rejects files under these paths with a stable out-of-slice error code
(`P-OOS-PATH`, T14 #19) — a profile rule, not a permanent domain prohibition. Later slices
may introduce a surface only through a governed decision.

- `access/iam/` — no IAM users or roles in slice A (T03 #4 decision 1; T11 #16, T12 #17
  closed Out of scope).
- `access/deployments/fleet-roles/` — no fleet roles or StackSets (T03 #4; T13 #18 closed
  Out of scope).
- `access/identity-center/identity-source/` — the identity source is an evidenced
  prerequisite, not desired configuration (T03 #4 decision 2; T22 #21 decision 2).
- `access/identity-center/bootstrap/` — no bootstrap procedures surface in slice A
  (T04 #6 decision 6).
- `governance/exceptions/` — no IAM-user exception records (T03 #4; T11 #16).
- `governance/runtime-mutations/` — the OD-16 convention is inherited; slice A contains no
  runtime-mutation contract (T04 #6 decision 6).

## Absent or pending documentation (T23 #23 decision 7)

- `docs/generated/` — generated effective-access examples and views arrive only with the
  S6 tooling under the T20 #22 decision-6 metadata contract; nothing generated is authored
  by hand.
- Validator, schemas, fixtures, workflows, CODEOWNERS, and all implementation — S6 work
  items of the accepted engineering specification; none exist yet.
- The lab environment itself (AWS Organization, Identity Center instance, accounts) — the
  T16 #11 decision-11 staged remediation, each stage separately authorized; committed
  `access/` content including `instance.yml` lands at S6.

## Status

The slice-A architecture set (register, normative documents, guides, specifications) is
proposed for acceptance at ⟦G-Accept⟧; see
[`.ai/repository/state/STATUS.md`](.ai/repository/state/STATUS.md) for the authoritative
current objective. Wayfinder discovery records live under
[`docs/wayfinding/`](docs/wayfinding/README.md); the intake brief
([`aws-identity-access-poc-prompt.md`](aws-identity-access-poc-prompt.md)) is historical
input, not authority.
