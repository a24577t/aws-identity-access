---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 11
title: "T16 — Lab account topology and fixtures"
url: https://github.com/a24577t/aws-identity-access/issues/11
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-23
sources:
  inherited_inputs:
    - https://github.com/a24577t/aws-identity-access/issues/11#issuecomment-5382170519
    - https://github.com/a24577t/aws-identity-access/issues/11#issuecomment-5382919599
    - https://github.com/a24577t/aws-identity-access/issues/11#issuecomment-5383471180
    - https://github.com/a24577t/aws-identity-access/issues/11#issuecomment-5386642338
  t15_record: https://github.com/a24577t/aws-identity-access/blob/62b76c4cf3f4b0aea856ee10c63650e3a0f9a02d/docs/wayfinding/map-1/10-lab-environment-test-and-deployment-contract.md
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  discovery: read-only AWS discovery 2026-08-23 via the named lab profile (STS, Organizations, IAM Identity Center, Identity Store reads only); all identifiers withheld
---

# T16 — Lab account topology and fixtures

> Proposed discovery record — the complete durable result of T16 #11. Decisions approved by Eric
> as the human project owner and decision authority after collaborator review; executed by Claude
> in the repository-owner role under `wayfinder-repo-owner` with `grill-with-docs`, using the
> batch-question rule (operating-guide governing invariant 3). **Nothing here is accepted
> architecture: every decision is a proposal until ⟦G-Verdict⟧ and ⟦G-Accept⟧.** GitHub issue #11
> is the workflow/index surface and links to this record.

## Authorization scope of this record

Accepting T16 approves the **proposed topology decisions only**. It does **not** authorize any AWS
mutation, account sign-up, Organization creation, invitation, account creation, OU operation,
Identity Center operation, delegated-administrator registration, budget change, tagging, evidence
upload, or any other infrastructure change. Every remediation item in this record is an
**independently authorized and ordered** action requiring separate, explicit Eric authorization
at S6. There is **no automatic or inferred fallback** to the T15 decision-2 options B or C; each
would require its own explicit replacement decision by Eric.

## Sanitized discovery result (2026-08-23)

Read-only discovery used the established named lab profile (confirmed as the `mcp_gateway01`
ADR-0007 canonical profile; credentials never read), restricted to STS identity verification,
AWS Organizations reads, IAM Identity Center instance/permission-set reads, and Identity Store
reads. No identifier is recorded here.

| Element (T15 decision 2 target) | Observed | Status |
|---|---|---|
| Caller identity | an IAM user in the `mcp_gateway01` sandbox account (boolean match to its committed lab configuration) | candidate `role-host` exists |
| AWS Organization | the account is standalone — every Organizations call returned `AWSOrganizationsNotInUseException` | **absent** |
| Management account distinct from `role-host` | none | **absent** |
| Two usable active `lab-workload` member accounts | none (no Organization) | **absent** |
| Identity Center organization instance, `us-east-1` | no instance in us-east-1 or in seven other Regions scanned | **absent** |
| Default identity store | none (no instance) | **absent** |
| Delegated administrator for Identity Center | none (no Organization) | **absent** |
| Permission sets beginning `ialab-` | none exist (no instance) | vacuously clear; re-verify at the S6 gate |
| OUs | none | **absent** |
| GitHub review topology | public, owner type User, one collaborator (`a24577t`, admin), no rulesets/environments/secrets/workflows | unchanged (T06/T15 basis) |

Disposition under T15 decision 2: prerequisites absent → **stop with remediation**. No alternative
topology is inferred. T16 resolves its architectural decisions now (decision 11) and carries all
live provisioning as S6 remediation behind the staged, separately authorized gates of decision 11.

## Claim-resolution record (grill-with-docs)

| # | Claim | Authority | Result | Upstream amendment / refinement |
|---|---|---|---|---|
| 1 | Provisioning through the lab's authorized organization-management mechanism preserves the repository boundary; any lab-only exception is a separate, explicitly recorded, owner-approved decision | `01` (account/OU lifecycle is never owned by this repository), `06` (vending is a governed lifecycle workflow), I-10 | **compatible** — this repository never creates, invites, moves, tags, or closes accounts; every such action is an Eric action outside the repository; a T15 option-2B topology would be a recorded lab-only exception and is not selected | none new; T02's document-09 refinement and T15's inventory-fixture rule reaffirmed |
| 2 | The requested-account fixture is an inventory entry with no account ID and is never provisioned | `06` (deferred references), RD-08 | **inherited** — decision 8 | none |
| 3 | OU placement is a lab inventory property, never part of an assignment key | RD-06, `03`, T03 d5, T04 | **inherited** — decision 9 | none |
| 4 | A fleet-role target account exists only if T13 is in the selected slice | T03 #4 revalidation (T13 out of scope) | **void** | none |

## Decisions (approved option A, with collaborator corrections integrated)

### Decision 1 — Discovered topology versus T15 decision 2A; remediation path
Remediate **toward T15 decision 2A exactly**: a new, dedicated management account and the
Organization created from it; the sandbox account invited as a member (it becomes `role-host`,
keeping the T02 state backend and OIDC provider where they are); two new member accounts as
`lab-workload`; Identity Center enabled as an organization instance in `us-east-1` with the
default identity store; `role-host` registered as delegated administrator. Every step is an
independently authorized and ordered Eric action (decision 11, Stages 0–6).

**Financial consequence and gate (collaborator correction).** Creating or joining an AWS
Organization changes the billing boundary. Any account on the current AWS Free Plan automatically
becomes a Paid Plan account when it creates or joins an Organization, and its remaining Free Tier
credits expire. Free-tier usage allowances that remain applicable are aggregated across the
Organization rather than granted independently to each account, and the management account
becomes responsible for all member-account charges. A newly opened management account must not
be assumed eligible for promotional credits. These consequences are gated by the staged,
separately authorized remediation of decision 11: the informed signup gate (Stage 0), the
management-account verification and Organization gate after that account exists (Stage 1), and
the sandbox billing verification before any invitation (Stage 2) — each with its own non-public
verification and Eric's separate informed authorization. If Eric does not authorize that
paid-plan exposure at any stage, provisioning stops and T15 option 2C (plan-only) requires an
explicit replacement decision; it is never inferred automatically.

The T02 requirements — zero incremental recurring spend, the payer-level zero-spend budget, Free
Tier usage alerts, and rejection of any separately billed service — remain in force. They are
**controls and desired outcomes, not a guarantee that a Paid Plan account cannot incur charges**.

Classification: absent upstream; compatible with `01`, `06`, `08`, `09`, T02, T15 d2/d4.
Rejected: option B (Organization created from the sandbox account; T15 2B double exception);
option C (no Organization; plan-only) — each only by Eric's explicit decision, never inferred;
option D (third account as `role-host`) — strands the T02 substrate.

### Decision 2 — Class assignments (logical aliases only)
`lab-management` → `management`; `lab-tooling` → `role-host` (the sandbox account);
`lab-workload-a`, `lab-workload-b` → `lab-workload`; `lab-requested` → `requested-fixture`.
Aliases follow the T05 grammar and are never live names. Classification: inherited from T15
d1/d5. Rejected: the #11 seed names ("restricted" implies a review class T06 does not give
slice A).

### Decision 3 — `role-host` does not coincide with a `lab-workload` account
The sandbox account hosts pipeline roles and state only and is never an assignment target; both
workload targets are new member accounts. Regional rule (collaborator correction): **All regional
IAM Identity Center and Identity Store operations use us-east-1. AWS Organizations is a global
service; its topology and inventory are not represented as Region-owned.** Classification:
compatible with T15 d1 ("may coincide"), `08`/`09`; inherited for Regions (RD-03, `03`).
Rejected: the sandbox account doubling as `lab-workload-b` (assignments into the Tier-0 host).

### Decision 4 — Two usable active workload accounts
Both created via Organizations `CreateAccount` from the management account (Eric action; new
root-e-mail aliases; `ACTIVE` state verified by re-discovery). Accounts persist after the POC.
**Closure is never automatic and requires separate Eric authorization. After an account is
closed, AWS provides a 90-day post-closure period during which AWS Support may reopen it; after
that period the account is permanently closed and remaining content is deleted. The management
account cannot be closed until the Organization's member accounts are removed or fully closed and
the Organization can be deleted.** Classification: inherited (T03 d5, `06`). Rejected: inviting
existing personal accounts (none identified).

### Decision 5 — Organization-instance and default-identity-store prerequisites
Enable IAM Identity Center as an **organization instance** in `us-east-1` from the management
account with the **Identity Center default store** as identity source; create at least one
workforce group by hand (group lifecycle stays with the identity source; T22 names the slice-A
group references). Enablement evidence, verification timestamp, and owner go to `instance.yml` /
T22 in alias form. **IAM Identity Center has no separate service charge for this use, but
enabling the organization instance occurs only after the decision-1 paid-plan/credit-impact gate.
Usage by related AWS services and every member account remains subject to the T02 cost
boundary.** Group creation remains a manual identity-source prerequisite and is not authorized by
approving T16. Classification: inherited (`07`, RD-03, T03 d2/d3). Rejected: an account instance
in the sandbox account (cannot assign to other accounts).

### Decision 6 — Delegated-administrator prerequisite
Register `lab-tooling` as Identity Center delegated administrator from the management account
after decision 5 (Eric action). Deployment roles never reside in the management account;
permission sets provisioned in, or assignments targeting, the management account are out of reach
(consistent with `lab-management` never being a target). Classification: compatible (`01`, T15
d4).

### Decision 7 — Aliases and fixture entries
Proposed labeled lab inventory fixture (committed at S6 under the accepted layout; see decision
15):

```yaml
# labeled lab inventory fixture — logical aliases only; no live identifiers
source: lab-fixture
accounts:
  - { alias: lab-management, class: management,        status: active,    intended_classification: none }
  - { alias: lab-tooling,    class: role-host,         status: active,    intended_classification: none }
  - { alias: lab-workload-a, class: lab-workload,      status: active,    intended_classification: identity-platform }
  - { alias: lab-workload-b, class: lab-workload,      status: active,    intended_classification: identity-platform }
  - { alias: lab-requested,  class: requested-fixture, status: requested, intended_classification: identity-platform }
```

`intended_classification` = the T06 account-delegation review class resolved for assignments
under that alias (`none` = never an assignment target). Exactly these four fields per entry (T15
d5); purposes and scenarios live in this record, not the fixture. Classification: compatible (T15
d5, T06 d3, T05). Rejected: purpose/scenario fields in the fixture.

### Decision 8 — The requested-fixture entry and its deferred behavior
`lab-requested` has `status: requested`, no binding (the binding record marks it `unbound`), no
OU, is referenced by exactly one slice-A assignment file, validates as **deferred** (never
invalid), is omitted from the applicable saved plan, is reported as deferred in the T20 plan
summary, and is **never created** — no Organizations action, account tag, or OU operation ever
targets it. Classification: inherited (RD-08, `06`, T03 d5). Rejected: binding it to a real
suspended account.

### Decision 9 — OU classification without live OU paths
Target OU classification as logical classes only: `lab-management` remains at the Organization
root; `lab-tooling`, `lab-workload-a`, and `lab-workload-b` reside in one **lab OU** (logical
class `lab`); `lab-requested` has no OU. Live OU IDs and paths exist only in the non-public
binding record. OU class is inventory metadata, never key or path input. OU creation and account
moves are separately authorized decision-11 actions. Classification: inherited (`03`, `06`,
RD-06, T03/T04). Rejected: all accounts directly under root (loses the stable scope `05`
prefers).

### Decision 10 — `ialab-` collision findings
No Identity Center instance existed on 2026-08-23, therefore no permission sets and no
collision. The collision check **must be re-run by the S6 re-discovery gate after the instance
exists**, before any plan. Classification: inherited (T15 d8, T05). Rejected: treating the
result as permanently clear.

### Decision 11 — Stop-with-remediation disposition
T16 resolves its proposed architectural decisions now; all live provisioning remains separately
authorized S6 remediation. No authorization below is implied by approving T16.

**Stage 0 — informed signup gate**

0.1 Present the known consequences of creating a new standalone management account: a unique
root email, secured root credentials and MFA, contact information, a valid payment method,
possible ineligibility for promotional credits, and future payer responsibility.

0.2 Eric may separately authorize creation of the standalone management account only. This
authorization does not authorize creation of an AWS Organization.

**Stage 1 — management-account verification and Organization gate**

1.1 After the management account exists, perform read-only, non-public verification of its
account plan, available/expiring credits, payment-method readiness, contact readiness, and
billing responsibility. Record no payment details or credentials.

1.2 Present the verified impact that creating an Organization may upgrade the account to Paid
Plan and expire remaining Free Tier credits.

1.3 Eric may separately authorize CreateOrganization in all-features mode.

1.4 After the Organization exists, separately authorize and apply the management account's
approved Organizations tags.

**Stage 2 — organizational structure**

2.1 Separately authorize creation of the logical lab OU.

2.2 Before inviting sandbox, perform read-only, non-public verification of sandbox's current
account plan, remaining credits, current bill/service lines, and the effect of joining the
Organization.

2.3 Present the verified consequences: possible Paid Plan conversion and credit expiration,
consolidated payer responsibility moving to lab-management, and Organization-wide aggregation
of applicable Free Tier allowances.

2.4 Eric may separately authorize the sandbox invitation and acceptance as one coordinated
action group.

2.5 After sandbox joins, separately authorize its approved Organizations tags and movement into
the lab OU.

**Stage 3 — workload accounts**

3.1 Eric may separately authorize creation of lab-workload-a. After it becomes ACTIVE,
separately authorize its approved tags and movement into the lab OU.

3.2 Eric may separately authorize creation of lab-workload-b. After it becomes ACTIVE,
separately authorize its approved tags and movement into the lab OU.

3.3 Neither account is presumed to receive independent promotional credits or an independent
Free Tier allowance.

**Stage 4 — cost controls**

4.1 Before enabling Identity Center or creating any POC resource, separately authorize creation
of the payer-level zero-spend AWS Budget.

4.2 Separately authorize enabling payer-level Free Tier usage alerts.

4.3 Verify both controls are active. Their presence is a control, not a guarantee that a Paid
Plan account cannot incur charges.

**Stage 5 — Identity Center prerequisites**

5.1 Separately authorize enabling the IAM Identity Center organization instance in us-east-1
with the default identity store.

5.2 Separately authorize creating the first workforce group in the default store.

5.3 Separately authorize registering lab-tooling as the IAM Identity Center delegated
administrator.

**Stage 6 — re-discovery and binding**

6.1 Perform read-only re-discovery and verify every T15 Decision 2 prerequisite, live OU
placement, approved account tags, payer-level budget and alerts, billing-plan evidence, payer
responsibility, default identity store, delegated administrator, and the ialab- collision
result.

6.2 A failed verification stops remediation before repository bootstrap or Terraform plan.

6.3 Only after successful re-discovery may Eric separately authorize creation of the encrypted
non-public binding record under aws-identity-access/evidence/binding/<fixture-digest>/.

lab-management remains at the Organization root. lab-tooling and both workload accounts belong
to the lab OU. lab-requested remains unbound, untagged, and without an OU. No fallback to T15
option 2B or 2C is inferred.

Classification: compatible (T15 d2; map note that lab provisioning never blocks S3/S4; `06`,
`09`). Rejected: keeping #11 open until provisioning; closing #11 as blocked.

### Decision 12 — Non-public binding evidence
*What:* exactly one record mapping each alias → live account name, ID, OU placement, status,
joined method; plus the fixture digest, discovery timestamp, caller identity type, and the
Identity Center instance and identity-store identifiers. *Where:* encrypted under
`aws-identity-access/evidence/binding/<fixture-digest>/` in the existing state bucket (T15
d12/d16). *When:* only after the decision-11 Stage 6.1 re-discovery succeeds — every T15
decision-2 prerequisite, live OU placement, approved account tags, payer-level budget and
alerts, billing-plan evidence, payer responsibility, default identity store, delegated
administrator, and the `ialab-` collision result verified — **and** under Eric's separate
authorization per Stage 6.3, which is the S6 authorization that first permits an S3 write. No
binding artifact and no S3 write now; until then the mapping exists nowhere in this repository
or any session. Classification:
compatible (T15 d5/d12/d16, RD-06). Rejected: an interim local copy.

### Decision 13 — Governing-document classifications and upstream refinements
As recorded in the claim-resolution record: claim 1 compatible, claims 2–3 inherited, claim 4
void. No new upstream amendment; T02's document-09 refinement and T15's inventory-fixture rule
are reaffirmed; OD-21 (inventory consumption model) remains open upstream and is noted for T09.
Rejected: a document-06 refinement for lab inventories (duplicates T15 d5).

### Decision 14 — Downstream handoffs and dependency effects
Handoffs to T09 #12, T22 #21, T14 #19, T20 #22, and T19 #14 (texts below). Closing #11 reduces
T20 #22's open blockers from five to four (#12, #15, #20, #21 remain); no ticket becomes newly
unblocked; the next frontier in map order is T09 #12. Rejected: creating an S6 provisioning
ticket now (an S6 ticket is generated from the accepted S5 plan).

### Decision 15 — Durable record and publication sequence
This record at `docs/wayfinding/map-1/11-lab-account-topology-and-fixtures.md` with a README
index line, published through the fail-closed sequence (validate → commit → push → verify
immutable URL → resolution → handoffs → map line → round-trip → close #11 with assignee retained
→ dependency check → continuity replace/commit/push/verify). The fixture **file** is not
committed now (layout is Pre-Baseline); it lands at S6 under the accepted layout. Rejected:
committing the fixture file under `docs/wayfinding/`.

### Decision 16 — Account lifecycle fields
**For each real active AWS account represented by the fixture, apply Organizations account tags
after that account has been created or joined: `project=aws-identity-access`, `environment=lab`,
`owner=identity-platform`, `class=<bound fixture class>`. The management account, role-host, and
two workload accounts receive their corresponding tags. `lab-requested` represents no AWS account
and therefore receives no AWS tag or Organizations mutation. Tagging is a separately authorized
decision-11 / S6 action.** Budget: payer-level zero-spend budget and Free Tier usage alerts only
(T15 d10); no per-account budgets. Regions: `us-east-1` for all regional Identity Center and
Identity Store operations; Organizations is global. No automatic expiry; governed cleanup of POC
resources per T15 d11 before any closure; closure only under the decision-4 rule and separate
Eric authorization. Classification: compatible (`06`, T15 d3/d10/d11, T06). Rejected:
per-account budgets and scheduled closure.

## Downstream handoffs (proposals; posted after publication)

- **T09 #12:** the alias fixture (decision 7) and the single non-public binding record
  (decision 12) are the snapshot inputs; transport/snapshot form is T09's; OD-21 remains open
  upstream.
- **T22 #21:** instance and identity-store prerequisites (decision 5): organization instance in
  `us-east-1`, default store, the hand-created first workforce group; enablement evidence and
  delegated-administrator evidence (decision 6) in alias form; all behind decision 11 Stages 0–5
  (each a distinct, separate authorization).
- **T14 #19:** fixture schema = exactly `alias`, `class`, `status`, `intended_classification`;
  `class` ∈ {management, role-host, lab-workload, requested-fixture}; `status: requested` ⇒
  deferred; **requested-fixture entries must never result in AWS account tags or OU
  operations**; a live identifier in the fixture is an error.
- **T20 #22:** two active workload aliases as distinct assignment targets; the deferred
  `lab-requested` target reported as deferred; no live identifier in plan summaries.
- **T19 #14:** account lifecycle stance — paid-plan/credit impact and payer responsibility
  (decision 1); 90-day post-closure semantics (decision 4); management-account teardown
  dependency (member accounts removed or fully closed before the Organization can be deleted);
  no scheduled or automatic account closure.
- **Future S6 remediation gate (carried to the S5 plan):** execute decision 11 Stages 0–6 in
  order, each step separately authorized — informed signup gate; management-account
  verification (after it exists) and Organization gate; lab OU; sandbox billing verification
  before invitation, then invitation/acceptance, tags, and move; per-account workload
  authorizations; payer-level zero-spend budget and Free Tier alerts before Identity Center;
  Identity Center enablement, first group, and delegated administrator as distinct
  authorizations; read-only re-discovery before the binding record, any repository bootstrap,
  or any plan.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Verdict⟧ and ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub mutation.
