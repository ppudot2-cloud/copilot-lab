---
name: fix-workflow-failure
description: Use when handling a [pipeline-failure] issue or a failed Actions run. Turns evidence into a fix plus a guard, and adds a regression fixture.
---

# From failure to fix

1. Read the issue's fingerprint, category, and evidence. Reproduce the classification locally with `python -m pipelineintel triage --run <run.json> --log <log>`.
2. Decide the owner: **workflow** (a PR fixes it), **platform** (secret expiry, env config, retention: write the ask, do not patch around it), **human** (investigate).
3. For workflow-owned failures implement two changes:
   - the **fix** (retry with backoff for idempotent calls only, correct reference, preflight validation);
   - the **guard** that fails earlier and louder (validate required `vars.*` and secrets in a first job, a preflight auth call, a new audit rule).
4. Add a sanitized log under `tests/fixtures/runs/` and a `classify` test so the same failure is recognized next time. If it was `unknown` or `log-unavailable`, improve capture so it is not again.
5. Link the issue (`Closes #n`) and state how you verified: re-run the demo scenario or the mock-deploy path.
