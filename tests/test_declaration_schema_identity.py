"""R1 #26 row-8 mechanical check: the declaration schemas wired under
governance/change-declarations/schemas/ agree byte-for-byte with the row-2
schema content under schemas/governance/change-declaration/ (ticket #26 row 8
acceptance criterion; the configuration contract prevails over both)."""

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUTHORED = REPO / "schemas" / "governance" / "change-declaration"
WIRED = REPO / "governance" / "change-declarations" / "schemas"

KINDS = [
    "principal-replacement",
    "group-key-rename",
    "permission-set-key-replacement",
]


class DeclarationSchemaByteIdentity(unittest.TestCase):
    def test_wired_copies_are_byte_identical(self) -> None:
        for kind in KINDS:
            with self.subTest(kind=kind):
                authored = (AUTHORED / f"{kind}.schema.json").read_bytes()
                wired = (WIRED / f"{kind}.schema.json").read_bytes()
                self.assertEqual(authored, wired)

    def test_no_extra_wired_schema(self) -> None:
        wired = sorted(p.name for p in WIRED.glob("*.schema.json"))
        self.assertEqual(sorted(f"{k}.schema.json" for k in KINDS), wired)


if __name__ == "__main__":
    unittest.main()
