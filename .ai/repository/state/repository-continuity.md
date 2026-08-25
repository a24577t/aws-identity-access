# Repository Continuity Artifact

- **Created:** 2026-08-24

## Resume Context

- Status Artifact: [STATUS.md](STATUS.md).
- Wayfinder map #1 — in-flight position: Skill Step **S2** (working the map):
  https://github.com/a24577t/aws-identity-access/issues/1
- Skill governance: [Skill Execution Map](../methodology/skill-execution-map.md),
  [wayfinder-repo-owner](../../../.claude/skills/wayfinder-repo-owner/SKILL.md), and the
  HITL batch-question directive (governing invariant 3 in the
  [repository-owner operating guide](../../repository-owner/operating-guide.md)).
- Wayfinder result records: [`docs/wayfinding/`](../../../docs/wayfinding/README.md) — the T20
  record is
  [`docs/wayfinding/map-1/22-ci-plan-contract-and-pr-classes-for-slice-a.md`](../../../docs/wayfinding/map-1/22-ci-plan-contract-and-pr-classes-for-slice-a.md)
  (commit `87dedbce41beb0213579d2c4fc62fe9556850f91`); T23 is
  [`docs/wayfinding/map-1/23-normative-document-header-and-slice-a-documentation-set.md`](../../../docs/wayfinding/map-1/23-normative-document-header-and-slice-a-documentation-set.md)
  (commit `063a827`); T22 is
  [`docs/wayfinding/map-1/21-manual-prerequisites-as-governed-configuration-and-evidence.md`](../../../docs/wayfinding/map-1/21-manual-prerequisites-as-governed-configuration-and-evidence.md)
  (commit `6f2d84f`); T21 is
  [`docs/wayfinding/map-1/20-permission-set-policy-representation-for-slice-a-aws-managed-attachment-and-embedded-inline-policy.md`](../../../docs/wayfinding/map-1/20-permission-set-policy-representation-for-slice-a-aws-managed-attachment-and-embedded-inline-policy.md)
  (commit `6129808`); T10 is
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
- Frontier after T20: **T14 #19 is the final open child of map #1, unblocked (zero open
  blockers), and unclaimed.** After T14 resolves, the frontier is empty and the map proceeds
  to S3 (close map) per the Skill Execution Map.
- The T20 CI plan contract and PR classes are targets, not authorizations: no workflow,
  environment, ruleset, CODEOWNERS, classifier, generator, or manifest exists or is
  configured; the contract governs implementation/change PRs after ⟦G-Verdict⟧ /
  ⟦G-Accept⟧ and never retroactively classifies the Wayfinder record and continuity
  commits. **Three mandatory open conditions carried explicitly:**
  1. **Provider-execution gate:** authoring-host execution of the pinned AWS provider
     remains NOT RUN/BLOCKED; lab-CI execution remains unverified until executed in the
     designated lab-CI boundary; documentary CV-07 evidence is not S6 execution readiness.
  2. **`forget`-representation activation condition:** Terraform-core `1.15.7`
     documentary/offline evidence (T21 F8) demonstrates the `forget` plan-JSON action
     spelling for `removed { lifecycle { destroy = false } }`; the representation with the
     pinned AWS provider in the designated fixture/lab-CI boundary remains empirically
     unverified; any divergent or unsupported representation fails closed; the dormant T19
     `state-removal-only` class cannot activate until that verification passes.
  3. **Import-redaction gate:** `change.importing.id` rendering, sensitivity, and redaction
     remain a separate OPEN verification — no T19 rehearsal, and no activation of the
     dormant rehearsal PR classes, until it passes with empirical evidence.
- The T23 documentation-set and header decisions are targets, not authorizations: no
  document of the set exists — the two normative documents, the five guides, and the
  informative upstream-proposals index are S5 activities on the acceptance branch under the
  gate; generated content arrives only with the S6 tooling; nothing under
  `docs/architecture/`, `docs/guides/`, `docs/adr/`, or `docs/generated/` is created before
  then.
- No committed `instance.yml` exists: the T22 field set and verification-block structure are
  proposals; the file lands at S6 under the accepted layout (T22 record, authorization scope).
  The first Prerequisite Verification Record and binding snapshot exist only after the
  separately authorized T16 decision-11 Stage 6.1/6.3 sequence; no S3 write, AWS call, or
  evidence creation is authorized by the map.
- Result-record backfill for T01–T06 and T11–T13 is a T08 decision 13 prerequisite for S5:
  separately authorized by Eric before it may begin; **not begun** — no backfill file exists.
- The T19 import rehearsal, its seeds, drift probe, restoration, rollback/re-import
  transitions, and cleanup are all post-POC-acceptance activities, each requiring separate
  Eric authorization (T19 decisions 2 and 16); nothing is authorized by the map. The lab has
  no AWS Organization or Identity Center instance (T16 discovery, 2026-08-23); all lab
  provisioning is separately authorized S6 remediation per T16 decision 11; the T09 binding
  snapshot contract is exercised only at Stage 6.1/6.3 under separate authorization; no AWS
  call, S3 write, or evidence creation is authorized by the map.
- Upstream proposals carried by Eric (not yet carried): document 09 (T02), document 05 (T02),
  document 02 (T05), document 07 (T04, extended by T10), documents 01/11 (T07), OD-21 (T09),
  RD-09 clarification (T08), OD-08 (T22). None added by T21, T23, or T20; OD-09 and OD-12
  remain open platform-wide. `aws_ami` is never edited by this repository. T08 decision 8
  requires an informative `docs/architecture/upstream-proposals.md` index no later than the
  S5 acceptance branch.

## Recommended Next Activity

1. Run Session Bootstrap.
2. Consume this artifact.
3. Load map #1.
4. Claim and work T14 #19 (https://github.com/a24577t/aws-identity-access/issues/19) under
   `wayfinder-repo-owner`, applying the document-grounded rule as its claims require and the
   HITL batch directive; record its result under `docs/wayfinding/map-1/`. T14 is the final
   open child: its closure empties the frontier and routes the map to S3.
5. One HITL ticket for the session.

## Notes

- Tracker writes use only the active `a24577t` keyring `gh` login; remove `GITHUB_TOKEN` and
  `GH_TOKEN` from every `gh` command's environment and never inspect token values.
- Read-only AWS discovery, when separately authorized, uses the established named lab profile
  with every identifier masked before output; no AWS mutation is authorized during Wayfinder.
  The T02 (#3) deployment mode, the T15 (#10) contract, the T16 (#11) topology, the T09 (#12)
  snapshot contract, the T19 (#14) adoption/migration strategy, the T10 (#15) assignment
  rules, the T21 (#20) permission-set representation, the T22 (#21) manual-prerequisite
  model, the T23 (#23) header and documentation-set decisions, and the T20 (#22) CI plan
  contract and PR classes are targets, not authorizations. Nothing in GitHub (protections,
  environments, secrets, workflows) has been configured by the map; T06's mechanisms and
  T15's minimum control set are proposals for S5/S6 under separate authorization.
