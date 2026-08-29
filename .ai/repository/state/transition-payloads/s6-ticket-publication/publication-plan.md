# Publication plan — S6 eight-ticket publication (one fail-closed transaction)

Executed only under Eric's hash-bound publication authorization (this package's
`MANIFEST.sha256`). One authorization covers the whole transaction below — the
transition-start commit, the eight issue creations, the seven native edges, and the
final STATUS-reconciliation commit that deletes the transients. **No label,
milestone, project, assignee, ruleset, environment, or other GitHub configuration;
no AWS contact; no Terraform execution; no tag or release; no implementation claim.**
`gh` uses keyring auth (account `a24577t`; `GITHUB_TOKEN`/`GH_TOKEN` stripped).
Completed tracker writes are never repeated, edited, or automatically undone.

**Byte identity:** all verification binds Git-blob bytes per the repository
byte-identity amendment. After the transition-start commit, every issue body, the
STATUS successor, and the status commit message are generated **only from committed
transport bytes** (`git show <transition-start-sha>:<path>`, hash-verified before
use); `.review-staging/` is never a source after transition start and may disappear.

## 1. Transaction preconditions

- `main == origin/main == 64675b0d9d97cc566ce65b3741a0cd3faa3b452e`; working tree
  clean except `.review-staging/`; no tags; no open PRs;
  `.ai/repository/state/repository-continuity.md` and
  `.ai/repository/state/transition-payloads/` absent.
- Tracker: no issue (any state) whose title starts `R1 — ` … `R8 — ` per the §3
  titles (collision scan; adoption rules in §7 apply on resume only).
- Package `MANIFEST.sha256` verified byte-for-byte against Eric's externally
  authorized digest; all entries verify (`sha256sum -c --strict`).

## 2. Transition-start commit on `main` (step 2 of the transaction)

Adds exactly these thirteen paths, byte-exact from this package (hashes per
`MANIFEST.sha256`); each placed path's **staged blob** is verified before commit:

| Repository path | Staged source |
|---|---|
| `.ai/repository/state/repository-continuity.md` | `continuity/repository-continuity.md` |
| `.ai/repository/state/transition-payloads/s6-ticket-publication/MANIFEST.sha256` | `MANIFEST.sha256` |
| `…/s6-ticket-publication/publication-plan.md` | `publication-plan.md` |
| `…/s6-ticket-publication/COMMIT-MESSAGE-STATUS.txt` | `COMMIT-MESSAGE-STATUS.txt` |
| `…/s6-ticket-publication/status/STATUS.md` | `status/STATUS.md` |
| `…/s6-ticket-publication/tickets/r1.md` … `tickets/r8.md` (eight files) | `tickets/r1.md` … `tickets/r8.md` |

In-directory check: `sha256sum -c --ignore-missing MANIFEST.sha256` inside the
committed transport directory must report **exactly eleven checked entries**
(`publication-plan.md`, `COMMIT-MESSAGE-STATUS.txt`, `status/STATUS.md`, the eight
`tickets/r*.md`), **11/11 OK, zero failed**; the transported `MANIFEST.sha256` is the
twelfth transported file but self-excluded, verified separately against the
authorized digest (pre-commit from the package file; post-push from the Git blob).
Commit with `git commit -F .review-staging/s6-ticket-publication/COMMIT-MESSAGE-CONTINUITY.txt`
(review-staged only — it messages this commit itself); push `main`.

## 3. Exact titles and creation order (step 3)

Created strictly in this order; issue bodies extracted from the committed transport
(`git show`, hash-verified), tokens substituted per §4 on a scratch copy:

| Order | Committed body | Exact title |
|---|---|---|
| 1 | `tickets/r1.md` | `R1 — Foundation and contracts (slice A rows 1, 2, 8)` |
| 2 | `tickets/r2.md` | `R2 — Validation and catalog system (slice A rows 3–7)` |
| 3 | `tickets/r3.md` | `R3 — Plan analysis and generated governance (slice A rows 9, 10, 12)` |
| 4 | `tickets/r4.md` | `R4 — CI workflows (slice A row 11)` |
| 5 | `tickets/r5.md` | `R5 — Terraform roots and resource model (slice A row 13)` |
| 6 | `tickets/r6.md` | `R6 — Repository-side control activation (slice A row 14a; separately authorized)` |
| 7 | `tickets/r7.md` | `R7 — AWS-side OIDC/bootstrap (slice A row 14b; separately authorized)` |
| 8 | `tickets/r8.md` | `R8 — Lab remediation Stages 0–6 (slice A row 15; each stage separately authorized)` |

Per create: collision scan first (§7); `gh issue create --title "<exact>"
--body-file <scratch>`; capture the number from the returned URL; **round-trip
verify immediately** (`gh issue view <n> --json title,body`): title byte-exact; body
byte-exact to the substituted scratch copy or minus one final LF only. Any other
difference stops the transaction (§7). GitHub numbers are adopted as returned —
never assumed contiguous (unrelated external issues may interleave).

## 4. Issue-number substitution (the only permitted placeholders)

Tokens `{{R1}} … {{R8}}` denote the eight issue numbers as created/adopted. Bodies
use one token each in `## Blocked by` (r2:`{{R1}}`, r3:`{{R2}}`, r4:`{{R3}}`,
r5:`{{R1}}`, r6:`{{R4}}`, r7:`{{R5}}`, r8:`{{R7}}`; r1 none); `status/STATUS.md` and
`COMMIT-MESSAGE-STATUS.txt` use all eight explicitly (R1 #{{R1}} … R8 #{{R8}} — no
numeric ranges). Substitution happens on scratch copies only; committed transport
stays tokenized; after substitution no `{{` may remain in the copy (checked every
time). Creation order guarantees every referenced number exists before use.

## 5. Native dependency edges (step 4) and frontier (step 5)

After all eight verify, add exactly seven edges in this order (child ← blocker):
R2←R1, R3←R2, R4←R3, R6←R4, R5←R1, R7←R5, R8←R7. Per edge: GET the child's
`dependencies/blocked_by` first (idempotence — an existing correct edge is verified,
not re-added); otherwise resolve the blocker's database id
(`gh api repos/:owner/:repo/issues/<blocker#> --jq .id`) and POST
`repos/:owner/:repo/issues/<child#>/dependencies/blocked_by -F issue_id=<id>`;
**round-trip verify** the edge by GET. Then verify totals: exactly seven edges;
per-child blocked_by counts R2…R8 = 1 each, R1 = 0. **Frontier check:** R1 is the
only open issue with zero open blockers.

## 6. STATUS reconciliation and transient deletion (steps 6–8; same authorization)

Only after 8/8 issues and 7/7 edges verify, one final commit on `main`, atomically:

1. Extract committed `status/STATUS.md` and `COMMIT-MESSAGE-STATUS.txt` from the
   transition-start commit (`git show`, hash-verified against the manifest).
2. Substitute all eight tokens with the verified issue-number map; verify no `{{`
   remains in either derivation.
3. Place STATUS at `.ai/repository/state/STATUS.md`; `git rm` the Repository
   Continuity Artifact and `git rm -r` the complete
   `transition-payloads/s6-ticket-publication/` directory; stage exactly those
   paths; verify the staged STATUS blob equals the substituted bytes (record its
   SHA-256 in the log).
4. `git commit -F` the substituted message; push `main`.
5. **Post-transaction verification:** `origin/main` advanced; STATUS blob equals the
   recorded substituted hash; both transient paths absent; net repository diff vs
   the stable base `64675b0…` is exactly one change (STATUS replaced); tracker holds
   the eight issues and seven edges; frontier R1. STATUS now records S6 complete and
   the S7/R1 objective with all eight exact issue numbers.

STATUS remains byte-unchanged from the stable base until this step — during the
whole transition it stays the last-stable-state view (S6 objective), and the
in-flight position lives in the committed continuity artifact.

## 7. Recovery, resume, and abort (repository + tracker only)

- **Resume source:** the committed transition-start transport plus live tracker
  state — never chat, never `.review-staging/`. A fresh clone suffices.
- **Issue-number reconstruction:** for each k, search issues (any state) whose title
  is byte-exactly the §3 title; adopt its number after verifying its body equals the
  substituted committed bytes (tolerance: minus one final LF). Zero matches → not
  yet created (continue at that create). One match with body mismatch, or more than
  one match → **stop and surface**; never edit or close without renewed
  authorization.
- **Edges:** GET-before-POST makes every edge step idempotent.
- **Completed tracker writes are never repeated, edited, or automatically undone.**
- **Abort (owner-authorized only):** a new cleanup commit on `main` deleting the
  continuity artifact and the transport directory; STATUS and all accepted artifacts
  unchanged; already-created issues remain and are dispositioned only by explicit
  owner instruction; no reset, force-push, history rewrite, or automatic revert.
- Interruption at any point leaves `main` in one of two shapes — stable base
  (nothing pushed) or continuity-bridged (transition-start pushed) — both fully
  resumable from the repository and tracker alone.

## 8. Completion

Report the eight issue numbers, edge verifications, frontier, STATUS commit SHA, and
final state; **claim nothing** — S7 does not start under this authorization. The
review-staging package is deletable under separate confirmation afterward; the
session closes clean (S10) with S7 (frontier R1) as the standing objective.
