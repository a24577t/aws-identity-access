"""The two-layer deterministic plan-effect classifier (R3 #28 row 9).

Pure classification data and functions for the T20 #22 contract; the CLS-*
findings themselves are emitted by checks_cls on the row-3 core.

Layer 1 (T20 #22 d5): every recognized plan-JSON action list maps to exactly
one action class - no-op, read, create, update, delete, replace (accepting
BOTH delete-then-create and create-then-delete orders), and forget (the
T21 F8 representation for `removed { lifecycle { destroy = false } }`).
Anything else is unrecognized and fails closed. Read rows are excluded from
the mutation aggregate under this explicit deterministic rule - they are
listed in the summary's read section, never silently dropped.

The aggregate operates over the complete normalized vector of
managed-resource effects, never one label from a single resource:
empty / creates-only / updates-only / deletes-only / mixed; the
contract-level classes (imports-only, state-removal-only,
guard-removal-no-live-change) are layer 2 - they require their
configuration marker AND their aggregate condition together, and any
inconsistency fails closed (checks_cls).

PR classes (T20 #22 d1/d2): classification is by changed path, evaluated
per file against the decision-2 table exactly; a file matching no row is a
fail-closed classification error (CLS-UNCOVERED-PATH). The permitted plan
effects follow the d5 matrix rendered per-row: every mutation row must be
attributable to an allowed changed surface of one matched class, and the
plan is permitted iff every row is attributable and every matched class's
constraints hold.
"""

# --- Layer 1: action classes ---------------------------------------------

_ACTION_CLASSES = {
    ("no-op",): "no-op",
    ("read",): "read",
    ("create",): "create",
    ("update",): "update",
    ("delete",): "delete",
    ("delete", "create"): "replace",
    ("create", "delete"): "replace",
    ("forget",): "forget",
}

LIVE_MUTATION = frozenset({"create", "update", "delete", "replace"})


def action_class(actions):
    """The T21 F8 action class for one plan-JSON action list, or None for
    any unrecognized list (fail closed at the caller)."""
    if not isinstance(actions, (list, tuple)):
        return None
    return _ACTION_CLASSES.get(tuple(actions))


def aggregate_class(classes):
    """The aggregate over the live-mutation vector (forget and read rows
    are handled by their own layer-2 / read-section rules)."""
    live = [c for c in classes if c in LIVE_MUTATION]
    if not live:
        return "empty"
    if all(c == "create" for c in live):
        return "creates-only"
    if all(c == "update" for c in live):
        return "updates-only"
    if all(c == "delete" for c in live):
        return "deletes-only"
    return "mixed"


# --- PR classes: the decision-2 changed-path table ------------------------

_EXACT_PATHS = {
    "CLAUDE.md": "platform-change",
    "README.md": "documentation",
    "CONTEXT.md": "documentation",
}

# Ordered most-specific-first; each changed file takes its first match.
_PATH_RULES = (
    ("access/identity-center/account-assignments/", "access-grant"),
    ("access/identity-center/groups/", "access-definition"),
    ("access/identity-center/permission-sets/", "access-definition"),
    ("access/identity-center/configuration/", "verification-update"),
    ("governance/change-declarations/", "exceptional-change"),
    ("governance/", "platform-change"),
    ("schemas/", "platform-change"),
    ("infrastructure/", "platform-change"),
    ("src/", "platform-change"),
    ("tests/", "platform-change"),
    (".github/", "platform-change"),
    (".ai/", "platform-change"),
    (".claude/", "platform-change"),
    ("docs/architecture/", "platform-change"),
    ("docs/adr/", "platform-change"),
    ("docs/", "documentation"),
)


def path_class(path):
    """The T20 d2 class for one changed file, or None (uncovered - the
    caller fails closed; CLS-UNCOVERED-PATH)."""
    if path in _EXACT_PATHS:
        return _EXACT_PATHS[path]
    for prefix, cls in _PATH_RULES:
        if path.startswith(prefix):
            return cls
    return None


def classify_paths(paths):
    """(matched class set, uncovered path list) for a changed-path set."""
    classes = set()
    uncovered = []
    for path in sorted(paths):
        cls = path_class(path)
        if cls is None:
            uncovered.append(path)
        else:
            classes.add(cls)
    return classes, uncovered


def prohibited_combination(classes):
    """The d1 prohibited combinations decidable from the path classes: a
    declaration/cleanup-arm PR changes only the declaration and its
    documentary/control material - never an access surface (a PR must not
    introduce a declaration and execute its exceptional change
    simultaneously)."""
    if "exceptional-change" in classes and classes & {
        "access-grant", "access-definition", "verification-update"
    }:
        return ("a declaration or cleanup PR combined with requester-surface "
                "changes - a PR must not introduce a declaration and execute "
                "its exceptional change simultaneously (T20 #22 d1)")
    return None


# --- Row attribution and the d5 matrix, rendered per row ------------------

# Managed slice-A resource types and the PR class whose changed surface
# each is attributable to (T20 d5 composition; T21 F5-F7 resource set).
RESOURCE_SURFACES = {
    "aws_ssoadmin_account_assignment": "access-grant",
    "aws_ssoadmin_permission_set": "access-definition",
    "aws_ssoadmin_managed_policy_attachment": "access-definition",
    "aws_ssoadmin_permission_set_inline_policy": "access-definition",
}

# Permission-set-shaped types carry the deployed Name for the
# protected-resource guard (T15 #10 d7; ADR-0009).
NAMED_TYPES = frozenset({"aws_ssoadmin_permission_set"})

# Per-class permitted row actions outside any overlay (the d5 matrix
# rendered per row; deletes-only for access-grant additionally requires the
# exact-entry revocation acknowledgement - checks_cls).
PERMITTED_ACTIONS = {
    "access-grant": frozenset({"create", "delete"}),
    "access-definition": frozenset({"create", "update"}),
}


def overlay_permits(overlay, surface, cls):
    """Whether a matched exceptional-change overlay permits a row action the
    plain matrix rejects (T06 #8 d5 fixed classes; GOV-DECL-MATCH owns the
    declaration matching itself)."""
    if not isinstance(overlay, dict):
        return False
    kind = overlay.get("kind")
    phase = overlay.get("phase")
    if kind == "permission-set-key-replacement" and phase == "retire":
        # Retiring the old permission set and its old assignments only.
        return cls == "delete" and surface in ("access-definition",
                                               "access-grant")
    return False
