"""The plan/apply-stage battery (R2 #27 row 4): INV snapshot/live
verification (T09 #12 d4-d5, d10-d13, d18-d19), the PRQ prerequisite gate
(T22 #21 d3/d4; ADR-0006), the KEY-PROTECTED pre-existing arm (T05 #7 d5;
T15 #10 d8; ADR-0009), and the plan-side GOV codes (T06 #8 d3/d5).

Plan and apply own the clock, snapshot, evidence, and AWS-derived facts
(T22 #21 d4). This validator core never contacts AWS: the stage's facts
arrive as the explicit plan-context input - a mapping (or JSON file path)
with the shape documented below - and the pipeline wiring that populates it
from the live read APIs is CI work (R4 #29). Fixtures supply it synthetically
with a controlled clock (T14 #19 d6/C10).

Plan-context shape (all synthetic-safe; every field explicit):
  clock: RFC 3339 UTC string - the stage's controlled clock
  snapshot: null | {envelope: {snapshot_id, body}, object_key_id,
            metadata_id, sidecar_id}
  current_pointer: null | 64-hex; pointer_changed: bool
  live: {accounts: [{Id, Name, State, ParentOuId}], pagination_complete,
         api_error, lab_ou_account_ids, organization, identity_center,
         permission_set_names, groups, prerequisites}
  attestations: [{characteristic, snapshot_id, valid}]
  enforcement: [{control, result, lab_exception_current}]
  review_events: [{event, identity, class}]; co_satisfaction_rule: bool
  trusted_base_declarations: [declaration keys merged into the trusted base]
  operation: null | the attempted exceptional operation (GOV-DECL-MATCH)

Harmonization (T14 #19 d4a): defects of the snapshot artifact itself emit
the canonical INV code; PRQ-SNAPSHOT covers only instance.yml's reference or
binding to that artifact, carries related_inv context in its message, and is
suppressed when the snapshot surface itself owns the root cause.
"""

import hashlib
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

from . import grammar, tree
from .checks_access import _fixture_accounts
from .checks_governance import DECLARATION_KINDS

BACKSTOP_DAYS = 90

BOUND_ENTRY_FIELDS = {
    "alias", "live_name", "account_id", "state", "joined_method",
    "joined_timestamp", "ou", "tags_verified",
}
_EMAIL_RE = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$"
)
_ARN_RE = re.compile(r"^arn:")


class CanonicalizationError(Exception):
    pass


def jcs_digest(value):
    """RFC 8785 canonical digest for the snapshot body's value domain
    (objects, arrays, strings, integers, booleans, null). Floats and any
    non-string keys fail closed (I-JSON constraints; T09 #12 d4/d6)."""

    def render(node):
        if node is None or node is True or node is False:
            return json.dumps(node)
        if isinstance(node, str):
            return json.dumps(node, ensure_ascii=False)
        if isinstance(node, int):
            return str(node)
        if isinstance(node, float):
            raise CanonicalizationError("non-integer number in body")
        if isinstance(node, list):
            return "[" + ",".join(render(item) for item in node) + "]"
        if isinstance(node, dict):
            if any(not isinstance(k, str) for k in node):
                raise CanonicalizationError("non-string object key")
            parts = []
            for key in sorted(node):
                parts.append(
                    json.dumps(key, ensure_ascii=False) + ":" + render(node[key])
                )
            return "{" + ",".join(parts) + "}"
        raise CanonicalizationError(f"unsupported value type {type(node)!r}")

    return hashlib.sha256(render(value).encode("utf-8")).hexdigest()


def _parse_ts(value):
    if not isinstance(value, str) or not grammar.RFC3339_UTC_RE.match(value):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _context(ctx):
    raw = ctx.config.plan_context
    if isinstance(raw, (str, Path)):
        with open(raw, encoding="utf-8") as fh:
            raw = json.load(fh)
    return raw


def _referenced_aliases(ctx):
    """(alias, rel, field_path) references from assignments and
    instance.yml, exactly as the validation stage sees them."""
    m = tree.model(ctx)
    refs = []
    for account_dir, doc in m.assignments:
        if not doc.parse_error and isinstance(doc.body, dict):
            account = doc.body.get("account")
            if isinstance(account, str) and account == account_dir \
                    and grammar.alias_valid(account):
                refs.append((account, doc.rel, "/account"))
    if m.instance and not m.instance.parse_error and isinstance(
            m.instance.body, dict):
        admin = m.instance.body.get("delegated_administrator")
        if isinstance(admin, str) and grammar.alias_valid(admin):
            refs.append((admin, m.instance.rel, "/delegated_administrator"))
    return refs


def check_plan_stage(ctx):
    plan = _context(ctx)
    if not isinstance(plan, dict):
        return
    clock = _parse_ts(plan.get("clock"))
    m = tree.model(ctx)
    accounts_table = _fixture_accounts(m)
    snapshot = plan.get("snapshot")
    pointer = plan.get("current_pointer")
    live = plan.get("live") or {}

    snapshot_surface_defect = False

    # --- Snapshot artifact surface (canonical INV codes) ---
    body = None
    if snapshot is None or pointer is None:
        ctx.emit("INV-MISSING",
                 message="no snapshot or current pointer")
        snapshot_surface_defect = True
    else:
        envelope = snapshot.get("envelope") or {}
        body = envelope.get("body")
        if plan.get("pointer_changed"):
            ctx.emit("INV-STALE",
                     message="current pointer changed during verification")
            snapshot_surface_defect = True
        discovered = _parse_ts((body or {}).get("discovered_at"))
        if clock and discovered and \
                clock - discovered > timedelta(days=BACKSTOP_DAYS):
            ctx.emit("INV-STALE",
                     message="snapshot beyond the 90-day backstop from "
                             "discovered_at (T09 #12 d10)")
            snapshot_surface_defect = True
        try:
            recomputed = jcs_digest(body)
        except CanonicalizationError as exc:
            ctx.emit("INV-DIGEST",
                     message=f"canonicalization or I-JSON failure: {exc}")
            snapshot_surface_defect = True
            recomputed = None
        if recomputed is not None:
            locations = {
                "envelope snapshot_id": envelope.get("snapshot_id"),
                "object key": snapshot.get("object_key_id"),
                "S3 metadata": snapshot.get("metadata_id"),
                "sidecar": snapshot.get("sidecar_id"),
            }
            for name, value in sorted(locations.items()):
                if value != recomputed:
                    ctx.emit("INV-DIGEST",
                             message=f"digest disagreement at the {name}")
                    snapshot_surface_defect = True
            if ctx.config.inventory_fixture is not None and body:
                fixture_digest = hashlib.sha256(
                    Path(ctx.config.inventory_fixture).read_bytes()
                ).hexdigest()
                declared = (body.get("fixture") or {}).get("digest")
                if declared != fixture_digest:
                    ctx.emit("INV-DIGEST",
                             message="fixture-digest mismatch with the "
                                     "committed fixture bytes")
                    snapshot_surface_defect = True

    # --- Boundary checks (INV-BOUNDARY) ---
    if body:
        _check_boundary(ctx, body, live, m)
        _check_prohibited(ctx, body, accounts_table)
        _check_bindings(ctx, body, live, accounts_table)

    if live:
        if live.get("pagination_complete") is False or live.get("api_error"):
            ctx.emit("INV-PARTIAL",
                     message="incomplete pagination or API error during live "
                             "verification; retry within the run")

    # --- Referenced aliases (plan arms of INV-ABSENT / INV-DEFERRED) ---
    if accounts_table is not None:
        for alias, rel, field_path in _referenced_aliases(ctx):
            entries = accounts_table.get(alias)
            if not entries:
                ctx.emit("INV-ABSENT", file_path=rel, field_path=field_path,
                         value=alias,
                         message="referenced alias absent from the consumed "
                                 "inventory")
            elif any(e.get("status") == "requested" for e in entries):
                ctx.emit("INV-DEFERRED", file_path=rel, field_path=field_path,
                         value=alias,
                         message="deferred — requested account omitted from "
                                 "the executable plan (never invalid; RD-08)")

    # --- PRQ battery ---
    _check_prerequisites(ctx, plan, m, pointer, body,
                         snapshot_surface_defect, live)

    # --- KEY-PROTECTED pre-existing arm ---
    existing = set(live.get("permission_set_names") or ())
    if existing:
        prefix = ctx.config.resource_name_prefix
        for doc in m.permission_sets:
            if doc.parse_error or not isinstance(doc.body, dict):
                continue
            key = doc.body.get("key")
            if isinstance(key, str):
                composed = prefix + key
                if composed in existing:
                    ctx.emit("KEY-PROTECTED", file_path=doc.rel,
                             value=composed,
                             message="deployed-Name collision with a "
                                     "pre-existing permission set - "
                                     "protected-resource error, never "
                                     "silently imported, adopted, renamed, "
                                     "suffixed, or overwritten")

    # --- GOV plan codes ---
    _check_enforcement(ctx, plan)
    _check_approval_classes(ctx, plan)
    _check_declaration_match(ctx, plan, m, clock)


def _check_boundary(ctx, body, live, m):
    if body.get("schema_version") != 1:
        ctx.emit("INV-BOUNDARY", field_path="/schema_version",
                 message="body.schema_version must equal 1 (T09 #12 d5)")
    if body.get("kind") != "lab-binding-snapshot":
        ctx.emit("INV-BOUNDARY", field_path="/kind",
                 message="body.kind must equal lab-binding-snapshot")
    org = body.get("organization") or {}
    live_org = live.get("organization") or {}
    for field, live_field in (("organization_id", "organization_id"),
                              ("root_id", "root_id")):
        if live_org and org.get(field) != live_org.get(live_field):
            ctx.emit("INV-BOUNDARY", field_path=f"/organization/{field}",
                     message="authoritative organization boundary mismatch")
    ic = body.get("identity_center") or {}
    live_ic = live.get("identity_center") or {}
    for field in ("instance_arn", "identity_store_id"):
        if live_ic and ic.get(field) != live_ic.get(field):
            ctx.emit("INV-BOUNDARY", field_path=f"/identity_center/{field}",
                     message="authoritative Identity Center boundary mismatch")
    # Regional authority: instance.yml prevails (T09 #12 d5).
    if m.instance and not m.instance.parse_error and isinstance(
            m.instance.body, dict):
        declared_region = m.instance.body.get("primary_region")
        if ic.get("region") != declared_region:
            ctx.emit("INV-BOUNDARY", field_path="/identity_center/region",
                     message="snapshot region projection must equal "
                             "instance.yml primary_region - instance.yml is "
                             "the regional authority")


def _check_prohibited(ctx, body, accounts_table):
    """INV-PROHIBITED-FIELD (T09 #12 d5/d12): prohibited content in the
    snapshot body; a requested entry bound or carrying live fields."""
    instance_arn = (body.get("identity_center") or {}).get("instance_arn")
    requested_aliases = set()
    if accounts_table:
        for alias, entries in accounts_table.items():
            if any(e.get("status") == "requested" for e in entries):
                requested_aliases.add(alias)

    def walk(node, pointer):
        if isinstance(node, dict):
            for key in sorted(node):
                if key == "Status":
                    ctx.emit("INV-PROHIBITED-FIELD",
                             field_path=f"{pointer}/{key}",
                             message="the retired Status field is never read "
                                     "or stored")
                    continue
                walk(node[key], f"{pointer}/{key}")
        elif isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{pointer}/{index}")
        elif isinstance(node, str):
            if _EMAIL_RE.match(node):
                ctx.emit("INV-PROHIBITED-FIELD", field_path=pointer,
                         message="e-mail address in the snapshot body")
            elif _ARN_RE.match(node) and node != instance_arn:
                ctx.emit("INV-PROHIBITED-FIELD", field_path=pointer,
                         message="non-instance ARN in the snapshot body")

    walk(body, "")
    for index, entry in enumerate(body.get("accounts") or []):
        if not isinstance(entry, dict):
            continue
        alias = entry.get("alias")
        if alias in requested_aliases:
            if entry.get("binding") != "unbound" or \
                    set(entry) != {"alias", "binding"}:
                ctx.emit("INV-PROHIBITED-FIELD",
                         field_path=f"/accounts/{index}",
                         message="a requested entry must remain unbound and "
                                 "carry no live fields")


def _check_bindings(ctx, body, live, accounts_table):
    """T09 #12 d11 uniqueness and state checks over bindings and live."""
    entries = [e for e in (body.get("accounts") or []) if isinstance(e, dict)]
    bound = {}
    seen_ids = {}
    seen_names = {}
    seen_aliases = {}
    for entry in entries:
        alias = entry.get("alias")
        if entry.get("binding") == "unbound":
            continue
        if isinstance(alias, str):
            seen_aliases.setdefault(alias, []).append(entry)
            bound[alias] = entry
        account_id = entry.get("account_id")
        if isinstance(account_id, str):
            seen_ids.setdefault(account_id, []).append(alias)
        name = entry.get("live_name")
        if isinstance(name, str):
            seen_names.setdefault(name, []).append(alias)
    for table, label in ((seen_aliases, "alias"), (seen_ids, "account id"),
                         (seen_names, "live name")):
        for value, hits in sorted(table.items()):
            if len(hits) > 1:
                ctx.emit("INV-DUP",
                         message=f"duplicate {label} binding in the snapshot")
    live_accounts = [a for a in (live.get("accounts") or ())
                     if isinstance(a, dict)]
    live_by_id = {}
    for account in live_accounts:
        live_by_id.setdefault(account.get("Id"), []).append(account)
    if accounts_table:
        for alias in sorted(accounts_table):
            if any(e.get("status") == "requested"
                   for e in accounts_table[alias]):
                continue
            entry = bound.get(alias)
            if entry is None:
                ctx.emit("INV-UNBOUND", value=alias,
                         message="active alias without a live binding in the "
                                 "binding snapshot")
                continue
            matches = live_by_id.get(entry.get("account_id"), [])
            if len(matches) != 1:
                ctx.emit("INV-BOUNDARY", value=alias,
                         message="bound account does not appear exactly once "
                                 "in the live listing")
                continue
            (account,) = matches
            if account.get("State") != "ACTIVE":
                ctx.emit("INV-STATE", value=alias,
                         message="bound account State is not ACTIVE "
                                 "(Status is never read)")
            if account.get("Name") != entry.get("live_name"):
                ctx.emit("INV-RENAME", value=alias,
                         message="live Name differs from live_name - names "
                                 "are immutable once active (OD-12)")
            declared_ou = (entry.get("ou") or {}).get("ou_id")
            if account.get("ParentOuId") != declared_ou:
                ctx.emit("INV-OU", value=alias,
                         message="live parent OU differs from ou_id")
    bound_ids = {e.get("account_id") for e in bound.values()}
    lab_ou_ids = set(live.get("lab_ou_account_ids") or ())
    for account in live_accounts:
        if account.get("Id") in lab_ou_ids and \
                account.get("Id") not in bound_ids:
            ctx.emit("INV-UNALIASED",
                     message="unaliased live account discovered in the "
                             "governed lab OU - never a permissive fallback")


def _check_prerequisites(ctx, plan, m, pointer, body,
                         snapshot_surface_defect, live):
    if m.instance is None or m.instance.parse_error or not isinstance(
            m.instance.body, dict):
        return
    verification = m.instance.body.get("verification")
    if not isinstance(verification, dict):
        ctx.emit("PRQ-MISSING", file_path=m.instance.rel,
                 message="committed verification block absent - unverified "
                         "prerequisites block plan and apply")
    elif not snapshot_surface_defect and pointer is not None:
        reference = verification.get("snapshot_id")
        if reference != pointer:
            ctx.emit("PRQ-SNAPSHOT", file_path=m.instance.rel,
                     field_path="/verification/snapshot_id",
                     message="verification reference does not name the "
                             "current snapshot (related_inv: INV-STALE)")
        elif body is not None:
            verified_at = verification.get("verified_at")
            if verified_at != body.get("discovered_at"):
                ctx.emit("PRQ-SNAPSHOT", file_path=m.instance.rel,
                         field_path="/verification/verified_at",
                         message="verified_at is not byte-equal to the "
                                 "referenced snapshot's discovered_at")
    prerequisites = (live.get("prerequisites") or {})
    if prerequisites.get("instance") not in (None, "pass"):
        ctx.emit("PRQ-INSTANCE",
                 message="API-verifiable instance presence/type failure")
    if prerequisites.get("identity_store") not in (None, "pass"):
        ctx.emit("PRQ-IDENTITY-STORE",
                 message="identity-store binding failure")
    admin_failed = prerequisites.get("delegated_admin") not in (None, "pass")
    service = (live.get("identity_center") or {}).get(
        "delegated_admin_service")
    if admin_failed or (service is not None
                        and service != "sso.amazonaws.com"):
        ctx.emit("PRQ-DELEGATED-ADMIN",
                 message="sso.amazonaws.com-scoped delegated-administrator "
                         "registration failure")
    for index, attestation in enumerate(plan.get("attestations") or ()):
        if not isinstance(attestation, dict):
            continue
        if not attestation.get("valid") or (
                pointer is not None
                and attestation.get("snapshot_id") != pointer):
            ctx.emit("PRQ-ATTESTATION", field_path=f"/attestations/{index}",
                     message="missing, stale, mismatched, or invalid human "
                             "attestation")
    groups = live.get("groups")
    if groups is not None:
        for doc in m.groups:
            if doc.parse_error or not isinstance(doc.body, dict):
                continue
            name = doc.body.get("identity_store_name")
            if not isinstance(name, str):
                continue
            result = groups.get(name)
            if (not isinstance(result, dict) or not result.get("resolved")
                    or result.get("multiple")
                    or not result.get("display_name_exact")):
                ctx.emit("PRQ-GROUP", file_path=doc.rel,
                         field_path="/identity_store_name",
                         message="referenced-group resolution failure "
                                 "(GetGroupId with exact-DisplayName "
                                 "verification; never created, never "
                                 "deferred - ADR-0007)")


def _check_enforcement(ctx, plan):
    for index, entry in enumerate(plan.get("enforcement") or ()):
        if not isinstance(entry, dict):
            continue
        result = entry.get("result")
        current = bool(entry.get("lab_exception_current"))
        if result in ("unenforced", "unknown", "lab-exception") and not current:
            ctx.emit("GOV-ENFORCEMENT", field_path=f"/enforcement/{index}",
                     value=str(entry.get("control")),
                     message="required control unenforced/unknown without a "
                             "current applicable lab exception")


def _check_approval_classes(ctx, plan):
    if plan.get("co_satisfaction_rule"):
        return
    by_event = {}
    by_identity = {}
    for event in plan.get("review_events") or ():
        if not isinstance(event, dict):
            continue
        cls = event.get("class")
        by_event.setdefault(event.get("event"), set()).add(cls)
        by_identity.setdefault(event.get("identity"), set()).add(cls)
    for label, table in (("review event", by_event),
                         ("physical identity", by_identity)):
        for key, classes in sorted(table.items(), key=lambda kv: str(kv[0])):
            if len(classes) > 1:
                ctx.emit("GOV-APPROVAL-CLASS", value=str(key),
                         message=f"one {label} counted toward more than one "
                                 "independently required class without an "
                                 "accepted co-satisfaction rule")
                break


def _declared_keys(body):
    kind = body.get("kind")
    if kind == "principal-replacement":
        return [body.get("group_key")]
    return [body.get("from_key"), body.get("to_key")]


def _check_declaration_match(ctx, plan, m, clock):
    operation = plan.get("operation")
    if not isinstance(operation, dict):
        return
    trusted = set(plan.get("trusted_base_declarations") or ())
    kind = operation.get("kind")
    if kind not in DECLARATION_KINDS:
        ctx.emit("GOV-DECL-MATCH", value=str(kind),
                 message="attempted exceptional operation with an unknown "
                         "declaration kind")
        return
    candidates = []
    for doc in m.declarations:
        if doc.parse_error or not isinstance(doc.body, dict):
            continue
        body = doc.body
        if doc.stem not in trusted:
            continue
        if body.get("kind") != kind:
            continue
        if kind == "permission-set-key-replacement" and \
                body.get("phase") != operation.get("phase"):
            continue
        if sorted(map(str, _declared_keys(body))) != \
                sorted(map(str, operation.get("keys") or ())):
            continue
        declared_paths = set(body.get("affected_paths") or ())
        if not set(operation.get("paths") or ()) <= declared_paths:
            continue
        if operation.get("environment") != body.get("deployment_scope"):
            continue
        candidates.append(doc)
    if not candidates:
        ctx.emit("GOV-DECL-MATCH",
                 message="no matching declaration merged into the trusted "
                         "base - a declaration on the change branch is "
                         "intent-under-review, never active authorization")
        return
    if len(candidates) > 1:
        ctx.emit("GOV-DECL-MATCH",
                 message="multiple matching current declarations")
        return
    (doc,) = candidates
    body = doc.body
    valid_from = _parse_ts(body.get("valid_from"))
    valid_until = _parse_ts(body.get("valid_until"))
    if clock is None or valid_from is None or valid_until is None or \
            not valid_from <= clock <= valid_until:
        ctx.emit("GOV-DECL-MATCH", file_path=doc.rel,
                 message="declaration expired or not yet valid - expired "
                         "declarations fail closed")
    if operation.get("effect_class") != body.get("expected_plan_effect_class"):
        ctx.emit("GOV-DECL-MATCH", file_path=doc.rel,
                 value=str(operation.get("effect_class")),
                 message="plan effects outside the authorized shape")
    if operation.get("group_id_changed") and kind != "principal-replacement":
        ctx.emit("GOV-DECL-MATCH", file_path=doc.rel,
                 message="a GroupId change without the principal-replacement "
                         "kind is principal replacement, not a rename")
    if kind == "group-key-rename" and \
            (operation.get("aws_mutation_rows") or 0) > 0:
        ctx.emit("GOV-DECL-MATCH", file_path=doc.rel,
                 message="a group-key-rename plan must contain zero AWS "
                         "mutations")
    if kind == "permission-set-key-replacement":
        if operation.get("phase") == "introduce" and \
                (operation.get("delete_rows") or 0) > 0:
            ctx.emit("GOV-DECL-MATCH", file_path=doc.rel,
                     message="an introduce plan contains only creates - no "
                             "deletes or replacements")
        if operation.get("phase") == "retire" and \
                not operation.get("introduce_completion_verified"):
            ctx.emit("GOV-DECL-MATCH", file_path=doc.rel,
                     message="retirement without verified introduce-phase "
                             "completion evidence")
