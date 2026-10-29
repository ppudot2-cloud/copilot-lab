# 03 Capture failures live with the Demo Pipeline
labels: learning,failures,phase-2

## Context
The real history shows logs are gone (HTTP 410) for nearly every failure, so they cannot be diagnosed later. `failure-triage.yml` captures at failure time and files one issue per fingerprint.

## Do
- [ ] Run **Demo Pipeline** with each scenario: `auth`, `config`, `solution-checker`, `import`, `flaky-infra`, `hang`.
- [ ] Watch **Failure Triage** run after each. Open the issue it creates: check category, owner (workflow / platform / human), evidence block, and acceptance criteria.
- [ ] Run `auth` twice. Confirm the second run COMMENTS on the first issue instead of opening a duplicate (fingerprint dedupe).
- [ ] Run `hang`. Does it end as `timed_out` or `failure`? Does triage still classify it? Record what you see in `docs/reports/live-capture-notes.md`.
- [ ] Run `python -m pipelineintel collect --repo <you>/copilot-lab` and compare with the issues.

## You understand it when
You can explain the 3 design choices that make capture safe: it runs from the default branch, log text is escaped before it reaches an issue, and dedupe is by fingerprint not by title.
