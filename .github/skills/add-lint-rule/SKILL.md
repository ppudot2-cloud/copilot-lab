---
name: add-lint-rule
description: Use when asked to add a new rule to the deployment-settings linter in settings_lint.py. Covers rule naming, Issue format, tests, and docs.
---

# Add a lint rule

1. Pick a kebab-case rule id (for example `duplicate-schema-name`).
2. In `src/solutionops/settings_lint.py`, add the check inside `lint_settings` (or a small helper it calls). Return `Issue(rule_id, f"{env}: <message>")`. Do not raise.
3. In `tests/test_settings_lint.py` add at least: one passing case, one failing case asserting the exact rule id, and one edge case (empty list, wrong type).
4. Run `pytest` and `ruff check .`.
5. Add a line for the rule to the table in `docs/lint-rules.md` (create it if missing).
