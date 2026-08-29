"""The T14 #19 code catalogue (R2 #27 rows 3-4).

The complete slice-A validation contract as data: 79 codes, 13 families,
78 active, 1 dormant. Transcribed from the T14 #19 record's Catalogue section
(docs/wayfinding/map-1/19-validation-contract-for-the-selected-slice.md); the
record prevails on any divergence. Stable domain ADR IDs join the citations
per T08 #13 d11. Severity is fixed here and only here: no validator, profile,
configuration, or implementation may downgrade it (T14 #19 d1).
"""

from collections import namedtuple

SEVERITIES = frozenset({"error", "warning", "deferred"})
STAGES = frozenset({"validation", "plan", "apply", "generated-ci"})

# layer: the canonical triggering layer (T14 #19 d2 - exactly one per code).
# rule_ids: ordered authority citations (T14 #19 d9a; ADR IDs per T08 #13 d11).
# activation: dormant codes name their activation condition (T14 #19 C6).
Entry = namedtuple(
    "Entry",
    ["family", "severity", "stages", "layer", "rule_ids", "state", "activation"],
    defaults=("active", None),
)

V = "validation"
P = "plan"
A = "apply"
G = "generated-ci"


def _e(family, severity, stages, layer, rule_ids, state="active", activation=None):
    return Entry(family, severity, tuple(stages), layer, tuple(rule_ids), state, activation)


CATALOGUE = {
    # --- INV: organization-inventory and snapshot classes (T09 d18-d19) ---
    "INV-DEFERRED": _e("INV", "deferred", (V, P, A),
                       "referenced alias has status: requested in the consumed inventory",
                       ("RD-08", "T09 #12 d12/d19", "T10 #15 d1")),
    "INV-ABSENT": _e("INV", "error", (V, P, A),
                     "referenced alias absent from the committed fixture (validation) or consumed snapshot (plan/apply)",
                     ("RD-06", "T09 #12 d19", "T10 #15 d1")),
    "INV-UNBOUND": _e("INV", "error", (P, A),
                      "active alias without a live binding in the binding snapshot",
                      ("T09 #12 d11/d19",)),
    "INV-STATE": _e("INV", "error", (P, A),
                    "bound account State is not ACTIVE (Status is never read)",
                    ("T09 #12 d11/d19",)),
    "INV-RENAME": _e("INV", "error", (P, A),
                     "live Name differs from live_name",
                     ("T09 #12 d19", "OD-12")),
    "INV-OU": _e("INV", "error", (P, A),
                 "ListParents result differs from ou_id",
                 ("T09 #12 d13/d19",)),
    "INV-DUP": _e("INV", "error", (V, P, A),
                  "duplicate alias entry in the committed fixture; duplicate alias, live-name, or live-ID binding",
                  ("T09 #12 d19", "T10 #15 d1/d4")),
    "INV-UNALIASED": _e("INV", "error", (P, A),
                        "unaliased live account discovered in the governed lab OU",
                        ("T09 #12 d19", "ADR-0002")),
    "INV-DIGEST": _e("INV", "error", (P, A),
                     "digest disagreement among key, envelope snapshot_id, metadata, sidecar; canonicalization or I-JSON failure",
                     ("T09 #12 d4/d19",)),
    "INV-STALE": _e("INV", "error", (P, A),
                    "snapshot expired (90-day backstop), superseded, or current pointer changed during verification",
                    ("T09 #12 d10/d19",)),
    "INV-MISSING": _e("INV", "error", (P, A),
                      "no snapshot or current pointer",
                      ("T09 #12 d19",)),
    "INV-PARTIAL": _e("INV", "error", (P, A),
                      "incomplete pagination, API error, or throttling during live verification",
                      ("T09 #12 d19",)),
    "INV-PROHIBITED-FIELD": _e("INV", "error", (P, A),
                               "prohibited field in the snapshot body; a lab-requested entry bound or carrying live fields",
                               ("T09 #12 d5/d12/d19",)),
    "INV-BOUNDARY": _e("INV", "error", (P, A),
                       "authoritative organization/Identity Center boundary mismatch; body.schema_version differs from 1",
                       ("T09 #12 d19",)),
    "INV-PUBLIC-LEAK": _e("INV", "error", (V, P, A, G),
                          "live, account-local, or generated identifier in public content; sole exemption the T21 AWS-managed-policy ARN vocabulary",
                          ("T09 #12 d22", "T15 #10 d12", "T20 #22 d3/d7", "T19 #14 d8", "T21 #20 d2")),
    # --- PRQ: prerequisite verification (T22 d4; error, never deferred) ---
    "PRQ-MISSING": _e("PRQ", "error", (P, A),
                      "committed verification block absent - unverified prerequisites block plan and apply",
                      ("T22 #21 d1/d4", "ADR-0006")),
    "PRQ-SNAPSHOT": _e("PRQ", "error", (P, A),
                       "instance.yml verification reference fails against the binding snapshot (related_inv context, never a second finding for the same root cause)",
                       ("T22 #21 d1/d4", "T09 #12 d9/d10", "T14 #19 d4a", "ADR-0006")),
    "PRQ-INSTANCE": _e("PRQ", "error", (P, A),
                       "API-verifiable instance presence/type failure",
                       ("T22 #21 d3/d4", "ADR-0006")),
    "PRQ-IDENTITY-STORE": _e("PRQ", "error", (P, A),
                             "identity-store binding failure",
                             ("T22 #21 d3/d4", "ADR-0006")),
    "PRQ-DELEGATED-ADMIN": _e("PRQ", "error", (P, A),
                              "sso.amazonaws.com-scoped delegated-administrator registration failure",
                              ("T22 #21 d3/d4", "ADR-0006")),
    "PRQ-ATTESTATION": _e("PRQ", "error", (P, A),
                          "missing, stale, mismatched, integrity-invalid, or otherwise invalid human attestation",
                          ("T22 #21 d3/d4/d5", "ADR-0006")),
    "PRQ-GROUP": _e("PRQ", "error", (P, A),
                    "referenced-group resolution failure (GetGroupId with exact-DisplayName verification)",
                    ("T22 #21 d4", "T05 #7 d2", "ADR-0007")),
    # --- P-OOS: selected-slice profile (T21 d7; fixed wording) ---
    "P-OOS-CMP": _e("P-OOS", "error", (V,),
                    "customer-managed policy reference in a permission set",
                    ("T21 #20 d7", "T03 #4 d4", "ADR-0004")),
    "P-OOS-BOUNDARY": _e("P-OOS", "error", (V,),
                         "permission-boundary content",
                         ("T21 #20 d7", "T03 #4 d4", "ADR-0004")),
    "P-OOS-USER": _e("P-OOS", "error", (V,),
                     "principal.type USER in an assignment (profile layer; intentionally paired with ASN-SHAPE per T10 d7)",
                     ("T21 #20 d7", "T10 #15 d2", "RD-05", "ADR-0004")),
    "P-OOS-IDENTITY-SOURCE": _e("P-OOS", "error", (V,),
                                "instance.yml identity_source.type other than identity-center-default",
                                ("T22 #21 d2", "ADR-0004")),
    "P-OOS-PATH": _e("P-OOS", "error", (V,),
                     "file under one of the six enumerated absent-for-slice surfaces",
                     ("T04 #6 d6", "T03 #4", "ADR-0004")),
    "P-OOS-POLICY-FORM": _e("P-OOS", "error", (V,),
                            "domain-valid permission set with more than one managed_policies entry, or both forms present",
                            ("T21 #20 d1", "ADR-0004")),
    # --- KEY: identity, grammar, uniqueness, reference integrity (T05 d1-d5) ---
    "KEY-GRAMMAR": _e("KEY", "error", (V,),
                      "key violates the T05 grammar or its length bounds (permission-set 2-24; group 2-64)",
                      ("T05 #7 d1/d5",)),
    "KEY-FILENAME": _e("KEY", "error", (V,),
                       "filename stem differs from key",
                       ("02 v1", "T05 #7 d2/d3")),
    "KEY-COMPOSED": _e("KEY", "error", (V,),
                       "composed deployed Name over 32, failing the AWS Name pattern, or prefix budget over 8 including delimiter",
                       ("T05 #7 d1/d3", "T15 #10 d8")),
    "KEY-DESCRIPTION": _e("KEY", "error", (V,),
                          "permission-set description missing, outside 1-700, or failing the documented AWS pattern",
                          ("T05 #7 d3",)),
    "KEY-IDSTORE-NAME": _e("KEY", "error", (V,),
                           "identity_store_name missing, empty, or with leading/trailing Unicode whitespace or control characters",
                           ("T05 #7 d2/d5",)),
    "KEY-DUP": _e("KEY", "error", (V,),
                  "duplicate key within groups/ or permission-sets/; more than one group file per exact identity_store_name",
                  ("T05 #7 d5",)),
    "KEY-DANGLING": _e("KEY", "error", (V,),
                       "dangling reference, alias, redirect, or derived key anywhere in the key space",
                       ("T05 #7 d4/d5",)),
    "KEY-PROTECTED": _e("KEY", "error", (V, P, A),
                        "deployed-Name collision within desired configuration (validation) or with a pre-existing permission set (plan/apply)",
                        ("T05 #7 d5", "T15 #10 d8", "ADR-0009")),
    # --- ASN: assignment shape and agreement (T10 d1-d3) ---
    "ASN-SHAPE": _e("ASN", "error", (V,),
                    "unrecognized domain assignment representation (domain layer)",
                    ("T10 #15 d2",)),
    "ASN-ACCOUNT-ALIAS": _e("ASN", "error", (V,),
                            "account-alias form violation in the assignment directory or alias grammar",
                            ("T10 #15 d1", "T15 #10 d5", "T05 #7 d1")),
    "ASN-AGREEMENT": _e("ASN", "error", (V,),
                        "three-way path/content mismatch: directory-account; filename segment 1-principal.group; segment 2-permission_set",
                        ("T10 #15 d3", "02 v1", "I-1")),
    # --- ADM: standing administrator (T07 d1-d2; T21 d6; T14 d5; ADR-0008) ---
    "ADM-CAPABLE": _e("ADM", "error", (V,),
                      "the five-rule hazard detector rejects an admin-capable definition (single-file definition hazard)",
                      ("T21 #20 d6", "T07 #9 d1", "ADR-0008")),
    "ADM-STANDING": _e("ADM", "error", (V,),
                       "cross-file: admin-capable definition combined with a standing workforce GROUP assignment referencing it",
                       ("T07 #9 d1/d2", "ADR-0008")),
    "ADM-CATALOG": _e("ADM", "error", (V,),
                      "action catalog or privileged-mutation set absent, digest-mismatched, schema-unsupported, or unable to expand a required wildcard - fail closed",
                      ("T14 #19 d5", "T21 #20 d6", "ADR-0008")),
    # --- GOV: governance registry, routing, declarations, enforcement (T06) ---
    "GOV-PRINCIPAL": _e("GOV", "error", (V,),
                        "principal record schema violation",
                        ("T06 #8 d2",)),
    "GOV-CLASS": _e("GOV", "error", (V,),
                    "review-class record violation (unresolved principal; duplicates; authored enforcement status)",
                    ("T06 #8 d2",)),
    "GOV-OWNER": _e("GOV", "error", (V,),
                    "a governed file's owner does not resolve to a principal key",
                    ("T06 #8 d1",)),
    "GOV-ROUTE": _e("GOV", "error", (V,),
                    "uncovered governed path, or an unknown/ambiguous/inactive account under account-assignments",
                    ("T06 #8 d3",)),
    "GOV-CODEOWNERS": _e("GOV", "error", (G,),
                         "generated CODEOWNERS disagrees with the registry, routing, and handle mapping",
                         ("T06 #8 d2/d3",)),
    "GOV-DECLARATION": _e("GOV", "error", (V,),
                          "change-declaration schema violation (discriminated kind; required fields; prohibited fields)",
                          ("T06 #8 d5", "declaration-vocabulary amendment")),
    "GOV-DECL-MATCH": _e("GOV", "error", (P,),
                         "plan-gate declaration matching failure",
                         ("T06 #8 d5", "T20 #22 d5")),
    "GOV-ENFORCEMENT": _e("GOV", "error", (P, A),
                          "a required control's evidence is unenforced/unknown without a current applicable lab exception",
                          ("T06 #8 d3/d4",)),
    "GOV-APPROVAL-CLASS": _e("GOV", "error", (P,),
                             "one review event or physical identity satisfying more than one independently required class",
                             ("T06 #8 d1/d3",)),
    # --- FIX: alias inventory fixture (T15 d5; T16 d7) ---
    "FIX-FIELDS": _e("FIX", "error", (V,),
                     "fixture entry field set not exactly {alias, class, status, intended_classification}",
                     ("T16 #11 d7", "T15 #10 d5")),
    "FIX-CLASS": _e("FIX", "error", (V,),
                    "class outside {management, lab-workload, role-host, requested-fixture}",
                    ("T16 #11 d7", "T15 #10 d1")),
    "FIX-ALIAS": _e("FIX", "error", (V,),
                    "alias violates the T05/T15 grammar",
                    ("T15 #10 d5", "T05 #7 d1")),
    "FIX-LIVE": _e("FIX", "error", (V,),
                   "any live identifier (account ID, live name, ARN, e-mail, OU path) in the fixture",
                   ("T16 #11 d7", "T15 #10 d5")),
    # --- CFG: instance.yml internal form (T22 d1; ADR-0005) ---
    "CFG-FIELDS": _e("CFG", "error", (V,),
                     "field-set violation: missing required field, unknown field, or structure outside the exact T22 d1 set",
                     ("T22 #21 d1", "ADR-0005")),
    "CFG-VOCAB": _e("CFG", "error", (V,),
                    "closed-vocabulary violation: instance_type, delegated_administrator grammar, malformed subtree",
                    ("T22 #21 d1/d2", "ADR-0005")),
    "CFG-REGION": _e("CFG", "error", (V,),
                     "primary_region not us-east-1 or additional_regions not empty",
                     ("T22 #21 d1", "T15 #10 d3", "ADR-0005")),
    "CFG-VERIFICATION": _e("CFG", "error", (V,),
                           "verification block violation: partial block; snapshot_id not 64 lowercase hex; verified_at not RFC 3339 UTC",
                           ("T22 #21 d1", "ADR-0005")),
    # --- DOC: documentation headers (T23 d1-d3) ---
    "DOC-NORMATIVE": _e("DOC", "error", (V,),
                        "normative-header violation",
                        ("T23 #23 d1",)),
    "DOC-INFORMATIVE": _e("DOC", "error", (V,),
                          "informative-header violation (derives_from empty, duplicated, or unresolvable; unknown fields)",
                          ("T23 #23 d2",)),
    "DOC-SCOPE": _e("DOC", "error", (V,),
                    "a file inside the applicability boundary missing its class header, wrong class form, or carrying supersedes",
                    ("T23 #23 d1/d3",)),
    # --- GEN: generated-artifact metadata (T20 d6; detection lands with R3 #28) ---
    "GEN-MANIFEST": _e("GEN", "error", (V, G),
                       "manifest missing, malformed, misordered; digest mismatch; generated artifact absent from the manifest",
                       ("T20 #22 d6",)),
    "GEN-ENVELOPE": _e("GEN", "error", (V, G),
                       "embedded envelope missing, malformed, or misordered where required; whole-target self-digest",
                       ("T20 #22 d6",)),
    "GEN-DRIFT": _e("GEN", "error", (G,),
                    "deterministic regeneration produces different bytes",
                    ("T20 #22 d6",)),
    "GEN-CODEOWNERS": _e("GEN", "error", (V, G),
                         ".github/CODEOWNERS not valid syntax, carrying an embedded envelope, or absent from the manifest",
                         ("T20 #22 d6",)),
    # --- CLS: classification and plan-effect contract (T20; detection lands with R3 #28) ---
    "CLS-UNCOVERED-PATH": _e("CLS", "error", (V, P),
                             "a changed file matching no row of the T20 d2 classification table",
                             ("T20 #22 d2",)),
    "CLS-COMBINATION": _e("CLS", "error", (V, P),
                          "a prohibited class combination",
                          ("T20 #22 d1",)),
    "CLS-UNKNOWN-ACTION": _e("CLS", "error", (P,),
                             "an unknown or unsupported plan-JSON action list",
                             ("T20 #22 d5",)),
    "CLS-UNRESOLVED-VALUE": _e("CLS", "error", (P,),
                               "a sensitive or unknown value prevents a required classification",
                               ("T20 #22 d5",)),
    "CLS-REPRESENTATION": _e("CLS", "error", (P,),
                             "the pinned toolchain emits a different or unsupported representation for a removed-block resource",
                             ("T20 #22 d5", "T21 #20 F8")),
    "CLS-FORGET-PATTERN": _e("CLS", "error", (P,),
                             "a forget row combined with any live-mutation row, or lacking its one-to-one removed block",
                             ("T20 #22 d5",)),
    "CLS-MARKER-MISMATCH": _e("CLS", "error", (P,),
                              "contract-level marker/aggregate inconsistency",
                              ("T20 #22 d5",)),
    "CLS-UNATTRIBUTABLE": _e("CLS", "error", (P,),
                             "a plan effect not attributable to an allowed changed surface of a matched class",
                             ("T20 #22 d1/d5",)),
    "CLS-EFFECT": _e("CLS", "error", (P,),
                     "aggregate effect outside the matched classes' permitted set, including any effect targeting a deferred alias",
                     ("T20 #22 d5", "RD-08", "T16 #11 d8")),
    "CLS-PROTECTED": _e("CLS", "error", (P, A),
                        "any operation on a resource outside the derived POC-managed (ialab-) set or on protected pre-existing resources",
                        ("T15 #10 d7", "T04 #6 d5", "ADR-0009")),
    "CLS-REVOCATION-ACK": _e("CLS", "error", (P,),
                             "an assignment delete effect without the exact-entry access-revocation acknowledgement",
                             ("T20 #22 d3/d5",)),
    # --- ADO: adoption and rehearsal (T19 d2/d21; detection lands with R3 #28) ---
    "ADO-PHASE": _e("ADO", "error", (V,),
                    "any import, moved, or removed block - or other adoption-shaped change - outside an authorized rehearsal phase",
                    ("T19 #14 d2",)),
    "ADO-MANIFEST": _e("ADO", "error", (V,),
                       "adoption-manifest schema violation",
                       ("T19 #14 d21",),
                       state="dormant",
                       activation="Eric's separate authorization of the post-acceptance import-rehearsal phase and the import-redaction gate passing with empirical evidence (T19 d2/d16; T14 #19 C6)"),
}


def validate_catalogue(catalogue=None):
    """Catalogue self-validation (T14 #19 d1/C6/C7): list of defect strings.

    A severity outside the closed vocabulary, a stage outside the closed
    stage set, an unknown state, or a dormant code without its activation
    condition fails validation of the catalogue itself - fail closed.
    """
    table = CATALOGUE if catalogue is None else catalogue
    defects = []
    for code, entry in sorted(table.items()):
        if entry.severity not in SEVERITIES:
            defects.append(
                f"{code}: severity {entry.severity!r} outside the closed vocabulary"
            )
        if not entry.stages:
            defects.append(f"{code}: empty stage list")
        for stage in entry.stages:
            if stage not in STAGES:
                defects.append(f"{code}: stage {stage!r} outside the closed stage set")
        if entry.state not in ("active", "dormant"):
            defects.append(f"{code}: unknown state {entry.state!r}")
        if entry.state == "dormant" and not entry.activation:
            defects.append(f"{code}: dormant without a named activation condition")
        if not entry.rule_ids:
            defects.append(f"{code}: no authority citation")
    return defects
