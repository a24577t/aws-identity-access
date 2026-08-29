"""R2 #27 row-5 external checks - the T21 #20 d6 standing-admin-capability
hazard detector (ADM-CAPABLE), the T07 #9 cross-file condition
(ADM-STANDING), and fail-closed catalog integrity (ADM-CATALOG), per
T14 #19 d5 and ADR-0008.

Row-5 state: rules 1/3/5 are executable as specified; the universal
unconditional Allow of all actions over all resources is detected without
catalog data (T07's named minimum equivalence); service-scoped wildcard
expansion (rules 2/4) is data-blocked and fails closed as ADM-CATALOG until
the row-6 catalogs exist with matching digests.
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from tests.test_validator_governance_families import GovTreeCase  # noqa: E402

ADMIN_ARN = "arn:aws:iam::aws:policy/AdministratorAccess"


def ps(key, statements=None, managed=None):
    lines = [f"key: {key}", "description: Specimen definition.",
             "session_duration: PT1H"]
    if managed:
        lines.append("managed_policies:")
        lines.extend(f"  - {arn}" for arn in managed)
    if statements is not None:
        lines.append("inline_policy:")
        lines.append("  Version: \"2012-10-17\"")
        lines.append("  Statement:")
        lines.extend(statements)
    return "\n".join(lines) + "\n"


class NoCatalogCase(GovTreeCase):
    """Row-5 state: no catalog data configured."""

    def adm(self, key, content):
        self.write(
            f"access/identity-center/permission-sets/{key}.yml", content
        )
        return self.codes(catalog_dir=self.target / "no-catalogs",
                          catalog_reference=self.target / "no-reference.json")


class RuleOne(NoCatalogCase):
    def test_exact_administrator_access_arn_fires(self) -> None:
        self.assertEqual(
            ["ADM-CAPABLE"], self.adm("admin", ps("admin", managed=[ADMIN_ARN]))
        )

    def test_other_aws_managed_policy_passes(self) -> None:
        self.assertEqual(
            [],
            self.adm("viewer", ps(
                "viewer",
                managed=["arn:aws:iam::aws:policy/ViewOnlyAccess"])),
        )


class RuleThree(NoCatalogCase):
    def test_allow_with_notaction_fails_closed(self) -> None:
        self.assertEqual(
            ["ADM-CAPABLE"],
            self.adm("inv", ps("inv", statements=[
                "    - Effect: Allow",
                "      NotAction: [\"iam:DeleteUser\"]",
                "      Resource: \"*\"",
            ])),
        )

    def test_allow_with_notresource_fails_closed(self) -> None:
        self.assertEqual(
            ["ADM-CAPABLE"],
            self.adm("inv", ps("inv", statements=[
                "    - Effect: Allow",
                "      Action: [\"iam:GetUser\"]",
                "      NotResource: [\"arn:aws:iam::aws:policy/X\"]",
            ])),
        )


class RuleTwoUniversal(NoCatalogCase):
    def test_unconditional_allow_star_star_fires(self) -> None:
        self.assertEqual(
            ["ADM-CAPABLE"],
            self.adm("wide", ps("wide", statements=[
                "    - Effect: Allow",
                "      Action: \"*\"",
                "      Resource: \"*\"",
            ])),
        )

    def test_conditional_broad_allow_fails_closed_rule_five(self) -> None:
        # A condition never excuses a broad grant; the detector does not
        # compute condition semantics - unknown broad pattern, fail closed.
        self.assertEqual(
            ["ADM-CAPABLE"],
            self.adm("wide", ps("wide", statements=[
                "    - Effect: Allow",
                "      Action: \"*\"",
                "      Resource: \"*\"",
                "      Condition:",
                "        Bool: { \"aws:MultiFactorAuthPresent\": \"true\" }",
            ])),
        )

    def test_deny_star_star_is_not_a_grant(self) -> None:
        self.assertEqual(
            [],
            self.adm("deny", ps("deny", statements=[
                "    - Effect: Allow",
                "      Action: [\"iam:GetUser\"]",
                "      Resource: \"*\"",
                "    - Effect: Deny",
                "      Action: \"*\"",
                "      Resource: \"*\"",
            ])),
        )


class RuleFive(NoCatalogCase):
    def test_unsupported_action_type_fails_closed(self) -> None:
        self.assertEqual(
            ["ADM-CAPABLE"],
            self.adm("odd", ps("odd", statements=[
                "    - Effect: Allow",
                "      Action: { deep: structure }",
                "      Resource: \"*\"",
            ])),
        )

    def test_unknown_effect_fails_closed(self) -> None:
        self.assertEqual(
            ["ADM-CAPABLE"],
            self.adm("odd", ps("odd", statements=[
                "    - Effect: Maybe",
                "      Action: [\"iam:GetUser\"]",
                "      Resource: \"*\"",
            ])),
        )


class DataBlockedRules(NoCatalogCase):
    def test_service_wildcard_without_catalogs_is_adm_catalog(self) -> None:
        # Rules 2/4 are contract-complete and data-blocked (T14 #19 d5 C9):
        # any invocation without valid catalog data raises ADM-CATALOG.
        self.assertEqual(
            ["ADM-CATALOG"],
            self.adm("wild", ps("wild", statements=[
                "    - Effect: Allow",
                "      Action: [\"iam:*\"]",
                "      Resource: \"*\"",
            ])),
        )

    def test_explicit_bounded_list_needs_no_catalog(self) -> None:
        # The accepted valid basis (inventory-reader) predates the catalogs:
        # a finite explicit action list is bounded by construction and does
        # not invoke wildcard expansion.
        self.assertEqual(
            [],
            self.adm("inv2", ps("inv2", statements=[
                "    - Effect: Allow",
                "      Action:",
                "        - iam:GetAccountSummary",
                "        - iam:ListAccountAliases",
                "      Resource: \"*\"",
            ])),
        )


class Standing(NoCatalogCase):
    def test_the_approved_pair(self) -> None:
        # The T07 negative pair carries expected set exactly
        # {ADM-CAPABLE, ADM-STANDING} (T14 #19 d6).
        self.write(
            "access/identity-center/permission-sets/admin.yml",
            ps("admin", managed=[ADMIN_ARN]),
        )
        self.write(
            "access/identity-center/account-assignments/lab-workload-a/"
            "lab-readers--admin.yml",
            "account: lab-workload-a\nprincipal:\n  type: GROUP\n"
            "  group: lab-readers\npermission_set: admin\n",
        )
        self.assertCodes(
            ["ADM-CAPABLE", "ADM-STANDING"],
            catalog_dir=self.target / "no-catalogs",
            catalog_reference=self.target / "no-reference.json",
        )

    def test_capable_definition_without_assignment_is_single(self) -> None:
        self.write(
            "access/identity-center/permission-sets/admin.yml",
            ps("admin", managed=[ADMIN_ARN]),
        )
        self.assertCodes(
            ["ADM-CAPABLE"],
            catalog_dir=self.target / "no-catalogs",
            catalog_reference=self.target / "no-reference.json",
        )


if __name__ == "__main__":
    unittest.main()
