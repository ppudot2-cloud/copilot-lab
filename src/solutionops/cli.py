"""Command line entry: python -m solutionops <order|lint> ..."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .registry import deploy_order, load_registry
from .settings_lint import lint_settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="solutionops")
    sub = parser.add_subparsers(dest="command", required=True)
    order = sub.add_parser("order", help="print deploy order")
    order.add_argument("registry")
    lint = sub.add_parser("lint", help="lint a deployment-settings file")
    lint.add_argument("file")
    lint.add_argument("--env", required=True)
    args = parser.parse_args(argv)

    if args.command == "order":
        print("\n".join(deploy_order(load_registry(args.registry))))
        return 0

    issues = lint_settings(json.loads(Path(args.file).read_text()), args.env)
    for issue in issues:
        print(f"[{issue.rule}] {issue.message}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
