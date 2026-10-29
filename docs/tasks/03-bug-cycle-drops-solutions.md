# 03 Bug: dependency cycles silently drop solutions from deploy order
labels: agent-ready,bug,phase-2

## Context
`deploy_order` in `src/solutionops/registry.py` uses Kahn's algorithm. If solutions form a cycle (A depends on B, B depends on A) they never reach indegree 0 and are silently omitted. A pipeline would then deploy a partial set with no warning.

## Acceptance criteria
- [ ] `deploy_order` raises `ValueError` whose message names the solutions in the cycle.
- [ ] A regression test `test_cycle_regression` fails on current `main` and passes after the fix.
- [ ] Existing tests still pass; coverage stays at or above 80%.

## Out of scope
Changing the CLI output format.

## Lesson
First end-to-end run: assign this issue to Copilot (or label it `agent-ready` once automation is on) and watch issue → session → draft PR → CI → review. Record what it got right and wrong.
