"""The validator run seam (R2 #27 row 3).

One public entry: run(stage, target, config) -> canonically ordered findings.
Stages are the closed T14 #19 d3 vocabulary. The hermetic boundary is
enforced structurally: the validation stage refuses a plan context and holds
no clock, snapshot, evidence, or AWS input (T22 #21 d4; T09 #12 d15; T15 #10
d6); plan and apply require their explicit plan-context input - this validator
core never contacts AWS itself, the pipeline supplies the stage's facts.
Locators derive from canonical traversal of the canonically ordered input
domain: files in byte-lexicographic path order, document order within a file
(T14 #19 C14) - never from filesystem enumeration order.
"""

from pathlib import Path

from . import catalogue, findings, leak


class RunConfig:
    """Explicit run inputs - everything the checks may consume.

    resource_name_prefix: the deployment-scope prefix (T15 #10 d8 selects
    ialab-); part of run configuration so the prefix-budget rule is checkable.
    inventory_fixture: path to the committed labeled lab inventory fixture
    consumed by validation-stage INV checks (T09 #12 d3).
    plan_context: the plan/apply-stage input document (snapshot envelope,
    controlled clock, live facts, evidence stubs) - prohibited at validation.
    handle_mapping / codeowners: generated-ci-stage inputs (GOV-CODEOWNERS).
    """

    def __init__(self, resource_name_prefix="ialab-", inventory_fixture=None,
                 plan_context=None, handle_mapping=None, codeowners=None):
        self.resource_name_prefix = resource_name_prefix
        self.inventory_fixture = inventory_fixture
        self.plan_context = plan_context
        self.handle_mapping = handle_mapping
        self.codeowners = codeowners


class Context:
    """Per-run state handed to checks."""

    def __init__(self, stage, target, config):
        self.stage = stage
        self.target = Path(target)
        self.config = config
        self.findings = []
        self._cache = {}

    def emit(self, code, file_path=None, field_path=None, value=None,
             message=""):
        entry = catalogue.CATALOGUE[code]
        self.findings.append(
            findings.Finding(
                code=code,
                stage=self.stage,
                file_path=file_path,
                field_path=field_path,
                rule_ids=entry.rule_ids,
                value=value,
                message=message,
            )
        )

    def files(self):
        """Every regular file under the target, repo-relative POSIX paths,
        byte-lexicographic order (C14 canonical traversal)."""
        key = "files"
        if key not in self._cache:
            paths = [
                p.relative_to(self.target).as_posix()
                for p in self.target.rglob("*")
                if p.is_file()
            ]
            self._cache[key] = sorted(paths)
        return self._cache[key]

    def read_bytes(self, rel):
        return (self.target / rel).read_bytes()


# Check registry: (name, frozenset of stages, callable(Context) -> None).
# Populated by the family modules; the row-3 core registers the leak rule.
CHECKS = []


def register(name, stages, fn):
    CHECKS.append((name, frozenset(stages), fn))


def run(stage, target, config=None):
    """Run every registered check for the stage; return canonical findings."""
    config = config or RunConfig()
    if stage not in catalogue.STAGES:
        raise findings.ContractViolation(
            f"stage {stage!r} outside the closed stage vocabulary"
        )
    if stage == "validation" and config.plan_context is not None:
        raise findings.ContractViolation(
            "hermetic boundary: the validation stage holds no clock and reads "
            "no snapshot, evidence, or plan context (T22 #21 d4)"
        )
    if stage in ("plan", "apply") and config.plan_context is None:
        raise findings.ContractViolation(
            f"the {stage} stage requires its explicit plan-context input"
        )
    ctx = Context(stage, target, config)
    for _name, stages, fn in CHECKS:
        if stage in stages:
            fn(ctx)
    return findings.canonical(ctx.findings)


register("public-leak", ("validation", "generated-ci"), leak.check_tree)
