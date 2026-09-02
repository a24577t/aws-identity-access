"""R3 #28 allocation reconciliation - ADO-PHASE detection (T19 #14 d2).

The greenfield/adoption boundary is mechanism-defined: slice A contains no
`import` block, no `moved`/`removed` state surgery of any kind. Adoption
exists only inside the separately authorized post-acceptance
import-rehearsal phase; any adoption-shaped configuration outside that
phase is a validation error - ADO-PHASE at its canonical validation layer.
ADO-MANIFEST remains dormant (activation condition recorded in the
catalogue) and carries no fixture.
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from tests.test_validator_governance_families import GovTreeCase  # noqa: E402


class AdoPhase(GovTreeCase):
    def setUp(self) -> None:
        super().setUp()
        # Route the infrastructure surface so ADO specimens isolate their
        # own code (GOV-ROUTE owns uncovered paths, a different root cause).
        self.write(
            "governance/ownership/routing.yml",
            "unrouted: fail-closed\n"
            "routes:\n"
            "  - path: access/**\n    review_classes: [identity-platform]\n"
            "  - path: governance/**\n    review_classes: [identity-platform]\n"
            "  - path: docs/**\n    review_classes: [identity-platform]\n"
            "  - path: infrastructure/**\n"
            "    review_classes: [identity-platform]\n"
            "  - path: access/identity-center/account-assignments/*/**\n"
            "    resolution: account-delegation\n",
        )

    def test_import_block_fires(self) -> None:
        self.write(
            "infrastructure/identity-center/adopt.tf",
            "import {\n  to = aws_ssoadmin_permission_set.old\n"
            "  id = \"[omitted]\"\n}\n",
        )
        self.assertCodes(["ADO-PHASE"])

    def test_moved_block_fires(self) -> None:
        self.write(
            "infrastructure/identity-center/moves.tf",
            "moved {\n  from = aws_ssoadmin_permission_set.a\n"
            "  to = aws_ssoadmin_permission_set.b\n}\n",
        )
        self.assertCodes(["ADO-PHASE"])

    def test_removed_block_fires(self) -> None:
        self.write(
            "infrastructure/identity-center/removals.tf",
            "removed {\n  from = aws_ssoadmin_permission_set.old\n"
            "  lifecycle {\n    destroy = false\n  }\n}\n",
        )
        self.assertCodes(["ADO-PHASE"])

    def test_ordinary_terraform_configuration_is_clean(self) -> None:
        self.write(
            "infrastructure/identity-center/main.tf",
            "resource \"aws_ssoadmin_permission_set\" \"read_only\" {\n"
            "  name = \"ialab-read-only\"\n}\n\n"
            "# imported wording in a comment is not an import block\n",
        )
        self.assertCodes([])

    def test_non_terraform_files_never_fire(self) -> None:
        self.write("docs/guides/adoption-notes.md",
                    "---\nauthority: informative\nderives_from:\n"
                    "  - governance/ownership/routing.yml\n---\n\n"
                    "import { } moved { } removed { } as prose\n")
        self.assertCodes([])


if __name__ == "__main__":
    unittest.main()
