# 06 Permissions, timeouts, and concurrency in the deploy workflows
labels: agent-ready,security,reliability,phase-3

## Context
Real pipeline facts: no job has `timeout-minutes`, several workflows have no `permissions`, and the history is mostly cancelled runs. Deploys to Power Platform must be sequential and must never be cancelled mid-import.

## Acceptance criteria
- [ ] Workflow-level `permissions: {contents: read}` in each example, widened only where a job needs it (state which and why).
- [ ] `timeout-minutes` on every non-reusable job; justify each value from typical durations (use `gh run list --json startedAt,updatedAt`).
- [ ] Deploy-path concurrency uses `cancel-in-progress: false`; non-prod validation may cancel.
- [ ] Ratchet ceilings lowered. `workflow-security-reviewer` confirms no approval gate or `environment:` was touched.

## Lesson
Timeouts and approvals interact: record in `docs/reports/timeout-vs-approval.md` what you verified about whether `timeout-minutes` bounds an environment approval wait (the 30-day run suggests it does not), and cite the GitHub docs page you checked.
