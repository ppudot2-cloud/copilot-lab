# 04 Teach the triager a failure it classifies wrong
labels: agent-ready,failures,phase-2

## Context
Failures that land in `unknown` or `log-unavailable` are gaps in capture, not just bad luck. Take a real failure from your own pipeline (copy a sanitized `--log-failed` excerpt) or invent one realistic for Power Platform, such as `pac solution import` returning "Solution 'X' requires 'Y' version 1.2.0.0 or later".

## Acceptance criteria
- [ ] Sanitized run JSON + log added under `tests/fixtures/runs/`.
- [ ] Regex added to `CATEGORY_PATTERNS` (or a new category with a `REMEDIATIONS` entry) so it is no longer `unknown`.
- [ ] Regression test fails before the change and passes after.
- [ ] The remediation names a **fix and a guard** (for example: a preflight that checks dependency versions before import).

## Lesson
Assign to Copilot's coding agent with the `fix-workflow-failure` skill. Check whether it added a guard or only matched the string. If it only matched the string, tighten the skill text and re-run on a fresh branch.
