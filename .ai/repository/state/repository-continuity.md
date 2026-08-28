# Repository Continuity Artifact

**Type:** transient continuity artifact (`.ai/repository/state/repository-continuity.md`);
subordinate to authoritative repository state and consumed by session bootstrap as
resumption intent only (MADR-0001 D3 — on any conflict the repository prevails and the
discrepancy is surfaced). Present only while the transition below is in flight. It
restates no accepted architecture.

## Transition in flight

Narrow ⟦G-Accept⟧: acceptance of two append-only records — the slice-A
execution-grouping amendment (supersedes only the engineering specification §10
ticket-consumption mapping — eight grouped tickets R1–R8) and the repository
byte-identity amendment with its root `.gitattributes` — together with Status
Artifact reconciliation. The base of the transition is the stable commit
`a3a2825e1e0eb3a92a8ca6fefa7764e6ec39ea5f`, whose tree is
`26632224a80190e0e7d9c9fb756d3139e8c131b6` (equal to the tree of the earlier stable
base `b4a62035afc476c55061506ee3d29a542363f0f3`, as historical corroboration).

## Committed transport (the recovery source)

The commit that added this artifact also committed byte-exact transport copies of the
owner-authorized payloads under
`.ai/repository/state/transition-payloads/s6-grouping-amendment/`. Per the
byte-identity policy being accepted, every hash below is the SHA-256 of the exact Git
blob bytes (all payloads are LF-only, so blob bytes equal the authored bytes):

| Committed path (under `transition-payloads/s6-grouping-amendment/`) | SHA-256 |
|---|---|
| `MANIFEST.sha256` | the authorization-bound review-package manifest, byte-identical; verified against Eric's externally authorized manifest digest, never by its own lines |
| `COMMIT-MESSAGE.txt` | `2c87859d9bede37dbd120b752c0ef49a694134445551e86ea507fb591be082ab` |
| `PR-BODY.md` | `76a14f709b4d2423860e469e7b03152a5f9769c3425868cd44269b125fa0e4e3` |
| `amendment/slice-a-execution-grouping-amendment.md` | `a04edc33f3bcd5e5ea23812d22966fc83a3ddbc823b7b5f5e7defd98eabcecd8` (6,875 bytes) |
| `amendment/repository-byte-identity-amendment.md` | `3d17114e9f97138f4f30fab68b75400833d003cc32d6069bd361298d42758671` (4,199 bytes) |
| `gitattributes` | `66d63f7b48418c1aa0c3f46aee04688cad52a0ef2715ade00000aa38095771bb` (32 bytes; destination `/.gitattributes`) |
| `status/STATUS.md` | `b5c0662ae017fb602b46c7d4db55e670d2fb01355b8fecc3ed24c942605491cd` (3,071 bytes), replacing the Status Artifact at canonical blob `d7a57c9064fa45ddefa8509e8aaad080f44d8dd0` (2,304 bytes, SHA-256 `8db3a4c62e5f43b35a2c9a3c35e55d3b5e2ddf376787e6153643dee92c3e8104`) |

Verification of the committed copies: `sha256sum -c --ignore-missing MANIFEST.sha256`
run inside the committed directory must report **exactly six checked entries** — the
six payload files above — **all six OK, zero checked entries failed**; the committed
`MANIFEST.sha256` is the seventh transported file but self-excluded, so it is
verified separately, byte-for-byte, against Eric's externally authorized manifest
digest. **Recovery never depends on any untracked local directory**: the
pre-publication review staging (`.review-staging/`) may be absent; a fresh clone of
the commit carrying this artifact holds every byte needed to complete the transition.

## Intended branch and pull request

One acceptance branch `acceptance/s6-grouping-amendment`, created from the `main`
commit that carries this artifact; one pull request to `main` titled
`G-Accept (narrow): execution-grouping and repository byte-identity amendments`,
body = the committed `PR-BODY.md` bytes; merged only by Eric.

## Steps

Completed once this artifact is on `main`: stable base verified; this
transition-start commit (this artifact + the transport directory above) created and
pushed.

Remaining, in order:

1. Create the acceptance branch from the transition-start commit.
2. Copy the four payloads **from the committed transport paths** onto their
   destinations — `docs/specifications/slice-a-execution-grouping-amendment.md`,
   `docs/specifications/repository-byte-identity-amendment.md`, `/.gitattributes`
   (from `gitattributes`), `.ai/repository/state/STATUS.md` — and verify each
   destination's **staged Git blob** against the hashes above.
3. On the acceptance branch, delete **both** this artifact and the whole
   `transition-payloads/s6-grouping-amendment/` directory.
4. Commit using the exact committed `COMMIT-MESSAGE.txt` bytes (extract from the
   transition-start commit via `git show`; hash-verify before use); push; reverify
   the four destination blobs at the acceptance commit.
5. Open the pull request using the exact committed `PR-BODY.md` bytes (same
   extraction and hash verification); byte-verify the stored PR body.
6. Stop for Eric's merge; then post-merge verification.

## Intended authoritative changes (exactly four)

1. Add `docs/specifications/slice-a-execution-grouping-amendment.md`.
2. Add `docs/specifications/repository-byte-identity-amendment.md`.
3. Add root `.gitattributes` (exact bytes as bound above; no renormalization of any
   existing blob — the pre-adoption survey found every indexed blob already LF).
4. Replace `.ai/repository/state/STATUS.md` (bytes as bound above).

The accepted engineering specification remains byte-unchanged: canonical Git blob
`97faf7cb658e1238c695dcfe6ab00e2b749a10a0`, 17,938 bytes, SHA-256
`5679d79656052410e118b18a224b590e303315906c132fc8bdc92f72297557ad`. The deletions of
this artifact and the transport directory in the completing merge are transition
bookkeeping, not authoritative changes: the merge's net effect against the stable
base tree is exactly the four changes above.

## Constraint

No S6 ticket may be created before the acceptance pull request merges.

## Recovery

If a session resumes while this artifact is present: verify the six payload hashes
above directly from the committed blobs, and verify the committed `MANIFEST.sha256`
blob against the externally authorized manifest digest; if the acceptance branch or
pull request exists, verify its placed destination blobs against the bound hashes and
continue at the first unsatisfied remaining step; if neither exists, recreate the
branch from the commit carrying this artifact and continue from step 1. A fresh clone
suffices; no local staging is required. On any hash or state divergence: stop,
surface the discrepancy, and make no write without renewed owner authorization.

**Abort (owner-authorized only):** abort is a new cleanup commit on `main` deleting
this artifact and the `transition-payloads/s6-grouping-amendment/` directory. STATUS
and every accepted artifact remain unchanged; repository content returns to the
pre-transition stable state while HEAD advances. No history rewrite, no reset of
`main`, no force-push, no automatic revert — ever.

This artifact is removed only by the acceptance pull request's merge or by such an
owner-authorized abort commit.
