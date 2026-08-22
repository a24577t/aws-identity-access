# T01 research — aws_ami governing revision and intake-brief provenance

> **Location note.** This repository has no research-notes convention yet (`docs/` holds only
> `docs/agents/`). This file is placed at `docs/research/<topic>.md` as a proposed convention for
> Wayfinder `research` tickets. If a different location is adopted later, move this file; its
> contents do not depend on the path.

- Ticket: [#2 — T01](https://github.com/a24577t/aws-identity-access/issues/2)
  (part of map [#1](https://github.com/a24577t/aws-identity-access/issues/1))
- Recorded: 2026-08-22
- Method: facts were read from the local clone `aws_ami` (`C:\Users\Eric\Documents\GitHub\aws_ami`,
  read-only) and cross-checked against the GitHub API (`gh api repos/a24577t/aws_ami/...`). No
  file in `aws_ami` was modified. Every claim below names its source in §7.

---

## 1. Summary of facts

| Fact | Value | Source |
|------|-------|--------|
| aws_ami `main` HEAD | `5f3cb7163f468730fd2ceb5d565c90b0bfda6099` | S1, S2 |
| Commit date | 2026-08-22T07:49:46-04:00 (11:49:46Z) | S1, S2 |
| Commit subject / body | `aws-identity-access` / `Inline trust policies in identity access roles` | S1, S2 |
| Local HEAD == local `origin/main` == GitHub `main` | **yes** (all three `5f3cb716…`) | S1, S2 |
| Tags in aws_ami | **none** — local `git tag` empty; GitHub tags endpoint returns `[]` | S1, S3 |
| Repository visibility / default branch | public / `main` | S4 |
| Uncommitted or untracked files in local aws_ami | exactly one entry: `?? docs/bootstrap/` (the directory containing the brief). No modified tracked files. | S1 |
| Intake brief tracked in aws_ami at HEAD? | **no** — `git ls-tree HEAD docs/bootstrap/` is empty; GitHub contents API for `docs/bootstrap` on `main` returns 404 | S5, S6 |
| Brief sha256 (aws_ami working copy) | `f87fa000a2a39897b5be20a650ce400584c339fdd99606dee928a4e266ad4068` (16,204 bytes) | S7 |
| Brief sha256 (this repository's `aws-identity-access-poc-prompt.md`) | `f87fa000a2a39897b5be20a650ce400584c339fdd99606dee928a4e266ad4068` | S7 |
| Byte-identical? | **yes** (`diff -q` reports no difference) | S7 |
| Brief tracked in this repository? | yes — first tracked at commit `7a7d3edec2ba57f2e5ab1a81c9f3ab861c27f7da` (2026-08-22, "governance"), blob `91c92d2db4314bfa6eaaab1bfedd9af615199a01` | S8 |
| Is that commit on GitHub? | **no** — this repository's `origin/main` is `1c86d1174134c76147126088ac9bb6d83c44f445` (Initial commit); GitHub contents API for the brief on `main` returns 404 | S8, S9 |
| Immutable URL for the brief | **none exists anywhere today** (untracked in aws_ami; tracked but unpushed here) | S5, S6, S8, S9 |
| `decided` date of every cited aws_ami document | `2026-08-17` (all 13 architecture documents + README) | S10 |

### Governed documents at the pinned revision

All immutable URLs are of the form
`https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/<path>`.

| Path | `status` | `destination` | `decided` | Immutable URL |
|------|----------|---------------|-----------|---------------|
| `CONTEXT.md` | — (no frontmatter; file opens with `# AWS Governance Platform`) | — | — | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/CONTEXT.md |
| `docs/architecture/README.md` | normative | all | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/README.md |
| `docs/architecture/00-governing-principles.md` | normative | all | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/00-governing-principles.md |
| `docs/architecture/01-repository-boundaries.md` | normative | all | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/01-repository-boundaries.md |
| `docs/architecture/02-configuration-model.md` | normative | all | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/02-configuration-model.md |
| `docs/architecture/03-region-model.md` | normative | all | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/03-region-model.md |
| `docs/architecture/04-enforcement-plane-precedence.md` | normative | aws-organization-governance | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/04-enforcement-plane-precedence.md |
| `docs/architecture/05-runtime-mutation-contracts.md` | normative | all | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/05-runtime-mutation-contracts.md |
| `docs/architecture/06-account-lifecycle.md` | normative | aws-organization-governance | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/06-account-lifecycle.md |
| `docs/architecture/07-identity-center-platform.md` | normative | aws-identity-access | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/07-identity-center-platform.md |
| `docs/architecture/08-management-account.md` | normative | aws-organization-governance | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/08-management-account.md |
| `docs/architecture/09-tier0-execution.md` | normative | all | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/09-tier0-execution.md |
| `docs/architecture/10-codeowners-model.md` | normative | all | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/10-codeowners-model.md |
| `docs/architecture/11-decision-register.md` | register | all | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/11-decision-register.md |
| `docs/architecture/12-capability-validation.md` | checklist | aws-organization-governance | 2026-08-17 | https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/12-capability-validation.md |

Meaning of the `status` values, per aws_ami `docs/architecture/README.md` ("Document status
values"): `normative` — binding architectural rules; `register` — decision tracking; open items gate
the implementation steps they name; `checklist` — validation work that must complete before the
decisions it feeds are frozen. `destination` is the platform repository a document migrates to
when the platform repositories are created; "Documents marked `destination: all` define
platform-wide rules and are extracted to a shared location chosen at migration time" (S11).

---

## 2. Pin — which revision governs, and how it is named

**The revision is `5f3cb7163f468730fd2ceb5d565c90b0bfda6099`** (aws_ami `main`, 2026-08-22). It
is the only candidate: it is HEAD locally, on `origin/main`, and on GitHub, it is untagged, and the
intake brief was written against it (the brief is the one untracked file sitting on top of it).

### Option A — commit pin (available now, no owner action)

- Record the 40-character SHA in this repository and cite documents via the `blob/<sha>/<path>`
  URL form above.
- Immutable by construction: the SHA is content-addressed; nobody can move it. Verifiable at any
  time with `gh api repos/a24577t/aws_ami/commits/5f3cb7163f468730fd2ceb5d565c90b0bfda6099`.
- Trade-off: not human-memorable; a reader cannot tell from the SHA *why* this revision was
  chosen, so the provenance record (§4) must carry that context.

### Option B — owner-created tag in aws_ami (requires an action in aws_ami by its owner)

- Example: an annotated tag such as `aws-identity-access-poc-intake` on `5f3cb716…`.
- Human-readable; a natural anchor for later "what changed since intake" diffs
  (`git diff <tag>..main`).
- Trade-offs: (1) tags are **mutable references** unless tag protection is configured, so a tag
  alone is weaker than a SHA; (2) creating it is out of scope for this repository (this ticket may
  not mutate aws_ami); (3) it adds nothing to immutability that the SHA does not already give.

### Recommendation (the choice is the repository owner's, not this note's)

Adopt **Option A now** as the record of truth — it is available immediately and is the strongest
form of the pin. If the owner also wants a readable alias, create the tag as a **supplement** that
points at the same SHA and record both (tag name *and* SHA) so that the SHA remains authoritative
if the tag ever moves. Do not adopt a tag *instead of* the SHA.

---

## 3. Intake-brief provenance

### Status at the pinned revision

- `docs/bootstrap/aws-identity-access-poc-prompt.md` is **not tracked** in aws_ami at
  `5f3cb716…` — it is the sole untracked entry in the local clone's `git status`, and it does not
  exist on GitHub (S5, S6). Therefore **no immutable aws_ami URL exists for the brief**; any
  `blob/5f3cb716…/docs/bootstrap/...` URL would 404.
- Digest (sha256): `f87fa000a2a39897b5be20a650ce400584c339fdd99606dee928a4e266ad4068`, 16,204
  bytes (S7).
- The aws_ami working copy and this repository's `aws-identity-access-poc-prompt.md` are
  **byte-identical** (same digest; `diff -q` silent) (S7).
- In this repository the brief has been tracked since local commit `7a7d3ed` (2026-08-22,
  "governance"), blob `91c92d2d…`, but that commit is **not yet pushed** — `origin/main` is still
  the initial commit `1c86d11` and GitHub returns 404 for the file (S8, S9). So this repository
  has a *committed* copy but not yet an *immutable URL* either; pushing `main` would create one.

### Option 1 — commit the brief in aws_ami `docs/bootstrap/` (owner action in aws_ami)

- Pros: the brief was authored in the design workspace and would live next to the architecture
  it cites; it would gain an immutable aws_ami URL.
- Cons: it requires an aws_ami commit *after* `5f3cb716…`, which means **either** the governing
  pin moves forward to a commit whose only change is the brief, **or** the record carries two
  aws_ami SHAs (one for the architecture, one for the brief). It also places a document whose
  subject is exclusively `aws-identity-access` into a workspace whose README says its documents
  migrate to their `destination` repository (S11) — it would migrate here anyway.

### Option 2 — this repository's copy is the intake of record

- Pros: the copy is already tracked here (S8); the brief's subject is this repository; no aws_ami
  action is needed; the pin stays at `5f3cb716…` unchanged; the digest recorded in §4 ties this
  copy to the aws_ami working copy that produced it. The copy becomes immutable (URL
  `https://github.com/a24577t/aws-identity-access/blob/<commit>/aws-identity-access-poc-prompt.md`)
  as soon as `main` is pushed.
- Cons: the untracked aws_ami working copy remains a drift risk — a future edit there would not
  be noticed unless the digest is re-checked. Mitigation: the owner deletes it from the aws_ami
  working tree, or commits it (Option 1 as a *secondary* reference) and the record notes that
  commit.

### Recommendation (owner decision required)

**Option 2** — treat this repository's tracked copy as the intake of record, record its digest and
the fact that the aws_ami copy was untracked at intake, and push `main` so the copy has an
immutable URL. Option 1 remains available to the aws_ami owner as a secondary reference; if taken,
record that aws_ami commit in the provenance record *in addition to* the `5f3cb716…` architecture
pin, not in place of it.

---

## 4. Proposed provenance record for this repository

A small, machine-checkable file (proposed path `docs/governance/aws-ami-provenance.yml`; the path is
a proposal, not a convention). Every field below is a fact established in §1; nothing is
aspirational. Values are shown filled in for the current state.

```yaml
# Provenance of the governing aws_ami revision and of the intake brief for this POC.
aws_ami:
  repository: https://github.com/a24577t/aws_ami
  commit: 5f3cb7163f468730fd2ceb5d565c90b0bfda6099
  commit_date: 2026-08-22T11:49:46Z
  tag: null            # owner decision (a); fill in if an owner-created tag is adopted as alias
  url_form: https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/<path>
  documents:           # every document this repository cites; `decided` from frontmatter
    - { path: CONTEXT.md,                                          status: null,      destination: null,                        decided: null }
    - { path: docs/architecture/README.md,                         status: normative, destination: all,                         decided: 2026-08-17 }
    - { path: docs/architecture/00-governing-principles.md,        status: normative, destination: all,                         decided: 2026-08-17 }
    - { path: docs/architecture/01-repository-boundaries.md,       status: normative, destination: all,                         decided: 2026-08-17 }
    - { path: docs/architecture/02-configuration-model.md,         status: normative, destination: all,                         decided: 2026-08-17 }
    - { path: docs/architecture/03-region-model.md,                status: normative, destination: all,                         decided: 2026-08-17 }
    - { path: docs/architecture/04-enforcement-plane-precedence.md, status: normative, destination: aws-organization-governance, decided: 2026-08-17 }
    - { path: docs/architecture/05-runtime-mutation-contracts.md,  status: normative, destination: all,                         decided: 2026-08-17 }
    - { path: docs/architecture/06-account-lifecycle.md,           status: normative, destination: aws-organization-governance, decided: 2026-08-17 }
    - { path: docs/architecture/07-identity-center-platform.md,    status: normative, destination: aws-identity-access,         decided: 2026-08-17 }
    - { path: docs/architecture/08-management-account.md,          status: normative, destination: aws-organization-governance, decided: 2026-08-17 }
    - { path: docs/architecture/09-tier0-execution.md,             status: normative, destination: all,                         decided: 2026-08-17 }
    - { path: docs/architecture/10-codeowners-model.md,            status: normative, destination: all,                         decided: 2026-08-17 }
    - { path: docs/architecture/11-decision-register.md,           status: register,  destination: all,                         decided: 2026-08-17 }
    - { path: docs/architecture/12-capability-validation.md,       status: checklist, destination: aws-organization-governance, decided: 2026-08-17 }
intake_brief:
  path_here: aws-identity-access-poc-prompt.md
  sha256: f87fa000a2a39897b5be20a650ce400584c339fdd99606dee928a4e266ad4068
  bytes: 16204
  governed_copy: null  # owner decision (b): "this-repository" | "aws_ami:docs/bootstrap/<commit>"
  aws_ami_status_at_intake: untracked   # docs/bootstrap/ was untracked at 5f3cb716...
  identical_to_aws_ami_working_copy: true
recorded: 2026-08-22
recorded_by_ticket: "#2 (T01)"
```

Re-verification procedure (any time): compare `gh api repos/a24577t/aws_ami/commits/main --jq .sha`
with `aws_ami.commit` to know whether the platform has moved on; `sha256sum
aws-identity-access-poc-prompt.md` against `intake_brief.sha256` to know whether the brief has
changed.

---

## 5. Verbatim identifier texts at `5f3cb7163f468730fd2ceb5d565c90b0bfda6099`

Quoted exactly as they appear (Markdown link syntax retained). Each entry names the file and the
nearest heading. Line numbers refer to the file at the pinned revision.

### 5.1 `docs/architecture/00-governing-principles.md` — under `# Governing Principles`

Preamble (lines 9–10): "These invariants bind every repository, document, and implementation
decision in the platform. A change that violates an invariant is an architecture change and MUST
be made here first."

**`## I-1 — Identity chain`** (line 12)

> ```text
> Human-readable path
>         │
>         ▼
> governed configuration
>         │
>         ▼
> authoritative AWS key
> ```
>
> Paths locate things for people. Configuration holds the authoritative AWS identifiers. Automation
> MUST use the authoritative key from configuration and MUST NOT derive AWS identity from a
> directory name. See [02-configuration-model.md](./02-configuration-model.md).

**`## I-2 — Enforcement-plane principle`** (line 28)

> > Use the highest-authority AWS-native enforcement mechanism that correctly expresses the security
> > requirement; use Terraform to govern desired state around it; use CloudFormation only
> > where distributed resource creation is required; use APIs for explicitly authorized runtime
> > actions.
>
> The per-requirement selection procedure is defined in
> [04-enforcement-plane-precedence.md](./04-enforcement-plane-precedence.md).

**`## I-3 — Plane assignment`** (line 38)

> ```text
> desired state         → Terraform
> organization fan-out  → Terraform-owned StackSets
> temporary action      → AWS API
> ```
>
> CloudFormation is a distribution mechanism controlled by Terraform, never a second source of
> governance authority.

**`## I-4 — Organization inventory flows downstream`** (line 49)

> ```text
> organization inventory
>         │
>         ├── accounts
>         ├── OUs
>         └── enabled Regions
>               │
>               ▼
>       downstream repositories
> ```
>
> `aws-organization-governance` owns the authoritative inventory of accounts, OUs, and enabled
> Regions. Downstream repositories consume it and MUST NOT maintain independent authoritative copies.

**`## I-5 — Resource authority ≥ runtime authority`** (line 65)

> ```text
> resource-owning repository
>         │
>         └── defines allowed runtime-mutation contract
>                     │
>                     ▼
>             aws-privileged-access
>                     │
>                     └── executes approved runtime operation
> ```
>
> A lower-authority execution repository MUST NOT grant itself authority over higher-level state.
> See [05-runtime-mutation-contracts.md](./05-runtime-mutation-contracts.md).

**`## I-6 — Reconciliation invariant`** (line 81)

> > No reconciliation plane may overwrite an active authorized runtime mutation until
> > its owning security workflow releases or reconciles that mutation.
>
> This applies to Terraform, CloudFormation/StackSets, service-native organization policy
> mechanisms, and any future reconciliation engine. Divergence may also be deliberately
> unsupported: higher-authority enforcement planes may intentionally prohibit runtime divergence,
> and contracts MUST support `incident_divergence.supported = false` —
> [05-runtime-mutation-contracts.md](./05-runtime-mutation-contracts.md#incident-divergence-may-be-unsupported-by-design).

**`## I-7 — Authority ordering`** (line 92)

> ```text
> organization governance  >  identity/access  >  privileged access
> ```
>
> Higher authority carries stricter change control, not looser. The domain repositories
> (`aws-security-services`, `aws-ami-security`) operate under organization enforcement authority
> via the domain-contract pattern ([I-9](#i-9--domain-content-vs-organization-enforcement)); the
> rank of `aws-security-services` within this ordering is open
> ([OD-20](./11-decision-register.md#od-20)). The management account, which sits outside the
> platform's own technical guardrails, carries the strictest human controls of all
> ([08-management-account.md](./08-management-account.md)).

**`## I-8 — Boundaries follow authority and lifecycle`** (line 106)

> Repositories are bounded by who has authority over a change and what lifecycle the change follows —
> never by AWS object type. A change involving a role, a policy, and an assignment that share one
> authority boundary MUST be expressible as one atomic pull request.

### 5.2 `docs/architecture/11-decision-register.md`

Document preamble (lines 9–12, under `# Decision Register`): "Open owner decisions, with a
**blocking** flag for those that must resolve before the affected repository's internal layout (or
a boundary rule) can freeze. The repository **family** itself is frozen at five
([01-repository-boundaries.md](./01-repository-boundaries.md)). Resolved decisions are retained
with their dispositions; IDs are stable and never reused."

Summary-table rows (under `## Summary`, `| ID | Decision | Blocking | Status |`):

> | [OD-05](#od-05) | Elevation materialization / JIT mechanism | no | open |
> | [OD-08](#od-08) | Identity Center manual/bootstrap ownership | no | open |
> | [OD-10](#od-10) | Enterprise/shared IAM promotion threshold | no | open |
> | [OD-11](#od-11) | IAM-user exception expiry and recertification | no | open |
> | [OD-21](#od-21) | Inventory-contract consumption model | no | open |
> | [RD-03](#rd-03) | Identity Center organization-instance multi-Region | — | **resolved** |
> | [RD-04](#rd-04) | Platform configuration format and extension | — | **resolved** |
> | [RD-05](#rd-05) | Identity Center assignment principals | — | **resolved** |
> | [RD-06](#rd-06) | Downstream account references | — | **resolved** |
> | [RD-07](#rd-07) | Delegation vs. elevation | — | **resolved** |
> | [RD-08](#rd-08) | Deferred references to requested accounts | — | **resolved** |
> | [RD-09](#rd-09) | Decision register as sole decision authority | — | **resolved** |

**`### OD-05`** (line 68, under `## Open decisions`)

> **Elevation materialization / JIT mechanism.** Deliberately open — do not prematurely select
> between temporary Identity Center assignments, pre-provisioned elevated roles with brokered
> approval, third-party JIT/PAM, or another controlled mechanism. Evaluate candidates against:
>
> ```text
> native TTL
> revocation guarantee
> dependency availability
> Identity Center integration
> Okta/enterprise IdP integration
> ServiceNow/change integration
> credential exposure
> CloudTrail evidence
> emergency independence
> operational complexity
> ```
>
> **No longer layout-blocking**: `aws-privileged-access` is provider-neutral
> ([01-repository-boundaries.md](./01-repository-boundaries.md#aws-privileged-access)); the chosen
> mechanism plugs into `providers/`. Note: if materialization is Identity Center assignments, expiry
> has no native TTL — revocation is only as reliable as the automation enforcing it.

**`### OD-08`** (line 103, under `## Open decisions`)

> **Identity Center manual/bootstrap ownership.** Who performs console-only configuration, where
> evidence lives, revalidation cadence
> ([07-identity-center-platform.md](./07-identity-center-platform.md)).

**`### OD-10`** (line 113, under `## Open decisions`)

> **Enterprise/shared IAM promotion threshold.** The codified trigger that moves a workload role
> into `aws-identity-access` (prior working proposal: assumed by principals from two or more other
> teams' workloads, or referenced in another repository's trust policy). Includes disposition of the
> AMI pipeline's build/distribution roles (lean: AMI-repo-local — lifecycle follows the AMI
> pipeline).

**`### OD-11`** (line 120, under `## Open decisions`)

> **IAM-user exception expiry and recertification.** Default expiry, recertification cadence, and
> the owning reviewer for the exceptions register in `aws-identity-access`.

**`### OD-21`** (line 143, under `## Open decisions`)

> **Inventory-contract consumption model.** Whether downstream repositories consume the
> account/OU/`enabled_regions` inventory as **tracking** (always-current) or **pinned** versions
> (with an auto-bump mechanism). [I-9](./00-governing-principles.md#i-9--domain-content-vs-organization-enforcement)
> pins domain→enforcement contracts; the inventory is a different contract class and its model must
> be specified explicitly, or new-account propagation and reproducibility rules are undefined.

**`### RD-03`** (line 234, under `## Resolved decisions`)

> **Identity Center organization-instance multi-Region — resolved.** Replication of the
> organization instance to additional Regions is supported subject to AWS prerequisites.
> Represented as platform configuration, never an account/Region hierarchy
> ([03-region-model.md](./03-region-model.md), [07-identity-center-platform.md](./07-identity-center-platform.md)).

**`### RD-04`** (line 240, under `## Resolved decisions`)

> **Platform configuration format and extension — resolved.** Configuration files are YAML with the
> `.yml` extension, platform-wide, across all five repositories. This amends the runtime-mutation
> contract convention's extension ([OD-16](#od-16)) from `.yaml` to `.yml`. JSON Schemas in each
> repository's `schemas/` directory validate configuration in CI; one resource per file
> ([02-configuration-model.md](./02-configuration-model.md#format)).

**`### RD-05`** (line 247, under `## Resolved decisions`)

> **Identity Center assignment principals — resolved.** Standing assignments use **group principals
> only**. A user principal is exceptional and carries the same governance class as an IAM user:
> justification, review/expiry date, and security approval, enforced by schema validation.

**`### RD-06`** (line 252, under `## Resolved decisions`)

> **Downstream account references — resolved.** Downstream repositories reference accounts (and OUs
> and Regions) **by name only**; generated IDs are resolved from the organization inventory at
> execution time. The name→ID binding lives in exactly one place — the org repository's
> `account.yml`, maintained by the [RD-01](#rd-01) write-back flow. Account names are immutable once
> active; a rename is a governed cross-repository change ([OD-12](#od-12)). CI validation fails any
> reference to a name absent from the inventory; references to `status: requested` entries are
> governed by [RD-08](#rd-08). Version pinning of the consumed inventory remains open under
> [OD-21](#od-21).

**`### RD-07`** (line 262, under `## Resolved decisions`)

> **Delegation vs. elevation — resolved.** They are distinct concepts, both retained and documented
> separately; neither is deprecated. **Delegation** transfers an existing authority from one
> principal to another. **Elevation** grants a principal additional authority beyond its durable
> access. Either may be temporary, but they require different policy and approval semantics.
> Recorded in [CONTEXT.md](../../CONTEXT.md),
> [01-repository-boundaries.md](./01-repository-boundaries.md#aws-privileged-access), and
> [05-runtime-mutation-contracts.md](./05-runtime-mutation-contracts.md#temporary-privilege--the-durableruntime-split).

**`### RD-08`** (line 271, under `## Resolved decisions`)

> **Deferred references to requested accounts — resolved.** A downstream reference to a
> `status: requested` account is **valid but deployment-deferred**. [RD-06](#rd-06) fails only names
> **absent** from the organization inventory; a requested account is present in the inventory but
> has no resolvable deployment target yet. Schema/CI: pass, optionally warn. Plan/deployment: omit
> or explicitly defer account-targeted resources. Activation: the merged `account_id` write-back
> makes deployment eligible. A consumer that requires immediate resolution MUST report
> **"deferred"**, never **"invalid"**. Binding on every downstream consumer
> ([06-account-lifecycle.md](./06-account-lifecycle.md#deferred-references-resolved)).

**`### RD-09`** (line 281, under `## Resolved decisions`; last entry in the file)

> **Decision register as sole decision authority — resolved.** This register is the sole
> architecture-decision authority. Parallel ADR files are not created — they would duplicate
> identifiers, status, rationale, and disposition. If repository creation later warrants ADR-shaped
> files, they are migrated or generated from this register, never maintained alongside it.

#### RD-09 scope — every sentence at the pinned revision that bears on *whom it binds* (for T08)

The RD-09 entry itself contains **no sentence that names domain repositories or restricts the rule
to aws_ami**. Its scope has to be read from these surrounding statements, all at `5f3cb716…`:

1. RD-09 body, sentence 2: "This register is the sole **architecture-decision** authority."
   (The word "architecture" is the qualifier — it does not say "sole decision authority" of any
   kind.)
2. RD-09 body, sentence 4: "If **repository creation** later warrants ADR-shaped files, they are
   migrated or generated from this register, never maintained alongside it." (Contemplates the
   platform repositories holding ADR-shaped files, derived from the register.)
3. `11-decision-register.md` frontmatter: `destination: all`; README: "Documents marked
   `destination: all` define platform-wide rules" (S11).
4. `docs/architecture/README.md`, "Document status values" paragraph (lines 44–47): "The decision
   register is the **sole architecture-decision authority** (RD-09). Parallel ADR files are never
   maintained; if ADR-shaped files are ever needed, they are generated or migrated from the
   register. The platform's ubiquitous language lives in the root [CONTEXT.md](../../CONTEXT.md)."
5. `00-governing-principles.md` lines 9–10: "A change that violates an invariant is an
   architecture change and MUST be made here first." (Defines what an *architecture* change is
   relative to the invariants; does not address non-architecture domain decisions.)
6. README staging-workspace notice (lines 12–18): aws_ami "is a design workspace, not one of the
   five platform repositories"; documents migrate to their `destination`.

Reading: RD-09 is platform-wide (`destination: all`) for **architecture** decisions; whether a
domain repository's *non-architecture* decisions (e.g. this repository's own domain-model ADRs)
fall under it is **not stated at this revision**. That is precisely T08's question; this note does
not decide it.

### 5.3 `docs/architecture/12-capability-validation.md`

**`### CV-07`** (line 87, under `## Remaining assumptions that could reverse an enforcement-plane selection`)

> **Provider-pin support for the policy types and features used** (declarative policy types and S3
> org BPA in `aws_organizations_policy`; `aws_iam_organizations_features`; Identity Center
> resources).
> *Flip criterion:* none — lack of support changes the *authoring* mechanics, not the enforcement
> plane. An unsupported type would force interim API authoring inside the Terraform boundary, which
> the matrix must record as a temporary, dated exception.

---

## 6. Discrepancies between the map's citations and the text at the pinned revision

All 21 identifiers (I-1…I-8, RD-03…RD-09, OD-05, OD-08, OD-10, OD-11, OD-21, CV-07) **exist** at
`5f3cb716…`. Nothing cited is missing. Three wording points:

1. **RD-09 — the map's quotation is not from the RD-09 entry.** The map (T08 in the proposed map;
   the same wording is what the orchestrator relayed) cites RD-09 as "the register is the sole
   architecture-decision authority; parallel ADR files are never maintained". The phrase
   "Parallel ADR files are never maintained" is **verbatim from `docs/architecture/README.md`
   lines 44–45**, which restates RD-09. The **RD-09 entry itself** says "Parallel ADR files are
   **not created** — they would duplicate identifiers, status, rationale, and disposition. If
   repository creation later warrants ADR-shaped files, they are migrated or generated from this
   register, **never maintained alongside it**." Substance is the same; the citation should point
   at README.md for that sentence, or quote the entry's own words. The entry's added clause
   ("migrated or generated from this register") is the part T08 will care about.
2. **OD-21 — paraphrase is faithful.** The map's "inventory-contract consumption model — tracking
   vs pinned unspecified" matches the entry's title and its "**tracking** (always-current) or
   **pinned** versions … must be specified explicitly, or new-account propagation and
   reproducibility rules are undefined". No discrepancy.
3. **Minor:** the map issue #1 body (as posted on GitHub) does not contain the strings `RD-09`,
   `OD-21`, `CV-07`, or `I-1`…`I-3`/`I-5`…`I-8` at all — those identifiers appear in the *proposed*
   map file (scratchpad `wayfinder-map.proposed.md`) and in issue #2's own body. Whoever
   reconciles the map body with the proposed file should carry the identifier list over.

---

## 7. Sources

Every fact above traces to one of the following. Commands were run on 2026-08-22 from the local
clone unless an API URL is given.

- **S1** — local clone `C:\Users\Eric\Documents\GitHub\aws_ami`: `git log -1 --format='%H%n%cI%n%aI%n%s'`, `git branch --show-current`, `git rev-parse origin/main`, `git remote -v`, `git tag`, `git status --porcelain`.
- **S2** — `gh api repos/a24577t/aws_ami/commits/main` (`.sha`, `.commit.committer.date`, `.commit.message`).
- **S3** — `gh api repos/a24577t/aws_ami/tags` → `[]` (length 0).
- **S4** — `gh api repos/a24577t/aws_ami` (`.default_branch`, `.visibility`).
- **S5** — local aws_ami: `git ls-tree HEAD docs/bootstrap/` (empty output, exit 0); `git ls-files docs CONTEXT.md` (lists only `CONTEXT.md` and the 14 files under `docs/architecture/`).
- **S6** — `gh api "repos/a24577t/aws_ami/contents/docs/bootstrap?ref=main"` → HTTP 404.
- **S7** — `sha256sum` of `aws_ami/docs/bootstrap/aws-identity-access-poc-prompt.md` and of `aws-identity-access/aws-identity-access-poc-prompt.md`; `diff -q` between them; `ls -l` for byte size.
- **S8** — this repository (`aws-identity-access`): `git ls-files aws-identity-access-poc-prompt.md`; `git log --format='%H %cI %s' -- aws-identity-access-poc-prompt.md`; `git rev-parse HEAD:aws-identity-access-poc-prompt.md`; `git rev-parse origin/main` after `git fetch origin`.
- **S9** — `gh api "repos/a24577t/aws-identity-access/contents/aws-identity-access-poc-prompt.md?ref=main"` → HTTP 404; `gh api repos/a24577t/aws-identity-access/commits/main`.
- **S10** — frontmatter of each file under `aws_ami/docs/architecture/` and of `CONTEXT.md`, read with `awk` over the first `---`-delimited block (CONTEXT.md has none).
- **S11** — `aws_ami/docs/architecture/README.md` at `5f3cb716…`: staging-workspace notice (lines 12–18), "Document status values" (lines 38–47). URL: https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/README.md
- **S12** — `aws_ami/docs/architecture/00-governing-principles.md` lines 1–111 (`sed -n`). URL: https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/00-governing-principles.md
- **S13** — `aws_ami/docs/architecture/11-decision-register.md` lines 1–50, 68–90, 103–107, 113–123, 143–149, 234–285. URL: https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/11-decision-register.md
- **S14** — `aws_ami/docs/architecture/12-capability-validation.md` lines 1–18, 44–45, 87–100. URL: https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/12-capability-validation.md
- **S15** — `gh issue view 1 --repo a24577t/aws-identity-access --json body` (grep for identifier strings); `gh issue view 2 --repo a24577t/aws-identity-access --json body`; scratchpad `wayfinder-map.proposed.md` (T08 text, lines 195–213).

No AWS account IDs, credentials, or tokens appear in this document.
