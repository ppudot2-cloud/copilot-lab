# 05 Feature: lint rule `duplicate-schema-name`
labels: agent-ready,feature,skills,phase-2

## Context
Deployment settings entries have a `SchemaName`. Duplicate names in `EnvironmentVariables` make imports ambiguous.

## Acceptance criteria
- [ ] New rule id `duplicate-schema-name` in `settings_lint.py`, one `Issue` per duplicated name.
- [ ] Tests: no duplicates, one duplicate, entries missing `SchemaName` (ignored, not a crash).
- [ ] `docs/lint-rules.md` created with a table row for the rule.

## Lesson
This is the `add-lint-rule` skill exercise. In the PR, check whether the agent followed all five skill steps, including the docs file. If it skipped any, tighten the skill text and re-run on a fresh branch. That loop (observe, edit skill, re-run) is how you tune agents.
