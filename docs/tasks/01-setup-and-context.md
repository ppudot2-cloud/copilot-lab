# 01 Setup: repo, instructions, and the cloud agent environment
labels: learning,phase-1

**Concepts:** repository instructions, path-scoped instructions, `copilot-setup-steps.yml`.

## Do
- [ ] Open `.github/copilot-instructions.md` and `.github/instructions/python.instructions.md`. Ask Copilot Chat "how do I run tests here?" and confirm it answers from the instructions file.
- [ ] Run the `Copilot Setup Steps` workflow manually (Actions tab) and confirm it goes green.
- [ ] Edit the instructions file to add a rule you can test (for example "always name tests `test_<thing>_<outcome>`"), then ask Copilot to add a test and check it obeys.

## You understand it when
You can explain the difference between repo-wide instructions, path-scoped instructions, and setup steps, and which one fixes "the agent can't run pytest".
