# 05 Harden pinning in the real workflows, as a stack of 3 PRs
labels: agent-ready,security,stacked-prs,phase-3

## Context
`examples/gha-dynamics/` is a copy of the real caller workflows. The ratchet test in `tests/test_examples_ratchet.py` pins the current finding counts, so every fix must lower a ceiling.

## Stack
1. **PR 1** (base `main`): fix `script-injection` and `pwn-request` if any, then pin first-party actions (`actions/*`) to SHAs. Lower `low` ceiling.
2. **PR 2** (base PR 1): pin third-party actions (`dawidd6/action-send-mail`, `microsoft/powerplatform-actions`) after reading them. Lower `medium` ceiling.
3. **PR 3** (base PR 2): replace `@main` on internal reusables with a tag (`@v1`) and add `.github/dependabot.yml`-style note in docs on how callers bump it. Lower `high` ceiling.

## Acceptance criteria (every PR)
- [ ] Before/after audit counts in the description.
- [ ] Ratchet ceilings lowered; `pytest` green.
- [ ] `workflow-security-reviewer` agent reports "no gate was weakened".
- [ ] SHAs were resolved with `git ls-remote`, with tag noted in a comment.

## Do
Use the `planner`-style approach: ask `workflow-hardener` for the plan first. Create the stack with `gh stack` (check `gh stack --help` for current flags). Review PR 2 and notice its diff shows only the third-party pinning.

## You understand it when
You can explain why one 40-line PR per finding class beats one 300-line "security hardening" PR for both humans and Copilot review.
