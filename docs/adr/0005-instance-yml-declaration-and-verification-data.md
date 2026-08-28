---
status: accepted
decided: 2026-08-28
authority: normative
scope: the meaning and limits of the committed Identity Center instance declaration
decision_owner: "Eric — human project owner and decision authority"
---

# ADR-0005 — `instance.yml` is declaration-and-verification data

`access/identity-center/configuration/instance.yml` is governed
declaration-and-verification data — intended instance characteristics, primary Region,
identity-source type, delegated administrator, responsible owner, and a verification
reference — and never a claim that this repository creates or owns the instance
lifecycle. Reconciling the instance or identity source via Terraform would conflict with
document 07 and is not done.

## Consequences

- The exact committed field set and the all-or-nothing `verification` block are fixed by
  T22 #21 decision 1 and cited by the
  [configuration contract](../architecture/configuration-contract.md); the file lands at
  S6 under the accepted layout.
- `instance.yml` is the sole regional authority; the binding snapshot's Region field is a
  projection that must equal it (T09 #12 decision 5; T15 #10 decision 3).

## Provenance

T03 #4 claim 2 refinement (a), instantiated by T22 #21 decision 1 —
[T03 record @ 43bc0bb](https://github.com/a24577t/aws-identity-access/blob/43bc0bb3364abf57137bda502cd65cf1ee11885f/docs/wayfinding/map-1/04-smallest-poc-vertical-slice.md)
· [ticket #4](https://github.com/a24577t/aws-identity-access/issues/4) ·
[T22 record @ 6f2d84f](https://github.com/a24577t/aws-identity-access/blob/6f2d84f030691e34ea6c57994bf2007dfd7007e9/docs/wayfinding/map-1/21-manual-prerequisites-as-governed-configuration-and-evidence.md)
· [ticket #21](https://github.com/a24577t/aws-identity-access/issues/21).
