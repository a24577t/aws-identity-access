# Publication plan — narrow ⟦G-Accept⟧: declaration-vocabulary amendment

Deterministic, fail-closed transaction in the established transition shape
(precedent: the S6 grouping-amendment acceptance, transition-start `b76818d` →
acceptance `7db3347` → merge `64675b0`). Executes only under Eric's hash-bound
narrow ⟦G-Accept⟧ authorization of the exact `MANIFEST.sha256` bytes. Gate
discipline: the executor prepares and verifies; **only Eric merges**.

Slug: `g-accept-declaration-vocabulary`. Stable base:
`0f03e3d274986041d41f60e712a0fb16a62ec7f2`. Acceptance branch:
`acceptance/declaration-vocabulary`.

## P0 — Preconditions (verify; any failure stops before any write)

1. `main == origin/main == 0f03e3d…`; working tree clean apart from
   `.review-staging/`; no unexpected local branches or stashes.
2. Every staged file's canonical bytes hash to its `MANIFEST.sha256` line (LF-pure;
   working bytes = blob bytes; verified with `git hash-object --path`).
3. The owner's authorization names this manifest digest; any byte difference
   requires re-authorization, never silent correction.
4. #26 remains open and assigned; `ticket/r1-foundation-and-contracts` remains at
   `b23d2b9…` (untouched by this transaction).

## P1 — Transition start (one commit on `main`, then push)

1. Copy `repository-continuity.md` → `.ai/repository/state/repository-continuity.md`.
2. Copy the staging directory's other files byte-exactly to
   `.ai/repository/state/transition-payloads/g-accept-declaration-vocabulary/`
   (paths preserved: `record/…`, `methodology/…`, `status/…`,
   `COMMIT-MESSAGE-*.txt`, `PR-TITLE.txt`, `PR-BODY.md`, `publication-plan.md`,
   `MANIFEST.sha256`).
3. Verify every staged blob OID (`git rev-parse :<path>`) equals the manifest.
4. Commit with the literal `COMMIT-MESSAGE-TRANSITION-START.txt`; push `main`;
   verify remote HEAD and round-trip blob OIDs.
   - Failure before push: nothing remote — fix or discard locally; no continuity
     obligations arise. Failure after push: the interval below governs.

**In-flight interval (P4 repository-only resumability):** from this push until
closeout, every step is recoverable from the repository alone — the continuity
artifact carries the resume rule and the payload carries the authoritative bytes.
Any session (fresh context) bootstraps, reads the continuity artifact, inspects
which step completed, and continues at the first incomplete step. No conversation
state is required or consulted.

## P2 — Acceptance branch

1. `git switch -c acceptance/declaration-vocabulary <transition-start-commit>`.
2. Move payload → destinations, byte-exact (expect R100 for the new record):
   - `…/record/slice-a-declaration-vocabulary-amendment.md` →
     `docs/specifications/slice-a-declaration-vocabulary-amendment.md`
   - `…/methodology/skill-execution-map.md` →
     `.ai/repository/methodology/skill-execution-map.md` (replacement)
   - `…/status/STATUS.md` → `.ai/repository/state/STATUS.md` (replacement)
3. Delete both transient paths: `.ai/repository/state/repository-continuity.md`
   and `.ai/repository/state/transition-payloads/g-accept-declaration-vocabulary/`.
4. Verify: destination blob OIDs equal the manifest; `git diff 0f03e3d…` names
   exactly the three destination paths; no other change of any kind.
5. Commit with the literal `COMMIT-MESSAGE-ACCEPTANCE.txt`; push; verify remote.

## P3 — Pull request (executor act, distinct from the owner gate)

1. `gh pr create` — base `main`, head `acceptance/declaration-vocabulary`, title
   from `PR-TITLE.txt`, body from `PR-BODY.md` (keyring auth; GITHUB_TOKEN/GH_TOKEN
   stripped, never inspected).
2. Round-trip verify: fetched PR title/body byte-equal to the literal files; base,
   head, and diff file list exactly as P2.4.

## P4 — STOP: owner gate

Merge is Eric's owner-only ⟦G-Accept⟧ act. The executor stops after P3
verification and reports. No auto-merge, no merge-queue, no executor merge under
any condition.

## P5 — Post-merge closeout (executor, after Eric's merge)

1. Fetch; verify `origin/main` merge contains the acceptance commit.
2. Verify the net diff `0f03e3d…` → merged `main` is exactly the three destination
   paths; destination blob OIDs equal the manifest; both transient paths absent.
3. Verify STATUS on `main` byte-equals the authorized successor; working tree
   clean; `ticket/r1-foundation-and-contracts` and #26 untouched.
4. Only after all of P5.1–P5.3 pass: delete local `.review-staging/` and the
   local acceptance branch; report closeout. (Staging is never deleted earlier.)
5. Resume route (separately assigned sessions): S7 D1–D3 correction pass → narrow
   S8 revalidation → S9 only after S8 passes.

## Failure, recovery, abort

- **Any P0–P2 verification failure:** stop at the failed step; surface the exact
  discrepancy; make no further writes. Recovery = re-verify from the repository and
  re-run the failed step, or abort (below). Never force-push; never rewrite
  pushed history; never "fix" bytes past the authorized hashes.
- **P3 failure (PR create/verify):** the branch remains; re-run P3 idempotently
  (one PR only — close a malformed PR before recreating).
- **Abort (owner-directed, before merge):** close any open PR unmerged; delete the
  acceptance branch; add one cleanup commit on `main` removing the continuity
  artifact and the transport payload (precedent: abort cleanup `a3a2825`); record
  the abort in the cleanup commit message. Aborting never reverts unrelated work.
- **Post-merge failure:** never revert the merge unilaterally; surface to Eric
  with the exact discrepancy and await disposition.
- **Session death at any point:** the P4 repository-only interval rule applies —
  the next session resumes from the continuity artifact and payload alone.
