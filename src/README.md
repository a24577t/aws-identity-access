# src/

Validation and effective-plan implementation code (ADR-0003; T04 #6 decision 1),
governed by the T14 #19 validation contract. Landed through R2 #27 (validator
core, catalogue, code families, catalog generation), R3 #28 (plan-effect
classifier, effective-access generator, generated-governance generator), and
R4 #29 (CI wiring).

- `validator/` — the validator package: the 79-code catalogue and finding
  contract, the check families, the two-layer plan-effect classifier, the
  effective-access renderings, the catalog and governance generators, and
  `ci.py` — the thin command seams the committed workflows invoke
  (`python -m validator.ci`).
- `requirements.in` / `requirements.txt` — the §8.1 direct dependencies and the
  hash-locked set generated inside the pinned container; installs use only
  `pip install --require-hashes -r src/requirements.txt`. Regenerating the lock
  is a platform-change PR.
