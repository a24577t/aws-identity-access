---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 22
title: "T20 — CI plan contract and PR classes for slice A"
url: https://github.com/a24577t/aws-identity-access/issues/22
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-24
sources:
  decision_batch: "consolidated 8-question HITL batch (2026-08-24); collaborator corrections 1–10 plus three second-round fail-closed corrections applied throughout; decision direction approved by Eric; this record published only under Eric's separate hash-bound publication authorization"
  inherited_inputs:
    - https://github.com/a24577t/aws-identity-access/issues/22 (ten comments: T05 plan/view identity, T06 plan-contract inputs, T15 CI plan inputs, T16 plan inputs, T09 plan-contract inputs, T08 generated-view regime, T19 plan classes and redaction, T10 classification and summaries, T21 reporting and plan classes, T22 prerequisite gating, T23 generated metadata and scenarios)
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
---

# T20 — CI plan contract and PR classes for slice A

> Proposed discovery record — the complete durable result of T20 #22. Decisions approved by Eric
> as the human project owner and decision authority after collaborator review; executed by Claude
> in the repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`, using the
> batch-question directive (governing invariant 3 in the
> [repository-owner operating guide](../../../.ai/repository-owner/operating-guide.md)).
> **Nothing here is accepted architecture: every decision is a proposal until ⟦G-Verdict⟧ and
> ⟦G-Accept⟧.** GitHub issue #22 is the workflow/index surface and links to this record.

## Authorization scope of this record

Approving publication of this T20 result records the **proposed PR-classification and CI
plan contract only**. It authorizes no workflow, environment, ruleset, CODEOWNERS,
classifier, generator, or manifest implementation, no GitHub configuration, no AWS call or
mutation, no S3 or evidence creation, no Terraform execution against AWS, no backfill, no
tagging or release work, and no aws_ami edit. **Scope statement:** this classification and
enforcement contract governs implementation and change pull requests **after** ⟦G-Verdict⟧
and ⟦G-Accept⟧; it does **not** retroactively classify the Wayfinder discovery-record and
continuity closeout commits — including this record's own publication — as infrastructure
implementation PRs. Everything remains proposed pending ⟦G-Verdict⟧ and ⟦G-Accept⟧.

## Governing documents and evidence

Cited at the `aws_ami` revision pinned by T01 (#2): `09-tier0-execution.md` (an apply
executes the plan produced from reviewed code; plan artifacts are Tier-0 security assets),
`10-codeowners-model.md` (review authority expressible by path), RD-08 (deferred targets are
reported as "deferred", never "invalid"), `02-configuration-model.md` (validation
requirements). Inherited map decisions: T02 #3 (deployment mode), T03 #4 (slice), T04 #6
(layout; absent surfaces), T05 #7 (plan/view identity), T06 #8 (d1–d5: approval model,
registry, routing/enforcement evidence, apply authorization, change declarations), T09 #12
(d16/d17/d22: binding, invalidation, output boundary), T10 #15 (classification paths; alias
tuples; deferred reporting), T15 #10 (d6/d12/d13/d15: roles, tiers, pins, planning
lifecycle), T16 #11 (targets), T19 #14 (plan classes; rehearsal PR classes; redaction), T21
#20 (reporting; plan-action classes at the pin; CV-07 split disposition), T22 #21
(prerequisite gate; verification-update PR), T23 #23 (generated-metadata ownership;
`pr-scenarios.md` citations). Evidence (never authority): T21 F8 (empirical Terraform-core
plan-action classes at 1.15.7).

## Settled inputs (fixed by prior decisions; recorded, not re-decided)

- Planning lifecycle (T02, T15 d15): sanitized non-authoritative `plan-preview` on the PR;
  the applicable saved plan produced post-merge by the `lab-plan` environment job from the
  exact `main` commit; the `lab` environment consumes only that exact plan, commit, snapshot,
  and digests; any input change invalidates the authorization; apply never re-plans.
- Authorization binding (T06 d4 + T09 d16): plan-file SHA-256, source commit, artifact
  ID/digest, sanitized-summary digest, deployment scope, `snapshot_id`, `fixture.digest`,
  verification-record digest, state basis, pins, enforcement evidence, approver, environment,
  expiry.
- Review model (T06 d1–d3): derived review classes; set-union routing; per-class evidence
  (logical principal, physical identity, event, single class satisfied); duplicate identities
  across independent classes recorded as unenforced/lab-exception; uncovered paths fail
  closed.
- Exceptional changes (T06 d5): merged, expiring declarations with fixed expected plan-effect
  classes; declaration → declared change → terminal cleanup lifecycle; an exceptional-change
  PR is never an ordinary grant PR.
- Reporting boundary (T15 d12, T09 d22, T16, T10): alias-only public outputs; `lab-requested`
  reported deferred, never invalid; `plan-preview` never reads the snapshot; `TF_LOG` and
  verbose provider logging disabled in public workflows; the applicable plan encrypted and
  never printed.
- Permission-set reporting (T21): explicit effective `session_duration` always; policy form
  shown; `P-OOS-*` errors surface with out-of-slice wording; introduce plans are creates-only
  for the declared replacement set and its parallel assignments.
- Prerequisite gate (T22): runs at plan and apply before any mutation; public-safe
  verification-state reporting; the verification-update PR needs a T20 class.
- Generated regime (T23, T08 d10): `authority: generated` joins T20's metadata contract; no
  generated file is authored at S5.

## Claim-resolution record (grill-with-docs)

| # | Claim | Authority | Result | Upstream amendment / refinement |
|---|---|---|---|---|
| 1 | Changed-path classification distinguishes at least access-grant, access-definition, and platform-change; the IAM-exception/shared-role class is absent-for-slice | `10`, `02`, T03/T04, T06 d3, T10 d1 | **compatible** — the slice taxonomy adds the verification-update class and the exceptional-change **overlay** (not a plain path class) that the carried decisions require (decisions 1–2); the brief's class 3 has no slice content and is recorded absent-for-slice | none |
| 2 | The brief's ten-field effective-access plan is derivable from the saved Terraform plan plus governed configuration, with the T09 snapshot recorded | `09`, RD-08, T06 d4, T09 d16, T21, T22 | **compatible** — all ten fields derive for slice A (permission boundary as a recorded absent-for-slice constant; portal effect = deployed Name; deferral from inventory state), with the slice's binding fields added and the public/non-public identifier boundary stated precisely (decision 3) | none |
| 3 | Generated requester/account/principal views are non-authoritative, carry `do_not_edit: true`, and name their sources | brief (proposal); T04 d1, T08 d10, T23 | **compatible** — adopted through the format-neutral T20 generated-metadata contract (embedded envelope or digest-bound manifest; decision 6); production deferred to S6 | none |
| 4 | The effective-access plan and the saved Terraform plan apply consumes are the same reviewed artifact set — the human-readable plan never diverges from what is applied | `09`, T02, T06 d4, T15 d15 | **inherited** for the apply-exact-plan rule; the divergence-prevention mechanism (deterministic derivation from the exact plan bytes, summary-digest binding, and the fail-closed one-plan/one-attempt rerun rule) is this repository's **compatible** refinement (decision 4) | none |

## Decisions

Eric approved the **decision direction** — selections 1A–8A with the collaborator's
corrections 1–10 and the three second-round fail-closed corrections — applied throughout.
Publication of this record occurred only under Eric's separate, explicit hash-bound
publication authorization; decision approval and publication authorization are distinct
acts.

### Decision 1 — PR-class taxonomy, the exceptional-change overlay, and composition

Slice A recognizes six PR classes plus one recorded-but-dormant family:

1. **`access-grant`** — assignment changes only (the ordinary requester PR).
2. **`access-definition`** — group-reference and permission-set changes.
3. **`verification-update`** — the `instance.yml` prerequisite declaration/verification
   surface (the T22 `verified_at`/`snapshot_id` bump is its slice scenario).
4. **`exceptional-change`** — a **governed overlay/workflow, not a plain path class**, with
   three distinct PR phases:
   - **declaration PR** — changes only the declaration and its prerequisite
     documentary/control material;
   - **declared-change PR** — may begin only after the declaration is merged, and is
     classified from its **actual affected paths plus the exceptional-change overlay**;
   - **terminal cleanup PR** — removes the declaration only after terminal evidence
     satisfies the declared outcome.
   A path under `governance/change-declarations/**` identifies a declaration or cleanup PR;
   **that path alone never authorizes exceptional infrastructure effects**. A PR must not
   introduce a declaration and execute its exceptional change simultaneously (T06 d5's
   lifecycle made structural).
5. **`platform-change`** — control surfaces under the strictest review set (T06 d3), bounded
   by decision 5's mutation rule.
6. **`documentation`** — non-architecture documentation; validation-only; never
   plan-eligible.

The **T19 rehearsal family** (bundle-import, assignment-import, rollback, import-block
cleanup) is recorded in the taxonomy with T19's semantics but **dormant**: activatable only
under T19's separately authorized post-acceptance rehearsal and gated on the open
import-redaction verification (decision 7). The brief's IAM-exception/shared-role class is
**absent-for-slice** (no path, no content); the exceptional-change overlay is distinct from
it.

**Composition rule (every governed PR):** derive **all** applicable classes from the changed
paths and any valid exceptional overlay; required checks are the **union** of the classes'
checks; review controls are the **strictest applicable** set under T06's set-union routing;
permitted plan effects are those allowed by the **composition** of the matched classes
(decision 5). Fail closed on: an uncovered path; a contradictory combination; or a plan
effect **not attributable to an allowed changed surface** of a matched class. Prohibited
combinations (fail-closed): an exceptional change combined with any unrelated work; a
retirement combined with a new grant; a rehearsal-family PR combined with any other class.

Classification: **compatible** (claim 1; T06 d5, I-8 atomicity preserved — a new permission
set plus its assignments composes access-definition + access-grant in one PR). Rejected: the
brief's four classes alone (leaves carried PR shapes unclassifiable); single-class PRs only
(contradicts I-8); requester-declared classes (T06 d5 prohibits requester-weakened
approval).

### Decision 2 — Changed-path classification table

Classification is by changed path, evaluated per file:

| Path | Class |
|---|---|
| `access/identity-center/account-assignments/**` | access-grant |
| `access/identity-center/groups/**`, `access/identity-center/permission-sets/**` | access-definition |
| `access/identity-center/configuration/**` | verification-update |
| `governance/change-declarations/**` | exceptional-change (declaration/cleanup arm; never an effect authorization by itself) |
| `governance/**` (other), `schemas/**`, `infrastructure/**`, `src/**`, `tests/**`, `.github/**`, `.ai/**`, `.claude/**`, `CLAUDE.md`, `docs/architecture/**`, `docs/adr/**` | platform-change |
| `docs/**` (other: guides, research, wayfinding, agents, generated), `README.md`, `CONTEXT.md` | documentation |

`docs/adr/**` joins the strictest set by the same reasoning T06 applied to
`docs/architecture/**` (the register carries accepted decisions) — recorded as a
T06-consistent extension. A declared-change PR is identified by its merged declaration
(decision 1), never by path alone. Any file matching **no** row is a fail-closed
classification error. Files under absent-for-slice paths remain rejected by the slice
profile (T04 d6) independently of classification. Classification: **compatible**
(deterministic, enumerable, composing with T06 routing over the same paths). Rejected:
label/title classification (requester-authored); content-aware class assignment
(non-deterministic from paths; content rules stay in validation and the plan gate).

### Decision 3 — Effective-access plan: field contract and the identifier boundary

Per change row, the effective-access plan shows the brief's ten fields instantiated for
slice A:

1. **action** — the plan-effect classification per decision 5;
2. **principal** — the group key (T10 alias tuple);
3. **permission** — the permission-set key and policy form (the partition-qualified
   AWS-managed-policy reference or an inline-policy summary, per T21);
4. **target accounts** — account aliases; the two-account pair as two distinct rows;
5. **session duration** — always the explicit effective value (T21);
6. **permission boundary** — the constant `absent for slice A` (the field is kept so the
   brief's ten-field shape stays intact and honest);
7. **persistence/lifecycle** — `standing — until changed by governed PR`, or `deferred` for
   the `lab-requested` row;
8. **AWS access portal effect** — the derived deployed Name `<resource_name_prefix><key>`
   as the portal label; never a second identity (T05);
9. **required reviewers** — the full T06 shape: derived classes; per-class logical
   principal, physical reviewer identity, review event, and the single class satisfied;
   duplicates shown as unenforced/lab-exception, never independent satisfaction;
10. **deferred targets** — `lab-requested` reported **deferred**, never invalid (RD-08).

Plus the slice's binding fields, alias-only: prerequisite verification state (T22);
`snapshot_id`, `fixture.digest`, and the verification-record digest (T09 d16); the
Terraform/provider/lock pins (T15 d13); per-control enforcement-evidence results with
lab-exception references (T06 d3); and any `P-OOS-*`/`INV-*`/`PRQ-*` findings with their
established wording.

**Identifier boundary (public vs. non-public), stated precisely:**

- The saved Terraform plan, raw plan JSON, state-derived material, and non-public evidence
  **may contain provider-required identifiers**, handled under the repository's evidence
  rules (T15 d12 tier 2; T09).
- The **public effective-access summary must omit or replace every account-local,
  generated, or live identifier before serialization** — account IDs, GroupIds, principal
  IDs, instance and identity-store IDs, assignment IDs, generated role names, and generated
  or live ARNs.
- The **one permitted ARN-shaped public vocabulary** is the T21-approved
  partition-qualified AWS-managed-policy pattern (`arn:aws:iam::aws:policy/...`); this
  exception is never generalized to generated or account-local ARNs.
- Public display of a permission-set alias and its AWS-managed-policy attachment occurs
  only through the approved alias/configuration vocabulary.

Classification: **compatible** (claim 2). Rejected: dropping the permission-boundary field
(hides the absence instead of recording it); live identifiers in the summary (violates the
boundary above).

### Decision 4 — Production, binding, and the fail-closed rerun rule

Two renderings, one authority:

- The **sanitized `plan-preview`** on the PR: fixture-alias-only, never reads the snapshot,
  non-authoritative, **never apply-authoritative under any circumstance** (T15 d15, T09
  d15).
- The **authoritative effective-access summary**: generated **deterministically, in the
  same post-merge `lab-plan` job, from the exact applicable saved-plan bytes** (their JSON
  representation) plus governed configuration at the same commit and the pinned snapshot.
  Its digest is the sanitized-summary digest inside the authorization binding (T06 d4); the
  `lab` approver reviews exactly this artifact; apply consumes the same saved plan by
  immutable artifact ID and re-verifies every digest. One generator serves both renderings
  (preview mode: fixture-only inputs, no snapshot), so preview and summary semantics cannot
  drift. The summary is never hand-edited; divergence is prevented by deterministic
  derivation and detected by digest binding.

**Rerun/retry (fail-closed):** an apply authorization is bound to **exactly one immutable
saved plan and one attempt**. A failed, canceled, interrupted, or partially completed apply
may **not** reuse that plan. Any retry requires a fresh authoritative `lab-plan` run, a new
artifact and digest set, renewed review and authorization, and preservation of the prior
attempt's terminal evidence. An interrupted apply is presumed to have possibly changed
remote or stateful conditions; the fresh plan re-verifies live state before any further
mutation. Classification: **inherited** for apply-exact-plan (`09`, T02); the
divergence-prevention and rerun mechanics are **compatible** refinements (claim 4).
Rejected: pre-merge authoritative summaries (unbindable to the post-merge plan);
independent preview/summary generators (drift surface); plan reuse after a failed attempt
(replay surface T06 d4 already blocks, here made total).

### Decision 5 — Deterministic plan-effect classifier, the class matrix, revocation, and the platform bound

**Layer 1 — raw Terraform action classification (per managed resource, from plan JSON).**
Recognized action classes: `no-op`; `create`; `update`; `delete`; `replace` — accepting
**both** delete-then-create and create-then-delete action orders; and **`forget`** — the
plan-JSON action empirically demonstrated at Terraform-core `1.15.7` for a resource covered
by `removed { lifecycle { destroy = false } }` (T21 F8; builtin-provider offline runs) — a
**non-live-destruction state-removal primitive, distinct from `delete`**. `forget` rows are
**excluded from the live-mutation aggregate** (they mutate state only, never live AWS) and
are **never silently dropped**: they form the vector's own state-removal section. Read-only/
data-source refresh actions are reported in a separate read section of the summary and are
excluded from the mutation aggregate under this explicit deterministic rule — they are
listed, never silently dropped. **Any unknown or unsupported action list fails closed.
Classification that cannot be established because required values are sensitive or unknown
fails closed. If the pinned Terraform version emits any different or unsupported
representation for a removed-block resource, classification fails closed.**

**Aggregate classification** operates over the **complete normalized vector of
managed-resource effects** — never one label from a single resource. Live-mutation rows are
`create`/`update`/`delete`/`replace`; state-removal rows are `forget`. Classes: `empty`
(zero live-mutation rows and zero `forget` rows); `creates-only` (one or more creates, no
other live mutation, zero `forget` rows); `updates-only` and `deletes-only` (likewise);
`mixed` (any other combination of live-mutation rows, zero `forget` rows);
`state-removal-only` per Layer 2. **Any `forget` row outside the `state-removal-only`
pattern — combined with any live-mutation row, or lacking its exactly matching
`removed { destroy = false }` configuration — fails closed.**

**Layer 2 — contract-level workflow classes.** `imports-only`, `state-removal-only`, and
`guard-removal-no-live-change` are **not inferable from the action vector alone**; they are
contract-level classifications derived from the plan **together with** the changed
configuration/declaration and the applicable T19 markers. Classifier inputs, in precedence
order: (1) the normalized action vector; (2) plan-JSON import markers (`change.importing`);
(3) the changed configuration set (import blocks; `removed` blocks with
`lifecycle { destroy = false }`; guard-file changes); (4) the matched declaration, where the
overlay applies. A contract-level class applies only when its configuration marker **and**
its aggregate condition both hold — `imports-only`: every changed resource import-marked and
the mutation aggregate empty; `state-removal-only`: the **complete effect vector contains
only `forget` rows (at least one), zero live-mutation rows, and every `forget` row matches
one-to-one a `removed { lifecycle { destroy = false } }` block in the changed
configuration**; `guard-removal-no-live-change`: an empty aggregate with the guard
configuration removed. Any inconsistency between markers and the aggregate fails closed.
Fail-closed classification findings receive stable codes assigned by T14 (a `CLS-*` family
is proposed as input, not final code ownership).

**PR-class ↔ plan-class matrix:**

| PR class | Permitted plan effects |
|---|---|
| access-grant | `creates-only`; `deletes-only` where every delete corresponds exactly to a removed assignment file, carrying an **explicit access-revocation acknowledgement tied to the exact assignment entry and its expected delete effect**; `empty` (deferred-only changes) |
| access-definition | `creates-only`; `updates-only` (in-place description/session-duration/policy edits); composes with access-grant per decision 1; never `replace` or `deletes-only` outside the exceptional overlay |
| verification-update | `empty` only (`instance.yml` drives gating, never AWS resources) |
| exceptional-change (declared-change PR) | exactly the declared kind's fixed class (T06 d5): introduce `creates-only`; retire `deletes-only` with T06's destroy acknowledgement; group-key rename `empty` |
| platform-change | bounded rule below |
| documentation | not plan-eligible |
| T19 rehearsal family (dormant) | as T19 defines (`imports-only`, `empty`, `state-removal-only`, `guard-removal-no-live-change`, `deletes-only` cleanup); activatable only after the decision-7 gates close |

**Platform-change bound:** a platform-only change with no Terraform-managed AWS effect has
an **empty** plan. Any non-empty AWS effect must be **explicitly attributable to an
authorized in-scope change class and resource surface**; protected-resource replacement or
deletion remains prohibited unless the applicable exceptional workflow explicitly permits
it; **strict review never itself grants mutation authority**.

**Composition of aggregates:** in a composed PR, every mutation row must be attributable to
an allowed changed surface of one matched class; the plan is permitted iff every row is
attributable and every matched class's constraints hold. A composed PR is expected to
contain several resources with different primitive actions — no rule requires a single
primitive action per PR. The protected-resource guard (T15 d7) applies to every plan
regardless of class. Classification: **compatible** (T21 F8 is the empirical Terraform-core
basis; the AWS-provider rendering remains unverified until the first lab run — decision 7).
Rejected: single-label-per-plan classification (non-deterministic for composed PRs); generic
destroy acknowledgements (replaced by the exact-entry revocation acknowledgement); folding
revocation into the exceptional overlay (excess ceremony for the ordinary lifecycle);
"no fixed class" platform wording (unbounded).

### Decision 6 — Generated views and the format-neutral generated-metadata contract

The POC defines **three generated views** — requester view, account view, principal view —
derived only from `access/**`, the fixture, and the effective-access plan; **produced at S6**
(no generated file at S5, T23).

**Metadata contract (format-neutral; two valid forms; no self-referential digest).**

- **Central manifest — the uniform whole-file binding for every generated artifact.** A
  single generated-artifact manifest, itself a generated file at a fixed path in the
  generated subdirectory, binds each target's repository-relative path to its **whole-file
  SHA-256**. The manifest is outside every target it binds, so no digest is
  self-referential. The manifest carries no self-digest; its own integrity is established
  by deterministic regeneration and CI comparison.
- **Embedded-envelope form (documentation formats only).** Formats that support the
  envelope additionally embed it, **without any whole-target self-digest** (a whole-file
  digest embedded in the same file is self-referential and generally cannot be generated).
  If an embedded envelope ever carries a digest, it must name a precisely defined
  non-self-referential byte domain — such as the generated payload excluding the envelope —
  with an exact canonical extraction rule; **this option is not adopted for slice A**: the
  whole-file digest lives only in the manifest.
- **Control or machine formats** — `.github/CODEOWNERS` must remain valid CODEOWNERS
  syntax — carry no embedded envelope; their metadata lives in the manifest only.

Embedded-envelope schema (documentation formats):

```yaml
authority: generated
do_not_edit: true
generator:
  path: <repository-relative path>
  version: <pinned version or digest>
sources:
  - path: <repository-relative path>
    revision: <40-hex commit>
  - artifact: <stable artifact label>
    sha256: <64 lowercase hex>
target:
  path: <repository-relative path of this generated file>
```

Central-manifest entry schema (every generated artifact):

```yaml
- target:
    path: <repository-relative generated target>
    sha256: <64 lowercase hex — whole file>
  generator:
    path: <repository-relative path>
    version: <pinned version or digest>
  sources:
    - path: <repository-relative path>
      revision: <40-hex commit>
    - artifact: <stable artifact label>
      sha256: <64 lowercase hex>
```

Canonical ordering and serialization: fields exactly in the schema order above; manifest
entries sorted lexicographically by `target.path`; `sources` sorted lexicographically —
repository `path` entries first, then `artifact` entries by label; YAML, UTF-8, LF,
two-space indent, no flow style. Repository sources use an exact 40-hex commit;
external/non-repository inputs use an explicitly labeled digest algorithm. **No live
identifier may enter this public metadata.** Generation is deterministic — identical
sources and generator produce identical bytes; no wall-clock timestamp lives in generated
bytes (run timestamps belong to CI evidence) — so every artifact is verifiable through the
manifest's whole-file digests and, for envelope formats, by regeneration; hand edits are
rejected by CI comparison (an S6 check; the rule binds now).

Consistent application: the three views and any future ADR-shaped view (T08 d10) embed the
envelope **and** appear in the manifest; `.github/CODEOWNERS` and any other control/machine
format appear in the manifest only; the enforcement-evidence report embeds the envelope
where its format supports it and appears in the manifest regardless. Placement per T04 d1.
Classification: **compatible** (claim 3). Rejected: frontmatter in CODEOWNERS (invalid
syntax for its consumer); a whole-target self-digest inside its own file (self-referential;
generally not generable); timestamps in generated bytes (breaks reproducibility);
hand-authored S5 view examples (contradicts T23 and `do_not_edit`).

### Decision 7 — Public-output and redaction contract; two mandatory open gates

Consolidated public-output section of the plan contract: alias-only public outputs;
`plan-preview` sanitized, snapshot-blind, never apply-eligible; `TF_LOG` and verbose
provider logging disabled in public workflows; the decoded snapshot variable and every
derived identifier marked sensitive; the applicable plan encrypted and never printed;
import identifiers redacted from every public surface (preview, summaries, annotations,
diagnostics, generated artifacts — shared duty with T14); the decision-3 identifier
boundary applies to every public serialization. **Redaction must occur by omission or
replacement before public serialization; Terraform sensitivity markings alone are not
sufficient evidence of redaction.**

**Two mandatory unresolved gates — not editorial notes:**

1. **Provider-execution gate:** authoring-host execution of the pinned AWS provider remains
   NOT RUN/BLOCKED; lab-CI execution remains unverified **until executed in the designated
   lab-CI boundary**. T21's documentary PASS is not S6 execution readiness, and nothing in
   this record advances it.
2. **Import-redaction gate:** `change.importing.id` rendering, sensitivity, and redaction
   remain **unverified**; **no T19 rehearsal may begin until this gate passes with
   empirical evidence.** The dormant rehearsal PR classes stay dormant until then.

The `forget` representation and the `change.importing` markers, though empirically
demonstrated at Terraform-core `1.15.7` with the builtin provider (T21 F8), remain
unverified with the pinned AWS provider in the designated lab-CI boundary; **fixture/lab
verification of both representations is required before the dormant T19 rehearsal classes
activate.**

Classification: **inherited** (the carried output rules consolidated) with the
serialization-time redaction rule **compatible** (explicit strengthening). Rejected:
treating documentary CV-07 evidence as execution readiness; deferring the output contract
to T14 (T14 owns codes and validation, not the plan contract's boundary).

### Decision 8 — Durable record and publication sequence (hash-bound review-then-publish)

This record at `docs/wayfinding/map-1/22-ci-plan-contract-and-pr-classes-for-slice-a.md`
with a `docs/wayfinding/README.md` index line. Publication executes only after Eric reviews
the exact drafted bytes — the record, the whole README successor, the tracker-payload
bundle (resolution comment, close comment, map line, the T14 #19 handoff, and the
substitution instructions), and the continuity template, each bound by SHA-256 in the
review package — and gives consolidated approval; the fail-closed sequence below then runs
unchanged. The handoff goes **only to the open ticket T14 #19** (the sole remaining open
child) and adds no dependency edge. Closing #22 releases T14 #19's last open blocker: the
frontier becomes **T14 #19 (next claimable and final open child)**; after T14 resolves, the
frontier is empty and the map proceeds to S3 per the Skill Execution Map. Nothing else is
claimed. Rejected: publish-on-selection without byte review; in-comment resolution without
a durable record.

## Glossary candidates (S5 `domain-modeling`)

**PR class** — the changed-path-derived category (with the exceptional-change overlay)
fixing a PR's review derivation and permitted plan effects. **Plan-effect classification**
— the two-layer deterministic classification of a saved plan: raw per-resource action
classes aggregated over the complete effect vector, then contract-level workflow classes
derived with configuration and declaration inputs. **Effective-access plan** — the
deterministic, alias-only, digest-bound human-reviewable rendering of the applicable saved
plan. **Plan preview** — the sanitized, snapshot-blind, non-authoritative PR-time
rendering; never apply-authoritative. **Access-revocation acknowledgement** — the explicit
per-entry acknowledgement an ordinary assignment-removal PR carries for its exact expected
delete effect. **Generated-artifact manifest** — the deterministic digest-bound metadata
record for generated artifacts whose format cannot safely embed the envelope.

## Downstream handoffs (proposals; posted after publication — open tickets only)

- **T14 #19:** the decision-2 classification table and fail-closed uncovered-path rule; the
  decision-5 classifier as a validation contract (two layers; complete-vector aggregation;
  both replace orders; read-action separation rule; fail-closed unknown/unsupported actions
  and unresolvable sensitive values; contract-level classes requiring configuration/
  declaration/marker inputs with stated precedence; the proposed `CLS-*` family as input —
  final codes, severities, and harmonization are T14's); the access-revocation
  acknowledgement check (exact entry ↔ exact delete effect); the effective-access field
  contract including the constant permission-boundary field; the decision-3 identifier
  boundary as a serialization-time redaction validation (omission or replacement before
  public serialization; sensitivity markings alone insufficient; the single permitted
  AWS-managed-policy ARN pattern, never generalized); the decision-6 envelope/manifest
  schemas with canonical ordering as validation inputs; the shared import-identifier leak
  validation (with T19's gate open).

## Dependency effects and frontier

#22 has native edges blocked-by 0 (all eight blockers closed), **blocking 1** (#19).
Closing #22 reduces T14 #19 to **zero** open blockers (**unblocked**). Live frontier after
closure, in map order: **T14 #19 (next claimable — the final open child of map #1)**. After
T14 resolves, the frontier is empty and the map proceeds to S3 (close map) per the Skill
Execution Map. One HITL ticket per session — nothing is claimed at publication.

## Publication sequence (fail-closed; record before close)

Executed only under Eric's consolidated publication approval of the exact reviewed bytes. A
failure at any step through 8 leaves #22 open, with all later normal publication steps
unperformed; completed remote writes are not automatically undone. The exact partial state
is preserved through a Repository Continuity Artifact where necessary and reported.

1. Create this record at
   `docs/wayfinding/map-1/22-ci-plan-contract-and-pr-classes-for-slice-a.md`
   and the `docs/wayfinding/README.md` index line in the working tree, byte-identical to
   the approved package (SHA-256 verified).
2. Validate them on the final bytes: frontmatter parses, internal links resolve, the
   mechanical checks pass; no live identifier, no acceptance claim.
3. Commit both on `main`; push (authorized as part of the consolidated approval).
4. Verify the immutable record URL at the pushed commit resolves and is byte-equivalent to
   the local file.
5. Post the exact #22 resolution comment from the hash-bound tracker-payload bundle, with
   the record commit SHA filled in.
6. Post the exact informational handoff comment from the same bundle to T14 #19 only; no
   dependency edges; no comment to any closed ticket.
7. Update map #1: append exactly the one T20 Decisions-so-far line from the bundle. No fog
   edit and no map-order change (T20 graduates nothing and creates no ticket).
8. Round-trip verify: the #22 resolution comment, the T14 handoff comment, and the
   complete map #1 diff (exactly the one addition).
9. If any step through 8 fails: leave #22 open, perform no later normal publication step,
   preserve the exact partial state through continuity if necessary, and report it.
10. Close #22 as completed, retaining assignee `a24577t`, with the exact close comment
    from the bundle.
11. Round-trip verify the close; verify T14 #19 now shows zero open blockers (unblocked).
12. Recompute all dependency effects and the live frontier (expected state above) without
    claiming anything.
13. Replace the Repository Continuity Artifact (position after T20; frontier at T14 #19;
    both open gates and all carried items unchanged), substituting the actual record
    commit SHA. The template hash binds the pre-substitution bytes; the committed bytes
    differ only by deterministic replacement of `<RECORD-COMMIT-SHA>` with the 40-hex
    record commit SHA. Commit and push.
14. Verify `HEAD == origin/main`, a clean working tree, and the final tracker invariants
    (#22 closed with assignee retained; map body as verified; no other issue state
    changed).

Post-close failure rule: if a failure occurs after step 10, do not reopen #22 and do not
duplicate earlier writes; record the precise partial state in continuity where possible,
report it, and stop.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Verdict⟧ and ⟦G-Accept⟧; nothing in it authorizes any workflow,
environment, ruleset, CODEOWNERS, classifier, generator, or manifest implementation, any
AWS or GitHub mutation, any S3 or evidence creation, or any rehearsal activity; both
decision-7 gates remain open.
