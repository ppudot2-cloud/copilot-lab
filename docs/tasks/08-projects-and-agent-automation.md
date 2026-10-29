# 08 Project board and label-driven agent assignment
labels: learning,automation,phase-4

**Concepts:** GitHub Projects as the failure queue; label-triggered assignment to the coding agent; humans approve, agents propose.

## Do
- [ ] In the Project created by the bootstrap script, add fields `Category`, `Owner` (workflow / platform / human), and `Status` (New, Agent working, In review, Done).
- [ ] Turn on built-in Project workflows: item added -> New; PR merged -> Done.
- [ ] Make a rule: `pipeline-failure` issues with owner `workflow` get the label `agent-ready`; `platform` and `human` never do. Implement it as a step in `failure-triage.yml` (the JSON already carries `owner`).
- [ ] Create the `COPILOT_ASSIGN_TOKEN` secret and test `auto-assign-copilot.yml`. If assignment fails, find out why (token scope, assignee name, plan entitlement) and write it up in `docs/reports/automation-notes.md`.

## You understand it when
A `config`-category failure goes from red run to draft PR with no clicks, while an `auth` failure (expired secret) stops at a human on purpose.
