# 09 Safe merging: branch protection, merge queue, auto-merge
labels: learning,merge,phase-4

## Do
- [ ] Add a branch ruleset on `main`: require PR, require `test` status check, require 1 approval, enable merge queue.
- [ ] Land the task 06 stack through the merge queue and observe it as one merge group.
- [ ] Enable auto-merge on a Copilot-authored PR; confirm it still waits for the human approval and the green check.
- [ ] Break CI on purpose in a throwaway PR and confirm the queue ejects it.

## Open question to answer yourself
Which merges, if any, should an agent be allowed to perform unattended? Write your policy in `docs/experiments/merge-policy.md`. Verify against current GitHub docs what Copilot can and cannot merge on its own; do not assume.
