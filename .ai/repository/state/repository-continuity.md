# Repository Continuity Artifact

**Type:** transient continuity artifact (`.ai/repository/state/repository-continuity.md`);
subordinate to authoritative repository state and consumed by session bootstrap as
resumption intent only (MADR-0001 D3 — on any conflict the repository prevails and the
discrepancy is surfaced). Present only while the transition below is in flight. It
restates no accepted architecture.

## Transition in flight

Narrow ⟦G-Accept⟧: acceptance of the append-only slice-A execution-grouping amendment
(supersedes only the engineering specification §10 ticket-consumption mapping — eight
grouped tickets R1–R8) together with Status Artifact reconciliation. The base of the
transition is the stable commit `b4a62035afc476c55061506ee3d29a542363f0f3`.

## Committed transport (the recovery source)

The commit that added this artifact also committed byte-exact transport copies of the
owner-authorized payloads under
`.ai/repository/state/transition-payloads/s6-grouping-amendment/`:

| Committed path (under `transition-payloads/s6-grouping-amendment/`) | SHA-256 |
|---|---|
| `MANIFEST.sha256` | the authorization-bound review-package manifest, byte-identical; verified against Eric's externally authorized manifest digest, never by its own lines |
| `COMMIT-MESSAGE.txt` | `5251ace26b920c4e514a0e50d6723543820602123c7bf2f9bae57d43b7b1fffe` |
| `PR-BODY.md` | `78745d29ce9d126999f39d5895ce9a9c88832628eced12765136d4a9e1e1fd8c` |
| `amendment/slice-a-execution-grouping-amendment.md` | `1c602e325a75545b55b01873f0ee524974e96de8e58f8bf2805e9c3f2eb0408e` (6,644 bytes) |
| `status/STATUS.md` | `4a05813aed4ab2508f056737c9e45ea7d8ddbd00720ff5ee6c7471a68d434c13` (2,811 bytes), replacing STATUS at SHA-256 `8b661f7ad308d8fb3ee277797a6ca69083ec67b9c5ea0b7d2803a7f80d973d53` |

Verification of the committed copies: `sha256sum -c --ignore-missing MANIFEST.sha256`
run inside the committed directory must report **exactly four checked entries** — the
four payload files above — **all four OK, zero checked entries failed**; the
committed `MANIFEST.sha256` is the fifth transported file but self-excluded, so it is
verified separately, byte-for-byte, against Eric's externally authorized manifest
digest. **Recovery never
depends on any untracked local directory**: the pre-publication review staging
(`.review-staging/`) may be absent; a fresh clone of the commit carrying this artifact
holds every byte needed to complete the transition.

## Intended branch and pull request

One acceptance branch `acceptance/s6-grouping-amendment`, created from the `main`
commit that carries this artifact; one pull request to `main` titled
`G-Accept (narrow): slice-A execution-grouping amendment — §10 consumed as eight grouped tickets`,
body = the committed `PR-BODY.md` bytes; merged only by Eric.

## Steps

Completed once this artifact is on `main`: stable base verified; this
transition-start commit (this artifact + the transport directory above) created and
pushed.

Remaining, in order:

1. Create the acceptance branch from the transition-start commit.
2. Copy the amendment and the STATUS successor **from the committed transport paths**
   onto `docs/specifications/slice-a-execution-grouping-amendment.md` and
   `.ai/repository/state/STATUS.md`; verify both against the hashes above.
3. On the acceptance branch, delete **both** this artifact and the whole
   `transition-payloads/s6-grouping-amendment/` directory.
4. Commit using the exact committed `COMMIT-MESSAGE.txt` bytes (extract from the
   transition-start commit via `git show`; hash-verify before use); push the branch.
5. Open the pull request using the exact committed `PR-BODY.md` bytes (same
   extraction and hash verification); byte-verify the stored PR body.
6. Stop for Eric's merge; then post-merge verification.

## Intended authoritative changes (exactly two)

1. Add `docs/specifications/slice-a-execution-grouping-amendment.md` (bytes as bound
   above).
2. Replace `.ai/repository/state/STATUS.md` (bytes as bound above).

The accepted engineering specification remains byte-unchanged
(SHA-256 `f23bcad4c81f97864a63040a582f85efef7837ae794b58f455509789579e8fc4`). The
deletions of this artifact and the transport directory in the completing merge are
transition bookkeeping, not authoritative changes: the merge's net effect against the
stable base is exactly the two changes above.

## Constraint

No S6 ticket may be created before the acceptance pull request merges.

## Recovery

If a session resumes while this artifact is present: verify the four payload hashes
above directly, and verify the committed `MANIFEST.sha256` blob against the
externally authorized manifest digest; if the acceptance branch or pull request
exists, verify its placed files against the bound hashes and continue at the first
unsatisfied remaining step; if neither exists, recreate the branch from the commit
carrying this artifact and continue from step 1. A fresh clone suffices; no local
staging is required. On any hash or state divergence: stop, surface the discrepancy,
and make no write without renewed owner authorization.

**Abort (owner-authorized only):** abort is a new cleanup commit on `main` deleting
this artifact and the `transition-payloads/s6-grouping-amendment/` directory. STATUS
and every accepted artifact remain unchanged; repository content returns to the
pre-transition stable state while HEAD advances. No history rewrite, no force-push,
no automatic revert — ever.

This artifact is removed only by the acceptance pull request's merge or by such an
owner-authorized abort commit.
