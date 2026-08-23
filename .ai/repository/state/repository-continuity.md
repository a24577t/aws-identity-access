# Repository Continuity Artifact

- **Created:** 2026-08-23

## Resume Context

- Status Artifact: [STATUS.md](STATUS.md).
- Wayfinder map #1 — in-flight position: Skill Step **S2** (working the map):
  https://github.com/a24577t/aws-identity-access/issues/1
- Skill governance: [Skill Execution Map](../methodology/skill-execution-map.md),
  [wayfinder-repo-owner](../../../.claude/skills/wayfinder-repo-owner/SKILL.md), and the
  HITL batch-question directive (governing invariant 3 in the
  [repository-owner operating guide](../../repository-owner/operating-guide.md)).
- Wayfinder result records: [`docs/wayfinding/`](../../../docs/wayfinding/README.md) — the T10
  record is
  [`docs/wayfinding/map-1/15-group-and-user-assignment-identity-and-filename-rules.md`](../../../docs/wayfinding/map-1/15-group-and-user-assignment-identity-and-filename-rules.md)
  (commit `31ace74`); T19 is
  [`docs/wayfinding/map-1/14-brownfield-adoption-and-migration-strategy.md`](../../../docs/wayfinding/map-1/14-brownfield-adoption-and-migration-strategy.md)
  (commit `e7f7e33`); T08 is
  [`docs/wayfinding/map-1/13-domain-decision-register-form.md`](../../../docs/wayfinding/map-1/13-domain-decision-register-form.md)
  (commit `c970244`); T09 is
  [`docs/wayfinding/map-1/12-organization-inventory-transport-and-snapshot-contract.md`](../../../docs/wayfinding/map-1/12-organization-inventory-transport-and-snapshot-contract.md)
  (commit `16522a4`); T16 is
  [`docs/wayfinding/map-1/11-lab-account-topology-and-fixtures.md`](../../../docs/wayfinding/map-1/11-lab-account-topology-and-fixtures.md)
  (commit `d357db7`); T15 is
  [`docs/wayfinding/map-1/10-lab-environment-test-and-deployment-contract.md`](../../../docs/wayfinding/map-1/10-lab-environment-test-and-deployment-contract.md)
  (commit `62b76c4`); T07 is
  [`docs/wayfinding/map-1/09-standing-administrator-access.md`](../../../docs/wayfinding/map-1/09-standing-administrator-access.md)
  (commit `8530c46`).

## Work Not Yet Committed

- None in the working tree. The in-flight work is the map itself, which lives in the tracker
  (pointers above); this artifact only bridges the S2 position that STATUS does not yet
  represent (STATUS reconciles at the next Repository Gate). The T04 prototype lives on the
  throwaway branch `prototype/t04-layout` (context pointer on #6), never on `main`; its
  assignment stubs are superseded by the T10 record specimens.

## Outstanding Decisions

- The open child tickets of map #1 (sub-issues with native blocked-by dependencies):
  https://github.com/a24577t/aws-identity-access/issues/1
- Frontier after T10: T21 #20 is first in map order and is unclaimed; T22 #21 and T23 #23 are
  also unblocked. T20 #22 (two open blockers: #20, #21) and T14 #19 (three: #20, #21, #22)
  remain blocked.
- T23 #23 must close before S5 consolidation; it blocks no other ticket.
- Result-record backfill for T01–T06 and T11–T13 is a T08 decision 13 prerequisite for S5:
  separately authorized by Eric before it may begin; **not begun** — no backfill file exists.
- The T19 import rehearsal, its seeds, drift probe, restoration, rollback/re-import
  transitions, and cleanup are all post-POC-acceptance activities, each requiring separate Eric
  authorization (T19 decisions 2 and 16); nothing is authorized by the map. The lab has no AWS
  Organization or Identity Center instance (T16 discovery, 2026-08-23); all lab provisioning is
  separately authorized S6 remediation per T16 decision 11; the T09 binding snapshot contract
  is exercised only at Stage 6.1/6.3 under separate authorization; no AWS call, S3 write, or
  evidence creation is authorized by the map.
- Upstream proposals carried by Eric (not yet carried): document 09 (T02), document 05 (T02),
  document 02 (T05), document 07 (T04, extended by T10 with the per-account-identity /
  OU-planning-input sentence), documents 01/11 (T07), OD-21 (T09), RD-09 clarification (T08).
  OD-09 and OD-12 remain open platform-wide (T19 decision 20 makes OD-12 resolution or an
  owner-approved interim protocol a target-wave-0 prerequisite). `aws_ami` is never edited by
  this repository. T08 decision 8 requires an informative
  `docs/architecture/upstream-proposals.md` index no later than the S5 acceptance branch.

## Recommended Next Activity

1. Run Session Bootstrap.
2. Consume this artifact.
3. Load map #1.
4. Claim and work T21 #20 (https://github.com/a24577t/aws-identity-access/issues/20) under
   `wayfinder-repo-owner`, applying the document-grounded rule as its claims require and the
   HITL batch directive; record its result under `docs/wayfinding/map-1/`.
5. One HITL ticket for the session.

## Notes

- Tracker writes use only the active `a24577t` keyring `gh` login; remove `GITHUB_TOKEN` and
  `GH_TOKEN` from every `gh` command's environment and never inspect token values.
- Read-only AWS discovery, when separately authorized, uses the established named lab profile
  with every identifier masked before output; no AWS mutation is authorized during Wayfinder.
  The T02 (#3) deployment mode, the T15 (#10) contract, the T16 (#11) topology, the T09 (#12)
  snapshot contract, the T19 (#14) adoption/migration strategy, and the T10 (#15) assignment
  rules are targets, not authorizations. Nothing in GitHub (protections, environments,
  secrets, workflows) has been configured by the map; T06's mechanisms and T15's minimum
  control set are proposals for S5/S6 under separate authorization.
