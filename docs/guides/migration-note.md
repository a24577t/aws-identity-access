---
authority: informative
derives_from:
  - docs/architecture/domain-overview.md
  - docs/specifications/brownfield-implementation-plan.md
  - docs/wayfinding/map-1/14-brownfield-adoption-and-migration-strategy.md
  - https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/09-tier0-execution.md
---

# Migration note — where the brownfield came from and what was kept

Content owned by T19 #14 (decision 1 and 19); T23 #23 fixed only this note's place and
class. Informative — the cited records prevail.

## What the evidence was

The pinned aws_ami revision holds two inspectable implementation trees — the scaffold
(`scaffolding/aws-identity-access/`) and the exploratory repository
(`aws-identity-access/` + `REVIEW.md`). They are **evidence, never authority** (map #1
Notes), inventoried traceably as 104 components by T18 #5
(`docs/research/brownfield-inventory.md`).

## Dispositions (T19 #14 decision 1)

Every component carries a disposition with cited basis: **retain / adapt / replace /
retire / deferred**. Notable adaptations: the read-only permission-set form, the
group-reference registry shape, the deferred-reference mechanism, the
`instance.yml`/verification-record pattern, and the exploratory validator's reusable
codes. Notable replacements: aggregated assignment files → one grant per file with the
`--` filename rule; hand-written CODEOWNERS → the generated registry chain.

## The nine rejected conventions (preserved as evidence only)

1. Reusable trust profiles (trust policies live complete and local — rejected).
2. Bidirectional group membership (group-side only).
3. Cross-directory permission-set inline-policy references (documents are embedded).
4. Narrow-deny statements as a control idiom.
5. OU auto-expansion of grants (`_ou-wide`) — ADR-0002.
6. Aggregated multi-account assignment files (`_finance-reporting`).
7. A security-sensitive defaults layer (explicit values only — e.g. `session_duration`).
8. `pa-*`/`PA-*` reserved-namespace ownership (ownership comes from explicit metadata).
9. Name-pattern ownership exclusions (`excluded_role_patterns`) — generated identifiers
   are excluded by the document-02 invariant, not name lists.

## What retirement means

The scaffold and exploratory trees are retired **as implementation sources only** — they
remain citable evidence at the pin; **the pinned aws_ami architecture documents and
decision register are not retired** and remain governing platform authority until
properly superseded upstream (T19 #14 decision 19). Adoption of live legacy resources
happens only inside the separately authorized post-acceptance import-rehearsal phase and
target waves, under the
[brownfield implementation plan](../specifications/brownfield-implementation-plan.md);
slice A itself is greenfield-only with pre-existing resources protected (ADR-0004,
ADR-0009).
