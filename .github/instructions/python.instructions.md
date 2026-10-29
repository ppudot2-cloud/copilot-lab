---
applyTo: "src/**/*.py,tests/**/*.py"
---

- `from __future__ import annotations` at the top of every module; frozen dataclasses for records.
- Pure functions where possible; shell out to `gh` only in `collect.py`, via the injectable `Runner`.
- Tests are plain pytest functions; fixtures live in `tests/fixtures/`. Real failure logs go in `tests/fixtures/runs/` (sanitized) so every new failure category has a regression test.
- New audit rule: add it in `audit.py`, one passing and one failing fixture, and a row in `docs/audit-rules.md`.
- New failure category: add the regex to `CATEGORY_PATTERNS`, an entry in `REMEDIATIONS`, and a parametrized `classify` case.
