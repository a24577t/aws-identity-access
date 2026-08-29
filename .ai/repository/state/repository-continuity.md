# Repository Continuity Artifact

**Type:** transient continuity artifact (`.ai/repository/state/repository-continuity.md`);
subordinate to authoritative repository state and consumed by session bootstrap as
resumption intent only (MADR-0001 D3 — on any conflict the repository and tracker
prevail and the discrepancy is surfaced). Present only while the transition below is
in flight. It restates no accepted architecture.

## Transition in flight

S6 (`to-tickets`) publication: the execution-grouping amendment's eight grouped
tickets R1–R8 published to the issue tracker with the amendment §4 seven-edge native
dependency set, followed in the same authorized transaction by Status Artifact
reconciliation and removal of this artifact and the transport directory. The base of
the transition is the stable commit `64675b0d9d97cc566ce65b3741a0cd3faa3b452e`.
**STATUS remains byte-unchanged from that base — the last-stable-state S6 view —
until all eight issues and seven edges verify;** the in-flight position lives here.

## Committed transport (the recovery source)

The commit that added this artifact also committed byte-exact transport copies under
`.ai/repository/state/transition-payloads/s6-ticket-publication/`. Every hash is the
SHA-256 of the exact Git blob bytes (all files LF-only, so blob bytes equal authored
bytes):

| Committed path (under `transition-payloads/s6-ticket-publication/`) | SHA-256 |
|---|---|
| `MANIFEST.sha256` | the authorization-bound package manifest, byte-identical; verified against Eric's externally authorized manifest digest, never by its own lines |
| `publication-plan.md` | `e39b78fd4c66facfc9651fde9f1b9f235aec0a1d9b621f864f6a4772ac292d10` |
| `COMMIT-MESSAGE-STATUS.txt` | `1fde7fa9278b2826be745e829694d0954593e6fe7c10754ce00b23f089f84d37` |
| `status/STATUS.md` | `3e72171adeaa7b2522d2d3642b0735e559eb8ba644e756fe727d648d3520371b` |
| `tickets/r1.md` | `e9bd56a842a220656b547cc790fcc4f31ac7d80c6db4d5b363ff95378caca7d4` |
| `tickets/r2.md` | `af633019056c359a5675ff90c1e2a9d85f0b85f4db0bedc2277a7fd4092fa3f9` |
| `tickets/r3.md` | `ebf07bb80edeb2adf92dd17737bc93870fd53b69f65b91df56db9a01c3b3c816` |
| `tickets/r4.md` | `a0f7429f1fe05090039a455bf7f13414370b6ebbe6873ccdbf841f5f9de32a59` |
| `tickets/r5.md` | `26e13a9addb883cb18936effd717f3c9b5c3c5960e8b2c79039f6a73e19ca8d9` |
| `tickets/r6.md` | `e356f1ce40751d0cbea5489699cfcfce80a4345425ef9ea75aa1866bfda6bbca` |
| `tickets/r7.md` | `c9d2aeec9a2250d05e2c30a4b80cef81f3000d7c8608f2b81351148d46371c63` |
| `tickets/r8.md` | `287fe9a331e5abd7ed3faf4e3e4d3e57b8cad569e102f420a38fe69bc8ed076b` |

Verification: `sha256sum -c --ignore-missing MANIFEST.sha256` inside the committed
directory reports **exactly eleven checked entries** (the plan, the status commit
message, the STATUS successor, the eight ticket bodies), **11/11 OK, zero failed**;
the committed manifest blob is verified separately against the externally authorized
digest. **Recovery never depends on any untracked local directory** — the
pre-publication review staging (`.review-staging/`) may be absent; a fresh clone of
the commit carrying this artifact holds every byte needed. After this commit, every
issue body, the STATUS successor, and the status commit message are generated only
from these committed bytes.

## Deterministic creation order and titles

Strictly R1 → R8, one issue per committed body, with byte-exact titles as tabled in
the committed `publication-plan.md` §3 (`R1 — Foundation and contracts (slice A
rows 1, 2, 8)` … `R8 — Lab remediation Stages 0–6 (slice A row 15; each stage
separately authorized)`). Bodies are token-substituted per plan §4 (`{{R1}}…{{R8}}`,
the only placeholders; scratch copies only; no `{{` may remain). Native edges, added
after all eight verify, are exactly: R2←R1, R3←R2, R4←R3, R6←R4, R5←R1, R7←R5,
R8←R7 (GET-before-POST idempotent; per-edge round-trip verification). Initial
frontier: R1 only. No labels, milestones, projects, or assignees.

## Collision / adoption rules and issue-number reconstruction

For each k = 1…8: search issues of this repository (any state) whose title is
byte-exactly the plan §3 title for Rk.

- Zero matches → Rk is not yet created; the next remaining step is its creation.
- Exactly one match → verify its stored body equals the token-substituted committed
  `tickets/rk.md` bytes (tolerance: minus one final LF only), with substitutions
  taken from the numbers already reconstructed; on match, **adopt** its number into
  the map; on mismatch, stop and surface.
- More than one match → stop and surface.

The reconstructed map `{R1…R8} → issue numbers` is re-derived this way on every
resume; GitHub numbers are never assumed contiguous.

## Completed and remaining steps

Completed once this artifact is on `main`: stable base verified; transition-start
commit (this artifact + the transport above) created, verified, and pushed.

Remaining, in order (progress is reconstructed from the tracker via the rules above
— never from memory):

1. Create/adopt and round-trip verify R1…R8 sequentially from committed bytes.
2. Add/adopt and verify the seven native edges; verify totals (R1: 0 blockers;
   R2…R8: 1 each) and the frontier (R1 the only open issue with zero open blockers).
3. Final commit on `main`, atomically: derive STATUS from the committed tokenized
   successor using the verified number map; derive the commit message from the
   committed `COMMIT-MESSAGE-STATUS.txt` the same way; verify no token remains;
   place STATUS and verify its staged blob; delete this artifact and the complete
   `transition-payloads/s6-ticket-publication/` directory; commit and push exactly
   those changes.
4. Post-transaction verification: STATUS blob as derived; both transient paths
   absent; net repository diff vs the stable base is exactly the STATUS
   replacement; tracker holds eight issues and seven edges; frontier R1.

## Constraint

The whole transaction runs under one owner authorization already granted for it. No
S6 issue may be created outside that authorization; S7 does not start under it. No
label, milestone, project, assignee, or other tracker vocabulary; no GitHub
configuration; no AWS contact; no Terraform execution.

## Recovery and abort

If a session resumes while this artifact is present: verify the committed transport
per the rules above; reconstruct the issue-number map; continue at the first
unsatisfied remaining step. Completed tracker writes are never repeated, edited, or
automatically undone. On any hash, title, or state divergence: stop, surface the
discrepancy, and make no write without renewed owner authorization.

**Abort (owner-authorized only):** a new cleanup commit on `main` deleting this
artifact and the `transition-payloads/s6-ticket-publication/` directory. STATUS and
every accepted artifact remain unchanged; repository content returns to the
pre-transition stable state while HEAD advances; already-created issues remain and
are dispositioned only by explicit owner instruction. No history rewrite, no reset
of `main`, no force-push, no automatic revert — ever.

This artifact is removed only by the transaction's final STATUS-reconciliation
commit or by such an owner-authorized abort commit.
