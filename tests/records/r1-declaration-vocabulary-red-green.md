# S9 red/green record — R1 #26 declaration-vocabulary corrections (D1–D3)

Bounded red-first evidence for the S7 correction commit
`d7715240a607f79c4d18ab1370237a4e22b31198` on
`ticket/r1-foundation-and-contracts`, produced at S9 (`tdd`) after the narrow S8
revalidation PASS. Test seams are the S8-ratified ones only: declaration
instances validated through the public JSON Schema interface with the pinned
toolchain (`jsonschema == 4.23.0`, `PyYAML == 6.0.2`; specification §8.1). No R2
validator, `GOV-*` diagnostic, CLI, catalog, or runtime behavior is exercised or
implemented.

## Honest chronology

The correction tests (`tests/test_declaration_schemas.py`) and the D1–D3 schema
corrections entered the branch **in the same commit** (`d771524`); no separate
historical test-first commit exists, and none is claimed. The red evidence below
is a **parent-state replay**: the committed test bytes (verified SHA-256-identical
to blob `d771524:tests/test_declaration_schemas.py`) were run against the
pre-correction schemas of parent `e8eb28d629c9c4e6261a36b010620aa3cf108ada` in an
isolated scratch export (`git archive`), outside the ticket working tree. This
replay is the retained discriminatory red record for S9. To the extent the
red-first rule expects a chronological pre-implementation red, that narrow
process deviation is recorded here rather than reconstructed by history rewrite;
the deviation is bounded to mechanical conformance corrections whose target
constants were fixed in advance by the accepted declaration-vocabulary amendment.

## RED — committed tests vs pre-correction schemas (parent `e8eb28d`)

`python -m unittest tests.test_declaration_schemas` → **11 tests, FAILED
(failures=23)** — five failing test methods, each discriminating exactly one
correction:

| Correction | Failing evidence (pre-correction behavior) |
|---|---|
| D1 | `test_empty_accepted` FAIL (schema demanded the unratified `zero-aws-mutations`, rejecting `empty`); `test_old_token_rejected` FAIL (old token accepted) |
| D2 | `test_introduce_other_classes_rejected` FAIL × 8 subtests; `test_retire_other_classes_rejected` FAIL × 8 subtests (no per-phase class constraint existed) |
| D3 | `test_values_outside_vocabulary_rejected` FAIL × 5 subtests (`zero-aws-mutations`, `replace`, `creates_only`, `EMPTY`, `no-op` accepted; only the empty string was already rejected via `minLength`) |

Every test that passed in the replay covers behavior already correct before the
correction (retire-required fields; introduce non-prohibition of retire fields;
`""` rejection) — the suite discriminates the corrections and nothing else.

## GREEN — same tests vs HEAD `d771524`

`python -m unittest tests.test_declaration_schemas` → **11 tests, OK**.

## Full R1 mechanical suite vs HEAD `d771524`

`python -m unittest discover -s tests` → **28 tests, OK** (schema
self-validation and conformance, filename/agreement checks, routing coverage
with fail-closed demonstrations, authored/wired byte identity, D1–D3 coverage).

## Workspace hygiene

The replay export was created and removed in the session scratchpad; the ticket
working tree remained clean throughout (verified before and after; no worktree
registered). No production byte changed at S9.
