---
authority: informative
derives_from:
  - docs/architecture/domain-overview.md
  - docs/architecture/configuration-contract.md
  - docs/adr/0008-no-standing-administrator-access.md
  - docs/adr/0009-poc-managed-resource-set.md
  - docs/wayfinding/map-1/08-approval-declarations-versus-enforcement.md
  - docs/wayfinding/map-1/22-ci-plan-contract-and-pr-classes-for-slice-a.md
---

# Reviewer guide

How review works and what a reviewer is accountable for. Informative — the normative
sources above prevail.

## The three layers you sit in (T06 #8 decision 1)

1. **Declared ownership** routes your review — it is metadata, never approval.
2. **Your review** satisfies exactly one independent review class per event
   (identity-platform, security, architecture, deployment-authority). One person or one
   event never satisfies two independently required classes for the same change.
3. **Apply authorization** is separate: approving a PR never authorizes an apply; the
   `lab` environment approval is bound to one exact saved plan, one scope, one attempt.

In the current single-collaborator lab, multi-class independence is technically
unenforced and is recorded honestly as a lab exception — never reported as independently
satisfied (T06 #8 decision 3; T15 #10 decision 15).

## What to check, by PR class (T20 #22)

- **access-grant** — assignments only; plan effects `creates-only`, acknowledged
  `deletes-only`, or `empty` (deferred). Verify the exact-entry revocation
  acknowledgement on any delete.
- **access-definition** — group references and permission sets; `creates-only` or
  `updates-only`; both canonical policy forms carry an explicit `session_duration`; the
  partition-qualified AWS-managed ARN is the only ARN you should ever see in public
  content.
- **verification-update** — the `instance.yml` verification block bump; plan `empty`
  only.
- **exceptional-change** — a merged declaration precedes the change; the declared kind's
  fixed plan class is the only permitted effect; retirement carries the destroy
  acknowledgement.
- **platform-change** — strictest review set; strict review never itself grants mutation
  authority; a non-empty plan must be attributable to an authorized surface.
- **documentation** — never plan-eligible.

## Hard stops

Reject on sight: any admin-capable definition or standing-admin combination (ADR-0008 —
the validator's `ADM-*` codes are the mechanism, your review is defense-in-depth); any
plan row touching a resource outside the POC-managed set (ADR-0009); any live identifier
in public content; any attempt to weaken review by editing class lists or declarations
(review classes are derived, never requester-authored); any effect targeting a deferred
account.
