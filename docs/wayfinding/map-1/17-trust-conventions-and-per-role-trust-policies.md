---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 17
title: "T12 — Trust conventions and per-role trust policies: a compatibility decision"
url: https://github.com/a24577t/aws-identity-access/issues/17
type: grilling
lifecycle_status: closed
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner (T03 #4 revalidation)"
recorded: 2026-08-27
sources:
  backfill: "T08 #13 decision 13 result-record backfill (thin scope-closure record), reconstructed 2026-08-27 from the ticket; traceability, not authority"
  closure_comment: https://github.com/a24577t/aws-identity-access/issues/17#issuecomment-5382171307
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  closed: 2026-08-22 (as not planned)
---

# T12 — Trust conventions and per-role trust policies (closed Out of scope)

> **Backfilled thin scope-closure record** — produced 2026-08-27 under the separately
> authorized T08 #13 decision-13 backfill (T11–T13 as thin scope-closure records). T12 was
> **never resolved**: it was closed **Out of scope** (GitHub state `closed / not planned`,
> unassigned, unworked) by the T03 #4 revalidation under the map's Slice-first rule. The
> scope boundary itself is T03's decision; this record adds no decision and confers no
> authority. It is listed in the map's **Out of scope** section, not in Decisions so far.

## The question the ticket held (never worked)

How do the standardized trust conventions `01-repository-boundaries.md` assigns to this
repository and complete, local per-role trust policies compose — the working hypothesis
(conventions as validated constraints/templates, each role file carrying its complete trust
policy that must satisfy them), where conventions are declared, the trust-shape catalogue
the slice needs (service principal, GitHub OIDC with pinned subjects, role-to-role by
account name, third-party with ExternalId, the "unsafe OIDC wildcard" rule), and what
validation rejects? Document-governed context named on the ticket: `01`,
`05-runtime-mutation-contracts.md`, `09-tier0-execution.md`; REVIEW Q6. Blocked by T03 #4.

## Closure (verbatim from the closure comment, 2026-08-22)

> **Out of scope — closed by T03 revalidation (#4).** Slice A contains no IAM roles; the
> trust-convention ↔ local-trust-policy question and the trust-shape catalogue are beyond
> this map. 01's assignment of standardized trust/naming conventions to this repository is
> untouched; T19 records the exploratory trust-profile convention as rejected evidence only.
> Returns only with a redrawn destination.

## Status

Closed **Out of scope** by T03 #4 decision 7 (Slice-first rule); no decision was taken on
this ticket's question. Document 01's assignment of trust/naming conventions to this
repository is untouched; the reusable-trust-profile convention remains rejected evidence
(T19 #14 decision 1). The question returns only with a redrawn destination, as a fresh
effort. This backfill record changes nothing.
