---
applyTo: "src/**/*.py,tests/**/*.py"
---

Path-scoped instructions: applied only when Copilot works on files matching `applyTo`.

- Use `from __future__ import annotations` at the top of every module.
- Prefer frozen dataclasses for data carriers.
- Tests use plain `pytest` functions (no unittest classes) and `tmp_path` / `capsys` fixtures.
- Test names describe behavior: `test_<thing>_<expected outcome>`.
