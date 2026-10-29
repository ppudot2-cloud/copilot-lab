# 08 Projects board and automation
labels: learning,automation,phase-4

**Concepts:** GitHub Projects as the ticket pipeline; label-driven assignment to the coding agent.

## Do
- [ ] Open the Project created by `scripts/bootstrap.sh`. Add fields: `Phase`, `Agent?` (yes/no), `Status` (Backlog, Agent working, In review, Done).
- [ ] Turn on built-in Project workflows: item added → Backlog; PR merged → Done.
- [ ] Create a `COPILOT_ASSIGN_TOKEN` secret and test `.github/workflows/auto-assign-copilot.yml` by labelling issue 04 `agent-ready`.
- [ ] If assignment fails, find out why (token scope, assignee login, plan entitlement) and document it in `docs/experiments/automation-notes.md`.

## You understand it when
Moving a ticket to `agent-ready` starts work with zero clicks, and you know exactly where a human must still approve.
