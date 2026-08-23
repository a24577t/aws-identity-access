---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 15
title: "T10 — GROUP and USER assignment identity and filename rules"
url: https://github.com/a24577t/aws-identity-access/issues/15
type: prototype
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-23
sources:
  decision_batch: "consolidated 7-question HITL batch (2026-08-23); Eric selected 1A–7A with one integrated collaborator account-identity correction, applied throughout"
  inherited_inputs:
    - https://github.com/a24577t/aws-identity-access/issues/15 (four comments: T03 revalidation, T05 key grammar, T06 review routing, T19 adopted-assignment handoff)
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  prototype: throwaway T04 stub tree, branch prototype/t04-layout @ 1d1c625 (superseded by the specimens below)
---

# T10 — GROUP and USER assignment identity and filename rules

> Proposed discovery record — the complete durable result of T10 #15. Decisions approved by Eric
> as the human project owner and decision authority after collaborator review; executed by Claude
> in the repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`, using the
> batch-question directive (operating-guide governing invariant 3). **Nothing here is accepted
> architecture: every decision is a proposal until ⟦G-Verdict⟧ and ⟦G-Accept⟧.** GitHub issue
> #15 is the workflow/index surface and links to this record.

## Authorization scope of this record

Approving publication of this T10 result records the **proposed assignment identity and
filename rules only**. It does **not** authorize any AWS call or mutation, GitHub
configuration, Terraform operation, implementation, or backfill. Everything remains proposed
pending ⟦G-Verdict⟧ and ⟦G-Accept⟧.

## Governing documents and evidence

Cited at the `aws_ami` revision pinned by T01 (#2): `02-configuration-model.md` (path rule;
validation rule 1 — path↔configuration agreement), `07-identity-center-platform.md` (directory
shape; "assignments are structured per-OU/per-account so CODEOWNERS path rules can express
delegated authority"), `10-codeowners-model.md`, I-1, RD-04, RD-05, RD-06, RD-08. Inherited map
decisions: T03 #4 (d5 targeting; revalidation narrowing on this ticket — no USER example, no
`exceptions/` question in this map; OU never enters key or path), T04 #6 (d4 layout), T05 #7
(key grammar; `--` reserved for T10; reference-by-key only; atomic rename), T06 #8 (per-account
review routing from inventory delegation data), T09 #12 (pinned inventory; `INV-*` classes),
T15 #10 (d1/d5 aliases; alias grammar), T16 #11 (fixture aliases), T19 #14 (adopted
assignments keep tuple identity, represented identically). Evidence (never authority): T18
inventory rows X30–X36, S18, S21, X53, X71 and §2.5; the T04 prototype stubs.

## Settled inputs (fixed by prior decisions; recorded, not re-decided)

Natural key = `account + principal + permission set` (brief proposal adopted by T03 d5). One
grant per file, no aggregation (T03 d5; T06). OU never enters the key or directory path; OU is
planning input expanding to an explicit account list (T03 revalidation; T02 claim 4). No USER
example and no `exceptions/` isolation question in this map; RD-05's governed USER class stays
defined in the domain architecture and is rejected by the selected-slice validation profile.
Adopted assignments are represented identically (T19). `--` cannot occur inside a T05 key, so
it is unambiguous as a separator.

## Claim-resolution record (grill-with-docs)

Per claim: governing document + identifier · claim · result · upstream amendment/refinement.

| # | Claim | Authority | Result | Upstream amendment / refinement |
|---|---|---|---|---|
| 1 | Natural key = `account + principal + permission set` | brief §Natural identifiers (proposal); T03 d5; RD-05; RD-06 | **inherited** — adopted by the map; fixed here as decision 1 with the integrated account-alias identity rules | none |
| 2 | One assignment per file `account-assignments/<account>/<group-key>--<permission-set-key>.yml`, no aggregation | 02 path rule; RD-04; T04 d4; T05 (`--` reservation) | **compatible** — absent upstream as a rule; consistent with 02 and 07's per-account option; aggregated shapes (X30/X32/X33–X36/S18/S21/X53) replaced per T19 d1 | none |
| 3 | OU membership is not part of the key; OU selection is planning input expanding to an explicit, reviewable account list | 07 §Directory shape ("per-OU/per-account"); REVIEW Q2 (X30 auto-expansion hazard); T02 claim 4 | **absent** upstream as a prohibition — adopted domain-side; 07 is **compatible** (this repository selects the per-account arm) | decision 7 extends the carried document-07 proposal with the per-account-identity clarification |
| 4 | Per-OU CODEOWNERS delegation remains expressible under the chosen layout | 07; `10-codeowners-model.md`; T06 | **compatible** — per-account path rules with reviewer classes resolved from inventory delegation data; OU informs reviewer selection, never identity or path | none |

## Decisions

Eric selected 1A–7A from the consolidated batch; the collaborator's integrated account-identity
correction is applied throughout (decisions 1, 3, 4 and the T14 handoff).

### Decision 1 — Final filename rule, separator, and account-alias identity

`access/identity-center/account-assignments/<account-name>/<group-key>--<permission-set-key>.yml`
— filename = exactly two T05-valid keys joined by the reserved `--`; extension `.yml` (RD-04);
reject, never normalize (T05).

**Account-alias identity (integrated correction):** the `<account-name>` directory and the
in-file `account` value are both the **exact same stable inventory alias**. The alias is
**exactly one path segment** and satisfies the established T15/T05 lowercase alias grammar
(`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`); separators, traversal sequences, uppercase, normalization,
and unrecognized directory forms are rejected. The alias must occur exactly once as an entry
in the consumed, pinned organization inventory:

- an absent alias fails under the applicable T09 rule;
- an active entry must resolve to exactly one unique live binding;
- a `status: requested` entry must remain unbound, must carry no live fields, validates as
  deployment-deferred, and is omitted from the executable plan (RD-08);
- duplicate alias, live-name, or live-ID bindings fail closed under T09 `INV-DUP`.

Alternatives not taken: nested `<account>/<group>/<ps>.yml` directories (deeper tree, renames
touch directories, no benefit at slice scale); any other separator (abandons T05's deliberate
reservation). Classification: **compatible** (absent upstream as a rule; consistent with 02,
07 per-account, RD-06, T15 d5).

### Decision 2 — Strict two-segment GROUP-only rule; nothing reserved for USER

The currently defined domain assignment representation recognizes exactly the two-segment
GROUP form `<group-key>--<permission-set-key>.yml` with `principal.type: GROUP`; any other
filename or body shape is an unrecognized domain-shape error (wrong segment count, invalid key
grammar, uppercase, other separators, `_`-prefixed scope files, unrecognized body fields). No
USER filename, marker, directory, or body representation is defined or reserved by T10. This is
not a permanent domain prohibition on USER assignments: RD-05's exceptional USER class remains
part of the architecture, and a future governed decision that admits USER assignments must
define its representation and update the domain shape. Independently, the selected-slice
validation profile rejects `principal.type: USER` because USER assignments are outside slice A.
The T05 grammar guarantees that whatever representation such a future decision defines is
structurally distinguishable. Classification: **compatible**. Alternative not taken:
pre-reserving a concrete USER form (decides part of a question the T03 revalidation removed
from this map).

### Decision 3 — In-file field set and three-way path/content agreement

Exact field set, no additional properties:

```yaml
account: <account-name>
principal:
  type: GROUP
  group: <group-key>
permission_set: <permission-set-key>
```

The validator enforces **three-way agreement**: directory ↔ `account` (the same stable
inventory alias per decision 1), filename segment 1 ↔ `principal.group`, filename segment 2 ↔
`permission_set` (02 validation rule 1; the exploratory `E-NAME` check generalized). Automation
consumes only the in-file keys and never derives identity from the path (I-1). No `status`,
OU, ID, ARN, or deployment field appears in the file — deferral is purely an inventory
property (RD-08). Alternatives not taken: filename-only identity (violates I-1 and 02);
convenience fields (drift surface against `groups/` and `permission-sets/`). Classification:
**inherited** (I-1; 02) with the exact field set **compatible** (brief proposal adopted).

### Decision 4 — Duplicate prevention by construction (corrected proof)

Duplicate-prevention is recorded as **by construction**. The proof depends on the complete set
of construction-preserving checks:

1. one filesystem path per account/group/permission-set key tuple;
2. exact path/content agreement (decision 3);
3. the lowercase key grammar (T05 — no case variants);
4. unique group registry bindings (T05 — one file per identity-store name);
5. unique permission-set keys (T05 — per-directory uniqueness);
6. T09's unique account-alias/live-binding validation (decision 1 — `INV-DUP` fail-closed).

A separate cross-file tuple-uniqueness scan is **retired** because this complete check set
proves the invariant; **T09's inventory duplicate-binding checks are not retired** and remain
in force. The exploratory within-file `E-DUP` (X64) stands only as evidence of the replaced
aggregated shape. Classification: **compatible**. Dependency effect: the T14 handoff replaces
the former "cross-file duplicate code" item with the construction-preserving checks above.

### Decision 5 — Per-account review routing (claim 4)

Review authority is expressed as per-account path rules —
`access/identity-center/account-assignments/<account-name>/**` — with the account→reviewer
mapping resolved from the organization inventory's delegation data through T06's registry; OU
influences reviewer selection through the inventory but never identity or path. A per-OU
delegation is realized by enumerating its accounts into per-account rules (generation and
maintenance mechanics belong to T06's registry and S6 implementation, refreshed on
inventory-pin bumps per T09). Slice A resolves every assignment path to identity-platform.
Classification: **compatible** (07's stated purpose satisfied via the per-account arm;
document 10; T06). Alternative not taken: OU directories (conflicts with the fixed
OU-exclusion; REVIEW Q2 hazard).

### Decision 6 — The three example files (record specimens)

Approved exactly as shown. Placeholder keys are explicitly illustrative — the real group key
arrives with T16 Stage 5.2 / T22 evidence; permission-set keys with T21's verified forms.
Aliases are the T16 fixture aliases; the deferred file is byte-identical in shape to the active
ones — deferral lives only in the inventory (`lab-requested` is `status: requested`, never
created).

`access/identity-center/account-assignments/lab-workload-a/lab-readers--read-only.yml`

```yaml
account: lab-workload-a
principal:
  type: GROUP
  group: lab-readers
permission_set: read-only
```

`access/identity-center/account-assignments/lab-workload-b/lab-readers--read-only.yml`

```yaml
account: lab-workload-b
principal:
  type: GROUP
  group: lab-readers
permission_set: read-only
```

`access/identity-center/account-assignments/lab-requested/lab-readers--read-only.yml`

```yaml
account: lab-requested
principal:
  type: GROUP
  group: lab-readers
permission_set: read-only
```

These instantiate T03 d5 (the same grant to two active accounts as two distinct files; one
deferred reference omitted from the executable plan), supersede the T04 prototype stubs, and
become T14 valid-specimen inputs and the T20 plan-summary example. Specimen assertions carry
the decision-1 alias rules: each `account` value equals its directory segment, is one path
segment in the alias grammar, and occurs exactly once as an inventory entry. `lab-workload-a`
and `lab-workload-b` each require exactly one unique active live binding; `lab-requested` must
have no live binding or live fields and validates as deployment-deferred. Classification:
**inherited** (T03 d5 instantiated; T15 d5 aliases; RD-08).

### Decision 7 — Extended document-07 carried proposal

Eric's carried document-07 refinement (from T04) is extended with one sentence; the full
carried proposal now reads:

> **Document 07 refinement (one proposal, extended by T10):** add `groups/` to the Identity
> Center directory shape; rename `assignments/` → `account-assignments/`; and clarify:
> "Assignment identity is per-account (`account + principal + permission set`, one grant per
> file); OU structure is planning input that expands to explicit accounts, never part of
> assignment identity."

aws_ami is not edited by this repository; the local decisions stand regardless of when or
whether the proposal lands. Classification: 07 **compatible** either way; the clarification
addresses the REVIEW Q2 hazard at its source. Alternative not taken: no upstream text (leaves
both arms upstream).

## Dependency effects and frontier

#15 has native edges blocked-by 0, **blocking 2** (#22, #19). Closing #15 reduces T20 #22 to
**two** open blockers (#20, #21) and T14 #19 to **three** (#20, #21, #22); neither becomes
unblocked. Live frontier after closure, in map order: **T21 #20 (next claimable)** · T22 #21 ·
T23 #23. One HITL ticket per session — nothing is claimed at publication.

## Publication sequence (fail-closed; record before close)

Executed only under Eric's consolidated publication approval. A failure at any step through 8
leaves #15 open, with all later normal publication steps unperformed; completed remote writes
are not automatically undone. The exact partial state is preserved through a Repository
Continuity Artifact where necessary and reported.

1. Create this record at
   `docs/wayfinding/map-1/15-group-and-user-assignment-identity-and-filename-rules.md` and the
   `docs/wayfinding/README.md` index line in the working tree.
2. Validate them: frontmatter parses, internal links resolve, and the mechanical checks —
   including the account-alias/path/content/inventory-uniqueness checks — pass on the final
   bytes; no live identifier, no acceptance claim.
3. Commit both on `main`; push (authorized as part of the consolidated approval).
4. Verify the immutable record URL at the pushed commit resolves and is byte-equivalent to the
   local file.
5. Post the exact #15 resolution comment, with the record commit SHA filled in.
6. Post the exact informational handoff comments to T14 #19, T20 #22, and T22 #21; no
   dependency edges.
7. Update map #1: append exactly one T10 Decisions-so-far line. No fog edit and no map-order
   change (T10 graduates nothing and creates no ticket).
8. Round-trip verify: the #15 resolution comment, all three handoff comments, and the complete
   map #1 diff (exactly the one addition).
9. If any step through 8 fails: leave #15 open, perform no later normal publication step,
   preserve the exact partial state through continuity if necessary, and report it.
10. Close #15 as completed, retaining assignee `a24577t`, with the close comment.
11. Round-trip verify the close; verify T20 #22 now shows two open blockers and T14 #19 three.
12. Recompute all dependency effects and the live frontier (expected state above) without
    claiming anything.
13. Replace the Repository Continuity Artifact (position after T10; frontier at T21 #20);
    commit and push.
14. Verify `HEAD == origin/main`, a clean working tree, and the final tracker invariants
    (#15 closed with assignee retained; map body as verified; no other issue state changed).

Post-close failure rule: if a failure occurs after step 10, do not reopen #15 and do not
duplicate earlier writes; record the precise partial state in continuity where possible, report
it, and stop.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Verdict⟧ and ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub mutation
or any implementation.
