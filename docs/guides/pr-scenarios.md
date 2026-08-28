---
authority: informative
derives_from:
  - docs/architecture/configuration-contract.md
  - docs/adr/0003-requester-surface-and-top-level-layout.md
  - docs/wayfinding/map-1/22-ci-plan-contract-and-pr-classes-for-slice-a.md
  - docs/wayfinding/map-1/21-manual-prerequisites-as-governed-configuration-and-evidence.md
---

# PR scenarios — slice A

Three end-to-end scenarios (T23 #23 decision 6). PR classes are cited from the T20 #22
contract, never defined here. Informative — the normative sources prevail.

## Scenario 1 — an access-grant PR

Grant `lab-readers` the `read-only` permission set in both workload accounts, with the
deferred third target:

- Files added: `account-assignments/lab-workload-a/lab-readers--read-only.yml`,
  `account-assignments/lab-workload-b/lab-readers--read-only.yml`,
  `account-assignments/lab-requested/lab-readers--read-only.yml` (byte-identical shape;
  deferral lives only in the inventory).
- Class: **access-grant**. Review: the inventory-resolved account delegation
  (identity-platform for slice A).
- Preview on the PR: sanitized, fixture-alias-only. Post-merge: the applicable saved plan
  shows two distinct assignment creates and the `lab-requested` row as **deferred**;
  after environment approval, exactly that plan is applied.

## Scenario 2 — an access-definition PR

Introduce a new permission set (say a second inline-policy set) and its assignments in
one PR:

- Files added: `permission-sets/<new-key>.yml` plus its `account-assignments/` files.
- Classes compose: **access-definition + access-grant** (one atomic PR per pinned I-8);
  review is the union — identity-platform + security for the definition, the account
  delegation for the grants; permitted effects `creates-only`.
- The definition must carry an explicit `session_duration` and exactly one policy form;
  an admin-capable document is rejected outright (`ADM-CAPABLE`).

## Scenario 3 — a verification-update PR

Record a fresh prerequisite verification after a re-discovery (the T22 #21
`verified_at`/`snapshot_id` bump):

- File changed: `configuration/instance.yml` — only the `verification` block, both fields
  together (all-or-nothing).
- Class: **verification-update**. Permitted plan effect: **empty** — the declaration
  drives gating, never AWS resources.
- Plan and apply then verify the block against the current binding snapshot and live
  prerequisites; a mismatch fails closed (`PRQ-SNAPSHOT` and friends).

## Not shown here

The permission-set key-rename flow is a two-PR additive migration under a merged change
declaration (T05 #7 decision 4; T06 #8 decision 5) — deliberately not an introductory
scenario. Rehearsal-family PRs stay dormant until their gates pass (T20 #22 decision 7).
