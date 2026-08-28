---
status: accepted
decided: 2026-08-28
authority: normative
scope: the account scope of every ordinary access grant this repository declares
decision_owner: "Eric — human project owner and decision authority"
---

# ADR-0002 — No silent account expansion of ordinary access grants

Ordinary access grants never silently expand through StackSet or OU auto-deployment: OU
input may expand only into an explicit account list visible in the plan, and adding or
moving an account grants no automatic ordinary human access.

## Consequences

- OU membership is planning input only — never part of assignment identity or path
  (T10 #15 decision 1; T03 #4 decision 5).
- StackSets remain eligible only for identical fleet IAM resources with explicit targeting
  and explicit auto-deployment behavior — none of which exist in slice A (T13 #18, closed
  Out of scope).

## Provenance

T02 #3 claim 4 (absent upstream, compatible with the pinned `CONTEXT.md` *Baseline*
definition and document 04 Preference 3) —
[record @ 43bc0bb](https://github.com/a24577t/aws-identity-access/blob/43bc0bb3364abf57137bda502cd65cf1ee11885f/docs/wayfinding/map-1/03-deployment-in-the-poc.md)
· [ticket #3](https://github.com/a24577t/aws-identity-access/issues/3).
