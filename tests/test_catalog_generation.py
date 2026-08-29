"""R2 #27 row-6 external checks - catalog data production from the committed
specification-7 sources: pre-parse blob-hash verification (fail closed;
byte-identity amendment), the deterministic 7.3 transformation (no name
heuristics; abort on missing or non-boolean annotations), the 7.4 canonical
output form, byte-determinism of regeneration, the pinned catalog reference,
and the resulting executability of ADM rules 2/4.
"""

import hashlib
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from validator import catalog_generator as gen  # noqa: E402

HAS_GIT = shutil.which("git") is not None


class SourceVerification(unittest.TestCase):
    def test_tampered_bytes_abort_before_parse(self) -> None:
        def read_blob(path):
            return b"{} tampered"

        with self.assertRaises(gen.SourceIntegrityError) as caught:
            gen.generate(read_blob)
        self.assertIn("_index.json", str(caught.exception))

    def test_the_table_is_the_specification_table(self) -> None:
        # Spot-check the 7.1 constants against the specification literals.
        table = {s.name: s for s in gen.SOURCES}
        self.assertEqual(
            "7cfe03fdd10349530045f654d5dc2c9455a1506eaf7ba20ea4225901a96b2dda",
            table["_index.json"].sha256,
        )
        self.assertEqual(131515, table["iam.json"].bytes)
        self.assertEqual(
            "c03548fa4533682f3953b9b0ab583dd612beff2134c1425aa3f390e25ef5f70b",
            table["sso-directory.json"].sha256,
        )
        self.assertEqual(
            ["_index.json", "iam.json", "identitystore.json",
             "sso-directory.json", "sso.json"],
            sorted(table),
        )


class Transformation(unittest.TestCase):
    def synthetic(self, action):
        payloads = {}
        for source in gen.SOURCES:
            if source.name == "_index.json":
                body = json.dumps([]).encode()
            else:
                doc = {"Name": source.name.removesuffix(".json"),
                       "Actions": [action], "Version": "v1"}
                body = json.dumps(doc).encode()
            payloads[source.path] = body
        table = [
            source._replace(bytes=len(payloads[source.path]),
                            sha256=hashlib.sha256(
                                payloads[source.path]).hexdigest())
            for source in gen.SOURCES
        ]
        return payloads, table

    def test_missing_annotation_aborts_naming_the_action(self) -> None:
        payloads, table = self.synthetic({"Name": "DoThing"})
        with self.assertRaises(gen.TransformationError) as caught:
            gen.generate(lambda p: payloads[p], sources=table)
        self.assertIn("DoThing", str(caught.exception))

    def test_non_boolean_annotation_aborts(self) -> None:
        payloads, table = self.synthetic({
            "Name": "DoThing",
            "Annotations": {"Properties": {
                "IsList": False, "IsPermissionManagement": False,
                "IsTaggingOnly": False, "IsWrite": "yes"}},
        })
        with self.assertRaises(gen.TransformationError):
            gen.generate(lambda p: payloads[p], sources=table)

    def test_mutation_rule_is_the_annotation_disjunction(self) -> None:
        payloads, table = self.synthetic({
            "Name": "TagThing",
            "Annotations": {"Properties": {
                "IsList": False, "IsPermissionManagement": False,
                "IsTaggingOnly": True, "IsWrite": False}},
        })
        outputs = gen.generate(lambda p: payloads[p], sources=table)
        actions = json.loads(outputs["action-catalog.json"])
        mutations = json.loads(outputs["privileged-mutation-actions.json"])
        for prefix in ("iam", "sso", "identitystore", "sso-directory"):
            self.assertEqual(["TagThing"], actions[prefix])
            self.assertEqual(["TagThing"], mutations[prefix])


@unittest.skipUnless(HAS_GIT, "blob reading needs git (byte-identity "
                              "amendment: canonical bytes are the committed "
                              "blob, never the working tree)")
class CommittedGeneration(unittest.TestCase):
    def test_generation_is_byte_deterministic(self) -> None:
        one = gen.generate(gen.read_committed_blob)
        two = gen.generate(gen.read_committed_blob)
        self.assertEqual(one, two)

    def test_output_form_is_canonical(self) -> None:
        outputs = gen.generate(gen.read_committed_blob)
        actions = outputs["action-catalog.json"]
        self.assertNotIn(b"\r", actions)
        self.assertTrue(actions.endswith(b"\n"))
        parsed = json.loads(actions)
        self.assertEqual(
            ["iam", "identitystore", "sso", "sso-directory"], list(parsed)
        )
        for names in parsed.values():
            self.assertEqual(sorted(names), names)
            self.assertEqual(len(set(names)), len(names))
        # The pinned iam source carries 190 action entries.
        self.assertEqual(190, len(parsed["iam"]))

    def test_known_classifications(self) -> None:
        outputs = gen.generate(gen.read_committed_blob)
        actions = json.loads(outputs["action-catalog.json"])
        mutations = json.loads(outputs["privileged-mutation-actions.json"])
        self.assertIn("GetUser", actions["iam"])
        self.assertNotIn("GetUser", mutations["iam"])
        self.assertIn("CreateUser", mutations["iam"])
        self.assertIn("AttachUserPolicy", mutations["iam"])

    def test_sidecar_carries_the_table_and_version(self) -> None:
        outputs = gen.generate(gen.read_committed_blob)
        metadata = json.loads(outputs["catalog-metadata.json"])
        self.assertEqual("sri-20260828", metadata["source_set"])
        self.assertEqual(gen.GENERATOR_VERSION, metadata["generator_version"])
        self.assertEqual(5, len(metadata["sources"]))
        by_name = {s["name"]: s for s in metadata["sources"]}
        self.assertEqual(131515, by_name["iam.json"]["bytes"])

    def test_committed_catalogs_match_regeneration(self) -> None:
        # GEN-DRIFT's substance, run here as a row-6 acceptance check.
        outputs = gen.generate(gen.read_committed_blob)
        for name, blob in outputs.items():
            with self.subTest(file=name):
                committed = (REPO / "governance" / "catalogs" / name)
                self.assertTrue(committed.is_file(), f"{name} not committed")
                self.assertEqual(blob, committed.read_bytes())

    def test_committed_reference_pins_the_committed_bytes(self) -> None:
        reference = json.loads(
            (REPO / "src" / "validator" / "catalog_reference.json")
            .read_text(encoding="utf-8")
        )
        for name in ("action-catalog.json", "privileged-mutation-actions.json"):
            with self.subTest(file=name):
                committed = (REPO / "governance" / "catalogs" / name).read_bytes()
                self.assertEqual(
                    hashlib.sha256(committed).hexdigest(),
                    reference["catalogs"][name]["sha256"],
                )


class RulesTwoAndFourExecutable(unittest.TestCase):
    """With the pinned catalogs committed, ADM rules 2/4 are executable."""

    def setUp(self) -> None:
        import tempfile

        from tests.test_validator_governance_families import GovTreeCase

        class Case(GovTreeCase):
            def runTest(self):  # pragma: no cover
                pass

        self.case = Case()
        self.case.setUp()

    def tearDown(self) -> None:
        self.case.tmp.cleanup()

    def _codes(self, statements):
        self.case.write(
            "access/identity-center/permission-sets/wild.yml",
            "key: wild\ndescription: Specimen.\nsession_duration: PT1H\n"
            "inline_policy:\n  Version: \"2012-10-17\"\n  Statement:\n"
            + "\n".join(statements) + "\n",
        )
        return self.case.codes()

    def test_unbounded_iam_mutation_via_wildcard_fires(self) -> None:
        self.assertEqual(
            ["ADM-CAPABLE"],
            self._codes([
                "    - Effect: Allow",
                "      Action: [\"iam:*\"]",
                "      Resource: \"*\"",
            ]),
        )

    def test_bounded_wildcard_expansion_passes(self) -> None:
        self.assertEqual(
            [],
            self._codes([
                "    - Effect: Allow",
                "      Action: [\"iam:Get*\", \"iam:List*\"]",
                "      Resource: \"*\"",
            ]),
        )

    def test_prefix_outside_catalog_is_expansion_inability(self) -> None:
        self.assertEqual(
            ["ADM-CATALOG"],
            self._codes([
                "    - Effect: Allow",
                "      Action: [\"ec2:*\"]",
                "      Resource: \"*\"",
            ]),
        )


if __name__ == "__main__":
    unittest.main()
