# 06 Feature: `matrix` command, delivered as a stack of 3 PRs
labels: feature,stacked-prs,phase-3

## Context
GHA-Dynamics feeds a GitHub Actions matrix from `compute-solutions.py`. Add `python -m solutionops matrix samples/solutions.json` printing `{"include":[{"solution":"CoreSolution"}, ...]}` in deploy order.

## Plan as a stack (let the `planner` agent propose, then compare)
1. PR 1 (base: main): `registry.to_matrix(order) -> dict` plus unit tests.
2. PR 2 (base: PR 1): CLI `matrix` subcommand plus CLI tests.
3. PR 3 (base: PR 2): README/docs section and a sample workflow snippet.

## Do
- [ ] `gh stack init`, then `gh stack add` for each slice, commit, `gh stack submit`.
- [ ] Review PR 2 and note that its diff shows only the CLI layer.
- [ ] Request a change on PR 1, fix it, run `gh stack rebase` / `gh stack sync`, and confirm PR 2 and 3 update.
- [ ] Merge the bottom PR and watch the remaining PRs retarget.

## You understand it when
You can explain why a stack beats one 300-line PR for both human reviewers and Copilot review, and what rebasing a stack does to approvals.

Note: `gh stack` and native stacked PRs are recent. Run `gh stack --help` and check current GitHub docs for exact flags before relying on this sequence.
