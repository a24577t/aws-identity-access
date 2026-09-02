# Lesson learned — slice A scope divergence and assurance cost

**Date:** 2026-09-02  
**Type:** Informative retrospective; not architecture or methodology authority  
**Subject:** Why implementation of the AWS identity-access POC concentrated on a
narrow foundation while much of the intake brief remained deferred

## Observation

The repository has produced a rigorous foundation for governed AWS Identity
Center access: repository structure, schemas, validation, diagnostics,
ownership and routing, plan classification, effective-access reporting, and
generated governance. At this point, however, several prominent capabilities
from the original `aws-identity-access-poc-prompt.md` remain outside slice A:
native IAM users and groups, IAM roles and trust policies, permission-boundary
and credential controls, fleet roles, StackSets, and their executable examples.

The work is useful foundation, but the ratio of governance and assurance work
to delivered breadth is higher than the original POC intent warranted.

## Root cause

The primary cause was not testing alone. It was the interaction of a narrowed
destination with a methodology that rigorously proves arrival at the selected
destination but does not require the destination to preserve adequate coverage
of the initiating brief.

The sequence was:

1. The broad intake brief entered Wayfinder.
2. The destination was narrowed to slice A, Identity Center only.
3. IAM users, roles, trust, fleet deployment, and StackSets became out of scope
   for that destination.
4. The map exhaustively resolved the decisions needed for the narrow
   destination.
5. The Architecture Grill and specification gates checked internal coherence,
   but no gate required a coverage ledger back to the original brief.
6. S6 consumed the approved narrow breakdown one-to-one.
7. Every resulting implementation ticket entered the full S7–S11 assurance
   chain before the project reached live end-to-end AWS execution.

The project decision that established the narrow boundary is ADR-0004. The
methodology did not require that decision; it did, however, lack a guardrail
against narrowing away too much of the original value proposition.

## Methodology contributors

### 1. Destination-controlled scope without brief-coverage accounting

Wayfinder correctly makes the destination control the map and treats work past
the destination as out of scope. It does not also require each important intake
requirement to be classified as delivered, foundational, deferred to a named
successor, or rejected with owner rationale. Consequently, a central intake
requirement can disappear from the active delivery path while the map remains
formally complete.

### 2. No destination-adequacy gate

S3–S5 establish that the way is clear, the proposal is architecturally sound,
and the specification faithfully consolidates accepted decisions. They do not
ask whether the selected destination proves a representative end-to-end portion
of the initiating product thesis.

### 3. Architecture before executable feedback

The main path completes map discovery, an Architecture Grill, verdict approval,
specification consolidation, and acceptance before implementation starts. An
executable spike is available as a Wayfinder technique but is not a required
checkpoint. In this project, live AWS proof was placed near the end of the work
graph, after substantial investment in contracts and validators.

### 4. One-to-one consumption of the accepted breakdown

S6 consumes the approved specification breakdown one-to-one. This is valuable
for traceability, but it also makes omissions in the accepted specification
mechanically persistent. Downstream implementation cannot recover deferred
brief coverage without a new governed effort.

### 5. Full assurance chain for every implementation ticket

Each ticket runs S7 implementation, S8 design validation, S9 evidence closure,
S10 three-axis review, S11 independent Quality Gate, and an owner merge. That
chain is appropriate for high-risk production changes but is expensive when
applied uniformly to every foundational POC ticket. Evidence reuse reduces
re-execution but does not remove the number of mandatory transitions.

### 6. Fine-grained session and publication boundaries

Wayfinder's one-HITL-ticket-per-session rule combined with repository bootstrap,
fail-loud preconditions, remote-write round trips, clean-close requirements, and
continuity handling produced significant transaction overhead. The underlying
continuity principles remain sound; the costly behavior came from applying
them at very small work boundaries.

### 7. Halt-and-ratify behavior for small contract gaps

Implementation correctly refuses to invent externally observable contracts.
In practice, small vocabulary and representation gaps triggered separate
ratification transactions. This protected authority but increased cost where a
risk-tiered or batched decision route could have remained safe.

### 8. Append-only correction cost

Once architecture was accepted, corrections were recorded as amendments rather
than edits. This preserves history, but repeated narrow acceptance transactions
added disproportionate cost during a POC whose architecture was still being
tested.

## What did not cause the divergence

Repository-authoritative memory, human-owned authority, fail-loud preconditions,
and honest evidence are not themselves the problem. They prevented state loss
and fabricated assurance. The problem was the granularity and topology through
which those principles were applied, plus the absence of intent-coverage and
delivery-economics checks.

## Corrective recommendations

1. **Add an intake-coverage ledger at S1.** Classify every material requirement
   as delivered by this slice, prerequisite foundation, deferred to a named
   later slice, or rejected with owner rationale.
2. **Require destination adequacy at S3/S4.** Confirm that the destination proves
   a representative end-to-end part of the original value proposition.
3. **Require ownership for deferred requirements.** Important out-of-scope work
   must retain a named successor effort and ordering rather than disappearing.
4. **Require an early executable spike.** Before exhaustive specification,
   exercise one minimal repository-to-validation-to-plan-to-lab path.
5. **Introduce lifecycle risk tiers.** Permit a combined verification gate for
   low-risk foundation tickets; reserve the full separated S8–S11 chain for
   architecture-bearing, security-sensitive, or externally mutating work.
6. **Allow bounded HITL batches.** Closely related decisions governed by the same
   evidence may resolve in one session while preserving explicit human answers.
7. **Add a cost/value statement to gates.** Record user-visible capability
   delivered, risk retired, remaining intake coverage, and expected lifecycle
   cost.
8. **Measure POC progress by executable scenarios.** Prefer proof that a group
   receives governed access, a role can be safely assumed, or an exceptional
   IAM user is fully controlled over counts of records, schemas, or gates.

## Delivery implication

Finish slice A with the smallest safe R4–R8 path needed to prove Identity Center
deployment and lab verification. The next slice should return directly to the
deferred intake intent with one complete IAM role and trust policy plus one
exceptional IAM user/group path, including Terraform, validation, plan output,
and lab evidence. Avoid another general discovery expansion unless executable
evidence exposes a genuine architectural question.

## Status of this lesson

This document records experience and proposed process improvements. It does not
modify accepted architecture, methodology, ticket scope, or repository state.
Any recommendation adopted as methodology must follow the repository-owner
methodology-change route and receive the applicable owner authorization.
