---
authority: informative
derives_from:
  - docs/architecture/domain-overview.md
  - docs/architecture/configuration-contract.md
  - docs/adr/0003-requester-surface-and-top-level-layout.md
  - docs/adr/0007-workforce-groups-are-references.md
  - docs/adr/0008-no-standing-administrator-access.md
---

# Requester guide

How to request durable access. This guide is informative: it summarizes the normative
sources above and can neither create nor override a rule.

## What you can request

Everything you may change lives under `access/` — the requester surface (ADR-0003). For
slice A that means: referencing a workforce group, defining a permission set, and
assigning a group a permission set in a named account. You never create groups (they are
references to the identity store, ADR-0007), never touch anything outside `access/`, and
never request standing administrator access (ADR-0008).

## The three file kinds you will touch

The exact forms, grammars, and error codes are the
[configuration contract](../architecture/configuration-contract.md); in brief:

1. **A group reference** — `access/identity-center/groups/<group-key>.yml` with the exact
   identity-store DisplayName. If the group does not exist in the identity store, the
   plan fails; nothing is created for you.
2. **A permission set** — `access/identity-center/permission-sets/<key>.yml` with a
   required `description`, a required explicit `session_duration`, and exactly one policy
   form: an AWS-managed policy attachment **or** an embedded inline policy document.
3. **An assignment** — one grant per file:
   `account-assignments/<account-name>/<group-key>--<permission-set-key>.yml`, where
   `<account-name>` is the stable inventory alias.

## Canonical examples (proposed; keys illustrative until accepted)

The two canonical permission-set forms (from T21 #20, with the verdict C-A key
replacement applied — see the mapping note in the
[engineering specification](../specifications/slice-a-engineering-specification.md) §9):

`access/identity-center/permission-sets/read-only.yml`

```yaml
key: read-only
description: Read-only access via the AWS-managed ReadOnlyAccess policy.
session_duration: PT8H
managed_policies:
  - arn:aws:iam::aws:policy/ReadOnlyAccess
```

`access/identity-center/permission-sets/inventory-reader.yml`

```yaml
key: inventory-reader
description: Narrow read access to basic IAM account and identity inventory.
session_duration: PT1H
inline_policy:
  Version: "2012-10-17"
  Statement:
    - Sid: ReadIdentityInventory
      Effect: Allow
      Action:
        - iam:GetAccountSummary
        - iam:ListAccountAliases
      Resource: "*"
```

An assignment (from T10 #15):

`access/identity-center/account-assignments/lab-workload-a/lab-readers--read-only.yml`

```yaml
account: lab-workload-a
principal:
  type: GROUP
  group: lab-readers
permission_set: read-only
```

The same grant to a second account is a second file; a grant to a `status: requested`
account is written identically and reported **deferred**, never invalid — the account is
not created for it.

## What happens to your PR

Validation runs hermetically and rejects rule violations with stable codes; your PR is
routed to the required review classes derived from the paths you touched; a sanitized
plan preview appears on the PR (never authoritative); after merge, the applicable saved
plan is produced, separately approved, and applied exactly (T06 #8; T20 #22). Removing an
assignment requires the exact-entry access-revocation acknowledgement. Out-of-slice
content is rejected with "out of slice A — not prohibited by the domain architecture" —
ask for a governed slice change rather than working around the profile.
