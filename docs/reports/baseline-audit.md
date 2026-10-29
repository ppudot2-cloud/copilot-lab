# Baseline audit of the real pipelines (2026-10-29)

Generated with `pipelineintel audit` against the live workflow files. Re-run to measure progress.

## GHA-Dynamics (caller workflows)

| Severity | Rule | Count | Fix |
|---|---|---|---|
| high | `mutable-action-ref` | 10 | Pin to a release tag or full commit SHA: `ppudot2-cloud/GHA-CICD-Core/.github/workflows/_stage-export.yml@<sha>  # vX.Y.Z`. |
| medium | `missing-permissions` | 4 | Add `permissions: {contents: read}` at workflow level, then widen per job. |
| medium | `missing-timeout` | 10 | Set `timeout-minutes` to about 2x the normal duration of the job. |
| medium | `secrets-inherit` | 3 | Pass only the secrets the callee declares, by name. |
| medium | `static-credential` | 1 | Prefer OIDC federation to Azure so no client secret is stored in GitHub. |
| medium | `unpinned-third-party-action` | 10 | Pin `dawidd6/action-send-mail` to a full commit SHA after reviewing it. |
| low | `missing-concurrency` | 1 | Add a `concurrency` group per ref; use `cancel-in-progress: false` for deploys. |
| low | `unpinned-first-party-action` | 13 | Pin `actions/checkout` to a commit SHA and let Dependabot bump it. |

### `mutable-action-ref` (high)
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.stage-export
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.stage-build
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.stage-deploy
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.deploy-uat.steps[0]
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.deploy-uat.steps[1]
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.deploy-uat.steps[4]
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.deploy-prod.steps[0]
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.deploy-prod.steps[1]
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.deploy-prod.steps[4]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export.steps[1]

### `missing-permissions` (medium)
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.pipeline-summary
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.setup
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.create-pr

### `missing-timeout` (medium)
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.setup
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.pipeline-summary
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.guard
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.read-context
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.deploy-uat
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.deploy-prod
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.pipeline-summary
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.setup
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.create-pr

### `secrets-inherit` (medium)
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.stage-export
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.stage-build
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.stage-deploy

### `static-credential` (medium)
- `GHA-Dynamics/.github/workflows/export-solution.yml` workflow

### `unpinned-third-party-action` (medium)
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.pipeline-summary.steps[4]
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.pipeline-summary.steps[1]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export.steps[2]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export.steps[4]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export.steps[6]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export.steps[8]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export.steps[10]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export.steps[11]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export.steps[12]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export.steps[15]

### `missing-concurrency` (low)
- `GHA-Dynamics/.github/workflows/export-solution.yml` workflow

### `unpinned-first-party-action` (low)
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.setup.steps[0]
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.setup.steps[1]
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.pipeline-summary.steps[0]
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.pipeline-summary.steps[1]
- `GHA-Dynamics/.github/workflows/build-and-deploy.yml` jobs.pipeline-summary.steps[2]
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.read-context.steps[0]
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.read-context.steps[2]
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.deploy-uat.steps[2]
- `GHA-Dynamics/.github/workflows/deploy-prod.yml` jobs.deploy-prod.steps[2]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.setup.steps[0]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.setup.steps[1]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.export.steps[0]
- `GHA-Dynamics/.github/workflows/export-solution.yml` jobs.create-pr.steps[0]


## GHA-CICD-Core (reusable library)

| Severity | Rule | Count | Fix |
|---|---|---|---|
| high | `mutable-action-ref` | 32 | Pin to a release tag or full commit SHA: `ppudot2-cloud/GHA-CICD-Core/.github/actions/dynamics/reveille@<sha>  # vX.Y.Z`. |
| medium | `missing-permissions` | 13 | Add `permissions: {contents: read}` at workflow level, then widen per job. |
| medium | `missing-timeout` | 14 | Set `timeout-minutes` to about 2x the normal duration of the job. |
| medium | `no-failure-handling` | 2 | Add a final job `if: failure()` that notifies and links the run and failing step. |
| medium | `secrets-inherit` | 2 | Pass only the secrets the callee declares, by name. |
| medium | `static-credential` | 5 | Prefer OIDC federation to Azure so no client secret is stored in GitHub. |
| medium | `unpinned-third-party-action` | 1 | Pin `azure/login` to a full commit SHA after reviewing it. |
| low | `missing-concurrency` | 7 | Add a `concurrency` group per ref; use `cancel-in-progress: false` for deploys. |
| low | `unpinned-first-party-action` | 25 | Pin `actions/download-artifact` to a commit SHA and let Dependabot bump it. |

### `mutable-action-ref` (high)
- `GHA-CICD-Core/.github/workflows/_job-build.yml` jobs.build.steps[0]
- `GHA-CICD-Core/.github/workflows/_job-build.yml` jobs.build.steps[1]
- `GHA-CICD-Core/.github/workflows/_job-build.yml` jobs.build.steps[4]
- `GHA-CICD-Core/.github/workflows/_job-build.yml` jobs.build.steps[5]
- `GHA-CICD-Core/.github/workflows/_job-build.yml` jobs.build.steps[6]
- `GHA-CICD-Core/.github/workflows/_job-build.yml` jobs.build.steps[10]
- `GHA-CICD-Core/.github/workflows/_job-deploy.yml` jobs.deploy.steps[0]
- `GHA-CICD-Core/.github/workflows/_job-deploy.yml` jobs.deploy.steps[1]
- `GHA-CICD-Core/.github/workflows/_job-deploy.yml` jobs.deploy.steps[3]
- `GHA-CICD-Core/.github/workflows/_stage-build.yml` jobs.build
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-dev.steps[0]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-dev.steps[1]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-dev.steps[3]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-intg.steps[0]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-intg.steps[1]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-intg.steps[3]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-uat.steps[0]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-uat.steps[1]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-uat.steps[3]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-frs.steps[0]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-frs.steps[1]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-frs.steps[3]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-perf.steps[0]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-perf.steps[1]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-perf.steps[3]
- `GHA-CICD-Core/.github/workflows/_stage-export.yml` jobs.export.steps[0]
- `GHA-CICD-Core/.github/workflows/_stage-export.yml` jobs.export.steps[1]
- `GHA-CICD-Core/.github/workflows/_stage-export.yml` jobs.export.steps[2]
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.mock-build
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.mock-deploy-dev.steps[0]
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.mock-deploy-dev.steps[1]
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.mock-deploy-dev.steps[3]

### `missing-permissions` (medium)
- `GHA-CICD-Core/.github/workflows/_job-build.yml` jobs.build
- `GHA-CICD-Core/.github/workflows/_job-deploy.yml` jobs.deploy
- `GHA-CICD-Core/.github/workflows/_stage-build.yml` jobs.build
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-dev
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-intg
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-uat
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-frs
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-perf
- `GHA-CICD-Core/.github/workflows/_stage-export.yml` jobs.export
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.setup
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.pester-unit-tests
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.mock-build
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.test-summary

### `missing-timeout` (medium)
- `GHA-CICD-Core/.github/workflows/_job-build.yml` jobs.build
- `GHA-CICD-Core/.github/workflows/_stage-build.yml` jobs.validate
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.create-pr
- `GHA-CICD-Core/.github/workflows/_stage-export.yml` jobs.export
- `GHA-CICD-Core/.github/workflows/_stage-export.yml` jobs.commit
- `GHA-CICD-Core/.github/workflows/health-check.yml` jobs.scan
- `GHA-CICD-Core/.github/workflows/onboard-project.yml` jobs.onboard
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.setup
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.pester-unit-tests
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.mock-deploy-dev
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.test-summary
- `GHA-CICD-Core/.github/workflows/rollback.yml` jobs.validate
- `GHA-CICD-Core/.github/workflows/rollback.yml` jobs.rollback
- `GHA-CICD-Core/.github/workflows/test-servicenow.yml` jobs.simulate-servicenow

### `no-failure-handling` (medium)
- `GHA-CICD-Core/.github/workflows/_job-deploy.yml` workflow
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` workflow

### `secrets-inherit` (medium)
- `GHA-CICD-Core/.github/workflows/_stage-build.yml` jobs.build
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.mock-build

### `static-credential` (medium)
- `GHA-CICD-Core/.github/workflows/_job-build.yml` workflow
- `GHA-CICD-Core/.github/workflows/_job-deploy.yml` workflow
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` workflow
- `GHA-CICD-Core/.github/workflows/_stage-export.yml` workflow
- `GHA-CICD-Core/.github/workflows/onboard-project.yml` workflow

### `unpinned-third-party-action` (medium)
- `GHA-CICD-Core/.github/workflows/rollback.yml` jobs.rollback.steps[1]

### `missing-concurrency` (low)
- `GHA-CICD-Core/.github/workflows/_job-build.yml` workflow
- `GHA-CICD-Core/.github/workflows/_job-deploy.yml` workflow
- `GHA-CICD-Core/.github/workflows/_stage-build.yml` workflow
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` workflow
- `GHA-CICD-Core/.github/workflows/_stage-export.yml` workflow
- `GHA-CICD-Core/.github/workflows/onboard-project.yml` workflow
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` workflow

### `unpinned-first-party-action` (low)
- `GHA-CICD-Core/.github/workflows/_job-build.yml` jobs.build.steps[2]
- `GHA-CICD-Core/.github/workflows/_job-build.yml` jobs.build.steps[7]
- `GHA-CICD-Core/.github/workflows/_job-build.yml` jobs.build.steps[9]
- `GHA-CICD-Core/.github/workflows/_job-deploy.yml` jobs.deploy.steps[2]
- `GHA-CICD-Core/.github/workflows/_stage-build.yml` jobs.validate.steps[0]
- `GHA-CICD-Core/.github/workflows/_stage-build.yml` jobs.validate.steps[1]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-dev.steps[2]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-intg.steps[2]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-uat.steps[2]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-frs.steps[2]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.deploy-perf.steps[2]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.create-pr.steps[0]
- `GHA-CICD-Core/.github/workflows/_stage-deploy-chain.yml` jobs.create-pr.steps[1]
- `GHA-CICD-Core/.github/workflows/_stage-export.yml` jobs.export.steps[3]
- `GHA-CICD-Core/.github/workflows/_stage-export.yml` jobs.commit.steps[0]
- `GHA-CICD-Core/.github/workflows/_stage-export.yml` jobs.commit.steps[1]
- `GHA-CICD-Core/.github/workflows/health-check.yml` jobs.scan.steps[4]
- `GHA-CICD-Core/.github/workflows/onboard-project.yml` jobs.onboard.steps[0]
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.setup.steps[0]
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.setup.steps[1]
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.pester-unit-tests.steps[0]
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.pester-unit-tests.steps[3]
- `GHA-CICD-Core/.github/workflows/pipeline-test.yml` jobs.mock-deploy-dev.steps[2]
- `GHA-CICD-Core/.github/workflows/rollback.yml` jobs.rollback.steps[0]
- `GHA-CICD-Core/.github/workflows/rollback.yml` jobs.rollback.steps[4]

