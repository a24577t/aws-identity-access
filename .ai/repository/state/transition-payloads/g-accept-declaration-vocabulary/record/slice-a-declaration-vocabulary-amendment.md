# Slice-A declaration-vocabulary amendment

Append-only correction record to the accepted slice-A decision set, produced through
the methodology's halt-don't-decide excursion (E1) from the S8 `codebase-design`
validate review of ticket R1 #26 (branch `ticket/r1-foundation-and-contracts` @
`b23d2b9c363e72316d2dc5602cc2cdc8a3623c74`). It ratifies exactly one thing: the
**executable field table of the governed change-declaration records**
(`governance/change-declarations/*.yml`) — the renderings that
[T06 #8 decision 5](../wayfinding/map-1/08-approval-declarations-versus-enforcement.md)
fixes descriptively but does not spell. Because the repository is Pre-Baseline — no
Architecture Baseline exists and the Architecture Version counter is owned by
Baseline Publication — this record is accepted at a **narrow ⟦G-Accept⟧**, the
established Pre-Baseline correction route, and **no Architecture Version advances**;
the owner-approved Skill Execution Map correction accepted alongside this record
fixes that routing. This record carries no authority header (T23 #23 decision 4
scopes the normative-header rule to `docs/architecture/` and `docs/guides/`); its
authority derives from its approving narrow ⟦G-Accept⟧ record and this repository
placement. On any divergence between this amendment and the records it cites, **the
cited record prevails**: nothing here reopens, restates, or amends T06 #8 decision
5's semantics, the
[T20 #22 decision 5](../wayfinding/map-1/22-ci-plan-contract-and-pr-classes-for-slice-a.md)
classifier contract, the
[T14 #19](../wayfinding/map-1/19-validation-contract-for-the-selected-slice.md)
catalogue, the
[configuration contract](../architecture/configuration-contract.md), or any accepted
ADR — and nothing here advances the three open empirical conditions (engineering
specification §8.3) or activates any dormant class.

## 1. What is ratified, and what is not

**Ratified (executable renderings only):**

- the exact YAML field names, types, constants, formats, and per-kind applicability
  rules of the three declaration kinds, where T06 #8 d5 fixed the content
  descriptively ("affected paths/resource keys", "expected plan-effect class",
  "explicit destroy acknowledgement", …) without spelling the executable form;
- the `schema_version` value and type;
- the enforcement split between the JSON Schemas and the T14 #19 validator for these
  forms.

**Unchanged (binding by citation, never restated):**

- every field T06 #8 d5 already spells literally (`schema_version`, `key`, `kind`,
  `owner`, `justification`, `change_reference`, `deployment_scope`, `valid_from`,
  `valid_until`, `group_key`, `from_key`, `to_key`, the `phase` values `introduce`
  and `retire`, and the three kind tokens);
- T06 #8 d5's lifecycle, prohibited-field, no-self-authorization, and plan-gate
  matching semantics (`GOV-DECLARATION`, `GOV-DECL-MATCH`);
- the T20 #22 d5 plan-effect classification contract and its class vocabulary
  (reproduced in §3 for citation, not decided here);
- the T05 #7 key grammar and bounds;
- every other governed form's closed field set;
- the Architecture Baseline, Baseline Version, and Architecture Version conditions —
  all remain `none`; no counter is created or advanced by this record.

## 2. The normative executable declaration-vocabulary table

The following is the complete executable form of `governance/change-declarations/
<declaration-key>.yml`. JSON Schemas implementing it are its executable artifacts
(RD-04 at the pinned aws_ami revision); unknown fields are rejected in every kind
(closed forms; T06 #8 d5 "schema-validated"; `GOV-DECLARATION`).

### 2.1 Common fields (all three kinds)

| Field | Type and constraint | Rendering authority |
|---|---|---|
| `schema_version` | integer, exactly `1`; changes only atomically with the schema (T14 #19 d8's atomic schema+configuration rule) | value and type ratified **here** (Q2-A); field literal in T06 d5 |
| `key` | string, T05 #7 d1 grammar; equals the filename stem exactly | literal in T06 d5; grammar T05 #7 |
| `kind` | exactly one of `principal-replacement`, `group-key-rename`, `permission-set-key-replacement` | literal in T06 d5 |
| `owner` | string, T05 grammar; a T06 #8 d2 principal key (resolution is the validator's `GOV-OWNER`/`GOV-DECLARATION` duty) | literal in T06 d5 |
| `justification` | non-empty string | field literal in T06 d5; the non-empty-string realization is the S7 rendering adopted within Q1-A's executable-field-table scope |
| `change_reference` | non-empty string; an immutable reference (issue/PR URL or equivalent immutable identifier) | field and immutable-reference content rule literal in T06 d5; the non-empty-string realization is the S7 rendering adopted within Q1-A's executable-field-table scope |
| `deployment_scope` | non-empty string | field literal in T06 d5; the non-empty-string realization is the S7 rendering adopted within Q1-A's executable-field-table scope |
| `valid_from`, `valid_until` | RFC 3339 UTC timestamp with the `Z` designator, optional fractional seconds (the same representation T09/T22 use); `valid_until` mandatory — indefinite declarations prohibited | fields literal in T06 d5; format ratified **here** (Q3-A); enforcement split per §4 |
| `affected_paths` | array, ≥ 1 unique non-empty strings — the governed paths the declaration covers | ratified **here** (Q1-A): realizes T06 d5's "affected paths/resource keys" **jointly** with the kind-specific key fields (§2.2); no separate `affected_resource_keys` field exists |
| `expected_plan_effect_class` | string drawn from the closed T20 #22 d5 vocabulary (§3); per-kind constraints in §2.2 | field name ratified **here** (Q1-A); values are T20 #22 d5's, not decided here |
| `lab_exception_reference` | optional non-empty string — the applicable lab-exception reference, if any | field name ratified **here** (Q1-A); optionality and content rule literal in T06 d5 ("applicable lab-exception reference if any") |

**"Permitted phase/operation" realization (Q1-A):** T06 d5's common-list item is
realized per kind — `permission-set-key-replacement` carries the `phase` field with
the literal values `introduce` | `retire`; for `principal-replacement` and
`group-key-rename` the `kind` itself is the permitted operation and no separate
operation field exists, exactly as T06 d5's own kind-specific enumerations render
them.

**Prohibited everywhere (T06 d5, by citation):** `approved_by`, approval timestamps,
GroupIds, ARNs, account IDs, or any other generated/runtime identifier. Closed forms
make these structurally impossible; the rule itself is T06 d5's, not this record's.

### 2.2 Kind-specific fields

**`principal-replacement`** — additionally required:

| Field | Type and constraint | Rendering authority |
|---|---|---|
| `group_key` | string, T05 grammar, 2–64 | literal in T06 d5 |
| `reason` | non-empty string — why the external principal is replaced | ratified **here** (Q3-A) |
| `group_id_change_expected` | boolean, exactly `true` — the T06 d5 "explicit statement that a GroupId change is expected"; no GroupId value appears anywhere in the declaration | ratified **here** (Q3-A) |

`expected_plan_effect_class`: any single value of the §3 closed vocabulary; T06/T20
fix no single class for this kind, and the declared value is matched at the plan
gate (`GOV-DECL-MATCH`), never pre-decided by schema.

**`group-key-rename`** — additionally required:

| Field | Type and constraint | Rendering authority |
|---|---|---|
| `from_key`, `to_key` | string, T05 grammar, 2–64 | literal in T06 d5 |

`expected_plan_effect_class`: exactly `empty` — the T20 #22 d5 fixed class for the
group-key-rename declared-change PR, realizing T06 d5's "expected plan effect fixed
to zero AWS mutations". The token is T20's; only its use in this field is ratified
here.

**`permission-set-key-replacement`** — additionally required:

| Field | Type and constraint | Rendering authority |
|---|---|---|
| `from_key`, `to_key` | string, T05 grammar, 2–24 | literal in T06 d5 |
| `phase` | exactly `introduce` or `retire` | literal in T06 d5 |
| `introduce_completion_evidence` | non-empty string — immutable reference to verified introduce-phase completion evidence; **required when `phase: retire`** | ratified **here** (Q3-A, as rendered); content rule literal in T06 d5 |
| `destroy_acknowledgement` | boolean, exactly `true` — T06 d5's "explicit destroy acknowledgement"; **required when `phase: retire`** | ratified **here** (Q3-A, as rendered) |

`expected_plan_effect_class`: exactly `creates-only` when `phase: introduce`;
exactly `deletes-only` when `phase: retire` — the T20 #22 d5 fixed classes.
Schema-level requirement of the completion-evidence and acknowledgement fields at
`phase: retire` realizes T06 d5's "either design must prevent retire authorization
before verified introduce completion" at the structural layer; the plan gate's
evidence verification remains `GOV-DECL-MATCH`'s. T06 d5 leaves separate
declarations versus separately approved phases of one declaration as an
implementation choice; nothing here narrows it further.

## 3. The closed plan-effect vocabulary (T20 #22 decision 5, reproduced by citation)

Aggregate classes over the complete normalized effect vector: `empty`,
`creates-only`, `updates-only`, `deletes-only`, `mixed`, `state-removal-only`
(per Layer 2); contract-level workflow classes: `imports-only`,
`state-removal-only`, `guard-removal-no-live-change`. The
`expected_plan_effect_class` value set is therefore exactly:

`empty` · `creates-only` · `updates-only` · `deletes-only` · `mixed` ·
`imports-only` · `state-removal-only` · `guard-removal-no-live-change`

T20 #22 d5's matrix row for the exceptional-change declared-change PR fixes:
introduce `creates-only`; retire `deletes-only` with T06's destroy acknowledgement;
group-key rename `empty`. Nothing here alters that contract; the
`state-removal-only` activation gate (the unverified `forget` representation) and
the dormant rehearsal classes remain exactly as T20 d5/d7 and T14 #19 record them —
open and unadvanced.

## 4. Enforcement split (structural schema vs R2 validator)

- **Structural enforcement lives in the JSON Schemas** via `required`,
  `additionalProperties: false`, `const`, `enum`, `pattern`, and conditional
  (`if`/`then`) keywords, and is exercised by the T14 #19 validator applying these
  schemas at the hermetic validation stage (`GOV-DECLARATION`). JSON Schema `format`
  is **not** relied upon anywhere: under the pinned toolchain
  (`jsonschema == 4.23.0`, specification §8.1) `format` is annotation-only by
  default, so every structural constraint uses assertion keywords.
- **The RFC 3339 UTC representation is enforced structurally by regex pattern**
  (digit-shape, `T`/`Z` designators, optional fractional seconds). The pattern does
  not assert calendar validity (an impossible date can match); **calendar-validity
  parsing is the R2 #27 validator's duty at the validation stage** (clock-free,
  hermetic — T22 #21 d4's boundary), and **validity-window evaluation**
  (expired / not-yet-valid) **is the plan stage's** (`GOV-DECL-MATCH`; the clock
  lives at plan/apply only).
- Every cross-artifact and lifecycle check — trusted-base membership, kind/phase/
  path/scope matching, prerequisite completion evidence, expiry — is plan-gate work
  (`GOV-DECL-MATCH`), exactly as T06 d5 and T14 #19 assign it. The schemas never
  claim it.

## 5. Conformance-correction ledger and lifecycle re-entry

Recorded as corrections to an already-ratified rule — not architectural questions.
After this record merges at its narrow ⟦G-Accept⟧, the work item resumes its
decision-gated lifecycle where it halted:

1. **S7 correction pass** on `ticket/r1-foundation-and-contracts`, keeping the two
   schema copies byte-identical and re-running the R1 mechanical checks:
   - **D1** — `group-key-rename` schemas: replace the unratified
     `expected_plan_effect_class` constant `zero-aws-mutations` with the T20 #22 d5
     token `empty` (both copies).
   - **D2** — `permission-set-key-replacement` schemas: constrain
     `expected_plan_effect_class` per phase (`introduce` ⇒ `creates-only`;
     `retire` ⇒ `deletes-only`) via schema conditionals (both copies).
   - **D3** — `principal-replacement` schemas: constrain
     `expected_plan_effect_class` to the §3 closed vocabulary (enum), leaving the
     declared value to plan-gate matching (both copies).
2. **Narrow S8 revalidation** — E1 resumes the interrupted step, and this excursion
   halted S8: `codebase-design` re-runs in validate mode, narrowly, against this
   ratified table and the corrected schemas.
3. **S9 begins only after that S8 revalidation passes.**

No other schema, routing, ownership, or layout change is authorized by this record.

## 6. Provenance

Halt-don't-decide excursion E1 from the S8 `codebase-design` validate review of
R1 #26: the S8 verdict surfaced the unratified declaration-vocabulary seam and the
D1–D3 conformance defects; the three decision questions were presented as one
numbered batch (repository-owner operating guide, governing invariant 3) and Eric —
human architect and repository authority — approved directions Q1-A, Q2-A, and Q3-A
on 2026-08-28. The S8 package review then surfaced the Pre-Baseline routing
question; Eric decided on 2026-08-29 (Q-AV1/Q-AV2/Q-AV3): Pre-Baseline E1 decisions
are ratified through a narrow ⟦G-Accept⟧ with no Architecture Version advance, the
Skill Execution Map is corrected accordingly (accepted alongside this record), and
the Status Artifact lists this record as another narrowly accepted Pre-Baseline
correction record with all baseline/version conditions remaining `none`. Q3-A
ratifies the retire-phase fields **as rendered** (required when `phase: retire`);
no structural prohibition during `phase: introduce` is ratified or implied.

**Domain-model check (`domain-modeling`, applied 2026-08-29):** terms reviewed
against the domain glossary (`CONTEXT.md`): *Change declaration*, *Review class*,
*Principal (ownership registry)*, *Plan-effect classification*, *Domain decision
register*. Result: no conflict — this record's usage matches each definition
exactly; the ratified field spellings are executable configuration vocabulary, not
ubiquitous language, and the glossary's own navigation-exemption rule keeps
implementation detail out of `CONTEXT.md`; therefore **no `CONTEXT.md` term is
added or changed and no domain ADR is touched**. The ADR triple-test (hard to
reverse / surprising without context / real trade-off) fails on all three arms —
the renderings are reversible by a future governed correction, self-explaining from
this record, and mechanical. The only methodology-side change is the separately
scoped one-sentence Skill Execution Map correction (Q-AV2), an owner-approved
methodology edit, not a domain ADR.

This record was prepared under `grilling` (decision phase) and `to-spec-repo-owner`
(consolidation mode; no decision reopened; authority by reference), with
`domain-modeling` applied as above. Repository authority changes only at Repository
Gates: until the owner's hash-bound narrow ⟦G-Accept⟧ authorization and merge, this
record is a proposal, not repository truth.
