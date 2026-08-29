# schemas/

JSON Schemas for every governed configuration form (RD-04 at the pinned aws_ami
revision; ADR-0003), implementing the
[configuration contract](../docs/architecture/configuration-contract.md) exactly — the
schema is the contract's executable form and the contract prevails on any divergence.

| Governed form | Schema |
|---|---|
| `access/identity-center/groups/<group-key>.yml` | [`access/group.schema.json`](access/group.schema.json) |
| `access/identity-center/permission-sets/<permission-set-key>.yml` | [`access/permission-set.schema.json`](access/permission-set.schema.json) |
| `access/identity-center/account-assignments/<account-name>/<group-key>--<permission-set-key>.yml` | [`access/account-assignment.schema.json`](access/account-assignment.schema.json) |
| `access/identity-center/configuration/instance.yml` | [`access/instance.schema.json`](access/instance.schema.json) |
| Lab inventory fixture (T15 #10 d5; T16 #11 d7) | [`inventory/lab-inventory-fixture.schema.json`](inventory/lab-inventory-fixture.schema.json) |
| `governance/ownership/principals/*.yml` | [`governance/principal.schema.json`](governance/principal.schema.json) |
| `governance/ownership/review-classes/*.yml` | [`governance/review-class.schema.json`](governance/review-class.schema.json) |
| `governance/ownership/routing.yml` | [`governance/routing-table.schema.json`](governance/routing-table.schema.json) |
| `governance/change-declarations/*.yml`, `kind: principal-replacement` | [`governance/change-declaration/principal-replacement.schema.json`](governance/change-declaration/principal-replacement.schema.json) |
| `governance/change-declarations/*.yml`, `kind: group-key-rename` | [`governance/change-declaration/group-key-rename.schema.json`](governance/change-declaration/group-key-rename.schema.json) |
| `governance/change-declarations/*.yml`, `kind: permission-set-key-replacement` | [`governance/change-declaration/permission-set-key-replacement.schema.json`](governance/change-declaration/permission-set-key-replacement.schema.json) |

Schemas are JSON Schema draft 2020-12, self-contained (no cross-file `$ref`, no network
retrieval of meta-schemas), validated with the pinned toolchain
(`jsonschema == 4.23.0`, specification §8.1). The declaration-kind schemas are placed
and wired byte-for-byte under
[`governance/change-declarations/schemas/`](../governance/change-declarations/schemas/)
(R1 #26 row 8); constraints the records assign to the validator rather than the schema
(for example the documented AWS `PermissionSet.Description` character pattern,
`KEY-DESCRIPTION`, and the Unicode whitespace/control rules of `KEY-IDSTORE-NAME`) are
noted in `$comment` fields and enforced by the T14 #19 validator (R2 #27).
