---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 2
title: "T01 — Pin the governing aws_ami revision and record the brief's provenance"
url: https://github.com/a24577t/aws-identity-access/issues/2
type: research
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner (normal wayfinder route; no governing-document claim)"
recorded: 2026-08-27
sources:
  backfill: "T08 #13 decision 13 result-record backfill, reconstructed 2026-08-27 from the ticket's complete comment history; traceability, not authority"
  findings_comment: https://github.com/a24577t/aws-identity-access/issues/2#issuecomment-5381522324
  resolution_comment: https://github.com/a24577t/aws-identity-access/issues/2#issuecomment-5381627134
  research_evidence: https://github.com/a24577t/aws-identity-access/blob/55a650f4cd5112b1412e71adbbc2dffd6e69a303/docs/research/aws-ami-provenance.md
  resolved: 2026-08-22
---

# T01 — Pin the governing aws_ami revision and record the brief's provenance

> **Backfilled discovery record** — produced 2026-08-27 under the separately authorized T08
> #13 decision-13 result-record backfill, reconstructing the complete durable result of
> T01 #2 from the ticket's comment history and the committed research evidence. Backfill
> preserves provenance and traceability only: it confers no new authority, changes no
> decision, and does not alter the approved S4 Architecture Grill verdict. **Nothing here is
> accepted architecture: every decision is a proposal until ⟦G-Accept⟧** (the S4 verdict was
> approved at ⟦G-Verdict⟧ on 2026-08-26 with conditions C-A/C-B/C-C). GitHub issue #2 is the
> workflow/index surface and links to this record.

T01 was a `research` (AFK) ticket on the normal wayfinder route — provenance research with
no governing-document claim, so `grill-with-docs` was not invoked. The research ran 2026-08-22
against the local `aws_ami` clone (read-only) cross-checked with the GitHub API; the two
owner decisions it surfaced were resolved by Eric the same day.

## Question (from the ticket)

Which aws_ami revision governs this POC, and how is it recorded? Inputs: aws_ami `main` @
`5f3cb7163f468730fd2ceb5d565c90b0bfda6099` (2026-08-22, untagged); the intake brief existed
in aws_ami only as an untracked file `docs/bootstrap/aws-identity-access-poc-prompt.md`
(byte-identical to this repository's copy) with no immutable URL. To resolve: (1) commit pin
vs owner-created tag; (2) where the brief's governed copy lives; (3) the provenance record
format; (4) the current text at that revision of every identifier the map cites (OD-05,
OD-08, OD-10, OD-11, OD-21, RD-03…RD-09, I-1…I-8, CV-07), including RD-09's exact scope
wording for T08.

## Findings (research, 2026-08-22 — recorded verbatim from the findings comment)

1. **Governing revision:** aws_ami `main` @ `5f3cb7163f468730fd2ceb5d565c90b0bfda6099`
   (2026-08-22T11:49:46Z, "aws-identity-access / Inline trust policies in identity access
   roles"). Local HEAD == local `origin/main` == GitHub `main`. Confirmed.
2. **Tags:** none — `git tag` empty locally; the GitHub tags endpoint returns `[]`.
3. **Local aws_ami state:** clean except one untracked entry, `?? docs/bootstrap/`.
4. **Intake brief in aws_ami:** `docs/bootstrap/aws-identity-access-poc-prompt.md` is **not
   tracked** at `5f3cb716…`; **no immutable aws_ami URL exists for it.**
5. **Brief digest:** sha256
   `f87fa000a2a39897b5be20a650ce400584c339fdd99606dee928a4e266ad4068` (16,204 bytes);
   **byte-identical** to this repository's `aws-identity-access-poc-prompt.md`.
6. **Brief in this repository:** tracked since local commit `7a7d3ed` ("governance"), at the
   time not yet pushed — no immutable URL existed anywhere; pushing `main` would create one.
7. **Cited documents:** all 13 `docs/architecture/*.md` + README carry `decided: 2026-08-17`;
   statuses `normative` (00–10, README), `register` (11), `checklist` (12); destinations
   recorded per document; `CONTEXT.md` has no frontmatter. Immutable URL form:
   `https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/<path>`.
8. **Identifiers:** all 21 cited IDs (I-1…I-8, RD-03…RD-09, OD-05/08/10/11/21, CV-07)
   **exist** at the pin; verbatim text with file/heading/line captured in the research
   evidence (§5).
9. **Discrepancy — RD-09 wording:** the map's phrase "parallel ADR files are never
   maintained" is verbatim from `docs/architecture/README.md` (lines 44–45), not from the
   RD-09 entry, which says "Parallel ADR files are **not created** … If repository creation
   later warrants ADR-shaped files, they are migrated or generated from this register, never
   maintained alongside it." Same substance; cite README for that phrase or quote the entry.
10. **RD-09 scope (for T08):** the entry contains no sentence naming domain repositories or
    limiting itself to aws_ami. It is qualified as *architecture*-decision authority; the
    register is `destination: all`; sentence 4 contemplates platform repositories holding
    ADR-shaped files *derived from* the register. Whether a domain repository's
    non-architecture decisions fall under it is **not stated** at this revision — left to
    T08 (resolved there as decisions 1/3/14 with the RD-09 clarification proposal).
11. **OD-21:** the map's paraphrase ("tracking vs pinned unspecified") is faithful.
12. **Minor:** the posted map body did not then contain the identifier strings RD-09 / OD-21
    / CV-07 / most I-n; they lived in the proposed-map file and in this ticket's body.
13. A machine-checkable provenance record (`docs/governance/aws-ami-provenance.yml`: commit,
    URL form, per-document status/destination/decided, brief sha256 + bytes, aws_ami status
    at intake, recorded date/ticket) was drafted in the research evidence §4 as a proposal;
    no such file is committed by T01.

## Decisions (repository-owner resolution, 2026-08-22)

- **Governing aws_ami revision (pin):** `5f3cb7163f468730fd2ceb5d565c90b0bfda6099` — the
  full SHA is authoritative. **No tag adopted**; no aws_ami tag will be created. (Research
  option A; a tag remains available to the aws_ami owner only as a supplement recording tag
  *and* SHA, never the tag alone.)
- **Governed intake copy of record:** the tracked `aws-identity-access-poc-prompt.md` in
  this repository.
  - Intake digest (sha256):
    `f87fa000a2a39897b5be20a650ce400584c339fdd99606dee928a4e266ad4068`
  - Immutable link:
    https://github.com/a24577t/aws-identity-access/blob/7a7d3edec2ba57f2e5ab1a81c9f3ab861c27f7da/aws-identity-access-poc-prompt.md
- **Research evidence (non-authoritative):**
  [`docs/research/aws-ami-provenance.md`](../../research/aws-ami-provenance.md), first
  committed on the research branch at `55a650f4cd5112b1412e71adbbc2dffd6e69a303` and later
  carried onto `main`; it holds the verbatim identifier texts at the pin and the full
  source-command list.
- The RD-09 citation correction (finding 9) was applied to T08 #13; RD-09's scope over
  domain repositories remained unresolved there until T08 resolved it.

**Backfill corroboration (2026-08-27):** the committed brief's digest recomputes to exactly
`f87fa000a2a39897b5be20a650ce400584c339fdd99606dee928a4e266ad4068` (16,204 bytes) — the
intake of record is unchanged since T01.

## Downstream effects (as they occurred)

- Every later ticket cites governing documents at the T01 pin using the immutable URL form
  (finding 7); the map's Authority note fixes citation by ID at the pin.
- Finding 10 became T08's claim 1 input; the RD-09 clarification proposal is carried by Eric
  (T08 decision 14).
- The brief's provenance rule (digest-verified intake of record) is restated in the map's
  Decisions-so-far T01 line and consumed by T06's routing of the brief under the strictest
  set.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub mutation. This backfill
record changes nothing decided by T01.
