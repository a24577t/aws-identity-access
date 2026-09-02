"""CI wiring for the R4 #29 row-11 workflow files (T15 #10 d15; T20 #22
d1-d5; T06 #8 d4).

Thin command seams the committed workflows invoke. Orchestration lives in
`.github/workflows/**`; every deterministic validation, classification,
generation, and rendering behavior reached from here is an existing public
validator seam (`runner.run`, `render_preview` / `render_summary` /
`summary_digest`, `governance_generator.generate`,
`catalog_generator.generate` / `reference_for`). This module adds transport
and gating only: staging committed bytes into a run target, feeding the
explicit run inputs those seams already accept (`changed_paths`,
`regenerated`, `plan_context`, `inventory_fixture`, `resolution_paths`),
serializing findings, and mapping severities to exit codes - any `error`
finding exits 1 (fail closed); `deferred` findings report and never fail
(RD-08).

Byte identity: staged inputs are committed-blob bytes (repository
byte-identity amendment), never a working-tree rendering - read from the
local git object store at HEAD (`GitSources`), or from an export directory
produced by `export` where git lives (the CI runner - transport only,
spec 8.1) and consumed inside the pinned container, which carries no git.

The validation target domain is the governed surface set the accepted
validator models and the accepted valid fixture tree mirrors (T14 #19 d6):
the requester surface, the governance registry/declaration/inventory
surfaces, the T23 #23 documentation boundary, and the infrastructure root.
Wider repository content (wayfinding records, research, methodology) is
documentation evidence outside the modeled validation domain; reference
resolution still sees the whole committed path inventory
(RunConfig.resolution_paths).

Run: python -m validator.ci <command> - identical commands locally and in
CI (spec 8.2); `--export` swaps only the committed-byte transport.
Validator imports are deferred into the commands that need them: `export`
is the one transport command that runs where git lives (the CI runner,
stdlib-only Python - spec 8.1: the runner is transport); every other
command runs inside the pinned container, where the hash-locked
dependencies are installed.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

VALIDATE_PREFIXES = (
    "access/",
    "docs/architecture/",
    "docs/guides/",
    "governance/change-declarations/",
    "governance/inventory/",
    "governance/ownership/",
    "infrastructure/",
)
# Contract paths owned by the generator/validator modules; the wiring keeps
# import-free literals so `export` stays stdlib-only, and the wiring suite
# asserts equality with the owning constants.
FIXTURE_REL = "governance/inventory/lab-inventory-fixture.yml"
CODEOWNERS_REL = ".github/CODEOWNERS"
HANDLES_REL = "governance/ownership/handles.yml"
GENERATED_PREFIXES = (CODEOWNERS_REL, "docs/generated/")
CATALOG_DIR = "governance/catalogs"
CATALOG_REFERENCE = "src/validator/catalog_reference.json"

_ISO_INSTANT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class ExportedSources:
    """Committed-byte sources from an `export` directory: `tree/` carries
    every tracked blob at HEAD; `revisions.tsv` carries each path's
    last-touch commit (path<TAB>40-hex). Same read/ls/revision contract as
    GitSources, with no git dependency - the pinned container consumes it."""

    def __init__(self, root):
        self.root = Path(root)
        self.tree = self.root / "tree"
        self._revisions = {}
        tsv = self.root / "revisions.tsv"
        if tsv.is_file():
            for line in tsv.read_text(encoding="utf-8").splitlines():
                path, sep, revision = line.partition("\t")
                if sep and path:
                    self._revisions[path] = revision.strip()

    def read(self, path):
        full = self.tree / path
        return full.read_bytes() if full.is_file() else None

    def ls(self, prefix):
        if not self.tree.is_dir():
            return []
        if prefix == ".":
            # The repository-inventory listing (GitSources spells it as the
            # "." pathspec; here everything under tree/ is the inventory).
            prefix = ""
        return sorted(
            p.relative_to(self.tree).as_posix()
            for p in self.tree.rglob("*")
            if p.is_file()
            and p.relative_to(self.tree).as_posix().startswith(prefix)
        )

    def revision(self, path):
        return self._revisions.get(path)


def _source(args):
    export = getattr(args, "export", None)
    if export:
        return ExportedSources(export)
    from .governance_generator import GitSources
    return GitSources()


def _stage(source, prefixes, staged_root):
    """Write the committed bytes of every path under the prefixes (or the
    exact path, for a non-directory prefix) into the staged run target."""
    staged = Path(staged_root)
    for prefix in prefixes:
        rels = source.ls(prefix) if prefix.endswith("/") else (
            [prefix] if source.read(prefix) is not None else [])
        for rel in rels:
            blob = source.read(rel)
            dest = staged / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(blob)
    return staged


def _fixture_config(staged, source=None, **kwargs):
    from .runner import RunConfig

    fixture = Path(staged) / FIXTURE_REL
    if source is not None and "resolution_paths" not in kwargs:
        # The repository's committed path inventory: reference resolution is
        # repository-wide even though the run target is a staged subdomain.
        kwargs["resolution_paths"] = source.ls(".")
    return RunConfig(
        inventory_fixture=str(fixture) if fixture.is_file() else None,
        **kwargs)


def _emit(items, findings_path):
    """Serialize canonically, persist, and gate: error -> 1 (fail closed);
    deferred reports and never fails (RD-08)."""
    from . import findings

    blob = findings.serialize(items)
    if findings_path:
        Path(findings_path).parent.mkdir(parents=True, exist_ok=True)
        Path(findings_path).write_bytes(blob)
    sys.stdout.write(blob.decode("ascii"))
    return 1 if any(f.severity == "error" for f in items) else 0


def cmd_export(args):
    """Transport: materialize HEAD's committed bytes and last-touch
    revisions where git lives, for consumption where it does not."""
    root = Path(__file__).resolve().parents[2]

    def git(*cmd):
        return subprocess.run(["git", *cmd], cwd=root, capture_output=True,
                              check=True).stdout

    out = Path(args.out)
    tree = out / "tree"
    tree.mkdir(parents=True, exist_ok=True)
    paths = sorted(
        line for line in
        git("ls-tree", "-r", "--name-only", "HEAD").decode("utf-8").split("\n")
        if line)
    lines = []
    for rel in paths:
        dest = tree / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(git("cat-file", "blob", f"HEAD:{rel}"))
        revision = git("log", "-1", "--format=%H", "HEAD", "--",
                       rel).decode("utf-8").strip()
        lines.append(f"{rel}\t{revision}")
    (out / "revisions.tsv").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"exported {len(paths)} committed blobs to {out}")
    return 0


def cmd_validate(args):
    """The `validate` check: the validation stage over the staged governed
    domain, with the committed inventory fixture as its explicit input."""
    from . import runner

    source = _source(args)
    with tempfile.TemporaryDirectory() as tmp:
        staged = _stage(source, VALIDATE_PREFIXES, tmp)
        items = runner.run("validation", staged,
                           _fixture_config(staged, source))
        return _emit(items, args.findings)


def cmd_plan_preview(args):
    """The `plan-preview` check: the T20 #22 d2 classification arms over
    the PR's changed paths plus the sanitized, snapshot-blind,
    never-apply-eligible preview rendering (T15 #10 d15)."""
    from . import runner
    from .effective_access import render_preview

    changed = [
        line.strip()
        for line in Path(args.changed_paths).read_text(
            encoding="utf-8").splitlines()
        if line.strip()
    ]
    source = _source(args)
    with tempfile.TemporaryDirectory() as tmp:
        staged = _stage(source, VALIDATE_PREFIXES, tmp)
        config = _fixture_config(staged, source, changed_paths=changed)
        items = runner.run("validation", staged, config)
        preview = render_preview(staged, config)
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_bytes(preview)
        return _emit(items, args.findings)


def cmd_generated_check(args):
    """Regeneration determinism as a CI check (GEN-DRIFT, spec 8.2):
    regenerate the governance set and both catalogs from committed bytes,
    and run the generated-ci stage over the committed generated artifacts
    with the regeneration as its explicit run input."""
    import yaml

    from . import catalog_generator, governance_generator, runner

    source = _source(args)
    regenerated = governance_generator.generate(source)
    handles_doc = yaml.safe_load(source.read(HANDLES_REL).decode("utf-8"))
    committed_codeowners = source.read(CODEOWNERS_REL)
    with tempfile.TemporaryDirectory() as tmp:
        staged = _stage(source, GENERATED_PREFIXES, tmp)
        config = _fixture_config(
            staged,
            regenerated=regenerated,
            handle_mapping=(handles_doc or {}).get("handles"),
            codeowners=(committed_codeowners or b"").decode("utf-8"),
        )
        items = runner.run("generated-ci", staged, config)
        code = _emit(items, args.findings)

    catalogs = catalog_generator.generate(source.read)
    catalog_targets = {
        f"{CATALOG_DIR}/{name}": blob for name, blob in catalogs.items()
    }
    catalog_targets[CATALOG_REFERENCE] = catalog_generator.reference_for(
        catalogs)
    drift = [rel for rel, blob in sorted(catalog_targets.items())
             if source.read(rel) != blob]
    for rel in drift:
        print(f"CATALOG-DRIFT: {rel}")
    if not drift:
        print("catalog regeneration identical (deterministic)")
    return 1 if drift else code


def cmd_lab_plan(args):
    """The post-merge lab-plan derivation: the plan-stage battery over the
    explicit plan-context input, then - only on a clean gate - the
    digest-bound effective-access summary (one generator, two renderings)
    and the T06 #8 d4 authorization-binding record. Fail closed: an error
    finding leaves no summary and no binding."""
    from . import runner
    from .effective_access import PINS, render_summary, summary_digest

    if args.target:
        # Specimen mode (tests): the explicit target tree is both the run
        # target and the resolution domain.
        staged_ctx = None
        staged = Path(args.target)
        source = None
    else:
        staged_ctx = tempfile.TemporaryDirectory()
        source = _source(args)
        staged = _stage(source, VALIDATE_PREFIXES, staged_ctx.name)
    try:
        config = _fixture_config(staged, source, plan_context=args.context)
        items = runner.run("plan", staged, config)
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        code = _emit(items, args.findings or out / "findings.json")
        if code:
            return code
        summary = render_summary(staged, config)
        (out / "effective-access-summary.md").write_bytes(summary)
        context = json.loads(
            Path(args.context).read_text(encoding="utf-8"))
        plan_blob = Path(args.plan_file).read_bytes()
        fixture = Path(staged) / FIXTURE_REL
        binding = {
            "schema_version": 1,
            "plan_sha256": hashlib.sha256(plan_blob).hexdigest(),
            "summary_sha256": summary_digest(summary),
            "source_commit": args.source_commit,
            "snapshot_id": context.get("current_pointer"),
            "fixture_path": FIXTURE_REL,
            "fixture_sha256": (
                hashlib.sha256(fixture.read_bytes()).hexdigest()
                if fixture.is_file() else None),
            "deployment_scope": "lab",
            "pins": {name: value for name, value in PINS},
            "expires": args.expires,
        }
        (out / "authorization-binding.json").write_text(
            json.dumps(binding, indent=2, sort_keys=True) + "\n",
            encoding="utf-8", newline="\n")
        print(f"summary digest {binding['summary_sha256']}")
        return 0
    finally:
        if staged_ctx is not None:
            staged_ctx.cleanup()


def cmd_verify_binding(args):
    """The lab consumption rule's fail-closed verification (T06 #8 d4;
    T15 #10 d15): re-verify every bound input before anything else runs -
    any change invalidates the authorization; one binding, one plan, one
    attempt. Expiry compares ISO-8601 UTC instants (the pipeline supplies
    the clock; this validator core holds none)."""
    from .effective_access import summary_digest

    binding = json.loads(Path(args.binding).read_text(encoding="utf-8"))
    results = []

    def check(name, ok):
        results.append(bool(ok))
        print(f"{'ok' if ok else 'INVALID'}: {name}")

    plan_digest = hashlib.sha256(
        Path(args.plan_file).read_bytes()).hexdigest()
    summary_blob = Path(args.summary).read_bytes()
    check("plan_sha256", binding.get("plan_sha256") == plan_digest)
    check("summary_sha256",
          binding.get("summary_sha256") == summary_digest(summary_blob))
    check("source_commit",
          isinstance(binding.get("source_commit"), str)
          and binding["source_commit"] == args.source_commit)
    check("snapshot_id",
          isinstance(binding.get("snapshot_id"), str)
          and bool(binding["snapshot_id"]))
    check("fixture_sha256",
          isinstance(binding.get("fixture_sha256"), str)
          and bool(binding["fixture_sha256"]))
    expires = binding.get("expires")
    well_formed = (isinstance(expires, str) and _ISO_INSTANT.match(expires)
                   and _ISO_INSTANT.match(args.now))
    check("expiry_form", well_formed)
    check("unexpired", bool(well_formed) and args.now < expires)
    return 0 if all(results) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(prog="validator.ci")
    commands = parser.add_subparsers(dest="command", required=True)

    export = commands.add_parser("export")
    export.add_argument("--out", required=True)
    export.set_defaults(fn=cmd_export)

    validate = commands.add_parser("validate")
    validate.add_argument("--export")
    validate.add_argument("--findings")
    validate.set_defaults(fn=cmd_validate)

    preview = commands.add_parser("plan-preview")
    preview.add_argument("--export")
    preview.add_argument("--changed-paths", required=True)
    preview.add_argument("--out", required=True)
    preview.add_argument("--findings")
    preview.set_defaults(fn=cmd_plan_preview)

    generated = commands.add_parser("generated-check")
    generated.add_argument("--export")
    generated.add_argument("--findings")
    generated.set_defaults(fn=cmd_generated_check)

    lab_plan = commands.add_parser("lab-plan")
    lab_plan.add_argument("--export")
    lab_plan.add_argument("--target")
    lab_plan.add_argument("--context", required=True)
    lab_plan.add_argument("--plan-file", required=True)
    lab_plan.add_argument("--source-commit", required=True)
    lab_plan.add_argument("--expires", required=True)
    lab_plan.add_argument("--out-dir", required=True)
    lab_plan.add_argument("--findings")
    lab_plan.set_defaults(fn=cmd_lab_plan)

    verify = commands.add_parser("verify-binding")
    verify.add_argument("--binding", required=True)
    verify.add_argument("--plan-file", required=True)
    verify.add_argument("--summary", required=True)
    verify.add_argument("--source-commit", required=True)
    verify.add_argument("--now", required=True)
    verify.set_defaults(fn=cmd_verify_binding)

    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
