# tests/

Executable validation tests and specimens (ADR-0003; T04 #6 decision 1).
Contents are governed by the T14 #19 validation contract. Run with the pinned
toolchain (`jsonschema == 4.23.0`, `PyYAML == 6.0.2`; specification §8.1,
hash-locked in `src/requirements.txt`): `python -m unittest discover -s tests`.

## Suites

- `test_schema_validation.py` — R1 #26 row-2 mechanical check: every committed
  governed file validates against its schema, hermetically.
- `test_declaration_schema_identity.py` — R1 #26 row-8 check: the wired
  declaration schemas are byte-identical to the authored row-2 copies.
- `test_declaration_schemas.py` — R1 #26 correction-pass checks (D1–D3 of the
  declaration-vocabulary amendment): plan-effect-class constraints of the
  three declaration kinds.
- `test_governance_routing.py` — R1 #26 row-8 routing-table coverage: every
  tracked path resolves; unrouted paths fail closed (the tracked-path sweep
  needs `git` and skips inside the pinned container).
- `test_validator_catalogue.py` — R2 #27 row-3/row-4: the implemented
  catalogue equals the T14 #19 catalogue exactly (79 codes, 13 families,
  severities, exhaustive stage lists); catalogue self-validation fails closed.
- `test_validator_findings.py` — R2 #27 row-3: the T14 #19 d9/C14
  finding-record contract (canonical seven-key total ordering, deterministic
  duplicate collapse, `[omitted]` sentinel, global-finding representation,
  byte-deterministic serialization, escaped rendering).
- `test_validator_runner.py` — R2 #27 row-3: the validator run seam (closed
  stage vocabulary, hermetic validation boundary, deterministic output) and
  the `INV-PUBLIC-LEAK` rule with exactly its single ARN exemption.
- `test_validator_access_families.py` — R2 #27 row-4: the KEY / ASN / P-OOS /
  CFG families at their canonical layers, including the approved
  `{ASN-SHAPE, P-OOS-USER}` pair and the fixed out-of-slice wording.
- `test_validator_governance_families.py` — R2 #27 row-4: the FIX / GOV / DOC
  families, the fixture-surface INV validation arms, and the generated-ci
  `GOV-CODEOWNERS` agreement check.
- `test_validator_plan_stage.py` — R2 #27 row-4: the plan/apply battery over
  the explicit plan-context input — the INV snapshot/live verification
  classes, the PRQ prerequisite gate, the `KEY-PROTECTED` pre-existing arm,
  and the plan-side GOV codes (`GOV-DECL-MATCH`, `GOV-ENFORCEMENT`,
  `GOV-APPROVAL-CLASS`).

- `test_validator_adm.py` — R2 #27 row-5: the T21 #20 d6 five-rule hazard
  detector (`ADM-CAPABLE`), the T07 #9 cross-file pair (`ADM-STANDING`), and
  fail-closed catalog integrity (`ADM-CATALOG`; rules 2/4 data-blocked until
  the row-6 catalogs exist with matching digests).

- `test_catalog_generation.py` — R2 #27 row-6: pre-parse §7.1 blob-hash
  verification (fail closed), the deterministic §7.3 transformation, §7.4
  canonical output form, regeneration byte-determinism, the committed
  catalog reference pins, and the executability of ADM rules 2/4 (the
  blob-reading sweeps need `git` and skip inside the pinned container).

The per-code fixture tree `tests/fixtures/{valid,invalid/<CODE>}/` lands with
R2 #27 row 7.
