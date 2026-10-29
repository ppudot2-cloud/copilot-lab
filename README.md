# copilot-lab

A small, safe sandbox for learning GitHub Copilot end to end: instructions, custom agents, skills, prompt files, the cloud coding agent, Projects, automation, stacked PRs, Fusion, and merge queue.

The code (`solutionops`) mirrors two real pieces of the GHA-Dynamics ALM pipeline (deploy ordering and deployment-settings linting) but needs no Power Platform access, so an agent can build, test, and open PRs without touching any environment.

## How the pieces fit

```
Issue (agent-task template)           <- you write acceptance criteria
  │  label agent-ready ─────────────> auto-assign-copilot.yml (automation)
  ▼
Project board card                    <- Backlog → Agent working → In review → Done
  ▼
planner agent                         <- plan + PR stack          (.github/agents)
  ▼
Copilot coding agent                  <- env from copilot-setup-steps.yml
  │  reads copilot-instructions.md (always)
  │  loads skills when the task matches (.github/skills)
  │  model chosen by you or Fusion (Standard / High / Max)
  ▼
Stack of small PRs  (gh stack)        <- each PR reviewable alone
  ▼
CI (ruff + pytest ≥80%) + tester & reviewer agents
  ▼
Merge queue (whole stack as one group) → main
```

## Quick start

```bash
pip install -e ".[dev]"
ruff check . && pytest
python -m solutionops order samples/solutions.json
```

Publish to GitHub, create labels, issues and a Project board:

```bash
gh auth refresh -s project
scripts/bootstrap.sh <your-user>/copilot-lab --private
```

## Learning path

Work through `docs/tasks/` in order. Each file is also created as a GitHub issue by the bootstrap script.

| # | Task | Teaches |
|---|------|---------|
| 01 | Setup and context | instructions, setup steps |
| 02 | Agents, skills, prompts tour | when to use which |
| 03 | Bug: cycle drops solutions | first full ticket → PR run |
| 04 | Unknown dependency error | parallel sessions and conflicts |
| 05 | Lint rule | skill tuning loop |
| 06 | `matrix` command | stacked PRs |
| 07 | Fusion comparison | effort levels, cost vs quality |
| 08 | Projects and automation | label-triggered agent |
| 09 | Merge queue | safe merging, agent limits |
| 10 | Capstone | everything, hands-off |

Tasks 03 to 05 are seeded with real gaps in the code, so the agent has genuine work to do. The baseline is green: 8 tests pass.

## Things I could not verify offline

These Copilot features are new; check current GitHub docs when a step behaves differently: exact `gh stack` flags, how to assign Copilot via CLI/Actions (task 08), custom-agent `tools:` names, and what Copilot may merge unattended (task 09).
