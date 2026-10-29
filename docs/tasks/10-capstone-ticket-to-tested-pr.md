# 10 Capstone: ticket to tested, merged PR, hands-off
labels: capstone,phase-5

## Ticket
"Add a `lint` rule `prod-no-localhost`: in `prod` settings, flag any value containing `localhost` or `127.0.0.1`. Add `--all-envs` to the CLI that lints every `deployment-settings-*.json` in a folder."

## Pipeline to run end to end
1. File the ticket with the `Agent task` template.
2. `planner` agent comments a plan and a 2-PR stack.
3. Label `agent-ready`; Copilot's coding agent opens the draft PR (or stack).
4. CI plus coverage gate run; `tester` agent confirms red-then-green history in commits.
5. `reviewer` agent reviews; you request one change and the agent addresses it.
6. Merge via the queue. Project card moves to Done.

## Write-up
Fill `docs/experiments/capstone-retro.md`: what the agent got wrong, which instruction or skill edit would have prevented each miss, time saved vs doing it by hand.
