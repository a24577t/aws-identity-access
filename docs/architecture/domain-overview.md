---
status: accepted
decided: 2026-08-28
authority: normative
scope: the slice-A domain architecture of aws-identity-access — what this repository owns, consumes, and deliberately excludes
decision_owner: "Eric — human project owner and decision authority"
---

# Domain overview — slice A

This document synthesizes the accepted slice-A architecture with precise citations. It
creates no decision: authority lives in the domain decision register
([`docs/adr/`](../adr/README.md)), the closed Wayfinder records
([`docs/wayfinding/`](../wayfinding/README.md), cited at their commits), and the pinned
aws_ami platform architecture at `5f3cb7163f468730fd2ceb5d565c90b0bfda6099` (T01 #2),
cited by stable identifier and never restated as independently owned rules.

## What this repository is

Durable AWS access governed as configuration (pinned `01-repository-boundaries.md`;
platform `CONTEXT.md` *Durable access*): IAM Identity Center workforce-group references,
permission sets, and standing account assignments that persist until removed through a
governed PR. Slice A (ADR-0004) instantiates the smallest end-to-end vertical: two
permission sets, GROUP-only assignments to two named lab accounts plus one deferred
`status: requested` target, and the instance declaration — under the T02 #3 staged-lab-
apply deployment mode (validation → saved plan → explicit approval → that exact plan
applied to explicitly named lab accounts; never production).

## The requester surface

Ordinary access requests are PRs confined to `access/` (ADR-0003). The governed file
forms — `groups/`, `permission-sets/`, `account-assignments/`,
`configuration/instance.yml` — are specified by the
[configuration contract](configuration-contract.md). Review is derived, never
requester-authored: declared ownership routes to independent review classes through the
`governance/ownership/` registry, enforcement is evidenced per control, and saved-plan
apply authorization is a separate act (T06 #8 decisions 1–4). PR classification and
permitted plan effects are fixed by the T20 #22 contract.

## The federated identity chain, as instantiated here

Identity originates in the connected identity source (the Identity Center default store in
the lab; an enterprise IdP in the target), flows through workforce groups this repository
**references but never creates** (ADR-0007), and lands as permission-set assignments in
explicitly named accounts. The identity chain of pinned I-1 holds throughout: paths locate
things for people; governed configuration holds the authoritative keys; generated AWS
identifiers (GroupIds, permission-set ARNs, `AWSReservedSSO_*` roles) are outputs and
never repository identity (T05 #7 decisions 2–3).

## The manual-prerequisite model

The Identity Center instance, its identity store, the delegated administrator, and every
referenced group are manual prerequisites, consumed as declaration plus evidence
(ADR-0005): `instance.yml` declares; the non-public binding snapshot and Prerequisite
Verification Record evidence (T09 #12; T22 #21 decision 5); freshness gates plan and
apply, fail-closed (ADR-0006). API-verifiable prerequisites are re-verified live at every
plan and apply; console-only observations are human attestations, bound and never upgraded
to API-verified fact (T22 #21 decision 3).

## Profile versus domain

The **domain architecture** defines what forms exist; the **selected-slice validation
profile** narrows what slice A accepts (T03 #4 glossary; ADR-0004). Profile rejections
(`P-OOS-*`) say "out of slice A — not prohibited by the domain architecture" (T21 #20
decision 7): customer-managed policy references, permission boundaries, USER principals,
non-default identity-source types, additional policy forms, and the six absent surfaces
remain admissible to future slices only through governed decisions.

## Standing administrator access

Prohibited (ADR-0008). Slice A proves the negative path only: the deterministic,
conservative standing-admin-capability hazard detector (T21 #20 decision 6) and the
cross-file standing condition (T07 #9 decision 2) reject admin-capable definitions and
standing assignments under `ADM-*` codes, with detector rules 2/4 fail-closed until the
S5-selected catalog data exists (T14 #19 decision 5; the
[engineering specification](../specifications/slice-a-engineering-specification.md) §7
selects it).

## Repository-boundary counterexamples (what deliberately lives elsewhere)

Per pinned `01-repository-boundaries.md`, cited — this repository never owns:

- **Temporary elevation, runtime grants, sessions, credentials, delegation workflows,
  break-glass execution** — `aws-privileged-access`; elevation materialization (OD-05) is
  decided platform-side. This repository records only the durable constructs and the
  future dependency (ADR-0008).
- **Organization inventory authority — accounts, OUs, SCP/RCP, delegated-admin
  designation** — `aws-organization-governance`; this repository consumes inventory by
  alias under the T09 #12 pinned-snapshot contract and never maintains an authoritative
  copy (pinned I-4).
- **Workload-coupled execution roles** — workload repositories; the promotion threshold
  (OD-10) is platform-side.
- **Tier-0 pipeline provisioning, state backend, execution principal, provider pinning**
  (OD-03/04/09) — upstream; the lab substrate reuse is a recorded lab-only exception
  (T02 #3; T15 #10), never precedent.

## Environments and evidence

The lab contract (T15 #10) fixes account classes, the `us-east-1` regional rule, distinct
plan/apply OIDC roles, the permitted-mutation boundary (ADR-0009), `ialab-` naming, the
zero-incremental-spend cost boundary, three-tier evidence with alias-only public
artifacts, and Terraform `1.15.7` / `hashicorp/aws 6.53.0` pins. The lab topology is the
T16 #11 target reached only through its staged, separately authorized remediation; the
inventory consumption contract is T09 #12. Live identifiers never appear in public
content; `INV-PUBLIC-LEAK` (T14 #19 decision 4) is the single serialization-time leak
code, with the partition-qualified AWS-managed-policy ARN vocabulary as its only
exemption (T21 #20 decision 2).

## Validation and CI

The complete slice-A validation contract is the T14 #19 79-code catalogue (13 families,
78 active, 1 dormant) with the closed severity vocabulary `error | warning | deferred`,
exact stage attribution over `validation | plan | apply | generated-ci`, the hermetic
validation boundary, per-code deterministic fixtures, and the redaction-safe finding
contract. CI classification, the effective-access plan, the two-layer plan-effect
classifier, and the generated-artifact metadata contract are T20 #22. The
[configuration contract](configuration-contract.md) binds these to the governed file
forms; the [engineering specification](../specifications/slice-a-engineering-specification.md)
carries them to S6 implementation. Three empirical conditions remain open and unadvanced
— provider execution in the designated lab-CI boundary, the pinned-provider `forget`
representation, and `change.importing.id` redaction — gating execution-readiness claims,
the `state-removal-only` class, and every rehearsal activity (T20 #22 decision 7;
T21 #20 decision 8; T14 #19 decision 7).

## Brownfield stance

The first slice is greenfield-only with pre-existing resources protected (ADR-0004,
ADR-0009); the implementation stays brownfield: adoption occurs only inside a separately
authorized post-acceptance import-rehearsal phase and target waves, per the T19 #14
strategy and the
[brownfield implementation plan](../specifications/brownfield-implementation-plan.md).
