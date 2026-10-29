# Copilot instructions for solutionops

Repo-wide context. Copilot (chat, CLI, and the cloud coding agent) reads this automatically.

## What this repo is
`solutionops` is a small Python toolkit that mirrors two pieces of the GHA-Dynamics ALM pipeline:
- `registry.py`: loads `solutions.json` and computes deploy order (dependencies first).
- `settings_lint.py`: lints `deployment-settings-{env}.json` files.
- `cli.py`: `python -m solutionops order|lint`.

## Build and test (run these before opening a PR)
```bash
pip install -e ".[dev]"
ruff check .
pytest            # coverage is printed; keep it at or above 80%
```

## Conventions
- Python 3.10+, type hints on all public functions, no new runtime dependencies.
- Never mutate inputs; return new objects.
- Every behavior change needs a test. Bug fixes need a regression test that fails before the fix.
- Lint rules return `Issue(rule, message)`; rule ids are kebab-case.
- Keep PRs small. If a ticket needs more than ~200 changed lines, split it into a stack.

## Definition of done
Tests added, `ruff` clean, `pytest` green, PR description lists what changed and how it was verified.
