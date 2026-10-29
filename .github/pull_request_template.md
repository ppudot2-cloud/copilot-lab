## What changed

## Finding or failure addressed
<!-- audit rule id, or [pipeline-failure] issue + fingerprint -->

## Audit before / after
<!-- `python -m pipelineintel audit <dir>` counts: high/medium/low -->

## How it was verified
- [ ] `ruff check .` and `pytest` (coverage 80%+)
- [ ] Workflow audit clean at medium for `.github/workflows`
- [ ] Ratchet ceilings lowered if `examples/` improved
- [ ] No approval gate, `environment:`, or deploy order changed (or called out below)

## Stack position
<!-- Which PR is below this one? -->

Closes #
