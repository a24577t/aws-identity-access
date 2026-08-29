# governance/change-declarations/

One schema-validated file per active exceptional change:
`<declaration-key>.yml` — governed intent, never approval evidence
(T06 #8 decision 5). No declaration is active in slice A; the first declaration
lands only through the decision-5 lifecycle (preparatory declaration PR → the
exceptional change PR(s) referencing the merged declaration → terminal cleanup
PR after completion evidence).

## Wiring

A declaration is discriminated by its `kind` field and validated against the
matching schema under [`schemas/`](schemas/):

| `kind` | Schema |
|---|---|
| `principal-replacement` | [`schemas/principal-replacement.schema.json`](schemas/principal-replacement.schema.json) |
| `group-key-rename` | [`schemas/group-key-rename.schema.json`](schemas/group-key-rename.schema.json) |
| `permission-set-key-replacement` | [`schemas/permission-set-key-replacement.schema.json`](schemas/permission-set-key-replacement.schema.json) |

The schema content is authored once under
[`schemas/governance/change-declaration/`](../../schemas/governance/change-declaration/)
(R1 #26 row 2) and placed here byte-for-byte (row 8); byte identity is asserted
by `tests/test_declaration_schema_identity.py`, and the configuration contract
prevails over both copies. Schema violations are `GOV-DECLARATION`; plan-gate
matching is `GOV-DECL-MATCH` (T14 #19).
