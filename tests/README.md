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

The per-code fixture tree `tests/fixtures/{valid,invalid/<CODE>}/` lands with
R2 #27 row 7.
