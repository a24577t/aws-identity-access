# Slice-A root-control-path classification amendment

Narrow, append-only amendment to the accepted T20 #22 decision-2 changed-path
classification, ratified through the Pre-Baseline E1 route. It carries no
authority header (T23 #23 decision 4 scopes the normative-header rule to
`docs/architecture/` and `docs/guides/`); its authority derives from its
approving ⟦G-Accept⟧ record and this repository placement. On any divergence
between this amendment and the accepted records it cites, the cited record
prevails — except for the single omission this amendment closes.

## 1. The observed conflict

T06 #8 decision 3 inventories the root-level control files and routes them
through review (`.gitignore`, `LICENSE`, `aws-identity-access-poc-prompt.md`
→ the strictest review set), and the accepted
[repository byte-identity amendment](repository-byte-identity-amendment.md)
governs the root `.gitattributes` — so all four are governed repository
control surfaces. T20 #22 decision 2, however, enumerates the changed-path
classification table without any row matching them, and fixes the rule that
a file matching no row is a fail-closed classification error
(`CLS-UNCOVERED-PATH`). Under the two accepted records as written, a pull
request touching any of these governed files can never pass the
`plan-preview` check: a legitimate governed change fails permanently.

## 2. The ratified classification

The following **exact root-control paths** classify as **`platform-change`**:

| Exact path | Class |
|---|---|
| `.gitignore` | platform-change |
| `.gitattributes` | platform-change |
| `LICENSE` | platform-change |
| `aws-identity-access-poc-prompt.md` | platform-change |

- Matching is **exact-path**, never a root wildcard: no other root file, and
  no new root file, gains a classification from this amendment.
- Every other T20 #22 decision-2 row, the composition rule, the permitted
  plan-effect matrix, and the fail-closed uncovered-path behavior remain
  unchanged: any file matching no row — including any future root file —
  still fails closed as `CLS-UNCOVERED-PATH`.
- The basis mirrors decision 2's own recorded reasoning for `docs/adr/**`
  ("joins the strictest set by the same reasoning T06 applied"): these are
  repository authority/control surfaces already under the strictest review
  routing, and `platform-change` is decision 2's class for exactly that kind
  of surface (its plan-effect bound — a platform-only change plans empty —
  applies to them unchanged).

## 3. Provenance

The omission was demonstrated empirically by the first live `plan-preview`
run over a pull request whose changed set includes `.gitignore` — R5 #30's
PR #40, run
<https://github.com/a24577t/aws-identity-access/actions/runs/33682333199/job/100421587650>
(`CLS-UNCOVERED-PATH` on `.gitignore`, fail closed as the accepted records
require). The classifier implementation was verified faithful to the
accepted decision-2 table; the gap is in the accepted enumeration, not the
implementation. T06 #8, T20 #22, and the engineering specification remain
byte-unchanged; this amendment is the only new authority.

## 4. Resume route for R5 #30

1. Merge this amendment at its narrow ⟦G-Accept⟧ (owner-only).
2. Merge `main` into `ticket/r5-terraform-roots-and-resource-model` (no
   rebase; PR #40 stays open).
3. Apply the smallest classifier/test correction implementing §2 (exact
   paths only, red-first).
4. Delta revalidation of the affected surfaces and the S8–S11 addenda on
   the new head; then ⟦G-Merge⟧ for PR #40 under its own authorization.
