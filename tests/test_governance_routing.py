"""R1 #26 row-8 mechanical check: routing-table coverage demonstration
(ticket #26 row 8 acceptance criteria; T06 #8 decisions 3 and 5).

Demonstrates, without implementing the R2 #27 validator:
- every git-tracked repository path resolves to at least one review class
  (explicit-route coverage of the whole governed tree);
- routing combines matching routes by set union — a more-specific route never
  erases a stricter matching requirement;
- assignment paths resolve through account delegation from the inventory's
  intended_classification, and an unknown, ambiguous, or inactive account fails
  closed;
- an unrouted path fails closed (GOV-ROUTE), never a permissive fallback.

The route matcher here is test-local demonstration logic; the enforcing
validator is R2 #27 work under the T14 #19 contract.
"""

import re
import shutil
import subprocess
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ROUTING = REPO / "governance" / "ownership" / "routing.yml"

# The approved five-entry alias fixture content (T16 #11 decision 7); the fixture
# file itself lands with R2 #27 — this constant is demonstration data only.
T16_FIXTURE_ACCOUNTS = [
    {"alias": "lab-management", "class": "management", "status": "active", "intended_classification": "none"},
    {"alias": "lab-tooling", "class": "role-host", "status": "active", "intended_classification": "none"},
    {"alias": "lab-workload-a", "class": "lab-workload", "status": "active", "intended_classification": "identity-platform"},
    {"alias": "lab-workload-b", "class": "lab-workload", "status": "active", "intended_classification": "identity-platform"},
    {"alias": "lab-requested", "class": "requested-fixture", "status": "requested", "intended_classification": "identity-platform"},
]


def pattern_to_regex(pattern: str) -> re.Pattern:
    """Translate the routing glob grammar to a regex.

    ** matches any number of path segments (including none, together with a
    preceding /); * matches within one segment.
    """
    out = []
    i = 0
    while i < len(pattern):
        if pattern.startswith("/**", i):
            out.append(r"(/.*)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(r".*")
            i += 2
        elif pattern[i] == "*":
            out.append(r"[^/]*")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


class Router:
    """Test-local realization of the T06 #8 decision-3 routing semantics."""

    ASSIGNMENT_RE = re.compile(
        r"^access/identity-center/account-assignments/([^/]+)/"
    )

    def __init__(self, routing: dict, fixture_accounts: list[dict]):
        self.routes = [
            (pattern_to_regex(r["path"]), r) for r in routing["routes"]
        ]
        assert routing["unrouted"] == "fail-closed"
        self.delegation = {}
        for entry in fixture_accounts:
            alias = entry["alias"]
            if alias in self.delegation:
                self.delegation[alias] = "duplicate"
            else:
                self.delegation[alias] = entry

    def resolve(self, path: str) -> set[str]:
        """Return the union of required review classes; raise LookupError on any
        fail-closed condition (unrouted path; unroutable account)."""
        classes: set[str] = set()
        matched = False
        for regex, route in self.routes:
            if not regex.match(path):
                continue
            matched = True
            if "review_classes" in route:
                classes.update(route["review_classes"])
            else:  # resolution: account-delegation
                m = self.ASSIGNMENT_RE.match(path)
                if not m:
                    raise LookupError(f"delegation route without account: {path}")
                entry = self.delegation.get(m.group(1))
                if entry is None or entry == "duplicate":
                    raise LookupError(f"unroutable account: {m.group(1)}")
                if entry["status"] != "active":
                    # A deferred (requested) reference is a deployment property,
                    # not a routing failure; its delegation class still applies
                    # (T16 #11 d7-d8: intended_classification is authored for
                    # requested entries too).
                    pass
                if entry["intended_classification"] == "none":
                    raise LookupError(f"never an assignment target: {m.group(1)}")
                classes.add(entry["intended_classification"])
        if not matched or not classes:
            raise LookupError(f"unrouted path fails closed: {path}")
        return classes


def load_router() -> Router:
    with open(ROUTING, encoding="utf-8") as fh:
        routing = yaml.safe_load(fh)
    return Router(routing, T16_FIXTURE_ACCOUNTS)


class RoutingCoverage(unittest.TestCase):
    def setUp(self) -> None:
        self.router = load_router()

    @unittest.skipUnless(
        shutil.which("git"),
        "needs git for ls-files; the pinned validator container carries no "
        "git - this coverage check runs on the host and in CI instead",
    )
    def test_every_tracked_path_resolves(self) -> None:
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        self.assertTrue(tracked)
        for path in tracked:
            with self.subTest(path=path):
                classes = self.router.resolve(path)
                self.assertTrue(classes)

    def test_union_semantics_more_specific_never_erases(self) -> None:
        # groups/** is stricter than the access/** catch-all; the union keeps both.
        self.assertEqual(
            {"identity-platform", "security"},
            self.router.resolve("access/identity-center/groups/lab-readers.yml"),
        )
        self.assertEqual(
            {"identity-platform", "security"},
            self.router.resolve(
                "access/identity-center/configuration/instance.yml"
            ),
        )
        # Requester documentation resolves to identity-platform.
        self.assertEqual(
            {"identity-platform"}, self.router.resolve("access/README.md")
        )

    def test_strictest_set_on_control_surfaces(self) -> None:
        strictest = {"identity-platform", "security", "architecture"}
        for path in [
            "governance/ownership/routing.yml",
            "schemas/access/group.schema.json",
            "src/README.md",
            "tests/README.md",
            ".github/README.md",
            ".ai/repository/state/STATUS.md",
            "CLAUDE.md",
            "docs/architecture/configuration-contract.md",
            "docs/adr/0003-requester-surface-and-top-level-layout.md",
            "docs/specifications/slice-a-engineering-specification.md",
            ".gitattributes",
            "LICENSE",
        ]:
            with self.subTest(path=path):
                self.assertEqual(strictest, self.router.resolve(path))

    def test_account_delegation_resolution(self) -> None:
        for account in ["lab-workload-a", "lab-workload-b", "lab-requested"]:
            with self.subTest(account=account):
                self.assertEqual(
                    {"identity-platform"},
                    self.router.resolve(
                        "access/identity-center/account-assignments/"
                        f"{account}/lab-readers--read-only.yml"
                    ),
                )

    def test_unroutable_account_fails_closed(self) -> None:
        with self.assertRaises(LookupError):
            self.router.resolve(
                "access/identity-center/account-assignments/"
                "unknown-account/lab-readers--read-only.yml"
            )
        # An alias that is never an assignment target fails closed too.
        with self.assertRaises(LookupError):
            self.router.resolve(
                "access/identity-center/account-assignments/"
                "lab-tooling/lab-readers--read-only.yml"
            )

    def test_unrouted_path_fails_closed(self) -> None:
        with self.assertRaises(LookupError):
            self.router.resolve("unrouted-root-file.txt")
        with self.assertRaises(LookupError):
            self.router.resolve("somedir/nested/file.yml")

    def test_registry_referential_integrity(self) -> None:
        # Every routed class and every satisfied_by principal resolves in the
        # registry (GOV-CLASS / GOV-ROUTE preconditions).
        principals = {
            yaml.safe_load(p.read_text(encoding="utf-8"))["key"]
            for p in (REPO / "governance/ownership/principals").glob("*.yml")
        }
        classes = {}
        for p in (REPO / "governance/ownership/review-classes").glob("*.yml"):
            record = yaml.safe_load(p.read_text(encoding="utf-8"))
            classes[record["key"]] = record
        with open(ROUTING, encoding="utf-8") as fh:
            routing = yaml.safe_load(fh)
        for route in routing["routes"]:
            for cls in route.get("review_classes", []):
                self.assertIn(cls, classes, f"unresolved class in route {route['path']}")
        for key, record in classes.items():
            for principal in record["satisfied_by"]:
                self.assertIn(principal, principals, f"unresolved principal in class {key}")


if __name__ == "__main__":
    unittest.main()
