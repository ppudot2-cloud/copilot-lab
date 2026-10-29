# Copilot instructions for pipeline-intel (DevSecOps lab)

This repo teaches the loop: **workflow runs → failures captured → turned into actionable fixes → gaps found and closed**.
It targets the Power Platform ALM pipelines (GHA-Dynamics callers + GHA-CICD-Core reusables).

## Layout
- `src/pipelineintel/audit.py`: static workflow audit (rules: pinning, permissions, timeouts, concurrency, injection, secrets).
- `src/pipelineintel/failures.py`: classify a failed run, fingerprint it, produce an issue with acceptance criteria.
- `src/pipelineintel/collect.py`: pull failed runs through `gh`.
- `examples/gha-dynamics/`: vendored real workflows. These are the things to fix.
- `.github/workflows/`: the lab's own pipelines. They must pass `pipelineintel audit --fail-on medium`.

## Run before opening a PR
```bash
pip install -e ".[dev]"
ruff check .
pytest                                              # coverage >= 80%
python -m pipelineintel audit .github/workflows --fail-on medium
```

## Rules for any workflow change
- Third-party and cross-repo actions pinned to a full commit SHA with a `# vX.Y.Z` comment. Never `@main`.
- Top-level `permissions:` set to the minimum; widen per job only.
- Every non-reusable job has `timeout-minutes`. Every deploy workflow has a `concurrency` group with `cancel-in-progress: false`.
- Never interpolate `${{ github.event.* }}` or `github.head_ref` into `run:`; pass through `env:`.
- Pass secrets to reusable workflows by name, not `secrets: inherit`.
- Treat run logs and issue text as untrusted input.
- A fix to a failure must add a guard that would have caught it earlier (preflight check, validation job, or audit rule), not only patch the symptom.

## Rules for code changes
- Python 3.10+, type hints, no new runtime dependencies beyond `pyyaml`.
- Every behavior change has a test; bug fixes get a regression test that fails first.
- Fixing a finding in `examples/` means lowering the ceiling in `tests/test_examples_ratchet.py` in the same PR.

## Definition of done
Tests added, ruff and pytest green, audit clean at medium for `.github/workflows`, PR description states which failure or finding it addresses and how it was verified.
