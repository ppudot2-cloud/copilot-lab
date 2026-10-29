"""Static audit of GitHub Actions workflow files for DevSecOps gaps."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

SEVERITIES = ("info", "low", "medium", "high")
FIRST_PARTY = {"actions", "github"}
MUTABLE_REFS = {"main", "master", "HEAD", "develop"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
# Event fields an outsider can control; interpolating them into `run:` allows injection.
UNTRUSTED_RE = re.compile(
    r"\$\{\{\s*(github\.event\.(issue\.(title|body)|pull_request\.(title|body|head\.ref|head\.label)"
    r"|comment\.body|review\.body|head_commit\.message)|github\.head_ref)\s*\}\}"
)
STATIC_SECRET_RE = re.compile(r"secrets\.\w*(SECRET|PAT|PASSWORD|TOKEN_KEY|API_KEY)\w*", re.I)
FAILURE_HANDLING_RE = re.compile(r"\b(failure|always|cancelled)\(\)")


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    file: str
    location: str
    message: str
    fix: str


def _triggers(doc: dict) -> dict:
    # PyYAML parses the bare key `on` as boolean True.
    raw = doc.get("on", doc.get(True, {}))
    if isinstance(raw, str):
        return {raw: None}
    if isinstance(raw, list):
        return {t: None for t in raw}
    return raw or {}


def _check_uses(ref: str, file: str, location: str) -> list[Finding]:
    if ref.startswith(("./", "docker://")) or "@" not in ref:
        return []
    target, version = ref.rsplit("@", 1)
    owner = target.split("/", 1)[0]
    if SHA_RE.match(version):
        return []
    if version in MUTABLE_REFS:
        return [Finding(
            "mutable-action-ref", "high", file, location,
            f"`{ref}` follows a moving branch; any push to it changes what runs here.",
            f"Pin to a release tag or full commit SHA: `{target}@<sha>  # vX.Y.Z`.",
        )]
    if owner in FIRST_PARTY:
        return [Finding(
            "unpinned-first-party-action", "low", file, location,
            f"`{ref}` uses a mutable tag.",
            f"Pin `{target}` to a commit SHA and let Dependabot bump it.",
        )]
    return [Finding(
        "unpinned-third-party-action", "medium", file, location,
        f"`{ref}` is third-party code pinned only by a mutable tag.",
        f"Pin `{target}` to a full commit SHA after reviewing it.",
    )]


def _check_job(job_id: str, job: dict, doc: dict, file: str) -> list[Finding]:
    out: list[Finding] = []
    loc = f"jobs.{job_id}"
    is_call = "uses" in job
    if is_call:
        out += _check_uses(str(job["uses"]), file, loc)
    if job.get("secrets") == "inherit":
        out.append(Finding(
            "secrets-inherit", "medium", file, loc,
            "`secrets: inherit` hands every repo and org secret to the called workflow.",
            "Pass only the secrets the callee declares, by name.",
        ))
    if "permissions" not in doc and "permissions" not in job:
        out.append(Finding(
            "missing-permissions", "medium", file, loc,
            "No `permissions` at workflow or job level; GITHUB_TOKEN gets the repo default.",
            "Add `permissions: {contents: read}` at workflow level, then widen per job.",
        ))
    if not is_call and "timeout-minutes" not in job:
        out.append(Finding(
            "missing-timeout", "medium", file, loc,
            "No `timeout-minutes`; a hung step runs until the 6 hour platform limit.",
            "Set `timeout-minutes` to about 2x the normal duration of the job.",
        ))
    for i, step in enumerate(job.get("steps") or []):
        sloc = f"{loc}.steps[{i}]"
        if "uses" in step:
            out += _check_uses(str(step["uses"]), file, sloc)
        run = step.get("run")
        if run and UNTRUSTED_RE.search(run):
            out.append(Finding(
                "script-injection", "high", file, sloc,
                "Untrusted event data is interpolated directly into a shell script.",
                "Move the value into `env:` and reference it as a shell variable.",
            ))
    return out


def audit_text(text: str, file: str = "<memory>") -> list[Finding]:
    doc = yaml.safe_load(text)
    if not isinstance(doc, dict):
        return [Finding("invalid-workflow", "high", file, "", "Not a YAML mapping.", "Fix syntax.")]
    jobs = doc.get("jobs") or {}
    findings: list[Finding] = []
    for job_id, job in jobs.items():
        findings += _check_job(job_id, job or {}, doc, file)

    has_env = any("environment" in (j or {}) for j in jobs.values())
    deploys = has_env or re.search(r"deploy|rollback|release", Path(file).name, re.I)
    job_concurrency = any("concurrency" in (j or {}) for j in jobs.values())
    if "concurrency" not in doc and not job_concurrency:
        findings.append(Finding(
            "missing-concurrency", "medium" if deploys else "low", file, "workflow",
            "No concurrency group; overlapping runs can race, especially on deploys.",
            "Add a `concurrency` group per ref; use `cancel-in-progress: false` for deploys.",
        ))
    if has_env and not FAILURE_HANDLING_RE.search(text):
        findings.append(Finding(
            "no-failure-handling", "medium", file, "workflow",
            "Deploys to environments but nothing reacts to failure (no failure()/always() step).",
            "Add a final job `if: failure()` that notifies and links the run and failing step.",
        ))
    triggers = _triggers(doc)
    if "pull_request_target" in triggers and re.search(r"ref:\s*\$\{\{[^}]*head", text):
        findings.append(Finding(
            "pwn-request", "high", file, "on.pull_request_target",
            "pull_request_target checks out untrusted PR code with a privileged token.",
            "Use `pull_request`, or never check out or run PR head code in this trigger.",
        ))
    perms = str(doc.get("permissions", ""))
    if STATIC_SECRET_RE.search(text) and "id-token" not in text and "id-token" not in perms:
        findings.append(Finding(
            "static-credential", "medium", file, "workflow",
            "Long-lived secrets are used for auth and no OIDC (`id-token: write`) is configured.",
            "Prefer OIDC federation to Azure so no client secret is stored in GitHub.",
        ))
    return findings


def audit_file(path: Path) -> list[Finding]:
    return audit_text(path.read_text(), str(path))


def audit_dir(root: Path) -> list[Finding]:
    files = sorted([*root.glob("*.yml"), *root.glob("*.yaml")])
    return [f for p in files for f in audit_file(p)]


def at_or_above(findings: list[Finding], level: str) -> list[Finding]:
    floor = SEVERITIES.index(level)
    return [f for f in findings if SEVERITIES.index(f.severity) >= floor]


def render_markdown(findings: list[Finding]) -> str:
    if not findings:
        return "No findings.\n"
    by_rule: dict[str, list[Finding]] = {}
    for f in findings:
        by_rule.setdefault(f.rule, []).append(f)
    order = sorted(by_rule, key=lambda r: (-SEVERITIES.index(by_rule[r][0].severity), r))
    lines = ["| Severity | Rule | Count | Fix |", "|---|---|---|---|"]
    for rule in order:
        first = by_rule[rule][0]
        lines.append(f"| {first.severity} | `{rule}` | {len(by_rule[rule])} | {first.fix} |")
    lines.append("")
    for rule in order:
        lines.append(f"### `{rule}` ({by_rule[rule][0].severity})")
        lines += [f"- `{f.file}` {f.location}" for f in by_rule[rule]]
        lines.append("")
    return "\n".join(lines)
