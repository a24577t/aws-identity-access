"""Catalog data production from the committed specification-7 SRI sources
(R2 #27 row 6).

The two ADM action catalogs generate ONLY from the exact raw AWS Service
Reference Information bytes accepted at
governance/catalogs/sources/sri-20260828/ (specification 7; SOURCES.md):

- every input's SHA-256 is verified against the 7.1 table BEFORE any parse;
  a mismatch aborts generation (fail closed); nothing is ever re-fetched and
  review staging is never consumed;
- hash verification operates on the canonical committed Git-blob bytes
  (repository byte-identity amendment): read_committed_blob reads
  `git cat-file blob :<path>`, never the working tree;
- the transformation is 7.3 exactly - an action is mutation iff
  IsWrite or IsPermissionManagement or IsTaggingOnly; a missing
  Annotations.Properties block, a missing boolean, or a non-boolean value
  aborts naming the action; action names are never classified by prefix or
  phrase;
- outputs are the 7.4 canonical form: UTF-8, LF, two-space indent, keys and
  arrays sorted byte-lexicographically, no timestamps (the retrieval
  timestamps in the sidecar are the 7.1 retrieval-evidence table, not
  generation state);
- the sidecar catalog-metadata.json carries the 7.1 table, the generator
  version, and the source-set identifier; the SHA-256 of the exact committed
  catalog bytes is pinned in the validator's committed catalog reference
  (src/validator/catalog_reference.json), which ADM rules 2/4 verify before
  every use.

Refreshing the inputs is a platform-change PR adding a new dated
sources/sri-<YYYYMMDD>/ set - never overwriting this one (SOURCES.md).
Run: python -m validator.catalog_generator [--check]
"""

import hashlib
import json
import subprocess
import sys
from collections import namedtuple
from pathlib import Path

GENERATOR_VERSION = "1"
SOURCE_SET = "sri-20260828"
SOURCE_DIR = f"governance/catalogs/sources/{SOURCE_SET}"

Source = namedtuple("Source", ["name", "url", "retrieved", "bytes", "sha256"])

_BASE = "https://servicereference.us-east-1.amazonaws.com"

# The specification 7.1 byte inventory - normative constants.
SOURCES = (
    Source("_index.json", f"{_BASE}/", "2026-08-28T00:46:16Z", 70396,
           "7cfe03fdd10349530045f654d5dc2c9455a1506eaf7ba20ea4225901a96b2dda"),
    Source("iam.json", f"{_BASE}/v1/iam/iam.json", "2026-08-28T00:46:43Z",
           131515,
           "0cc573ce2dec7e2122845c45961e9fa3448ef76d364fb800db98292e0e3d6d61"),
    Source("sso.json", f"{_BASE}/v1/sso/sso.json", "2026-08-28T00:46:43Z",
           86805,
           "b950f51b6311417d035088e8092f96b0c4018c0572ee83bef668c94422282e7a"),
    Source("identitystore.json", f"{_BASE}/v1/identitystore/identitystore.json",
           "2026-08-28T00:46:43Z", 22020,
           "fbb14245e33e72a636168c53b27d03f0584314991f14a5a2a2950edd309b98c8"),
    Source("sso-directory.json", f"{_BASE}/v1/sso-directory/sso-directory.json",
           "2026-08-28T00:46:43Z", 20299,
           "c03548fa4533682f3953b9b0ab583dd612beff2134c1425aa3f390e25ef5f70b"),
)

# 7.2 service scope: the four included IAM service prefixes; the service
# index is a verified input only. Exclusions recorded in the sidecar.
INCLUDED = ("iam", "sso", "identitystore", "sso-directory")
EXCLUDED = {
    "sso-oauth": "authentication flows, no configuration mutation",
    "identitystore-auth": "authentication flows, no configuration mutation",
    "identity-sync": "organization-side sync administration, outside T21's "
                     "named scope",
    "signin": "unrelated surface",
    "cognito-identity": "unrelated surface",
    "clouddirectory": "unrelated surface",
}

ANNOTATION_BOOLEANS = ("IsList", "IsPermissionManagement", "IsTaggingOnly",
                       "IsWrite")


class SourceIntegrityError(Exception):
    """A generation input whose bytes do not match its selected hash."""


class TransformationError(Exception):
    """An action entry the deterministic 7.3 rule cannot classify."""


# Give each Source its repository path.
Source.path = property(lambda self: f"{SOURCE_DIR}/{self.name}")


def read_committed_blob(path, repo=None):
    """The canonical committed bytes: `git cat-file blob :<path>` (the
    byte-identity amendment) - never a working-tree rendering."""
    root = Path(repo) if repo else Path(__file__).resolve().parents[2]
    result = subprocess.run(
        ["git", "cat-file", "blob", f":{path}"],
        cwd=root, capture_output=True, check=True,
    )
    return result.stdout


def _canonical_json(obj):
    return (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)
            + "\n").encode("utf-8")


def _classify(service, action):
    if not isinstance(action, dict) or not isinstance(action.get("Name"), str):
        raise TransformationError(
            f"{service}: action entry without a Name is unsupported")
    name = action["Name"]
    properties = (action.get("Annotations") or {}).get("Properties")
    if not isinstance(properties, dict):
        raise TransformationError(
            f"{service}:{name}: missing Annotations.Properties - nothing is "
            "guessed")
    for key in ANNOTATION_BOOLEANS:
        if not isinstance(properties.get(key), bool):
            raise TransformationError(
                f"{service}:{name}: annotation {key} missing or non-boolean "
                "- nothing is guessed")
    mutation = (properties["IsWrite"] or properties["IsPermissionManagement"]
                or properties["IsTaggingOnly"])
    return name, mutation


def generate(read_blob, sources=SOURCES):
    """Produce the three canonical output files as bytes.

    read_blob(path) -> bytes supplies each committed source; every input is
    hash-verified before any parse."""
    verified = {}
    for source in sources:
        blob = read_blob(source.path)
        digest = hashlib.sha256(blob).hexdigest()
        if digest != source.sha256 or len(blob) != source.bytes:
            raise SourceIntegrityError(
                f"{source.name}: committed bytes do not match the selected "
                f"7.1 hash - generation aborts (fail closed); refreshing "
                f"inputs is a platform-change PR adding a new dated set"
            )
        verified[source.name] = blob

    action_catalog = {}
    mutation_catalog = {}
    for prefix in INCLUDED:
        document = json.loads(verified[f"{prefix}.json"].decode("utf-8"))
        declared = document.get("Name")
        if declared != prefix:
            raise TransformationError(
                f"{prefix}.json declares service {declared!r}")
        actions = document.get("Actions")
        if not isinstance(actions, list):
            raise TransformationError(f"{prefix}.json carries no action list")
        names = []
        mutations = []
        for action in actions:
            name, mutation = _classify(prefix, action)
            names.append(name)
            if mutation:
                mutations.append(name)
        action_catalog[prefix] = sorted(names)
        mutation_catalog[prefix] = sorted(mutations)

    metadata = {
        "source_set": SOURCE_SET,
        "generator_version": GENERATOR_VERSION,
        "sources": [
            {"name": s.name, "url": s.url, "retrieved": s.retrieved,
             "bytes": s.bytes, "sha256": s.sha256}
            for s in sources
        ],
        "included_prefixes": sorted(INCLUDED),
        "excluded_prefixes": EXCLUDED,
        "transformation": "mutation iff IsWrite or IsPermissionManagement "
                          "or IsTaggingOnly (specification 7.3; no name "
                          "heuristics)",
    }
    return {
        "action-catalog.json": _canonical_json(action_catalog),
        "privileged-mutation-actions.json": _canonical_json(mutation_catalog),
        "catalog-metadata.json": _canonical_json(metadata),
    }


def reference_for(outputs):
    """The validator's committed catalog reference: digests of the exact
    catalog bytes (specification 7.4)."""
    return _canonical_json({
        "source_set": SOURCE_SET,
        "catalogs": {
            name: {"sha256": hashlib.sha256(outputs[name]).hexdigest(),
                   "bytes": len(outputs[name])}
            for name in ("action-catalog.json",
                         "privileged-mutation-actions.json")
        },
    })


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    check_only = "--check" in argv
    root = Path(__file__).resolve().parents[2]
    outputs = generate(read_committed_blob)
    targets = {
        root / "governance" / "catalogs" / name: blob
        for name, blob in outputs.items()
    }
    targets[root / "src" / "validator" / "catalog_reference.json"] = (
        reference_for(outputs)
    )
    drift = []
    for path, blob in targets.items():
        if not path.is_file() or path.read_bytes() != blob:
            drift.append(path)
    if check_only:
        if drift:
            for path in drift:
                print(f"DRIFT: {path}")
            return 1
        print("regeneration identical (deterministic)")
        return 0
    for path, blob in targets.items():
        path.write_bytes(blob)
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
