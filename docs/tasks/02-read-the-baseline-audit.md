# 02 Read the baseline: what gaps do the real pipelines have?
labels: learning,security,phase-1

## Context
`docs/reports/baseline-audit.md` is a real audit of GHA-Dynamics and GHA-CICD-Core. Headline results: 42 `mutable-action-ref` (cross-repo `@main`), 17 jobs/workflows without `permissions`, 24 jobs without `timeout-minutes`, 5 uses of `secrets: inherit`, no `failure()` handling in 2 core workflows that deploy to environments, static client secrets instead of OIDC.

## Do
- [ ] Re-run it yourself: `python -m pipelineintel audit ../GHA-CICD-Core/.github/workflows --fail-on info`.
- [ ] Rank the rules by risk to YOUR pipeline. Which are real threats (a push to GHA-CICD-Core `main` changes what deploys to Prod) and which are noise?
- [ ] Ask the `workflow-security-reviewer` agent to review `examples/gha-dynamics/deploy-prod.yml` and compare its findings to the tool's. What did the agent find that the static rules cannot? What did the rules find that it missed?
- [ ] Write 5 sentences in `docs/reports/my-risk-ranking.md`.

## You understand it when
You can explain why `@main` on an internal reusable workflow is a supply-chain risk even though you own the repo, and why `cancel-in-progress` is dangerous on deploys.
