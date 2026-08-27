---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 18
title: "T13 — Fleet roles: identical enterprise roles across many accounts"
url: https://github.com/a24577t/aws-identity-access/issues/18
type: grilling
lifecycle_status: closed
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner (T03 #4 revalidation)"
recorded: 2026-08-27
sources:
  backfill: "T08 #13 decision 13 result-record backfill (thin scope-closure record), reconstructed 2026-08-27 from the ticket; traceability, not authority"
  closure_comment: https://github.com/a24577t/aws-identity-access/issues/18#issuecomment-5382171492
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  closed: 2026-08-22 (as not planned)
---

# T13 — Fleet roles: identical enterprise roles across many accounts (closed Out of scope)

> **Backfilled thin scope-closure record** — produced 2026-08-27 under the separately
> authorized T08 #13 decision-13 backfill (T11–T13 as thin scope-closure records). T13 was
> **never resolved**: it was closed **Out of scope** (GitHub state `closed / not planned`,
> unassigned, unworked) by the T03 #4 revalidation under the map's Slice-first rule. The
> scope boundary itself is T03's decision; this record adds no decision and confers no
> authority. It is listed in the map's **Out of scope** section, not in Decisions so far.

## The question the ticket held (never worked)

How is "this role in every target account" expressed and deployed — residency, the targets
grammar (explicit account list vs OU expansion that must resolve to a reviewable account
list), the reconciliation-owner rule's interaction with T02, and whether the mechanism is in
the slice or deferred? Document-governed context named on the ticket:
`11-decision-register.md` and `01-repository-boundaries.md` (expected result for a fleet
mechanism: absent; REVIEW Q1), I-3 / `04-enforcement-plane-precedence.md` (Terraform-owned
StackSets as distribution), the T02 one-reconciliation-owner outcome. Blocked by T02 #3 and
T03 #4.

## Closure (verbatim from the closure comment, 2026-08-22)

> **Out of scope — closed by T03 revalidation (#4).** Slice A has no enterprise roles and
> uses no StackSets; fleet residency and the targets grammar are beyond this map. The T02
> (#3) rules — StackSets only at Preference 3, one reconciliation owner, explicit targeting
> visible in the plan — already bind any future fleet mechanism; T16 withdraws the
> fleet-target account row. Returns only with a redrawn destination.

## Status

Closed **Out of scope** by T03 #4 decision 7 (Slice-first rule); no decision was taken on
this ticket's question. The T02 #3 rules bind any future fleet mechanism; T16 #11 recorded
the fleet-target claim as void (claim 4). The question returns only with a redrawn
destination, as a fresh effort. This backfill record changes nothing.
