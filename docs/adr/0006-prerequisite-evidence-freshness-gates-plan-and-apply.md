---
status: accepted
decided: 2026-08-28
authority: normative
scope: when missing or stale manual-prerequisite evidence blocks plan and apply
decision_owner: "Eric — human project owner and decision authority"
---

# ADR-0006 — Prerequisite-evidence freshness gates plan and apply

Missing or stale manual-prerequisite evidence blocks plan and apply, fail-closed and never
deferred: fresh requires the committed verification block, the current intact snapshot
within the 90-day backstop, live re-verification of every API-verifiable prerequisite at
every plan and apply, and validly bound human attestations for everything the authorized
APIs cannot observe.

## Consequences

- Validation stays hermetic (schema, formats, internal consistency; no clock, snapshot, or
  AWS call); the clock, snapshot, evidence, and AWS checks live at plan/apply
  (T22 #21 decision 4; T14 #19 decision 3).
- The `PRQ-*` code family carries the diagnostics; deferral remains reserved exclusively
  for `status: requested` inventory references (RD-08; `INV-DEFERRED`).

## Provenance

T03 #4 claim 2 refinement (b), instantiated by T22 #21 decisions 3–5 —
[T03 record @ 43bc0bb](https://github.com/a24577t/aws-identity-access/blob/43bc0bb3364abf57137bda502cd65cf1ee11885f/docs/wayfinding/map-1/04-smallest-poc-vertical-slice.md)
· [ticket #4](https://github.com/a24577t/aws-identity-access/issues/4) ·
[T22 record @ 6f2d84f](https://github.com/a24577t/aws-identity-access/blob/6f2d84f030691e34ea6c57994bf2007dfd7007e9/docs/wayfinding/map-1/21-manual-prerequisites-as-governed-configuration-and-evidence.md)
· [ticket #21](https://github.com/a24577t/aws-identity-access/issues/21).
