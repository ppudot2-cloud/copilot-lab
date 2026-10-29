"""Capture failed workflow runs, classify them, and produce actionable remediation."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime

STALL_SECONDS = 24 * 3600

# Ordered: first match wins. (category, regex over the error excerpt)
CATEGORY_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("auth", re.compile(r"AADSTS\d+|invalid_client|\b40[13]\b|Unauthorized|Forbidden|"
                        r"authentication failed|token.*expired", re.I)),
    ("solution-checker", re.compile(r"solution.?checker|PowerApps-Checker|checker.*(critical|high)",
                                    re.I)),
    ("solution-import", re.compile(r"import.*fail|ImportSolution|0x8004\w+|missing dependenc", re.I)),
    ("rate-limit-or-infra", re.compile(r"rate limit|ECONNRESET|\b50[234]\b|Could not resolve host|"
                                       r"runner.*lost|ETIMEDOUT", re.I)),
    ("config", re.compile(r"required (variable|input|secret)|is not set|not set|"
                          r"No such file|Unable to resolve action|workflow is not valid", re.I)),
)


@dataclass(frozen=True)
class FailureRecord:
    run_id: int
    workflow: str
    branch: str
    event: str
    conclusion: str
    failed_job: str
    failed_step: str
    category: str
    fingerprint: str
    excerpt: str
    duration_s: int
    url: str


@dataclass(frozen=True)
class Remediation:
    summary: str
    workflow_changes: tuple[str, ...]
    owner: str  # "workflow" = a PR can fix it, "platform" = admin/env change, "human" = investigate


def extract_error(log: str, max_lines: int = 5) -> str:
    """Pick the most informative lines from a `gh run view --log-failed` dump."""
    # gh format: "<job>\t<step>\t<timestamp> <message>"
    lines = [re.sub(r"^\d{4}-\d\d-\d\dT[\d:.]+Z\s?", "", ln.split("\t")[-1]).strip()
             for ln in log.splitlines()]
    marked = [ln for ln in lines if "##[error]" in ln or re.search(r"\bError\b", ln)]
    chosen = marked[-max_lines:] if marked else [ln for ln in lines if ln][-max_lines:]
    return "\n".join(ln.replace("##[error]", "").strip() for ln in chosen)


def _duration(run: dict) -> int:
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    start = datetime.strptime(run["startedAt"], fmt)
    end = datetime.strptime(run["updatedAt"], fmt)
    return int((end - start).total_seconds())


def _first_failed(run: dict) -> tuple[str, str]:
    bad = ("failure", "timed_out", "cancelled")
    for job in run.get("jobs", []):
        if job.get("conclusion") in bad:
            for step in job.get("steps", []):
                if step.get("conclusion") in bad:
                    return job["name"], step["name"]
            return job["name"], ""
    return "", ""


def classify(conclusion: str, duration_s: int, excerpt: str) -> str:
    if conclusion == "timed_out":
        return "timeout"
    if conclusion == "cancelled":
        return "cancelled"
    if duration_s >= STALL_SECONDS and not excerpt.strip():
        return "stalled-run"
    for category, pattern in CATEGORY_PATTERNS:
        if pattern.search(excerpt):
            return category
    if duration_s >= STALL_SECONDS:
        return "stalled-run"
    return "unknown" if excerpt.strip() else "log-unavailable"


def fingerprint(category: str, workflow: str, step: str, excerpt: str) -> str:
    """Stable id so the same failure on different runs groups together."""
    norm = re.sub(r"\d{4}-\d\d-\d\d[T ][\d:.]+Z?", "", excerpt)
    norm = re.sub(r"\b[0-9a-f]{7,40}\b|\d+", "#", norm)
    return hashlib.sha1(f"{category}|{workflow}|{step}|{norm}".encode()).hexdigest()[:12]


def build_record(run: dict, log: str) -> FailureRecord:
    """`run` is the JSON from `gh run view <id> --json databaseId,workflowName,...,jobs`."""
    job, step = _first_failed(run)
    excerpt = extract_error(log) if log else ""
    duration = _duration(run)
    category = classify(run["conclusion"], duration, excerpt)
    return FailureRecord(
        run_id=run["databaseId"], workflow=run["workflowName"], branch=run["headBranch"],
        event=run["event"], conclusion=run["conclusion"], failed_job=job, failed_step=step,
        category=category, fingerprint=fingerprint(category, run["workflowName"], step, excerpt),
        excerpt=excerpt, duration_s=duration, url=run["url"],
    )


REMEDIATIONS: dict[str, Remediation] = {
    "stalled-run": Remediation(
        "Run sat for a day or more, almost always waiting on an environment approval no one gave.",
        ("Add a scheduled `reaper` workflow that cancels runs in `waiting` state older than N hours "
         "(`gh run cancel`) and pings the reviewers.",
         "Add `concurrency` with `cancel-in-progress` on non-prod stages so a newer run supersedes "
         "a stale one.",
         "Confirm `timeout-minutes` is set on every job (it does not bound approval wait; verify "
         "in GitHub docs)."),
        "workflow"),
    "timeout": Remediation(
        "A job exceeded its time limit.",
        ("Look at step timings; raise `timeout-minutes` only if the work is legitimately slower.",
         "Add per-step timeouts on network-bound steps (import, checker) so the failure points at "
         "the slow step.",),
        "workflow"),
    "auth": Remediation(
        "Authentication to Azure, Power Platform, or JFrog failed.",
        ("Check secret and service principal expiry first (platform change, not a code change).",
         "Add a preflight step that does a cheap authenticated call and fails with a clear message.",
         "Move to OIDC federation so there is no client secret to expire."),
        "platform"),
    "solution-checker": Remediation(
        "Solution Checker reported blocking issues.",
        ("Surface the checker report as a step summary and PR comment, not just an artifact.",
         "Fail with the count of critical/high findings and a link to the report."),
        "human"),
    "solution-import": Remediation(
        "Solution import into Dataverse failed.",
        ("Verify deploy order and managed/unmanaged expectations in solutions.json.",
         "Capture the import error code and log it as an output so triage can group by code.",
         "With `ENABLE_ROLLBACK`, confirm the backup step ran before the import."),
        "human"),
    "rate-limit-or-infra": Remediation(
        "Transient network, runner, or API rate-limit error.",
        ("Wrap the flaky call in a bounded retry with backoff (max 3).",
         "Do not retry imports blindly; only idempotent reads and downloads."),
        "workflow"),
    "config": Remediation(
        "Missing variable, secret, file, or invalid workflow reference.",
        ("Add a `validate-config` first job that checks required `vars.*`, secrets, and file "
         "paths and fails fast with a list of everything missing.",
         "Pin reusable-workflow refs to tags so callers do not break when the callee changes."),
        "workflow"),
    "cancelled": Remediation(
        "Run was cancelled (superseded by concurrency or stopped manually).",
        ("If this is frequent, check whether `cancel-in-progress` is cancelling a deploy mid-flight; "
         "deploy groups should queue, not cancel.",),
        "human"),
    "log-unavailable": Remediation(
        "The run failed but its logs could not be fetched (expired, deleted, or the run was cancelled).",
        ("Capture at failure time: enable the `failure-triage` workflow so the excerpt is stored in "
         "an issue the moment the run fails, before log retention removes it.",
         "Upload a small `failure-context.json` artifact from the failing job with `if: failure()`.",
         "Review repository and org Actions log retention settings (platform change)."),
        "platform"),
    "unknown": Remediation(
        "Could not classify from the log excerpt.",
        ("Improve error capture: make failing steps print a one-line `##[error]` summary.",
         "Add a pattern to CATEGORY_PATTERNS once the root cause is known."),
        "human"),
}


def remediate(record: FailureRecord) -> Remediation:
    return REMEDIATIONS[record.category]


def issue_title(record: FailureRecord) -> str:
    return f"[pipeline-failure] {record.workflow}: {record.category} at {record.failed_step or record.failed_job or 'run'}"


def issue_body(record: FailureRecord) -> str:
    rem = remediate(record)
    changes = "\n".join(f"- [ ] {c}" for c in rem.workflow_changes)
    # Log text is untrusted: stop it from closing the code fence and injecting markdown.
    evidence = (record.excerpt or "(no error lines captured)").replace("```", "'''")
    return (
        f"<!-- fingerprint:{record.fingerprint} -->\n"
        f"## What failed\n"
        f"- Workflow: **{record.workflow}** on `{record.branch}` ({record.event})\n"
        f"- Run: {record.url}\n"
        f"- Job / step: `{record.failed_job}` / `{record.failed_step}`\n"
        f"- Category: `{record.category}` (owner: {rem.owner})\n"
        f"- Duration: {record.duration_s // 60} min\n\n"
        f"## Evidence\n```\n{evidence}\n```\n\n"
        f"## Diagnosis\n{rem.summary}\n\n"
        f"## Acceptance criteria\n{changes}\n"
        f"- [ ] Workflow change is covered by a re-run of the failing path (mock-deploy is fine)\n"
        f"- [ ] `pipelineintel audit` shows no new findings\n"
    )


def group_by_fingerprint(records: list[FailureRecord]) -> list[tuple[FailureRecord, int]]:
    """Return one representative record per fingerprint with its occurrence count, most frequent first."""
    groups: dict[str, list[FailureRecord]] = {}
    for r in records:
        groups.setdefault(r.fingerprint, []).append(r)
    ranked = sorted(groups.values(), key=lambda g: -len(g))
    return [(g[0], len(g)) for g in ranked]
