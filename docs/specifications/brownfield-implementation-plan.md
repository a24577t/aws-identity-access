# Brownfield implementation plan

The T19 #14 decision-21 skeleton instantiated as the S5 plan, in its eleven mandatory
sections. Consolidation only: every section cites its deciding record, which prevails on
any divergence. This plan carries no authority header (T23 #23 decision 4 does not cover
`docs/specifications/`; no accepted rule requires specification frontmatter): its
authority derives from the approved ⟦G-Accept⟧ record and this repository placement.
Nothing here authorizes execution — every stage, increment, mutation group, and state
transition named below requires its own separate Eric authorization, and the import
rehearsal exists only after POC acceptance (T19 d2/d16).

## 1. Staged lab rollout (T15 #10 decision 14, verbatim items)

The S5 brownfield implementation plan includes: (1) a staged lab rollout — bootstrap →
validation → post-merge saved plan → approval → apply → verification → cleanup — each
stage under its own separate authorization, targeting aliased lab accounts only; (2)
verification criteria per stage; (3) a rollback procedure executed as a governed change;
(4) an explicit boundary between architecture evidence and lab-specific results, with
live lab identifiers confined to encrypted non-public evidence; (5) brownfield
discovery, import/reconciliation sequencing, destroy blocking, and migration planning per
document 09. Sequencing prerequisite: the T16 #11 decision-11 remediation Stages 0–6
(informed signup gate; management-account verification and Organization gate; lab OU and
sandbox invitation with billing verification; workload accounts; payer-level zero-spend
budget and Free Tier alerts before Identity Center; Identity Center, first group,
delegated administrator; read-only re-discovery before the binding record, bootstrap, or
any plan) — each step separately authorized. Stage-by-stage verification criteria are the
T16 d11 per-stage verifications plus the engineering specification's per-work-item
acceptance.

## 2. Dispositions and the migration note

The complete disposition table over the 104 T18 components, with per-row cited basis, is
T19 #14 decision 1, adopted here by citation; the retire rows and the nine rejected
conventions are presented in the
[migration note](../guides/migration-note.md) (content T19's; T23 fixes place and class).

## 3. The adoption pipeline (normative procedure; T19 decisions 3–15)

- **Discovery semantics and API limitations (d3):** fresh full-enumeration discovery per
  increment — definitions and policy content; provisioned-to-account relationships via
  `ListPermissionSetsProvisionedToAccount` cross-checked per set; current assignments;
  asynchronous operation records (never a durable status; `IN_PROGRESS` blocks; `FAILED`
  requires disposition); every list paginated to a null continuation token; re-verified
  at plan and apply of every increment.
- **Eligibility and the bundle (d4):** permission-set adoption bundles (core + applicable
  AWS-managed attachment or inline-policy resource — the core alone never claims
  zero-diff) and their GROUP assignments; lab rehearsal targets lab-workload accounts
  only; target waves only accounts admitted by the separately approved wave manifest;
  the exclusion list is a committed plan artifact.
- **Bounded ownership proof and manifest (d5, per C-B: the manifest schema is decision
  5's; `ADO-MANIFEST` validates it):** per-resource manifest entry with live identifiers
  in tier-2 evidence, alias, discovery pointers, authority-boundary justification,
  bounded negative ownership proof (exactly what was checked, when, with required
  attestations — never a universal nonexistence claim), intended post-adoption
  configuration, and per-increment Eric approval; ambiguity quarantines, never imports
  (d6).
- **Transition model (d7):** observed → imported (bundle authored to live state; import
  applied; mandatory zero-diff verification plan evidenced) → authoritative (drift policy
  applies; this repository becomes sole reconciliation owner — ADR-0001).
- **Increments and the import mechanism (d8):** configuration-driven `import` blocks in
  reviewed code only (CLI import prohibited); one bundle per imports-only increment,
  atomically core + policy child; assignments one per increment, bundles before
  assignments; import ids derived at plan time from encrypted non-public inputs — no
  live identifier committed; import blocks removed post-authoritative via
  no-operation cleanup PRs; pins used for imports only after T21/CV-07 verifies the
  exact import identities and rendering (gated by §8 conditions).
- **Plan-classification gates (d10; T20 d5):** imports-only, empty, state-removal-only,
  guard-removal-no-live-change, destroy-only cleanup, prohibited — with **no destroy
  exception inside the import phase**; `prevent_destroy` while managed; the
  protected-resource gate covers everything outside the increment.
- **State isolation (d9):** the `import-rehearsal` root and state key beside `bootstrap`
  and `identity-center`; no state surgery except explicitly planned, separately
  authorized steps with a recorded state-version backup reference.
- **Ordering and prerequisites (d11):** prerequisites verified first (instance reachable;
  every referenced group resolves — missing stops, never creates); bundle before its
  assignments; deferred targets never imported or provisioned.
- **Collision, rename, tags (d12):** live names kept at import — no rename-on-import;
  tags on permission sets only, and adding managed-by tags to an adopted set is a
  separate post-authoritative governed change; `ialab-` never applied retroactively.
- **Coexistence and freeze (d13):** per-resource cutover at *authoritative*; a declared
  change-freeze window per increment (evidenced Eric commitment in the lab; enforced
  control in the target); freeze violations abort.
- **Rollback, abort, quarantine (d14):** rollback is a governed state-only removal — the
  resource block replaced by exactly `removed { from = <address>  lifecycle { destroy =
  false } }`, the plan classifying state-removal-only and touching no live object;
  destroy is never a rollback mechanism; abort → rollback → quarantine with a fresh
  manifest required; partial increments receive recorded disposition and fresh
  authorization.
- **Evidence and acceptance (d15):** the T15 three-tier model per increment; state never
  in the evidence prefix (version reference + digest only); an increment without its
  complete evidence set is not accepted regardless of live outcome.

## 4. The lab rehearsal (T19 decision 16)

Seeded stand-ins (fresh lab Identity Center has no genuine legacy): two seed bundles —
one AWS-managed attachment, one embedded inline — each with one GROUP assignment to one
lab-workload account; two bundle increments then two assignment increments; then the
exercised transitions. **Separately authorized live-mutation groups, each its own
explicit Eric authorization:** (1) seed creation (outside Terraform); (2) the
privilege-neutral drift-injection probe; (3) governed restoration of that probe; (4)
post-exit seed cleanup — first the guard-removal no-live-change PR, then the separately
approved destroy-only saved plan (assignments before bundles). Rollback and re-import are
separately approved state transitions. Exit criteria: every increment met §3 acceptance;
one rollback and one re-import exercised with evidence; the probe detected, evidenced,
and reconciled through the governed path; no protected-resource event; the alias-only
rehearsal report produced. Cleanup failure never invalidates rehearsal evidence and never
permits manual deletion. **Precondition: the import-redaction gate has passed with
empirical evidence — until then no rehearsal activity of any kind (§8).**

## 5. Target waves (T19 decision 17)

Wave 0 — prerequisites proven: the T06 adoption guard fully verified (no grandfathered
lab exceptions); OD-03/OD-04 resolved or explicitly excepted by owner decision; OD-12
resolved or an owner-approved interim coupled-change protocol; the T09 pinned inventory
consumption live; discovery and freeze machinery in place. Wave 1 — permission-set
bundles. Wave 2 — assignments, one per increment, only manifest-admitted accounts,
workload before sensitive. Wave 3+ — deferred durable-access classes only after their
slices define architecture (sequencing reservation). Every wave runs the §3 pipeline and
closes only on acceptance evidence.

## 6. Naming, collision, and tags in the target (T19 decisions 12, 18)

Target `resource_name_prefix = "ia-"` for newly created resources — a coexistence marker
while repository-managed and unadopted legacy sets coexist; adopted resources keep their
names; revisiting the prefix after full cutover is a normal governed change recorded as
an open option; collisions remain protected-resource plan errors.

## 7. Rollback points and dispositions (T19 decision 14)

Per stage and increment as §3 fixes them; every abort/quarantine/partial-state event
receives a recorded disposition and fresh authorization before any further action.

## 8. Owner-approval checklist and the open gates

**Every separately authorized point, enumerated:** each T16 d11 stage (0.2, 1.3, 1.4,
2.1, 2.4, 2.5, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 5.3, 6.3); the S6 bootstrap control set;
each rehearsal seed creation; each bundle-import increment manifest; each
assignment-import increment; each rollback; each re-import; the drift probe; the probe
restoration; the guard-removal PR; the destroy-only cleanup plan; every retention or
disposition decision; every wave manifest; every pin change. **Open empirical gates
(binding, unadvanced):** provider execution in the designated lab-CI boundary; the
pinned-provider `forget` representation (the `state-removal-only` class cannot activate);
`change.importing.id` redaction (no rehearsal, no dormant-class or `ADO-MANIFEST`
activation). Pin freezes during waves and the CV-07 re-verification rule on any pin
change are T15 d13 / T19 d20.

## 9. Evidence and retention map (T19 decision 15; T09 decision 20)

Tier-2 non-public per increment (discovery snapshot + digest, manifest, saved-plan
digests, zero-diff plan, apply log references, rollback records, state-object version
references and digests — never state content); alias-only public summaries; retention at
least through the POC phase gate; deletion only by explicit Eric disposition after the
gate and closure of dependent plans.

## 10. Decommissioning schedule (T19 decision 19)

Per wave at cutover: the legacy change path formally retired and recorded; the bounded
ownership checks re-run (never a universal claim); post-cutover out-of-band changes are
drift by definition; the scaffold and exploratory trees retired as implementation sources
only — the pinned platform documents and register remain governing authority; state
retirement follows T15 d11 (retire ≠ delete).

## 11. Deferred-class reservation (T19 decisions 1, 17)

IAM users, roles, trust policies, boundaries, fleet mechanisms, identity-source desired
configuration, and runtime-mutation contracts stay deferred with their evidence preserved;
each returns only through a redrawn destination and its own architecture slice, entering
this plan at wave 3+.
