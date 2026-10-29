# 07 Experiment: Copilot Fusion effort levels vs a fixed model
labels: learning,fusion,phase-3

**Concepts:** Fusion routes a prompt across models by effort level (Standard, High, Max). Cost and credits differ per level, and discarding a draft does not undo edits already made.

## Do
Use the same prompt on a clean branch each time: "Implement task 05 following repo conventions."
- [ ] Run 1: Fusion Standard.
- [ ] Run 2: Fusion Max.
- [ ] Run 3: a single model you choose manually.
- [ ] For each run, fill in `docs/experiments/fusion-log.md`: time, credits used, tests added, first-try CI result, reviewer-agent findings.
- [ ] Reset the branch between runs (`git restore . && git clean -fd`), since edits persist.

## You understand it when
You can say which task types justify Max and which do not, backed by your own numbers rather than the marketing benchmark.
