---
authority: informative
derives_from:
  - docs/architecture/domain-overview.md
  - docs/adr/0005-instance-yml-declaration-and-verification-data.md
  - docs/adr/0006-prerequisite-evidence-freshness-gates-plan-and-apply.md
  - docs/adr/0007-workforce-groups-are-references.md
  - https://github.com/a24577t/aws_ami/blob/5f3cb7163f468730fd2ceb5d565c90b0bfda6099/docs/architecture/07-identity-center-platform.md
---

# Federated access walkthrough — slice A

How a person ends up with access in an AWS account under this repository's model.
Informative — the normative sources above prevail.

## The chain, end to end

1. **A person exists in the identity source.** In the lab this is the Identity Center
   default store (lab caveat: no external IdP; the first workforce group is hand-created
   as a separately authorized prerequisite, T16 #11 Stage 5.2). In the target estate the
   identity source is the enterprise IdP; either way, this repository never manages users
   or group membership.
2. **The person belongs to a workforce group.** Group lifecycle stays with the identity
   source; this repository holds only a reference — the stable `group-key` plus the exact
   identity-store DisplayName (ADR-0007). At plan time the pipeline resolves the GroupId
   and verifies the name exactly; failure blocks the plan.
3. **A permission set defines what the group may do.** Declared under
   `permission-sets/<key>.yml` in one of the two slice-A policy forms; the deployed AWS
   Name is `<resource_name_prefix><key>` and is what the person sees in the AWS access
   portal.
4. **An assignment binds group → permission set → account.** One grant per file, per
   account, by stable inventory alias; the plan shows each assignment as its own row;
   deferred accounts are reported deferred and skipped.
5. **The prerequisites gate everything.** The instance declaration (`instance.yml`,
   ADR-0005) plus fresh prerequisite evidence (ADR-0006) must verify at plan and apply —
   the instance, identity store, delegated administrator, and every referenced group are
   consumed, never created.
6. **Apply is a separate authorization.** The reviewed saved plan — and only that exact
   plan — is applied to explicitly named lab accounts after environment approval
   (T02 #3; T06 #8 decision 4).
7. **The person signs in through the AWS access portal** and sees the deployed
   permission-set Name in the assigned accounts for the configured `session_duration`.

## What is deliberately not in this walkthrough

Temporary elevation, break-glass, and runtime grants (owned by `aws-privileged-access`;
say "elevation", never "JIT"); IAM users and roles (out of slice A); identity-source
configuration such as SCIM (an evidenced prerequisite only). The exceptional-IAM-user
walkthrough does not exist in slice A — that surface is recorded absent (ADR-0004).
