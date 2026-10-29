# 04 Feature: clear error for unknown dependencies
labels: agent-ready,feature,phase-2

## Context
If `dependsOn` names a solution that is not in the registry, `deploy_order` currently just never schedules it. We want a loud, specific failure.

## Acceptance criteria
- [ ] `deploy_order` raises `ValueError("<Solution> depends on unknown solution '<Dep>'")`.
- [ ] Test covers the message and that nothing is returned partially.
- [ ] CLI `order` prints the error to stderr and exits 2.

## Lesson
Run this and task 03 in parallel as two Copilot sessions. Both edit `deploy_order`: observe the merge conflict and decide how you would sequence them (this motivates task 07).
