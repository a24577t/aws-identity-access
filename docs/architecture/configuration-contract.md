---
status: accepted
decided: 2026-08-28
authority: normative
scope: the governed configuration file forms of the requester surface and their identity, grammar, and validation semantics
decision_owner: "Eric — human project owner and decision authority"
---

# Configuration contract — slice A

The governed file forms of the requester surface, **by citation** of the deciding records:
identity and grammar (T05 #7), assignment form (T10 #15), permission-set policy
representation (T21 #20), instance declaration (T22 #21), inventory fixture (T15 #10 d5;
T16 #11 d7), and the validation contract binding them (T14 #19). This document decides
nothing; on any divergence the cited decision prevails. JSON Schemas under `schemas/`
implement these forms at S6 (RD-04; the engineering specification).

## Common identity rules (T05 #7)

- Stable keys match `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`; permission-set keys 2–24
  characters, workforce-group keys 2–64. Filename stem = key exactly. Reject, never
  normalize (`KEY-GRAMMAR`, `KEY-FILENAME`).
- `--` is the reserved assignment-filename separator (structurally impossible inside a
  key) — T05 d1, T10 d1.
- Deployed permission-set Name = `<resource_name_prefix><key>`; prefix budget ≤ 8
  characters including delimiter; composed name ≤ 32 and unique including pre-existing
  sets (`KEY-COMPOSED`, `KEY-PROTECTED`). Lab prefix `ialab-` (T15 d8); target prefix
  `ia-` for newly created resources (T19 d18).
- Generated identifiers (GroupIds, ARNs, `AWSReservedSSO_*`) are outputs — never under
  `access/` (T05 d2–d3; pinned document 02 generated-identifier invariant).

## `access/identity-center/groups/<group-key>.yml` (T05 #7 d2)

Fields: `key` (= stem); required `identity_store_name` (exact Identity Store DisplayName;
Unicode code-point comparison; no normalization; `KEY-IDSTORE-NAME`); optional
informational `source: { provider, group_name }` (provenance only — never lookup,
authorization, or reconciliation input). Resolution via `GetGroupId` with
exact-DisplayName verification at plan/apply; failure is `PRQ-GROUP` — never creation,
never deferral (ADR-0007). One file per exact `identity_store_name`; unique keys
(`KEY-DUP`). Renames: lookup-name change under GroupId continuity; key rename atomic with
zero AWS mutations (T05 d4; `GOV-DECL-MATCH` for the declared workflows).

## `access/identity-center/permission-sets/<permission-set-key>.yml` (T21 #20 d1–d4; T05 d3)

Fields: `key`; required `description` (1–700, AWS pattern; `KEY-DESCRIPTION`); required
explicit `session_duration` (no inherited defaults); exactly one of `managed_policies`
(form 1) or `inline_policy` (form 2) under the slice profile (`P-OOS-POLICY-FORM`; the
domain schema admits both and multiple managed policies for later slices). AWS-managed
references use the full partition-qualified `arn:aws:iam::aws:policy/...` form — the sole
permitted ARN-shaped public vocabulary (T21 d2; `INV-PUBLIC-LEAK` exemption). No `tags`,
`relay_state` (omitted in slice A), `display_name`, ARN, or deployed-name field in YAML.
Admin-capable definitions are rejected by the T21 d6 hazard detector (`ADM-CAPABLE`;
ADR-0008). Key replacement = two-PR additive migration with field-level equivalence
(T05 d4; T21 d9; T06 d5 declarations).

## `access/identity-center/account-assignments/<account-name>/<group-key>--<permission-set-key>.yml` (T10 #15 d1–d6)

Filename: exactly two T05-valid keys joined by `--` (`ASN-SHAPE`). Directory and in-file
`account` are the exact same stable inventory alias — one path segment, alias grammar,
occurring exactly once in the consumed inventory (`ASN-ACCOUNT-ALIAS`; T09 rules for
absent/duplicate/deferred aliases). Exact field set, no additional properties:

```yaml
account: <account-name>
principal:
  type: GROUP
  group: <group-key>
permission_set: <permission-set-key>
```

Three-way path/content agreement is enforced (`ASN-AGREEMENT`; pinned I-1). Only the
two-segment GROUP form is recognized (`principal.type: USER` → `ASN-SHAPE` + `P-OOS-USER`,
the intentional T10 d7 dual-family pair). Duplicate prevention is by construction
(T10 d4's six-check proof). A `status: requested` account validates as deferred
(`INV-DEFERRED`), is omitted from the executable plan, and is never provisioned (RD-08).
Assignment deletes carry the exact-entry access-revocation acknowledgement
(`CLS-REVOCATION-ACK`; T20 d5).

## `access/identity-center/configuration/instance.yml` (T22 #21 d1–d2; ADR-0005)

Exact field set, unknown fields rejected (`CFG-FIELDS`): `instance_type: organization`
(`CFG-VOCAB`); `primary_region: us-east-1` and `additional_regions: []` — equality with
T15 d3; `instance.yml` is the sole regional authority (`CFG-REGION`);
`identity_source.type: identity-center-default` under the slice profile
(`P-OOS-IDENTITY-SOURCE`); `delegated_administrator: <alias>`; `owner: <principal key>`;
optional all-or-nothing `verification` block — `verified_at` byte-equal to the referenced
snapshot's `body.discovered_at`, `snapshot_id` 64 lowercase hex (`CFG-VERIFICATION`;
binding checks at plan/apply are `PRQ-*`, ADR-0006). No live identifier field exists in
the schema.

## Lab inventory fixture (T15 #10 d5; T16 #11 d7–d8)

Committed, explicitly labeled; entries carry exactly `alias`, `class`, `status`,
`intended_classification` (`FIX-FIELDS`); `class` ∈
`{management, role-host, lab-workload, requested-fixture}` (`FIX-CLASS`); aliases in the
T05/T15 grammar (`FIX-ALIAS`); no live identifier ever (`FIX-LIVE`). The five-entry
slice-A fixture and the requested-fixture deferred behavior are T16 d7/d8; the binding
snapshot contract is T09 #12.

## Governance records (T06 #8 d2, d5)

`governance/ownership/principals/*.yml` (`key`, `kind: role | team`, `description`; no
provider handles — `GOV-PRINCIPAL`); `governance/ownership/review-classes/*.yml` (`key`,
`description`, non-empty `satisfied_by`; no authored enforcement status — `GOV-CLASS`);
`governance/change-declarations/*.yml` (discriminated kinds with `schema_version`,
mandatory `valid_until`, no approval fields or live identifiers — `GOV-DECLARATION`,
`GOV-DECL-MATCH`). Catalog data under `governance/catalogs/` is specified by the
engineering specification §7.

## Validation binding (T14 #19)

The complete catalogue — 79 codes, 13 families, severity vocabulary, stage attribution,
canonical triggering layers, harmonization rules, fixture-tree contract
(`tests/fixtures/{valid,invalid/<CODE>}/`), and the redaction-safe finding contract — is
the [T14 record's Catalogue section](../wayfinding/map-1/19-validation-contract-for-the-selected-slice.md),
adopted by citation. Documentation headers are validated per T23 #23 (`DOC-*`); generated
artifacts per T20 #22 decision 6 (`GEN-*`); classification per T20 decisions 1–5
(`CLS-*`). Citation-anchor corrections applied under verdict condition C-B are recorded
in the engineering specification §9.
