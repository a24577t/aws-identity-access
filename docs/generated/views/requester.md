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
target:
  path: docs/generated/views/requester.md
---

# Requester view

What each workforce group receives, derived from the governed
requester surface. Non-authoritative rendering.

## lab-readers

- lab-requested: read-only (session PT8H; portal ialab-read-only) - unresolved - no committed inventory fixture (deferral derives from the fixture)
- lab-workload-a: read-only (session PT8H; portal ialab-read-only) - unresolved - no committed inventory fixture (deferral derives from the fixture)
- lab-workload-b: read-only (session PT8H; portal ialab-read-only) - unresolved - no committed inventory fixture (deferral derives from the fixture)
