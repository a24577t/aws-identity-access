---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 19
title: "T14 — Validation contract for the selected slice (rules, stable error codes, severities)"
url: https://github.com/a24577t/aws-identity-access/issues/19
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-26
sources:
  decision_batch: "consolidated 9-question HITL batch (2026-08-26); Eric's selections 1A–9A with collaborator corrections C1–C13 plus the final-round corrections C14–C15 applied throughout; decision direction approved by Eric; this record published only under Eric's separate hash-bound publication authorization"
  inherited_inputs:
    - https://github.com/a24577t/aws-identity-access/issues/19 (thirteen handoff comments: T05 validation conditions, T06 contract inputs, T07 negative administrator proof, T15 validation conditions, T16 fixture conditions, T09 snapshot contract and INV classes, T08 ADR-citation coordination, T19 adoption and plan-class inputs, T10 assignment identity inputs, T21 permission-set and hazard-detector inputs, T22 prerequisite inputs, T23 header-schema inputs, T20 classification and redaction inputs)
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
---

# T14 — Validation contract for the selected slice (rules, stable error codes, severities)

> Proposed discovery record — the complete durable result of T14 #19. Decisions approved by
> Eric as the human project owner and decision authority after collaborator review; executed
> by Claude in the repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`,
> using the batch-question directive (governing invariant 3 in the
> [repository-owner operating guide](../../../.ai/repository-owner/operating-guide.md)).
> **Nothing here is accepted architecture: every decision is a proposal until ⟦G-Verdict⟧ and
> ⟦G-Accept⟧.** GitHub issue #19 is the workflow/index surface and links to this record.

## Authorization scope of this record

Approving publication of this T14 result records the **proposed validation contract only**:
the severity vocabulary, the code catalogue, the stage model, the fixture-tree contract, and
the finding-record contract. It authorizes no validator, schema, fixture, generator, CI, or
workflow implementation, no file under `schemas/`, `src/`, `tests/`, or `.github/`, no GitHub
configuration, no AWS call or mutation, no Terraform execution, no S3 or evidence creation,
no backfill, no tagging or release work, and no aws_ami edit. Closing #19 empties the map's
child-ticket frontier but **does not itself execute S3**; S3 (close map) and S4 (Architecture
Grill) remain later activities under the
[Skill Execution Map](../../../.ai/repository/methodology/skill-execution-map.md). Everything
remains proposed pending ⟦G-Verdict⟧ and ⟦G-Accept⟧.

## Governing documents and evidence

Cited at the `aws_ami` revision pinned by T01 (#2): RD-08 (`11-decision-register.md` — a
consumer requiring immediate resolution MUST report "deferred", never "invalid"; schema/CI
pass, optionally warn), `02-configuration-model.md` (validation requirements 1–3; path rule;
generated-identifier invariant), I-1 (identity from configuration, never the path), RD-04,
RD-05, RD-06, and the exploratory `REVIEW.md` Q9 (`schema_version` has no migration story) at
the pin. Inherited map decisions: T02 #3, T03 #4, T04 #6 (d1/d6), T05 #7 (d1–d5), T06 #8
(d1–d5), T07 #9 (d1–d2), T09 #12 (d4–d5, d10–d13, d18–d19), T10 #15 (d1–d7), T15 #10
(d3/d5/d6/d7/d8/d12), T16 #11 (d5), T19 #14 (d2/d8/d21), T21 #20 (d1–d7), T22 #21 (d1–d4),
T23 #23 (d1–d3), T20 #22 (d1–d7). Evidence (never authority): the T18 inventory
(`docs/research/brownfield-inventory.md`) — the sixteen exploratory validator codes, §2 gap
analysis, §5.1 not-executed caveat; T21 F8 (Terraform-core `1.15.7` plan-action classes).

## Settled inputs (fixed by prior decisions; recorded, not re-decided)

- Hermetic boundary (T22 d4; T09 d15; T15 d6): validation holds no clock, reads no snapshot,
  makes no AWS call; plan and apply own the clock, snapshot, evidence, and AWS checks and
  fail closed; the plan gate is the primary control (T02).
- The fifteen `INV-*` classes with their triggers and the single deferring class (T09
  d18–d19); the seven `PRQ-*` distinctions (T22 d4); the three named `P-OOS-*` members with
  fixed wording (T21 d7); the proposed `CLS-*` family (T20 d5).
- The two-layer deterministic plan-effect classifier over the complete normalized effect
  vector, both replace orders, `forget` as a non-live-destruction state-removal primitive,
  read-action separation, fail-closed unknown/unsupported/divergent representations (T20 d5).
- The identifier boundary and serialization-time redaction rule (T20 d3/d7); the single
  permitted ARN-shaped public vocabulary (T21 d2).
- The T06 registry, routing, declaration, plan-gate, enforcement-evidence, and
  independent-approval contracts; the T05 identity contract; the T10 assignment identity and
  two-family separation; the T23 header contracts; the T20 d6 generated-metadata contract.
- The three carried empirical conditions (T20 d7; T21 d8): provider execution NOT
  RUN/BLOCKED on the authoring host and unverified in lab-CI; the pinned-provider `forget`
  representation unverified; `change.importing.id` rendering/sensitivity/redaction open.

## Claim-resolution record (grill-with-docs)

| # | Claim | Authority | Result | Upstream amendment / refinement |
|---|---|---|---|---|
| 1 | The severity model error / warning / deferred satisfies RD-08 | RD-08; `02` validation requirement 3 | **compatible** — `deferred` as a first-class non-blocking severity reserved exclusively for the RD-08 requested-inventory condition satisfies "report 'deferred', never 'invalid'"; its non-blocking rendering is RD-08's "optionally warn". The exploratory evidence typed deferral as a warning (`W-INV-DEFERRED`); T09 d12/d19 elevated it — a strengthening, not a conflict (decision 1) | none |
| 2 | Every non-obvious rule cites an inherited identifier or a closed map decision — schemas must not silently invent architecture | `02`; I-1; the brief (proposal); T08 d11 | **compatible** — every catalogue code carries an authority citation (I-n / RD-nn / document NN / CV-nn or a closed Tnn decision); purely mechanical codes are recorded as schema mechanics; stable domain ADR IDs join the citations at S5 per T08 d11 | none |
| 3 | The exploratory validator's 16 codes are evidence, not the catalogue to reproduce | Map Notes; T18 (X64/X66/X67, §5.2) | **inherited** — the catalogue derives only from closed decisions; every exploratory code is dispositioned in the evidence table below; T18 §5.1 (validator read, never executed) is immaterial because no contract element depends on exploratory runtime behavior | none |

## Decisions

Eric approved selections 1A–9A with the collaborator's corrections C1–C13 and the
final-round corrections C14–C15 applied throughout. Publication of this record occurs only
under Eric's separate, explicit hash-bound publication authorization; decision approval and
publication authorization are distinct acts.

### Correction ledger (applied)

- **C1 (Q1):** no validator may silently downgrade an error to warning or deferred; an
  unknown severity fails validation of the catalogue itself.
- **C2 (Q2):** `P-OOS-*` provenance corrected — three members adopted from T21; three
  minted by T14 (the identity-source naming input is T22's; the out-of-slice path
  requirement is T04's; the policy-form member is new).
- **C3 (Q2):** every code has exactly one canonical triggering layer; the four named
  overlap pairs (`P-OOS-PATH`/`CLS-UNCOVERED-PATH`, KEY/ASN shape, CFG/PRQ,
  `ADM-CAPABLE`/`ADM-STANDING`) are resolved in decision 2.
- **C4 (Q2):** `CLS-SENSITIVE` is renamed **`CLS-UNRESOLVED-VALUE`**: sensitivity itself is
  never an error; the error occurs only when a sensitive or unknown value prevents a
  classification the contract requires.
- **C5 (Q2):** the catalogue is exact — no approximate count, placeholder family, or
  unnamed active code remains.
- **C6 (Q2):** every code states active, dormant, or reserved; a dormant code names its
  activation condition.
- **C7 (Q3):** every code enumerates its exact allowed stages; no informal stage wording.
- **C8 (Q4a):** dual emission is replaced by canonical, surface-aware harmonization
  (decision 4).
- **C9 (Q5):** the action catalogs are repository-controlled, versioned, digest-pinned
  inputs whose source and bytes are not yet selected; detector rules 2 and 4 are not
  executable until they exist; absence, digest mismatch, unsupported schema, or
  wildcard-expansion inability fails closed (`ADM-CATALOG`); a runtime SDK/provider-derived
  catalog is rejected; the record distinguishes the complete architectural contract from
  still-unimplemented catalogue data.
- **C10 (Q6):** deterministic-fixture qualifications — exact expected finding sets;
  minimal multi-artifact sets where a finding inherently spans artifacts; synthetic
  committed inputs and a controlled clock; no wall-clock, AWS, live-identifier,
  credential, or mutable-external dependence; dormant codes acquire mandatory coverage at
  activation; T22's placeholder illustration is not a fixture; fixtures are never applied,
  uploaded, or treated as provider-execution evidence.
- **C11 (Q8):** exact implementation pins may be selected during S5/S6, but the S5 plan
  must make them explicit before implementation; unspecified future pins do not satisfy
  the pinning requirement; the map edit removes only the exact resolved T14 fog entry.
- **C12 (Q9a):** redaction-safe finding contract — canonical representation for global
  findings; sanitized value rules (hashing not automatically safe; Terraform sensitivity
  marking insufficient; no unsafe interpolation in messages); deterministic ordering and
  duplicate collapse (completed and finalized by C14).
- **C13 (Q9b):** closing T14 empties the frontier but does not execute S3; the continuity
  successor carries all three T20 conditions explicitly; the map payload removes only the
  exact T14 fog entry and appends exactly one Decisions-so-far line; no ticket is claimed
  after closing T14; everything remains proposed pending ⟦G-Verdict⟧ and ⟦G-Accept⟧.
- **C14 (final round):** the canonical finding ordering enumerates every serialized
  distinguishing field — `file_path`, `code`, `field_path`, `stage`, ordered `rule_ids`,
  the canonical sanitized `value` with the fixed `[omitted]` sentinel, the sanitized
  `message`; locators derive from canonical traversal of the canonically ordered input
  domain, never from filesystem enumeration order, map iteration order, concurrency,
  runtime timing, or discovery order; identical findings collapse before serialization;
  the occurrence index is **removed** — with location a total discriminator, no distinct
  findings can compare equal (decision 9(a) records the analysis).
- **C15 (final round):** lifecycle routing corrected in the continuity successor — S3
  closes map #1; S4 runs the Architecture Grill and produces a verdict; ⟦G-Verdict⟧ is
  the subsequent owner-approval gate; only an owner-approved verdict proceeds to S5
  (`to-spec-repo-owner`); a withheld or failed verdict returns to discovery/remediation
  as the Skill Execution Map specifies.

### Decision 1 — Severity vocabulary

The closed severity vocabulary is **`error | warning | deferred`**.

- **`error`** — blocking, fail-closed; the default disposition of every finding and of
  anything the contract does not match.
- **`deferred`** — non-blocking; restricted to the RD-08 requested-inventory condition
  (`INV-DEFERRED` is the only deferring code); reported as "deferred", never "invalid";
  its rendering realizes RD-08's "optionally warn".
- **`warning`** — a reserved, presently unpopulated vocabulary value. No slice-A code
  carries it; every carried decision that considered a warning rejected it (T21 d7's
  `W-REF-CMP` rejection; T22 d4's expiry-warning rejection; T09 d19's `INV-STALE`-as-warning
  rejection). Populating it is a future governed change.
- **No silent downgrade:** no validator, profile, configuration, or implementation may
  downgrade an error to warning or deferred; severity is fixed by this catalogue and
  changes only through a governed decision.
- **Catalogue self-validation:** a catalogue entry carrying a severity outside the closed
  vocabulary fails validation of the catalogue itself (error).

Classification: **compatible** (claim 1). Rejected: a two-value vocabulary (departs from
RD-08's own wording and makes a future warning a vocabulary change); deferral as a status
flag on a passing result (contradicts T09 d12's "severity deferred" as decided).

### Decision 2 — Code scheme, families, and canonical triggering layers

Codes are mnemonic uppercase `<FAMILY>-<MNEMONIC>` strings. Already published code strings
are preserved: the fifteen **`INV-*`** strings are adopted verbatim from T09 d19 (protecting
T10 d4's `INV-DUP`-citing proof text), the seven **`PRQ-*`** strings from T22 d4, and the
three named **`P-OOS-*`** strings from T21 d7. The remaining three `P-OOS-*` members and the
**`CLS-*`**, **`KEY-*`**, **`ASN-*`**, **`ADM-*`**, **`GOV-*`**, **`FIX-*`**, **`CFG-*`**,
**`DOC-*`**, **`GEN-*`**, and **`ADO-*`** families are minted by this decision (C2). The
exact roster is the Catalogue section: **79 codes across 13 families — 78 active, 1 dormant,
0 reserved** (C5, C6).

**Canonical triggering layers (C3).** Every code has exactly one canonical layer; the four
corrected pairs:

1. **`P-OOS-PATH` vs `CLS-UNCOVERED-PATH`:** `P-OOS-PATH` fires for a file under one of the
   six **recognized, enumerated absent-for-slice surfaces** (T04 d6) — a recognized path
   prohibited by the selected-slice profile. `CLS-UNCOVERED-PATH` fires when a changed file
   matches **no row of the T20 d2 classification table**.
2. **KEY vs ASN shape:** shape and grammar findings are **path-scoped** — `ASN-*` owns
   everything under `access/identity-center/account-assignments/**`; `KEY-*` owns
   `groups/`, `permission-sets/`, and **key-space referential integrity everywhere** (a
   dangling key reference is `KEY-DANGLING` regardless of the referencing file's location;
   an invalid key **in an assignment filename** is `ASN-SHAPE`).
3. **CFG vs PRQ:** `CFG-*` owns the committed `instance.yml`'s **internal form** (schema,
   formats, closed vocabularies — hermetic); `PRQ-*` owns its **relationship to external
   artifacts and live state** (snapshot binding, API-verifiable prerequisites,
   attestations — plan/apply).
4. **`ADM-CAPABLE` vs `ADM-STANDING`:** `ADM-CAPABLE` is the **single-file definition
   hazard** (T21 d6's five-rule detector); `ADM-STANDING` is the **cross-file condition**
   (an admin-capable definition combined with a standing workforce GROUP assignment
   referencing it — T07 d2).

**Intentional dual-family exception (T10 d7, preserved):** a USER-principal assignment
triggers both `ASN-SHAPE` (domain layer: no USER representation is defined or reserved) and
`P-OOS-USER` (profile layer: USER is outside slice A). This is the two-family separation
T10 decided; it is not an overlap — the layers, citations, and remediation horizons differ.

Classification: **compatible** (claim 2; the families map one-to-one onto the closed
decisions that source them). Rejected: a flat numeric registry (illegible; discards the
established families); stage-prefixed codes (conflates identity with the stage attribute);
renaming any inherited string (silently invalidates closed-record text).

### Decision 3 — One catalogue; exact stage attribution; hermetic boundary

One unified catalogue. Every code enumerates its **exact allowed stages** (C7) from the
closed stage vocabulary:

- **`validation`** — hermetic: schema, format, and repository-internal consistency over the
  committed tree and the PR changed-path set; no clock, no snapshot, no evidence, no AWS.
- **`plan`** — the post-merge `lab-plan` boundary: clock, snapshot, evidence, AWS-derived
  facts, and plan classification (T22 d4; T15 d15).
- **`apply`** — apply-time re-verification of the same facts against the bound artifacts
  (T09 d9/d11).
- **`generated-ci`** — deterministic regeneration and manifest checks for generated
  artifacts (T20 d6; an S6 check whose rule binds now).

A code lists more than one stage **only where inherited authority requires it** (each such
code cites that authority in the catalogue). A finding raised at a stage a code does not
enumerate is a contract violation (error). Classification: **compatible** (T22 d4's
boundary held code-by-code). Rejected: per-stage catalogues (fragments the T20 handoff).

### Decision 4 — Harmonization: canonical surface-aware reporting; the single leak code

**(a) `PRQ-SNAPSHOT` ↔ `INV-*` (C8).** Dual emission for one underlying defect is
rejected — it produces two blocking errors for one fact and weakens the
one-code/one-reason contract. Canonical, surface-aware harmonization instead:

- Validating the **inventory/snapshot artifact itself** emits the specific canonical
  `INV-MISSING`, `INV-STALE`, or `INV-DIGEST` code.
- Validating **`instance.yml`'s prerequisite reference or binding** to that artifact emits
  `PRQ-SNAPSHOT`.
- Both are **never** emitted for the same validation operation and root cause.
- `PRQ-SNAPSHOT` carries the related canonical INV category as **structured context**
  (`related_inv: INV-MISSING | INV-STALE | INV-DIGEST`) or citation — never as a second
  finding.
- When a single run validates both distinct surfaces and finds **independently actionable
  defects in each**, two findings are allowed only when each has a different location and
  remediation.

This preserves T22's prerequisite distinction ("five required distinctions" intact — the
seven codes stand) and T09's inventory codes without duplicate noise. T22's error/never-
deferred severities are confirmed unchanged.

**(b) The single leak code.** **`INV-PUBLIC-LEAK`** is the canonical public-serialization
leak code across its enumerated stages and every public surface: committed public content
(T15 d12), command output, Actions logs, annotations, job summaries, Terraform output, and
public artifacts (T09 d22), the effective-access summary and preview (T20 d3/d7), generated
artifacts (T20 d6; T19 d8), and import identifiers (T19 d8 — with the empirical rendering
verification still open). Redaction occurs **by omission or replacement before public
serialization**; sensitivity markings alone are never sufficient evidence. Its **only**
ARN-shaped exemption is the T21-approved partition-qualified AWS-managed-policy vocabulary
(`arn:aws:iam::aws:policy/...`); it never exempts account-local, generated, live, import,
principal, assignment, instance, store, or role identifiers.

Classification: **compatible** (T22 d4; T09 d19/d22; T20 d3/d7; T21 d2). Rejected: dual
emission (duplicate blocking noise); per-surface leak codes (one rule fragmented into
drift-prone copies); any second ARN exemption.

### Decision 5 — Standing-administrator codes and the pinned action catalogs

Three codes (canonical layers per decision 2):

- **`ADM-CAPABLE`** — the T21 d6 five-rule deterministic, conservative
  standing-admin-capability hazard detector rejecting an admin-capable permission-set
  definition. Rules 1 (exact `arn:aws:iam::aws:policy/AdministratorAccess`), 3
  (NotAction/NotResource breadth — fail closed), and 5 (unknown/unsupported broad
  pattern — fail closed) are **catalog-independent and fully executable as specified**.
  Rules 2 (wildcard expansion against a versioned, pinned action catalog) and 4 (unbounded
  IAM / SSO / SSO Admin / Identity Store mutation per an explicit versioned action set)
  **require the catalog data below and are not executable merely because this code
  exists** (C9).
- **`ADM-STANDING`** — the T07 d1/d2 cross-file condition: an admin-capable definition
  combined with a standing workforce GROUP assignment referencing it.
- **`ADM-CATALOG`** — fail-closed catalog integrity: the action catalog or
  privileged-mutation action set is absent, digest-mismatched, schema-unsupported, or
  unable to expand a required wildcard. Any invocation of rules 2 or 4 without valid
  catalog data raises this code.

**Catalog governance (C9):** both catalogs are **repository-controlled, versioned,
digest-pinned inputs**. Their exact source, transformation procedure, committed
representation, version, digest, update process, and review class are selected by the S5
plan **before implementation**; a runtime SDK/provider-derived catalog is **rejected**
(non-deterministic; breaks T21 d6's determinism). Until the S5-selected data exists, this
record is a **complete architectural contract over still-unimplemented catalogue data**:
rules 1/3/5 retain their inherited executable semantics; rules 2/4 are contract-complete
and data-blocked, failing closed through `ADM-CATALOG`.

Classification: **compatible** (implements T07 d1/d2 and T21 d6; T21 owns the equivalence
rule's content — this decision assigns codes and data governance only). Rejected:
runtime-derived catalogs; hand-maintained uncited lists; treating code existence as rule
executability.

### Decision 6 — Fixture tree and deterministic coverage

Fixture paths: **`tests/fixtures/valid/**`** (mirroring the `access/` and `governance/`
layouts) and **`tests/fixtures/invalid/<CODE>/**`** — one directory per code (T04 d1:
`tests/` contents are T14's; T07 d2: the T14-selected test-fixture path).

- **Coverage rule:** one deterministic negative fixture for every **active** code where the
  code can be isolated. Where a finding inherently requires multiple related artifacts
  (`ADM-STANDING`; `ASN-AGREEMENT`; `GOV-DECL-MATCH`), the code directory contains the
  complete **minimal** fixture set.
- **Exact expectation sets (C10):** "fails with exactly that code" means the fixture's
  expected finding set equals its declared set — normally exactly one code; multi-code
  expectations exist only where independent findings are intentionally exercised. The two
  approved multi-code expectations: the USER specimen → `{ASN-SHAPE, P-OOS-USER}` (T10 d7);
  the T07 negative pair → `{ADM-CAPABLE, ADM-STANDING}`.
- **Determinism (C10):** plan/apply-stage fixtures use synthetic, committed inputs
  (plan-JSON, snapshot envelopes, evidence stubs) and a **controlled clock** where time is
  relevant; no fixture depends on wall-clock time, AWS availability, live identifiers,
  credentials, or mutable external data.
- **Content rules:** no live identifiers ever — synthetic, format-valid digests and
  timestamps; the exact `AdministratorAccess` ARN is permitted under the decision-4(b)
  exemption; specimens are never planned against AWS, uploaded, applied, or treated as
  evidence of provider execution (T07 d2; C10).
- **Dormant codes** acquire mandatory fixture coverage when activated (C10).
- **Valid basis:** the inherited approved specimens — T10 d6's three assignment files and
  T21 d5's two permission-set files — plus T14-synthesized valid fixtures for the kinds no
  record has yet approved: a `groups/lab-readers.yml` reference (T05 d2 form, illustrative
  `identity_store_name`), `configuration/instance.yml` in both forms (without a
  `verification` block, and with a synthetic format-valid block), the exact five-entry T16
  d5 alias fixture, T06 d2 principal and review-class records, one T06 d5 declaration per
  kind, and T23 d1/d2 header examples. All keys remain illustrative pending S5. **T22's
  placeholder illustration is not a valid fixture** (C10).

Classification: **compatible** (mechanizes the brief's per-code specimen and completion
criteria, which are proposals adopted here by decision). Rejected: a flat specimen tree
(loses the code↔fixture mapping); fixtures with live identifiers or wall-clock dependence
(T18 §5.7 records that failure mode as evidence).

### Decision 7 — `CLS-*` defined now; no empirical gate advanced

The eleven `CLS-*` codes are defined now, exactly over T20 d5's classifier contract, and
three facts are preserved explicitly:

1. **Provider execution** remains NOT RUN/BLOCKED on the authoring host and **unverified in
   lab-CI** until executed in the designated lab-CI boundary; documentary CV-07 evidence is
   not S6 execution readiness.
2. The pinned-provider **`forget` representation remains unverified**; the
   `state-removal-only` contract class **cannot activate** until fixture/lab verification
   passes; a divergent representation fails closed (`CLS-REPRESENTATION`).
3. **`change.importing.id`** rendering, sensitivity, and redaction remain **open**; no
   rehearsal class can activate until that gate passes with empirical evidence.

Synthetic or Terraform-core builtin-provider fixtures (the T21 F8 method) demonstrate
**classifier logic only**; they are never AWS-provider execution evidence. Nothing in this
record advances, narrows, or reinterprets any of the three conditions.

Classification: **compatible** (T20 d5/d7 carried intact). Rejected: deferring the codes
until the gates close (leaves T20's contract codeless against its explicit handoff).

### Decision 8 — Fog resolution: no in-file `schema_version`; explicit pins

The "Schema versioning and test-environment pinning" fog patch (trigger: T14; REVIEW Q9 at
the pin: "`schema_version` has no migration story") is resolved without adding
`schema_version` to the closed exact-field-set formats:

- **Repository-internal schemas and their governed configuration change atomically** in the
  same commit (I-8); no mixed-version state can exist in-repo — that is the migration
  story Q9 found missing. The closed exact field sets (T10 d3, T16 d5, T22 d1, T21 d1)
  stand unmodified.
- **Cross-boundary artifacts retain their already decided schema versions:** the T09
  snapshot envelope (`body.schema_version` — the validator accepts exactly `1`, per the
  T09 d5 field-authority row) and the T06 d5 change-declaration `schema_version`.
- **Future per-file versioning requires a new governed decision.**
- **Hermetic validation is clock-free** (T22 d4; the exploratory validator's run-date
  dependence, T18 §5.7, is recorded as the failure mode; slice A's only clock checks live
  at plan/apply).
- **CI/local commands and dependency environments must be reproducible and pinned** —
  pinned base image, digest-locked dependencies, identical commands. Exact implementation
  pins may be selected during S5/S6, **but the S5 plan must make them explicit before
  implementation; unspecified future pins do not satisfy this requirement** (C11).

The eventual map edit removes **only** the exact resolved T14 fog entry, with no unrelated
fog or ordering change (C11). Classification: **compatible** (claim 2; Q9 resolved by
citation, not silently). Rejected: `schema_version: 1` in every governed file (reopens
three closed decisions); treating "pins later" as satisfying the pinning requirement.

### Decision 9 — Finding-record contract; durable record and publication

**(a) Finding-record contract (C12).** Every finding carries:

- `code`; `severity`; `stage`;
- `file_path` when a repository file owns the finding; `field_path` when applicable — a
  **global finding** (no owning file) uses the canonical representation
  `file_path: "-"`, `field_path: "-"`;
- ordered `rule_ids` (the authority citations from this catalogue);
- a sanitized `value` representation **only when safe and useful** — omitted or replaced
  before serialization whenever it could disclose a live identifier, secret, sensitive
  value, import ID, control character, or unsafe content; **hashing a sensitive value is
  not automatically safe; Terraform sensitivity marking alone is insufficient**;
- `message` — fixed wording where the catalogue requires it; messages never interpolate
  unsafe raw values; offending values are rendered escaped and unambiguous (T05 d5).

**Ordering and deduplication (C14):** canonical ordering is total and deterministic over
every serialized distinguishing field, in order: (1) `file_path`; (2) `code`; (3)
`field_path`; (4) `stage`; (5) ordered `rule_ids`; (6) the canonical sanitized `value`,
with the fixed sentinel `[omitted]` standing in whenever the value is absent or redacted
by omission; (7) the sanitized `message`. `severity` is serialized but is not an ordering
key: the catalogue fixes severity per code, so it is derivable from `code` and never
distinguishes findings. `file_path` and `field_path` carry the complete canonical locator
of the finding within its owning artifact — JSON-Pointer-style paths including list
indices, plan resource addresses, and canonical line/offset locators for byte-stream
surfaces — derived from canonical traversal of the canonically ordered input domain
(byte-lexicographic path order across files; document order of the canonical parse within
a file; lexicographic resource-address order within a plan), never from filesystem
enumeration order, map iteration order, concurrency, runtime timing, or discovery order.
Findings identical across all seven keys are collapsed deterministically before
serialization. **No occurrence index exists:** because the locator requirement makes
location a total discriminator, two findings identical across every semantic and location
field are the same finding — no legitimate non-identical case survives the collapse — so
the index is removed rather than retained as an unnecessary nondeterminism risk.
Serialization format is an S6 implementation choice whose output must preserve this
contract.

**(b) Durable record and publication (C13).** This record at
`docs/wayfinding/map-1/19-validation-contract-for-the-selected-slice.md` with one
`docs/wayfinding/README.md` index line. Publication executes only after Eric reviews the
exact drafted bytes — this record, the whole README successor, the tracker-payload bundle
(resolution comment, close comment, map payload, substitution instructions), and the
continuity successor, each bound by SHA-256 in the review package — and gives consolidated
approval; the fail-closed sequence below then runs unchanged. **No handoff comment is
posted — no open ticket remains.** Closing #19 empties the child-ticket frontier; **S3 (map
close) and S4 (Architecture Grill) remain later activities**; nothing is claimed after
closing T14. The map payload removes only the exact resolved fog entry and appends exactly
one Decisions-so-far line. Rejected: publish-on-selection without byte review; in-comment
resolution without a durable record.

## Catalogue — the complete slice-A validation contract

**Totals: 79 codes · 13 families · 78 active · 1 dormant (`ADO-MANIFEST`) · 0 reserved.**
Severity is `error` for every code except `INV-DEFERRED` (`deferred`). Unless a row states
otherwise: the negative-fixture basis is `tests/fixtures/invalid/<CODE>/` with expected
finding set exactly `{<CODE>}`; the valid-example basis is the decision-6 valid fixture
tree passing with zero findings; messages follow the decision-9 contract. Stage lists are
exhaustive (C7). "Remediation" names the party that owns the change that clears the
finding (C5/Q9b).

### `INV-*` — organization-inventory and snapshot classes (15; adopted verbatim from T09 d18–d19)

`INV-DEFERRED` messages say "deferred", never "invalid" (RD-08). Plan/apply-stage fixtures
are synthetic snapshot envelopes with a controlled clock.

| Code | Canonical trigger | Authority | Stages | State | Remediation |
|---|---|---|---|---|---|
| `INV-DEFERRED` | Referenced alias has `status: requested` in the consumed inventory; plan omits its resources | RD-08; T09 d12/d19; T10 d1 | validation, plan, apply (RD-08 spans schema/CI and plan) | active | none required — non-blocking; activation via the governed inventory write-back (Eric/lab) |
| `INV-ABSENT` | Referenced alias absent from the committed fixture (validation) or the consumed snapshot (plan/apply) | RD-06; T09 d19; T10 d1 | validation, plan, apply (fixture is committed; snapshot is plan-side — T09 d19) | active | requester corrects the reference, or governed fixture change |
| `INV-UNBOUND` | Active alias without a live binding in the binding snapshot | T09 d11/d19 | plan, apply | active | Eric/lab — Stage 6.1/6.3 re-discovery (T16 d11) |
| `INV-STATE` | Bound account `State` ≠ `ACTIVE` (`Status` is never read) | T09 d11/d19 | plan, apply | active | Eric/lab |
| `INV-RENAME` | Live `Name` ≠ `live_name` | T09 d19; OD-12 | plan, apply | active | Eric/lab — OD-12 governed rename |
| `INV-OU` | `ListParents` result ≠ `ou_id` | T09 d13/d19 | plan, apply | active | Eric/lab |
| `INV-DUP` | Duplicate alias entry in the committed fixture (validation); duplicate alias, live-name, or live-ID binding (plan/apply) | T09 d19; T10 d1/d4 | validation, plan, apply (T10 d1 cites the fixture side) | active | identity-platform (fixture) / Eric-lab (bindings) |
| `INV-UNALIASED` | Unaliased live account discovered in the governed lab OU | T09 d19 | plan, apply | active | Eric/lab — alias or remove; never a permissive fallback |
| `INV-DIGEST` | Digest disagreement among object key, envelope `snapshot_id`, S3 metadata, and sidecar; fixture-digest mismatch; canonicalization or I-JSON failure preventing digest verification | T09 d4/d19 | plan, apply | active | producer pipeline (Stage 6.1/6.3) |
| `INV-STALE` | Snapshot expired (90-day backstop), superseded, or `current` pointer changed during verification | T09 d10/d19 | plan, apply | active | Eric/lab — new Stage 6.1 re-discovery |
| `INV-MISSING` | No snapshot or `current` pointer | T09 d19 | plan, apply | active | Eric/lab |
| `INV-PARTIAL` | Incomplete pagination, API error, or throttling during live verification | T09 d19 | plan, apply | active | retry within the run; else Eric/lab |
| `INV-PROHIBITED-FIELD` | Prohibited field in the snapshot body (e-mail, credential, token, non-instance ARN, user name, `Status`; a `lab-requested` entry bound or carrying live fields) | T09 d5/d12/d19 | plan, apply | active | producer pipeline |
| `INV-BOUNDARY` | Authoritative organization/Identity Center boundary mismatch not assigned a more specific code (organization ID, root ID, management alias, instance ARN, identity-store ID, delegated-administrator alias, Region authority); `body.schema_version` ≠ `1` (T09 d5 field-authority row) | T09 d19 | plan, apply | active | Eric/lab |
| `INV-PUBLIC-LEAK` | A live, account-local, or generated identifier in public content: committed public files (validation); command output, logs, annotations, job summaries, Terraform output, public artifacts (plan, apply); generated artifacts (generated-ci). Sole exemption: the T21 partition-qualified AWS-managed-policy ARN vocabulary | T09 d22; T15 d12; T20 d3/d7; T19 d8; T21 d2 | validation, plan, apply, generated-ci (each stage cited: T15 d12 / T09 d22 / T09 d11 / T20 d6) | active | owner of the leaking surface; redaction by omission or replacement before serialization |

### `PRQ-*` — prerequisite verification (7; adopted from T22 d4; error, never deferred)

All plan and apply (T22 d4: clock, snapshot, evidence, and AWS checks live there).
`PRQ-SNAPSHOT` carries `related_inv` structured context per decision 4(a). Fixtures:
synthetic `instance.yml` + snapshot/evidence stubs with a controlled clock.

| Code | Canonical trigger | Authority | Stages | State | Remediation |
|---|---|---|---|---|---|
| `PRQ-MISSING` | Committed `verification` block absent — unverified prerequisites block plan and apply | T22 d1/d4 | plan, apply | active | Eric performs the separately authorized manual steps; verification-update PR records them |
| `PRQ-SNAPSHOT` | The `instance.yml` verification reference fails against the binding snapshot: `snapshot_id` ≠ `current`, `verified_at` not byte-equal to `body.discovered_at`, expiry beyond the backstop, or integrity failure — with `related_inv` context, never a second finding for the same root cause | T22 d1/d4; T09 d9/d10; decision 4(a) | plan, apply | active | Eric/lab re-verification; verification-update PR |
| `PRQ-INSTANCE` | API-verifiable instance presence/type failure | T22 d3/d4 | plan, apply | active | Eric — separately authorized remediation (T16 d11) |
| `PRQ-IDENTITY-STORE` | Identity-store binding failure | T22 d3/d4 | plan, apply | active | Eric — as above |
| `PRQ-DELEGATED-ADMIN` | `sso.amazonaws.com`-scoped delegated-administrator registration failure | T22 d3/d4 | plan, apply | active | Eric — as above |
| `PRQ-ATTESTATION` | Missing, stale, mismatched, integrity-invalid, or otherwise invalid human attestation for a non-API-verifiable characteristic | T22 d3/d4/d5 | plan, apply | active | Eric — new attestation in the Prerequisite Verification Record |
| `PRQ-GROUP` | Referenced-group resolution failure (`GetGroupId` with exact-DisplayName verification) | T22 d4; T05 d2 | plan, apply | active | Eric/identity-platform — group exists in the identity store or the reference is corrected |

### `P-OOS-*` — selected-slice profile, out of slice (6; three adopted from T21 d7, three minted — C2)

Severity error; message wording fixed: **"out of slice A — not prohibited by the domain
architecture"** (T21 d7). Stage: validation. Remediation: requester removes the
out-of-slice content; admitting it is a future governed slice change.

| Code | Canonical trigger | Authority | Stages | State | Provenance |
|---|---|---|---|---|---|
| `P-OOS-CMP` | Customer-managed policy reference in a permission set | T21 d7 (replacing exploratory `W-REF-CMP`); T03 d4 | validation | active | adopted |
| `P-OOS-BOUNDARY` | Permission-boundary content | T21 d7; T03 d4 | validation | active | adopted |
| `P-OOS-USER` | `principal.type: USER` in an assignment (profile layer; intentionally paired with `ASN-SHAPE` per T10 d7) | T21 d7; T10 d2; RD-05 | validation | active | adopted |
| `P-OOS-IDENTITY-SOURCE` | `instance.yml` `identity_source.type` other than `identity-center-default` (a domain-vocabulary value narrowed by the profile) | T22 d2 (naming input) | validation | active | minted |
| `P-OOS-PATH` | A file under one of the six enumerated absent-for-slice surfaces: `access/iam/`, `access/deployments/fleet-roles/`, `access/identity-center/identity-source/`, `access/identity-center/bootstrap/`, `governance/exceptions/`, `governance/runtime-mutations/` | T04 d6 (requirement); T03 | validation | active | minted |
| `P-OOS-POLICY-FORM` | A domain-valid permission set with more than one `managed_policies` entry, or both `managed_policies` and `inline_policy` present | T21 d1 (profile narrowing) | validation | active | minted |

### `KEY-*` — identity, grammar, uniqueness, reference integrity (8; T05 d1–d5)

Scope: `groups/`, `permission-sets/`, and key-space referential integrity everywhere
(decision 2). Reject, never normalize (T05 d1/d5). Remediation: requester, except the
`KEY-PROTECTED` pre-existing arm (Eric/lab disposition).

| Code | Canonical trigger | Authority | Stages | State | Remediation |
|---|---|---|---|---|---|
| `KEY-GRAMMAR` | Key violates `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` or its length bounds (permission-set 2–24; group 2–64) | T05 d1/d5 | validation | active | requester |
| `KEY-FILENAME` | Filename stem ≠ `key` | 02 v1; T05 d2/d3 | validation | active | requester |
| `KEY-COMPOSED` | Composed deployed Name > 32, failing the AWS Name pattern, or prefix budget > 8 including its delimiter, at the selected `ialab-` prefix | T05 d1/d3; T15 d8 | validation | active | requester / platform-change for a prefix change (returns to T05 d1) |
| `KEY-DESCRIPTION` | Permission-set `description` missing, outside 1–700, or failing the documented AWS `PermissionSet.Description` pattern (pin-reverified, T15) | T05 d3 | validation | active | requester |
| `KEY-IDSTORE-NAME` | `identity_store_name` missing, empty, or with leading/trailing Unicode whitespace or control characters; exact code-point comparison, no normalization | T05 d2/d5 | validation | active | requester |
| `KEY-DUP` | Duplicate key within `groups/` or `permission-sets/`; more than one group file per exact `identity_store_name` | T05 d5 | validation | active | requester |
| `KEY-DANGLING` | Dangling reference, alias, redirect, or derived key — including an assignment referencing an undefined group or permission-set key, and rename residue | T05 d4/d5 | validation | active | requester |
| `KEY-PROTECTED` | Deployed-Name collision within desired configuration (validation) or with a pre-existing permission set (plan/apply) — protected-resource error; never silently imported, adopted, renamed, suffixed, or overwritten | T05 d5; T15 d8 | validation, plan, apply (pre-existing arm needs live listing — T05 d5) | active | requester (in-config); Eric/lab (pre-existing) |

### `ASN-*` — assignment shape and agreement (3; T10 d1–d3)

Scope: `access/identity-center/account-assignments/**` (decision 2). Stage: validation.
Remediation: requester.

| Code | Canonical trigger | Authority | Stages | State |
|---|---|---|---|---|
| `ASN-SHAPE` | Unrecognized domain assignment representation: wrong segment count; invalid key grammar in the filename; uppercase; other separators; `_`-prefixed scope files; unrecognized body fields; any non-GROUP body form (no USER representation is defined or reserved) | T10 d2 | validation | active |
| `ASN-ACCOUNT-ALIAS` | Account-alias form violation: directory not exactly one path segment; alias grammar violation; separators, traversal sequences, uppercase, normalization, or unrecognized directory forms | T10 d1; T15/T05 grammar | validation | active |
| `ASN-AGREEMENT` | Three-way path/content mismatch: directory ↔ `account`; filename segment 1 ↔ `principal.group`; segment 2 ↔ `permission_set` | T10 d3; 02 v1; I-1 (generalizes exploratory `E-NAME`) | validation | active |

### `ADM-*` — standing administrator (3; T07 d1–d2; T21 d6; decision 5)

Stage: validation. `ADM-CAPABLE` fixture basis: the T07/T21 AdministratorAccess
counterexample exercises rule 1 now (catalog-independent); rule-2/4 fixtures become
mandatory when the S5-selected catalogs land. The T07 pair carries expected set
`{ADM-CAPABLE, ADM-STANDING}` (decision 6).

| Code | Canonical trigger | Authority | Stages | State | Remediation |
|---|---|---|---|---|---|
| `ADM-CAPABLE` | The five-rule hazard detector rejects an admin-capable definition (rules 1/3/5 executable now; rules 2/4 contract-complete, data-blocked pending the S5 catalogs — C9) | T21 d6; T07 d1 | validation | active | requester removes the hazard |
| `ADM-STANDING` | Cross-file: an admin-capable definition combined with a standing workforce GROUP assignment referencing it | T07 d1/d2 | validation | active | requester removes the assignment or the definition |
| `ADM-CATALOG` | Action catalog or privileged-mutation action set absent, digest-mismatched, schema-unsupported, or unable to expand a required wildcard — fail closed | decision 5 (C9); T21 d6 determinism | validation | active | platform-change PR restoring valid pinned catalog data |

### `GOV-*` — governance registry, routing, declarations, enforcement (9; T06 d1–d5)

Remediation: identity-platform via the strictest-set platform-change PR, except where a row
names the governed process.

| Code | Canonical trigger | Authority | Stages | State | Remediation |
|---|---|---|---|---|---|
| `GOV-PRINCIPAL` | `governance/ownership/principals/*.yml` schema violation (`key`, `kind: role \| team`, `description`; provider handles or class membership present) | T06 d2 | validation | active | identity-platform |
| `GOV-CLASS` | `governance/ownership/review-classes/*.yml` violation (`key`, `description`, non-empty `satisfied_by`; unresolved principal; duplicates; authored enforcement status) | T06 d2 | validation | active | identity-platform |
| `GOV-OWNER` | A governed file's `owner` does not resolve to a principal key | T06 d1 | validation | active | requester / identity-platform |
| `GOV-ROUTE` | Uncovered governed path (no explicit route or fail-closed default), or an unknown, ambiguous, or inactive account under `account-assignments/<account-name>/` | T06 d3 | validation | active | identity-platform (routing); requester (account reference) |
| `GOV-CODEOWNERS` | Generated CODEOWNERS disagrees with the registry, routing, and handle mapping | T06 d2/d3 | generated-ci | active | regenerate; identity-platform for source defects |
| `GOV-DECLARATION` | Change-declaration schema violation (discriminated `kind`; required common and kind-specific fields including `schema_version` and mandatory `valid_until`; prohibited fields — `approved_by`, GroupIds, ARNs, account IDs) | T06 d5 | validation | active | declaring owner |
| `GOV-DECL-MATCH` | Plan-gate declaration matching failure (no match; multiple; expired/not-yet-valid; not merged into the trusted base; mismatched kind/phase/keys/paths/environment/scope; effects outside the authorized shape; GroupId change without the principal-replacement kind; rename plan with any AWS mutation; introduce with deletes; retire without verified introduce evidence) | T06 d5 | plan | active | declaring owner via the governed exceptional workflow |
| `GOV-ENFORCEMENT` | A required control's evidence is `unenforced`/`unknown` without a current applicable lab exception | T06 d3 | plan, apply (both consume the evidence — T06 d4) | active | Eric — enforcement remediation or a recorded lab exception |
| `GOV-APPROVAL-CLASS` | One review event or physical identity satisfying more than one independently required class without an accepted co-satisfaction rule | T06 handoff (8); d3 | plan | active | Eric — independent review; else unenforced/lab-exception recording |

### `FIX-*` — alias inventory fixture (4; T15 d5; T16 d5)

Stage: validation. Remediation: identity-platform (governed fixture change).

| Code | Canonical trigger | Authority | Stages | State |
|---|---|---|---|---|
| `FIX-FIELDS` | Fixture entry field set not exactly `{alias, class, status, intended_classification}` | T16 d5 | validation | active |
| `FIX-CLASS` | `class` outside `{management, lab-workload, role-host, requested-fixture}` | T16 d5 | validation | active |
| `FIX-ALIAS` | Alias violates the T05/T15 grammar | T15 d5; T05 d1 | validation | active |
| `FIX-LIVE` | Any live identifier (account ID, live name, ARN, e-mail, OU path) in the fixture | T16 d5 | validation | active |

### `CFG-*` — `instance.yml` internal form (4; T22 d1)

Stage: validation (hermetic — decision 2's CFG/PRQ layer split). Remediation: requester via
the verification-update PR class.

| Code | Canonical trigger | Authority | Stages | State |
|---|---|---|---|---|
| `CFG-FIELDS` | Field-set violation: missing required field, unknown field, or structure outside the exact T22 d1 set | T22 d1 | validation | active |
| `CFG-VOCAB` | Closed-vocabulary violation: `instance_type` ≠ `organization`; `delegated_administrator` not in the alias grammar; malformed subtree structure | T22 d1/d2 | validation | active |
| `CFG-REGION` | `primary_region` ≠ `us-east-1` or `additional_regions` ≠ `[]` (equality with T15 d3) | T22 d1; T15 d3 | validation | active |
| `CFG-VERIFICATION` | `verification` block violation: partial block (all-or-nothing); `snapshot_id` not exactly 64 lowercase hexadecimal; `verified_at` not the complete RFC 3339 UTC representation T09 permits (fractional seconds accepted when present) | T22 d1 | validation | active |

### `DOC-*` — documentation headers (3; T23 d1–d3)

Stage: validation. Applicability: `docs/architecture/` + `docs/guides/` with T23's named
exclusions; `docs/generated/**` is governed by the `GEN-*` family instead. Remediation: the
document's author under the applicable review class.

| Code | Canonical trigger | Authority | Stages | State |
|---|---|---|---|---|
| `DOC-NORMATIVE` | Normative-header violation: `status` outside `{proposed, accepted}`; `authority` ≠ `normative`; missing `scope`/`decision_owner`; `decided` present while proposed or absent when accepted; unknown fields | T23 d1 | validation | active |
| `DOC-INFORMATIVE` | Informative-header violation: `authority` ≠ `informative`; `derives_from` empty, duplicated, or unresolvable; unknown fields | T23 d2 | validation | active |
| `DOC-SCOPE` | A file inside the applicability boundary missing its class header, carrying the other class's form, or carrying `supersedes` (register-exclusive) | T23 d1/d3 | validation | active |

### `GEN-*` — generated-artifact metadata (4; T20 d6)

The rules bind now; generated artifacts are produced only at S6. A hand-authored file under
`docs/generated/**` today fails here at validation. Remediation: regenerate with the pinned
generator; platform-change PR for generator or source defects.

| Code | Canonical trigger | Authority | Stages | State |
|---|---|---|---|---|
| `GEN-MANIFEST` | Manifest missing, malformed, or misordered; whole-file digest mismatch with committed bytes; a generated artifact (including any file under `docs/generated/**`) absent from the manifest | T20 d6 | validation, generated-ci (digests are hermetic; regeneration is CI — T20 d6) | active |
| `GEN-ENVELOPE` | Embedded envelope missing, malformed, or misordered where required; any whole-target self-digest; an envelope in a control/machine format | T20 d6 | validation, generated-ci | active |
| `GEN-DRIFT` | Deterministic regeneration produces different bytes (hand edit, generator drift, or source drift) | T20 d6 | generated-ci | active |
| `GEN-CODEOWNERS` | `.github/CODEOWNERS` not valid CODEOWNERS syntax, carrying an embedded envelope, or absent from the manifest | T20 d6 | validation, generated-ci | active |

### `CLS-*` — classification and plan-effect contract (11; T20 d1/d2/d5; T15 d7; minted)

Remediation: requester restructures the PR or plan; `CLS-PROTECTED`/`CLS-EFFECT`
dispositions involving pre-existing or deferred resources go to Eric.

| Code | Canonical trigger | Authority | Stages | State |
|---|---|---|---|---|
| `CLS-UNCOVERED-PATH` | A changed file matching no row of the T20 d2 classification table | T20 d2 | validation, plan (PR-time classification; recomputed by `lab-plan` — T20 d4) | active |
| `CLS-COMBINATION` | A prohibited class combination: exceptional change + unrelated work; retirement + new grant; a rehearsal-family PR + any other class | T20 d1 | validation, plan | active |
| `CLS-UNKNOWN-ACTION` | An unknown or unsupported plan-JSON action list | T20 d5 | plan | active |
| `CLS-UNRESOLVED-VALUE` | A sensitive or unknown value prevents a classification the contract requires — sensitivity itself is never an error (C4) | T20 d5 | plan | active |
| `CLS-REPRESENTATION` | The pinned toolchain emits a different or unsupported representation for a removed-block resource (`forget` divergence) | T20 d5; T21 F8 (evidence) | plan | active |
| `CLS-FORGET-PATTERN` | A `forget` row combined with any live-mutation row, or lacking its exactly-matching one-to-one `removed { lifecycle { destroy = false } }` block | T20 d5 | plan | active |
| `CLS-MARKER-MISMATCH` | Contract-level marker/aggregate inconsistency (import markers, removed blocks, or guard-file changes disagreeing with the normalized effect vector, under T20 d5's input precedence) | T20 d5 | plan | active |
| `CLS-UNATTRIBUTABLE` | A plan effect not attributable to an allowed changed surface of a matched class | T20 d1/d5 | plan | active |
| `CLS-EFFECT` | The aggregate effect outside the matched classes' permitted set (the decision-5 matrix), including any effect targeting a deferred/requested alias | T20 d5; RD-08; T16 d5 (condition 3) | plan | active |
| `CLS-PROTECTED` | Any operation on a resource outside the derived POC-managed (`ialab-`) set or on protected pre-existing resources | T15 d7; T04 d5 | plan, apply (apply re-verifies — T09 d11) | active |
| `CLS-REVOCATION-ACK` | An assignment delete effect without the exact-entry access-revocation acknowledgement, or an acknowledgement/effect mismatch | T20 d3/d5 | plan | active |

### `ADO-*` — adoption and rehearsal (2; T19 d2/d21)

| Code | Canonical trigger | Authority | Stages | State | Activation condition |
|---|---|---|---|---|---|
| `ADO-PHASE` | Any `import`, `moved`, or `removed` block — or other adoption-shaped change — in slice-A configuration outside a separately authorized rehearsal phase | T19 d2 | validation | active | — (remediation: requester removes it; adoption occurs only in the authorized rehearsal) |
| `ADO-MANIFEST` | Adoption-manifest schema violation (alias, evidence pointers, bounded ownership-proof fields, attestations, approvals) | T19 d21 | validation | **dormant** | Eric's separate authorization of the post-acceptance import-rehearsal phase (T19 d2/d16) **and** the import-redaction gate passing with empirical evidence; fixture coverage becomes mandatory at activation |

## Exploratory-code evidence disposition (claim 3)

The sixteen exploratory codes (T18: X64/X66/X67, §5.2) are evidence, not the catalogue.
Dispositions:

| Exploratory code | Disposition |
|---|---|
| `E-INV-UNKNOWN` | superseded by `INV-ABSENT` (T09 d19) |
| `E-SCHEMA` | subsumed by the per-family schema codes (`CFG-*`, `FIX-*`, `GOV-*`, `KEY-*`, `ASN-*`, `DOC-*`) |
| `E-NS-RESERVED` | no successor — no reserved namespace exists (T06; the brief's no-`pa-*` rule) |
| `E-NAME` | generalized into `ASN-AGREEMENT` and `KEY-FILENAME` (T10 d3; 02 v1) |
| `E-ID-LITERAL` | superseded by `INV-PUBLIC-LEAK` and the decision-4(b) rule (RD-06) |
| `E-TRUST-WILDCARD` | no slice-A successor (no IAM roles in slice A; T03) |
| `E-EXP-EXPIRED` | no slice-A successor (no IAM-user exceptions in slice A; declaration expiry is `GOV-DECL-MATCH` at plan) |
| `E-POLICY-WIDE` | superseded by `ADM-CAPABLE` (T21 d6; T07) |
| `W-INV-DEFERRED` | superseded by `INV-DEFERRED` — elevated from warning to the `deferred` severity (T09 d12; RD-08) |
| `E-DUP` | retired — duplicate prevention is by construction (T10 d4); stands only as evidence of the replaced aggregated shape |
| `W-REF-CMP` | rejected — replaced by error `P-OOS-CMP` (T21 d7) |
| `E-EXCL` | superseded by `CLS-PROTECTED` and `KEY-PROTECTED` (T15 d7/d8) |
| `E-YML` | subsumed by schema mechanics (a file failing to parse fails its family's schema code) |
| `E-REGION` | superseded by `CFG-REGION` (T22 d1; T15 d3) |
| `E-REF` | superseded by `KEY-DANGLING` (T05 d4/d5) |
| `E-TRUST-SOURCE` | no slice-A successor (no trust policies in slice A; T03) |

T18 §5.1 (the exploratory validator was read, never executed) is immaterial to this
contract: no element depends on exploratory runtime behavior, so no execution of
`tools/test_validate.py` is required.

## Glossary candidates (S5 `domain-modeling`)

**Validation finding** — one deterministic result under the decision-9 contract.
**Severity vocabulary** — the closed set `error | warning | deferred` with decision 1's
population rules. **Canonical triggering layer** — the single surface and rule layer on
which a code fires (decision 2). **Stage** — the closed set
`validation | plan | apply | generated-ci` (decision 3). **Catalogue** — the exact 79-code
contract in this record. **Fixture expectation set** — the declared exact finding set of a
negative fixture (decision 6). **Catalog data** — the two repository-controlled,
digest-pinned action-catalog inputs of decision 5. **Dormant code** — a catalogued code
whose enforcement and fixture obligations begin at its named activation condition.

## Downstream notes (no open ticket remains; inputs to S3/S5)

- **S3 (close map):** the frontier is empty at #19's closure; the "Schema versioning and
  test-environment pinning" fog entry is resolved by decision 8 and removed by the map
  payload; no fog remains.
- **S5 (consolidation):** the catalogue joins `configuration-contract.md` by citation
  (T23 d5's citation set extends to this record); stable domain ADR IDs join the
  catalogue's citations (T08 d11); the S5 plan must select the decision-5 catalog source,
  transformation, representation, version, digest, update process, and review class, and
  must make the decision-8 environment pins explicit, before implementation.
- **S6 (implementation):** validator, schemas, fixtures, generators, and CI implement this
  contract; nothing is implemented now.

## Dependency effects and frontier

#19 has native edges blocked-by 0 (all nine blockers closed), blocking 0. Closing #19
leaves map #1 with **zero open children: the frontier is empty**. Closing #19 does **not**
execute S3; per the [Skill Execution Map](../../../.ai/repository/methodology/skill-execution-map.md),
S2 completes with "Frontier empty → S3", and S3 (close map) then S4 (Architecture Grill)
are later activities. One HITL ticket per session — nothing is claimed at publication.

## Publication sequence (fail-closed; record before close)

Executed only under Eric's consolidated publication approval of the exact reviewed bytes. A
failure at any step through 8 leaves #19 open, with all later normal publication steps
unperformed; completed remote writes are not automatically undone. The exact partial state
is preserved through a Repository Continuity Artifact where necessary and reported.

1. Create this record at
   `docs/wayfinding/map-1/19-validation-contract-for-the-selected-slice.md` and the
   `docs/wayfinding/README.md` successor in the working tree, byte-identical to the
   approved package (SHA-256 verified).
2. Validate them on the final bytes: frontmatter parses, internal links resolve, the
   mechanical checks pass; no live identifier, no acceptance claim.
3. Commit both on `main`; push (authorized as part of the consolidated approval).
4. Verify the immutable record URL at the pushed commit resolves and is byte-equivalent to
   the local file.
5. Post the exact #19 resolution comment from the hash-bound tracker-payload bundle, with
   the record commit SHA substituted.
6. Post no handoff comment — no open ticket remains; no comment to any closed ticket.
7. Update map #1: append exactly the one T14 Decisions-so-far line from the bundle and
   remove exactly the resolved fog entry named in the bundle. No other change of any kind.
8. Round-trip verify: the #19 resolution comment and the complete map #1 diff (exactly one
   addition and one removal).
9. If any step through 8 fails: leave #19 open, perform no later normal publication step,
   preserve the exact partial state through continuity if necessary, and report it.
10. Close #19 as completed, retaining assignee `a24577t`, with the exact close comment
    from the bundle.
11. Round-trip verify the close; verify map #1 now has zero open children (frontier
    empty).
12. Recompute all dependency effects: the frontier is empty; the map is ready for S3 as a
    later activity; nothing is claimed.
13. Replace the Repository Continuity Artifact with the continuity successor (position:
    map #1 children complete; resume at S3; all three T20-carried conditions and every
    carried item explicit), substituting the actual record commit SHA. The template hash
    binds the pre-substitution bytes; the committed bytes differ only by deterministic
    replacement of `<RECORD-COMMIT-SHA>` with the 40-hex record commit SHA. Commit and
    push.
14. Verify `HEAD == origin/main`, a clean working tree, and the final tracker invariants
    (#19 closed with assignee retained; map body as verified; no other issue state
    changed).

Post-close failure rule: if a failure occurs after step 10, do not reopen #19 and do not
duplicate earlier writes; record the precise partial state in continuity where possible,
report it, and stop.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Verdict⟧ and ⟦G-Accept⟧; nothing in it authorizes any validator, schema,
fixture, generator, CI, or workflow implementation, any AWS or GitHub mutation, any S3
write or evidence creation, or any rehearsal activity; the three carried empirical
conditions — provider execution, the `forget` representation, and import-identifier
redaction — remain open and unadvanced.
