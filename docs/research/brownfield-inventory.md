# T18 research — brownfield current-state inventory and gap analysis (slice A)

- Ticket: [#5 — T18](https://github.com/a24577t/aws-identity-access/issues/5)
  (part of map [#1](https://github.com/a24577t/aws-identity-access/issues/1)); narrowed to slice A
  by the T03 revalidation comment on #5.
- Recorded: 2026-08-22
- Governing authority: aws_ami at the T01-pinned revision
  `5f3cb7163f468730fd2ceb5d565c90b0bfda6099` ([T01 research](aws-ami-provenance.md)). Immutable
  URL form for every path below:
  `https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/<path>`.
- Evidence sources (inspectable implementation evidence, **never architecture authority** — map
  #1 Notes, "Evidence, not authority — brownfield"):
  - **Scaffold** — `scaffolding/aws-identity-access/` (29 files, 29,524 bytes).
  - **Exploratory implementation** — `aws-identity-access/` (75 files, 128,971 bytes) including
    `REVIEW.md`.
- Slice A as resolved by [T03 #4](https://github.com/a24577t/aws-identity-access/issues/4):
  `instance.yml` as declaration/verification data; identity source and workforce groups as
  evidenced prerequisites; groups as references never created; exactly two permission sets
  (AWS-managed read-only; narrowly scoped embedded inline); GROUP-only assignments to two named
  active lab accounts plus one `status: requested` deferred assignment; explicit targeting and
  singular reconciliation ownership ([T02 #3](https://github.com/a24577t/aws-identity-access/issues/3));
  greenfield-only first slice with pre-existing resources protected.
- Method: every file in both trees was read from the local aws_ami clone at `HEAD ==
  5f3cb716…` via `git show <sha>:<path>` with line numbers; no AWS call was made; nothing in
  aws_ami was modified. `tools/validate.py` was **read, not executed** (no Python interpreter on
  the research host) — every statement about validator behaviour is a reading of the source,
  cited by line. Line references are `path:L<n>` or `:L<a>-<b>` at the pinned revision.

## 0. How to read the inventory

| Column | Meaning |
|---|---|
| Convention embodied | The design convention the component demonstrates — as evidence, not as a recommendation. |
| REVIEW disposition | What `aws-identity-access/REVIEW.md` says about it: **endorsed** (listed under "Normative interpretations", L6–18), **illustrative** (I-a…I-h, L20–31), **open Qn** (L33–114), **rejected** (Conflicts, L116–127, or fixed by the post-build review, L129–155), or **—** (not addressed). |
| Cites / visibly contradicts | Rule or decision identifiers the component itself cites (comment, docstring, README), and — only where the text is directly at odds with a governing document at the pinned revision or with a closed map decision (`T02`, `T03-d1…d6`) — what it visibly contradicts. Classification against the governing documents (inherited / compatible / absent / conflicting) is **T19's work**, not this inventory's. |
| Slice A relevance | **in-slice** (component maps onto a slice-A element), **beyond** (IAM users/roles/trust/fleet/StackSets/customer-managed policies — inventoried, gap analysis deferred beyond the first slice), or **platform** (tooling, docs, governance shared by any slice). |

Prefixes: `S/` = `scaffolding/aws-identity-access/`; `X/` = `aws-identity-access/` (exploratory).

## 1. Traceable inventory

### 1.1 Scaffold — `scaffolding/aws-identity-access/` (29 files)

| # | Path (`S/`) | Purpose | Convention embodied | REVIEW disposition | Cites / visibly contradicts | Evidence | Slice A |
|---|---|---|---|---|---|---|---|
| S01 | `README.md` | Scaffold navigation; "mirrors the future repository root; it migrates verbatim when the repository is created" | `configuration/` as the requester surface; `trust-profiles/`; `bootstrap/procedures/` at repository root; per-OU assignment directories | rejected (verbatim migration is refused by the intake brief; root `bootstrap/` relocated by the post-build review, REVIEW L146–147) | cites 00/01/02/03/05/07/10 (L8–11), RD-04 (L15), RD-06 (L20), RD-08 (L24), 03 (L25). Root `bootstrap/` (L51) visibly differs from 07's `identity-center/bootstrap/procedures` shape | `S/README.md:L6,L30-52` | platform |
| S02 | `CODEOWNERS` | Review authority by path | Strictest set on pipeline/schemas/defaults; security co-approval on trust-profiles, boundaries, identity-source, root `/bootstrap/`; per-OU delegation | — | cites 10 (L2) | `S/CODEOWNERS:L9-30` | platform |
| S03 | `.github/workflows/validate.yml` | CI stub — a single `echo` placeholder | Six intended checks listed as comments; no implementation | — | cites 10 (L3) | `S/.github/workflows/validate.yml:L15-22` | platform |
| S04 | `bootstrap/procedures/README.md` | Manual-control procedure index | "Manual does not mean unmanaged" five-part pattern; re-verify API coverage at each provider upgrade | endorsed pattern (REVIEW L17) | cites 07, OD-08 (L4, L17) | `S/bootstrap/procedures/README.md:L7-19` | in-slice (pattern for T22) |
| S05 | `configuration/defaults.yml` | Single-level defaults merge | Defaults layer; `PT4H` permission-set default; `excluded_role_patterns` incl. `stacksets-exec-*`; **uppercase** `PA-*` reserved namespace | open Q7 (defaults layer), Q4 / I-f (reserved namespace has no normative basis) | — | `S/configuration/defaults.yml:L5-28` | platform |
| S06 | `configuration/boundaries/enterprise-default.yml` | Default permission boundary | Allow `*` + narrow deny (4 actions) | rejected as written — post-build review widened the deny list (REVIEW L136–137) | — | `S/configuration/boundaries/enterprise-default.yml:L15-22` | beyond |
| S07 | `configuration/trust-profiles/cross-account-audit.yml` | Reusable cross-account trust profile | Trust by `source_accounts` **names** + `PrincipalTag` condition | rejected (Q6 resolved: trust is local per role; Conflict list) | cites RD-06 (L9) | `S/configuration/trust-profiles/cross-account-audit.yml:L6-12` | beyond |
| S08 | `configuration/trust-profiles/github-oidc.yml` | Reusable GitHub OIDC trust profile | Pinned subject pattern | rejected (Q6) | — | `S/configuration/trust-profiles/github-oidc.yml:L6-11` | beyond |
| S09 | `configuration/trust-profiles/workforce-saml.yml` | Reusable SAML trust profile with empty conditions | — | rejected (Q6) | — | `S/configuration/trust-profiles/workforce-saml.yml:L6-8` | beyond |
| S10 | `configuration/accounts/security-tooling/roles/security-audit.yml` | Enterprise audit role | `trust_profile: cross-account-audit` reference instead of a local trust policy; boundary/session/path inherited from defaults | rejected (Q6) | — | `S/configuration/accounts/security-tooling/roles/security-audit.yml:L6,L12` | beyond |
| S11 | `configuration/accounts/security-tooling/policies/security-audit-read.yml` | Customer-managed policy document | YAML policy document rendered at plan time | — | — | `S/configuration/accounts/security-tooling/policies/security-audit-read.yml:L6-15` | beyond |
| S12 | `configuration/accounts/legacy-billing/users/svc-legacy-billing.yml` | Exceptional IAM user | `groups:` listed **on the user** (bidirectional membership); no `permission_boundary`; no `approved_by` | rejected (Conflict 2; I-d); I-e (mandatory boundary) | — | `S/configuration/accounts/legacy-billing/users/svc-legacy-billing.yml:L13-14` | beyond |
| S13 | `configuration/accounts/legacy-billing/groups/legacy-billing-operators.yml` | Exceptional IAM group | `members:` on the group **and** on the user (bidirectional); no `approved_by` | rejected (Conflict 2); post-build "IAM groups lacked recorded approval" (REVIEW L148) | — | `S/configuration/accounts/legacy-billing/groups/legacy-billing-operators.yml:L9-13` | beyond |
| S14 | `configuration/identity-center/configuration/instance.yml` | Identity Center Regions | `primary_region` + `additional_regions` only | endorsed (RD-03, REVIEW L16) | cites 03 (L2) | `S/configuration/identity-center/configuration/instance.yml:L3-6` | in-slice |
| S15 | `configuration/identity-center/identity-source/desired-configuration.yml` | Identity-source desired state | 07's `desired-configuration` file name; `identity_source: external-saml`, provider, SCIM, MFA | endorsed pattern (REVIEW L17) | cites 07 (L4) | `S/configuration/identity-center/identity-source/desired-configuration.yml:L5-9` | beyond (identity-source desired configuration is Out of scope; the file *shape* is evidence for T22's prerequisite record) |
| S16 | `configuration/identity-center/identity-source/verification.yml` | Manual-control evidence record | `cadence_days: 90`; `last_verified`/`verified_by`/`evidence_ref` all `null`; `procedure` points to the root `bootstrap/` | endorsed pattern | cites OD-08 (L3) | `S/configuration/identity-center/identity-source/verification.yml:L4-9` | in-slice (evidence-record shape for T22) |
| S17 | `configuration/identity-center/permission-sets/platform-readonly.yml` | Read-only permission set | AWS-managed `ReadOnlyAccess` attachment only; session inherits defaults | — | — | `S/configuration/identity-center/permission-sets/platform-readonly.yml:L7-9` | in-slice (form 1) |
| S18 | `configuration/identity-center/assignments/security/security-tooling.yml` | Per-OU/per-account assignment file | One file per account holding an `assignments` list (aggregated grants); `principal: platform-engineers` with **no group registry** to resolve it | I-a (no group registry = unresolvable principal) | cites RD-06 (L2). Aggregated file shape is at odds with `T03-d5` (one assignment per file) | `S/configuration/identity-center/assignments/security/security-tooling.yml:L3-9` | in-slice (shape evidence) |
| S19 | `governance/runtime-mutations/session-revocation.yml` | Seed runtime-mutation contract (`status: draft`) | Contract fields incl. `reconciliation: terraform`; scope limited to `/enterprise/` roles | rejected scope (post-build widened to portal sessions, REVIEW L138–140) | cites OD-16 by convention (path) | `S/governance/runtime-mutations/session-revocation.yml:L5-27` | platform |
| S20 | `schemas/README.md` | Schema routing table | Routes `trust-profiles/`, `assignments.schema.yml` (plural), `group.schema.yml` = **IAM** group; canonical contract schema owned by org-governance | — | — | `S/schemas/README.md:L6-20` | platform |
| S21 | `schemas/assignments.schema.yml` | Assignment file schema | Requires `ou` + `account`; aggregated `assignments` array; USER principal requires `exception` block; `format: date` | — | cites RD-05 (L34), RD-06 (L20–21) | `S/schemas/assignments.schema.yml:L9-48` | in-slice (shape evidence) |
| S22 | `schemas/defaults.schema.yml` | Defaults schema | Structural exclusion of access-granting keys | open Q7 | — | `S/schemas/defaults.schema.yml:L4-6` | platform |
| S23 | `schemas/group.schema.yml` | **Exceptional IAM group** schema (no workforce-group schema exists in the scaffold) | `members` + `policies`; no `approved_by` | I-a (missing workforce-group construct) | — | `S/schemas/group.schema.yml:L3-7` | beyond |
| S24 | `schemas/permission-set.schema.yml` | Permission-set schema | `inline_policy` is a **string reference** "to a policy authored under an account policies/ dir"; unconstrained `managed_policies`; `customer_managed_policies`; `permission_boundary` | rejected (Conflict 1: cross-directory reference is unresolvable and semantically wrong; I-c) | — | `S/schemas/permission-set.schema.yml:L25-39` | in-slice (rejected form) |
| S25 | `schemas/policy.schema.yml` | Policy/boundary schema | Loose statement schema | — | — | `S/schemas/policy.schema.yml:L15-29` | beyond |
| S26 | `schemas/role.schema.yml` | Role schema | Requires `trust_profile`; "Raw trust documents are not permitted" | rejected (Q6 resolved; exploratory `role.schema.yml` L7 inverts it) | — | `S/schemas/role.schema.yml:L6,L15-17` | beyond |
| S27 | `schemas/trust-profile.schema.yml` | Trust-profile schema | Named reusable trust patterns; `source_accounts` by name | rejected (Q6) | cites RD-06 (L37) | `S/schemas/trust-profile.schema.yml:L4-7,L32-37` | beyond |
| S28 | `schemas/user.schema.yml` | IAM-user schema | `groups` on the user; no `permission_boundary`; no `approved_by`; `format: date` | rejected (Conflict 2); I-e | cites OD-11 (L26) | `S/schemas/user.schema.yml:L10,L32-34` | beyond |
| S29 | `tools/README.md` | Required-checks specification (7 checks), no code | `trust_profile` reference integrity; inventory resolution with "deferred, never invalid" | — | cites I-10 (L4), OD-21 (L14), RD-08 (L15) | `S/tools/README.md:L9-23` | platform |

### 1.2 Exploratory implementation — `aws-identity-access/` (75 files)

#### 1.2.1 Top level, docs, governance, inventory, CI

| # | Path (`X/`) | Purpose | Convention embodied | REVIEW disposition | Cites / visibly contradicts | Evidence | Slice A |
|---|---|---|---|---|---|---|---|
| X01 | `README.md` | Navigation; labels (normative interpretation / illustrative / open / external / non-deployable) | `configuration/` as requester surface; assignment files "hold N grants for one target" (aggregated carve-out); `_<label>` files for multi-account/OU scopes; `AWSReservedSSO_*` as outputs | self-described; I-b | cites RD-05/06/07/08 (L69–84). Aggregated assignment files and `_`-scoped files are at odds with `T03-d5` | `X/README.md:L3-6,L64-86` | platform |
| X02 | `REVIEW.md` | Design findings: 9 normative interpretations, 8 illustrative choices, Q1–Q14, 4 conflicts, post-build fixes, residual gaps | — | — | cites RD-03/04/05/06/07/08, I-4/I-5, 01/02/05/07, OD-02/05/08/11/16/21/23 | `X/REVIEW.md:L6-176` | platform |
| X03 | `docs/requesting-access.md` | Requester decision tree and lifecycle | CI reject list; `_`-prefixed multi-scope files; "deferred, never invalid" | — | cites RD-08 (L71) | `X/docs/requesting-access.md:L10-41,L60-71` | platform |
| X04 | `docs/federated-access.md` | Okta → portal walkthrough | `_ou-wide.yml` reaches every nonproduction account "now and later" | open Q2 | — | `X/docs/federated-access.md:L7-27,L44-45` | in-slice (shows the auto-expansion the slice excludes) |
| X05 | `docs/exceptional-iam-users.md` | IAM-user exception path | Mandatory field set; expiry fails CI | — | cites OD-11 (L46) | `X/docs/exceptional-iam-users.md:L23-32` | beyond |
| X06 | `docs/reviewer-guide.md` | Per-path CODEOWNER checklists | "Read the diff as an access statement"; `defaults.yml` grants by absence | — | — | `X/docs/reviewer-guide.md:L22-26,L30-47` | platform |
| X07 | `docs/boundaries-and-counterexamples.md` | Repository boundary counterexamples (`payments-deploy` absent by design) | Durable vs temporary; enterprise vs workload-local; outputs never represented | endorsed (01) | cites RD-07 (L15), OD-05 (L10), OD-10 (L36) | `X/docs/boundaries-and-counterexamples.md:L6-55` | platform |
| X08 | `docs/pr-scenarios.md` | Three PR scenarios (group grant; shared role; IAM user create/recertify) | One-PR atomicity; reviewer routing; rollback = revert | — | cites I-8 "atomicity rule" (L13) | `X/docs/pr-scenarios.md:L8-41` | in-slice (scenario 1 is the slice-A grant shape) |
| X09 | `CODEOWNERS` | Review authority | 3 team aliases (`identity-platform`, `security-engineering`, `sre-leads`); strictest set; per-OU delegation; `administrator.yml` and production paths gated | open Q13 (owner vocabulary vs aliases) | cites 10 (L2) | `X/CODEOWNERS:L6-47` | platform |
| X10 | `.github/workflows/validate.yml` | CI: `pip install pyyaml` (unpinned) then validator + tests on Python 3.12 | No pinned dependencies, no Dockerfile | — | — | `X/.github/workflows/validate.yml:L14-21` | platform |
| X11 | `.gitignore` | Python artefacts | — | — | — | `X/.gitignore:L1-2` | platform |
| X12 | `inventory/organization-inventory.fixture.yml` | **Labelled local fixture** standing in for the organization inventory (fake IDs); `consumption: tracking`; one `status: requested` account with `account_id: null` | Fixture labelling; the only file permitted to hold account IDs | I-h (tracking); open Q5/OD-21 | cites I-4, RD-06, OD-21, RD-08 (L4–8, L65) | `X/inventory/organization-inventory.fixture.yml:L1-17,L63-66` | in-slice (fixture pattern; T09 decides transport) |
| X13 | `governance/runtime-mutations/session-revocation.yml` | Draft runtime-mutation contract owned here, executed by aws-privileged-access; scope widened to `AWSReservedSSO_*` portal sessions; `reconciliation: terraform` | 05 contract fields | endorsed (I-5 / OD-16, REVIEW L18); post-build widened | cites I-5, OD-16 | `X/governance/runtime-mutations/session-revocation.yml:L4-33` | platform (evidence of the `reconciliation` field T02 claim 3 refines) |

#### 1.2.2 Exploratory — `configuration/identity-center/` (23 files)

| # | Path (`X/configuration/identity-center/`) | Purpose | Convention embodied | REVIEW disposition | Cites / visibly contradicts | Evidence | Slice A |
|---|---|---|---|---|---|---|---|
| X14 | `configuration/instance.yml` | Identity Center Regions | `primary_region` + `additional_regions` **only** — no enablement evidence, owner, or verification fields | endorsed (RD-03) | cites RD-03 (L1) | `…/configuration/instance.yml:L1-5` | in-slice |
| X15 | `identity-source/okta.yml` | Identity-source desired state (SAML/SCIM/MFA, console-only) | Records intent + integration metadata, never secrets; `group_naming_convention` | endorsed pattern (07) | — | `…/identity-source/okta.yml:L1-17` | beyond (Out of scope by T03-d2; shape evidence only) |
| X16 | `identity-source/verification.yml` | Evidence record for okta.yml | `cadence_days: 90`; `last_verified`, `verified_by`, `evidence_ref` all `null` — **never verified** | — | cites OD-08, OD-23 (L2) | `…/identity-source/verification.yml:L3-8` | in-slice (evidence-record shape; freshness gating absent) |
| X17 | `bootstrap/procedures/README.md` | Manual procedure index at 07's location; "Procedure documents are placeholders" | Five-part pattern; controls gaining API coverage leave the directory | post-build fix (REVIEW L146–147) | cites 07, OD-08, OD-23 | `…/bootstrap/procedures/README.md:L3-16` | in-slice (T22 input) |
| X18 | `groups/engineering.yml` | Workforce group **reference** ("Membership lives in Okta — never here") | `name` (= filename = Identity Center display name), `owner`, `source.{provider,group,sync}` | I-a (registry); open Q3 (no immutability rule) | — | `…/groups/engineering.yml:L1-9` | in-slice |
| X19 | `groups/cloud-admins.yml` | Group reference for the standing-administrator group | as X18 | I-a; Q14 context | — | `…/groups/cloud-admins.yml:L1-8` | in-slice (shape) / beyond (admin use) |
| X20 | `groups/finance-analysts.yml` | Group reference | as X18 | I-a | — | `…/groups/finance-analysts.yml:L1-8` | in-slice |
| X21 | `groups/platform-engineers.yml` | Group reference | as X18 | I-a | — | `…/groups/platform-engineers.yml:L1-8` | in-slice |
| X22 | `groups/security-analysts.yml` | Group reference | as X18 | I-a | — | `…/groups/security-analysts.yml:L1-8` | in-slice |
| X23 | `groups/sre-production.yml` | Group reference | as X18 | I-a | — | `…/groups/sre-production.yml:L1-8` | in-slice |
| X24 | `permission-sets/read-only.yml` | Read-only set | AWS-managed `ReadOnlyAccess` attachment only; session inherits `PT8H` from defaults | — | — | `…/permission-sets/read-only.yml:L1-8` | in-slice (**form 1 match**) |
| X25 | `permission-sets/developer.yml` | Non-production build set | `PowerUserAccess` **plus** an embedded inline **Deny** document | — | at odds with `T03-d4` (PowerUserAccess excluded from the slice) | `…/permission-sets/developer.yml:L8-22` | in-slice (inline-document shape evidence only) |
| X26 | `permission-sets/production-operator.yml` | Bounded operations set | `ReadOnlyAccess` + inline **Allow** document + `permission_boundary: production-operator-ceiling` (boundary deployed to every assigned account) + `PT1H` | — | — | `…/permission-sets/production-operator.yml:L10-27` | beyond (boundary on a permission set = account-local IAM prerequisite) |
| X27 | `permission-sets/administrator.yml` | Standing `AdministratorAccess` set | Standing admin in durable access; `PT1H` | open Q14 | open under T07 #9 | `…/permission-sets/administrator.yml:L1-10` | beyond (T07) |
| X28 | `permission-sets/billing.yml` | Billing job-function set (write authority) | AWS-managed job-function policy | post-build description fix (REVIEW L141–142) | — | `…/permission-sets/billing.yml:L1-10` | beyond (not in the two-set slice) |
| X29 | `permission-sets/security-audit.yml` | Audit-read set | AWS-managed `SecurityAudit`; `PT4H` | — | — | `…/permission-sets/security-audit.yml:L1-10` | beyond |
| X30 | `assignments/nonproduction/_ou-wide.yml` | **OU-scoped** assignment: every account in the OU, including accounts added later | `scope: ou`; auto-expanding grant | open Q2 ("most consequential open design question", L1–4); I-b | visibly contradicts `T02` claim 4 and `T03-d5` (no OU auto-expansion; no silent grant on account add/move) | `…/assignments/nonproduction/_ou-wide.yml:L1-16` | in-slice (the excluded shape) |
| X31 | `assignments/nonproduction/sandbox-data-science.yml` | **Deferred target**: `status: requested` account, file valid, deploy omitted until write-back | RD-08 live demonstration; grants `administrator` to `platform-engineers` | endorsed (RD-08, REVIEW L10–11) | cites RD-08 (L1). The grant is a standing administrator assignment — open under T07 #9 | `…/assignments/nonproduction/sandbox-data-science.yml:L1-13` | in-slice (**deferral match**; grant content beyond) |
| X32 | `assignments/production/_finance-reporting.yml` | Multi-account scope: same grant to an explicit account list in one file | `scope: accounts` + `accounts:` list; `_` prefix | I-b; open Q2 | aggregated single-file shape is at odds with `T03-d5` (two separate files) | `…/assignments/production/_finance-reporting.yml:L1-15` | in-slice (explicit-list evidence) |
| X33 | `assignments/production/production-payments.yml` | Per-account file, two GROUP grants | Aggregated grants per account; no `developer`/`administrator` in production | — | — | `…/assignments/production/production-payments.yml:L1-15` | in-slice (shape) |
| X34 | `assignments/production/production-fulfillment.yml` | Per-account file, two GROUP grants | as X33 | — | — | `…/assignments/production/production-fulfillment.yml:L1-13` | in-slice (shape) |
| X35 | `assignments/security/log-archive.yml` | Per-account file, one GROUP grant | — | — | — | `…/assignments/security/log-archive.yml:L1-9` | in-slice (shape) |
| X36 | `assignments/security/security-tooling.yml` | Per-account file: three GROUP grants incl. standing `administrator`, plus the **only USER-principal** grant with an `exception` block | RD-05 exception class enforced by schema | endorsed (RD-05, REVIEW L12) | cites RD-05 (L3). Standing administrator open under T07; USER principal is rejected by the selected-slice validation profile (`T03-d5`), not by the domain architecture | `…/assignments/security/security-tooling.yml:L18-33` | beyond (USER; admin) / in-slice (shape) |

#### 1.2.3 Exploratory — `configuration/accounts/`, `boundaries/`, `defaults.yml` (15 files)

| # | Path (`X/configuration/`) | Purpose | Convention embodied | REVIEW disposition | Cites / visibly contradicts | Evidence | Slice A |
|---|---|---|---|---|---|---|---|
| X37 | `defaults.yml` | Single-level defaults; exclusions; reserved namespace | `role_defaults` (boundary, 3600 s, `/enterprise/`), `permission_set_defaults.session_duration: PT8H`; `excluded_role_patterns` (5 patterns incl. `stacksets-exec-*`); lowercase `pa-*` reserved | open Q7 (layer not doc-authorized); Q4 (namespace needs a contract, not a defaults convention) | — | `…/defaults.yml:L8-34` | platform |
| X38 | `boundaries/enterprise-default.yml` | Default role boundary | Allow `*` + widened identity-mutation deny (post-build) | post-build fix (REVIEW L136–137) | — | `…/boundaries/enterprise-default.yml:L15-29` | beyond |
| X39 | `boundaries/elevation-ceiling.yml` | Durable ceiling consumed by aws-privileged-access | `DenyEscapeToDurableAccess` (post-build) | open Q12; post-build fix (REVIEW L134–135) | cites RD-07, OD-05 (L1–5) | `…/boundaries/elevation-ceiling.yml:L1-38` | beyond (Out of scope: boundaries/elevation ceiling) |
| X40 | `boundaries/production-operator-ceiling.yml` | Ceiling for the production-operator set | Boundary deployed to every assigned account as a deployment prerequisite | — | — | `…/boundaries/production-operator-ceiling.yml:L1-30` | beyond |
| X41 | `accounts/legacy-billing/users/svc-billing-export.yml` | Exceptional IAM user #1 (machine, keys, no console) | Mandatory owner/justification/approval/review/boundary; membership **not** listed on the user | endorsed (01) | — | `…/accounts/legacy-billing/users/svc-billing-export.yml:L6-21` | beyond |
| X42 | `accounts/legacy-billing/groups/legacy-billing-operators.yml` | Exceptional IAM group | `members` declared **group-side only**; `approved_by` required | I-d; post-build approval fix | — | `…/accounts/legacy-billing/groups/legacy-billing-operators.yml:L1-17` | beyond |
| X43 | `accounts/legacy-billing/policies/billing-export-writer.yml` | Narrow S3 write policy | Account-local customer-managed policy | — | — | `…/accounts/legacy-billing/policies/billing-export-writer.yml:L1-15` | beyond |
| X44 | `accounts/log-archive/roles/security-audit.yml` | Far side of a role-to-role pair | Complete inline `trust_policy` (`cross-account`, source by account **name** + role) | Q6 resolved (local trust) | — | `…/accounts/log-archive/roles/security-audit.yml:L8-20` | beyond |
| X45 | `accounts/log-archive/policies/security-audit-read.yml` | Evidence-bucket read policy | — | — | — | `…/accounts/log-archive/policies/security-audit-read.yml:L1-15` | beyond |
| X46 | `accounts/security-tooling/roles/evidence-collector.yml` | Service-principal trust (Lambda) | `trust_policy.type: service` | Q6 resolved | — | `…/accounts/security-tooling/roles/evidence-collector.yml:L8-15` | beyond |
| X47 | `accounts/security-tooling/roles/vendor-siem-reader.yml` | Third-party trust with ExternalId | `external_account_id` literal (exempt from the ID scan) + mandatory `external_id` | Q6 resolved | — | `…/accounts/security-tooling/roles/vendor-siem-reader.yml:L9-20` | beyond |
| X48 | `accounts/security-tooling/policies/evidence-collector-assume.yml` | Outbound AssumeRole by path convention | `aws:ResourceOrgID` condition on the account wildcard (post-build) | post-build fix (REVIEW L151–152) | — | `…/accounts/security-tooling/policies/evidence-collector-assume.yml:L7-18` | beyond |
| X49 | `accounts/security-tooling/users/assessor-pentest-2026.yml` | Exceptional IAM user #2 (human, console + hardware MFA) | `console_access: true` ⇒ `mfa` required | endorsed (01) | — | `…/accounts/security-tooling/users/assessor-pentest-2026.yml:L6-24` | beyond |
| X50 | `accounts/shared-services/roles/ci-deploy-broker.yml` | GitHub OIDC trust with pinned subjects; "shared-services has NO Identity Center assignments" | `trust_policy.type: oidc`, `subject_patterns` pinned to `main` of two repositories | Q6 resolved | — | `…/accounts/shared-services/roles/ci-deploy-broker.yml:L13-23` | beyond |
| X51 | `accounts/shared-services/policies/deploy-broker-assume.yml` | Assume workload-owned deploy roles by path | `/workload-deploy/*` convention + `aws:ResourceOrgID` | — | cites the 01 workload-local rule by convention | `…/accounts/shared-services/policies/deploy-broker-assume.yml:L1-17` | beyond |

#### 1.2.4 Exploratory — `schemas/` (12 files)

| # | Path (`X/schemas/`) | Purpose | Convention embodied | REVIEW disposition | Cites / visibly contradicts | Evidence | Slice A |
|---|---|---|---|---|---|---|---|
| X52 | `README.md` | Routing table (12 routes); runtime-mutation contracts validated upstream only | Schemas carry structural policy; resolution is the validator's | — | cites RD-05 (L25) | `X/schemas/README.md:L6-29` | platform |
| X53 | `assignment.schema.yml` | Assignment schema | `scope: account \| accounts \| ou`; aggregated `assignments` array (`minItems: 1`); USER ⇒ `exception` required; `additionalProperties: false` | I-b; RD-05 endorsed | cites RD-05 (L44), RD-06 (L24), Q2 (L8). `ou` scope is at odds with `T02` claim 4 / `T03-d5` | `X/schemas/assignment.schema.yml:L13-75` | in-slice (shape; `ou` scope excluded) |
| X54 | `defaults.schema.yml` | Defaults schema | Structural exclusion of access-granting keys | Q7 | — | `X/schemas/defaults.schema.yml:L3-39` | platform |
| X55 | `group.schema.yml` | **Workforce group reference** schema | "governed references … never membership"; `name` doubles as the Identity Center display name; `source.provider ∈ {okta, active-directory}`, `sync: scim` only | I-a; Q3 | — | `X/schemas/group.schema.yml:L3-33` | in-slice |
| X56 | `iam-group.schema.yml` | Exceptional IAM group schema | Group-side membership; `approved_by` required | I-d | — | `X/schemas/iam-group.schema.yml:L3-31` | beyond |
| X57 | `iam-user.schema.yml` | Exceptional IAM user schema | `permission_boundary` **required**; `console_access` ⇒ `mfa` | I-e | cites OD-11 (L41) | `X/schemas/iam-user.schema.yml:L12-20,L65-70` | beyond |
| X58 | `identity-source.schema.yml` | Identity-source desired-state schema | Never secrets/tokens/certificates; `configured_via: console` | — | cites 07 (L5) | `X/schemas/identity-source.schema.yml:L3-39` | beyond (shape evidence for T22) |
| X59 | `instance.schema.yml` | Instance schema | Regions only; Region membership in `enabled_regions` is a validator check | endorsed (RD-03) | cites RD-03 (L4) | `X/schemas/instance.schema.yml:L3-14` | in-slice |
| X60 | `permission-set.schema.yml` | Permission-set schema | `managed_policies` constrained to `arn:aws:iam::aws:policy/`; `inline_policy` is an **embedded document** ("Never a cross-directory reference"); `customer_managed_policies[].name` with per-account existence warning; `permission_boundary` reference; `relay_state` | I-c (inline document) | — | `X/schemas/permission-set.schema.yml:L26-74` | in-slice (forms 1–2) / beyond (customer-managed, boundary) |
| X61 | `policy.schema.yml` | Policy/boundary schema | Statement shape with `additionalProperties: false` | — | — | `X/schemas/policy.schema.yml:L19-39` | beyond |
| X62 | `role.schema.yml` | Role schema | `trust_policy` required, complete, inline ("reusable trust references are rejected"); `permission_boundary: null` ⇒ `boundary_exception` | Q6 resolved | — | `X/schemas/role.schema.yml:L6-7,L19-80,L117-122` | beyond |
| X63 | `verification.schema.yml` | Manual-control verification record schema | `cadence_days`, nullable `last_verified`/`verified_by`/`evidence_ref`, `procedure` | — | cites OD-08, OD-23 (L5) | `X/schemas/verification.schema.yml:L3-17` | in-slice (evidence-record shape) |

#### 1.2.5 Exploratory — `tools/` and `examples/invalid/` (12 files)

| # | Path (`X/`) | Purpose | Convention embodied | REVIEW disposition | Cites / visibly contradicts | Evidence | Slice A |
|---|---|---|---|---|---|---|---|
| X64 | `tools/validate.py` | Validator: 16 codes (docstring L4–20); schema mini-evaluator; path routing; inventory resolution; reference integrity; reserved namespace; exclusions; expiry; ID scan; trust hygiene; duplicates; wide-policy | Fixture consumed from a hard-coded path (L155–156); `W-INV-DEFERRED` never says "invalid" (L180–183); expiry vs `date.today()` (L36, L190); `E-DUP` detects duplicates **within one file only** (L275–292); `verification.yml` is schema-checked only — **no freshness check** (L124, L246–249); `customer_managed_policies` → `W-REF-CMP` warning (L326–332) | I-g (date normalisation); residual gaps (REVIEW L157–168) | cites RD-06 (L15), RD-08 (L9, L23) | `X/tools/validate.py:L4-24,L155-163,L175-183,L255-295,L316-332` | platform |
| X65 | `tools/test_validate.py` | Executable proof: tree has zero errors + a deferred warning that never says "invalid"; 8 invalid specimens fail with their codes; schemas parse | `EXPECTED_INVALID` maps 8 files → 8 codes | — | — | `X/tools/test_validate.py:L18-27,L38-45` | platform |
| X66 | `tools/README.md` | Validator contract (9 ordered checks); known limitation (expiry fails the build, alerts the wrong person) | — | — | cites I-10, OD-19 (L3), RD-08 (L22), OD-11 (L40) | `X/tools/README.md:L14-40` | platform |
| X67 | `examples/invalid/README.md` | Specimen table (8 rows) | One violated rule per specimen | — | cites RD-05/06/08 | `X/examples/invalid/README.md:L8-17` | platform |
| X68 | `examples/invalid/…/assignments/production/payments-prod.yml` | Unknown inventory name → `E-INV-UNKNOWN` | — | — | cites RD-08 contrast (L3–4) | `X/examples/invalid/configuration/identity-center/assignments/production/payments-prod.yml:L1-12` | in-slice (specimen for T14) |
| X69 | `examples/invalid/…/assignments/security/security-tooling.yml` | USER principal without `exception` → `E-SCHEMA` | — | — | cites RD-05 (L2) | `X/examples/invalid/configuration/identity-center/assignments/security/security-tooling.yml:L1-12` | beyond (USER) |
| X70 | `examples/invalid/…/permission-sets/pa-emergency-admin.yml` | Reserved namespace → `E-NS-RESERVED` | Runtime ownership inferred from a name prefix | Q4 | at odds with the brief's "no reserved namespace as architecture" (brief = proposal, not authority) | `X/examples/invalid/configuration/identity-center/permission-sets/pa-emergency-admin.yml:L1-9` | platform |
| X71 | `examples/invalid/…/groups/data-team.yml` | Filename ≠ `name` → `E-NAME` | Path↔config agreement (02) | — | — | `X/examples/invalid/configuration/identity-center/groups/data-team.yml:L1-11` | in-slice (specimen for T14) |
| X72 | `examples/invalid/…/accounts/security-tooling/policies/evidence-restricted.yml` | Raw account ID → `E-ID-LITERAL` | RD-06 | — | cites RD-06 (L3) | `X/examples/invalid/configuration/accounts/security-tooling/policies/evidence-restricted.yml:L1-15` | platform (rule applies to any file) |
| X73 | `examples/invalid/…/accounts/shared-services/roles/rogue-admin.yml` | Wildcard-leading OIDC subject → `E-TRUST-WILDCARD` | — | — | — | `X/examples/invalid/configuration/accounts/shared-services/roles/rogue-admin.yml:L1-16` | beyond |
| X74 | `examples/invalid/…/accounts/legacy-billing/users/svc-old-integration.yml` | Expired `review_date` → `E-EXP-EXPIRED` | — | — | — | `X/examples/invalid/configuration/accounts/legacy-billing/users/svc-old-integration.yml:L1-17` | beyond |
| X75 | `examples/invalid/…/accounts/shared-services/policies/do-anything.yml` | Allow `*`/`*` outside boundaries → `E-POLICY-WIDE` | — | post-build addition (REVIEW L149–150) | — | `X/examples/invalid/configuration/accounts/shared-services/policies/do-anything.yml:L1-14` | beyond |

**Inventory count:** 29 scaffold + 75 exploratory = 104 files, all listed (S01–S29, X01–X75).

### 1.3 What exists in neither source (absences that matter to any slice)

| Absent component | Checked by | Consequence |
|---|---|---|
| Any Terraform, CloudFormation, or `infrastructure/` code | `git ls-tree -r` of both trees — no `*.tf`, `*.hcl`, template, or provider lock file | No evidence for deployment mechanics, state isolation, provider pinning, CV-07, StackSets, or reconciliation ownership beyond the `reconciliation:` contract field (X13) |
| A CI plan / effective-access-plan generator, PR classification, generated views | no code under `tools/` beyond the validator and its test | The T20 surface has no implementation evidence |
| A Dockerfile or pinned Python dependencies | `X/.github/workflows/validate.yml:L17` (`pip install pyyaml`, unpinned) | Reproducible-environment requirement has no evidence |
| A workforce-group schema in the scaffold | `S/schemas/` holds `group.schema.yml` for **IAM** groups only | Scaffold assignment principals are unresolvable (REVIEW I-a) |
| An inventory schema | REVIEW L164–165 | The fixture is CODEOWNERS-gated but unvalidated |
| Any fleet-role mechanism or StackSet definition | REVIEW Q1; `stacksets-exec-*` appears only as an exclusion pattern | Beyond the first slice (T13 Out of scope) |
| Any protected-resource or pre-existing-resource guard; any POC naming/prefix convention | no such file or validator check | Slice-A element "pre-existing protected" has no evidence |
| Any prerequisite-evidence gate on plan/apply | `validate.py` routes `verification.yml` to its schema only (L124); no freshness logic | Slice-A element "missing/stale evidence blocks plan/apply" has no evidence |
| Populated verification evidence | `X/configuration/identity-center/identity-source/verification.yml:L5-7` and `S/configuration/identity-center/identity-source/verification.yml:L6-8` are all `null` | No manual verification has ever been recorded in either source |

## 2. Gap analysis — slice A only

For each slice-A element (T03 #4): what the slice needs · what exists · which existing
components embody a **rejected** convention · what exists with **unknown basis** · the gap.
Dispositions (retain / adapt / replace / retire) are **not** proposed here — that is T19.

### 2.1 `instance.yml` as declaration-and-verification data (T03-d2; T22)

- **Needs:** intended instance characteristics, primary Region, enablement evidence, verification
  timestamp/cadence, responsible owner; never a lifecycle-ownership claim.
- **Exists:** X14 and S14 carry `primary_region` + `additional_regions` only; X59 validates
  Regions against `enabled_regions`. The *evidence-record* shape exists separately for the
  identity source (X16/S16, schema X63: `cadence_days`, `last_verified`, `verified_by`,
  `evidence_ref`, `procedure`).
- **Rejected convention present:** none.
- **Unknown basis:** `additional_regions` replication is asserted as a platform property
  (RD-03) but no evidence shows whether the lab instance is multi-Region; T15 records the fact.
- **Gap:** no enablement-evidence, owner, or verification fields on the instance record; the
  verification-record shape is never applied to the instance; no populated evidence anywhere.

### 2.2 Identity source and workforce groups as evidenced prerequisites (T03-d2/d3; T22)

- **Needs:** the lab identity source and every referenced group declared as prerequisites with
  evidence; missing or stale evidence blocks plan/apply.
- **Exists:** okta.yml (X15) + verification.yml (X16) + bootstrap procedure index (X17) model
  the identity source as desired state + evidence; `group.schema.yml` (X55) states membership
  lives in the IdP; the validator resolves a group principal only to the **existence of a file**
  (`X/tools/validate.py:L283-285`).
- **Rejected convention present:** none; but okta.yml-style *desired configuration* of the
  identity source is Out of scope for this map (T03-d2) — it is shape evidence, not a component
  the slice carries.
- **Unknown basis:** the `cadence_days: 90` value (X16:L4, S16:L5) has no cited source; OD-08 is
  open.
- **Gap:** no evidence record for group existence in the identity store; no freshness rule; no
  gate — `validate.py` never reads `last_verified` (routes X16 to schema only, L124; the
  `instance` branch at L246–249 is the only per-kind check near it). The evidence values are
  `null` in both sources.

### 2.3 Workforce groups as references, never created (T03-d3; T05)

- **Needs:** `groups/<key>.yml` with a stable key, source metadata, and the identity-store lookup
  name; plan resolves the group (data source) and fails if absent; no creation.
- **Exists:** six group-reference files (X18–X23) and their schema (X55): `name` = filename =
  Identity Center display name; `source.{provider, group, sync}`; `owner`. REVIEW endorses the
  registry (I-a) and records the missing immutability rule (Q3).
- **Rejected convention present:** none.
- **Unknown basis:** `sync: scim` is the only permitted value (X55:L33) — the lab's identity
  source may not be SCIM; no evidence either way.
- **Gap:** no separation of stable `key` from the mutable display/lookup name (the brief proposes
  `key` + `display_name`; T05 decides); no rename procedure; no Terraform lookup implementation
  (no Terraform exists at all — §1.3).

### 2.4 Exactly two permission sets (T03-d4; T21)

- **Needs:** (1) read-only via an AWS-managed attachment; (2) narrowly scoped embedded inline
  document; nothing else; customer-managed references rejected by the selected-slice
  validation profile.
- **Exists:** X24 `read-only.yml` matches form (1) exactly (S17 `platform-readonly.yml` is the
  same shape). The embedded inline-document shape exists in the schema (X60:L50-73) and in two
  files: X25 `developer.yml` (inline **Deny** on top of `PowerUserAccess`) and X26
  `production-operator.yml` (inline **Allow** plus `ReadOnlyAccess` plus a boundary). No file is
  an inline-only, narrowly scoped set.
- **Rejected convention present:** S24's `inline_policy` as a cross-directory string reference
  (REVIEW Conflict 1) — rejected and already inverted by X60.
- **Unknown basis:** `PT8H` default session duration (X37:L14) and `PT4H` (S05:L11) differ and
  cite nothing; T20 requires the effective value to be reported.
- **Gap:** a narrowly scoped inline-only set does not exist; X60 admits `customer_managed_policies`
  and `permission_boundary` with no mechanism to reject them for a slice (no validation-profile
  concept exists; `W-REF-CMP` is a warning, not a rejection — `X/tools/validate.py:L326-332`).

### 2.5 GROUP-only assignments to two named active accounts, one per file (T03-d5; T10)

- **Needs:** the same group→permission-set grant as two separate files under two named active
  lab accounts; the saved plan shows two distinct assignments; per-file natural key
  `account + principal + permission set`.
- **Exists:** per-account files (X33–X36, S18) keyed by account name with an **aggregated**
  `assignments` list; `_finance-reporting.yml` (X32) shows an explicit multi-account list in
  one file; schema X53 enforces GROUP/USER and path↔`ou`/`account` agreement; `E-DUP` catches a
  duplicate pair within one file only (`X/tools/validate.py:L289-292`).
- **Rejected convention present:** aggregated multi-grant files (brief; at odds with T03-d5);
  `scope: ou` auto-expansion (X30; at odds with T02 claim 4 / T03-d5); OU directory as part of
  the path (`assignments/<ou>/<account>.yml`, X53:L17-20) — at odds with the T10 narrowing (OU
  never enters the natural key or directory path).
- **Unknown basis:** the `_` filename prefix for non-account scopes (X01:L67-68) cites nothing.
- **Gap:** no one-assignment-per-file shape, no `<group>--<permission-set>.yml` naming, no
  cross-file duplicate detection, no `account-assignments/<account>/` layout without an OU
  segment.

### 2.6 One `status: requested` deferred assignment (T03-d5; T09/T16)

- **Needs:** an assignment referencing a `status: requested` inventory account that validates as
  deferred, is omitted from the executable plan, and whose account is never provisioned.
- **Exists:** the strongest evidence in either source — fixture entry with `account_id: null`
  (X12:L63-66), the assignment file (X31), the validator's `W-INV-DEFERRED` path that never says
  "invalid" (X64:L175-183), and the test asserting both the warning and its wording
  (X65:L42-45). The scaffold specifies the same behaviour in prose (S29:L13-16).
- **Rejected convention present:** X31 grants `administrator` to the deferred account — standing
  administrator access is open under T07 #9 and excluded from the slice's two sets; the
  *deferral mechanism* is separable from the grant content.
- **Unknown basis:** `consumption: tracking` (X12:L17) is self-labelled illustrative (I-h; OD-21
  open); T09 decides transport.
- **Gap:** no plan-level evidence of omission (no Terraform); the "never provisioned" rule is a
  lab-contract matter (T15/T16) with no evidence here.

### 2.7 Explicit targeting and singular reconciliation ownership (T02; T03-d5)

- **Needs:** every target explicit and visible in the saved plan; one reconciliation owner per
  resource; no OU/StackSet expansion for ordinary grants.
- **Exists:** explicit account lists (X32, X33–X36); the `reconciliation: terraform` contract
  field (X13:L30, S19:L24) as the only reconciliation-ownership metadata; `excluded_role_patterns`
  (X37:L22-27) as "never represented, never reconciled" name-pattern exclusions.
- **Rejected convention present:** `scope: ou` (X30) — auto-expanding, contradicts T02 claim 4;
  reconciliation/runtime ownership inferred from name patterns (`pa-*` reserved namespace
  X37:L32-34, `excluded_role_patterns`) — REVIEW Q4 itself says ownership should come from a
  dispositioned rule or contract, not a defaults convention; the brief rejects it as a proposal.
- **Unknown basis:** none beyond Q4.
- **Gap:** no reconciliation-owner declaration per resource; no plan; no StackSet evidence of any
  kind (StackSets are beyond the first slice in any case).

### 2.8 Greenfield-only first slice; pre-existing lab resources protected (T03-d6; T15)

- **Needs:** the slice creates only new, repository-named resources in its isolated state; a plan
  that creates, modifies, imports, or destroys a pre-existing Identity Center resource is
  rejected; a naming convention distinguishes POC-created resources.
- **Exists:** nothing directly. Nearest analogues: `excluded_role_patterns` (X37:L22-27) excludes
  AWS-generated principals from representation; `E-EXCL` (X64:L297-303) rejects configuration
  that names them.
- **Rejected convention present:** none.
- **Unknown basis:** none.
- **Gap:** no protected-resource list, no plan guard, no naming/prefix convention, no state
  isolation evidence (no backend configuration exists). T04 (naming) and T15 (protected
  resources) decide; the 09 import phase for pre-existing resources is T19's later rehearsal.

### 2.9 Summary table — slice A

| Slice-A element | Exists as reusable shape? | Rejected convention in the way? | Gap severity for the slice |
|---|---|---|---|
| 2.1 instance.yml declaration/verification | partial (Regions only; evidence-record shape exists elsewhere) | no | field set missing — T22 |
| 2.2 prerequisites evidenced; gate | partial (evidence record shape; all values null) | no (okta.yml desired config is out of scope, not rejected) | no freshness gate — T22/T14 |
| 2.3 groups as references | yes (X18–X23, X55) | no | key vs lookup name; no lookup code — T05 |
| 2.4 two permission sets | form 1 yes (X24); form 2 shape only (X60) | S24 cross-directory reference (already inverted) | narrow inline set absent; no profile rejection — T21/T14 |
| 2.5 per-file GROUP assignments, two accounts | shape partial (aggregated per-account files) | aggregated files; `scope: ou`; OU in path | file/key rule absent — T10/T04 |
| 2.6 deferred assignment | **yes** (X12, X31, X64, X65) | admin grant content only | plan-level omission unproven (no Terraform) |
| 2.7 explicit targeting; one owner | partial (explicit lists; `reconciliation` field) | `scope: ou`; ownership by name pattern | no per-resource owner declaration; no plan |
| 2.8 greenfield-only; protected | no | no | everything — T15/T04 |

## 3. Components beyond the first slice — inventoried, gap analysis deferred

Per #5's narrowing: these are listed with exact evidence pointers; their gaps are **beyond the
first slice** and their future architecture is **not decided here**.

| Component class | Scaffold evidence | Exploratory evidence | Rejected-convention evidence to preserve | Where it would be decided |
|---|---|---|---|---|
| Exceptional IAM users | S12, S28 | X41, X49, X57; specimen X74; doc X05 | S12/S28 bidirectional membership, no boundary, no approval (Conflict 2, I-d, I-e) | T11 closed Out of scope (#16); a later effort |
| Exceptional IAM groups | S13, S23 | X42, X56 | S13 bidirectional membership; S23 no `approved_by` | as above |
| Enterprise IAM roles | S10, S26 | X44, X46, X47, X50, X62; specimen X73 | S10/S26 `trust_profile` references; "raw trust documents are not permitted" (S26:L17) | T12 closed Out of scope (#17) |
| Reusable trust profiles | S07, S08, S09, S27 | none (inverted by X62:L7) | the whole `trust-profiles/` directory and schema | T12 (#17) |
| Customer-managed account policies | S11, S25 | X43, X45, X48, X51, X61; specimens X72, X75 | — | later effort |
| Permission boundaries / elevation ceiling | S06 | X38, X39, X40; `permission_boundary` on X26 | S06 narrow deny list (post-build widened) | Out of scope (boundaries / elevation-ceiling residency) |
| Customer-managed permission-set policies | S24:L25-33 | X60:L30-44 (`customer_managed_policies`), `W-REF-CMP` (X64:L326-332); **no example file uses it** | S24 cross-directory `inline_policy` (Conflict 1) | Out of scope; rejected by the selected-slice validation profile (T21) |
| Standing administrator permission set | — | X27, X19, X31 (deferred-account grant), X36:L18-21; CODEOWNERS X09:L27 | — (open Q14) | T07 #9 |
| USER-principal assignment | S21:L36-48 | X36:L22-33, X53:L50-64; specimen X69 | — (RD-05 exception class, endorsed) | rejected by the selected-slice validation profile (T10); class remains in the domain architecture |
| OU-scoped / multi-account aggregated assignments | — | X30 (`scope: ou`), X32 (`scope: accounts`), X53:L16 | X30 auto-expansion (Q2) | T10 (OU-expansion authoring input beyond this map) |
| Fleet roles | none | none (REVIEW Q1) | — | T13 closed Out of scope (#18) |
| StackSets | `stacksets-exec-*` exclusion (S05:L22) | same (X37:L27) | ownership by name pattern | T13 (#18); T02 rules bind any future mechanism |
| Runtime-mutation contract / `pa-*` namespace | S19, S05:L26-28 (`PA-*`) | X13, X37:L29-34, X70 | runtime ownership inferred from a reserved name (Q4) | T06 #8 (ownership metadata vs naming) |
| Defaults layer | S05, S22 | X37, X54 | — (open Q7; "access-granting fields never defaultable") | T04/T14 (whether a defaults layer exists in the POC) |
| Identity-source desired configuration | S15 | X15, X58 | — | Out of scope (T03-d2); T22 carries the prerequisite/evidence half |

## 4. Inspectable implementation evidence T19 can cite

Grouped by the convention it evidences; each item is a stable pointer at `5f3cb716…`.

1. **Deferred references (RD-08) working end to end:** X12:L63-66 · X31 · X64:L175-183 ·
   X65:L42-45.
2. **Group-reference registry shape:** X18–X23 · X55; the missing-immutability question Q3
   (`X/REVIEW.md:L48-52`).
3. **Permission-set forms:** AWS-managed attachment only — X24, S17; embedded inline document —
   X60:L50-73, X25:L10-22, X26:L14-27; the rejected cross-directory reference — S24:L37-39 and
   Conflict 1 (`X/REVIEW.md:L118-122`).
4. **Assignment file shapes:** per-account aggregated — X33–X36, S18; explicit multi-account
   list — X32; OU auto-expansion — X30 and Q2 (`X/REVIEW.md:L41-46`); USER exception — X36:L22-33,
   X53:L50-64.
5. **Manual-does-not-mean-unmanaged pattern:** S04, X17 (procedure index) · S15/X15 (desired
   state) · S16/X16 + X63 (evidence record, all values null).
6. **Instance record:** S14, X14, X59.
7. **Validator contract and its codes:** X64:L4-24 (16 codes) · X66 (9 ordered checks) · X67/X65
   (8 specimen-proven codes).
8. **Reconciliation-ownership metadata:** `reconciliation: terraform` — X13:L30, S19:L24;
   name-pattern exclusions — X37:L22-34, S05:L17-28.
9. **Local complete trust policies (rejected trust profiles):** X62:L19-80 vs S26/S27/S07–S09;
   Q6 resolution (`X/REVIEW.md:L64-68`).
10. **Group-side-only IAM membership vs bidirectional:** X42/X56 vs S12:L13-14, S13:L9-10, S28:L32-34.
11. **CODEOWNERS and owner vocabulary:** X09, S02; Q13 (`X/REVIEW.md:L100-108`).
12. **Counterexample and boundary documentation:** X07 (`payments-deploy` deliberately absent).
13. **CI and environment:** X10 (unpinned `pyyaml`), S03 (placeholder).

## 5. Uncertainty and missing evidence (recorded, not resolved)

1. **Validator not executed.** No Python interpreter was available on the research host; every
   behaviour statement about `validate.py`/`test_validate.py` is from reading the source. T19 or
   T14 should execute `python tools/test_validate.py` at the pinned revision before relying on
   the 8-specimen proof.
2. **REVIEW.md residual-gap list is internally inconsistent with the test.** `X/REVIEW.md:L159-161`
   lists `E-TRUST-WILDCARD` among the codes "not specimen-proven", but `X/tools/test_validate.py:L23`
   asserts `rogue-admin.yml → E-TRUST-WILDCARD` (X73). The unproven set, by reading, is
   `E-YML, E-REGION, E-REF, W-REF-CMP, E-EXCL, E-TRUST-SOURCE, E-DUP` plus `W-INV-DEFERRED`,
   which is proven by the tree test (X65:L42-43) rather than a specimen.
3. **No Terraform in either source** (§1.3): deployment, state isolation, provider pin, CV-07,
   plan omission of deferred targets, and reconciliation ownership have no implementation
   evidence; T15/T21 start from zero on these.
4. **Verification evidence never populated** (X16, S16): there is no record that any manual
   control was ever verified; the freshness rule T22 defines has no baseline.
5. **Lab state not inventoried.** No AWS call was made; which Identity Center resources, groups,
   or identity source exist in the `mcp_gateway01` lab is unknown to this inventory. T15/T16
   record those facts; the greenfield-only rule (T03-d6) means none of them enter the slice.
6. **Scaffold versus exploratory precedence.** The scaffold README claims verbatim migration
   (S01:L6); the exploratory README supersedes it for every shared component and REVIEW
   Conflict 1 recommends "retiring the scaffold in favor of this example" (`X/REVIEW.md:L121-122`).
   Both are evidence; neither is authority.
7. **Dates.** All valid-example `review_date` values are in 2027 (not expired at 2026-08-22); the
   validator compares against the run date (X64:L36), so the deployable tree's zero-error claim
   is date-dependent.

## 6. Sources

- aws_ami `5f3cb7163f468730fd2ceb5d565c90b0bfda6099` — `scaffolding/aws-identity-access/**` (29
  files) and `aws-identity-access/**` (75 files), read via `git show`; file list from
  `git ls-tree -r --name-only HEAD`.
- Governing documents at the same revision, cited by identifier only (not classified here):
  00 (I-4, I-5, I-8, I-10), 01, 02, 03, 05, 07, 09, 10, 11 (RD-03…RD-09, OD-02/05/08/11/16/19/21/23),
  12 (CV-07).
- Map decisions: [T02 #3](https://github.com/a24577t/aws-identity-access/issues/3) and
  [T03 #4](https://github.com/a24577t/aws-identity-access/issues/4) resolution comments; the T03
  narrowing comment on [#5](https://github.com/a24577t/aws-identity-access/issues/5).
- [T01 research](aws-ami-provenance.md) for the pin and the intake-brief provenance.
