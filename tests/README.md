# tests/

Executable validation tests and specimens (ADR-0003; T04 #6 decision 1). Contents are
governed by the T14 #19 validation contract: the per-code fixture tree
`tests/fixtures/{valid,invalid/<CODE>}/` lands with R2 #27. R1 #26 contributes only the
mechanical schema-conformance and governance-routing coverage checks
(`test_schema_validation.py`, `test_declaration_schema_identity.py`,
`test_governance_routing.py`); the validator itself is R2 work and no fixture specimen
exists yet.
