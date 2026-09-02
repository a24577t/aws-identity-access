"""The GEN-* checks - generated-artifact metadata (R3 #28 row 10;
T20 #22 d6).

Applicability: a target tree carrying generated artifacts - files under
docs/generated/** (documentation formats with the embedded envelope; the
central manifest itself) or the control-format .github/CODEOWNERS. A tree
with none of them is clean: there is nothing generated to bind.

- GEN-MANIFEST (validation, generated-ci): the central manifest at its
  fixed path is missing while generated artifacts exist; malformed or
  misordered (entries sorted lexicographically by target.path; the schema
  field order and shapes of d6); a bound target's whole-file SHA-256
  mismatch; a generated artifact absent from the manifest.
- GEN-ENVELOPE: a documentation-format generated file missing its embedded
  envelope, malformed or misordered envelope fields, a target.path naming a
  different file, or a whole-target self-digest (self-referential - d6
  prohibits it; whole-file digests live only in the manifest).
- GEN-CODEOWNERS: .github/CODEOWNERS not valid CODEOWNERS syntax, carrying
  an embedded envelope (invalid for its consumer), or absent from the
  manifest.
- GEN-DRIFT (generated-ci): a pipeline-supplied regeneration
  (RunConfig.regenerated: {path: bytes}) differing from the committed
  bytes - deterministic regeneration must be identical (spec 8.2; hand
  edits are rejected by this comparison).
"""

import hashlib
import re

import yaml

MANIFEST_PATH = "docs/generated/generated-artifacts.yml"
GENERATED_PREFIX = "docs/generated/"
CODEOWNERS_PATH = ".github/CODEOWNERS"

ENVELOPE_KEY_ORDER = ("authority", "do_not_edit", "generator", "sources",
                      "target")
_TOP_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):", re.MULTILINE)
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")


def _entry_defect(entry):
    """The first structural defect of one manifest entry, or None."""
    if not isinstance(entry, dict):
        return "entry is not a mapping"
    target = entry.get("target")
    if not isinstance(target, dict) or not isinstance(target.get("path"), str) \
            or not isinstance(target.get("sha256"), str) \
            or not _HEX64_RE.match(target["sha256"]):
        return "target must carry path and a 64-hex whole-file sha256"
    generator = entry.get("generator")
    if not isinstance(generator, dict) \
            or not isinstance(generator.get("path"), str) \
            or not isinstance(generator.get("version"), str):
        return "generator must carry path and version"
    sources = entry.get("sources")
    if not isinstance(sources, list) or not sources:
        return "sources must be a non-empty list"
    for source in sources:
        if not isinstance(source, dict):
            return "source entry is not a mapping"
        if isinstance(source.get("path"), str):
            revision = source.get("revision")
            if not isinstance(revision, str) or not _HEX40_RE.match(revision):
                return "repository source without its exact 40-hex commit"
        elif isinstance(source.get("artifact"), str):
            digest = source.get("sha256")
            if not isinstance(digest, str) or not _HEX64_RE.match(digest):
                return "artifact source without its labeled digest"
        else:
            return "source is neither a repository path nor an artifact"
    return None


def _envelope(text):
    """(frontmatter dict, raw frontmatter text) or (None, None)."""
    if not text.startswith("---\n"):
        return None, None
    end = text.find("\n---", 4)
    if end < 0:
        return None, None
    raw = text[4:end + 1]
    try:
        header = yaml.safe_load(raw)
    except Exception:
        return None, raw
    return (header if isinstance(header, dict) else None), raw


def check_generated(ctx):
    files = ctx.files()
    generated = [f for f in files
                 if f.startswith(GENERATED_PREFIX) and f != MANIFEST_PATH]
    has_codeowners = CODEOWNERS_PATH in files
    manifest_present = MANIFEST_PATH in files
    if not generated and not has_codeowners and not manifest_present:
        return

    bound = {}
    if manifest_present:
        try:
            entries = yaml.safe_load(
                ctx.read_bytes(MANIFEST_PATH).decode("utf-8"))
        except Exception:
            entries = None
        if not isinstance(entries, list):
            ctx.emit("GEN-MANIFEST", file_path=MANIFEST_PATH,
                     message="manifest malformed: not a YAML entry list")
            entries = []
        paths = []
        for index, entry in enumerate(entries):
            defect = _entry_defect(entry)
            if defect:
                ctx.emit("GEN-MANIFEST", file_path=MANIFEST_PATH,
                         field_path=f"/{index}",
                         message=f"manifest malformed: {defect}")
                continue
            path = entry["target"]["path"]
            paths.append(path)
            bound[path] = entry["target"]["sha256"]
            if path not in files:
                ctx.emit("GEN-MANIFEST", file_path=MANIFEST_PATH,
                         field_path=f"/{index}", value=path,
                         message="manifest binds an absent target")
            elif hashlib.sha256(ctx.read_bytes(path)).hexdigest() \
                    != bound[path]:
                ctx.emit("GEN-MANIFEST", file_path=path,
                         message="whole-file digest mismatch with the "
                                 "manifest binding")
        if paths != sorted(paths):
            ctx.emit("GEN-MANIFEST", file_path=MANIFEST_PATH,
                     message="manifest misordered: entries must sort "
                             "lexicographically by target.path")
    elif generated:
        ctx.emit("GEN-MANIFEST", file_path=MANIFEST_PATH,
                 message="generated artifacts exist without the central "
                         "manifest at its fixed path")

    for rel in generated:
        if manifest_present and rel not in bound:
            ctx.emit("GEN-MANIFEST", file_path=rel,
                     message="generated artifact absent from the manifest")
        if rel.endswith((".md", ".markdown")):
            _check_envelope(ctx, rel)

    if has_codeowners:
        _check_codeowners(ctx, bound if manifest_present else None)


def _check_envelope(ctx, rel):
    try:
        text = ctx.read_bytes(rel).decode("utf-8")
    except UnicodeDecodeError:
        ctx.emit("GEN-ENVELOPE", file_path=rel,
                 message="generated documentation file is not readable text")
        return
    header, raw = _envelope(text)
    if header is None:
        ctx.emit("GEN-ENVELOPE", file_path=rel,
                 message="embedded envelope missing or malformed where "
                         "required (documentation format)")
        return
    keys = tuple(_TOP_KEY_RE.findall(raw))
    if keys != ENVELOPE_KEY_ORDER[:len(keys)] or set(header) != set(
            ENVELOPE_KEY_ORDER):
        top = tuple(k for k in keys if k in set(ENVELOPE_KEY_ORDER))
        if top != ENVELOPE_KEY_ORDER or set(header) != set(ENVELOPE_KEY_ORDER):
            ctx.emit("GEN-ENVELOPE", file_path=rel,
                     message="envelope fields must be exactly the d6 schema "
                             "in schema order")
            return
    if header.get("authority") != "generated" \
            or header.get("do_not_edit") is not True:
        ctx.emit("GEN-ENVELOPE", file_path=rel,
                 message="envelope must declare authority: generated and "
                         "do_not_edit: true")
        return
    target = header.get("target")
    if not isinstance(target, dict) or target.get("path") != rel:
        ctx.emit("GEN-ENVELOPE", file_path=rel, field_path="/target/path",
                 message="envelope target.path must name this exact file")
        return
    if "sha256" in target or "digest" in target:
        ctx.emit("GEN-ENVELOPE", file_path=rel, field_path="/target",
                 message="whole-target self-digest is self-referential and "
                         "prohibited - whole-file digests live only in the "
                         "manifest (T20 #22 d6)")


def _check_codeowners(ctx, bound):
    try:
        text = ctx.read_bytes(CODEOWNERS_PATH).decode("utf-8")
    except UnicodeDecodeError:
        ctx.emit("GEN-CODEOWNERS", file_path=CODEOWNERS_PATH,
                 message="CODEOWNERS is not readable text")
        return
    if text.startswith("---"):
        ctx.emit("GEN-CODEOWNERS", file_path=CODEOWNERS_PATH,
                 message="an embedded envelope is invalid CODEOWNERS syntax "
                         "for its consumer - metadata lives in the manifest "
                         "only (T20 #22 d6)")
        return
    for line_no, line in enumerate(text.split("\n"), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split()
        if len(parts) < 2 or not all(p.startswith("@") for p in parts[1:]):
            ctx.emit("GEN-CODEOWNERS", file_path=CODEOWNERS_PATH,
                     field_path=f"L{line_no}",
                     message="not valid CODEOWNERS syntax: pattern plus at "
                             "least one @owner per rule line")
            return
    if bound is not None and CODEOWNERS_PATH not in bound:
        ctx.emit("GEN-CODEOWNERS", file_path=CODEOWNERS_PATH,
                 message="generated CODEOWNERS absent from the manifest")


def check_drift(ctx):
    regenerated = ctx.config.regenerated
    if not regenerated:
        return
    for rel in sorted(regenerated):
        try:
            committed = ctx.read_bytes(rel)
        except FileNotFoundError:
            committed = None
        if committed != regenerated[rel]:
            ctx.emit("GEN-DRIFT", file_path=rel,
                     message="deterministic regeneration produced different "
                             "bytes - hand edits and drift are rejected "
                             "(spec 8.2)")
