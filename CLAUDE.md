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

## Repository-owner execution assignment

Claude is assigned the repository-owner **execution** function for routine work in this
repository. Within the current lifecycle step, Claude may inspect and search repository
content, edit files, run validation and tests, create or switch local branches, stage changes,
and create local commits without requesting separate command-by-command approval.

This operational assignment does not transfer design authority or bypass Repository Gates.
Eric remains the human architect and repository authority under methodology principle P1.
Pushes, merges, tags, releases, destructive Git recovery, and progression across a Repository
Gate require Eric's explicit authorization. Permission to invoke a tool is capability, not
lifecycle authorization.

## Engineering standards

Project engineering standards — the Standards axis of `code-review` — are established
through the lifecycle and recorded here as they are accepted. None are accepted yet:
the project is Pre-Baseline. The effort brief,
[`aws-identity-access-poc-prompt.md`](aws-identity-access-poc-prompt.md), is input to
`wayfinder`, not accepted architecture or standards.

## Agent skills

### Issue tracker

Issues live in the GitHub Issues of this repository (`gh` CLI); wayfinder maps and
tickets are GitHub issues wired with native issue dependencies. See
[`docs/agents/issue-tracker.md`](docs/agents/issue-tracker.md).

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`,
`wontfix`. See [`docs/agents/triage-labels.md`](docs/agents/triage-labels.md).

### Domain docs

Single-context: root `CONTEXT.md` + `docs/adr/` (layout provisional pending the wayfinder
decision on the domain decision-register form). See
[`docs/agents/domain.md`](docs/agents/domain.md).
