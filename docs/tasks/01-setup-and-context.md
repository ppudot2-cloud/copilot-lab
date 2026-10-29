# 01 Setup: make Copilot understand a pipeline repo
labels: learning,phase-1

**Concepts:** repo instructions, path-scoped instructions, `copilot-setup-steps.yml`, custom agents, skills, prompt files.

## Do
- [ ] Read `.github/copilot-instructions.md` and `.github/instructions/workflows.instructions.md`. Ask Copilot Chat "what are the rules for changing a workflow here?" and confirm it answers from them.
- [ ] Run **Copilot Setup Steps** from the Actions tab; confirm green.
- [ ] Pick each agent in turn (`failure-triager`, `workflow-hardener`, `workflow-security-reviewer`) and ask it "what is your job and what will you refuse to do?".
- [ ] Ask "add timeouts to examples/gha-dynamics/deploy-prod.yml" WITHOUT naming a skill. Check whether `harden-workflow` was applied (before/after audit counts in the answer).

## You understand it when
You can say which behavior belongs in instructions (always on), a skill (loaded when the task matches), an agent (a role you choose), or a prompt (a shortcut), and which one fixes "the agent cannot run the audit".
