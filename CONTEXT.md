# aws-identity-access

Durable AWS access governed as configuration: IAM Identity Center workforce-group
references, permission sets, and standing account assignments that persist until removed
through a governed PR. Platform-wide vocabulary (Baseline, Elevation, Delegation,
Exception, and the rest) lives in the pinned aws_ami root `CONTEXT.md` at
`5f3cb7163f468730fd2ceb5d565c90b0bfda6099` and is cited, never restated; honour its
`_Avoid_` rules — say "elevation", never "JIT". Terms below are this repository's domain
language, each fixed by a closed Wayfinder decision (cited by ticket).

## Language

### Identity and configuration

**Stable key**:
The immutable repository identity of a governed resource; equals the filename stem; the
only value other files reference. (T05 #7)
_Avoid_: name, id, slug

**Identity-store name**:
The exact DisplayName of an externally managed workforce group in the connected identity
store, used for plan-time lookup. (T05 #7)
_Avoid_: group name, display name

**Deployed name**:
`<resource_name_prefix><key>`, the AWS permission-set Name derived at plan time; never a
requester-authored value. (T05 #7)
_Avoid_: display_name, portal label (as an authored field)

**Deployment-scope prefix**:
A non-empty lab/POC string prepended to deployed permission-set names by
`infrastructure/`, never part of a stable key. (T04 #6)

**Requester surface**:
The `access/` tree; the only directory ordinary access-request PRs modify. (T04 #6)

**Selected-slice validation profile**:
The POC's validation profile for the selected slice, which rejects out-of-slice forms
without prohibiting them in the domain architecture. (T03 #4)
_Avoid_: schema prohibition (for profile rules)

### Prerequisites and evidence

**Manual prerequisite**:
A condition established outside this repository by separately authorized human action,
consumed here only as declaration plus evidence. (T22 #21)

**Declaration-and-verification data**:
Governed configuration stating intended manual state and referencing its evidence, never
asserting lifecycle ownership. (T22 #21)

**API-verifiable prerequisite**:
A manual prerequisite whose satisfaction the pipeline's authorized read APIs can establish
live at plan/apply. (T22 #21)

**Human attestation**:
A recorded, named-actor observation of a characteristic not exposed to the authorized
APIs, bound into the verification record and never upgraded to API-verified fact.
(T22 #21)

**Prerequisite Verification Record**:
The non-public per-re-discovery record of prerequisite-by-prerequisite results and
methods, digest-bound into the saved-plan authorization. (T22 #21)

**Prerequisite evidence**:
The tier-3 committed alias-form declaration plus its tier-2 non-public verification
artifacts. (T22 #21)

**Fresh / stale**:
Fresh requires the committed verification block, the current intact unexpired snapshot,
live API checks, and validly bound attestations; anything less is stale or missing and
blocks plan and apply. (T22 #21)

### Governance and review

**Review class**:
An independent class of approval (identity-platform, security, architecture,
deployment-authority) satisfied by registered principals. (T06 #8)

**Principal (ownership registry)**:
A stable, provider-neutral role or team; never a GitHub identity. (T06 #8)

**Change declaration**:
A merged, expiring governed record of intent that a plan gate requires before accepting an
exceptional operation. (T06 #8)

**Enforcement evidence**:
A derived, per-control, non-authoritative record of what GitHub actually enforces for a
governed route. (T06 #8)

**Domain decision register**:
The set of accepted domain ADRs under `docs/adr/` together with their subordinate index;
the authoritative record of decisions this repository owns. (T08 #13)
_Avoid_: decision log, parallel register

### Plans and CI

**PR class**:
The changed-path-derived category (with the exceptional-change overlay) fixing a PR's
review derivation and permitted plan effects. (T20 #22)

**Plan-effect classification**:
The two-layer deterministic classification of a saved plan: raw per-resource action
classes aggregated over the complete effect vector, then contract-level workflow classes
derived with configuration and declaration inputs. (T20 #22)

**Effective-access plan**:
The deterministic, alias-only, digest-bound human-reviewable rendering of the applicable
saved plan. (T20 #22)

**Plan preview**:
The sanitized, snapshot-blind, non-authoritative PR-time rendering; never
apply-authoritative. (T20 #22)

**Access-revocation acknowledgement**:
The explicit per-entry acknowledgement an ordinary assignment-removal PR carries for its
exact expected delete effect. (T20 #22)

**Generated-artifact manifest**:
The deterministic digest-bound metadata record for generated artifacts whose format cannot
safely embed the envelope. (T20 #22)

### Validation

**Validation finding**:
One deterministic result under the T14 finding-record contract. (T14 #19)

**Severity vocabulary**:
The closed set `error | warning | deferred`; `deferred` is reserved for the RD-08
requested-inventory condition and `warning` is reserved-unpopulated. (T14 #19)

**Stage**:
The closed set `validation | plan | apply | generated-ci` attributing where a code may
fire. (T14 #19)

**Canonical triggering layer**:
The single surface and rule layer on which a validation code fires. (T14 #19)

**Catalog data**:
The two repository-controlled, digest-pinned action-catalog inputs of the
standing-administrator detector. (T14 #19)

**Dormant code**:
A catalogued code whose enforcement and fixture obligations begin at its named activation
condition. (T14 #19)

**Fixture expectation set**:
The declared exact finding set of a negative fixture. (T14 #19)

### Documentation

**Authority class**:
The one-field answer to what binds a domain document: `normative`, `informative`, or
`generated`. (T23 #23)

**Derives-from citation**:
The mandatory non-empty, deduplicated, resolvable list of normative sources an informative
document derives from. (T23 #23)

**Documentation set**:
The accepted list of slice-A domain documents with their authority classes and owning
tickets. (T23 #23)

**Navigation exemption**:
The root README and this glossary carry no authority header, hold no independent
authority, and summarize or navigate only by citation, with accepted decisions prevailing
on any conflict. (T23 #23)
