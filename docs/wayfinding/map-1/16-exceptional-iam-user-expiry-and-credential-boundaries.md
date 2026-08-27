---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 16
title: "T11 — Exceptional IAM-user expiry and credential boundaries"
url: https://github.com/a24577t/aws-identity-access/issues/16
type: grilling
lifecycle_status: closed
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner (T03 #4 revalidation)"
recorded: 2026-08-27
sources:
  backfill: "T08 #13 decision 13 result-record backfill (thin scope-closure record), reconstructed 2026-08-27 from the ticket; traceability, not authority"
  closure_comment: https://github.com/a24577t/aws-identity-access/issues/16#issuecomment-5382171151
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  closed: 2026-08-22 (as not planned)
---

# T11 — Exceptional IAM-user expiry and credential boundaries (closed Out of scope)

> **Backfilled thin scope-closure record** — produced 2026-08-27 under the separately
> authorized T08 #13 decision-13 backfill (T11–T13 as thin scope-closure records). T11 was
> **never resolved**: it was closed **Out of scope** (GitHub state `closed / not planned`,
> unassigned, unworked) by the T03 #4 revalidation under the map's Slice-first rule. The
> scope boundary itself is T03's decision; this record adds no decision and confers no
> authority. It is listed in the map's **Out of scope** section, not in Decisions so far.

## The question the ticket held (never worked)

What does an exceptional IAM user require, and what does "expired" mean — default and
maximum expiry, the credential-constraint vocabulary (console sign-in vs access keys, MFA,
rotation), the mandatory-permission-boundary claim, expiry semantics for validation, and the
OD-11 proposal to carry back to aws_ami? Document-governed context named on the ticket:
`01-repository-boundaries.md` (IAM users exceptional), root `CONTEXT.md` ("Exception"
class), OD-11 (open), `10-codeowners-model.md` (security approval without exception).
Blocked by T03 #4 and T06 #8.

## Closure (verbatim from the closure comment, 2026-08-22)

> **Out of scope — closed by T03 revalidation (#4).** T03 selected slice A (Identity Center
> only): the slice contains no IAM users, so exception expiry, credential constraints, and
> the OD-11 proposal are beyond this map's destination. OD-11 remains open upstream; the
> `Exception` class stays defined in aws_ami `CONTEXT.md`; the exclusion is recorded as a
> first-slice boundary in #4's resolution. Returns only with a redrawn destination.

## Status

Closed **Out of scope** by T03 #4 decision 7 (Slice-first rule); no decision was taken on
this ticket's question. OD-11 remains open platform-wide. The question returns only with a
redrawn destination, as a fresh effort. This backfill record changes nothing.
