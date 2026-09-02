"""Validation-stage checks for the FIX and GOV families, the fixture-surface
INV validation arms, and the generated-ci GOV-CODEOWNERS agreement check
(R2 #27 row 4).

Canonical layers and harmonization:
- FIX-* owns the labeled lab inventory fixture's own form (T15 #10 d5;
  T16 #11 d7); FIX-LIVE canonically owns the fixture's leak semantics, so the
  generic public-content scan skips the fixture surface (one root cause, one
  canonical code - T14 #19 d4 principle). Duplicate alias entries are
  INV-DUP's validation arm (T09 #12 d19; T10 #15 d1/d4).
- GOV-ROUTE's account arm fires for delegation-resolution failures the
  inventory-reference layer does not already own: an account whose
  intended_classification is the literal none (never an assignment target,
  T16 #11 d7) or names an unknown review class. An alias absent from the
  fixture is INV-ABSENT's layer; a duplicate binding is INV-DUP's.
- The declaration schemas applied here are the authored executable forms
  committed with this validator (schemas/governance/change-declaration/);
  the wired copies' byte identity is enforced separately (R1 #26 row 8).
- Registry, routing, and declaration checks evaluate the surfaces present in
  the target tree; the CI wiring (R4 #29) supplies the full repository tree.
  GOV-OWNER evaluates when a principals registry is present in the tree -
  resolution is meaningless without its authority surface.
"""

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator

from . import grammar, leak, tree
from .checks_access import _fixture_accounts

FIX_ENTRY_FIELDS = ("alias", "class", "status", "intended_classification")
FIX_CLASSES = {"management", "lab-workload", "role-host", "requested-fixture"}
FIX_STATUSES = {"active", "requested"}

_SCHEMA_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "schemas" / "governance" / "change-declaration"
)
DECLARATION_KINDS = (
    "principal-replacement",
    "group-key-rename",
    "permission-set-key-replacement",
)


def check_fixture(ctx):
    """FIX-* and the fixture-surface INV-DUP validation arm."""
    m = tree.model(ctx)
    doc = m.fixture
    if doc is None:
        return
    rel = doc.rel
    if doc.parse_error or not isinstance(doc.body, dict):
        ctx.emit("FIX-FIELDS", file_path=rel,
                 message="fixture failing to parse fails its family's schema "
                         "code")
        return
    body = doc.body
    if body.get("source") != "lab-fixture" or set(body) != {"source", "accounts"}:
        ctx.emit("FIX-FIELDS", file_path=rel,
                 message="the fixture is explicitly labeled: exactly "
                         "source: lab-fixture plus accounts")
    accounts = body.get("accounts")
    if not isinstance(accounts, list):
        return
    seen = {}
    for index, entry in enumerate(accounts):
        pointer = f"/accounts/{index}"
        if not isinstance(entry, dict):
            ctx.emit("FIX-FIELDS", file_path=rel, field_path=pointer,
                     message="fixture entry is not a mapping")
            continue
        if tuple(sorted(entry)) != tuple(sorted(FIX_ENTRY_FIELDS)):
            ctx.emit("FIX-FIELDS", file_path=rel, field_path=pointer,
                     message="entry field set not exactly {alias, class, "
                             "status, intended_classification}")
        alias = entry.get("alias")
        if alias is not None and not grammar.alias_valid(alias):
            ctx.emit("FIX-ALIAS", file_path=rel, field_path=f"{pointer}/alias",
                     message="alias violates the T05/T15 grammar")
        cls = entry.get("class")
        if cls is not None and cls not in FIX_CLASSES:
            ctx.emit("FIX-CLASS", file_path=rel, field_path=f"{pointer}/class",
                     value=str(cls),
                     message="class outside the closed account-class set")
        status = entry.get("status")
        if status is not None and status not in FIX_STATUSES:
            ctx.emit("FIX-FIELDS", file_path=rel,
                     field_path=f"{pointer}/status", value=str(status),
                     message="status outside the closed set active|requested")
        classification = entry.get("intended_classification")
        if classification is not None and not grammar.alias_valid(classification):
            ctx.emit("FIX-FIELDS", file_path=rel,
                     field_path=f"{pointer}/intended_classification",
                     message="intended_classification outside the key grammar")
        # FIX-LIVE: any live-identifier shape anywhere in the entry.
        blob = json.dumps(entry, sort_keys=True)
        for _line, kind, _token in leak.scan_text(blob):
            ctx.emit("FIX-LIVE", file_path=rel, field_path=pointer,
                     message=f"{kind}-shaped live identifier in the fixture; "
                             "aliases only, ever")
        if isinstance(alias, str):
            seen.setdefault(alias, []).append(index)
    for alias, indices in sorted(seen.items()):
        for index in indices[1:]:
            ctx.emit("INV-DUP", file_path=rel,
                     field_path=f"/accounts/{index}/alias", value=alias,
                     message="duplicate alias entry in the committed fixture")


def _registry(ctx):
    """principal keys and review-class keys present in the tree."""
    m = tree.model(ctx)
    principals = set()
    for doc in m.principals:
        if not doc.parse_error and isinstance(doc.body, dict):
            key = doc.body.get("key")
            if isinstance(key, str):
                principals.add(key)
    classes = set()
    for doc in m.review_classes:
        if not doc.parse_error and isinstance(doc.body, dict):
            key = doc.body.get("key")
            if isinstance(key, str):
                classes.add(key)
    return principals, classes


def check_registry(ctx):
    """GOV-PRINCIPAL / GOV-CLASS / GOV-OWNER (T06 #8 d1-d2)."""
    m = tree.model(ctx)
    principals, _classes = _registry(ctx)
    for doc in m.principals:
        if doc.parse_error or not isinstance(doc.body, dict):
            ctx.emit("GOV-PRINCIPAL", file_path=doc.rel,
                     message="principal record fails to parse")
            continue
        body = doc.body
        if set(body) != {"key", "kind", "description"}:
            ctx.emit("GOV-PRINCIPAL", file_path=doc.rel,
                     message="principal carries exactly key, kind, "
                             "description - no provider handles or class "
                             "membership")
        elif body.get("kind") not in ("role", "team"):
            ctx.emit("GOV-PRINCIPAL", file_path=doc.rel, field_path="/kind",
                     message="kind outside role|team")
        elif (not grammar.alias_valid(body.get("key"))
              or body["key"] != doc.stem
              or not isinstance(body.get("description"), str)
              or not body["description"]):
            ctx.emit("GOV-PRINCIPAL", file_path=doc.rel,
                     message="key grammar, filename-stem equality, or "
                             "description violated")
    for doc in m.review_classes:
        if doc.parse_error or not isinstance(doc.body, dict):
            ctx.emit("GOV-CLASS", file_path=doc.rel,
                     message="review-class record fails to parse")
            continue
        body = doc.body
        if set(body) != {"key", "description", "satisfied_by"}:
            ctx.emit("GOV-CLASS", file_path=doc.rel,
                     message="review class carries exactly key, description, "
                             "satisfied_by - enforcement is derived, never "
                             "authored")
            continue
        satisfied = body.get("satisfied_by")
        if (not isinstance(satisfied, list) or not satisfied
                or len(set(map(str, satisfied))) != len(satisfied)):
            ctx.emit("GOV-CLASS", file_path=doc.rel, field_path="/satisfied_by",
                     message="satisfied_by must be a non-empty duplicate-free "
                             "list of principal keys")
        elif not grammar.alias_valid(body.get("key")) or body["key"] != doc.stem:
            ctx.emit("GOV-CLASS", file_path=doc.rel,
                     message="key grammar or filename-stem equality violated")
        else:
            for index, principal in enumerate(satisfied):
                if principal not in principals:
                    ctx.emit("GOV-CLASS", file_path=doc.rel,
                             field_path=f"/satisfied_by/{index}",
                             value=str(principal),
                             message="unresolved principal key")
    # GOV-OWNER: owner fields resolve against the registry when one exists.
    if m.principals:
        owner_bearing = []
        if m.instance and not m.instance.parse_error and isinstance(
                m.instance.body, dict):
            owner_bearing.append((m.instance, m.instance.body.get("owner")))
        for doc in m.declarations:
            if not doc.parse_error and isinstance(doc.body, dict):
                owner_bearing.append((doc, doc.body.get("owner")))
        for doc, owner in owner_bearing:
            if isinstance(owner, str) and grammar.alias_valid(owner) \
                    and owner not in principals:
                ctx.emit("GOV-OWNER", file_path=doc.rel, field_path="/owner",
                         value=owner,
                         message="owner does not resolve to a principal key")


def _route_regex(pattern):
    out = []
    i = 0
    while i < len(pattern):
        if pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


ASSIGNMENT_PATH_RE = re.compile(
    r"^access/identity-center/account-assignments/([^/]+)/"
)


def _routes(ctx):
    m = tree.model(ctx)
    doc = m.routing
    if doc is None or doc.parse_error or not isinstance(doc.body, dict):
        return None
    routes = doc.body.get("routes")
    if not isinstance(routes, list):
        return None
    return doc, routes


def check_routing(ctx):
    """GOV-ROUTE (T06 #8 d3/d5): union semantics; fail-closed default;
    account-delegation resolution from the fixture's intended_classification."""
    m = tree.model(ctx)
    found = _routes(ctx)
    if found is None:
        return
    doc, routes = found
    if m.routing.body.get("unrouted") != "fail-closed":
        ctx.emit("GOV-ROUTE", file_path=doc.rel, field_path="/unrouted",
                 message="the fail-closed default must be stated explicitly")
    compiled = []
    for route in routes:
        if not isinstance(route, dict) or not isinstance(route.get("path"), str):
            ctx.emit("GOV-ROUTE", file_path=doc.rel,
                     message="malformed route record")
            continue
        compiled.append((route, _route_regex(route["path"])))
    _principals, classes = _registry(ctx)
    accounts = _fixture_accounts(m)
    flagged_accounts = set()
    for rel in ctx.files():
        matched = False
        yields_class = False
        for route, regex in compiled:
            if not regex.match(rel):
                continue
            matched = True
            if "review_classes" in route:
                declared = route["review_classes"]
                if isinstance(declared, list) and declared:
                    yields_class = True
            elif route.get("resolution") == "account-delegation":
                account_match = ASSIGNMENT_PATH_RE.match(rel)
                if not account_match:
                    continue
                alias = account_match.group(1)
                if accounts is None or alias not in (accounts or {}):
                    # INV-ABSENT's layer owns an alias missing from the
                    # fixture; the route neither passes nor double-fires.
                    continue
                entries = accounts[alias]
                classification = entries[0].get("intended_classification")
                if classification == "none":
                    if alias not in flagged_accounts:
                        ctx.emit("GOV-ROUTE", file_path=rel,
                                 value=alias,
                                 message="account is never an assignment "
                                         "target (intended_classification "
                                         "none)")
                        flagged_accounts.add(alias)
                elif classification not in classes:
                    if alias not in flagged_accounts:
                        ctx.emit("GOV-ROUTE", file_path=rel,
                                 value=str(classification),
                                 message="intended_classification does not "
                                         "resolve to a review class")
                        flagged_accounts.add(alias)
                else:
                    yields_class = True
        if not matched:
            ctx.emit("GOV-ROUTE", file_path=rel,
                     message="uncovered governed path - fail closed, never a "
                             "permissive fallback")
        elif not yields_class:
            # A path matched only by a delegation route whose resolution
            # failed is already flagged above; a path matched only by
            # malformed routes fails closed here.
            account_match = ASSIGNMENT_PATH_RE.match(rel)
            if not (account_match and account_match.group(1) in flagged_accounts) \
                    and not (account_match and accounts is not None
                             and account_match.group(1) not in accounts):
                ctx.emit("GOV-ROUTE", file_path=rel,
                         message="no matching route yields a review class")


def _declaration_validator(kind):
    with open(_SCHEMA_DIR / f"{kind}.schema.json", encoding="utf-8") as fh:
        return Draft202012Validator(json.load(fh))


def check_declarations(ctx):
    """GOV-DECLARATION (T06 #8 d5; declaration-vocabulary amendment 4)."""
    m = tree.model(ctx)
    for doc in m.declarations:
        if doc.parse_error or not isinstance(doc.body, dict):
            ctx.emit("GOV-DECLARATION", file_path=doc.rel,
                     message="declaration fails to parse")
            continue
        body = doc.body
        kind = body.get("kind")
        if kind not in DECLARATION_KINDS:
            ctx.emit("GOV-DECLARATION", file_path=doc.rel, field_path="/kind",
                     value=str(kind),
                     message="kind outside the three discriminated "
                             "declaration kinds")
            continue
        validator = _declaration_validator(kind)
        for error in sorted(validator.iter_errors(body), key=str):
            pointer = "/" + "/".join(str(p) for p in error.absolute_path)
            ctx.emit("GOV-DECLARATION", file_path=doc.rel,
                     field_path=pointer if pointer != "/" else None,
                     message=f"schema violation: {error.message[:120]}")
        if body.get("key") != doc.stem:
            ctx.emit("GOV-DECLARATION", file_path=doc.rel, field_path="/key",
                     message="key must equal the filename stem exactly")
        for field in ("valid_from", "valid_until"):
            value = body.get(field)
            if isinstance(value, str) and grammar.RFC3339_UTC_RE.match(value) \
                    and not grammar.rfc3339_utc_calendar_valid(value):
                ctx.emit("GOV-DECLARATION", file_path=doc.rel,
                         field_path=f"/{field}", value=value,
                         message="calendar-invalid RFC 3339 timestamp "
                                 "(clock-free validity parsing; "
                                 "declaration-vocabulary amendment 4)")


def _derived_codeowners(ctx):
    """The expected CODEOWNERS rules derived from routing, the registry, and
    the handle mapping (T06 #8 d2/d3; T10 #15 d5): one rule per explicit
    route in routing order, then per-account rules enumerated from the
    fixture in byte-lexicographic alias order."""
    found = _routes(ctx)
    if found is None:
        return None
    _doc, routes = found
    m = tree.model(ctx)
    handles = ctx.config.handle_mapping or {}
    _principals, classes = _registry(ctx)
    class_principals = {}
    for doc in m.review_classes:
        if not doc.parse_error and isinstance(doc.body, dict):
            key = doc.body.get("key")
            satisfied = doc.body.get("satisfied_by")
            if isinstance(key, str) and isinstance(satisfied, list):
                class_principals[key] = satisfied
    def handles_for(class_keys):
        out = set()
        for cls in class_keys:
            for principal in class_principals.get(cls, ()):
                handle = handles.get(principal)
                if handle:
                    out.add(handle)
        return sorted(out)

    rules = []
    delegation_patterns = []
    for route in routes:
        if not isinstance(route, dict):
            continue
        if "review_classes" in route:
            rules.append((f"/{route['path']}", handles_for(route["review_classes"])))
        elif route.get("resolution") == "account-delegation":
            delegation_patterns.append(route["path"])
    if delegation_patterns:
        accounts = _fixture_accounts(m) or {}
        for alias in sorted(accounts):
            entry = accounts[alias][0]
            classification = entry.get("intended_classification")
            if classification and classification != "none" \
                    and classification in classes:
                rules.append((
                    f"/access/identity-center/account-assignments/{alias}/**",
                    handles_for([classification]),
                ))
    return rules


def check_codeowners(ctx):
    """GOV-CODEOWNERS (generated-ci): the given CODEOWNERS must agree with
    the registry, routing, and handle mapping."""
    given = ctx.config.codeowners
    if given is None:
        return
    derived = _derived_codeowners(ctx)
    if derived is None:
        return
    parsed = []
    for line in given.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        parsed.append((parts[0], sorted(parts[1:])))
    for index, (expected, got) in enumerate(zip(derived, parsed)):
        if expected != got:
            ctx.emit("GOV-CODEOWNERS", field_path=f"L{index + 1}",
                     value=got[0],
                     message="generated CODEOWNERS disagrees with the "
                             "registry, routing, and handle mapping")
    if len(derived) != len(parsed):
        ctx.emit("GOV-CODEOWNERS",
                 message=f"rule count {len(parsed)} differs from the derived "
                         f"rule set {len(derived)}")
