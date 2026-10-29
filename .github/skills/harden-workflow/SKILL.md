---
name: harden-workflow
description: Use when asked to fix audit findings, harden, pin, or secure GitHub Actions workflow files. Gives the order of fixes, how to resolve SHAs safely, and how to prove the result.
---

# Harden a workflow

Order matters (highest risk, lowest blast radius first):

1. **script-injection**: move `${{ github.event.* }}` into `env:` and use `"$VAR"` in the script.
2. **mutable-action-ref**: replace `@main` with a tag or SHA. For org-internal reusables, tag the callee repo (`v1`) and pin callers to that tag or SHA.
3. **permissions**: add top-level `permissions: {contents: read}`; add only what each job needs (`id-token: write` for OIDC, `pull-requests: write` for comments).
4. **timeout-minutes**: about 2x typical runtime. Cannot be set on a reusable-workflow call job; set it inside the callee.
5. **concurrency**: deploys use a group per environment with `cancel-in-progress: false`; PR checks use `cancel-in-progress: true`.
6. **secrets-inherit**: replace with explicit `secrets:` mapping.
7. **third-party and first-party pinning**: resolve with `git ls-remote https://github.com/<o>/<r> refs/tags/<tag>`, write `uses: o/r@<sha> # <tag>`. Add `.github/dependabot.yml` with the `github-actions` ecosystem so pins keep moving.

Prove it: audit before/after counts in the PR body, ratchet test ceilings lowered, and a mock/dry-run of the workflow still passes. Never alter approval gates or deploy order.
