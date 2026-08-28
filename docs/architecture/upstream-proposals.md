---
authority: informative
derives_from:
  - docs/wayfinding/map-1/03-deployment-in-the-poc.md
  - docs/wayfinding/map-1/06-top-level-layout-and-the-requester-surface.md
  - docs/wayfinding/map-1/07-natural-identifiers-for-workforce-groups-and-permission-sets.md
  - docs/wayfinding/map-1/09-standing-administrator-access.md
  - docs/wayfinding/map-1/12-organization-inventory-transport-and-snapshot-contract.md
  - docs/wayfinding/map-1/13-domain-decision-register-form.md
  - docs/wayfinding/map-1/15-group-and-user-assignment-identity-and-filename-rules.md
  - docs/wayfinding/map-1/21-manual-prerequisites-as-governed-configuration-and-evidence.md
  - https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/11-decision-register.md
---

# Upstream proposals carried by the owner

Proposal tracking only (T08 #13 decision 8) — this index is informative, creates no rule,
and never edits aws_ami. Each proposal is carried by Eric to the platform's governing
acceptance process; every local decision stands regardless of when or whether a proposal
lands. Status: **none yet carried** as of this document's date. OD-09 and OD-12 remain
open platform-wide and are dispositioned locally by T15 #10 d13 and T19 #14 d20 without
upstream text from this repository. `aws_ami` is never edited by this repository.

| # | Target | Proposal (exact carried text lives in the source record) | Source |
|---|---|---|---|
| 1 | document 09 | Define whether a controlled nonproduction POC exception (state backend co-located in a lab workload account) is permitted, and under what boundaries | T02 #3 ([record](../wayfinding/map-1/03-deployment-in-the-poc.md)) |
| 2 | document 05 | Singular reconciliation-owner clarification (one reconciliation owner per resource; Terraform never directly manages StackSet-reconciled resources) | T02 #3 ([record](../wayfinding/map-1/03-deployment-in-the-poc.md)) |
| 3 | document 02 | One-sentence clarification: generated Identity Center GroupIds, permission-set ARNs, and provisioned `AWSReservedSSO_*` roles are outputs under the generated-identifier invariant | T05 #7 ([record](../wayfinding/map-1/07-natural-identifiers-for-workforce-groups-and-permission-sets.md)) |
| 4 | document 07 | One refinement, extended by T10: add `groups/` to the directory shape; rename `assignments/` → `account-assignments/`; per-account assignment identity with OU as planning input only | T04 #6 ([record](../wayfinding/map-1/06-top-level-layout-and-the-requester-surface.md)); extended by T10 #15 d7 ([record](../wayfinding/map-1/15-group-and-user-assignment-identity-and-filename-rules.md)) |
| 5 | documents 01/11 | One-sentence refinement: standing `AdministratorAccess`-equivalent workforce assignments prohibited in durable access; authority only through the governed elevation lifecycle owned by `aws-privileged-access` | T07 #9 ([record](../wayfinding/map-1/09-standing-administrator-access.md)) |
| 6 | OD-21 | Downstream inventory consumption is pinned with an auto-PR bump; tracking consumption prohibited for Tier-0 consumers | T09 #12 d23 ([record](../wayfinding/map-1/12-organization-inventory-transport-and-snapshot-contract.md)) |
| 7 | RD-09 | Clarification: RD-09's sole-authority scope covers platform architecture decisions; a domain repository may maintain a register for decisions it owns, referencing and never restating this register | T08 #13 d14 ([record](../wayfinding/map-1/13-domain-decision-register-form.md)) |
| 8 | OD-08 | Manual/console Identity Center configuration: identity-platform owner, per-step authorization, declaration-and-verification representation, two evidence tiers, live re-verification, 90-day backstop | T22 #21 d7 ([record](../wayfinding/map-1/21-manual-prerequisites-as-governed-configuration-and-evidence.md)) |
