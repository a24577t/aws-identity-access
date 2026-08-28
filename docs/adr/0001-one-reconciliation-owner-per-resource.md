---
status: accepted
decided: 2026-08-28
authority: normative
scope: reconciliation ownership of every AWS resource this repository manages or consumes
decision_owner: "Eric — human project owner and decision authority"
---

# ADR-0001 — One reconciliation owner per resource

Every resource has exactly one reconciliation owner. Terraform must not directly manage
resources generated and reconciled by StackSets; runtime-mutation contracts name the
applicable reconciliation plane; this repository never reconciles resources owned by
another mechanism.

## Consequences

- The POC-managed resource set (ADR-0009) is the exact boundary of this repository's
  reconciliation ownership in the lab.
- A proposed upstream clarification to aws_ami document 05 is carried by the owner
  ([upstream-proposals index](../architecture/upstream-proposals.md)); the local decision
  stands regardless of when or whether it lands.

## Provenance

T02 #3 claim 3 (compatible with I-3, I-6, and the `reconciliation` field of
`05-runtime-mutation-contracts.md` at the pin) —
[record @ 43bc0bb](https://github.com/a24577t/aws-identity-access/blob/43bc0bb3364abf57137bda502cd65cf1ee11885f/docs/wayfinding/map-1/03-deployment-in-the-poc.md)
· [ticket #3](https://github.com/a24577t/aws-identity-access/issues/3).
