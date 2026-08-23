---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 12
title: "T09 — Organization-inventory transport and snapshot contract"
url: https://github.com/a24577t/aws-identity-access/issues/12
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-23
sources:
  inherited_inputs:
    - https://github.com/a24577t/aws-identity-access/issues/12#issuecomment-5383470536
    - https://github.com/a24577t/aws-identity-access/issues/12#issuecomment-5386980272
  t15_record: https://github.com/a24577t/aws-identity-access/blob/62b76c4cf3f4b0aea856ee10c63650e3a0f9a02d/docs/wayfinding/map-1/10-lab-environment-test-and-deployment-contract.md
  t16_record: https://github.com/a24577t/aws-identity-access/blob/d357db7beb48f86b2e20fa20f4961cbab6512a89/docs/wayfinding/map-1/11-lab-account-topology-and-fixtures.md
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  primary_sources:
    - AWS Organizations API Reference — Account data type (State values; Status retired 2026-09-09), ListAccounts, ListParents
    - AWS Organizations User Guide — Monitor the state of your AWS accounts
    - RFC 8785 — JSON Canonicalization Scheme (informational)
    - Amazon S3 User Guide — conditional writes (If-None-Match / If-Match), security best practices, Object Lock
---

# T09 — Organization-inventory transport and snapshot contract

> Proposed discovery record — the complete durable result of T09 #12. Decisions approved by Eric
> as the human project owner and decision authority after collaborator review; executed by Claude
> in the repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`, using the
> batch-question rule (operating-guide governing invariant 3). **Nothing here is accepted
> architecture: every decision is a proposal until ⟦G-Verdict⟧ and ⟦G-Accept⟧.** GitHub issue #12
> is the workflow/index surface and links to this record.

## Authorization scope of this record

Accepting T09 approves the **proposed contract decisions only**. It does not authorize AWS calls,
S3 writes, evidence or snapshot creation, GitHub configuration, schema or implementation files,
or any S6 remediation action. No binding record, snapshot, fixture file, or pointer object is
created by this record.

## Claim-resolution record (grill-with-docs)

| # | Claim | Authority | Result | Upstream amendment / refinement |
|---|---|---|---|---|
| 1 | References are by inventory name only; the name→ID binding lives only in the org repository's `account.yml` | I-1, `02` (single binding, downstream by name), RD-06 | **inherited** for the target estate; the lab's single non-public binding snapshot (decisions 1, 3) is a **compatible, recorded lab-only exception** that stands in for the absent publication and is never a second authority | none |
| 2 | `status: requested` references are valid but deployment-deferred — warn, omit at deploy, report "deferred", never "invalid"; a name absent from the inventory fails | RD-08, `06`, `02` validation rule 3 | **inherited** — decisions 12, 19 | none |
| 3 | "Consume the current published inventory but record the exact version or digest in CI plans and deployment evidence" resolves OD-21 | OD-21, I-9, the brief | **compatible** — resolved for this consumer as **pinned** consumption with a governed bump (decision 23); the upstream proposal text is carried by Eric | OD-21 proposal (decision 23) |
| 4 | A local inventory may exist only as an explicitly labeled test fixture | the brief, T15 d5, T16 d7 | **inherited** — decision 3 | none |

## Decisions (approved option A, with collaborator corrections integrated)

### Decision 1 — Authoritative producer and the lab-only producer exception
Target: `aws-organization-governance` is the sole producer of the organization inventory
(accounts, OUs, `enabled_regions`) through its governed `account.yml` / `ou.yml` write-back flow.
Lab-only exception (recorded, never precedent): while that repository is absent, the **Stage 6.1
read-only re-discovery performed by the repository owner under the named lab profile from
`lab-tooling`** (a delegated administrator, so Organizations read operations are permitted) is
the producer of exactly one binding snapshot per fixture digest, published only under Stage 6.3
authorization (T16 decision 11). This repository never becomes the inventory authority.
Classification: target **inherited** (I-4, I-10, `01`, `06`, RD-01, RD-06); lab producer
**absent upstream, compatible** (T15 d5, T16 d11–d12). Rejected: pipeline-produced snapshots
(an unattended pipeline as inventory authority); hand-authored bindings (no API-derived
evidence).

### Decision 2 — Consumer boundary
This repository consumes inventory **by alias only** under `access/`, resolves live identifiers
**only at plan and apply time inside the pipeline**; resolved identifiers are never committed;
there is no durable persistence outside the evidence prefix; restricted transient Stage 6.1
handling is permitted only as defined by decision 22; and this repository never maintains or
amends inventory. The per-account delegation class (T06) travels as `intended_classification`
in the fixture (lab) or as inventory data (target), never authored in assignment files.
Classification: **inherited** (I-4, `02`, RD-06, T06 d3, T15 d5/d12). Rejected: a resolved copy
under `docs/generated/` (second binding location; public-identifier boundary).

### Decision 3 — Fixture versus binding snapshot
The **committed fixture** (aliases plus exactly `class`, `status`, `intended_classification`)
is the only inventory artifact in git. The **binding snapshot** is a single non-public object
per fixture digest; `body.fixture.digest` must equal the SHA-256 of the exact committed
fixture-file bytes at the consumed source commit, or the run fails closed (`INV-DIGEST`). A
fixture change produces a new fixture digest and therefore requires a new snapshot through
Stage 6.1/6.3 again. Classification: **inherited** (T15 d5, T16 d7/d12, RD-06). Rejected: one
snapshot binding several fixture versions.

### Decision 4 — Snapshot envelope schema (illustrative, non-live)
The stored object is an **envelope**; `snapshot_id` is never inside `body`:

```json
{
  "snapshot_id": "<lowercase hex SHA-256 of RFC 8785 canonical body>",
  "body": {
    "schema_version": 1,
    "kind": "lab-binding-snapshot",
    "supersedes": "<previous snapshot_id or null>",
    "fixture": { "path": "<repository path>", "digest": "<sha256 of committed bytes>", "source_commit": "<commit sha>" },
    "discovered_at": "<RFC 3339 UTC string>",
    "producer": { "identity_type": "iam-user | assumed-role", "account_alias": "lab-tooling" },
    "organization": { "organization_id": "<o-…>", "feature_set": "ALL", "root_id": "<r-…>", "management_account_alias": "lab-management" },
    "identity_center": { "instance_arn": "<instance ARN>", "identity_store_id": "<d-…>", "region": "us-east-1", "delegated_admin_alias": "lab-tooling" },
    "accounts": [
      { "alias": "lab-workload-a", "live_name": "<Organizations Name>", "account_id": "<12-digit string>", "state": "ACTIVE",
        "joined_method": "CREATED | INVITED", "joined_timestamp": "<RFC 3339 string>",
        "ou": { "ou_id": "<ou-…>", "logical_class": "lab", "path": "<Organizations Paths[0]>" }, "tags_verified": true },
      { "alias": "lab-requested", "binding": "unbound" }
    ]
  }
}
```

Rules: `snapshot_id = lowercase_hex(SHA-256(RFC8785(body)))`; the complete envelope is stored
using deterministic RFC 8785 serialization; the object key, the envelope `snapshot_id`, the S3
metadata value, and the `.sha256` sidecar must all equal the recomputed body digest, and a
mismatch among any of those locations is `INV-DIGEST`; RFC 8785's I-JSON constraints apply —
duplicate keys, invalid Unicode, unsupported numeric values, or canonicalization failure are
fail-closed; identifiers and timestamps are JSON strings, never JSON numbers. Every account entry
uses the Organizations `State` value; the retired `Status` field is never read or stored.
Classification: **absent upstream, compatible** (`02` generated-identifier invariant, `06`, T16
d12). Rejected: a minimal alias/id/state schema (OU, tag, and provenance checks unverifiable).

### Decision 5 — Exhaustive field-authority table and the Regions boundary

| Field | Class | Verification source |
|---|---|---|
| `snapshot_id` (envelope) | derived | recomputed SHA-256 of RFC 8785 `body`; must equal key, metadata, sidecar |
| `body` | container | — |
| `body.schema_version` | authoritative (contract) | must equal the version T14 validates |
| `body.kind` | authoritative (contract) | must equal `lab-binding-snapshot` |
| `body.supersedes` | informational | must name an existing retained snapshot or be null |
| `body.fixture.path` | informational | repository path at `source_commit` |
| `body.fixture.digest` | derived | SHA-256 of the committed fixture-file bytes at `source_commit` |
| `body.fixture.source_commit` | authoritative (binding) | git commit on `main` containing the fixture |
| `body.discovered_at` | informational | producer clock; used only for the freshness backstop |
| `body.producer.identity_type` | informational | STS `GetCallerIdentity` ARN class (`user/` vs `assumed-role/`); value never stores the ARN |
| `body.producer.account_alias` | derived | caller account ID mapped to its fixture alias |
| `body.organization.organization_id` | authoritative (binding) | `DescribeOrganization` |
| `body.organization.feature_set` | informational | `DescribeOrganization` |
| `body.organization.root_id` | authoritative (binding) | `ListRoots` |
| `body.organization.management_account_alias` | derived | `DescribeOrganization` management account ID mapped to its alias |
| `body.identity_center.instance_arn` | authoritative (binding) | `sso-admin:ListInstances` / `DescribeInstance` |
| `body.identity_center.identity_store_id` | authoritative (binding) | `sso-admin:ListInstances` |
| `body.identity_center.region` | informational (projection) | must equal `instance.yml` `primary_region`; `instance.yml` is the regional authority |
| `body.identity_center.delegated_admin_alias` | derived | `ListDelegatedAdministrators --service-principal sso.amazonaws.com` mapped to its alias |
| `body.accounts[].alias` | authoritative (binding) | committed fixture |
| `body.accounts[].live_name` | authoritative (binding) | `ListAccounts` `Name`, byte-equal |
| `body.accounts[].account_id` | authoritative (binding) | `ListAccounts` `Id` |
| `body.accounts[].state` | authoritative (binding, at discovery) | `ListAccounts` `State`; must be `ACTIVE` for bound accounts |
| `body.accounts[].joined_method` | informational | `ListAccounts` `JoinedMethod` |
| `body.accounts[].joined_timestamp` | informational | `ListAccounts` `JoinedTimestamp` |
| `body.accounts[].ou.ou_id` | authoritative (binding) | `ListParents` single parent; `DescribeOrganizationalUnit` |
| `body.accounts[].ou.logical_class` | derived | T16 decision 9 mapping of `ou_id` |
| `body.accounts[].ou.path` | informational | `ListAccounts` `Paths[0]`; never public |
| `body.accounts[].tags_verified` | derived | `ListTagsForResource` equals the T16 decision 16 tag set |
| `body.accounts[].binding` (`unbound`) | authoritative (contract) | present only for `status: requested` aliases; no other field permitted on that entry |
| root e-mail, credentials, tokens, payment data, account ARNs other than the instance ARN, user names, `Status` | prohibited | must not appear; presence is `INV-PROHIBITED-FIELD` |

**Regions boundary:** T09's binding projection covers Organization/account/OU identity and
Identity Center prerequisite identity only. T15 `instance.yml` remains authoritative for the
regional configuration consumed by this repository. If the future `aws-organization-governance`
publication contains `enabled_regions`, this consumer may verify it for compatibility but must
not import it as a second regional authority or override `instance.yml`. This lab snapshot does
not own enabled-Region configuration. Classification: **compatible** (`02`, `03`, RD-03, RD-06,
T15 d3/d9/d12). Rejected: treating `live_name` as informational (rename detection lost).

### Decision 6 — Canonical serialization and digests
Body canonicalization is **RFC 8785** (recursively sorted keys, no inter-token whitespace,
ECMAScript number serialization, UTF-8, I-JSON constraints); the digest is **SHA-256**, lowercase
hex. `snapshot_id` is computed over `body` only and stored in the envelope, the object key, the
S3 metadata, and the `.sha256` sidecar — never inside `body`. The fixture digest is SHA-256 over
the exact committed fixture-file bytes (git blob bytes are its canonical form). Classification:
**absent upstream, compatible** (T06 d4 digest binding). Rejected: YAML-based canonicalization
(no standard); git blob SHA for binding (SHA-1).

### Decision 7 — Encryption at rest and in transit
At rest: the existing bucket's SSE-KMS customer-managed key default (no new key; KMS data-plane
only, per T15 d6). In transit: TLS required by the clients (CLI/SDK HTTPS); `aws:SecureTransport`
bucket-policy enforcement is a substrate change outside pipeline authority and is recorded as a
separately authorizable hardening, not assumed. No client-side second encryption layer and no
second binding location. Classification: **compatible** (`09`, T15 d7/d9/d12). Rejected:
additional envelope encryption with the plan-encryption key (second key-custody path).

### Decision 8 — Storage paths and separation from state
Objects: `aws-identity-access/evidence/binding/<fixture-digest>/<snapshot_id>.json`, its
`<snapshot_id>.sha256` sidecar, and `aws-identity-access/evidence/binding/<fixture-digest>/current`
(the pointer; contents: fixture digest and snapshot ID only, plus an informational update
timestamp if required). Terraform state and lockfiles stay exclusively under
`aws-identity-access/lab/<root>/`; no cross-prefix copies. Classification: **inherited** (T15
d12/d16, T16 d12). Rejected: a single mutable `binding.json`.

### Decision 9 — Identity, immutability, supersession, replay, and the pointer compare-and-swap protocol
Snapshot objects are content-addressed and **write-once**; supersession creates a new object and
updates the pointer; superseded objects remain retained (decision 20). Conditional writes for
every object:

| Object | Write rule |
|---|---|
| Snapshot envelope | `PutObject` with `If-None-Match: *` |
| `.sha256` sidecar | `PutObject` with `If-None-Match: *` |
| Initial `current` pointer | `PutObject` with `If-None-Match: *` |
| Replacement `current` pointer | `GetObject` the current pointer and its ETag, then `PutObject` with `If-Match: <observed-etag>` |

A `409`, `412`, unexpected missing pointer, or ETag change is fail-closed; **never retry as an
unconditional overwrite**. The producer reads the pointer before and after candidate verification
and confirms the expected ETag before publication. Plan reads `current`, fetches and verifies the
snapshot, and confirms `current` did not change during verification. Apply requires that
`current` still names the exact snapshot bound into the saved plan (anti-replay). Pipeline roles
have no evidence-object Delete permission. S3 Object Lock remains an optional later hardening
(bucket versioning/lock configuration — a separately authorized substrate change).
Classification: **absent upstream, compatible** (`09`, T06 d4, T15 d6/d11). Rejected: a mutable
object relying on bucket versioning.

### Decision 10 — Freshness and stale/missing behavior
No calendar-based trust: **every plan and every apply re-verifies the snapshot against live
Organizations and Identity Center state** (decisions 11, 13); divergence fails closed. Backstop
maximum age for consumption without a new Stage 6.1 re-discovery: **90 days** from
`discovered_at`. A missing snapshot, missing pointer, digest mismatch, or expired snapshot is a
fail-closed error, never a deferral. Classification: **absent upstream, compatible** (`02`
validation rule 3, RD-08, T06 d4). Rejected: 30-day maximum (excess ceremony); no maximum
(weaker provenance discipline).

### Decision 11 — Uniqueness and state checks
At plan and apply: (1) every `active` fixture alias has exactly one binding; (2) each
`account_id` and each `live_name` appears at most once in the snapshot; (3) `ListAccounts`,
paginated until `NextToken` is null, contains exactly one account with that `account_id`, whose
`Name` equals `live_name` byte-for-byte and whose **`State` is `ACTIVE`** (`PENDING_ACTIVATION`,
`SUSPENDED`, `PENDING_CLOSURE`, `CLOSED` all fail); (4) any unaliased live account discovered in
the governed lab OU is `INV-UNALIASED` (never a permissive fallback). The `Status` field is never
read. Classification: **inherited** (RD-06, T06 handoff, T15 d5); the `State` rule
**compatible** (AWS retirement of `Status`, 2026-09-09). Rejected: match by name only.

### Decision 12 — Requested-fixture behavior
`lab-requested` must remain unbound and must have no live fields. No AWS alias tag exists. Any
unaliased live account discovered in the governed lab OU is handled by decision 11 as
`INV-UNALIASED`; it is never assumed to represent `lab-requested`. Validation passes with
severity **deferred**; the applicable plan omits every resource targeting it; the T20 summary
lists it as deferred; no Organizations mutation ever targets it. Classification: **inherited**
(RD-08, `06`, T03 d5, T16 d8). Rejected: omitting it from the snapshot (deferred-by-design
indistinguishable from absent).

### Decision 13 — OU verification without exposing paths
The snapshot records `ou_id` and the `Paths` element; verification calls `ListParents` (single
parent) and `DescribeOrganizationalUnit` per bound account and requires equality with `ou_id`
and the T16 decision-9 logical class (`root` for `lab-management`, `lab` for the three members).
Public outputs show only `logical_class`; OU identity never enters assignment keys, filenames,
or plan summaries. Classification: **inherited** (`02` path rule, RD-06, T03 d5, T16 d9).
Rejected: verification by OU name (mutable).

### Decision 14 — Producer authentication and least privilege
Lab producer identity = the named lab profile (an IAM user in `lab-tooling`, long-lived keys —
recorded honestly as reduced lab assurance under T15 d9's named-profile allowance). Required
reads: `organizations:DescribeOrganization, ListRoots, ListOrganizationalUnitsForParent,
DescribeOrganizationalUnit, ListAccounts, ListAccountsForParent, ListParents, DescribeAccount,
ListTagsForResource, ListDelegatedAdministrators` (service-scoped to
`sso.amazonaws.com`; a delegated-administrator registration for any other service is not
accepted); `sso-admin:ListInstances, DescribeInstance, ListPermissionSets,
DescribePermissionSet`; `identitystore:ListGroups`. Stage 6.3 publication: conditional
`s3:PutObject` and `s3:GetObject` on the binding prefix only (compare-and-swap needs the read),
plus the KMS data-plane operations the bucket key requires. The final implementation must verify
the precise API/action set against the pinned AWS provider/CLI behavior rather than granting
wildcard read access. S6 hardening proposal: a dedicated read-only discovery role in `lab-tooling`
with exactly this policy (IAM mutation, separately authorized). Classification: **compatible**
(`08`, `09`, T15 d6/d9; Organizations caller rule). Rejected: discovery from the management
account.

### Decision 15 — Consumer authorization, stages, and the permission matrix

| Principal | Organizations / Identity Center / Identity Store | Binding prefix (S3) | Evidence runs prefix | Notes |
|---|---|---|---|---|
| Validation | none (no AWS identity) | none | none | never reads the snapshot |
| `plan-preview` (PR) | none | none | none | fixture aliases only |
| Plan role | the decision-14 read set (no writes) | `GetObject` | run-scoped `Put`/`Get` | live verification; passes snapshot to Terraform as a decoded, sensitive input variable, never a data source |
| Apply role | the same narrowly scoped read set (apply-time live verification) | `GetObject` | `Put`/`Get` | re-verifies `current` and live state before credentials are used for mutation |
| Stage 6 producer/publisher | the decision-14 read set | conditional `PutObject`, `GetObject` | none | no Delete; no Organizations writes |

Neither pipeline role receives Organizations writes; no role receives evidence-object Delete.
Classification: **compatible** (`09`, T06 d4, T15 d6/d15). Rejected: `aws_s3_object` data-source
consumption.

### Decision 16 — Binding set for the saved plan
Authorization binds: `fixture.digest`, `snapshot_id`, verification-record digest, source commit,
plan-file SHA-256, sanitized-summary digest, deployment scope (the exact alias set),
tool/provider pins, enforcement-evidence reference, environment, approver, and expiry (the T06 d4
list extended by the snapshot and verification digests). Classification: **inherited** (T06 d4,
T15 d15). Rejected: binding the fixture digest only.

### Decision 17 — Invalidation rules
Any change to the fixture, the `current` pointer, the live verification outcome, the source
commit, the pins, the inventory scope, or the enforcement evidence invalidates an approved saved
plan; a new plan is required. A new snapshot always requires a new plan; a new fixture always
requires a new snapshot. Classification: **inherited** (T06 d4, T15 d15). Rejected: refreshing an
approved plan by re-verification.

### Decision 18 — Event handling

| Event | Plan/apply behavior | Recovery |
|---|---|---|
| Account `State` ≠ `ACTIVE` (pending activation, suspended, pending closure, closed) | fail closed (`INV-STATE`) | Eric disposition; new snapshot after the state changes |
| Account moved OU (`ListParents` ≠ `ou_id`) | fail closed (`INV-OU`) | Stage 6.1 re-discovery; new snapshot under separate authorization |
| Live `Name` ≠ `live_name` (rename) | fail closed (`INV-RENAME`; names are immutable once active — OD-12 governs renames) | governed rename decision; new fixture and snapshot |
| Duplicate binding, duplicate live name or id | fail closed (`INV-DUP`) | corrected snapshot via re-discovery |
| Unaliased account in the lab OU | fail closed (`INV-UNALIASED`) | fixture decision (alias or remove) |
| Pagination incomplete, API error, throttling | fail closed (`INV-PARTIAL`); retry within the run only | rerun |
| `lab-requested` bound or carrying live fields | fail closed (`INV-PROHIBITED-FIELD`) | remediation |
| Organization ID, root ID, management-account alias, Identity Center instance ARN, identity-store ID, delegated-administrator alias, or Region-authority mismatch | fail closed (`INV-BOUNDARY`) | re-discovery under separate authorization |
| `current` pointer changed during verification | fail closed (`INV-STALE`) | rerun after the pointer settles |

Classification: **compatible** (`05` drift policy, I-6, OD-12, RD-08). Rejected: OU moves as
warnings.

### Decision 19 — Fail-closed versus deferred; stable error classes for T14
Deferred (pass with warning): only `INV-DEFERRED` (alias with `status: requested`). Fail closed:
`INV-ABSENT` (alias not in fixture), `INV-UNBOUND` (active alias without binding), `INV-STATE`,
`INV-RENAME`, `INV-OU`, `INV-DUP`, `INV-UNALIASED`, `INV-DIGEST` (fixture, snapshot, key,
metadata, or sidecar mismatch), `INV-STALE` (expired, superseded, or pointer changed),
`INV-MISSING` (no snapshot or pointer), `INV-PARTIAL`, `INV-PROHIBITED-FIELD` (e-mail,
credential, ARN, or live field where none is permitted), `INV-PUBLIC-LEAK` (live identifier in
public output), `INV-BOUNDARY` (any authoritative organization or Identity Center boundary
mismatch not assigned a more specific code, including organization ID, root ID,
management-account alias, Identity Center instance ARN, identity-store ID,
delegated-administrator alias, or Region-authority mismatch). T14 assigns the final codes and
severities. Classification: deferred semantics
**inherited** (RD-08, `02`); classes **absent upstream, compatible**. Rejected: `INV-STALE` as a
warning.

### Decision 20 — Audit evidence, public summaries, retention, disposition
Non-public: snapshots, sidecars, pointers, verification records, and the CloudTrail event
references for discovery reads. **Retained at least through the POC phase gate. No snapshot,
pointer, verification record, plan-binding evidence, or associated CloudTrail reference is
deleted automatically. Deletion or lifecycle configuration requires an explicit Eric disposition
after the applicable phase gate and after all dependent plans and investigations are closed.** A
superseded snapshot remains retained under the same rule. State-prefix retirement (T15 d11) does
not delete binding evidence. Public (workflow summaries, docs): aliases, counts, `snapshot_id`,
`fixture.digest`, `logical_class`, and "verified"/"deferred" states — never names, IDs, OU paths,
or account-identifying timestamps. Classification: **compatible** (T15 d11/d12, T06 d3/d4).
Rejected: a one-year lifecycle expiry (bucket configuration; may delete before disposition).

### Decision 21 — Cost boundary
Reuse only the existing encrypted bucket and customer-managed key; S3 requests and KMS data-plane
calls under the existing bucket key; no new service, trail, table, or key. Object Lock,
bucket-policy TLS enforcement, and lifecycle rules are optional hardenings deferred to separate
authorization, each recorded with its (zero or near-zero) cost effect before adoption.
Classification: **inherited** (T02 cost boundary, T15 d10/d12). Rejected: a dedicated evidence
bucket.

### Decision 22 — Stage 6.1 / 6.3 integration and the transient-data and public-log boundary
Stage 6.1 may produce a **transient candidate**, but it is not an authoritative or durable
snapshot. Prefer in-memory generation; if a temporary file is unavoidable, use a restricted
temporary location, never the repository, and remove it on completion or failure without
claiming forensic secure erasure. Stage 6.3, under separate authorization, publishes the
candidate write-once and sets `current` per decision 9; the first pipeline plan then re-verifies
it. **No authoritative or durable binding snapshot exists before the successful Stage 6.3
publication**; the candidate is discarded if 6.3 is not authorized.

Public-log boundary: no live identifier may enter command stdout, GitHub Actions logs,
annotations, job summaries, Terraform console output, or public artifacts; `TF_LOG` and
equivalent verbose provider logging are disabled in public workflows; the decoded snapshot
variable and every derived identifier are marked sensitive; the applicable Terraform plan is
never printed and is encrypted before upload; public `plan-preview` uses only aliases and never
reads the snapshot; only sanitized alias-based summaries are public. Classification:
**inherited** (T16 d11–d12, T15 d6/d12/d15). Rejected: uploading at 6.1.

### Decision 23 — Target-estate transport versus the lab exception; OD-21
Target: consume `aws-organization-governance`'s inventory as a **pinned immutable publication** —
the org repository's git commit SHA plus the SHA-256 of its RFC 8785 canonical inventory export —
bumped only by a governed pin-bump PR (RD-01 "bot proposes, never approves" pattern), with the
pin recorded in every plan and evidence record. **OD-21 proposal to carry upstream:** "Downstream
consumption of the organization inventory is pinned, with an auto-PR bump; tracking
(always-current) consumption is prohibited for Tier-0 consumers." The lab snapshot is the pinned
publication's stand-in; the consumer contract (alias → verified live identifiers, fail-closed
checks, digests in evidence) is identical in both. Classification: pinned model **absent upstream
(OD-21 open), compatible** with I-4, I-9, OD-22, RD-01, and the brief; the lab stand-in is a
**recorded lab-only exception**. Rejected: tracking consumption (unreproducible plans; silent
scope expansion — conflicts with T02).

### Decision 24 — Downstream handoffs and dependency effects
Handoffs (texts below) to T14 #19, T20 #22, T22 #21, and T19 #14; T21 #20 has no inventory
dependency and receives none. Closing #12 reduces T20 #22's open blockers from four to three
(#15, #20, #21) and T14 #19's from five to four (#15, #20, #21, #22); nothing becomes newly
unblocked; the next frontier in map order is T08 #13. Rejected: a T08 handoff (T08 decides the
register form, not content).

### Decision 25 — Claim classifications and upstream proposals
As recorded in the claim-resolution record: claims 1, 2, 4 inherited (with the lab binding
exception compatible); claim 3 compatible with the OD-21 proposal of decision 23 carried by Eric.
No amendment to `02` or `06`; the `State`-field rule is an informational note for the org
repository's future write-back tooling. Rejected: an `02` amendment naming RFC 8785
platform-wide (premature).

### Decision 26 — Durable record and publication sequence
This record at `docs/wayfinding/map-1/12-organization-inventory-transport-and-snapshot-contract.md`
with a README index line, published through the established fail-closed sequence (validate →
commit → push → verify immutable URL → resolution → handoffs → map line → round-trip → close #12
with assignee retained → dependency check → continuity replace/commit/push/verify). No JSON
Schema, fixture file, or implementation file is committed now (Pre-Baseline layout; T14 owns the
schema). Rejected: committing a snapshot JSON Schema now.

## Lab exception versus target transport (summary)

| Aspect | Target estate | Lab (recorded exception) |
|---|---|---|
| Producer | `aws-organization-governance` write-back flow | Stage 6.1 read-only discovery by the repository owner from `lab-tooling` |
| Publication | pinned git commit + canonical export digest | one content-addressed snapshot per fixture digest under the binding prefix |
| Bump | governed pin-bump PR | Stage 6.1/6.3 re-discovery and publication under separate authorization |
| Consumer contract | identical: alias → verified live identifiers; fail-closed checks; digests in evidence | identical |
| Regional authority | `instance.yml` (T15); `enabled_regions` verified for compatibility only | `instance.yml` (T15) |

## Downstream handoffs (proposals; posted after publication)

- **T14 #19:** snapshot envelope schema (decision 4) and field-authority table (decision 5);
  `State` rule; digest checks across key/envelope/metadata/sidecar; the decision-19 error
  classes including `INV-BOUNDARY`; **log/output leakage validation** — any live identifier in command output, Actions
  logs, annotations, job summaries, Terraform output, or public artifacts is `INV-PUBLIC-LEAK`.
- **T20 #22:** `snapshot_id`, `fixture.digest`, and verification-record digest in the plan
  summary and authorization binding (decision 16); deferred reporting for `lab-requested`;
  alias-only outputs; `plan-preview` never reads the snapshot; `TF_LOG`/verbose logging disabled
  in public workflows; sensitive marking of the decoded snapshot variable; the applicable plan
  never printed and encrypted before upload.
- **T22 #21:** identity-store and instance identifiers live only in the snapshot; prerequisite
  evidence references `snapshot_id`; `instance.yml` remains the regional authority;
  delegated-administrator verification is scoped to `sso.amazonaws.com`.
- **T19 #14:** target transport pin and the OD-21 proposal; OD-12 rename rule; retention and
  disposition rule (decision 20); producer/consumer permission matrix as S6 hardening input.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Verdict⟧ and ⟦G-Accept⟧; nothing in it authorizes an AWS call, S3 write,
evidence creation, GitHub configuration, or implementation.
