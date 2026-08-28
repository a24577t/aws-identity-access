---
status: accepted
decided: 2026-08-28
authority: normative
scope: the content boundary of the first POC vertical slice and its recorded absences
decision_owner: "Eric — human project owner and decision authority"
---

# ADR-0004 — The slice-A boundary and its absent surfaces

The first POC vertical slice is slice A, Identity Center only: workforce groups as
identity-store references, exactly two permission sets (one AWS-managed attachment, one
narrowly scoped embedded inline document), GROUP-only per-file assignments to two named
lab accounts plus one `status: requested` deferral, and `instance.yml` as
declaration-and-verification data — with no IAM users, roles, trust policies, fleet roles,
or StackSets. Six surfaces are deliberately absent (`access/iam/`,
`access/deployments/fleet-roles/`, `access/identity-center/identity-source/`,
`access/identity-center/bootstrap/`, `governance/exceptions/`,
`governance/runtime-mutations/`), rejected by the selected-slice validation profile as a
profile rule, never a permanent domain-schema prohibition.

## Consequences

- The slice is greenfield-only with pre-existing lab resources protected; the overall
  implementation remains brownfield (T19 #14; the brownfield implementation plan).
- Out-of-slice forms are rejected under the `P-OOS-*` code family with wording "out of
  slice A — not prohibited by the domain architecture" (T21 #20 decision 7; T14 #19).
- T11 #16, T12 #17, and T13 #18 were closed Out of scope by this boundary and return only
  with a redrawn destination.

## Provenance

T03 #4 decisions 1–7 and T04 #6 decision 6 —
[T03 record @ 43bc0bb](https://github.com/a24577t/aws-identity-access/blob/43bc0bb3364abf57137bda502cd65cf1ee11885f/docs/wayfinding/map-1/04-smallest-poc-vertical-slice.md)
· [ticket #4](https://github.com/a24577t/aws-identity-access/issues/4) ·
[T04 record @ 43bc0bb](https://github.com/a24577t/aws-identity-access/blob/43bc0bb3364abf57137bda502cd65cf1ee11885f/docs/wayfinding/map-1/06-top-level-layout-and-the-requester-surface.md)
· [ticket #6](https://github.com/a24577t/aws-identity-access/issues/6).
