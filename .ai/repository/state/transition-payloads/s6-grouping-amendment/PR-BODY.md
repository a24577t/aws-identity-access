## What this PR does

Adds the append-only slice-A execution-grouping amendment, reconciles STATUS in the
same gate merge, and removes the transient Repository Continuity Artifact and
transition-payload directory that bridged the open-PR interval. The accepted
engineering specification remains byte-unchanged (SHA-256
f23bcad4c81f97864a63040a582f85efef7837ae794b58f455509789579e8fc4). The amendment
supersedes exactly one thing: the form in which S6 `to-tickets` consumes the §10
work-item breakdown — eight grouped tickets (R1–R8) instead of sixteen, with all
sixteen §10 rows as traced sub-items and all twenty §10 dependency edges carried
(seven native tracker edges = the transitive reduction; nine in-ticket ordered
checkpoints; three transitively implied group edges documented row-by-row).

## Why

Specification-planning correction: sixteen independent ticket lifecycles impose
excessive bootstrap, review, publication, and closeout cost. No invariant, contract,
externally observable behavior, catalog selection, pin, authorization boundary, or
open architecture question changes — so no S4 / Architecture Grill re-run applies.

## Contents

- docs/specifications/slice-a-execution-grouping-amendment.md — new; 6,644 bytes;
  SHA-256 1c602e325a75545b55b01873f0ee524974e96de8e58f8bf2805e9c3f2eb0408e
- .ai/repository/state/STATUS.md — replaced; SHA-256
  8b661f7ad308d8fb3ee277797a6ca69083ec67b9c5ea0b7d2803a7f80d973d53 →
  4a05813aed4ab2508f056737c9e45ea7d8ddbd00720ff5ee6c7471a68d434c13
- .ai/repository/state/repository-continuity.md — deleted (transient
  transition-start artifact; the transition completes in this merge)
- .ai/repository/state/transition-payloads/s6-grouping-amendment/ — deleted
  (transient byte-exact transport copies committed at transition start so a fresh
  clone can complete or resume the transition; net authoritative effect of the
  whole transition is exactly the two changes above)

## Invariants preserved

- 14a (R6), 14b (R7), and 15 (R8) remain separate tickets, separately authorized
  beyond ticket creation; 14a and 14b are not one atomic dependency.
- No Terraform apply before the item-14a control set is active (T15 d15).
- The three empirical conditions (provider execution; `forget` representation; import
  redaction) remain open and unadvanced.
- All accepted architecture, §7 catalog scope and source bytes, §8.1 pins and action
  SHAs, and behavioral contracts are unchanged.
- No S6 ticket exists yet; publication of the eight tickets remains separately
  authorized after this merge.
