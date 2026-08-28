## What this PR does

Adds two append-only records — the slice-A execution-grouping amendment and the
repository byte-identity amendment — together with the root `.gitattributes` the
latter governs, reconciles STATUS in the same gate merge, and removes the transient
Repository Continuity Artifact and transition-payload directory that bridged the
open-PR interval. The accepted engineering specification remains byte-unchanged:
canonical Git blob `97faf7cb658e1238c695dcfe6ab00e2b749a10a0`, 17,938 bytes, SHA-256
`5679d79656052410e118b18a224b590e303315906c132fc8bdc92f72297557ad`.

The execution-grouping amendment supersedes exactly one thing: the form in which S6
`to-tickets` consumes the §10 work-item breakdown — eight grouped tickets (R1–R8)
instead of sixteen, with all sixteen §10 rows as traced sub-items and all twenty §10
dependency edges carried (seven native tracker edges = the transitive reduction;
nine in-ticket ordered checkpoints; three transitively implied group edges
documented row-by-row). The byte-identity amendment fixes hash authority on
canonical committed Git-blob bytes (working-tree renderings are diagnostics only),
declares LF as canonical text, and keeps JSON exact-byte (`*.json -text`).

## Why

Specification-planning correction: sixteen independent ticket lifecycles impose
excessive bootstrap, review, publication, and closeout cost. Byte-identity
correction: the previous, aborted acceptance attempt bound platform-specific CRLF
working-tree hashes where canonical Git-blob hashes were required. No invariant,
contract, externally observable behavior, catalog selection, pin, authorization
boundary, or open architecture question changes — so no S4 / Architecture Grill
re-run applies.

## Contents

- docs/specifications/slice-a-execution-grouping-amendment.md — new
- docs/specifications/repository-byte-identity-amendment.md — new
- .gitattributes — new (`* text=auto eol=lf`; `*.json -text`; no renormalization of
  existing blobs — the pre-adoption survey found every indexed blob already LF)
- .ai/repository/state/STATUS.md — replaced (canonical pre-state blob
  `d7a57c9064fa45ddefa8509e8aaad080f44d8dd0`, 2,304 bytes, SHA-256
  `8db3a4c62e5f43b35a2c9a3c35e55d3b5e2ddf376787e6153643dee92c3e8104`)
- .ai/repository/state/repository-continuity.md — deleted (transient
  transition-start artifact; the transition completes in this merge)
- .ai/repository/state/transition-payloads/s6-grouping-amendment/ — deleted
  (transient byte-exact transport copies committed at transition start so a fresh
  clone can complete or resume the transition; net authoritative effect of the whole
  transition is exactly the four changes above)

All added or replaced files are verified from their staged and committed Git blobs
against the authorization manifest; per-file blob hashes are bound by the
owner-authorized MANIFEST.sha256 committed in the transport directory.

## Invariants preserved

- 14a (R6), 14b (R7), and 15 (R8) remain separate tickets, separately authorized
  beyond ticket creation; 14a and 14b are not one atomic dependency.
- No Terraform apply before the item-14a control set is active (T15 d15).
- The three empirical conditions (provider execution; `forget` representation; import
  redaction) remain open and unadvanced.
- All accepted architecture, §7 catalog scope and source bytes, §8.1 pins and action
  SHAs, and behavioral contracts are unchanged; no existing blob is renormalized.
- No S6 ticket exists yet; publication of the eight tickets remains separately
  authorized after this merge.
