"""Validation-stage checks for the requester-surface families
KEY / ASN / P-OOS / CFG and the validation arms of INV (R2 #27 row 4).

Canonical triggering layers per T14 #19 d2:
- ASN-* owns everything under account-assignments/**; KEY-* owns groups/,
  permission-sets/, and key-space referential integrity everywhere.
- P-OOS-* is the profile layer (fixed wording, T21 #20 d7); the USER
  specimen intentionally triggers both ASN-SHAPE and P-OOS-USER (T10 d7).
- CFG-* owns instance.yml's internal form only (hermetic); its external
  relationships are PRQ-* at plan/apply.

Residual schema mechanics: T14 #19 dispositions E-SCHEMA / E-YML subsume
schema conformance into the per-family schema codes. On the KEY-owned
surfaces (groups/, permission-sets/) the family exposes facet codes
(KEY-FILENAME, KEY-DESCRIPTION, KEY-IDSTORE-NAME) but no separate shape
code; residual form violations there (unknown fields, missing or malformed
non-facet fields, unparseable YAML) are canonicalized to KEY-GRAMMAR with the
exact defect named in the message - an implementation-level canonicalization
under those dispositions, recorded for the conformance review.

Harmonization (T14 #19 d4 principle): one root cause, one canonical code -
an alias that fails the grammar is rejected at its form layer and not also
resolved against the inventory; a file under an absent-for-slice surface is
rejected by P-OOS-PATH alone and receives no other file check.
"""

from . import grammar, tree

OUT_OF_SLICE_MESSAGE = (
    "out of slice A — not prohibited by the domain architecture"
)

PROFILE_FIELDS_CMP = ("customer_managed_policies",)
PROFILE_FIELDS_BOUNDARY = ("permissions_boundary", "permission_boundary")

EXEMPT_MANAGED_PREFIX = "arn:aws:iam::aws:policy/"

PS_FIELDS = {
    "key", "description", "session_duration", "relay_state",
    "managed_policies", "inline_policy",
}
GROUP_FIELDS = {"key", "identity_store_name", "source"}
INSTANCE_REQUIRED = {
    "instance_type", "primary_region", "additional_regions",
    "identity_source", "delegated_administrator", "owner",
}
INSTANCE_OPTIONAL = {"verification"}
ASSIGNMENT_FIELDS = {"account", "principal", "permission_set"}


def check_out_of_slice(ctx):
    """P-OOS-PATH: the six enumerated absent-for-slice surfaces."""
    m = tree.model(ctx)
    for rel, _surface in m.out_of_slice:
        ctx.emit("P-OOS-PATH", file_path=rel,
                 message=OUT_OF_SLICE_MESSAGE)


def _check_keyed_doc(ctx, doc, bounds, family_dir):
    """Shared stem/key discipline for groups/ and permission-sets/."""
    if doc.parse_error:
        ctx.emit("KEY-GRAMMAR", file_path=doc.rel,
                 message=f"file failing to parse fails its family's schema "
                         f"code ({doc.parse_error})")
        return None
    if not doc.name.endswith(".yml"):
        ctx.emit("KEY-GRAMMAR", file_path=doc.rel,
                 message="governed files carry the .yml extension")
        return None
    body = doc.body
    if not isinstance(body, dict):
        ctx.emit("KEY-GRAMMAR", file_path=doc.rel,
                 message="body is not a mapping")
        return None
    stem_ok = grammar.key_valid(doc.stem, bounds)
    key = body.get("key")
    key_ok = grammar.key_valid(key, bounds)
    if not key_ok:
        ctx.emit("KEY-GRAMMAR", file_path=doc.rel, field_path="/key",
                 message="key violates the grammar or its length bounds")
    if not stem_ok and doc.stem != key:
        # stem == key is one root cause already reported on /key.
        ctx.emit("KEY-GRAMMAR", file_path=doc.rel,
                 message="filename stem violates the key grammar or bounds")
    if stem_ok and key_ok and doc.stem != key:
        ctx.emit("KEY-FILENAME", file_path=doc.rel, field_path="/key",
                 value=key,
                 message="filename stem must equal key exactly")
    return body


def check_groups(ctx):
    m = tree.model(ctx)
    by_name = {}
    by_key = {}
    for doc in m.groups:
        body = _check_keyed_doc(ctx, doc, grammar.GROUP_KEY_BOUNDS,
                                tree.GROUPS_DIR)
        if body is None:
            continue
        unknown = sorted(set(body) - GROUP_FIELDS)
        for field in unknown:
            ctx.emit("KEY-GRAMMAR", file_path=doc.rel, field_path=f"/{field}",
                     message=f"unknown field {field} in a group reference")
        name = body.get("identity_store_name")
        defects = grammar.idstore_name_defects(name)
        for defect in defects:
            ctx.emit("KEY-IDSTORE-NAME", file_path=doc.rel,
                     field_path="/identity_store_name",
                     message=f"identity_store_name: {defect}")
        source = body.get("source")
        if source is not None:
            if (not isinstance(source, dict)
                    or set(source) != {"provider", "group_name"}
                    or not all(isinstance(v, str) and v for v in source.values())):
                ctx.emit("KEY-GRAMMAR", file_path=doc.rel, field_path="/source",
                         message="malformed informational source block")
        if isinstance(name, str) and not defects:
            by_name.setdefault(name, []).append(doc.rel)
        key = body.get("key")
        if isinstance(key, str):
            by_key.setdefault(key, []).append(doc.rel)
    for name, rels in sorted(by_name.items()):
        for rel in rels[1:]:
            ctx.emit("KEY-DUP", file_path=rel,
                     field_path="/identity_store_name", value=name,
                     message="more than one group file per exact "
                             "identity_store_name")
    for key, rels in sorted(by_key.items()):
        for rel in rels[1:]:
            ctx.emit("KEY-DUP", file_path=rel, field_path="/key", value=key,
                     message="duplicate key within groups/")


def _statements(policy):
    statements = policy.get("Statement")
    return statements if isinstance(statements, list) else []


def check_permission_sets(ctx):
    m = tree.model(ctx)
    by_key = {}
    prefix = ctx.config.resource_name_prefix
    for doc in m.permission_sets:
        body = _check_keyed_doc(ctx, doc, grammar.PERMISSION_SET_KEY_BOUNDS,
                                tree.PERMISSION_SETS_DIR)
        if body is None:
            continue
        # Profile layer first: profile-owned fields are canonically P-OOS.
        has_cmp = any(f in body for f in PROFILE_FIELDS_CMP)
        has_boundary = any(f in body for f in PROFILE_FIELDS_BOUNDARY)
        if has_cmp:
            ctx.emit("P-OOS-CMP", file_path=doc.rel,
                     field_path="/customer_managed_policies",
                     message="customer-managed policy reference: "
                             + OUT_OF_SLICE_MESSAGE)
        if has_boundary:
            field = next(f for f in PROFILE_FIELDS_BOUNDARY if f in body)
            ctx.emit("P-OOS-BOUNDARY", file_path=doc.rel,
                     field_path=f"/{field}",
                     message="permission-boundary content: "
                             + OUT_OF_SLICE_MESSAGE)
        profile_fields = set(PROFILE_FIELDS_CMP) | set(PROFILE_FIELDS_BOUNDARY)
        unknown = sorted(set(body) - PS_FIELDS - profile_fields)
        for field in unknown:
            ctx.emit("KEY-GRAMMAR", file_path=doc.rel, field_path=f"/{field}",
                     message=f"unknown field {field} in a permission set")
        description = body.get("description")
        if (not isinstance(description, str) or not 1 <= len(description) <= 700
                or not grammar.DESCRIPTION_RE.match(description)):
            ctx.emit("KEY-DESCRIPTION", file_path=doc.rel,
                     field_path="/description",
                     message="description missing, outside 1-700, or failing "
                             "the documented AWS pattern")
        duration = body.get("session_duration")
        if not isinstance(duration, str) or not grammar.DURATION_RE.match(duration):
            ctx.emit("KEY-GRAMMAR", file_path=doc.rel,
                     field_path="/session_duration",
                     message="session_duration missing or not an ISO-8601 "
                             "duration (required explicitly; no inherited "
                             "defaults - T21 #20 d3)")
        managed = body.get("managed_policies")
        inline = body.get("inline_policy")
        if managed is None and inline is None and not has_cmp:
            ctx.emit("KEY-GRAMMAR", file_path=doc.rel,
                     message="no policy form: exactly one of managed_policies "
                             "or inline_policy is required")
        if managed is not None and inline is not None:
            ctx.emit("P-OOS-POLICY-FORM", file_path=doc.rel,
                     message="both policy forms present: " + OUT_OF_SLICE_MESSAGE)
        if isinstance(managed, list):
            if len(managed) > 1:
                ctx.emit("P-OOS-POLICY-FORM", file_path=doc.rel,
                         field_path="/managed_policies",
                         message="more than one managed_policies entry: "
                                 + OUT_OF_SLICE_MESSAGE)
            for index, entry in enumerate(managed):
                if (not isinstance(entry, str)
                        or not entry.startswith(EXEMPT_MANAGED_PREFIX)):
                    ctx.emit("P-OOS-CMP", file_path=doc.rel,
                             field_path=f"/managed_policies/{index}",
                             message="managed_policies entry outside the "
                                     "partition-qualified AWS-managed "
                                     "vocabulary: " + OUT_OF_SLICE_MESSAGE)
        elif managed is not None:
            ctx.emit("KEY-GRAMMAR", file_path=doc.rel,
                     field_path="/managed_policies",
                     message="managed_policies must be a list")
        if inline is not None:
            if (not isinstance(inline, dict)
                    or not isinstance(inline.get("Version"), str)
                    or not _statements(inline)
                    or not set(inline) <= {"Version", "Id", "Statement"}):
                ctx.emit("KEY-GRAMMAR", file_path=doc.rel,
                         field_path="/inline_policy",
                         message="malformed inline policy document")
        # Composed deployed Name (T05 d1/d3; T15 d8).
        if len(prefix) > grammar.PREFIX_BUDGET:
            ctx.emit("KEY-COMPOSED", file_path=doc.rel, value=prefix,
                     message="prefix budget over 8 characters including its "
                             "delimiter")
        key = body.get("key")
        if grammar.key_valid(key, grammar.PERMISSION_SET_KEY_BOUNDS):
            composed = prefix + key
            if len(composed) > grammar.COMPOSED_NAME_MAX:
                ctx.emit("KEY-COMPOSED", file_path=doc.rel, value=composed,
                         message="composed deployed Name over 32 characters")
            elif not grammar.DEPLOYED_NAME_RE.match(composed):
                ctx.emit("KEY-COMPOSED", file_path=doc.rel, value=composed,
                         message="composed deployed Name fails the AWS Name "
                                 "pattern")
            by_key.setdefault(composed, []).append(doc.rel)
        key2 = body.get("key")
        if isinstance(key2, str):
            pass
    for composed, rels in sorted(by_key.items()):
        for rel in rels[1:]:
            ctx.emit("KEY-PROTECTED", file_path=rel, value=composed,
                     message="deployed-Name collision within desired "
                             "configuration")


def _fixture_accounts(m):
    """alias -> list of entries from the labeled inventory fixture (only
    well-formed entries participate; the FIX checks own the fixture's own
    form)."""
    if m.fixture is None or m.fixture.parse_error or not isinstance(
            m.fixture.body, dict):
        return None
    accounts = m.fixture.body.get("accounts")
    if not isinstance(accounts, list):
        return None
    table = {}
    for entry in accounts:
        if isinstance(entry, dict) and isinstance(entry.get("alias"), str):
            table.setdefault(entry["alias"], []).append(entry)
    return table


def _check_alias_reference(ctx, alias, rel, field_path, accounts):
    """INV validation arms for one alias reference (T09 d19; RD-08)."""
    if accounts is None:
        return
    entries = accounts.get(alias)
    if not entries:
        ctx.emit("INV-ABSENT", file_path=rel, field_path=field_path,
                 value=alias,
                 message="referenced alias absent from the committed fixture")
    elif any(e.get("status") == "requested" for e in entries):
        ctx.emit("INV-DEFERRED", file_path=rel, field_path=field_path,
                 value=alias,
                 message="deferred — referenced account has "
                         "status: requested and is omitted from the "
                         "executable plan (never invalid; RD-08)")


def check_assignments(ctx):
    m = tree.model(ctx)
    accounts = _fixture_accounts(m)
    group_keys = {
        d.body.get("key") for d in m.groups
        if not d.parse_error and isinstance(d.body, dict)
    }
    ps_keys = {
        d.body.get("key") for d in m.permission_sets
        if not d.parse_error and isinstance(d.body, dict)
    }
    for doc in m.assignment_stray:
        ctx.emit("ASN-ACCOUNT-ALIAS", file_path=doc.rel,
                 message="unrecognized directory form: assignments live under "
                         "exactly one account-alias path segment")
    for account_dir, doc in m.assignments:
        tail = doc.rel[len(tree.ASSIGNMENTS_DIR) + 1 :]
        if tail.count("/") != 1:
            ctx.emit("ASN-ACCOUNT-ALIAS", file_path=doc.rel,
                     message="account directory is not exactly one path "
                             "segment")
            continue
        alias_ok = grammar.alias_valid(account_dir)
        if not alias_ok:
            ctx.emit("ASN-ACCOUNT-ALIAS", file_path=doc.rel,
                     message="account-alias form violation in the directory "
                             "segment (grammar; separators; uppercase; "
                             "normalization all rejected)")
        # Filename shape (domain layer).
        shape_ok = True
        if not doc.name.endswith(".yml"):
            ctx.emit("ASN-SHAPE", file_path=doc.rel,
                     message="assignment files carry the .yml extension")
            shape_ok = False
        segments = doc.stem.split("--")
        if len(segments) != 2:
            ctx.emit("ASN-SHAPE", file_path=doc.rel,
                     message="filename is not exactly two keys joined by the "
                             "reserved -- separator")
            shape_ok = False
        else:
            g_seg, p_seg = segments
            if not grammar.key_valid(g_seg, grammar.GROUP_KEY_BOUNDS) or \
                    not grammar.key_valid(p_seg, grammar.PERMISSION_SET_KEY_BOUNDS):
                ctx.emit("ASN-SHAPE", file_path=doc.rel,
                         message="invalid key grammar in the assignment "
                                 "filename")
                shape_ok = False
        if doc.stem.startswith("_"):
            ctx.emit("ASN-SHAPE", file_path=doc.rel,
                     message="underscore-prefixed scope files are not a "
                             "recognized representation")
            shape_ok = False
        # Body shape.
        if doc.parse_error:
            ctx.emit("ASN-SHAPE", file_path=doc.rel,
                     message=f"file failing to parse fails its family's "
                             f"schema code ({doc.parse_error})")
            continue
        body = doc.body
        if not isinstance(body, dict):
            ctx.emit("ASN-SHAPE", file_path=doc.rel,
                     message="body is not a mapping")
            continue
        unknown = sorted(set(body) - ASSIGNMENT_FIELDS)
        for field in unknown:
            ctx.emit("ASN-SHAPE", file_path=doc.rel, field_path=f"/{field}",
                     message=f"unrecognized body field {field}")
        principal = body.get("principal")
        principal_ok = isinstance(principal, dict)
        if not principal_ok or set(principal) != {"type", "group"}:
            ctx.emit("ASN-SHAPE", file_path=doc.rel, field_path="/principal",
                     message="unrecognized principal form")
        ptype = principal.get("type") if principal_ok else None
        if ptype == "USER":
            # The intentional dual-family pair (T10 d7): domain layer +
            # profile layer, distinct citations and remediation horizons.
            ctx.emit("ASN-SHAPE", file_path=doc.rel,
                     field_path="/principal/type",
                     message="no USER representation is defined or reserved")
            ctx.emit("P-OOS-USER", file_path=doc.rel,
                     field_path="/principal/type",
                     message="principal.type USER: " + OUT_OF_SLICE_MESSAGE)
        elif principal_ok and ptype != "GROUP":
            ctx.emit("ASN-SHAPE", file_path=doc.rel,
                     field_path="/principal/type",
                     message="only the two-segment GROUP form is recognized")
        account = body.get("account")
        # Three-way agreement (T10 d3; I-1) - only for parseable shapes.
        if shape_ok and len(segments) == 2:
            g_seg, p_seg = segments
            if isinstance(account, str) and account != account_dir:
                ctx.emit("ASN-AGREEMENT", file_path=doc.rel,
                         field_path="/account", value=account,
                         message="directory and in-file account must be the "
                                 "exact same stable inventory alias")
            group_val = principal.get("group") if principal_ok else None
            if isinstance(group_val, str) and group_val != g_seg:
                ctx.emit("ASN-AGREEMENT", file_path=doc.rel,
                         field_path="/principal/group", value=group_val,
                         message="filename segment 1 must equal "
                                 "principal.group")
            ps_val = body.get("permission_set")
            if isinstance(ps_val, str) and ps_val != p_seg:
                ctx.emit("ASN-AGREEMENT", file_path=doc.rel,
                         field_path="/permission_set", value=ps_val,
                         message="filename segment 2 must equal "
                                 "permission_set")
        # Key-space referential integrity (KEY-DANGLING, T05 d4/d5).
        group_val = principal.get("group") if principal_ok else None
        if isinstance(group_val, str) and grammar.key_valid(
                group_val, grammar.GROUP_KEY_BOUNDS) and group_val not in group_keys:
            ctx.emit("KEY-DANGLING", file_path=doc.rel,
                     field_path="/principal/group", value=group_val,
                     message="assignment references an undefined group key")
        ps_val = body.get("permission_set")
        if isinstance(ps_val, str) and grammar.key_valid(
                ps_val, grammar.PERMISSION_SET_KEY_BOUNDS) and ps_val not in ps_keys:
            ctx.emit("KEY-DANGLING", file_path=doc.rel,
                     field_path="/permission_set", value=ps_val,
                     message="assignment references an undefined "
                             "permission-set key")
        # Inventory reference (INV validation arms) - only for a
        # grammar-valid alias (one root cause, one canonical code).
        if alias_ok and isinstance(account, str) and account == account_dir:
            _check_alias_reference(ctx, account, doc.rel, "/account", accounts)


def check_instance(ctx):
    m = tree.model(ctx)
    doc = m.instance
    if doc is None:
        return
    if doc.parse_error:
        ctx.emit("CFG-FIELDS", file_path=doc.rel,
                 message=f"file failing to parse fails its family's schema "
                         f"code ({doc.parse_error})")
        return
    body = doc.body
    if not isinstance(body, dict):
        ctx.emit("CFG-FIELDS", file_path=doc.rel,
                 message="body is not a mapping")
        return
    for field in sorted(INSTANCE_REQUIRED - set(body)):
        ctx.emit("CFG-FIELDS", file_path=doc.rel, field_path=f"/{field}",
                 message=f"missing required field {field}")
    for field in sorted(set(body) - INSTANCE_REQUIRED - INSTANCE_OPTIONAL):
        ctx.emit("CFG-FIELDS", file_path=doc.rel, field_path=f"/{field}",
                 message=f"unknown field {field}")
    if "instance_type" in body and body["instance_type"] != "organization":
        ctx.emit("CFG-VOCAB", file_path=doc.rel, field_path="/instance_type",
                 value=str(body["instance_type"]),
                 message="closed vocabulary: an account instance is rejected")
    if "primary_region" in body and body["primary_region"] != "us-east-1":
        ctx.emit("CFG-REGION", file_path=doc.rel, field_path="/primary_region",
                 value=str(body["primary_region"]),
                 message="primary_region must equal us-east-1 (T15 #10 d3)")
    if "additional_regions" in body and body["additional_regions"] != []:
        ctx.emit("CFG-REGION", file_path=doc.rel,
                 field_path="/additional_regions",
                 message="additional_regions must equal []")
    source = body.get("identity_source")
    if source is not None:
        if not isinstance(source, dict) or set(source) != {"type"}:
            ctx.emit("CFG-VOCAB", file_path=doc.rel,
                     field_path="/identity_source",
                     message="malformed identity_source subtree structure")
        elif source.get("type") != "identity-center-default":
            ctx.emit("P-OOS-IDENTITY-SOURCE", file_path=doc.rel,
                     field_path="/identity_source/type",
                     value=str(source.get("type")),
                     message="identity_source.type other than "
                             "identity-center-default: " + OUT_OF_SLICE_MESSAGE)
    admin = body.get("delegated_administrator")
    if admin is not None:
        if not grammar.alias_valid(admin):
            ctx.emit("CFG-VOCAB", file_path=doc.rel,
                     field_path="/delegated_administrator",
                     message="delegated_administrator must be an inventory "
                             "alias in the established grammar")
        else:
            _check_alias_reference(ctx, admin, doc.rel,
                                   "/delegated_administrator",
                                   _fixture_accounts(m))
    owner = body.get("owner")
    if owner is not None and not grammar.alias_valid(owner):
        ctx.emit("CFG-VOCAB", file_path=doc.rel, field_path="/owner",
                 message="owner must be a principal key in the established "
                         "grammar")
    verification = body.get("verification")
    if verification is not None:
        if not isinstance(verification, dict):
            ctx.emit("CFG-VERIFICATION", file_path=doc.rel,
                     field_path="/verification",
                     message="verification must be a mapping")
            return
        required = {"verified_at", "snapshot_id"}
        if set(verification) != required:
            ctx.emit("CFG-VERIFICATION", file_path=doc.rel,
                     field_path="/verification",
                     message="verification is structurally all-or-nothing: "
                             "exactly verified_at and snapshot_id")
        snapshot_id = verification.get("snapshot_id")
        if "snapshot_id" in verification and (
                not isinstance(snapshot_id, str)
                or not grammar.SNAPSHOT_ID_RE.match(snapshot_id)):
            ctx.emit("CFG-VERIFICATION", file_path=doc.rel,
                     field_path="/verification/snapshot_id",
                     message="snapshot_id must be exactly 64 lowercase "
                             "hexadecimal characters")
        verified_at = verification.get("verified_at")
        if "verified_at" in verification and not \
                grammar.rfc3339_utc_calendar_valid(verified_at):
            ctx.emit("CFG-VERIFICATION", file_path=doc.rel,
                     field_path="/verification/verified_at",
                     message="verified_at must be the complete, "
                             "calendar-valid RFC 3339 UTC representation "
                             "(fractional seconds accepted when present)")
