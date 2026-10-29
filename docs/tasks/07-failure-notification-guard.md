# 07 Close the "nothing reacts to failure" gap
labels: agent-ready,failures,reliability,phase-3

## Context
No example workflow uses `if: failure()`. When a deploy fails, the only signal is the red run.

## Acceptance criteria
- [ ] In `examples/gha-dynamics/deploy-prod.yml` add a final `notify-failure` job: `needs:` all deploy jobs, `if: failure()`, `permissions: {issues: write}`, links the run URL and the first failed job, and does not mask the original failure.
- [ ] The notification passes untrusted values via `env:`, not inline.
- [ ] A new audit rule `notify-uses-needs-context` OR a test proving `no-failure-handling` disappears for that file; ratchet ceiling lowered.
- [ ] Short note in the PR: when would you prefer `failure-triage.yml` (workflow_run) over an in-workflow job? (Hint: reusable workflow failures, logs, permissions.)

## Lesson
Compare the two capture styles by running the same failure through both. Which gives the better evidence? Which survives a workflow that fails before the notify job is even reached?
