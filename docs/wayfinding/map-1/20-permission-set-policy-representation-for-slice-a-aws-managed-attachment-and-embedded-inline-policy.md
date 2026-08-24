---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 20
title: "T21 — Permission-set policy representation for slice A: AWS-managed attachment and embedded inline policy"
url: https://github.com/a24577t/aws-identity-access/issues/20
type: prototype
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-23
sources:
  decision_batch: "consolidated 9-question HITL batch (2026-08-23); Eric + collaborator selected 1A–9A with corrections to Q2, Q4, Q5, Q6, Q8, and Q9, applied throughout"
  inherited_inputs:
    - https://github.com/a24577t/aws-identity-access/issues/20 (five comments: T05 file identity, T06 change semantics, T07 detection duty, T15 pins and tags, T19 verification items)
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  capability_sources: "Terraform v1.15.7 local binary (empirical plan runs); hashicorp/terraform-provider-aws docs at the immutable v6.53.0 tag (a0c8167); Terraform import-block reference documentation"
---

# T21 — Permission-set policy representation for slice A: AWS-managed attachment and embedded inline policy

> Proposed discovery record — the complete durable result of T21 #20. Decisions approved by Eric
> as the human project owner and decision authority after collaborator review; executed by Claude
> in the repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`, using the
> batch-question directive (operating-guide governing invariant 3). **Nothing here is accepted
> architecture: every decision is a proposal until ⟦G-Verdict⟧ and ⟦G-Accept⟧.** GitHub issue
> #20 is the workflow/index surface and links to this record.

## Authorization scope of this record

Approving publication of this T21 result records the **proposed permission-set policy
representation and the CV-07 verification disposition only**. It does **not** authorize any AWS
call or mutation, GitHub configuration, Terraform execution against AWS, implementation, or
backfill. IAM and IAM Identity Center are offered at no additional charge; **actual assumption
or use of the specimen permissions remains separately authorized** and is not authorized here.
Everything remains proposed pending ⟦G-Verdict⟧ and ⟦G-Accept⟧.

## Governing documents and evidence

Cited at the `aws_ami` revision pinned by T01 (#2): `07-identity-center-platform.md`
(manageable boundary; verify against the pinned provider), `12-capability-validation.md`
(CV-07; unsupported features become temporary dated exceptions, never silent workarounds),
`02-configuration-model.md` / RD-04 (one resource per file; path↔key agreement), I-1, RD-05,
RD-06. Inherited map decisions: T03 #4 (d4 — two permission sets; profile-vs-domain
separation), T05 #7 (key/description/deployed-name rules; T21 owns session duration, relay
state, policy representation, equivalence demonstration), T06 #8 (key-replacement declaration
flow), T07 #9 (detection duty and its minimum rule set; non-narrowing requirement), T15 #10
(d13 pins; d8 tags; d12 alias-only examples), T19 #14 (six verification items), T10 #15
(assignment references by key). Evidence (never authority): T18 rows X24/X25/X26/X37/X60/X75;
S17/S24/S05.

## Verified pinned-version capability facts (primary sources; no AWS contact)

| # | Fact | Source |
|---|---|---|
| F1 | Terraform **v1.15.7** confirmed locally — the exact T15 d13 pin | local binary |
| F2 | `hashicorp/aws` **6.53.0** fetched and hash-locked in a scratchpad-only workspace (`h1:eD0xCJQCp+iQQKpU/SpMk/pGRrkF16UUJAEMCXvWCWo=`) | `.terraform.lock.hcl` |
| F3 | Full ssoadmin resource surface at `v6.53.0` (14 types) enumerated at the immutable tag `a0c8167`: the four slice/adoption resources exist; `aws_ssoadmin_customer_managed_policy_attachment` and `aws_ssoadmin_permissions_boundary_attachment` also exist — slice-A exclusion is profile policy, not a capability gap | provider repo tree @ tag |
| F4 | `aws_ssoadmin_permission_set`: `name`, `instance_arn` required/forces-new; `description`, `relay_state` optional; `session_duration` optional, ISO-8601, default `PT1H`; `tags` supported (`default_tags` inheritance, `tags_all`); import id `<permission-set ARN>,<instance ARN>`; import block documented | docs @ v6.53.0 tag |
| F5 | `aws_ssoadmin_managed_policy_attachment`: three required forces-new args; import id `managed_policy_arn,permission_set_arn,instance_arn`; attachment triggers re-provisioning to assigned accounts; deletion ordering vs assignments via `depends_on`; never combined with `*_exclusive` | docs @ tag |
| F6 | `aws_ssoadmin_permission_set_inline_policy`: `inline_policy`, `permission_set_arn`, `instance_arn` required; one inline policy per permission set; import id `permission_set_arn,instance_arn`; `jsonencode()` guidance | docs @ tag |
| F7 | `aws_ssoadmin_account_assignment`: six required forces-new args (`principal_type` USER/GROUP; `target_type` AWS_ACCOUNT); **no tags argument or attribute**; import id `principal_id,principal_type,target_id,target_type,permission_set_arn,instance_arn` | docs @ tag |
| F8 | Plan-JSON action classes empirically demonstrated at 1.15.7 (offline, builtin provider): `["no-op"]`, `["update"]`, `["delete","create"]` (replace), `["forget"]` for `removed { lifecycle { destroy = false } }` (state-removal-only), `["delete"]`; `prevent_destroy` accepted; the T19 rollback mechanics (resource block replaced by the removed block) parse and plan exactly as specified | scratchpad runs |
| F9 | Import-block `id`: a string or expression evaluating to a string, known during plan (variables/locals allowed). Sensitive/ephemeral-value restrictions are not documented on the official reference pages. The plan-JSON import marker is `change.importing` (with `change.importing.id` carrying the import identifier) — its rendering, sensitivity, and redaction behavior are **not demonstrable on this host** and remain an OPEN verification (decision 8) | Terraform docs; F10 |
| F10 | Environmental record: `GetProviderSchema` for the pinned AWS provider fails on this authoring host — TLS interception (Norton) breaks the Terraform↔plugin loopback mTLS handshake (`x509: certificate signed by unknown authority`). Exact AWS-provider schema/validate/plan execution on this host: **NOT RUN / BLOCKED**. **Lab-CI execution remains unverified.** | `tf.log` |

## Claim-resolution record (grill-with-docs)

Per claim: governing document + identifier · claim · result · upstream amendment/refinement.

| # | Claim | Authority | Result | Upstream amendment / refinement |
|---|---|---|---|---|
| 1 | An AWS-managed policy attachment is referenced by stable AWS policy name/ARN as configuration, never a generated identifier | 02 path rule; RD-06; X60 | **compatible** — the full `arn:aws:iam::aws:policy/...` form for the current commercial AWS partition, described as **partition-qualified stable AWS-managed-policy vocabulary, not globally identical across every AWS partition** (decision 2); never a generated identifier | none |
| 2 | The inline policy document is embedded in the permission-set file and never references an account-local policy | X60 (inverting S24); REVIEW Conflict 1; F6 | **inherited** — embedded document (decision 5); account-local references impossible by schema | none |
| 3 | Customer-managed references are absent from slice A and rejected as out-of-slice by the profile — not a domain prohibition | T03 d4; F3 | **compatible** — `P-OOS-*` profile code family, error severity, wording states "out of slice A — not prohibited by the domain architecture" (decision 7); the capability exists at the pin | none |
| 4 | Every Identity Center feature the two example files use is supported by the provider at the T15 pin (CV-07) | CV-07; F1–F9 | **split disposition** (decision 8): documentary PASS at the exact pins + empirical PASS for Terraform-core plan classes; authoring-host provider execution NOT RUN/BLOCKED; lab-CI execution unverified; import-ID rendering/sensitivity/redaction OPEN and mandatory before any T19 import rehearsal | none |

## Decisions

Eric and the collaborator selected 1A–9A with corrections to decisions 2, 4, 5, 6, 8, and 9,
applied throughout.

### Decision 1 — Permission-set file shape and policy-form exclusivity

Fields: `key` (T05: 2–24, filename stem), `description` (required, 1–700, AWS pattern),
`session_duration` (required — decision 3), and exactly one of `managed_policies` (form 1) or
`inline_policy` (form 2). The **selected-slice profile** requires exactly one entry in
`managed_policies` and forbids mixing forms in one file; the **domain schema** admits both
fields and multiple managed policies for later slices. No `tags`, `relay_state`
(decision 4), `display_name`, ARN, or deployed-name field in YAML — deployed Name and the
T15 d8 tags are derived in `infrastructure/` (T04 d5; F4 confirms tag support there).
Rejected: a slice-shaped domain schema (hardens a profile boundary into domain architecture).
Classification: compatible (T03 d4; T05; RD-04).

### Decision 2 — AWS-managed policy reference form (corrected)

`managed_policies` entries use the full `arn:aws:iam::aws:policy/...` form **for the current
commercial AWS partition**; the validator requires that exact prefix, which is itself the
aws-managed guarantee (X60's device). This form is **partition-qualified stable
AWS-managed-policy vocabulary — not globally identical across every AWS partition**; a future
non-commercial-partition deployment is a new governed decision. It is configuration
vocabulary, never a generated identifier and never a live lab identifier. **T14's
identifier-leak rule may exempt only the narrowly validated AWS-managed-policy ARN pattern
(`arn:aws:iam::aws:policy/...`); arbitrary ARNs remain prohibited** in committed content.
Rejected: bare policy names with infrastructure-side ARN derivation (invisible derivation
policy). Classification: compatible (02; RD-06; F5).

### Decision 3 — `session_duration` policy and values

`session_duration` is required and explicit in every permission-set file — no inherited
defaults, ever (the defaults layer is retired, T19 d1). Slice values: `read-only` = `PT8H`;
`identity-inventory-reader` = `PT1H` (equals the provider/AWS default, stated explicitly).
Rejected: uniform `PT1H` (needless re-authentication friction on read-only); omitting the
field (reintroduces an invisible default). Classification: compatible (values absent
upstream; explicitness follows the no-defaults decision; F4).

### Decision 4 — `relay_state` (corrected)

`relay_state` is **omitted from slice A** (absent = AWS default portal behavior). The domain
schema defines the optional field so a later slice can adopt it without schema change; the
profile leaves it unused. **Any future domain constraint on its value must mirror the exact
pinned provider/AWS contract once verified; until then that validation is deferred to T14** —
no generic value-shape rule is asserted here. Rejected: setting it in the slice (any value
would be invented). Classification: compatible (absent upstream; F4).

### Decision 5 — The two example files (record specimens; corrected)

Approved exactly as shown. Keys are illustrative pending S5 authoring; alias-free; no live
identifiers. The earlier CloudWatch-based candidate was **replaced** because
`cloudwatch:GetMetricData` can incur charges, conflicting with the zero-incremental-spend lab
boundary (T02). **IAM and IAM Identity Center are offered at no additional charge; actual
assumption or use of these permissions remains separately authorized.**

`access/identity-center/permission-sets/read-only.yml`

```yaml
key: read-only
description: Read-only access via the AWS-managed ReadOnlyAccess policy.
session_duration: PT8H
managed_policies:
  - arn:aws:iam::aws:policy/ReadOnlyAccess
```

`access/identity-center/permission-sets/identity-inventory-reader.yml`

```yaml
key: identity-inventory-reader
description: Narrow read access to basic IAM account and identity inventory.
session_duration: PT1H
inline_policy:
  Version: "2012-10-17"
  Statement:
    - Sid: ReadIdentityInventory
      Effect: Allow
      Action:
        - iam:GetAccountSummary
        - iam:ListAccountAliases
      Resource: "*"
```

These instantiate T03 d4 (form 1: AWS-managed attachment; form 2: narrowly scoped embedded
inline document; no `PowerUserAccess`, no administrator-class breadth — T07). The embedded
document is rendered to JSON at plan time (`jsonencode`, F6). They become T14 valid-specimen
inputs; the T10 assignment specimens reference `read-only`; T19 rehearsal seeds mirror these
two forms. Classification: inherited (T03 d4 instantiated; T07 respected).

### Decision 6 — The standing-admin-capability hazard detector (amended)

T21 defines the detection rule T07 assigned. It is a **deterministic, conservative
standing-admin-capability hazard detector — not a complete calculation of effective AWS
permissions.** A permission-set definition is rejected (validation error; negative specimens
only under the T14 fixture path, never `access/`) when any of the following holds:

1. `managed_policies` contains the exact AWS-managed `AdministratorAccess` ARN
   (`arn:aws:iam::aws:policy/AdministratorAccess`).
2. After normalizing scalar/list forms of `Action`, `NotAction`, `Resource`, and
   `NotResource`, and expanding action wildcards against a **versioned, pinned action
   catalog**, the inline document contains an unconditional `Allow` of all actions over all
   resources.
3. A broad `Allow` statement uses `NotAction` or `NotResource` — **fail closed** (inversion
   breadth is not computed).
4. The inline document grants unbounded IAM, SSO/SSO Admin, or Identity Store **mutation
   capability**, detected against an **explicit versioned action set** for those services —
   never a phrase-level heuristic.
5. Any unknown or unsupported broad pattern — **fail closed**.

The detector never subtracts `Deny` statements and never relies on permission boundaries,
SCPs, RCPs, resource policies, or session policies to excuse a broad grant. The initial
counterexample specimen exercises rule 1, and the rule text records — per T07's requirement —
that the AdministratorAccess specimen is **only one counterexample, not the entire rule**.
Classification: compatible (implements the carried T07 domain decision; X75 evidence).

### Decision 7 — Profile rejection codes for out-of-slice policy forms

A distinct profile-code family `P-OOS-*` (profile, out-of-slice), separate from domain `E-*`
codes (the T10 d2 two-family separation): `P-OOS-CMP` (customer-managed policy reference),
`P-OOS-BOUNDARY` (permissions boundary), and `P-OOS-USER` (relabeling T10's USER profile
error into the family). Severity: error under the selected-slice profile; message wording
states "out of slice A — not prohibited by the domain architecture." The capabilities exist
at the pin (F3), so these codes are pure policy. Rejected: reusing the exploratory warning
`W-REF-CMP` (a warning cannot enforce the profile — T18 §2.4). Classification: compatible.

### Decision 8 — CV-07 verification record: split disposition (corrected)

- **Provider capability at Terraform `1.15.7` / `hashicorp/aws 6.53.0`: documentary PASS at
  the exact pins** — per-capability table F3–F7 citing the provider documentation at the
  immutable `v6.53.0` tag, covering the permission-set core, AWS-managed attachment,
  inline-policy resource, account assignment, import identities, permission-set-only tag
  support, and the existence of the excluded resource types.
- **Terraform-core plan-action classes: empirical PASS** — F8, demonstrated offline at
  exactly 1.15.7, including `["forget"]` for `removed { lifecycle { destroy = false } }`.
- **Exact AWS-provider schema/validate/plan execution on the authoring host: NOT RUN /
  BLOCKED** by the recorded loopback TLS interception (F10). **Lab-CI execution remains
  unverified.**
- **Import-ID rendering, sensitivity, and redaction: OPEN — mandatory verification before any
  T19 import rehearsal**, explicitly accounting for `change.importing.id` in Terraform plan
  JSON (F9): where that identifier surfaces (plan JSON, human-readable plan output, logs) and
  how it is redacted from public artifacts.
- **Overall disposition:** sufficient documentary capability evidence **for the S2
  proposal**, but **not S6 execution-readiness evidence and not satisfaction of T19's
  import/redaction gate**.
- **No provider upgrade or dated capability exception is triggered** — no pinned-provider
  capability failure has been demonstrated (the T15 d13 rule remains dormant).

Classification: inherited (CV-07 applied as written; #20 disposition rule respected).

### Decision 9 — Behavior-equivalence demonstration for key replacement (clarified)

Equivalence for a permission-set key replacement (T05 C1(4), T06 C2(2)) is field-level
identity of the governed definition: identical `managed_policies` set; semantically identical
inline document under **canonical JSON comparison that preserves array semantics and
normalizes only JSON object-member ordering and insignificant serialization whitespace**;
identical `session_duration` and `relay_state`. **`description` may differ — it is
informational and mutable in place** (T06 C2(3)). Demonstrated by (i) a validator equivalence
report over the two YAML definitions and (ii) an introduce plan whose **creates apply only to
the declared replacement permission set and its parallel assignments — the plan must contain
no update, no delete, and no unrelated create.** Deployed Name and tags are expected to
differ; ARNs are outputs and never compared. Rejected: live-behavior probing (an AWS
operation the map cannot authorize). Classification: compatible.

## Dependency effects and frontier

#20 has native edges blocked-by 0, blocking 2 (#22, #19). Closing #20 reduces T20 #22 to
**one** open blocker (#21) and T14 #19 to **two** (#21, #22); neither becomes unblocked. Live
frontier after closure, in map order: **T22 #21 (next claimable)** · T23 #23. **T14 #19
remains scheduled after T22 #21, T23 #23, and T20 #22 under the current map order.** One HITL
ticket per session — nothing is claimed at publication.

## Publication sequence (fail-closed; record before close)

Executed only under Eric's consolidated publication approval. A failure at any step through 8
leaves #20 open, with all later normal publication steps unperformed; completed remote writes
are not automatically undone. The exact partial state is preserved through a Repository
Continuity Artifact where necessary and reported.

1. Create this record at
   `docs/wayfinding/map-1/20-permission-set-policy-representation-for-slice-a-aws-managed-attachment-and-embedded-inline-policy.md`
   and the `docs/wayfinding/README.md` index line in the working tree.
2. Validate them: frontmatter parses, internal links resolve, and the mechanical checks pass
   on the final bytes; no live identifier, no acceptance claim, and none of the superseded
   specimen, unqualified-verdict, or lab-CI-status wording remains.
3. Commit both on `main`; push (authorized as part of the consolidated approval).
4. Verify the immutable record URL at the pushed commit resolves and is byte-equivalent to
   the local file.
5. Post the exact #20 resolution comment, with the record commit SHA filled in.
6. Post the exact informational handoff comments to T14 #19, T20 #22, and T23 #23; no
   dependency edges.
7. Update map #1: append exactly one T21 Decisions-so-far line. No fog edit and no map-order
   change (T21 graduates nothing and creates no ticket).
8. Round-trip verify: the #20 resolution comment, all three handoff comments, and the
   complete map #1 diff (exactly the one addition).
9. If any step through 8 fails: leave #20 open, perform no later normal publication step,
   preserve the exact partial state through continuity if necessary, and report it.
10. Close #20 as completed, retaining assignee `a24577t`, with the close comment.
11. Round-trip verify the close; verify T20 #22 now shows one open blocker and T14 #19 two.
12. Recompute all dependency effects and the live frontier (expected state above) without
    claiming anything.
13. Replace the Repository Continuity Artifact (position after T21; frontier at T22 #21; the
    OPEN import/redaction verification and the split CV-07 disposition carried forward);
    commit and push.
14. Verify `HEAD == origin/main`, a clean working tree, and the final tracker invariants
    (#20 closed with assignee retained; map body as verified; no other issue state changed).

Post-close failure rule: if a failure occurs after step 10, do not reopen #20 and do not
duplicate earlier writes; record the precise partial state in continuity where possible,
report it, and stop.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Verdict⟧ and ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub mutation,
any use of the specimen permissions, or any implementation.
