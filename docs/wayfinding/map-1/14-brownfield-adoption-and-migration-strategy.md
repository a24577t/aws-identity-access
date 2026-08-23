---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 14
title: "T19 — Brownfield adoption and migration strategy"
url: https://github.com/a24577t/aws-identity-access/issues/14
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-23
sources:
  decision_batch: "consolidated 22-question HITL batch (2026-08-23); Eric selected all 22 recommendations with seven integrated collaborator corrections, applied throughout"
  inherited_inputs:
    - https://github.com/a24577t/aws-identity-access/issues/14 (five inherited comments: T03 revalidation, T06 adoption guard, T15 S5 wording, T16 lifecycle, T09 transport)
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  evidence: docs/research/brownfield-inventory.md (T18 #5; 104 components S01–S29, X01–X75)
---

# T19 — Brownfield adoption and migration strategy

> Proposed discovery record — the complete durable result of T19 #14. Decisions approved by Eric
> as the human project owner and decision authority after collaborator review; executed by Claude
> in the repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`, using the
> batch-question directive (operating-guide governing invariant 3). **Nothing here is accepted
> architecture: every decision is a proposal until ⟦G-Verdict⟧ and ⟦G-Accept⟧.** GitHub issue
> #14 is the workflow/index surface and links to this record.

## Authorization scope of this record

Approving publication of this T19 result records the **proposed adoption and migration
architecture only**. It does **not**
authorize any AWS call or mutation, GitHub configuration, Terraform plan or apply, import,
state operation, seed creation, drift probe, cleanup, backfill, or implementation. The lab
import rehearsal occurs only after POC acceptance and separate Eric authorization; within it,
**every live-mutation group is separately authorized** (decision 16). Slice A remains
greenfield-only with pre-existing resources protected (T03 d6, T15 d7).

## Governing documents and evidence

Cited at the `aws_ami` revision pinned by T01 (#2): `09-tier0-execution.md` (§Brownfield
adoption — deliberate import/reconciliation phase, destroy-class operations blocked throughout,
apply from reviewed artifact), `01-repository-boundaries.md`, `02-configuration-model.md`
(RD-04), `05-runtime-mutation-contracts.md` (drift policy; I-6), `07-identity-center-platform.md`,
I-4, RD-05, RD-06, RD-08; OD-09 and OD-12 (open). Inherited map decisions: T02 #3 (staged lab
apply; one reconciliation owner; zero incremental spend), T03 #4 (slice A; d6 greenfield-only),
T04 #6 (d5 target prefix assigned to T19), T05 #7 (rename semantics), T06 #8 (target adoption
guard), T07 #9, T15 #10 (d6–d16; d14 fixed S5 wording), T16 #11 (standalone-lab discovery;
staged remediation), T09 #12 (pinned transport; retention), T08 #13 (register form). Evidence
(never authority): the T18 inventory at the pin; `mcp_gateway01` lab facts recorded by T02/T15.

## Claim-resolution record (grill-with-docs)

Per claim: governing document + identifier · claim · result · upstream amendment/refinement.

| # | Claim | Authority | Result | Upstream amendment / refinement |
|---|---|---|---|---|
| 1 | Each retained or adapted component embodies an inherited or compatible convention | per-row citations in the decision 1 table (T03 d2–d6, T04 d4, T05, RD-03, RD-05, RD-08, I-1) | **compatible** — every retain/adapt row carries its cited basis | none |
| 2 | Each replaced or retired component embodies a rejected or absent convention, basis cited | per-row citations (REVIEW Conflicts 1–2, Q2/Q4/Q6/Q7; brief rejected-conventions list; T02 claim 4; T03 d5; T06; T07 d1) | **compatible** — every replace/retire row cites its rejection or absence | none |
| 3 | Migration increments and coexistence respect 09's import-phase and reviewed-artifact model | `09` §Brownfield adoption + Execution rules | **inherited** — the three-state model (d7), configuration-driven import blocks in reviewed code (d8), plan-classification gates with no destroy exception inside the import phase (d10, d14), and per-increment saved plans implement 09 directly | none |
| 4 | Configuration and data transition preserves names-not-IDs (I-4 / RD-06) and deferred references (RD-08) | I-4; RD-06; RD-08 | **inherited**, strengthened: no live identifier is ever committed (d8 — import ids derived at plan time from encrypted non-public inputs); deferred targets are never imported or provisioned (d11) | none |

**Upstream proposals:** none new from T19. The carried set (documents 09, 05, 02, 07, 01/11,
OD-21, RD-09 clarification) is unchanged; OD-09 and OD-12 stay open platform-wide (decision 20).

## Decisions

Each decision was selected by Eric from the recommended option of the consolidated batch; the
seven integrated collaborator corrections (discovery semantics; permission-set adoption bundle;
bounded ownership proof; import-block data handling; exact rollback with no destroy exception;
tag and seeded-rehearsal behavior; authority boundaries and the T21 handoff) are applied
throughout.

### Decision 1 — Disposition table over the T18 inventory

Vocabulary: **retain** (as-is) / **adapt** (reuse shape, change per cited decisions) /
**replace** (new artifact; old is evidence) / **retire** (rejected; preserved only as
evidence/specimen) / **deferred** (beyond slice A — basis recorded, not decided).

| T18 rows | Disposition | Basis |
|---|---|---|
| X24, S17 read-only set; X60 schema forms 1–2 | **adapt** | inherited form 1 (T03 d4); relocate per T04 d4, key per T05; profile-reject customer-managed/boundary fields (T21/T14). Adoption treats a permission set as a **bundle** (decision 4): core resource + its AWS-managed attachment or embedded inline-policy resource |
| X18–X23 group references; X55 schema | **adapt** | inherited reference model (T03 d3, RD-05, I-1); T05 key/lookup-name split + GroupId continuity; `sync` values verified against the lab store (T22) |
| X31 deferred assignment; X12 fixture deferral path; X64 `W-INV-DEFERRED`; X65 test | **adapt** | RD-08 inherited end-to-end (T18 §4.1); the admin grant content **retired** per T07 d1; the fixture itself **replaced** by the T16 alias fixture + T09 snapshot (T15 d5 — no live IDs, no `consumption: tracking`) |
| X14/S14 `instance.yml`; X59 schema | **adapt** | declaration/verification data (T03 d2); field set → T22 |
| X16/S16/X63 verification record; S04/X17 procedures pattern | **adapt** | endorsed pattern; freshness gate absent (T18 §2.2) → T22/T14 |
| X64/X66 validator + codes; X67–X75 specimens | **adapt** | 16 codes + "deferred, never invalid" reusable; add profile / protected-path / freshness / cross-file-duplicate / plan-classification codes (T14); executed under the pinned environment (T18 §5.1) |
| X53/S21 assignment schemas; X33–X36/S18 aggregated files | **replace** | aggregated arrays, `scope: ou/accounts`, OU-in-path rejected for the slice (T03 d5, T04 d4, T02 claim 4; brief); one grant per file + `--` key → T10 |
| X30 `_ou-wide` | **retire** | auto-expansion rejected (T02 claim 4, T03 d5; REVIEW Q2); negative-specimen input (T14) |
| X32 `_finance-reporting` | **retire** | aggregated multi-account file out of slice; explicit-list idea recorded as future authoring evidence |
| S05/X37 defaults layer; S22/X54 schemas | **retire** | unauthorized layer (REVIEW Q7); security-sensitive defaults rejected (brief); T04 layout has no defaults root; effective values reported per T20 |
| `pa-*`/`PA-*` namespace; X70 specimen | **retire** | ownership-from-name rejected (brief; REVIEW Q4; T06 — no `pa-*` namespace) |
| S07–S10, S26–S27 trust profiles; S12/S13/S28 bidirectional membership; S24 cross-directory inline; S06 narrow deny | **retire** | rejected conventions (REVIEW Conflicts 1–2, Q6; I-c/I-d/I-e); preserved in the migration note (→ T23) |
| X27 admin set; X36 admin/USER grants; X19 admin-group use | **retire** (in-slice surface) | T07 d1; negative specimens only under the T14 fixture path |
| X09/S02 CODEOWNERS; X10 CI; S03 stub | **replace** | T06 registry + review classes supersede alias vocabulary (REVIEW Q13); unpinned `pip` vs pinned environment (brief; T14); workflow shape per T15 d15/T20 |
| X01–X08 docs set | **adapt** | rewritten under the T23 documentation set; X07 counterexamples endorsed; X08 scenario 1 in-slice; migration-note content from this table |
| X13/S19 runtime-mutation contract; boundaries X38–X40; accounts X41–X51; IAM schemas X56/X57/X61/X62; identity-source X15/X58; S15; StackSets/fleet | **deferred** | beyond slice A (T03 d1, T04 d6, Out-of-scope closures #16/#17/#18); rejected-convention evidence preserved; the `reconciliation:` field feeds the T02 claim-3 domain decision |

### Decision 2 — The exact greenfield/adoption boundary

Mechanism-defined: slice A contains **no `import` block, no CLI `terraform import`, no
`moved`/`removed` state surgery of any kind**; its plan gate rejects any operation outside the
derived POC-managed (`ialab-`) set (T15 d7). Adoption exists only inside a distinct
**import-rehearsal phase** — entered only after POC acceptance and separate Eric authorization —
with its own root, plan classes, and rules (decisions 3–16). Any adoption-shaped change outside
that phase is a validation/plan error (T14 code). Classification: inherited (T03 d6; 09).
Rejected: a resource-list-only boundary with import tooling allowed in-slice.

### Decision 3 — Rehearsal discovery and inventory prerequisites (corrected semantics)

Before any import increment: (1) a fresh read-only **full-enumeration discovery snapshot**,
recorded as tier-2 non-public evidence with digest, alias-mapped, distinguishing four separate
result sets — **permission-set definitions and policy content**; **the accounts to which each
permission set is currently provisioned** (established by `ListPermissionSetsProvisionedToAccount`
per account, cross-checked per set); **current account assignments**; and **paginated
asynchronous provisioning/assignment operation records where relevant**. Provisioning-status
APIs describe **asynchronous operation requests, not a durable current-status field** on the
permission set — no persistent health is inferred from an old `SUCCEEDED` operation; any
relevant `IN_PROGRESS` operation **blocks the increment**; a relevant `FAILED` operation
**requires disposition before proceeding**. **Every list operation paginates to a null
continuation token.** (2) The T16 Stage-6 verifications still green. (3) The T09 binding
snapshot live-verified. (4) Discovery re-verified at plan **and** apply of every increment; a
stale or divergent snapshot stops the increment. These API limitations are recorded as
implementation-plan input (decision 21). Classification: inherited (09; T16 d11 Stage 6; T09
live re-verification; T15 d12). Rejected: a one-time snapshot at rehearsal start.

### Decision 4 — Adoption eligibility, the permission-set bundle, and exclusions

The T19-eligible resource classes are **permission-set adoption bundles and their GROUP
account assignments**. In the lab rehearsal, assignments may target **lab-workload accounts
only** — the class the apply role can manage (T15 d6/d7). In target waves, assignments may
target **only accounts explicitly admitted by the separately approved wave manifest**.
Management-account targets and all deferred/excluded classes remain prohibited.
The importable **bundle** consists of: the `aws_ssoadmin_permission_set` core resource; **plus**
its supported AWS-managed policy attachment resource, when present; **or** its embedded
inline-policy resource, when present. **The permission-set core alone is not sufficient to
claim zero-diff adoption of its policy content.** Customer-managed policy references and
permission boundaries remain excluded from slice A (T03 d4). Permanently excluded from this
phase: the instance and identity source (prerequisites, never adopted); identity-store users
and groups (references only, T03 d3); applications; anything owned or reconciled by
`mcp_gateway01`; management-account-provisioned sets or management-targeting assignments (T15
d4); all Organizations resources (I-4, `01`); everything matching excluded patterns. The
exclusion list is a committed artifact of the plan. Classification: compatible (T15 d4/d6/d7;
T03 d3/d4; I-4; `01`). Rejected: broader eligibility (roles/users) — would widen the permission
envelope and decide deferred architecture by import.

### Decision 5 — Bounded ownership proof before import (adoption manifest)

A per-resource **adoption manifest** entry is a precondition of any import: live identifiers
(tier-2 non-public), alias, discovery evidence pointer, authority-boundary justification (`01`),
**bounded negative ownership proof**, intended post-adoption configuration, and per-increment
Eric approval before the import PR merges. The bounded proof: **enumerate every known
authoritative Terraform backend/workspace/state registry and reconciler within the declared
adoption boundary; record exactly which locations and systems were checked, their
snapshot/version references, and the evidence time; obtain the required human/team attestations
for non-queryable legacy paths.** Incomplete enumeration, an unknown state location, an
unverifiable reconciler, or contradictory ownership evidence is **ambiguous ownership → the
resource is quarantined** (decision 6). **The proof never claims nonexistence across unknown
systems** — it claims exactly what was checked, when, and what was attested. Classification:
compatible (T02 claim 3; `01`; MADR-0004 spirit — repository-provable claims only). Rejected:
class-level blanket approval; any universal "not managed anywhere" claim.

### Decision 6 — Unmanaged / shared / externally reconciled / ambiguous / drifted

Fixed taxonomy, recorded per discovery: **unmanaged + eligible** → adoption candidate
(decision 5 manifest). **Shared or externally reconciled** → excluded from **this adoption
phase** — not necessarily forever: a later, separately governed **ownership-transfer plan** may
make such a resource eligible only after the prior reconciliation path is demonstrably retired
and a new manifest is approved. **Ambiguous ownership** → quarantine: excluded, protected by
the plan gate, escalated to Eric with the evidence; **ambiguity never permits import.**
**Drifted** (live ≠ documented intent) → import is still authored to **live** state
(decision 7); the intent gap becomes a post-authoritative governed change PR, never folded into
the import. Classification: compatible (09; T15 d7; `05`/I-6). Rejected: normalize-as-you-adopt.

### Decision 7 — Import → zero-diff → authoritative transition model

Three explicit per-resource states, each provable: **observed** (in discovery, in manifest) →
**imported** (configuration authored to match live state exactly — for a permission set, the
whole decision-4 bundle; import applied; the mandatory **zero-diff verification plan** — a
saved plan showing no changes — evidenced) → **authoritative** (declared per resource only
after zero-diff; from then on the T15 d7 drift policy applies and this repository is the sole
reconciliation owner). No resource skips a state; the manifest records each transition and its
evidence digest. Classification: inherited (09 §Brownfield adoption; T15 d7; T02 plan/approval
separation). Rejected: import and first reconcile in one step.

### Decision 8 — Increment granularity, ordering unit, and the import mechanism

Configuration-driven **`import` blocks in reviewed code** are mandatory; **CLI
`terraform import` remains prohibited** (out-of-band state mutation); `moved`/`removed` blocks
likewise ride reviewed PRs only. Increment structure (corrected):

- **one permission-set bundle per import increment** — the bundle's core and applicable policy
  child resource are imported **atomically in the same imports-only saved plan**;
- the bundle's import apply and mandatory zero-diff verification complete **before** any
  assignment referencing it is imported;
- **one account-assignment resource per subsequent increment**, consistent with the
  one-assignment-per-file model (T03 d5, T10);
- across a wave, **all selected permission-set bundles precede their assignment increments**.

Each increment = one PR (matching configuration + import blocks) → post-merge saved plan
classified *imports only, zero changes* → explicit approval → that exact plan applied →
zero-diff verification plan evidenced.

**Import-block data handling (corrected):** no live account ID, ARN, GroupId, permission-set
ARN, or composite import ID is ever committed literally to this public repository. Import
`id`/`identity` expressions are **derived at plan time from the encrypted, non-public,
sensitive binding/adoption inputs** (T15 d5/d12, T09 model); import values must be known at
plan time and are treated as sensitive. Saved plans and plan JSON remain encrypted non-public
artifacts and are never printed into public logs; T20/T14 verify that no import identifier
leaks through console rendering, annotations, summaries, diagnostics, or generated artifacts.
Import blocks remain through the import apply and zero-diff verification; **after the resource
becomes authoritative, the completed import blocks are removed in a separate reviewed cleanup
PR whose plan must contain no infrastructure or state operation.** Git history, the adoption
manifest, the commit pointer, and non-public evidence retain import provenance. Terraform
`1.15.7` and `hashicorp/aws = 6.53.0` are used for imports **only after T21/CV-07 verifies the
exact pinned import identities and rendering behavior** for the permission-set core, the
AWS-managed attachment, the inline-policy resource, and the account assignment (decision 22
handoff). Classification: inherited (09 execution rules; T15 d11/d15; T06 d4; T02) with the
sensitive-input rule compatible (I-4/RD-06 strengthened). Rejected: CLI-import runbook;
literal import IDs in configuration.

### Decision 9 — State isolation and movement

The rehearsal runs in its own root and state key — `aws-identity-access/lab/import-rehearsal/`
beside `bootstrap` and `identity-center` (T15 d16 convention) — so slice-A state is never
touched by rehearsal operations. `terraform state mv`, cross-root moves, and any state surgery
are prohibited except as explicitly planned, separately authorized steps with a state-version
backup reference recorded first; consolidation of adopted resources into a long-term root is an
optional, later governed step in the plan, not part of the rehearsal. Classification:
compatible (T15 d16/d6; T02 isolated prefix; 09 — state as high-authority asset). Rejected:
reusing the `identity-center` root.

### Decision 10 — Preventing unintended create, replace, destroy (no destroy exception)

Throughout discovery, import, zero-diff verification, and deliberate rollback, **there is no
destroy exception — nothing makes destroy permissible inside the import phase.** Mechanics: an
import-phase plan is **rejected if it contains any create, update, replace, or destroy**
(imports only); the zero-diff verification plan is rejected unless empty; `-replace`/taint and
destroy-class operations are blocked for the whole phase (09); `lifecycle.prevent_destroy` is
set on every adopted resource **while it remains managed** (its resource block present — the
decision-14 rollback transition substitutes `destroy = false` as the live-object protection);
the protected-resource gate (T15 d7)
continues to cover everything not in the current increment's manifest. Plan-classification is
computable (T20/T14 codes; T21 verifies plan-JSON distinguishability). **An acknowledgement
does not make destroy permissible inside the import phase.** Classification: inherited (09
"destroy-class operations blocked throughout"; T15 d7/d15). Rejected: reviewer-vigilance-only
classification; any human-override destroy escape inside the phase.

### Decision 11 — Adoption ordering and prerequisites

Order: (1) prerequisites verified first — instance reachable, identity-store **group
references resolve** for every principal named by assignments to be adopted (missing group =
stop, never create); (2) **the permission-set bundle before its assignments** — an assignment
is never imported while its bundle is not yet authoritative; (3) assignments one per increment,
workload accounts only; (4) deferred-account references stay deferred (RD-08) — never imported,
never provisioned. Across a wave: all selected bundles, then their assignments (decision 8).
Classification: inherited (T03 d3/d5; RD-05; RD-08; I-1; T15 d4). Rejected: type-agnostic
ordering.

### Decision 12 — Collision, rename, and tag behavior (corrected)

Adopted resources **keep their live names at import** — no rename-on-import, ever; the
`ialab-` prefix marks POC-created resources only and is never applied retroactively. **Tags are
supported on permission sets, not account assignments**: permission-set seeds may be tagged at
their separately authorized creation; account-assignment seeds are identified by their **exact
tuple and adoption manifest, never by tags**; a pre-existing untagged target permission set is
**imported exactly as found** — adding managed-by/project tags to an adopted target permission
set is a **separate post-authoritative governed change, never part of the zero-diff import**.
Tags remain coexistence markers, never ownership authority (T04 d5). A rename after a resource
is authoritative follows T05's two-PR additive-replacement semantics. A new resource whose
deployed name collides with any pre-existing or adopted name remains a protected-resource plan
error (T15 d8); a discovery collision with `ialab-*` aborts the increment. Classification:
compatible (T05; T15 d8; T04 d5; 09 — a rename at import is a change, breaking zero-diff).
Rejected: normalize names at import.

### Decision 13 — Coexistence and cutover windows

Per-resource cutover tied to the decision-7 state: before *authoritative*, the legacy change
path still owns the resource and repository files for it are non-authoritative; from
*authoritative*, any out-of-band mutation is drift (alert → evidence → governed reconciliation
— T15 d7). Each increment declares a **change-freeze window** on its resources from
discovery-refresh to zero-diff verification — in the lab an evidenced Eric commitment; in the
target an enforced control (T06 guard). Freeze violations abort the increment (decision 14).
Classification: compatible (T15 d7; `05`/I-6; T06 guard; 09). Rejected: no declared freeze.

### Decision 14 — Rollback, abort, quarantine, partial migration (exact rollback)

**Rollback of an import is a governed state-only removal**: a reviewed rollback PR **replaces
the adopted resource's configuration block (including its `prevent_destroy` guard) with
exactly**

```hcl
removed {
  from = <resource address>
  lifecycle {
    destroy = false
  }
}
```

During that transition, **`destroy = false` — not `prevent_destroy` — is the live-object
protection.** The saved plan **must classify as state removal only and leave the AWS object
untouched** → approval → apply. The resource returns to unmanaged; nothing is destroyed. **Destroy is never a
rollback mechanism**, and no destroy exception exists inside the import phase (decision 10).
**The state object itself is never copied into evidence** — only its protected state-object
version reference and digest are recorded under the decision-15 evidence model. Abort criteria
per increment: zero-diff not achieved, freeze violated, ownership evidence contradicted,
protected set touched — abort → rollback → **quarantine** (excluded until a new Eric-approved
manifest). A partially applied increment receives a recorded disposition and fresh
authorization before any further action (T15 d11 pattern). Rollback and re-import are
separately approved state transitions even though they do not mutate the live resource.
Classification: compatible (T15 d11; 09; T05). Rejected: destroy-and-recreate rollback; manual
state edits.

### Decision 15 — Evidence, audit, retention, acceptance criteria

The T15 d12 three-tier model applies wholesale: per increment, tier-2 non-public evidence
(discovery snapshot + digest, adoption manifest, saved-plan digests, zero-diff plan, apply log
references, rollback records, state-object **version references and digests — never state
content**), alias-only public summaries, state never in the evidence prefix; retention at least
through the POC phase gate with disposition only by explicit Eric decision (T09 retention
rule). **Acceptance per increment:** imports-only plan applied cleanly + zero-diff verification
plan + protected set untouched + manifest complete + freeze unbroken + full evidence set. An
increment without its evidence is not accepted regardless of live outcome. Classification:
compatible (T15 d12; T09; MADR-0004; T14 public-identifier code). Rejected: final-report-only
evidence.

### Decision 16 — Lab rehearsal scope, seeding, exit criteria, and authorization points

The remediated lab's Identity Center is created fresh (T16), so no genuine legacy resources
will exist; the rehearsal uses **seeded stand-ins**. Scope: two seed permission-set bundles —
one with an AWS-managed attachment, one with an embedded inline document — each with one GROUP
assignment to one lab-workload account; non-`ialab-` names; permission-set seeds tagged at
creation (decision 12); assignment seeds identified by tuple and manifest. Pipeline: discover →
manifest → freeze → author-to-match → import → zero-diff → authoritative → drift probe →
deliberate rollback → re-import → exit → cleanup. Per the corrected increment model this
produces **two bundle increments followed by two assignment increments**, then the exercised
rollback/re-import transitions.

**Separately authorized live-mutation groups (each its own explicit Eric authorization):**

1. Seed permission-set and assignment creation (console/CLI, outside Terraform).
2. The bounded **drift-injection probe** — changes only a privilege-neutral attribute (an
   informational description or an approved tag on a permission-set seed); it must not alter
   policy authority, group membership, or an account assignment.
3. Governed restoration/reconciliation of that probe (the T15 d7 drift path exercised).
4. Post-exit seed cleanup (below).

Rollback and re-import are separately approved state transitions even though they do not
mutate the live resource. **Seed cleanup** happens only after successful rehearsal exit as a
distinct, separately authorized cleanup phase: first a reviewed **no-live-change PR removes the
applicable `prevent_destroy` guard**; then a **separately approved destroy-only saved plan**
removes the seed resources in dependency-safe order (assignments before their bundles).
**Cleanup failure does not retroactively invalidate the rehearsal evidence and does not permit
manual deletion.**

**Exit criteria:** every increment met decision-15 acceptance; one rollback and one re-import
exercised with evidence; the drift probe detected, evidenced, and reconciled through the
governed path; no protected-resource or unintended-change event; alias-only rehearsal report
produced as planned evidence for the target waves. Classification: compatible (T16 d11; T03
d6; T15 d7/d10/d11; 09; zero incremental spend — Identity Center and seeds are free).
Rejected: state-surgery-only rehearsal (never tests authoring-to-match a foreign resource;
touches slice-A state); skipping the rehearsal (conflicts with the T03-d6 mandate).

### Decision 17 — Target-estate wave strategy and prerequisites

Waves per resource class, each gated: **wave 0** — prerequisites proven: the T06 adoption guard
fully verified (no grandfathered lab exceptions), OD-03/OD-04 resolved or explicitly excepted
by owner decision, OD-12 resolved or an owner-approved interim coupled-change protocol in place
(decision 20), the T09 pinned inventory consumption live, discovery + freeze machinery in
place; **wave 1** — permission-set bundles (no principal impact until assignments move);
**wave 2** — account assignments, one per increment, targeting only accounts explicitly
admitted by the separately approved wave manifest, workload before sensitive accounts;
**wave 3+** — deferred durable-access classes only after their slices
define their architecture (decision 1 deferred rows) — sequencing reservation only. Every wave
runs the decisions 3–15 pipeline; a wave closes only on its acceptance evidence. Classification:
compatible (T06 guard; T09; 09; T03 d1; I-8). Rejected: per-account waves mixing classes.

### Decision 18 — Target-estate deployed-name prefix (assigned to T19 by T04 d5)

Target `resource_name_prefix = "ia-"` (3 characters, within T05's ≤ 8) for **newly created**
resources during and after migration — a coexistence marker distinguishing repository-managed
new sets from unadopted legacy sets while both exist. Adopted resources keep their names
(decision 12) and are marked, where applicable, by post-authoritative governed tag changes
only. Revisiting the prefix (including dropping it) after full cutover is a normal governed
change recorded in the plan as an open option. Classification: compatible (T04 d5; T05 d1;
T15 d8 pattern). Rejected: empty prefix from the start (loses the coexistence marker);
deferring the value to S5 (T04 d5 routes it here).

### Decision 19 — Decommissioning superseded reconciliation paths

Per wave, at cutover: the legacy change path for that class is formally retired — recorded in
the plan; post-cutover out-of-band changes are drift by definition (T15 d7) with the
alarm/evidence path active. The bounded Decision-5 checks are re-run and confirm that no
enumerated backend, workspace, state registry, or reconciler — and no required attestation —
identifies another reconciliation owner; this is never a universal nonexistence claim.
Rehearsal seeds are removed by the decision-16 cleanup phase. **The pinned aws_ami `scaffolding/aws-identity-access/` and exploratory
`aws-identity-access/` trees are retired as implementation sources only** — recorded in the
migration note, remaining citable evidence at the pin; **the pinned aws_ami architecture
documents and decision register are not retired — they remain governing platform authority
until properly superseded upstream.** State-prefix or root retirement follows T15 d11 (retire
≠ delete; evidence retained). Classification: compatible (T02 claim 3; T15 d7/d11; T18 §5.6;
brief migration-note deliverable; map Authority note). Rejected: indefinite legacy fallback
paths.

### Decision 20 — OD-09 and OD-12 dispositions

**OD-09:** the repo-local rule fixed by T15 d13 is extended for migration: pins frozen for the
duration of any wave; a pin change between waves is a platform-change PR requiring CV-07
re-verification (T21) and a fresh zero-diff baseline over all adopted resources before the next
increment. OD-09 stays open platform-wide; no new upstream text (T02's document-09 proposal
already carried). **OD-12:** the lab rehearsal requires no cross-repository coupled change; for
the target, **resolution of OD-12 — or an explicit owner-approved interim coupled-change
protocol — is a wave-0 prerequisite** (account renames and inventory write-backs during
migration are its subject; T09's `INV-RENAME` rule applies meanwhile). No upstream amendment
proposed by T19. Classification: compatible (OD-09/OD-12 at the pin; T15 d13; T09; T08 d3 —
this repository consumes, never authors, platform-wide decisions). Rejected: proposing upstream
resolutions from this repository.

### Decision 21 — The S5 brownfield implementation-plan skeleton

Mandatory sections:

1. The fixed T15 d14 items verbatim (staged lab rollout; per-stage verification; governed
   rollback; evidence boundary; document-09 discovery, import/reconciliation sequencing,
   destroy blocking, migration planning).
2. The decision-1 disposition table with per-row basis, and the migration-note content
   (retire rows) for the T23 documentation set.
3. The adoption pipeline (decisions 3–15) as normative procedure: discovery semantics and API
   limitations (decision 3 — provisioned-to-account relationships, asynchronous operation
   records, pagination to a null continuation token, `IN_PROGRESS`/`FAILED` handling); bundle
   and assignment increment ordering (decision 8); bounded ownership proof and manifest
   (decision 5); plan-classification gates (imports-only, empty, state-removal-only,
   destroy-only cleanup, prohibited) with no destroy exception inside the import phase;
   sensitive import-input handling and import-block cleanup PRs (decision 8).
4. The rehearsal plan and exit criteria (decision 16) with **every separately authorized
   live-mutation group and state transition enumerated**: seed creation; each bundle-import
   increment; each assignment-import increment; rollback; re-import; drift probe; probe
   restoration; guard-removal PR; destroy-only cleanup plan.
5. Target wave strategy and wave-0 prerequisites (decisions 17, 20).
6. Target prefix, naming, collision, and tag rules (decisions 12, 18).
7. Rollback points and abort/quarantine dispositions per stage (decision 14).
8. Owner-approval points as an explicit checklist (every stage, increment manifest, rollback,
   re-import, probe, restoration, guard removal, cleanup, and retention decision).
9. Evidence and retention map (decision 15), including the state-object
   version-reference-and-digest rule.
10. Decommissioning schedule and the implementation-source retirement note (decision 19).
11. The deferred-class reservation (decisions 1, 17 — wave 3+).

Classification: compatible (T15 d14; skill-execution-map S5/S6; decision-gated lifecycle —
no decisions at the keyboard). Rejected: a slimmer plan deferring these to S6.

### Decision 22 — Handoff set

Informational handoff comments (no dependency edges) to **T14 #19**, **T20 #22**, **T23 #23**,
**T10 #15**, and **T21 #20** — exact texts in the tracker payloads; the T21 handoff (added by
correction 7) requests exactly six verifications:

1. the exact Terraform `1.15.7` and `hashicorp/aws = 6.53.0` pins are active;
2. configuration-driven import support and exact import identities for the permission-set
   core, AWS-managed attachment, inline-policy resource, and account assignment;
3. `removed` blocks with `lifecycle { destroy = false }`;
4. permission-set-only tag support;
5. sensitive import expressions and public-output redaction;
6. deterministic plan-JSON classification of import-only, empty, state-removal-only, and
   prohibited create/update/replace/destroy classes.

**S5 requirements:**
this record and the decision-21 skeleton are consolidation inputs; the decision-13 backfill
prerequisite from T08 stands. **S6 seeds:** rehearsal-seed authorization; import-rehearsal root
bootstrap; plan-classification implementation; import-block cleanup PR class. Classification:
compatible (T15/T09 handoff pattern). Rejected: S5-only handoffs.

## Dependency effects and frontier

#14 carries no native dependency edges (blocked-by 0 — T02/T03/T18 closed; blocking 0).
Closing #14 releases nothing. Live frontier after closure, in map order: **T10 #15 (next
claimable)** · T21 #20 · T22 #21 · T23 #23. T20 #22 remains blocked (three open blockers:
#15, #20, #21); T14 #19 remains blocked (four: #15, #20, #21, #22).

## Publication sequence (fail-closed; record before close)

Executed only under Eric's consolidated publication approval. A failure at any step through 8
leaves #14 open, with all later normal publication steps unperformed; completed remote writes
are not automatically undone. The exact partial state is preserved through a Repository
Continuity Artifact where necessary and reported.

1. Create this record at `docs/wayfinding/map-1/14-brownfield-adoption-and-migration-strategy.md`
   and the `docs/wayfinding/README.md` index line in the working tree.
2. Validate them: frontmatter parses, internal links resolve, and the mechanical correction
   checks pass on the final bytes.
3. Commit both on `main`; push (authorized as part of the consolidated approval).
4. Verify the immutable record URL at the pushed commit resolves and is byte-equivalent to the
   local file.
5. Post the exact #14 resolution comment, with the record commit SHA filled in.
6. Post the exact informational handoff comments to T14 #19, T20 #22, T23 #23, T10 #15, and
   T21 #20; no dependency edges.
7. Update map #1: append exactly one T19 Decisions-so-far line. No fog edit and no map-order
   change (T19 graduates nothing and creates no ticket).
8. Round-trip verify: the #14 resolution comment, all five handoff comments, and the complete
   map #1 diff (exactly the one addition).
9. If any step through 8 fails: leave #14 open, perform no later normal publication step,
   preserve the exact partial state through continuity if necessary, and report it.
10. Close #14 as completed, retaining assignee `a24577t`, with the close comment.
11. Round-trip verify the close.
12. Recompute all dependency effects and the live frontier (expected state above) without
    claiming anything.
13. Replace the Repository Continuity Artifact (position after T19; frontier at T10 #15;
    rehearsal and backfill authorization boundaries restated); commit and push.
14. Verify `HEAD == origin/main`, a clean working tree, and the final tracker invariants
    (#14 closed with assignee retained; no other issue state changed; map body as verified).

Post-close failure rule: if a failure occurs after step 10, do not reopen #14 and do not
duplicate earlier writes; record the precise partial state in continuity where possible, report
it, and stop.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Verdict⟧ and ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub mutation,
an import, a seed, a probe, a cleanup, or any implementation.
