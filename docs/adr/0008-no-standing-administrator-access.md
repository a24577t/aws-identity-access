---
status: accepted
decided: 2026-08-28
authority: normative
scope: standing administrator authority for workforce principals in durable access
decision_owner: "Eric — human project owner and decision authority"
---

# ADR-0008 — No standing administrator access

No standing account assignment grants `AdministratorAccess`-equivalent authority to a
workforce principal in durable access, in every environment including the lab;
administrative authority is obtained only through the governed elevation lifecycle
(request → grant → automatic expiry → reconciliation) once a governed elevation service is
accepted and implemented.

## Consequences

- An admin-capable permission-set definition may exist only as a durable construct
  supporting the future elevation service; its existence never authorizes an assignment
  (T07 #9 decision 1).
- Slice A demonstrates no valid administrator path — negative validator proof only, via
  the `ADM-CAPABLE`/`ADM-STANDING`/`ADM-CATALOG` codes and the T21 #20 decision-6
  detector, with specimens confined to the test-fixture tree (T07 #9 decision 2;
  T14 #19 decision 5).
- Management-account, root, recovery, and lab-operator access is an external operational
  prerequisite — not represented, reconciled, or treated as precedent here; a proposed
  upstream refinement to documents 01/11 is carried by the owner
  ([upstream-proposals index](../architecture/upstream-proposals.md)).

## Provenance

T07 #9 decisions 1–3 —
[record @ 8530c46](https://github.com/a24577t/aws-identity-access/blob/8530c4671c538cb0332a844ff6210c636fc3f016/docs/wayfinding/map-1/09-standing-administrator-access.md)
· [ticket #9](https://github.com/a24577t/aws-identity-access/issues/9).
