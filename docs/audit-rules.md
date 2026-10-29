# Audit rules

| Rule | Severity | What it catches | Why it matters here |
|---|---|---|---|
| `mutable-action-ref` | high | `uses: x@main` (any moving branch) | A push to GHA-CICD-Core `main` changes what deploys to Prod |
| `script-injection` | high | `${{ github.event.* }}` / `github.head_ref` in `run:` | Attacker-controlled title or branch name becomes shell |
| `pwn-request` | high | `pull_request_target` checking out PR head | Privileged token plus untrusted code |
| `unpinned-third-party-action` | medium | third-party action pinned to a tag only | Tags can be moved by the action's owner |
| `missing-permissions` | medium | no `permissions` at workflow or job level | Token gets repo default scope |
| `missing-timeout` | medium | job without `timeout-minutes` | Hung step runs up to 6 hours |
| `secrets-inherit` | medium | `secrets: inherit` | Callee receives every secret |
| `no-failure-handling` | medium | environment deploys, no `failure()`/`always()` | Failures are silent |
| `static-credential` | medium | long-lived secret auth, no OIDC | Secret expiry causes auth outages (see `auth` failures) |
| `missing-concurrency` | medium (deploy) / low | no concurrency group | Overlapping deploys race |
| `unpinned-first-party-action` | low | `actions/*@v4` tag | Lower risk, still mutable |
| `invalid-workflow` | high | file is not a workflow mapping | Broken file |

Known limits: static analysis only, no line numbers (reports job and step index), does not follow composite actions, and treats every `uses: ...@main` the same whether internal or external.
