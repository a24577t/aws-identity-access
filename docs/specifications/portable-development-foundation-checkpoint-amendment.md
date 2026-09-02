# Portable-development foundation checkpoint amendment

Narrow accepted-specification amendment, ratified at a Pre-Baseline
⟦G-Accept⟧, to the accepted
[slice-A engineering specification](slice-a-engineering-specification.md) as
already amended by the
[execution-grouping amendment](slice-a-execution-grouping-amendment.md). It
carries no authority header (T23 #23 decision 4 scopes the normative-header
rule to `docs/architecture/` and `docs/guides/`); its authority derives from
its approving ⟦G-Accept⟧ record and this repository placement. On any
divergence between this amendment and the accepted records it cites, the
cited record prevails — except for the two things this amendment supersedes:
the **current-repository execution destination** of grouped tickets R6–R8
(§10 items 14a, 14b, 15) and the **milestone boundary** of this repository's
development. No other invariant, contract, behavior, pin, authorization
boundary, or open architecture question is changed or resolved here.

## 1. What changes, and what does not

**Changes (execution destination and milestone scope only):**

- R1–R5 constitute this repository's completed **portable source-code
  foundation checkpoint**; the repository's development milestone ends at
  that checkpoint rather than at R8.
- This personal repository will **not execute R6, R7, or R8**:
  - R6 (repository-side control activation, item 14a) moves to the
    destination company repository;
  - R7 (AWS-side OIDC/bootstrap, item 14b) moves to the destination company
    AWS/GitHub environment;
  - R8 (environment validation/remediation, item 15) moves to that same
    destination environment.
- After this amendment merges, tickets #31–#33 are dispositioned as
  **transferred/deferred — never as completed** (§6).

**Unchanged (binding by citation, never restated):**

- all accepted R1–R5 architecture and implementation — every merged product
  of PRs #35, #37, #38, #39, and #40 remains exactly as reviewed and merged;
- the R6–R8 contracts themselves — the item 14a/14b/15 contract columns,
  deciding records, separate-authorization rules, and the rule that **no
  Terraform apply may occur before the item-14a control set is active** —
  preserved intact **for destination-environment use** (§3);
- condition C1 from the R5 S11 verdict, preserved for the destination
  R7-equivalent work (§4);
- IR-R5-2 and IR-R4-1…4, which remain non-blocking recommendations only (§4);
- the three open empirical conditions (specification §8.3): provider
  execution, `forget` representation, and import redaction — open,
  unadvanced, and never claimed closed (§4);
- every security, validation, evidence, and fail-closed contract of the
  accepted records.

## 2. The portable foundation checkpoint (R1–R5)

The checkpoint comprises the merged products of grouped tickets R1 #26,
R2 #27, R3 #28, R4 #29, and R5 #30 (§10 rows 1–13): repository structure and
contracts, the validation and catalog system, plan analysis and generated
governance, the CI workflows, and the two Terraform roots with their resource
model. Each passed the full decision-gated verify chain (S7–S11) recorded on
its ticket. The checkpoint is **source code and committed evidence only**:
this repository makes **no claim** of GitHub control activation, AWS
deployment, lab verification, production readiness, or closure of any
empirical condition.

## 3. Destination transfer of R6–R8

The R6–R8 contracts transfer as **contracts to be satisfied in the
destination company environment**, not as work deleted:

- their accepted content (deciding records, acceptance criteria,
  authorization boundaries, ordering rules) continues to govern the
  destination-environment equivalents of items 14a, 14b, and 15;
- each remains **separately authorized** in its destination, exactly as the
  execution-grouping amendment requires here;
- **external-state evidence does not transfer as fresh evidence**: every
  GitHub- or AWS-side condition the R6–R8 contracts require must be observed
  again, in the destination environment, before it may be relied upon there.

## 4. Conditions and recommendations — preserved dispositions

- **C1** (R5 S11, comment 5516268640; handoff on #32): *at the first
  authorized rehearsal, verify Terraform saved-plan `file()` re-read
  semantics; if apply re-reads the value, stage the retrieved plan context at
  the identical path before applying the reviewed saved plan.* C1 travels
  with the **destination R7-equivalent work**.
- **IR-R5-2 and IR-R4-1…4** remain non-blocking recommendations only, with
  their natural owners now read as the destination equivalents of the
  `validator.ci` touch and the control-activation pass.
- **The three empirical conditions remain open**: provider execution,
  `forget` representation, import redaction. This amendment neither advances
  nor closes any of them.

## 5. Company-transfer boundary

- Company-specific identifiers, inventory bindings, OIDC trust subjects,
  repositories, secrets, environments, roles, and controls must be
  **established and verified anew** in the destination; nothing in this
  repository pre-establishes any of them.
- **No credential, private key, live identifier, or company-confidential
  value transfers through this repository** — in either direction, at any
  time. The committed-content boundary of the accepted records continues to
  hold.
- This amendment names no company, environment, account, or system: it
  invents no company-specific fact.

## 6. Tracker disposition after merge (#31–#33)

After this amendment merges — and only then — the owner dispositions the
three remaining grouped tickets, each with a closing comment citing this
amendment:

- **R6 #31** — closed as **not planned** in this repository, recorded as
  *transferred* to the destination company repository (item 14a contract
  preserved per §3);
- **R7 #32** — closed as **not planned** in this repository, recorded as
  *transferred* to the destination company environment (item 14b contract
  and C1 preserved per §§3–4);
- **R8 #33** — closed as **not planned** in this repository, recorded as
  *transferred/deferred* to the destination environment (item 15 contract
  preserved per §3).

None of the three is ever dispositioned as *completed*. Native dependency
edges are left as history; no new edge is created.

## 7. Checkpoint version and release-gate route

The proposed repository checkpoint version is **`v0.1.0-foundation.1`**
(SemVer `0.1.0` with prerelease identifiers `foundation.1`). It is created
**only after all of the following**, in order:

1. this amendment is accepted and merged at its ⟦G-Accept⟧;
2. #31–#33 receive their §6 transferred/deferred dispositions;
3. STATUS is reconciled;
4. the applicable phase/release gate (operator-guide S4/S5 as applicable,
   then S7) passes over the checkpoint scope;
5. the annotated tag, the GitHub Release, and STATUS can be made consistent
   **atomically** (operator-guide S8).

If the gate does not pass, no version is created and the gate's findings
route through normal remediation.

## 8. First destination product objective — the IAM PR MVP

The first product objective of the destination company repository — stated
here as destination scope, **not** as implementation in this repository — is
the **IAM PR MVP**:

- one IAM role with a complete trust policy;
- one exceptional IAM user;
- one IAM group with group-owned membership;
- a mandatory permission boundary;
- credential, console/MFA, owner, justification, and expiry controls;
- schema, validation, effective-access plan, Terraform, and CI integration
  built on the transferred foundation.

Fleet roles and StackSets remain **deferred beyond that MVP**.

## 9. What this amendment does not do

This amendment does **not** itself create a repository version, an
architecture baseline, a tag, a GitHub Release, a company repository, or any
external configuration; it performs no GitHub-configuration change, no AWS
contact, and no Terraform execution. It changes no committed R1–R5 byte. It
edits no accepted specification, ADR, or prior amendment in place — it is a
new, append-only record whose effect begins at its approving ⟦G-Accept⟧.
