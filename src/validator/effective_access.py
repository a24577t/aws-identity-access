"""The effective-access generator - one generator, two renderings
(R3 #28 row 10; T20 #22 d3/d4).

- render_preview: the sanitized, fixture-alias-only, snapshot-blind PR
  rendering. Non-authoritative and NEVER apply-eligible under any
  circumstance (T15 #10 d15; T09 #12 d15): it derives from the governed
  configuration and the committed fixture alone - no snapshot, no clock, no
  plan bytes are read in preview mode.
- render_summary: the authoritative digest-bound rendering, derived
  deterministically from the same row model plus the explicit plan-context
  input (the exact applicable saved-plan facts the pipeline supplies).
  Its SHA-256 over the exact serialized bytes is the sanitized-summary
  digest of the authorization binding (T06 #8 d4).

Both renderings come from the one row model below, so preview and summary
semantics cannot drift (T20 d4). Identical inputs produce identical bytes:
sorted traversal, no wall-clock, LF, UTF-8.

Identifier boundary (T20 #22 d3, serialization-time): every account-local,
generated, or live identifier is omitted or replaced BEFORE public
serialization - sanitize_public_text runs over every rendered line, the
single permitted ARN-shaped vocabulary being the partition-qualified
AWS-managed-policy pattern; a final whole-document scan fails closed if any
leak-shaped token survived. Terraform sensitivity markings are never
treated as sufficient redaction.
"""

import hashlib
import re

from . import checks_governance, classifier, grammar, leak, runner, tree
from .checks_access import _fixture_accounts

GENERATOR_VERSION = "1"
BOUNDARY_CONSTANT = "absent for slice A"

# The specification 8.1 pins the summary must surface (T15 #10 d13).
PINS = (
    ("terraform", "1.15.7"),
    ("hashicorp/aws", "= 6.53.0"),
    ("container",
     "python:3.12.7-slim@sha256:60d9996b6a8a3689d36db740b49f4327be3be09a2"
     "1122bd02fb8895abb38b50d"),
)

OMITTED = "[omitted]"


def sanitize_public_text(text):
    """Omission/replacement redaction over one public line (T20 d3): every
    leak-shaped token is replaced with the fixed sentinel; the exempt
    AWS-managed-policy vocabulary passes through unchanged."""

    def replace_arn(match):
        token = match.group(0)
        return token if leak.EXEMPT_ARN.match(token) else OMITTED

    out = text
    for kind, pattern in leak._PATTERNS:
        if kind == "arn":
            out = pattern.sub(replace_arn, out)
        elif kind in leak._NEEDS_DIGIT:
            out = pattern.sub(
                lambda m: m.group(0)
                if not any(c.isdigit() for c in m.group(0)) else OMITTED,
                out,
            )
        else:
            out = pattern.sub(OMITTED, out)
    return out


def _assert_public(blob_text):
    """Fail closed if any leak-shaped token survived sanitization."""
    scrubbed = blob_text.replace(OMITTED, "")
    for line_no, kind, _token in leak.scan_text(scrubbed):
        raise RuntimeError(
            f"public serialization aborted: {kind}-shaped identifier "
            f"survived sanitization at line {line_no}"
        )


def _policy_form(body):
    managed = body.get("managed_policies")
    if isinstance(managed, list) and managed:
        return str(managed[0])
    inline = body.get("inline_policy")
    if isinstance(inline, dict):
        statements = inline.get("Statement")
        count = len(statements) if isinstance(statements, list) else 0
        return f"inline policy ({count} statement{'s' if count != 1 else ''})"
    return "no policy form"


def _reviewers_for(ctx, rel, accounts):
    """The routing-derived review classes and satisfying principals for one
    governed path (T06 #8 d1-d3)."""
    found = checks_governance._routes(ctx)
    if found is None:
        return "unroutable - fail closed"
    _doc, routes = found
    _principals, classes = checks_governance._registry(ctx)
    m = tree.model(ctx)
    class_principals = {}
    for doc in m.review_classes:
        if not doc.parse_error and isinstance(doc.body, dict):
            key = doc.body.get("key")
            satisfied = doc.body.get("satisfied_by")
            if isinstance(key, str) and isinstance(satisfied, list):
                class_principals[key] = [str(p) for p in satisfied]
    required = set()
    for route, regex in ((r, checks_governance._route_regex(r["path"]))
                         for r in routes
                         if isinstance(r, dict) and isinstance(r.get("path"), str)):
        if not regex.match(rel):
            continue
        declared = route.get("review_classes")
        if isinstance(declared, list):
            required.update(str(c) for c in declared)
        elif route.get("resolution") == "account-delegation":
            match = checks_governance.ASSIGNMENT_PATH_RE.match(rel)
            if match and accounts:
                entries = accounts.get(match.group(1)) or []
                if entries:
                    classification = entries[0].get("intended_classification")
                    if classification and classification != "none" \
                            and classification in classes:
                        required.add(str(classification))
    parts = []
    for cls in sorted(required):
        principals = ", ".join(sorted(class_principals.get(cls, ()))) or "-"
        parts.append(f"{cls} (satisfied by: {principals})")
    return "; ".join(parts) if parts else "none derived"


def _rows(ctx):
    """The shared row model both renderings derive from (T20 d3's ten
    fields per row, instantiated for slice A)."""
    m = tree.model(ctx)
    accounts = _fixture_accounts(m)
    ps_bodies = {}
    for doc in m.permission_sets:
        if not doc.parse_error and isinstance(doc.body, dict):
            key = doc.body.get("key")
            if isinstance(key, str):
                ps_bodies[key] = doc.body
    prefix = ctx.config.resource_name_prefix
    rows = []
    deferred = []
    for _account_dir, doc in sorted(m.assignments, key=lambda t: t[1].rel):
        if doc.parse_error or not isinstance(doc.body, dict):
            continue
        body = doc.body
        alias = body.get("account")
        group = (body.get("principal") or {}).get("group") \
            if isinstance(body.get("principal"), dict) else None
        ps_key = body.get("permission_set")
        if not all(isinstance(v, str) for v in (alias, group, ps_key)):
            continue
        ps = ps_bodies.get(ps_key, {})
        entry_list = (accounts or {}).get(alias) or []
        is_deferred = any(e.get("status") == "requested" for e in entry_list)
        if is_deferred:
            deferred.append(alias)
        rows.append({
            "principal": group,
            "permission_set": ps_key,
            "policy": _policy_form(ps),
            "target": alias,
            "session_duration": str(ps.get("session_duration", "-")),
            "lifecycle": ("deferred" if is_deferred
                          else "standing - until changed by governed PR"),
            "portal": (prefix + ps_key
                       if grammar.key_valid(
                           ps_key, grammar.PERMISSION_SET_KEY_BOUNDS)
                       else "-"),
            "reviewers": _reviewers_for(ctx, doc.rel, accounts),
        })
    return rows, sorted(set(deferred))


def _render_row_block(out, row, action):
    out.append(f"- action: {action}")
    out.append(f"  principal: {row['principal']}")
    out.append(f"  permission: {row['permission_set']} - {row['policy']}")
    out.append(f"  target account: {row['target']}")
    out.append(f"  session duration: {row['session_duration']}")
    out.append(f"  permission boundary: {BOUNDARY_CONSTANT}")
    out.append(f"  persistence/lifecycle: {row['lifecycle']}")
    out.append(f"  AWS access portal effect: {row['portal']}")
    out.append(f"  required reviewers: {row['reviewers']}")


def _finish(out):
    text = "\n".join(sanitize_public_text(line) for line in out) + "\n"
    _assert_public(text)
    return text.encode("utf-8")


def render_preview(target, config):
    """The sanitized plan-preview rendering (fixture-alias-only,
    snapshot-blind, never apply-eligible)."""
    ctx = runner.Context("validation", target, config)
    rows, deferred = _rows(ctx)
    out = [
        "# Effective-access plan preview",
        "",
        "authority: none - sanitized preview; never apply-eligible "
        "(T15 #10 d15)",
        "inputs: governed configuration and the committed fixture only "
        "(snapshot-blind)",
        "",
        "## Change rows",
        "",
        "standing configuration (no authoritative plan in preview mode)",
        "",
    ]
    for row in rows:
        _render_row_block(out, row, "standing (validated configuration)")
        out.append("")
    out.append("## Deferred targets")
    out.append("")
    if deferred:
        for alias in deferred:
            out.append(f"- {alias}: deferred - reported deferred, "
                       "never rejected (RD-08)")
    else:
        out.append("none")
    return _finish(out)


def render_summary(target, config):
    """The digest-bound effective-access summary, derived from the same row
    model plus the explicit plan-context input."""
    from .checks_plan import _context as load_context

    ctx = runner.Context("plan", target, config)
    plan = load_context(ctx) or {}
    rows, deferred = _rows(ctx)
    section = plan.get("plan") or {}
    changes = [r for r in section.get("resource_changes") or []
               if isinstance(r, dict)]
    out = [
        "# Effective-access summary",
        "",
        "authority: the digest of these exact bytes binds the apply "
        "authorization (T06 #8 d4)",
        "",
        "## Binding",
        "",
        f"- snapshot_id: {plan.get('current_pointer', '-')}",
    ]
    fixture_path = ctx.config.inventory_fixture
    if fixture_path is not None:
        from pathlib import Path

        digest = hashlib.sha256(Path(fixture_path).read_bytes()).hexdigest()
        out.append(f"- fixture digest: {digest}")
    for name, value in PINS:
        out.append(f"- pin {name}: {value}")
    out.extend(["", "## Plan effects", ""])
    mutations = []
    reads = []
    for row in changes:
        cls = classifier.action_class((row.get("change") or {}).get("actions"))
        address = str(row.get("address"))
        if cls == "read":
            reads.append(address)
        elif cls not in (None, "no-op"):
            mutations.append((address, cls))
    if mutations:
        for address, cls in sorted(mutations):
            out.append(f"- {cls}: {address}")
    else:
        out.append("none (empty aggregate)")
    out.extend(["", "## Read-only refresh (listed, never mutation)", ""])
    if reads:
        out.extend(f"- {address}" for address in sorted(reads))
    else:
        out.append("none")
    out.extend(["", "## Standing effective access", ""])
    for row in rows:
        _render_row_block(out, row, "standing")
        out.append("")
    out.append("## Deferred targets")
    out.append("")
    if deferred:
        out.extend(f"- {alias}: deferred (RD-08)" for alias in deferred)
    else:
        out.append("none")
    out.extend(["", "## Enforcement evidence", ""])
    enforcement = [e for e in plan.get("enforcement") or ()
                   if isinstance(e, dict)]
    if enforcement:
        for entry in sorted(enforcement, key=lambda e: str(e.get("control"))):
            control = sanitize_public_text(str(entry.get("control")))
            result = sanitize_public_text(str(entry.get("result")))
            exception = ("; current lab exception"
                         if entry.get("lab_exception_current") else "")
            out.append(f"- {control}: {result}{exception}")
    else:
        out.append("none supplied")
    return _finish(out)


def summary_digest(blob):
    """The sanitized-summary digest of the authorization binding."""
    return hashlib.sha256(blob).hexdigest()
