# Slice-A execution-grouping amendment

Append-only amendment to the accepted
[slice-A engineering specification](slice-a-engineering-specification.md), produced as
a specification-planning correction. The specification file remains byte-unchanged
(SHA-256 `f23bcad4c81f97864a63040a582f85efef7837ae794b58f455509789579e8fc4`); this
record supersedes exactly one thing — the form in which `to-tickets` consumes the §10
work-item breakdown at S6. Sixteen independent ticket lifecycles impose excessive
bootstrap, review, publication, and closeout cost; S6 instead consumes the eight-row
grouping in §2 below 1:1 (one ticket per row of this amendment). Nothing else is
superseded: every §10 row, contract citation, dependency, sequencing rule,
authorization boundary, and empirical condition remains binding exactly as accepted.

This amendment carries no authority header: T23 #23 decision 4 scopes the
normative-header rule to `docs/architecture/` and `docs/guides/`, and no accepted rule
requires specification frontmatter — its authority derives from its approving
⟦G-Accept⟧ record and this repository placement. On any divergence between this
amendment and the accepted records it cites, the cited record prevails. No invariant,
contract, externally observable behavior, catalog selection, pin, authorization
boundary, or open architecture question is changed or resolved here.

## 1. What changes, and what does not

**Changes (execution planning only):**

- S6 publishes eight grouped tickets (R1–R8) instead of sixteen; the sixteen §10 rows
  become traced sub-items of the eight tickets per §2.
- Native tracker blocking edges are the seven-edge transitive reduction in §4; the
  nine §10-internal edges become mandatory ordered checkpoints inside their grouped
  tickets per §3.
- One closeout may cover all original rows within a grouped ticket **only when every
  contained row's acceptance criteria and required verification evidence pass**; any
  incomplete row keeps the whole grouped ticket open.

**Unchanged (binding by citation, never restated):**

- every §10 row's contract column and deciding records;
- the §10 sequencing rules (correction-4 reconciliation) in full, including: items
  14a, 14b, and 15 remain separately authorized beyond ticket creation; 14a and 14b
  are not one atomic dependency; **no Terraform apply may occur before the item-14a
  control set is active** (T15 d15's planning lifecycle); and the recorded T15 d15
  temporary procedural interval;
- the three open empirical conditions (specification §8.3) — open, unadvanced, and
  never claimed closed by any ticket;
- the decision-gated implementation lifecycle (S7–S11) with the Standards + Spec +
  Conformance review axes and the independent Quality Gate, applied to every grouped
  ticket;
- all accepted architecture, the §7 catalog scope and committed source bytes, the
  §8.1 toolchain and action pins, and every behavioral contract.

## 2. The eight-row breakdown (consumed 1:1 by `to-tickets` at S6)

| Row | Ticket | Original §10 rows | Blocked by (native) |
|---|---|---|---|
| R1 | Foundation and contracts | 1, 2, 8 | — |
| R2 | Validation and catalog system | 3, 4, 5, 6, 7 | R1 |
| R3 | Plan analysis and generated governance | 9, 10, 12 | R2 |
| R4 | CI workflows | 11 | R3 |
| R5 | Terraform roots and resource model | 13 | R1 |
| R6 | Repository-side control activation (separately authorized) | 14a | R4 |
| R7 | AWS-side OIDC/bootstrap (separately authorized) | 14b | R5 |
| R8 | Lab remediation Stages 0–6 (each stage separately authorized) | 15 | R7 |

Coverage: each of the sixteen §10 rows (1–13, 14a, 14b, 15) appears in exactly one
ticket; no row is added, split, or dropped.

## 3. Complete §10 edge traceability (all twenty edges)

**Internal edges (nine)** — mandatory ordered checkpoints inside their grouped ticket:
the blocked row's acceptance criteria may not be evaluated as passing before the
blocking row's acceptance criteria pass.

| # | §10 edge (blocked ← blocker) | Carried as |
|---|---|---|
| 1 | 2 ← 1 | R1 in-ticket checkpoint |
| 2 | 8 ← 2 | R1 in-ticket checkpoint |
| 3 | 4 ← 3 | R2 in-ticket checkpoint |
| 4 | 5 ← 3 | R2 in-ticket checkpoint |
| 5 | 6 ← 5 | R2 in-ticket checkpoint |
| 6 | 7 ← 4 | R2 in-ticket checkpoint |
| 7 | 7 ← 5 | R2 in-ticket checkpoint |
| 8 | 10 ← 9 | R3 in-ticket checkpoint |
| 9 | 12 ← 10 | R3 in-ticket checkpoint |

**Cross-group edges (eleven)** — mapped onto the eight-ticket graph:

| # | §10 edge (blocked ← blocker) | Group edge | Native representation |
|---|---|---|---|
| 10 | 3 ← 2 | R2 ← R1 | native edge |
| 11 | 9 ← 3 | R3 ← R2 | native edge |
| 12 | 12 ← 8 | R3 ← R1 | implied by native chain R3 ← R2 ← R1 |
| 13 | 11 ← 3 | R4 ← R2 | implied by native chain R4 ← R3 ← R2 |
| 14 | 11 ← 8 | R4 ← R1 | implied by native chain R4 ← R3 ← R2 ← R1 |
| 15 | 11 ← 9 | R4 ← R3 | native edge |
| 16 | 11 ← 10 | R4 ← R3 | native edge (same native edge as #15) |
| 17 | 13 ← 1 | R5 ← R1 | native edge |
| 18 | 14a ← 11 | R6 ← R4 | native edge |
| 19 | 14b ← 13 | R7 ← R5 | native edge |
| 20 | 15 ← 14b | R8 ← R7 | native edge |

The seven native edges of §4 are the transitive reduction of the derived group graph.
The three transitively redundant group edges (R3 ← R1, R4 ← R1, R4 ← R2) are **not**
published as native blockers; each is enforced by the published chain named in its
row. No scheduling constraint is lost: every §10 edge is a native group edge, is
implied by a chain of native group edges, or is an ordered in-ticket checkpoint.

## 4. Native dependency graph and initial frontier

Native blocked-by edges (seven, published as tracker dependencies):

- R2 blocked by R1
- R3 blocked by R2
- R4 blocked by R3
- R6 blocked by R4
- R5 blocked by R1
- R7 blocked by R5
- R8 blocked by R7

The graph is acyclic — two chains from R1: R1 → R2 → R3 → R4 → R6 and
R1 → R5 → R7 → R8. **Initial frontier: R1 only.**

## 5. Consumption rule

At S6, `to-tickets` consumes this amendment's §2 breakdown 1:1 — one published ticket
per row R1–R8, native edges exactly per §4, each ticket body carrying its original
§10 rows as traced sub-items with the §3 in-ticket checkpoints. The specification's
§10 sentence "consumed 1:1 by `to-tickets` at S6" is satisfied through this record:
1:1 at amendment-row → ticket level, and 1:1 at §10-row → traced-sub-item level. No
S6 ticket exists before this amendment is accepted at ⟦G-Accept⟧, and ticket
publication remains separately authorized after acceptance.
