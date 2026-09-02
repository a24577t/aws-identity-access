# .github/

CI, generated CODEOWNERS, and repository automation (ADR-0003; T04 #6 decision 1).

- `CODEOWNERS` — generated, never hand-authored (T20 #22 d6; R3 #28); its
  metadata lives in the central manifest `docs/generated/generated-artifacts.yml`.
- `workflows/` — the four R4 #29 row-11 workflow files, authored with exactly the
  specification §8.1 pins: `validate.yml` and `plan-preview.yml` (the two T15 #10
  d15 required status checks, run for reviewed PRs), `lab-plan.yml` (the
  post-merge environment job producing the encrypted applicable saved plan,
  digest-bound summary, and T06 #8 d4 authorization binding), and
  `lab-apply.yml` (the `lab` environment consumption rule — verify every bound
  input, then apply exactly the approved saved plan, one attempt). Workflow YAML
  stays thin: orchestration here, validation behavior in `src/validator`
  (invoked through `python -m validator.ci`).

Nothing here activates any GitHub configuration — rulesets, required checks,
environments, secrets, and variables are server-side control activation,
R6 #31, separately authorized. Until R6/R7 complete, the `lab-plan` and `lab`
jobs are necessarily inert: their preflights fail closed naming the missing
prerequisite (T15 #10 d15 procedural interval).
