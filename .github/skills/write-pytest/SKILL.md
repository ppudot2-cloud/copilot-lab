---
name: write-pytest
description: Use when writing or fixing tests in this repo. Defines the red-green workflow and test style.
---

# Writing tests here

- Red first: write the test, run it, confirm it fails for the expected reason.
- Style: plain pytest functions, `tmp_path` for files, `capsys` for CLI output, parametrize for tables of cases.
- A bug fix gets a regression test named `test_<bug>_regression` that fails on the old code.
- Assert on rule ids and exit codes, not on full message text, unless the message is the feature.
- Finish with `pytest` (coverage 80% or higher) and `ruff check .`.
