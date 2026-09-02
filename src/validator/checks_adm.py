"""ADM - the standing-administrator family (R2 #27 row 5; ADR-0008).

ADM-CAPABLE is the T21 #20 d6 five-rule deterministic, conservative
standing-admin-capability hazard detector - not a complete calculation of
effective AWS permissions. It never subtracts Deny statements and never
relies on permission boundaries, SCPs, RCPs, resource policies, or session
policies to excuse a broad grant.

Rules, exactly as ratified:
1. managed_policies contains the exact AWS-managed AdministratorAccess ARN.
2. After normalizing scalar/list forms and expanding action wildcards
   against the versioned, pinned action catalog, the inline document
   contains an unconditional Allow of all actions over all resources. The
   universal wildcard "*" denotes all actions by normalization alone (T07's
   named minimum, "an unrestricted Allow */*"), so that arm needs no
   catalog; service-scoped wildcard expansion requires valid catalog data.
3. A broad Allow statement uses NotAction or NotResource - fail closed
   (inversion breadth is not computed).
4. The inline document grants unbounded IAM / SSO / Identity Store mutation
   capability, detected against the explicit versioned mutation-action set -
   never a phrase-level heuristic. A finite explicit action list is bounded
   by construction (the accepted valid basis predates the catalogs);
   unboundedness arises through wildcards, whose expansion requires the
   catalogs, and through expanded coverage of a service's complete mutation
   set once the catalogs exist.
5. Any unknown or unsupported broad pattern - fail closed.

Condition-gating boundary (R2 S11 condition C2, documented): the rule-2/4
coverage arms evaluate only unconditional statements with Resource "*" -
rule 2's ratified text says "unconditional" explicitly, and rule 4's
"unbounded" is read the same way. A Condition-gated UNIVERSAL grant
(Action "*" / "*:*") still fails closed via rule 5 (a broad pattern the
detector does not compute conditions for), while a Condition-gated
service-scoped wildcard whose expansion covers a full mutation set is not
flagged - the detector is ratified as deterministic and conservative, not
a complete effective-permissions calculation (T21 #20 d6). Changing this
asymmetry is a behavior change and routes through the halt-don't-decide E1
refinement channel, never through a silent edit here.

ADM-CATALOG (T14 #19 d5, C9): any invocation of rules 2/4 without valid
pinned catalog data - absent, digest-mismatched, schema-unsupported, or
unable to expand a required wildcard - fails closed.

ADM-STANDING (T07 #9 d1/d2): the cross-file condition - an admin-capable
definition combined with a standing workforce GROUP assignment referencing
it (every committed slice-A assignment is standing: durable access persists
until removed by governed PR).
"""

import fnmatch
import hashlib
import json

from . import tree

ADMIN_ARN = "arn:aws:iam::aws:policy/AdministratorAccess"


def _as_list(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return value
    return None


def load_catalogs(ctx):
    """Load and digest-verify the pinned catalogs (spec 7.4).

    Returns (action_catalog, mutation_catalog) or (None, reason)."""
    reference_path = ctx.config.catalog_reference
    if not reference_path.is_file():
        return None, "catalog reference absent"
    try:
        reference = json.loads(reference_path.read_text(encoding="utf-8"))
        pins = reference["catalogs"]
    except Exception:
        return None, "catalog reference unreadable"
    loaded = {}
    for name in ("action-catalog.json", "privileged-mutation-actions.json"):
        pin = pins.get(name)
        path = ctx.config.catalog_dir / name
        if not isinstance(pin, dict) or not path.is_file():
            return None, f"{name} absent or unpinned"
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != pin.get("sha256"):
            return None, f"{name} digest mismatch with the pinned reference"
        try:
            catalog = json.loads(data)
        except ValueError:
            return None, f"{name} unparseable"
        if not isinstance(catalog, dict) or not all(
                isinstance(v, list) and all(isinstance(a, str) for a in v)
                for v in catalog.values()):
            return None, f"{name} schema unsupported"
        loaded[name] = catalog
    return (loaded["action-catalog.json"],
            loaded["privileged-mutation-actions.json"]), None


def _expand(actions, action_catalog):
    """Expand service-scoped wildcards against the action catalog.

    Returns (expanded set, None) or (None, inability reason)."""
    expanded = set()
    for action in actions:
        if action == "*":
            # Universal - handled by the caller before expansion.
            continue
        if ":" not in action:
            return None, f"unexpandable action token {action!r}"
        prefix, name = action.split(":", 1)
        if "*" in action or "?" in action:
            if prefix not in action_catalog or "*" in prefix or "?" in prefix:
                return None, (f"wildcard prefix {prefix!r} outside the "
                              "catalog - expansion inability")
            matches = fnmatch.filter(action_catalog[prefix], name)
            expanded.update(f"{prefix}:{m}" for m in matches)
        else:
            expanded.add(action)
    return expanded, None


def detect(body, catalogs):
    """The five-rule detector over one permission-set definition.

    Returns (capable: bool, catalog_failures: [reason])."""
    managed = body.get("managed_policies")
    if isinstance(managed, list) and ADMIN_ARN in managed:
        return True, []  # rule 1
    inline = body.get("inline_policy")
    if not isinstance(inline, dict):
        return False, []
    statements = inline.get("Statement")
    if not isinstance(statements, list):
        return True, []  # rule 5: unsupported document shape
    catalog_failures = []
    for statement in statements:
        if not isinstance(statement, dict):
            return True, []  # rule 5
        effect = statement.get("Effect")
        if effect == "Deny":
            continue  # never subtracted, never a grant
        if effect != "Allow":
            return True, []  # rule 5: unknown effect
        if "NotAction" in statement or "NotResource" in statement:
            return True, []  # rule 3: fail closed
        actions = _as_list(statement.get("Action"))
        resources = _as_list(statement.get("Resource"))
        if actions is None or resources is None:
            return True, []  # rule 5: unsupported form
        unconditional = "Condition" not in statement
        all_resources = "*" in resources
        if "*" in actions or "*:*" in actions:
            # Rule 2's universal arm - all actions by normalization alone.
            if unconditional and all_resources:
                return True, []
            # A broad pattern the detector cannot excuse - fail closed.
            return True, []  # rule 5
        has_wildcard = any("*" in a or "?" in a for a in actions)
        if not has_wildcard and catalogs is None:
            # Bounded by construction; rule-4 coverage awaits the catalogs.
            continue
        if catalogs is None:
            catalog_failures.append(
                "wildcard expansion invoked without valid catalog data")
            continue
        action_catalog, mutation_catalog = catalogs
        expanded, inability = _expand(actions, action_catalog)
        if inability:
            catalog_failures.append(inability)
            continue
        if unconditional and all_resources:
            # Rule 2 coverage: every catalogued action of every prefix.
            universe = {
                f"{prefix}:{name}"
                for prefix, names in action_catalog.items()
                for name in names
            }
            if universe and universe <= expanded:
                return True, []
            # Rule 4: the complete mutation set of any one service.
            for prefix, names in mutation_catalog.items():
                mutation_set = {f"{prefix}:{name}" for name in names}
                if mutation_set and mutation_set <= expanded:
                    return True, []
    return False, catalog_failures


def check_adm(ctx):
    m = tree.model(ctx)
    catalogs, failure = load_catalogs(ctx)
    capable_keys = set()
    invoked_without_data = []
    for doc in m.permission_sets:
        if doc.parse_error or not isinstance(doc.body, dict):
            continue
        available = catalogs if failure is None else None
        capable, catalog_failures = detect(doc.body, available)
        if capable:
            key = doc.body.get("key")
            if isinstance(key, str):
                capable_keys.add(key)
            ctx.emit("ADM-CAPABLE", file_path=doc.rel,
                     message="admin-capable permission-set definition "
                             "rejected by the T21 #20 d6 hazard detector "
                             "(ADR-0008)")
        for reason in catalog_failures:
            invoked_without_data.append((doc.rel, reason))
    for rel, reason in invoked_without_data:
        detail = failure or reason
        ctx.emit("ADM-CATALOG", file_path=rel,
                 message=f"rules 2/4 fail closed: {detail} - never guess")
    for _account, doc in m.assignments:
        if doc.parse_error or not isinstance(doc.body, dict):
            continue
        principal = doc.body.get("principal")
        if not isinstance(principal, dict) or principal.get("type") != "GROUP":
            continue
        ps_key = doc.body.get("permission_set")
        if ps_key in capable_keys:
            ctx.emit("ADM-STANDING", file_path=doc.rel,
                     field_path="/permission_set", value=ps_key,
                     message="standing workforce GROUP assignment references "
                             "an admin-capable definition (T07 #9 d1/d2; "
                             "ADR-0008)")
