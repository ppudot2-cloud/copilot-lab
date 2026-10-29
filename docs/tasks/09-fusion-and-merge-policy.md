# 09 Fusion experiment and a merge policy for agent PRs
labels: learning,fusion,merge,phase-4

## Part A: Fusion
Same prompt, clean branch each time: "Fix task 06's `missing-timeout` findings in examples/gha-dynamics/build-and-deploy.yml."
- [ ] Run with Fusion Standard, Fusion Max, and one fixed model. Reset between runs (edits persist).
- [ ] Log in `docs/reports/fusion-log.md`: time, credits, audit before/after, ratchet updated?, security-reviewer verdict, first-try CI result.
- [ ] Decide which finding classes deserve Max (injection? gate-adjacent changes?) and which do not (SHA pinning).

## Part B: merge policy
- [ ] Ruleset on `main`: require PR, require the `test` check, require 1 human approval, merge queue on.
- [ ] Require CODEOWNERS review for `.github/workflows/**` so no agent PR changes a pipeline without a person.
- [ ] Land the task 05 stack through the merge queue; observe it as one group.
- [ ] Write `docs/reports/merge-policy.md`: which agent PRs may auto-merge (docs, fixtures?) and which never (anything under `.github/workflows`). Verify against current GitHub docs what Copilot can and cannot merge by itself; do not assume.

## You understand it when
Your policy answers: who approves a pipeline change that an agent wrote, and what stops a hardening PR from quietly removing an approval gate.
