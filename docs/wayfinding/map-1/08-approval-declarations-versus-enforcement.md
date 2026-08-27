---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 8
title: "T06 — Approval declarations versus enforcement"
url: https://github.com/a24577t/aws-identity-access/issues/8
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-27
sources:
  backfill: "T08 #13 decision 13 result-record backfill, reconstructed 2026-08-27 from the ticket's complete comment history; traceability, not authority"
  t05_handoff_comment: https://github.com/a24577t/aws-identity-access/issues/8#issuecomment-5382918672
  resolution_comment: https://github.com/a24577t/aws-identity-access/issues/8#issuecomment-5383470321
  close_comment: https://github.com/a24577t/aws-identity-access/issues/8#issuecomment-5383474172
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  resolved: 2026-08-22 (grill) / 2026-08-23 (published and closed)
---

# T06 — Approval declarations versus enforcement (slice A)

> **Backfilled discovery record** — produced 2026-08-27 under the separately authorized T08
> #13 decision-13 result-record backfill, reconstructing the complete durable result of
> T06 #8 from the ticket's comment history. Backfill preserves provenance and traceability
> only: it confers no new authority, changes no decision, and does not alter the approved S4
> Architecture Grill verdict. **Nothing here is accepted architecture: every decision is a
> proposal until ⟦G-Accept⟧.** GitHub issue #8 is the workflow/index surface and links to
> this record.

Grill completed with five HITL decisions approved by Eric as the human project owner and
decision authority. Claude executed the session in the repository-owner role under
`wayfinder-repo-owner` with `grill-with-docs` (both invoked by loading and executing their
SKILL.md instructions; both are `disable-model-invocation`), 2026-08-22. Governing documents
cited at the aws_ami revision pinned by T01 (#2); the T18 inventory and the T05
resolution/handoff were used as evidence and closed-decision inputs. Nothing below accepted
architecture, implemented anything, configured GitHub, or authorized an AWS mutation. GitHub
capability facts are recorded as current implementation constraints, not domain
architecture.

**Inherited T05 #7 handoff (recorded on the ticket):** (1) a change to a group's
`identity_store_name` requires identity-platform and security review; T06 defines the
enforcement. (2) A stable-key rename carries the strictest required owner set across every
touched surface. (3) A resolved GroupId that differs from state under an unchanged key is
principal replacement, not a rename — T06 defines the separately declared and approved
principal-replacement workflow. (4) Optional `source` metadata is non-authoritative
provenance with no approval semantics. (5) `--` is the only reserved key token in slice A;
T06 may introduce separately governed runtime namespaces later.

## Capability facts observed (keyring read, 2026-08-22)

Repository `a24577t/aws-identity-access`: **public**, owner type User; `main`
**unprotected**; **no rulesets**; **no environments**; **one collaborator** (`a24577t`,
admin); no CODEOWNERS on `main`. Consequence: GitHub Free provides CODEOWNERS, branch
protection/rulesets, and environment protection for this public repository; independently, a
single collaborator cannot provide independent review or approval of their own change.

## Decisions (approved by Eric)

**1. Approval model — three distinct layers.**
- *Declared ownership:* every governed file carries a stable owner-registry key —
  informational routing metadata validated against the ownership registry; never itself an
  approval, authorization, signature, or evidence that review occurred. CODEOWNERS is
  generated from the registry and the committed/generated artifact is validated to match.
  Routine approval declarations are not duplicated inside requester files.
- *Enforced review:* target-state invariant — changes enter the protected branch only
  through a pull request, applicable owner review is required, direct pushes are blocked.
  CODEOWNERS provides ownership resolution and review routing; it does not independently
  enforce review. Enforcement requires an available branch-protection or ruleset mechanism
  (the eligible mechanism for the repository and plan; "ruleset" is not hard-coded). Listing
  several owners in one CODEOWNERS rule does not enforce approval from every owner (GitHub
  accepts any one listed code owner); where policy requires distinct classes
  (identity-platform AND security) each class is enforced independently through eligible
  required-reviewer/ruleset/check mechanisms, and any class the plan cannot enforce is
  recorded as unenforced.
- *Independent approval classes:* each simultaneously required review class is an
  independent approval obligation. One review event, or one physical GitHub identity, cannot
  satisfy more than one independently required class for the same change unless an accepted
  governing rule explicitly allows co-satisfaction. Mapping the same GitHub account to
  logical principals in several required classes does not create independent approval. In
  the current single-collaborator lab such classes remain technically unenforced; the lab
  exception covers the reduced assurance but must not report those classes as independently
  satisfied. Enforcement evidence records the logical principal, the physical reviewer
  identity, the review event, and the single required class that event satisfied; duplicate
  reviewer identities across independently required classes are an enforcement failure or a
  lab-exception condition. (`satisfied_by` sets need not be globally disjoint; the
  constraint applies to satisfying the independent classes for a particular change.)
- *Apply authorization:* separate from ownership and code review; bound to the reviewed
  saved plan and its deployment scope ("deployment-environment approval" is the logical
  boundary; decision 4 selects the mechanism); never inferred from a merge, CODEOWNER
  approval, owner key, issue assignment, or prior lab approval.
- *Lab constraint:* decision 3 defines an explicit lab-only exception where the
  repository/plan/collaborator topology cannot enforce the target invariant — reduced or
  detective assurance, never enforced independent approval, never the target model.
- *Approval artifacts:* declared approval fields only where upstream requires a durable
  artifact — exceptional rename/principal-replacement acknowledgements (decision 5) and
  governed exception-class records (none in slice A).

**2. Ownership registry.** `governance/ownership/principals/<principal-key>.yml` — stable,
provider-neutral logical principals (not GitHub users): required `key`,
`kind: role | team`, `description`; governed files reference a principal key through
`owner`; no review-class membership and no GitHub usernames/teams/e-mails or other provider
handles in these records — the principal-to-GitHub-handle binding is an implementation
mapping deferred under document 10. `governance/ownership/review-classes/<class-key>.yml` —
independent approval classes: required `key`, `description`, `satisfied_by` (non-empty list
of principal keys); the sole authority for the class-to-principal relationship; every
referenced principal, duplicate, missing record, and empty satisfaction set is validated;
multiple classes remain independent, and a principal (or the physical identity behind it)
appearing in several classes' `satisfied_by` never lets one review event satisfy more than
one required class for a change (decision 1). No authored enforcement-status scalar: a class
declares normative semantics; actual enforcement is derived and evidenced (decision 3); an
authored `enforced` value never substitutes for verification. Generation chain: governed
path → required review class(es) → satisfying logical principal(s) → implementation GitHub
handle mapping → CODEOWNERS/protection configuration; generated CODEOWNERS validated against
all authoritative inputs; `owner` remains declared ownership, not approval evidence.
Registry changes carry the strictest applicable owner and review-class requirements; the
registry and its generation/mapping inputs are protected against self-approval or silent
weakening and are never self-authorizing (bootstrap mechanism: see "Derived items").
Rejected: option A's bidirectional class membership and self-declared enforcement status.

**3. Routing, enforcement evidence, lab exception.**
- *Routing semantics:* routing yields a set of required independent review classes; all
  matching routes combine by set union; a more-specific route never erases a stricter
  matching requirement; GitHub's last-match-wins is not the domain model (the generator
  orders and validates CODEOWNERS safely); every governed path matches an explicit route or
  a fail-closed default — an uncovered path is a validation error.
- *Slice-A requester routes:* `access/identity-center/configuration/instance.yml`,
  `access/identity-center/groups/**`, `access/identity-center/permission-sets/**` →
  identity-platform + security (conservative path-level enforcement: a provenance-only edit
  to `source` may receive security review; `source` does not become an identity binding).
  `access/identity-center/account-assignments/<account-name>/**` → inventory-resolved
  account delegation; for slice A the resolved requirement is identity-platform; an
  unknown, ambiguous, inactive, or otherwise unroutable account is an error, never a
  permissive fallback; later target-estate delegation may add account-specific classes
  through governed inventory data. Requester README/documentation → identity-platform.
- *Platform and control-surface routes (strictest set = identity-platform + security +
  architecture):* `governance/**`, `schemas/**`, `infrastructure/**`, `src/**`, `tests/**`,
  `.github/**`, `.ai/**`, `.claude/**`, `CLAUDE.md`, `docs/architecture/**`,
  ownership-registry records, path-routing records, principal-to-GitHub-handle mappings,
  CODEOWNERS generation and validation code, CI/workflow definitions,
  enforcement-evidence generation/validation code. Other project documentation (research,
  guides, agents, generated) → at least identity-platform unless a more-specific route is
  stricter. Root-level control files inventoried on `main` @ 3643cf7 and routed:
  `.gitignore`, `LICENSE`, `aws-identity-access-poc-prompt.md` (digest-verified intake of
  record, T01) → strictest set; `README.md` → identity-platform. The rule protects
  modifications to `.ai/**`; it does not broaden or reclassify accepted `.ai` governance
  authority.
- *Enforcement evidence (derived, never self-declared):* for every governed route and
  required class, per control: repository identity and visibility; observed plan/capability;
  protected branch; required-PR/direct-push control; required status checks; CODEOWNER
  review routing; independently enforced reviewer class where required; active ruleset or
  branch-protection identifier; bypass actors/roles; observation timestamp; source commit;
  API/source used; result `enforced | unenforced | unknown | lab-exception`; applicable
  governed exception reference. No single aggregate flag; partial enforcement stays visible.
  API failure, insufficient permission, stale observation, missing rule, unexpected bypass,
  or unverifiable reviewer topology → `unknown`/`unenforced`, never `enforced`. The
  generated report is non-authoritative evidence; CI compares live configuration with
  normative routing; the plan/apply gate consumes evidence bound to the commit and saved
  plan and blocks when a required control is `unenforced`/`unknown` unless an applicable,
  current lab exception covers that exact control. The checker and workflow are protected
  from modification by the change they evaluate (trusted base-branch definitions or an
  equivalent fail-closed mechanism).
- *Independent-class evidence:* for every change, enforcement evidence records, per
  required class, the logical principal, the physical reviewer identity, the review event,
  and the single class that event satisfied; a review event or physical identity counted
  toward more than one independently required class — absent an accepted governing rule
  allowing co-satisfaction — is recorded as an enforcement failure or a lab-exception
  condition, never as independent satisfaction (decision 1). In the single-collaborator lab
  the identity-platform, security, and architecture classes therefore remain technically
  unenforced for any change requiring more than one of them.
- *Lab-only exception (recorded in T15's lab contract, not in requester files):* identifies
  repository, branch, lab deployment scope, visibility/plan, reviewer topology; enumerates
  each unavailable or unenforced control separately; distinguishes server-enforced from
  procedural/detective controls; never claims PRs, no-direct-push, required checks, or
  code-owner approval are enforced unless live evidence proves each; requires PR/merge
  records and validation evidence procedurally where server enforcement is unavailable;
  states that code-owner review may be requested but is not independently enforceable with
  the single-collaborator topology; prohibits target/production use; expires at POC
  acceptance or an earlier stated date/milestone; requires reevaluation on any change of
  visibility, plan, collaborator topology, branch rules, or deployment scope; never
  satisfies a target-state assurance claim; authorizes reduced lab assurance only — never an
  AWS apply.
- *Classification:* instance and group security co-review — inherited/compatible with 10;
  permission-set security co-review — domain refinement beyond 10; inventory-resolved
  assignment delegation — compatible; live enforcement evidence and control-by-control lab
  exception — absent upstream, compatible with the declared/enforced distinction; no
  upstream document amended.

**4. Plan/apply authorization — environment gate + environment-bound OIDC + plan-digest
binding.**
- *Jobs and identities:* separate validation, read-only plan, and environment-gated apply
  jobs; the plan job holds only the separate read-only planning role; the apply job is the
  only mutation-capable identity and requests mutation-capable AWS credentials only after
  every verification below passes.
- *What may be applied:* only the exact approved saved plan, for the exact approved commit
  on protected `main`; apply never re-plans, never falls back to a newly generated plan or a
  bare `terraform apply`. The apply job downloads the approved encrypted plan by immutable
  artifact ID — never merely by artifact name — and verifies the plan-file digest, artifact
  digest, sanitized-summary digest, source commit, state basis, inventory snapshot,
  enforcement evidence, deployment scope, and expiry before requesting credentials.
- *Environment and branch:* the `lab` environment is restricted to the approved deployment
  branch; administrator bypass is disabled where supported and otherwise recorded per
  control as unenforced/lab-exception; deployment concurrency limits lab applies to one at a
  time.
- *Binding:* authorization is bound to the plan-file SHA-256, source commit, artifact
  ID/digest, sanitized-summary digest, deployment scope, inventory snapshot, state basis,
  tool/provider pins, enforcement evidence, approver, environment, and expiry. One approval
  authorizes one plan, one deployment scope, one apply attempt; replay, stale plans,
  mismatched state, superseded artifacts, and silent fallback are blocked; reruns or
  recovery after partial mutation require explicit disposition and new authorization.
- *Transport:* the binary plan is encrypted during planning with public encryption
  material; environment-gated private decryption material is available only to the apply job
  after the `lab` gate. Plaintext plan files, state, unredacted plan JSON, credentials, and
  secret-bearing logs are never public artifacts of this public repository. The approver
  receives a sanitized human-reviewable plan summary before approval. Short artifact
  retention; encrypted transport artifacts deleted after terminal audited disposition;
  non-secret digests and evidence retained.
- *OIDC trust:* the exact observed GitHub subject format — immutable repository identity
  where applicable, the `lab` environment, the trusted workflow identity, audience
  `sts.amazonaws.com` — with no wildcard repository, environment, workflow, branch, tag, or
  pull-request trust.
- *Approval authority:* the `deployment-authority` class maps to the environment's required
  reviewers. Target state enables self-review prevention and requires an independent
  deployment authority; the current single-collaborator self-approval is recorded honestly
  as reduced lab assurance under the lab exception — not independent approval, forbidden for
  target/production — and self-review prevention is enabled as soon as an independent
  reviewer exists.
- *Authorization evidence (generated; never requester fields; never content under
  `access/`):* immutable repository identity; protected branch and source commit; workflow
  path/revision; plan/apply run IDs and attempts; deployment/environment record ID;
  approver and timestamps; self-review-prevention status and lab-exception reference;
  account names and resolved IDs; inventory digest; Terraform/provider/lock pins;
  backend/workspace/state-key identity and state lineage/serial where available; plan-file,
  artifact, and summary digests; encryption key identifier; enforcement-evidence reference;
  exact issued OIDC subject; planning/deployment role ARNs; expiry, consumption status, and
  final outcome.
- *Classification:* absent upstream while OD-04 remains open; compatible with document 09
  and T02.

**5. Change declarations for exceptional changes.** One schema-validated file per active
exceptional change: `governance/change-declarations/<declaration-key>.yml` — governed
intent, not approval evidence; no acknowledgements inside requester files; PR labels/issue
links alone never authorize; no `approved_by`, approval timestamps, GroupIds, ARNs, account
IDs, or other generated/runtime evidence in the declaration (runtime identifiers appear only
in generated plan/apply evidence); GitHub review and merge evidence establishes approval.
- *No self-authorization — lifecycle:* (1) preparatory declaration PR adds the declaration,
  receives every derived required review, merges to the protected base; (2) the exceptional
  change PR(s) reference the already-merged declaration — the plan gate resolves it from the
  trusted base; a declaration present only on the change branch is intent-under-review,
  never active authorization; (3) terminal cleanup PR, only after completion evidence proves
  the terminal state, removes the active declaration, references the immutable
  approval/execution/completion evidence, and receives the strictest applicable reviews.
- *Discriminated kinds* — common required fields: `schema_version`, `key`, `kind`, `owner`,
  `justification`, immutable `change_reference`, `deployment_scope`, `valid_from`,
  `valid_until`, affected paths/resource keys, permitted phase/operation, expected
  plan-effect class, applicable lab-exception reference if any. `principal-replacement`:
  `group_key`, reason the external principal is replaced, permitted deployment scope,
  explicit statement that a GroupId change is expected, no GroupId value.
  `group-key-rename`: `from_key`, `to_key`, affected assignment-reference scope, expected
  plan effect fixed to zero AWS mutations. `permission-set-key-replacement`: `from_key`,
  `to_key`, phase `introduce` (creates only; parallel assignments; old resources retained)
  or `retire` (immutable reference to verified introduce-phase completion evidence; plan
  effect fixed to retiring only the old assignments and old permission set; explicit destroy
  acknowledgement). Whether introduce and retire are separate declarations or separately
  approved phases of one declaration is an implementation choice; either design must prevent
  retire authorization before verified introduce completion.
- *Review classes are derived, never requester-authored:* the union of the kind's semantic
  requirements, decision-3 routing for every affected path, routing for
  `governance/change-declarations/**` (strictest set, so architecture review applies), and
  the strictest owner set across touched surfaces; a generated review-class summary is
  non-authoritative evidence; the requester cannot weaken approval by editing a class list.
- *Plan-gate matching:* exactly one current declaration matching kind and phase, source
  commit/base ancestry, affected stable keys and paths, deployment environment and scope,
  expected plan-effect class, validity window, immutable change reference, and prerequisite
  completion evidence. Reject: no match; multiple matches; expired/not-yet-valid; not merged
  into the trusted base; mismatched keys/phase/paths/environment/accounts; creates,
  updates, replacements, or destroys outside the authorized shape; a different GroupId where
  principal-replacement is not the declared kind; group-key-rename plans containing any AWS
  mutation; introduce plans containing deletes/replacements; retirement without verified
  introduce completion. A declaration authorizes only its exact exceptional operation —
  never unrelated changes in the same PR or plan.
- *Evidence (generated, not the declaration):* declaration blob/commit digest; approval PR
  and merge commit; reviewers and satisfied independent classes; lab-exception status; plan
  digest and plan-effect comparison; source commit; deployment scope; execution
  authorization; apply result; terminal completion evidence. Lab self-approval references
  the bounded lab exception and is never represented as independent security or
  architecture approval.
- *Retirement:* `valid_until` mandatory, indefinite declarations prohibited; expired
  declarations fail closed; removal only through the terminal cleanup PR after verified
  completion; Git history and generated evidence retain the audit trail; a failed or
  abandoned change requires explicit disposition before cleanup; removal never erases
  history.
- *Classification:* absent upstream; compatible with document 05's
  exceptional/emergency-change artifact shape and RD-05's declared-exception pattern;
  preserves decision 1 (no duplicated person-approval fields).

## Derived items (no separate HITL decision — flagged for Eric's review at resolution)

- **Claim (3) — no `pa-*` reserved namespace; ownership from explicit metadata.** Resolved
  by decisions 1–2 and T05 decision 5: reconciliation/runtime ownership comes from explicit
  contract fields (05 `reconciliation`, `approval authority` → a review-class key) and
  ownership-registry metadata, never from a name pattern; no reserved namespace is adopted
  in slice A (`--` remains the only reserved key token; a separately governed runtime
  namespace may be introduced later by a governed decision, not by convention).
- **Authoritative source for "generated / AWS-owned role name" exclusions.** Slice A
  contains no IAM roles. The authoritative basis for excluding generated identifiers is
  document 02's generated-identifier invariant as applied by T05 decision 3
  (`AWSReservedSSO_*` names/ARNs and permission-set ARNs are outputs); a name-pattern list
  (`excluded_role_patterns`, T18 X37/S05) is evidence of a rejected convention, not an
  ownership mechanism. A future role slice derives exclusions from that invariant and the
  registry, never from a defaults file.
- **Registry bootstrap / root protection.** Decisions 2–3 make the registry, routing
  records, handle mappings, generator, and evidence checker strictest-set surfaces evaluated
  from the trusted base; the concrete bootstrap (the first registry/CODEOWNERS/protection
  commit and who may alter protections) is an implementation item carried to T15 (lab) and
  the S5 plan, under document 09's documented-bootstrap rule.

## Claim-resolution record (grill-with-docs)

**1. Ownership, CODEOWNER review, security approval, and runtime approval are distinct
concepts with stable keys.** Authority: 10 (tiers and cross-cutting rules), 05 (`approval
authority` declared; contract approved by CODEOWNERS), 01/RD-05 (exception records), I-8.
Result: the distinction is **inherited**; stable keys for each are **absent** upstream and
**compatible** (decisions 1–2). Upstream: none.

**2. A governed organizational-principal registry under `governance/ownership/`.**
Authority: 10 L9-12 ("expressed as roles; concrete team/individual mappings are assigned at
implementation"), RD-04, I-1. Result: **absent** upstream; **compatible** with 10's
roles-first / provider-mapping-later separation and RD-04 (decision 2). Upstream: none.

**3. No `pa-*` reserved namespace — runtime/reconciliation ownership from explicit contract
or ownership metadata.** Authority: 05 (`reconciliation`, `approval authority` fields;
"never a second source of governance authority" I-3), 02 generated-identifier invariant.
Result: **compatible** — ownership by explicit metadata is the documented shape; a
reserved-name convention is **absent** upstream and rejected as an ownership mechanism
(REVIEW Q4). Upstream: none.

**4. Declared approvals coexist with CODEOWNERS enforcement without drifting (REVIEW
Q4/Q13).** Authority: 10, 05, RD-05. Result: **compatible with refinement** — drift is
removed by construction: one registry is the source, CODEOWNERS is generated and validated
against it, enforcement status is derived from live configuration, and declared approval
artifacts exist only as change declarations and exception-class records (decisions 1, 2, 3,
5). Upstream: none.

Evidence used (not authority): T18 X09 (hand-written CODEOWNERS; 3 aliases vs 7 `owner:`
values), X13/S19 (`approval_authority` drift, REVIEW L104-108), X36/X41/X42/X62 (declared
exception shapes), X37/S05 (`pa-*`, `excluded_role_patterns` — rejected conventions).

## Downstream handoffs (as they occurred)

Handoff comments carrying each ticket's inherited T06 constraints were posted before #8
closed on T09 #12, T10 #15, T14 #19, T15 #10, T16 #11, T19 #14, T20 #22, and T21 #20; each
links back to #8. T22 #21 received no T06 handoff.

## Upstream proposals

None. No accepted aws_ami document is amended by T06.

## Glossary candidates (S5 `domain-modeling`)

**Review class** — an independent class of approval (e.g. identity-platform, security,
architecture, deployment-authority) satisfied by registered principals. **Principal
(ownership registry)** — a stable, provider-neutral role or team; never a GitHub identity.
**Change declaration** — a merged, expiring governed record of intent that a plan gate
requires before accepting an exceptional operation. **Enforcement evidence** — a derived,
per-control, non-authoritative record of what GitHub actually enforces for a governed route.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub mutation, and nothing
was configured in GitHub or AWS by T06. This backfill record changes nothing decided by T06.
