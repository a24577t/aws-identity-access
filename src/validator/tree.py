"""Parsed model of the target tree's governed surfaces.

Canonical traversal only (T14 #19 C14): files are visited in
byte-lexicographic path order; parse results are cached per run. A YAML
parse failure is recorded on the entry (parse_error) and mapped to its
family's schema code by the owning check - a file failing to parse fails its
family's schema code (T14 #19 exploratory disposition E-YML).
"""

import yaml

GROUPS_DIR = "access/identity-center/groups"
PERMISSION_SETS_DIR = "access/identity-center/permission-sets"
ASSIGNMENTS_DIR = "access/identity-center/account-assignments"
INSTANCE_PATH = "access/identity-center/configuration/instance.yml"
PRINCIPALS_DIR = "governance/ownership/principals"
REVIEW_CLASSES_DIR = "governance/ownership/review-classes"
ROUTING_PATH = "governance/ownership/routing.yml"
DECLARATIONS_DIR = "governance/change-declarations"

# The six enumerated absent-for-slice surfaces (T04 #6 d6; ADR-0004).
ABSENT_SURFACES = (
    "access/iam/",
    "access/deployments/fleet-roles/",
    "access/identity-center/identity-source/",
    "access/identity-center/bootstrap/",
    "governance/exceptions/",
    "governance/runtime-mutations/",
)


class Doc:
    """One governed file: path, stem, parsed body or parse_error."""

    def __init__(self, rel, body=None, parse_error=None):
        self.rel = rel
        name = rel.rsplit("/", 1)[-1]
        self.name = name
        self.stem = name[: -len(".yml")] if name.endswith(".yml") else name
        self.body = body
        self.parse_error = parse_error


def _load(ctx, rel):
    try:
        body = yaml.safe_load(ctx.read_bytes(rel).decode("utf-8"))
    except Exception as exc:  # yaml or decode errors - fail the family code
        return Doc(rel, parse_error=str(exc.__class__.__name__))
    return Doc(rel, body=body)


class Model:
    def __init__(self, ctx):
        self.groups = []
        self.permission_sets = []
        self.assignments = []      # (account_dir, Doc)
        self.assignment_stray = [] # files directly under ASSIGNMENTS_DIR
        self.instance = None
        self.principals = []
        self.review_classes = []
        self.routing = None
        self.declarations = []
        self.out_of_slice = []     # (rel, surface)
        self.fixture = None        # Doc for the configured inventory fixture

        for rel in ctx.files():
            for surface in ABSENT_SURFACES:
                if rel.startswith(surface):
                    self.out_of_slice.append((rel, surface))
                    break
            else:
                self._place(ctx, rel)

        fixture_path = ctx.config.inventory_fixture
        if fixture_path is not None:
            from pathlib import Path

            path = Path(fixture_path)
            try:
                rel = path.resolve().relative_to(ctx.target.resolve()).as_posix()
            except ValueError:
                rel = path.as_posix()
            try:
                body = yaml.safe_load(path.read_bytes().decode("utf-8"))
                self.fixture = Doc(rel, body=body)
            except FileNotFoundError:
                self.fixture = None
            except Exception as exc:
                self.fixture = Doc(rel, parse_error=str(exc.__class__.__name__))

    def _place(self, ctx, rel):
        if rel.startswith(GROUPS_DIR + "/"):
            self.groups.append(_load(ctx, rel))
        elif rel.startswith(PERMISSION_SETS_DIR + "/"):
            self.permission_sets.append(_load(ctx, rel))
        elif rel.startswith(ASSIGNMENTS_DIR + "/"):
            tail = rel[len(ASSIGNMENTS_DIR) + 1 :]
            parts = tail.split("/")
            if len(parts) == 1:
                self.assignment_stray.append(_load(ctx, rel))
            else:
                self.assignments.append((parts[0], _load(ctx, rel)))
        elif rel == INSTANCE_PATH:
            self.instance = _load(ctx, rel)
        elif rel.startswith(PRINCIPALS_DIR + "/"):
            self.principals.append(_load(ctx, rel))
        elif rel.startswith(REVIEW_CLASSES_DIR + "/"):
            self.review_classes.append(_load(ctx, rel))
        elif rel == ROUTING_PATH:
            self.routing = _load(ctx, rel)
        elif rel.startswith(DECLARATIONS_DIR + "/") and rel.endswith(".yml"):
            # Direct children only: the wired schemas/ subdirectory and the
            # README are not declaration instances.
            if "/" not in rel[len(DECLARATIONS_DIR) + 1 :]:
                self.declarations.append(_load(ctx, rel))


def model(ctx):
    if "model" not in ctx._cache:
        ctx._cache["model"] = Model(ctx)
    return ctx._cache["model"]
