# 10 Capstone: a failure becomes a merged, tested fix, hands-off
labels: capstone,phase-5

## Scenario
Add a new demo scenario `missing-secret` to `demo-pipeline.yml` that fails with "Input required and not supplied: password". Then make the whole loop handle it end to end.

## Loop to run
1. Dispatch the scenario. `failure-triage` files an issue (category should be `config`, owner `workflow`).
2. Automation labels it `agent-ready`; Copilot's coding agent opens a draft PR.
3. The agent must deliver a **fix and a guard**: a `validate-config` job that checks required secrets/vars exist and prints all that are missing, plus a classify regression fixture.
4. CI: tests, coverage gate, workflow audit at medium. `workflow-security-reviewer` reviews.
5. You request one change; the agent addresses it. Merge via the queue. Card moves to Done.
6. Re-dispatch the scenario: the new guard now fails in seconds with a better message, and triage dedupes onto the existing issue.

## Write-up
`docs/reports/capstone-retro.md`: what the agent got wrong, which instruction or skill edit would have prevented each miss, minutes from red run to merged fix versus doing it yourself, and the one gap in the pipeline you would close next.
