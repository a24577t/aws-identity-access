---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 7
title: "T05 — Natural identifiers for workforce groups and permission sets"
url: https://github.com/a24577t/aws-identity-access/issues/7
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-27
sources:
  backfill: "T08 #13 decision 13 result-record backfill, reconstructed 2026-08-27 from the ticket's complete comment history; traceability, not authority"
  revalidation_comment: https://github.com/a24577t/aws-identity-access/issues/7#issuecomment-5382170133
  resolution_comment: https://github.com/a24577t/aws-identity-access/issues/7#issuecomment-5382918449
  close_comment: https://github.com/a24577t/aws-identity-access/issues/7#issuecomment-5382923014
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  resolved: 2026-08-22
---

# T05 — Natural identifiers for workforce groups and permission sets (slice A)

> **Backfilled discovery record** — produced 2026-08-27 under the separately authorized T08
> #13 decision-13 result-record backfill, reconstructing the complete durable result of
> T05 #7 from the ticket's comment history. Backfill preserves provenance and traceability
> only: it confers no new authority, changes no decision, and does not alter the approved S4
> Architecture Grill verdict. **Nothing here is accepted architecture: every decision is a
> proposal until ⟦G-Accept⟧.** GitHub issue #7 is the workflow/index surface and links to
> this record.

Grill completed with five HITL decisions approved by Eric as the human project owner and
decision authority; Claude executed the session in the repository-owner role under
`wayfinder-repo-owner` with `grill-with-docs`, 2026-08-22. Governing documents cited at the
aws_ami revision pinned by T01 (#2); the T18 inventory and the T04 prototype
(`prototype/t04-layout` @ `1d1c625`) were used as implementation evidence only.

**T03 revalidation (slice A), recorded on the ticket before resolution:** identifier classes
are workforce groups and permission sets only. Groups are references resolved in the identity
store (#4 decision 3): resolve the relation between the stable `key`, the identity-store
lookup name, and the external `source.group_name`, and the rename procedure when the lookup
name changes. Role, user, and fleet-role keys are beyond this map.

## Decisions (approved by Eric)

**1. Stable key grammar.** Workforce-group and permission-set keys match
`^[a-z][a-z0-9]*(-[a-z0-9]+)*$` (lowercase ASCII; starts with a letter; single hyphens
between segments; no leading, trailing, or consecutive hyphens). Permission-set keys are
2–24 characters; workforce-group keys are 2–64 characters (a repository contract, not a
claim about an AWS group-name limit). The filename stem must equal the key exactly (02
validation requirement 1), validator-enforced, with no other derivation from the path. `--`
is reserved for T10's assignment-filename separator; T10 still owns the final
assignment-filename rule. The permission-set deployment prefix budget is ≤8 characters
including its delimiter; T15/T16 must select and enforce a lab prefix within that budget,
and validation must also enforce that the composed deployed permission-set name is no more
than AWS's 32-character limit. Invalid keys or composed names are never silently lowercased,
normalized, truncated, abbreviated, or hashed — they are rejected with a clear validation
error. A future deployment needing a prefix longer than 8 characters returns to this
decision rather than weakening the key contract implicitly.

**2. Workforce-group identity.** `key` is the stable repository identity and equals the
filename stem exactly; assignments reference only `key`. `identity_store_name` is required
and records the externally managed group's exact Identity Store DisplayName. Resolution uses
AWS Identity Store `GetGroupId` with `displayName` as the UniqueAttribute — never the
deprecated `ListGroups` DisplayName filter. After resolution the returned group's
DisplayName must equal `identity_store_name` exactly, compared by Unicode code-point
sequence — a repository validation contract, not a claim about AWS lookup semantics. A
missing group, lookup failure, exact-name verification failure, or multiple-result condition
from any alternative implementation is a plan error; the group is never created and never
deferred. Optional `source: { provider, group_name }` is informational provenance only and
never drives lookup, authorization, reconciliation, or an IdP API call. The resolved GroupId
may exist only in the generated plan, Terraform state, or evidence and is never written
under `access/`. `key` is immutable during ordinary edits (rename procedure: decision 4).

**3. Permission-set identity.** `key` is the sole stable repository identity, equals the
filename stem exactly, follows decision 1, and is the only permission-set value assignments
reference. No `display_name` field is introduced (it would imply a separate portal label AWS
does not have). `description` is required human-readable explanatory metadata mapped
directly to the AWS permission-set Description: length 1–700, validated against the
documented AWS `PermissionSet.Description` character pattern (as published in the IAM
Identity Center / SSO Admin API reference; T15 reverifies the constraint against the
selected provider/API pin); T14 owns the stable validation code; description is metadata and
never identity. Generated views may show the key, description, and derived deployed name but
never manufacture a second identity or a requester-authored portal label. The deployed AWS
permission-set Name is exactly `<resource_name_prefix><key>`; the decision-1 prefix budget,
the composed 32-character maximum, AWS's Name pattern, and uniqueness within the Identity
Center instance are enforced. The AWS access portal displays the deployed Name; Description
is console metadata and does not replace it. Permission-set ARN, generated
`AWSReservedSSO_*` role name, role ARN, and unique suffix are outputs, never stored under
`access/`, and never treated as stable identity (deletion and recreation can change the
suffix). The brief's claim that `display_name` becomes the portal label is recorded as
conflicting with documented AWS behavior and resolved by this decision. Session duration,
relay state, and policy representation remain T21's.

**4. Rename semantics.**
- *Group lookup-name change:* change only `identity_store_name`; the repository key,
  filename, and assignment references are unchanged. Identity-platform and security review,
  enforced by T06. Resolve the new name and verify it returns the same GroupId already
  recorded in Terraform state/evidence; a different GroupId is principal replacement, not a
  rename — rejected unless a separately declared and approved principal-replacement workflow
  is being performed. GroupId is never stored under `access/`.
- *Workforce-group stable-key rename (exceptional):* one atomic PR that moves the group
  file, changes its `key`, and updates every assignment reference and filename. Aliases,
  redirects, derived keys, duplicate keys, and dangling references are rejected. The plan
  must show zero AWS mutations, verified by the plan gate — never assumed from
  repository-only semantics; if Terraform addressing would otherwise change, the
  implementation must preserve or explicitly migrate the resource address so no assignment
  is deleted or recreated. Strictest required owner set across every touched surface.
- *Permission-set stable-key rename:* an AWS replacement, because the derived deployed Name
  changes and `UpdatePermissionSet` does not support changing Name. Two-PR additive
  migration. **PR 1 — introduce and verify:** add the new permission-set key while retaining
  the old permission set; the new set's policies, session duration, relay state, and other
  effective behavior must be equivalent unless a separate behavior change is explicitly
  approved; add parallel assignment files targeting the new permission set; keep all old
  assignment files and the old permission set unchanged; the plan contains only creates — no
  deletes or replacements; apply and verify that the new permission set is provisioned and
  every intended new assignment succeeds; temporary duplicate portal roles are an
  acknowledged migration state. **PR 2 — retire:** only after PR 1 is applied and verified,
  remove the old assignments and then the old permission set, with explicit destroy
  acknowledgement and a plan limited to retiring the old resources; never combined with an
  ordinary grant PR or unrelated policy changes. PR 1 adds parallel assignments; it does not
  "re-target" them. Description-only changes are in-place updates. Generated ARNs and
  `AWSReservedSSO_*` identifiers remain outputs.

**5. Collision and normalization.** Keys and filename stems are lowercase ASCII by grammar;
uppercase or any other invalid character is rejected — never lowercased, case-folded,
trimmed, repaired, or normalized. `identity_store_name` is stored as the string produced by
YAML parsing and compared by exact Unicode code-point sequence (different YAML spellings
decoding to the same Unicode string are necessarily equivalent); no NFC/NFD/NFKC/NFKD, case
folding, whitespace normalization, or trimming; it must be non-empty with no leading or
trailing Unicode whitespace and no Unicode control characters, violations rejected.
Uniqueness domains: group keys within `groups/`; permission-set keys within
`permission-sets/`; exactly one group file per exact `identity_store_name` (aliases
prohibited); the derived deployed permission-set Name unique across desired configuration
**and** every pre-existing permission set in the selected Identity Center instance — a
collision with a pre-existing set is a protected-resource plan error, never silently
imported, adopted, renamed, suffixed, or overwritten. `--` is the only reserved key token in
slice A (T10 owns its final use; T06 may introduce separately governed runtime namespaces
later). Every validation failure has a stable code assigned by T14 and identifies the
offending field path; offending values are rendered escaped and unambiguous (never raw
control characters or log-injection content); diagnostics are deterministic, including their
ordering when several violations are reported.

## Claim-resolution record (grill-with-docs)

Per claim: governing document + identifier · claim · result · upstream amendment/refinement.

**1. `key` + `display_name`, with the key immutable and used in filenames/references.**
- Authority: I-1; `02-configuration-model.md` path rule and validation requirement 1; RD-06
  (names as immutable join keys — stated for accounts).
- Result: **compatible** for the immutable key used as filename and reference (decisions
  1–2); **absent** as an explicit rule for groups and permission sets (REVIEW Q3). The
  permission-set `display_name` half is **conflicting** with documented AWS behavior and
  superseded by decision 3 (no `display_name`; `description` maps to AWS Description and is
  never identity).
- Refinement: decisions 1–3. Upstream: none for this claim.

**2. `source.provider` / `group_name` as mutable metadata requiring identity-platform +
security review.**
- Authority: `01-repository-boundaries.md` (IdP integration metadata);
  `10-codeowners-model.md` (security co-approval on IdP configuration);
  `07-identity-center-platform.md`.
- Result: **compatible with refinement** — `identity_store_name`, not optional `source`
  metadata, is the authoritative lookup binding and receives the decision-4/T06 review.
  `source` is non-authoritative provenance and never participates in lookup, authorization,
  or reconciliation.
- Refinement: decision 2; decision 4 (lookup-name change guarded by GroupId continuity).

**3. Permission-set display names (end-user UX) vs the kebab-case path rule (REVIEW Q8).**
- Authority: `02-configuration-model.md` path rule; T04-d5 (deployed name = prefix + key).
- Result: kebab-case key/path rule — **compatible**, no carve-out; requester-authored
  `display_name` as the portal label — **conflicting** with AWS behavior and superseded by
  decision 3; AWS displays the derived deployed Name; Q8 is therefore resolved without
  `display_name`.
- Refinement: decision 3.

**4. Permission-set ARNs and Identity Center group IDs are generated identifiers, never keys
(REVIEW Q10).**
- Authority: `02-configuration-model.md` generated-identifier invariant; RD-06 (single
  binding lives with the entity's owner).
- Result: **compatible**; **absent** as an explicit application to identity objects.
- Refinement: decisions 2–3. **Proposed upstream document-02 clarification (one
  sentence):** generated IAM Identity Center GroupIds, permission-set ARNs, and provisioned
  `AWSReservedSSO_*` roles are outputs under the generated-identifier invariant, not
  requester-authored identifiers. Carried by Eric as decision authority; aws_ami not edited.

Evidence used (not authority): T18 X55/X60 single `name` = filename = deployed name
(partial); X37 `AWSReservedSSO_*` exclusions; X64 reference-by-file-existence only; REVIEW
Q3/Q8/Q10; T04 stubs assume key = filename (reusable).

## Downstream handoffs (as they occurred)

Handoff comments carrying each ticket's inherited T05 constraints were posted before #7
closed on T06 #8, T10 #15, T14 #19, T15 #10, T16 #11, T20 #22, T21 #20, and T22 #21; each
links back to #7.

## Glossary candidates (S5 `domain-modeling`)

**Stable key** — the immutable repository identity of a governed resource; equals the
filename stem; the only value other files reference. **Identity-store name** — the exact
DisplayName of an externally managed group in the connected identity store, used for
plan-time lookup. **Deployed name** — `<resource_name_prefix><key>`, the AWS permission-set
Name derived at plan time; never a requester-authored value.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub mutation. This backfill
record changes nothing decided by T05. (Note: the approved S4 verdict's condition C-A —
replacing the over-length illustrative `identity-inventory-reader` specimen key at S5 —
enforces this record's decision-1 bound; it does not change it.)
