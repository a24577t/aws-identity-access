---
authority: generated
do_not_edit: true
generator:
  path: src/validator/governance_generator.py
  version: "1"
sources:
  - path: access/identity-center/account-assignments/lab-requested/lab-readers--read-only.yml
    revision: "cef077592b396a4467d8437aeee301f1f321a2b8"
  - path: access/identity-center/account-assignments/lab-workload-a/lab-readers--read-only.yml
    revision: "cef077592b396a4467d8437aeee301f1f321a2b8"
  - path: access/identity-center/account-assignments/lab-workload-b/lab-readers--read-only.yml
    revision: "cef077592b396a4467d8437aeee301f1f321a2b8"
  - path: access/identity-center/groups/lab-readers.yml
    revision: "cef077592b396a4467d8437aeee301f1f321a2b8"
  - path: access/identity-center/permission-sets/inventory-reader.yml
    revision: "cef077592b396a4467d8437aeee301f1f321a2b8"
  - path: access/identity-center/permission-sets/read-only.yml
    revision: "cef077592b396a4467d8437aeee301f1f321a2b8"
  - path: governance/inventory/lab-inventory-fixture.yml
    revision: "8dceaa192b73e9948e795be8a28dcafa6720dbd1"
target:
  path: docs/generated/views/account.md
---

# Account view

Effective access per stable account alias. Aliases only, ever.

## lab-requested

- lab-readers -> read-only (portal ialab-read-only) - deferred - reported deferred, never rejected (RD-08)

## lab-workload-a

- lab-readers -> read-only (portal ialab-read-only) - standing - until changed by governed PR

## lab-workload-b

- lab-readers -> read-only (portal ialab-read-only) - standing - until changed by governed PR
