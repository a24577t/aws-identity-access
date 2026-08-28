# Slice-A engineering specification

Consolidation of the grill-approved, ⟦G-Verdict⟧-approved decision set into the
implementation contract S6 consumes (`to-tickets` reads §10 one-to-one). Produced under
`to-spec-repo-owner` in consolidation mode: nothing here reopens a decision; every
section cites its deciding record, and on any divergence the cited decision prevails.
This specification carries no authority header: T23 #23 decision 4 scopes the
normative-header rule to `docs/architecture/` and `docs/guides/`, and no accepted rule
requires specification frontmatter — its authority derives from the approved ⟦G-Accept⟧
record and this repository placement. Verdict conditions C-A/C-B/C-C are discharged in
§9, §9, and §7–§8. Nothing in this specification authorizes implementation before
⟦G-Accept⟧, and nothing in it advances the three open empirical conditions (§8.3).

## 1. Problem and solution

**Problem.** Durable AWS access must be governed as reviewable configuration with
deterministic validation, derived review, saved-plan-exact deployment, and honest
evidence — none of which exists yet as implementation.

**Solution.** Implement slice A exactly as decided: the `access/` requester surface and
its four governed file forms ([configuration contract](../architecture/configuration-contract.md)),
the 79-code validation contract (T14 #19), the governance registry and declarations
(T06 #8), the CI plan contract and PR classes (T20 #22), the lab deployment contract
(T15 #10) over the remediated T16 #11 topology, and the T09 #12 inventory consumption —
all under the accepted ADRs ([register](../adr/README.md)).

## 2. Actors and stories (condensed)

1. As a **requester**, I change only `access/` and get deterministic validation, derived
   review, an honest preview, and a deferred-not-invalid answer for requested accounts.
2. As a **reviewer**, I see the PR's derived classes, the sanitized preview, and — for
   the applicable plan — the digest-bound effective-access summary with per-control
   enforcement evidence.
3. As the **owner**, I approve exactly one saved plan for one scope and one attempt, and
   every gate fails closed.
4. As a **platform consumer**, I get alias-only public artifacts with zero live
   identifiers, ever.

## 3. Work areas (each cites its complete contract)

- **W1 Repository skeleton.** The eight roots and root README sections (ADR-0003;
  T04 #6 d1/d6). `access/` content: the five committed slice files — two permission sets
  (§9 keys), three assignments (T10 #15 d6) — plus `groups/lab-readers.yml` (T05 d2
  form; real key confirmed at Stage 5.2) and `configuration/instance.yml` without a
  `verification` block until first verification (T22 #21 d1).
- **W2 Schemas.** JSON Schemas under `schemas/` for the four requester forms, the
  fixture, the governance records, and the declaration kinds — implementing the
  [configuration contract](../architecture/configuration-contract.md) exactly (RD-04).
- **W3 Validator.** `src/` implementation of the T14 #19 catalogue: 79 codes, canonical
  triggering layers, stage attribution, hermetic validation boundary, harmonization
  rules, the finding-record contract with C14 total ordering and duplicate collapse, and
  the leak rule with its single ARN exemption.
- **W4 Fixtures.** `tests/fixtures/{valid,invalid/<CODE>}/` per T14 #19 d6: one
  deterministic negative fixture per active isolatable code; the two approved multi-code
  expectations (`{ASN-SHAPE, P-OOS-USER}`, `{ADM-CAPABLE, ADM-STANDING}`); synthetic
  clock-controlled plan/apply fixtures; the valid tree passing with zero findings.
- **W5 Governance registry and declarations.** `governance/ownership/{principals,
  review-classes}/` with the slice principals and classes; `governance/
  change-declarations/` schemas for the three kinds; routing table and fail-closed
  default (T06 #8 d2–d3, d5).
- **W6 CI and planning lifecycle.** Workflow files implementing `validate` +
  `plan-preview` checks, the post-merge `lab-plan` job, the `lab` environment
  consumption rule, the two-layer plan-effect classifier, the effective-access summary
  generator (one generator, two renderings), and the authorization binding (T15 #10 d15;
  T20 #22 d1–d5; T06 #8 d4) — authored with exactly the §8 accepted pins. Server-side
  activation of the control set is W-Act (§10 item 14a), separately authorized.
- **W7 Generated artifacts.** The three views, generated CODEOWNERS, the enforcement-
  evidence report, and the central generated-artifact manifest under the T20 #22 d6
  metadata contract — produced only at S6, never hand-authored.
- **W8 Infrastructure.** `infrastructure/` Terraform roots `bootstrap` and
  `identity-center` under the T15 #10 state/evidence-prefix, role, deny, and pin
  contract; deployed-name derivation `ialab-<key>`; the T16 #11 d11 staged lab
  remediation (Stages 0–6) remains **separately authorized per stage** and is sequenced
  by the [brownfield implementation plan](brownfield-implementation-plan.md) §1.
- **W9 Catalog data.** §7 below.

## 4. Deployment mode and evidence

Staged lab apply exactly as T02 #3 defines; three-tier evidence with alias-only public
artifacts (T15 #10 d12); binding snapshot consumption with fail-closed live
re-verification and the 90-day backstop (T09 #12); one plan / one scope / one attempt
with the fail-closed rerun rule (T20 #22 d4).

## 5. Testing decisions

External behavior only: the validator is tested through the fixture tree (expected
finding sets, never internals); the classifier through synthetic plan-JSON fixtures
covering every action class, both replace orders, `forget` patterns, and fail-closed
divergence; the generator through byte-determinism (identical inputs → identical bytes);
CI checks through the generated-vs-regenerated comparison. Prior art: the fixture
expectation-set pattern of T14 #19 d6. No test contacts AWS; no fixture is ever planned
against AWS, uploaded, or applied.

## 6. Out of scope (this specification)

Everything outside slice A (ADR-0004's absent surfaces and the Out-of-scope register of
map #1); the import rehearsal and target waves (the
[brownfield implementation plan](brownfield-implementation-plan.md); post-acceptance,
separately authorized); lab provisioning itself (T16 #11 d11 — separately authorized
remediation); everything the three open empirical conditions gate (§8.3).

## 7. S5-selected catalog data (verdict condition C-C; T14 #19 decision 5)

The two ADM action catalogs are repository-controlled, versioned, digest-pinned outputs
generated **only** from the exact raw AWS Service Reference Information (SRI) bytes
selected here — **accepted, durable specification inputs committed at
`governance/catalogs/sources/sri-20260828/`** (five JSON files plus their `SOURCES.md`
handling note), landing atomically in the ⟦G-Accept⟧ acceptance merge and available from
the repository alone. The first S6 catalog-production ticket (§10 item 6) consumes
exactly those committed paths, **verifies each file's §7.1 SHA-256 before any parse,
never consumes review staging, and never re-fetches**; a mismatch aborts generation
(fail closed). The input set is immutable — refreshing means a platform-change PR adding
a new dated `sources/sri-<YYYYMMDD>/` set, never overwriting this one. Retrieval
timestamps are evidence, never identity.

**7.1 Exact raw inputs (version string `sri-20260828`):**

| Input | Source URL | Retrieved (UTC) | Bytes | SHA-256 |
|---|---|---|---|---|
| service index | `https://servicereference.us-east-1.amazonaws.com/` | 2026-08-28T00:46:16Z | 70,396 | `7cfe03fdd10349530045f654d5dc2c9455a1506eaf7ba20ea4225901a96b2dda` |
| `iam` | `https://servicereference.us-east-1.amazonaws.com/v1/iam/iam.json` | 2026-08-28T00:46:43Z | 131,515 | `0cc573ce2dec7e2122845c45961e9fa3448ef76d364fb800db98292e0e3d6d61` |
| `sso` | `https://servicereference.us-east-1.amazonaws.com/v1/sso/sso.json` | 2026-08-28T00:46:43Z | 86,805 | `b950f51b6311417d035088e8092f96b0c4018c0572ee83bef668c94422282e7a` |
| `identitystore` | `https://servicereference.us-east-1.amazonaws.com/v1/identitystore/identitystore.json` | 2026-08-28T00:46:43Z | 22,020 | `fbb14245e33e72a636168c53b27d03f0584314991f14a5a2a2950edd309b98c8` |
| `sso-directory` | `https://servicereference.us-east-1.amazonaws.com/v1/sso-directory/sso-directory.json` | 2026-08-28T00:46:43Z | 20,299 | `c03548fa4533682f3953b9b0ab583dd612beff2134c1425aa3f390e25ef5f70b` |

A generation input whose bytes do not match its selected hash aborts generation (fail
closed).

**7.2 Service scope — actual IAM service prefixes present in the pinned index (T21 #20
decision 6):** included — `iam` (named by T21 rule 4); `sso` (the actual IAM prefix of
Identity Center administration; the SDK namespace `sso-admin` is not an IAM prefix — its
actions authorize as `sso:*`); `identitystore` (Identity Store); `sso-directory` (the
Identity Center directory mutation surface, within T21's Identity Store intent).
Excluded, with rationale recorded: `sso-oauth` and `identitystore-auth` (authentication
flows, no configuration mutation); `identity-sync` (organization-side sync
administration, outside T21's named scope); `signin`, `cognito-identity`,
`clouddirectory` (unrelated surfaces). Scope changes are platform-change PRs
regenerating from newly fetched, newly hashed SRI inputs.

**7.3 Deterministic transformation (no name heuristics):** every SRI action entry
carries `Annotations.Properties` booleans `IsList`, `IsPermissionManagement`,
`IsTaggingOnly`, `IsWrite` (verified present in the pinned bytes). An action is
**mutation** iff `IsWrite ∨ IsPermissionManagement ∨ IsTaggingOnly` — the Write,
Permissions management, and Tagging access classes; Read/List-class actions are
excluded; action names are never classified by prefix or phrase. An entry missing
`Annotations.Properties`, missing any of the four booleans, or carrying a non-boolean
value **aborts generation** naming the action — nothing is guessed.

**7.4 Generated artifacts:** `governance/catalogs/action-catalog.json` — per included
prefix, the complete sorted action-name list exactly as the pinned bytes spell them
(wildcard-expansion catalog, T21 rule 2; a wildcard whose prefix is outside the catalog
is an expansion inability → `ADM-CATALOG`, fail closed); and
`governance/catalogs/privileged-mutation-actions.json` — per included prefix, the
complete sorted mutation-action list per §7.3 (T21 rule 4's explicit versioned set).
Canonical form: UTF-8, LF, two-space indent, keys and arrays sorted
byte-lexicographically, no timestamps; a sidecar metadata record carries the §7.1 table,
the generator version, and `sri-20260828`. SHA-256 over the exact committed catalog
bytes is pinned in the validator's committed catalog reference; absence, mismatch,
unsupported schema, or expansion inability fails closed as `ADM-CATALOG`; updates only
via platform-change PR through this same contract. Detector rules 2/4 become executable
only when these files exist with matching digests (T14 #19 d5).

## 8. S5-selected environment pins (verdict condition C-C; T14 #19 decision 8)

**8.1 Toolchain pins (selected and fixed now; changes only via platform-change PR):**

| Pin | Value |
|---|---|
| Terraform | `1.15.7` exact (T15 #10 d13) |
| `hashicorp/aws` provider | `= 6.53.0`; committed `.terraform.lock.hcl` whose provider entry must carry `h1:eD0xCJQCp+iQQKpU/SpMk/pGRrkF16UUJAEMCXvWCWo=` (T21 #20 F2) |
| Validator execution container | `python:3.12.7-slim@sha256:60d9996b6a8a3689d36db740b49f4327be3be09a21122bd02fb8895abb38b50d` (immutable multi-arch index digest; CPython 3.12.7) |
| pip / pip-tools | `pip 24.2`; `pip-tools 7.4.1` |
| Direct dependencies | `PyYAML == 6.0.2`; `jsonschema == 4.23.0` |
| Dependency lock contract | `pip-compile --generate-hashes` over the committed `requirements.in` run **inside the pinned container**; installs only with `pip install --require-hashes -r requirements.txt`; the generated hash-locked `requirements.txt` is committed in the same PR as the first `src/` code and regenerating it is a platform-change PR |
| `actions/checkout` | `fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09` (v5.1.0) |
| `actions/upload-artifact` | `330a01c490aca151604b8cf639adc76d48f6c5d4` (v5.0.0) |
| `actions/download-artifact` | `634f93cb2916e3fdff6788551b99b062d0335ce0` (v5.0.0) |
| `aws-actions/configure-aws-credentials` | `61815dcd50bd041e203e49132bacad1fd04d2708` (v5.1.1) |
| Runner | `ubuntu-24.04` as **transport only** — deterministic execution occurs inside the digest-pinned container above, and every run records the actual runner-image identity in its evidence |

Workflow files reference every action exclusively by its full 40-hex SHA above (tag
recorded as a trailing comment); adding an action to this set is a platform-change PR.

**8.2 Reproducibility rule:** identical commands locally and in CI (both inside the
pinned container); no unpinned network installation; regeneration determinism is a CI
check (`GEN-DRIFT`).

**8.3 The three open empirical conditions (unchanged, binding):** provider execution
NOT RUN/BLOCKED on the authoring host and unverified until executed in the designated
lab-CI boundary; the pinned-provider `forget` representation unverified —
`state-removal-only` cannot activate (`CLS-REPRESENTATION` fails closed);
`change.importing.id` rendering/sensitivity/redaction OPEN — no rehearsal activity and no
dormant-class activation until it passes with empirical evidence. Nothing in this
specification advances them.

## 9. Verdict-condition ledger (C-A and C-B)

**C-A — canonical key replacement.** The illustrative T21 #20 specimen key
`identity-inventory-reader` (25 characters) exceeded the T05 #7 24-character
permission-set bound. The S5 replacement, applied consistently across this specification,
the guides, and every future fixture/example, is:

| Superseded illustrative key | Replacement (16 chars, T05-valid) |
|---|---|
| `identity-inventory-reader` | `inventory-reader` |

No T05 bound changed; the T21 record remains the byte-unchanged decision source, its key
explicitly illustrative; the policy content, description, and `session_duration` are
unchanged.

**C-B — citation-anchor corrections** (applied wherever this set translates the T14
record's anchors into stable citations; the T14 record itself stays byte-unchanged):

| T14 anchor as recorded | Correct source authority |
|---|---|
| "T16 d5" for the five-entry alias fixture and field set | T16 #11 decision 7 (fields per T15 #10 decision 5) |
| "T16 d5" for `class` vocabulary | T16 #11 decision 2 (classes per T15 #10 decision 1) |
| "T16 d5 (condition 3)" for requested-fixture deferral | T16 #11 decision 8 |
| "T19 d21" for the adoption-manifest schema (`ADO-MANIFEST`) | T19 #14 decision 5 (carried into the plan by d21 §3) |

At S6, catalogue citations additionally join the accepted ADR IDs (T08 #13 d11).

## 10. Work-item breakdown (consumed 1:1 by `to-tickets` at S6)

| # | Work item | Contract | Depends on |
|---|---|---|---|
| 1 | Repository skeleton, root README sections, `access/` slice files | §3 W1 | — |
| 2 | JSON Schemas for all governed forms | §3 W2 | 1 |
| 3 | Validator core + finding contract + severity/stage model | §3 W3 | 2 |
| 4 | Catalogue implementation: INV/PRQ/P-OOS/KEY/ASN/GOV/FIX/CFG/DOC families | §3 W3 | 3 |
| 5 | ADM detector (rules 1/3/5 executable; 2/4 data-blocked) + `ADM-CATALOG` | §3 W3, §7 | 3 |
| 6 | Catalog data production from the committed §7 sources (`governance/catalogs/sources/sri-20260828/`, hash-verified before parse; no review-staging consumption; no re-fetch) | §7 | 5 |
| 7 | Fixture tree (valid + per-code invalid) | §3 W4 | 4, 5 |
| 8 | Governance registry, routing, declaration schemas | §3 W5 | 2 |
| 9 | Plan-effect classifier (two layers) + `CLS-*` | §3 W6 | 3 |
| 10 | Effective-access generator (preview + summary) + `GEN-*` checks | §3 W6, W7 | 9 |
| 11 | CI workflow files (validate, plan-preview, lab-plan, lab consumption) using exactly the §8 pins | §3 W6, §8 | 3, 8, 9, 10 |
| 12 | Generated CODEOWNERS + views + manifest | §3 W7 | 8, 10 |
| 13 | Terraform roots + deployed-name derivation + role/deny model | §3 W8 | 1 |
| 14a | **Repository-side control activation** (ruleset, required checks, environments) — separately authorized; only after its referenced checks exist (item 11 merged) | T15 d15 | 11 |
| 14b | **AWS-side OIDC/bootstrap** (roles, trust policies, one-time bootstrap root apply) — separately authorized; only after its Terraform prerequisites exist (item 13) | T15 d15; document 09 | 13 |
| 15 | Lab remediation Stages 0–6 — each stage separately authorized | T16 d11; plan §1 | 14b |

**Sequencing rules (correction-4 reconciliation):** the §8 pins are selected and accepted
at S5; workflow files land in item 11 using exactly those pins; server-side GitHub
controls (item 14a) activate under separate authorization only once the checks they
require exist on `main`; AWS-side bootstrap (item 14b) is independently and separately
authorized when its Terraform prerequisites exist — 14a and 14b are **not** one atomic
dependency; **no Terraform apply may occur before the item-14a control set is active**
(T15 d15's planning lifecycle). **Temporary procedural interval, recorded explicitly:**
between the first implementation PR and item 14a's activation, `main` cannot yet require
the not-yet-existing status checks; during that interval every implementation PR is
covered procedurally under the recorded T15 d15 lab exception (PR/merge records and
validation evidence kept; no apply is possible — no roles, no controls, no environment).
Every item lands through the decision-gated implementation lifecycle (S7–S11) with the
Standards + Spec + Conformance review axes and the Quality Gate; no item claims the
empirical conditions closed.
