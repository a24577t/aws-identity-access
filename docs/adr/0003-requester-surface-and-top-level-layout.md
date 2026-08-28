---
status: accepted
decided: 2026-08-28
authority: normative
scope: the repository's top-level layout and the boundary of ordinary requester changes
decision_owner: "Eric — human project owner and decision authority"
---

# ADR-0003 — The `access/` requester surface and the top-level layout

The repository has eight roots — `access/`, `governance/`, `docs/`, `schemas/`,
`infrastructure/`, `src/`, `tests/`, `.github/` — and ordinary requester PRs are confined
to `access/`, which carries document 07's `identity-center/` subtree re-rooted under the
named requester surface and contains no code, credentials, generated AWS identifiers, or
runtime state.

## Considered options

The brief's `configuration/` root name was rejected by decision (no governing document
names or prohibits any root name); nested per-OU directories were rejected with the
OU-exclusion rule.

## Consequences

- Documents under `docs/` do not share equal authority; generated material is visibly
  non-authoritative (T20 #22 decision 6).
- `.github/`, `governance/`, `schemas/`, `infrastructure/`, and authoritative
  documentation carry the strictest applicable owner set (T06 #8 decision 3).
- One proposed document-07 refinement (add `groups/`; rename `assignments/` →
  `account-assignments/`; per-account-identity clarification) is carried by the owner
  ([upstream-proposals index](../architecture/upstream-proposals.md)).

## Provenance

T04 #6 decisions 1–2 and 4 —
[record @ 43bc0bb](https://github.com/a24577t/aws-identity-access/blob/43bc0bb3364abf57137bda502cd65cf1ee11885f/docs/wayfinding/map-1/06-top-level-layout-and-the-requester-surface.md)
· [ticket #6](https://github.com/a24577t/aws-identity-access/issues/6).
