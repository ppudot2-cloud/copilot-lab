"""Pull failed runs from GitHub via the gh CLI and turn them into FailureRecords."""
from __future__ import annotations

import json
import subprocess
from collections.abc import Callable

from .failures import FailureRecord, build_record

Runner = Callable[[list[str]], str]
RUN_FIELDS = "databaseId,workflowName,headBranch,event,conclusion,startedAt,updatedAt,url,jobs"
BAD = {"failure", "timed_out", "cancelled"}


def gh(args: list[str]) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def collect(repo: str, limit: int = 30, run: Runner = gh,
            include_cancelled: bool = False) -> list[FailureRecord]:
    listing = json.loads(run(["run", "list", "--repo", repo, "--limit", str(limit),
                              "--json", "databaseId,conclusion,status"]))
    wanted = BAD if include_cancelled else BAD - {"cancelled"}
    records: list[FailureRecord] = []
    for item in listing:
        if item.get("conclusion") not in wanted:
            continue
        rid = str(item["databaseId"])
        detail = json.loads(run(["run", "view", rid, "--repo", repo, "--json", RUN_FIELDS]))
        try:
            log = run(["run", "view", rid, "--repo", repo, "--log-failed"])
        except RuntimeError:
            log = ""  # logs expire or are unavailable; still classify from metadata
        records.append(build_record(detail, log))
    return records
