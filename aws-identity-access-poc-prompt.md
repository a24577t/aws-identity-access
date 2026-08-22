# AWS Identity Access Repository POC Bootstrap Prompt

Use this prompt to initialize a new, empty `aws-identity-access` repository. The existing
`scaffolding/aws-identity-access/` and exploratory `aws-identity-access/` directories in the
architecture repository are design evidence only. Do not clone, copy, or mechanically migrate
their layouts.

---

You are the lead implementation agent for a new repository named `aws-identity-access`.

Build a working proof of concept from an empty repository. Use multiple agents for bounded,
independent reviews of architecture, requester experience, AWS resource modeling, validation,
and security. Coordinate their findings before integrating changes.

## Authority and reference material

Before designing the repository, read:

- The complete `docs/architecture/` set in the `aws_ami` architecture repository.
- Its root `CONTEXT.md` ubiquitous-language glossary.
- The old `scaffolding/aws-identity-access/` directory.
- The exploratory `aws-identity-access/` implementation and its `REVIEW.md`.

The architecture documents and glossary are authoritative. The scaffold and exploratory
implementation are references only. They contain useful examples as well as rejected decisions.
Do not preserve a convention merely because it already exists.

Record the exact architecture repository commit used to initialize this POC. Link back to
immutable source URLs where possible.

## Repository purpose

This repository owns durable AWS access: access that persists until explicitly changed through a
governed pull request.

It owns:

- AWS IAM Identity Center configuration.
- Workforce group references sourced from Okta or Active Directory.
- Permission sets.
- Standing account assignments.
- Enterprise/shared IAM roles and policies.
- Permission boundaries.
- Exceptional native IAM users and IAM groups.
- Identity-access runtime-mutation contracts owned by this resource domain.
- Validation, planning, and deployment implementation for those resources.

It does not own:

- Temporary request -> grant -> expire workflows; those belong to `aws-privileged-access`.
- Runtime requests, grants, sessions, or credentials.
- Workload-coupled execution roles; those remain in workload repositories.
- The authoritative organization account/OU/Region inventory.
- Generated AWS identifiers as configuration keys.

## Human access model

Model the two AWS entry experiences explicitly.

Federated workforce access is the normal path:

```text
Okta or AD user
-> enterprise group
-> IAM Identity Center group
-> permission set
-> AWS account assignment
-> generated AWS IAM role/session
-> AWS access portal
```

Exceptional native access is account-local:

```text
IAM user
-> IAM group/policy or assumable role
-> IAM-user AWS Management Console sign-in page or access keys
```

IAM users are exceptions. Require owner, justification, security approval, review/expiry date,
account, credential constraints, and a permission boundary.

Temporary elevation is not standing access. Administrator access should be elevation-only; do
not create standing `AdministratorAccess` account assignments. Break-glass is separate from both
ordinary access and elevation.

## Top-level separation of concerns

Make it visually obvious whether a change affects desired access, authoritative documentation,
governance, implementation, or deployment.

Use this top-level model:

```text
aws-identity-access/
|-- README.md
|-- CONTEXT.md
|-- access/                 # governed desired access; normal requester PR surface
|-- governance/             # exceptional/high-authority authorization declarations
|-- docs/
|   |-- architecture/       # authoritative domain documentation
|   |-- guides/             # explanatory, non-authoritative user documentation
|   `-- generated/          # generated views; never manually edited
|-- src/                    # implementation code
|-- infrastructure/         # Terraform and CloudFormation deployment code
|-- schemas/                # machine-enforced configuration contracts
|-- tests/
`-- .github/
```

The name `access/` is deliberate. Do not rename it to `configuration/`, `config/`, or `vars/`.

Define it in the root README as:

> `access/` contains governed desired access. Routine access-request pull requests modify this
> directory. It contains no implementation code, credentials, generated AWS identifiers, or
> runtime requests, grants, and sessions.

## Authority hierarchy

Document this precedence:

```text
Platform architecture in aws_ami
-> domain architecture in docs/architecture/
-> machine-enforced contracts in schemas/ and validation code
-> desired-access instances in access/
-> implementation in src/ and infrastructure/
-> generated views and runtime state
```

The root README is navigation, not normative architecture.

Every file in `docs/architecture/` must carry metadata identifying it as normative, its authority,
scope, and decision owner. Guides must identify themselves as informative and cite the normative
documents from which they derive. Generated documentation must say `do_not_edit: true` and name
its source inputs.

Schemas enforce architecture but must not silently invent it. Each non-obvious policy validation
should cite an architecture rule or stable decision ID.

## Desired-access structure

Organize `access/` around AWS-native services and resource/workflow names:

```text
access/
|-- identity-center/
|   |-- instance.yml
|   |-- identity-source/
|   |   |-- okta.yml
|   |   |-- verification.yml
|   |   `-- procedures/
|   |-- groups/
|   |-- permission-sets/
|   `-- account-assignments/
|       `-- <account-name>/
|           `-- <group-key>--<permission-set-key>.yml
`-- iam/
    `-- accounts/
        `-- <account-name>/
            |-- roles/
            |-- customer-managed-policies/
            |-- permission-boundaries/
            |-- users/
            `-- groups/
```

Use `.yml` throughout governed access configuration. Prefer one AWS resource or access grant per
file.

## Natural identifiers

Use stable human keys rather than generated AWS identifiers.

Permission set:

```yaml
key: developer
display_name: Developer
```

The immutable `key` is used by filenames and references. `display_name` is the user-facing AWS
access portal label.

Workforce group:

```yaml
key: engineering
display_name: Engineering
source:
  provider: okta
  group_name: AWS-Engineering
```

Assignments reference the stable group key. The external Okta/AD group name is mutable metadata
whose change requires identity-platform and security review.

An account assignment is naturally identified by:

```text
account + principal + permission set
```

Represent it as one file:

```text
access/identity-center/account-assignments/dev-payments/engineering--developer.yml
```

```yaml
account: dev-payments
principal:
  type: GROUP
  group: engineering
permission_set: developer
```

Do not aggregate several account assignments into one account file.

## Account and inventory rules

Reference internal accounts, OUs, and Regions by stable inventory names, never copied IDs. The
authoritative binding remains in `aws-organization-governance`.

A reference to an account with `status: requested` is valid but deployment-deferred:

- schema and reference validation pass;
- tooling emits a warning;
- deployment omits the target until its account ID exists;
- it is never described as invalid.

A name absent from the inventory fails validation.

Consume the current published inventory but record the exact version or digest in CI plans and
deployment evidence. A local inventory may exist only as an explicitly labeled test fixture.

## Account-assignment targeting

IAM Identity Center assigns principals to accounts, not OUs. Do not make OU membership part of an
assignment's natural key.

OU selection may exist as authoring or planning input only if it expands into a reviewable,
explicit account list. Adding or moving an account must not silently grant human access. An
inventory change should produce a pull request showing the resolved assignment changes.

Do not enable silent StackSet or other OU auto-deployment for ordinary access grants.

## IAM role model

Every IAM role must contain its complete `trust_policy` directly in the role file. Do not create
reusable trust profiles or trust-policy references. Trust is deliberately duplicated so a
reviewer sees permissions and every allowed assumer together, and changing one role cannot
silently alter another.

Each role should explicitly state:

- name/key;
- description;
- owner;
- complete trust policy;
- managed and customer-managed policies;
- permission boundary;
- maximum session duration;
- IAM path;
- tags where relevant.

Do not use security-sensitive defaults for trust, policies, permission boundaries, session
duration, assignments, or role paths. Defaults may cover non-authorizing metadata such as tags.

Keep IAM group membership on the group only. Do not duplicate group membership on both IAM user
and IAM group records.

Permission-set inline policies are embedded in their permission-set files. They must not reference
an account-local policy. Customer-managed permission-set policy references require the named
policy to exist in every assigned account.

## Fleet roles and deployment

Account-specific IAM resources are managed directly from their account-scoped access definition.
For a genuinely identical enterprise role deployed to many accounts, support an explicit fleet
definition:

```text
access/deployments/fleet-roles/<role-key>/
|-- role.yml
`-- targets.yml
```

The target expansion must be visible in the pull-request plan. Do not copy identical role files
into every account.

Use Terraform as the primary desired-state orchestrator. Use service-native organization
mechanisms where they provide stronger governance. CloudFormation StackSets may be used as a
Terraform-governed deployment engine for identical multi-account IAM resources.

A resource has exactly one reconciliation owner. Terraform and CloudFormation must never both
manage the same generated IAM role or policy.

## Governance

Use `governance/` for declarations that are not routine desired-access grants:

```text
governance/
|-- runtime-mutations/
|-- exceptions/
`-- ownership/
```

Define a governed organizational-principal registry. Keep resource ownership, CODEOWNER review,
security approval, and runtime approval as distinct concepts with stable keys.

Runtime-mutation contracts are owned here when they authorize mutations to identity-access
resources, but execution belongs to `aws-privileged-access`.

Do not create a `pa-*` or similar reserved namespace as architecture. Runtime/reconciliation
ownership must come from an explicit contract or ownership metadata, not a naming convention.

## Pull-request experience

Define at least four PR classes:

1. Access grant: changes account assignments; requested by teams/account owners.
2. Access definition: changes groups or permission sets; identity and security review.
3. IAM exception/shared role: changes account IAM or governance exceptions; identity and security
   review.
4. Platform change: changes architecture, schemas, validation, or infrastructure; architecture,
   platform, and security review.

Ordinary requesters should normally modify only `access/`. They must not need to edit `src/`,
`schemas/`, `infrastructure/`, or authoritative architecture for a routine grant.

CI must classify the PR by changed paths and generate an effective-access plan showing:

```text
action
principal
permission
target accounts
session duration
permission boundary
persistence/lifecycle
AWS access portal effect
required reviewers
deferred targets
```

Generate workflow-oriented and account-oriented views from the AWS-native source configuration:

- requester view: which grant should be changed;
- account view: who can access this account;
- principal view: which accounts and permissions a group receives.

Generated views are not authoritative and must never be manually edited.

## CODEOWNERS expectations

Apply distinct review authority to:

- domain architecture;
- schemas and validation;
- implementation code;
- infrastructure;
- governance declarations;
- permission sets;
- production account assignments;
- IAM roles and trust policies;
- exceptional IAM users and groups.

Every IAM role change requires identity-platform and security review because its trust and
permissions are co-located.

## POC examples

Create realistic valid examples covering:

- Okta-backed workforce groups;
- read-only, developer, billing, security-audit, and production-operator permission sets;
- single-account group assignments;
- explicit multi-account grants represented as separate assignment resources;
- a requested-account assignment that validates as deferred;
- a USER-principal assignment isolated as an exception;
- service-principal trust;
- GitHub OIDC trust with pinned subjects;
- internal role-to-role trust using account names;
- third-party trust with ExternalId;
- an enterprise fleet role with explicit targets;
- two materially different exceptional IAM users;
- an IAM group containing exceptional IAM users;
- a workload-local role documented as a counterexample and deliberately absent.

Do not create standing administrator assignments.

Create invalid specimens for every validator error code, including unknown inventory names,
expired exceptions, missing approvals, unresolved references, raw internal account IDs, unsafe
OIDC wildcards, malformed external trust, overly broad policies, duplicate assignments, and
generated/AWS-owned role names.

## Validation and tests

Implement executable validation for:

- schema conformance;
- path/key agreement;
- natural composite assignment identifiers;
- inventory resolution;
- requested-account deferral;
- cross-file references;
- immutable key usage;
- exception approvals and expiry;
- trust-policy safety;
- raw internal account IDs;
- generated resource exclusions;
- duplicate grants;
- policy breadth;
- no standing administrator assignments;
- exactly one reconciliation owner.

Provide a pinned, reproducible test environment. A small Dockerfile using an official Python image
and pinned Python dependencies is acceptable. CI and local instructions must run the same commands.

## Documentation deliverables

Create:

- a root navigation README;
- authoritative domain architecture documents;
- a domain decision register;
- a configuration-contract document;
- requester and reviewer guides;
- federated and exceptional-IAM-user walkthroughs;
- repository-boundary counterexamples;
- at least three end-to-end PR scenarios;
- generated effective-access examples;
- a migration/reference note describing which old scaffold conventions were rejected.

Explicitly record these rejected conventions:

- reusable trust profiles;
- `configuration/` or `vars/` as the requester surface (use `access/`);
- aggregated multi-grant account assignment files;
- OU directories as account-assignment identity;
- security-sensitive defaults;
- bidirectional IAM group membership;
- account-local policy references from permission-set inline policies;
- standing administrator access;
- runtime ownership inferred from reserved names.

## Completion criteria

Before finishing:

- Run all validation and tests.
- Confirm every valid example passes.
- Confirm every invalid specimen fails for its documented reason.
- Confirm the requested-account example passes with a deferred warning.
- Confirm every role carries its own complete trust policy.
- Confirm no standing administrator assignment exists.
- Confirm ordinary requester workflows touch only `access/`.
- Confirm architecture, code, infrastructure, governance, schemas, and desired access are visually
  and mechanically distinct.
- Review the result as an access requester, account owner, identity engineer, security reviewer,
  auditor, and repository maintainer.

Return a concise report containing the resulting tree, architectural interpretations, validation
results, unresolved decisions, and the files each persona should read first. Do not stop at a
design proposal: create the working POC repository.

---

