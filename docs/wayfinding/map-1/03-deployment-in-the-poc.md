---
map: 1
map_url: https://github.com/a24577t/aws-identity-access/issues/1
ticket: 3
title: "T02 — Deployment in the POC: excluded, plan-only, or implemented"
url: https://github.com/a24577t/aws-identity-access/issues/3
type: grilling
lifecycle_status: resolved
architectural_status: proposed
decision_authority: "Eric — human project owner and decision authority"
executed_by: "Claude — repository-owner role, under wayfinder-repo-owner with grill-with-docs"
recorded: 2026-08-27
sources:
  backfill: "T08 #13 decision 13 result-record backfill, reconstructed 2026-08-27 from the ticket's complete comment history; traceability, not authority"
  resolution_comment: https://github.com/a24577t/aws-identity-access/issues/3#issuecomment-5381840972
  close_comment: https://github.com/a24577t/aws-identity-access/issues/3#issuecomment-5381842564
  governing_revision: aws_ami 5f3cb7163f468730fd2ceb5d565c90b0bfda6099 (T01, #2)
  resolved: 2026-08-22
---

# T02 — Deployment in the POC: staged lab apply

> **Backfilled discovery record** — produced 2026-08-27 under the separately authorized T08
> #13 decision-13 result-record backfill, reconstructing the complete durable result of
> T02 #3 from the ticket's comment history. Backfill preserves provenance and traceability
> only: it confers no new authority, changes no decision, and does not alter the approved S4
> Architecture Grill verdict. **Nothing here is accepted architecture: every decision is a
> proposal until ⟦G-Accept⟧.** GitHub issue #3 is the workflow/index surface and links to
> this record.

Grill completed and approved by Eric as the human project owner and decision authority,
2026-08-22, under `wayfinder-repo-owner` with `grill-with-docs` on the four document-governed
claims. Governing documents cited at the aws_ami revision pinned by T01 (#2). Nothing below
authorized an AWS mutation during Wayfinder, Architecture Grill, or specification work; AWS
apply requires later, separate owner authorization.

## Deployment mode

The POC completion target is **staged lab apply**:

1. Validation must pass.
2. Terraform produces a saved plan from reviewed code.
3. The saved plan is reviewed and explicitly approved.
4. That exact plan may be applied only to explicitly named lab accounts.
5. No production environment is authorized.

This defines the POC *target*. It does **not** authorize an AWS mutation; apply requires
later, separate owner authorization.

## Tier-0 lab assumption

The POC may reuse the existing `mcp_gateway01` AWS lab substrate with these boundaries:

- Use an isolated `aws-identity-access` state-key prefix.
- Create repository-specific OIDC/deployment and execution roles; do not reuse or broaden the
  MCP project's roles.
- Pin Terraform and the AWS provider exactly before apply.
- Verify CV-07 support for every Identity Center feature at the selected provider pin.
- Apply only the reviewed saved plan.
- If any prerequisite cannot be satisfied, stop at plan-only.

**Lab-only exception (explicit, never production precedent).** The existing backend shares
the lab workload account rather than residing in the dedicated state account required by
`09-tier0-execution.md`. Recorded as a lab-only exception for the POC.

**Proposed upstream refinement — document 09:** define whether a controlled nonproduction POC
exception (state backend co-located in a lab workload account) is permitted, and under what
boundaries. The owner carries the proposal; this map never edits aws_ami.

**OD-03, OD-04, and OD-09** (state backend, execution principal, provider pinning) remain
unresolved platform-wide; the lab assumption above does not resolve them.

## Cost boundary

Lab execution must add **zero incremental recurring spend** relative to the existing
`mcp_gateway01` lab baseline:

1. Limit the first slice to no-additional-charge IAM, IAM Identity Center, Organizations,
   STS, and CloudFormation/StackSets capabilities.
2. Use named lab accounts and the minimum Region scope.
3. Reuse the existing backend and KMS key; create no new customer-managed KMS key.
4. Reject any plan introducing a separately billed service unless Eric separately approves
   it.
5. Establish Free Tier / cost-budget alerts before apply.
6. Remove temporary test resources after verification.
7. Treat Free Tier usage as aggregated across the AWS Organization, not multiplied per test
   account.
8. Treat the existing customer-managed KMS key as baseline cost, not new POC spend.

Official cost sources recorded on the ticket: the AWS Organizations pricing page, the IAM
User Guide, the CloudFormation StackSets getting-started guide, the consolidated-billing
guide, the AWS Budgets pricing page, and the KMS pricing page.

## Claim-resolution record (grill-with-docs)

Per claim: governing document + identifier · claim · result · upstream amendment/refinement.

**1. "Terraform is the primary desired-state orchestrator."**
- Authority: `00-governing-principles.md` I-2 and I-3.
- Result: **inherited**. Amendment: none.

**2. "CloudFormation StackSets may serve as a Terraform-governed engine for identical
multi-account IAM resources."**
- Authority: I-2, I-3, and `04-enforcement-plane-precedence.md` Preference 3.
- Result: **inherited**, with the precedence constraint retained.
- Refinement (this repository): a requirement may use StackSets only after reaching
  Preference 3. Terraform owns the StackSet definition and targeting;
  CloudFormation/StackSets reconcile the generated resources.
- Upstream amendment: none.

**3. "A resource has exactly one reconciliation owner."**
- Authority: I-3, I-6, and the `reconciliation` field in `05-runtime-mutation-contracts.md`.
- Result: **compatible**; the blanket singular rule is not explicit upstream.
- Refinement: adopt as an `aws-identity-access` domain decision, and record a **proposed
  upstream clarification to document 05**. Terraform must not directly manage resources
  generated and reconciled by StackSets. Runtime-mutation contracts name the applicable
  reconciliation plane. T08 (#13) determined the durable domain decision-register form.

**4. "Ordinary access grants never silently expand through StackSet or OU auto-deployment."**
- Authority: root `CONTEXT.md` definition of *Baseline*, and document 04's Preference 3 /
  automatic-new-account fields.
- Result: **absent but compatible**.
- Refinement: adopt as a domain decision; no upstream amendment. OU input may expand only
  into an explicit account list visible in the plan. Adding or moving an account grants no
  automatic ordinary human access. StackSets remain eligible only for identical fleet IAM
  resources with explicit targeting and explicit auto-deployment behavior.

## Carried forward (as recorded at resolution)

- Upstream proposals for the owner to carry: document 09 (nonproduction POC exception),
  document 05 (singular reconciliation-owner clarification).
- Domain decisions awaiting the T08 register form: singular reconciliation ownership; no
  silent account expansion of ordinary access grants.
- Lab contract details (T15 #10, T16 #11) and the slice (T03 #4) are decided by their own
  tickets; this resolution set their deployment-mode, Tier-0, and cost boundaries.

## Status

`lifecycle_status: resolved` · `architectural_status: proposed`. Nothing in this record is
accepted until ⟦G-Accept⟧; nothing in it authorizes an AWS or GitHub mutation. This backfill
record changes nothing decided by T02.
