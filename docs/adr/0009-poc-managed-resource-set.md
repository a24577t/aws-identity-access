---
status: accepted
decided: 2026-08-28
authority: normative
scope: the exact mutation boundary of the POC pipeline and the protection of everything else
decision_owner: "Eric — human project owner and decision authority"
---

# ADR-0009 — The POC-managed resource set and protected resources

The POC pipeline may create, update, or delete only POC-managed resources — permission
sets whose deployed Name carries the selected prefix and tags, their AWS-managed-policy
attachment or embedded inline policy, and GROUP account assignments of those sets to
`lab-workload` accounts — and every pre-existing resource is protected: any plan touching
anything outside the derived POC-managed set is rejected, with the plan gate as the
primary control and role policies as defense-in-depth.

## Consequences

- Divergence detected in POC-managed resources is alerted, evidenced, and reconciled only
  through a governed PR; pre-existing resources are never reconciled (T15 #10 decision 7;
  document 05 drift policy).
- Prefix and tags are coexistence markers, never reconciliation-ownership authority
  (ADR-0001; T04 #6 decision 5); a deployed-name collision with a pre-existing set is a
  protected-resource error (`KEY-PROTECTED`, `CLS-PROTECTED`; T14 #19).

## Provenance

T15 #10 decision 7 —
[record @ 62b76c4](https://github.com/a24577t/aws-identity-access/blob/62b76c4cf3f4b0aea856ee10c63650e3a0f9a02d/docs/wayfinding/map-1/10-lab-environment-test-and-deployment-contract.md)
· [ticket #10](https://github.com/a24577t/aws-identity-access/issues/10).
