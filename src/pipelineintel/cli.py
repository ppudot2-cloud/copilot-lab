"""CLI: pipelineintel audit|triage|collect."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .audit import SEVERITIES, at_or_above, audit_dir, render_markdown
from .collect import collect
from .failures import build_record, group_by_fingerprint, issue_body, issue_title, remediate


def _cmd_audit(args: argparse.Namespace) -> int:
    findings = audit_dir(Path(args.dir))
    print(render_markdown(findings))
    return 1 if at_or_above(findings, args.fail_on) else 0


def _cmd_triage(args: argparse.Namespace) -> int:
    run = json.loads(Path(args.run).read_text())
    log = Path(args.log).read_text() if args.log else ""
    record = build_record(run, log)
    if args.json:
        print(json.dumps({"title": issue_title(record), "body": issue_body(record),
                          "fingerprint": record.fingerprint, "category": record.category,
                          "owner": remediate(record).owner}))
    else:
        print(f"# {issue_title(record)}\n\n{issue_body(record)}")
    return 0


def _cmd_collect(args: argparse.Namespace) -> int:
    records = collect(args.repo, args.limit, include_cancelled=args.include_cancelled)
    if not records:
        print("No failed runs found.")
        return 0
    print("| Count | Category | Workflow | Step | Owner | Fingerprint |\n|---|---|---|---|---|---|")
    for rec, count in group_by_fingerprint(records):
        print(f"| {count} | {rec.category} | {rec.workflow} | {rec.failed_step or '-'} | "
              f"{remediate(rec).owner} | `{rec.fingerprint}` |")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pipelineintel")
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit", help="static gap audit of a workflows directory")
    audit.add_argument("dir")
    audit.add_argument("--fail-on", choices=SEVERITIES, default="high")
    audit.set_defaults(func=_cmd_audit)

    triage = sub.add_parser("triage", help="turn one failed run (gh JSON + log) into an issue body")
    triage.add_argument("--run", required=True)
    triage.add_argument("--log")
    triage.add_argument("--json", action="store_true", help="emit title/body/fingerprint as JSON")
    triage.set_defaults(func=_cmd_triage)

    coll = sub.add_parser("collect", help="group recent failed runs of a repo by fingerprint")
    coll.add_argument("--repo", required=True)
    coll.add_argument("--limit", type=int, default=30)
    coll.add_argument("--include-cancelled", action="store_true")
    coll.set_defaults(func=_cmd_collect)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
