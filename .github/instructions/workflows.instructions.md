---
applyTo: ".github/workflows/**,examples/**/*.yml"
---

Workflow files: apply the "Rules for any workflow change" in copilot-instructions.md.

- Keep `on:` triggers minimal. `pull_request_target` and `workflow_run` run with write tokens: never check out or execute code from the triggering PR or run.
- Use `if: failure()` / `always()` deliberately; a notification job must not mask the original failure.
- Reusable workflow calls cannot set `timeout-minutes` on the calling job; set it inside the callee.
- After editing, run `python -m pipelineintel audit <dir>` and paste the before/after counts in the PR.
