"""R2 #27 row-3/row-4 external check: the implemented catalogue equals the
T14 #19 catalogue exactly - 79 codes, 13 families, 78 active, 1 dormant;
severity error everywhere except INV-DEFERRED (deferred); stage lists
exhaustive per the T14 tables; catalogue self-validation fails closed on a
severity outside the closed vocabulary (T14 #19 d1).

Expected values below are transcribed from the T14 #19 record
(docs/wayfinding/map-1/19-validation-contract-for-the-selected-slice.md),
never derived from the implementation.
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import catalogue  # noqa: E402

# family -> {code: (severity, (stages...))} - T14 #19 Catalogue section.
T14 = {
    "INV": {
        "INV-DEFERRED": ("deferred", ("validation", "plan", "apply")),
        "INV-ABSENT": ("error", ("validation", "plan", "apply")),
        "INV-UNBOUND": ("error", ("plan", "apply")),
        "INV-STATE": ("error", ("plan", "apply")),
        "INV-RENAME": ("error", ("plan", "apply")),
        "INV-OU": ("error", ("plan", "apply")),
        "INV-DUP": ("error", ("validation", "plan", "apply")),
        "INV-UNALIASED": ("error", ("plan", "apply")),
        "INV-DIGEST": ("error", ("plan", "apply")),
        "INV-STALE": ("error", ("plan", "apply")),
        "INV-MISSING": ("error", ("plan", "apply")),
        "INV-PARTIAL": ("error", ("plan", "apply")),
        "INV-PROHIBITED-FIELD": ("error", ("plan", "apply")),
        "INV-BOUNDARY": ("error", ("plan", "apply")),
        "INV-PUBLIC-LEAK": ("error", ("validation", "plan", "apply", "generated-ci")),
    },
    "PRQ": {
        code: ("error", ("plan", "apply"))
        for code in (
            "PRQ-MISSING",
            "PRQ-SNAPSHOT",
            "PRQ-INSTANCE",
            "PRQ-IDENTITY-STORE",
            "PRQ-DELEGATED-ADMIN",
            "PRQ-ATTESTATION",
            "PRQ-GROUP",
        )
    },
    "P-OOS": {
        code: ("error", ("validation",))
        for code in (
            "P-OOS-CMP",
            "P-OOS-BOUNDARY",
            "P-OOS-USER",
            "P-OOS-IDENTITY-SOURCE",
            "P-OOS-PATH",
            "P-OOS-POLICY-FORM",
        )
    },
    "KEY": {
        "KEY-GRAMMAR": ("error", ("validation",)),
        "KEY-FILENAME": ("error", ("validation",)),
        "KEY-COMPOSED": ("error", ("validation",)),
        "KEY-DESCRIPTION": ("error", ("validation",)),
        "KEY-IDSTORE-NAME": ("error", ("validation",)),
        "KEY-DUP": ("error", ("validation",)),
        "KEY-DANGLING": ("error", ("validation",)),
        "KEY-PROTECTED": ("error", ("validation", "plan", "apply")),
    },
    "ASN": {
        code: ("error", ("validation",))
        for code in ("ASN-SHAPE", "ASN-ACCOUNT-ALIAS", "ASN-AGREEMENT")
    },
    "ADM": {
        code: ("error", ("validation",))
        for code in ("ADM-CAPABLE", "ADM-STANDING", "ADM-CATALOG")
    },
    "GOV": {
        "GOV-PRINCIPAL": ("error", ("validation",)),
        "GOV-CLASS": ("error", ("validation",)),
        "GOV-OWNER": ("error", ("validation",)),
        "GOV-ROUTE": ("error", ("validation",)),
        "GOV-CODEOWNERS": ("error", ("generated-ci",)),
        "GOV-DECLARATION": ("error", ("validation",)),
        "GOV-DECL-MATCH": ("error", ("plan",)),
        "GOV-ENFORCEMENT": ("error", ("plan", "apply")),
        "GOV-APPROVAL-CLASS": ("error", ("plan",)),
    },
    "FIX": {
        code: ("error", ("validation",))
        for code in ("FIX-FIELDS", "FIX-CLASS", "FIX-ALIAS", "FIX-LIVE")
    },
    "CFG": {
        code: ("error", ("validation",))
        for code in ("CFG-FIELDS", "CFG-VOCAB", "CFG-REGION", "CFG-VERIFICATION")
    },
    "DOC": {
        code: ("error", ("validation",))
        for code in ("DOC-NORMATIVE", "DOC-INFORMATIVE", "DOC-SCOPE")
    },
    "GEN": {
        "GEN-MANIFEST": ("error", ("validation", "generated-ci")),
        "GEN-ENVELOPE": ("error", ("validation", "generated-ci")),
        "GEN-DRIFT": ("error", ("generated-ci",)),
        "GEN-CODEOWNERS": ("error", ("validation", "generated-ci")),
    },
    "CLS": {
        "CLS-UNCOVERED-PATH": ("error", ("validation", "plan")),
        "CLS-COMBINATION": ("error", ("validation", "plan")),
        "CLS-UNKNOWN-ACTION": ("error", ("plan",)),
        "CLS-UNRESOLVED-VALUE": ("error", ("plan",)),
        "CLS-REPRESENTATION": ("error", ("plan",)),
        "CLS-FORGET-PATTERN": ("error", ("plan",)),
        "CLS-MARKER-MISMATCH": ("error", ("plan",)),
        "CLS-UNATTRIBUTABLE": ("error", ("plan",)),
        "CLS-EFFECT": ("error", ("plan",)),
        "CLS-PROTECTED": ("error", ("plan", "apply")),
        "CLS-REVOCATION-ACK": ("error", ("plan",)),
    },
    "ADO": {
        "ADO-PHASE": ("error", ("validation",)),
        "ADO-MANIFEST": ("error", ("validation",)),
    },
}

DORMANT = {"ADO-MANIFEST"}


class CatalogueRoster(unittest.TestCase):
    def test_exact_code_roster(self) -> None:
        expected = {code for family in T14.values() for code in family}
        self.assertEqual(expected, set(catalogue.CATALOGUE))

    def test_totals(self) -> None:
        self.assertEqual(79, len(catalogue.CATALOGUE))
        self.assertEqual(13, len({e.family for e in catalogue.CATALOGUE.values()}))
        active = [c for c, e in catalogue.CATALOGUE.items() if e.state == "active"]
        dormant = [c for c, e in catalogue.CATALOGUE.items() if e.state == "dormant"]
        self.assertEqual(78, len(active))
        self.assertEqual(DORMANT, set(dormant))

    def test_family_membership(self) -> None:
        for family, codes in T14.items():
            for code in codes:
                with self.subTest(code=code):
                    self.assertEqual(family, catalogue.CATALOGUE[code].family)

    def test_severity_per_code(self) -> None:
        for family in T14.values():
            for code, (severity, _stages) in family.items():
                with self.subTest(code=code):
                    self.assertEqual(severity, catalogue.CATALOGUE[code].severity)

    def test_exact_stage_lists(self) -> None:
        for family in T14.values():
            for code, (_severity, stages) in family.items():
                with self.subTest(code=code):
                    self.assertEqual(stages, catalogue.CATALOGUE[code].stages)

    def test_closed_vocabularies(self) -> None:
        self.assertEqual(
            frozenset({"error", "warning", "deferred"}), catalogue.SEVERITIES
        )
        self.assertEqual(
            frozenset({"validation", "plan", "apply", "generated-ci"}),
            catalogue.STAGES,
        )

    def test_warning_reserved_unpopulated(self) -> None:
        # Decision 1: warning is a reserved, presently unpopulated value.
        self.assertEqual(
            [], [c for c, e in catalogue.CATALOGUE.items() if e.severity == "warning"]
        )

    def test_every_code_cites_authority(self) -> None:
        # Decision 2 / T08 #13 d11: every code carries authority citations.
        for code, entry in catalogue.CATALOGUE.items():
            with self.subTest(code=code):
                self.assertTrue(entry.rule_ids)

    def test_dormant_code_names_activation(self) -> None:
        self.assertTrue(catalogue.CATALOGUE["ADO-MANIFEST"].activation)


class CatalogueSelfValidation(unittest.TestCase):
    def test_committed_catalogue_is_clean(self) -> None:
        self.assertEqual([], catalogue.validate_catalogue())

    def test_unknown_severity_fails_catalogue(self) -> None:
        # Decision 1: a severity outside the closed vocabulary fails validation
        # of the catalogue itself (error) - never a silent downgrade surface.
        broken = dict(catalogue.CATALOGUE)
        entry = broken["KEY-GRAMMAR"]
        broken["KEY-GRAMMAR"] = entry._replace(severity="info")
        defects = catalogue.validate_catalogue(broken)
        self.assertTrue(any("KEY-GRAMMAR" in d for d in defects))

    def test_unknown_stage_fails_catalogue(self) -> None:
        broken = dict(catalogue.CATALOGUE)
        entry = broken["CFG-FIELDS"]
        broken["CFG-FIELDS"] = entry._replace(stages=("compile",))
        defects = catalogue.validate_catalogue(broken)
        self.assertTrue(any("CFG-FIELDS" in d for d in defects))


if __name__ == "__main__":
    unittest.main()
