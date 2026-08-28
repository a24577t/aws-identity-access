---
status: accepted
decided: 2026-08-28
authority: normative
scope: the lifecycle boundary between this repository and workforce-group management
decision_owner: "Eric — human project owner and decision authority"
---

# ADR-0007 — Workforce groups are references, never created here

Workforce groups are references resolved in the connected identity store, never created by
this repository: `groups/<group-key>.yml` declares the stable key and the exact
identity-store name, resolution uses Identity Store `GetGroupId` with exact-DisplayName
verification, and a missing group is a plan error — never a silent creation, never a
deferral. Group lifecycle stays with the identity source in lab and target alike.

## Consequences

- The resolved GroupId exists only in the generated plan, Terraform state, or evidence —
  never under `access/` (T05 #7 decision 2).
- A resolved GroupId that differs from state under an unchanged key is principal
  replacement, not a rename, and requires the declared exceptional workflow
  (T05 #7 decision 4; T06 #8 decision 5).

## Provenance

T03 #4 decision 3 and claim 2 refinement (c), instantiated by T05 #7 decision 2 —
[T03 record @ 43bc0bb](https://github.com/a24577t/aws-identity-access/blob/43bc0bb3364abf57137bda502cd65cf1ee11885f/docs/wayfinding/map-1/04-smallest-poc-vertical-slice.md)
· [ticket #4](https://github.com/a24577t/aws-identity-access/issues/4) ·
[T05 record @ 43bc0bb](https://github.com/a24577t/aws-identity-access/blob/43bc0bb3364abf57137bda502cd65cf1ee11885f/docs/wayfinding/map-1/07-natural-identifiers-for-workforce-groups-and-permission-sets.md)
· [ticket #7](https://github.com/a24577t/aws-identity-access/issues/7).
