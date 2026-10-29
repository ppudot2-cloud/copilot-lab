# copilot-lab: DevSecOps for GitHub Actions with Copilot

A sandbox for one loop, applied to your real Power Platform pipelines (GHA-Dynamics callers + GHA-CICD-Core reusables):

```
workflow runs ──> failure captured at failure time ──> classified + fingerprinted
      ^                                                        │
      │                                                        v
 gaps found by audit <── fix AND guard merged <── agent PR <── issue with acceptance criteria
```

Everything Copilot-specific (instructions, agents, skills, projects, automation, stacked PRs, Fusion, merge queue) is exercised **through** that loop, not in isolation.

## What the real pipelines told us

From `docs/reports/` (generated from your live repos):

| Finding | Evidence | Guard in this repo |
|---|---|---|
| Cross-repo reusables/actions referenced at `@main` | 42 high findings | `audit` rule `mutable-action-ref`, task 05 |
| Almost no failure can be diagnosed later | HTTP 410 on logs for nearly all failed runs | `failure-triage.yml` captures at failure time |
| A run lived about 30 days | 720h "Build and Deploy" run | `stale-run-reaper.yml`, task 06 |
| No `timeout-minutes` on 24 jobs, no `permissions` on 17 | audit | tasks 05, 06 |
| `secrets: inherit` x5, static client secrets | audit | `audit`, OIDC note |
| Deploys with nothing reacting to failure | audit | task 07 |
| Mostly cancelled runs | 14 of 40 recent runs | `concurrency` review, task 06 |

## How the pieces work

| Piece | File | Role in the loop |
|---|---|---|
| Audit | `src/pipelineintel/audit.py`, `docs/audit-rules.md` | finds gaps statically |
| Capture | `.github/workflows/failure-triage.yml`, `collect.py` | grabs evidence while logs exist, one issue per fingerprint |
| Classify | `failures.py` | category, owner (workflow / platform / human), fix + guard checklist |
| Agents | `.github/agents/` | `failure-triager`, `workflow-hardener`, `workflow-security-reviewer` |
| Skills | `.github/skills/` | `fix-workflow-failure`, `harden-workflow` load when the task matches |
| Instructions | `.github/copilot-instructions.md`, `instructions/` | always-on pipeline rules |
| Agent env | `copilot-setup-steps.yml` | lets the cloud agent run tests and the audit |
| Automation | `auto-assign-copilot.yml` | `agent-ready` label starts the coding agent |
| Safety | `CODEOWNERS`, ratchet test, dogfood audit in CI | agents cannot quietly weaken a pipeline |
| Practice target | `examples/gha-dynamics/` + `tests/test_examples_ratchet.py` | real workflows to fix; findings may only go down |
| Failure generator | `demo-pipeline.yml` | breaks on purpose in 6 realistic ways |

## Try it (no GitHub needed)

```bash
pip install -e ".[dev]"
ruff check . && pytest
python -m pipelineintel audit examples/gha-dynamics --fail-on info
python -m pipelineintel triage --run tests/fixtures/runs/stalled-run.json
python -m pipelineintel collect --repo ppudot2-cloud/GHA-Dynamics --limit 40 --include-cancelled
```

## Publish and start the tasks

```bash
gh auth refresh -s project
scripts/bootstrap.sh <your-user>/copilot-lab --private
```

Then work through `docs/tasks/` in order (also created as issues).

| # | Task | Copilot topic | DevSecOps topic |
|---|------|---------------|-----------------|
| 01 | Setup and context | instructions, agents, skills | |
| 02 | Read the baseline audit | security-reviewer agent | gap analysis |
| 03 | Capture failures live | | failure capture, dedupe |
| 04 | Teach the triager | coding agent + skill | classification gaps |
| 05 | Harden pinning | **stacked PRs** | supply chain |
| 06 | Permissions, timeouts, concurrency | agent on real workflows | blast radius, hangs |
| 07 | Failure notification guard | | detection |
| 08 | Projects + label automation | **Projects, automation** | owner-based routing |
| 09 | Fusion + merge policy | **Fusion, merge queue** | who approves pipeline changes |
| 10 | Capstone | everything | red run to merged fix |

## Caveats

- Static audit only: no line numbers, does not follow composite actions, treats internal and external `@main` alike.
- Not verified here: exact `gh stack` flags, assigning Copilot via CLI/Actions, custom-agent `tools:` names, whether `timeout-minutes` bounds an approval wait, and what Copilot may merge unattended. Tasks 05, 06, 08, 09 tell you to check current docs.
- `examples/` is a vendored copy; fixing it does not change your real repos. Port the changes to GHA-CICD-Core (where the logic lives) once you trust them.
