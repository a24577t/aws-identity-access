# ADM catalog sources — `sri-20260828` (accepted, durable specification inputs)

The exact raw AWS Service Reference Information bytes from which both ADM action
catalogs generate. These five JSON files are **accepted, durable specification inputs**:
they land atomically in the ⟦G-Accept⟧ acceptance merge and remain available from the
repository alone — no review staging, local state, or network fetch is ever required to
reproduce the catalogs from a fresh clone.

The **normative contract** — the byte inventory (URLs, retrieval-evidence timestamps,
byte counts, SHA-256 values), the service-scope selection and exclusions, the
access-level transformation rule, canonicalization, generated paths, and fail-closed
behavior — is the
[engineering specification §7](../../../../docs/specifications/slice-a-engineering-specification.md);
this note adds only the handling rules:

- **Consumption:** the first catalog-production work item (specification §10 item 6)
  reads exactly these committed files, **verifies each file's §7.1 SHA-256 before any
  parse**, and never re-fetches; a mismatch aborts generation (fail closed) and routes
  to remediation.
- **Identity:** the SHA-256 of the exact bytes is the identity; retrieval timestamps are
  evidence only.
- **Immutability:** these files are never edited. Refreshing the catalog inputs means a
  platform-change PR adding a new `governance/catalogs/sources/sri-<YYYYMMDD>/` set with
  newly fetched, newly hashed bytes and repointing the specification's contract — never
  overwriting this set.
- **Generated outputs** (`governance/catalogs/action-catalog.json`,
  `governance/catalogs/privileged-mutation-actions.json`) live beside `sources/`, are
  produced only by the pinned generator, and are never confused with these raw inputs.
