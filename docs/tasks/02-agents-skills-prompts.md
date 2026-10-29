# 02 Tour: custom agents, skills, and prompt files
labels: learning,phase-1

**Concepts:** `.github/agents/*.agent.md` (you pick them), `.github/skills/*/SKILL.md` (loaded automatically when the description matches), `.github/prompts/*.prompt.md` (reusable slash prompts).

## Do
- [ ] Select the `planner` agent (agent picker in VS Code, or `/agent` in Copilot CLI) and give it the text of task 06. Save the plan it produces.
- [ ] Without naming any skill, ask Copilot to "add a lint rule that flags empty environment variable lists". Check whether it follows `add-lint-rule` (look for the docs/lint-rules.md step).
- [ ] Run the `ticket-to-plan` prompt on issue 06.
- [ ] Write a third skill of your own, `bump-version`, and test that it triggers.

## You understand it when
You can say, for any behavior you want, whether it belongs in instructions (always on), a skill (task-triggered), an agent (a role you choose), or a prompt (a shortcut you type).
