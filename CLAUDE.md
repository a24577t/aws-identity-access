# aws-identity-access — agent configuration

Project-specific engineering rules and navigation for AI participants. Pointer-first:
governance, methodology, and state are owned under [`.ai/`](.ai/README.md); this file
never restates them.

## Entry points

- Repository owner: [`.ai/repository-owner/bootstrap.md`](.ai/repository-owner/bootstrap.md).
- Collaborator (instructor / architect / reviewer / quality gate):
  [`.ai/collaborator/bootstrap.md`](.ai/collaborator/bootstrap.md).
- Every session runs the
  [operator guide](.ai/repository/methodology/prompts/operator-guide.md) S1 →
  [session bootstrap](.ai/repository/methodology/prompts/session-bootstrap.md)
  (read-only) before any work.
- Current repository state: [`STATUS.md`](.ai/repository/state/STATUS.md).

## Repository rules

- The repository is authoritative
  ([MADR-0001](.ai/repository/methodology/adr/0001-repository-authoritative-continuity.md)).
  Repository authority changes only at Repository Gates; skills prepare changes, the
  owner authorizes them
  ([Skill Execution Map](.ai/repository/methodology/skill-execution-map.md)).
- Skills are installed under `.claude/skills/`. Upstream Matt Pocock skills are never
  edited; repository behavior is specialized only through `*-repo-owner` skills
  ([repo-owner-skills.md](.ai/repository-owner/repo-owner-skills.md)).
- `.ai/repository/history/` is evolution evidence: never loaded, never a link target
  or instruction source.

## Engineering standards

Project engineering standards — the Standards axis of `code-review` — are established
through the lifecycle and recorded here as they are accepted. None are accepted yet:
the project is Pre-Baseline. The effort brief,
[`aws-identity-access-poc-prompt.md`](aws-identity-access-poc-prompt.md), is input to
`wayfinder`, not accepted architecture or standards.
