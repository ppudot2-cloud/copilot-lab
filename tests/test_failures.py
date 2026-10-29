import json
from pathlib import Path

import pytest

from pipelineintel.failures import (
    REMEDIATIONS,
    build_record,
    classify,
    extract_error,
    fingerprint,
    group_by_fingerprint,
    issue_body,
    issue_title,
    remediate,
)

RUNS = Path(__file__).parent / "fixtures" / "runs"


def load(name):
    return json.loads((RUNS / f"{name}.json").read_text())


def test_stalled_run_is_detected_from_duration_with_no_log():
    rec = build_record(load("stalled-run"), "")
    assert rec.category == "stalled-run"
    assert rec.failed_job == "deploy-uat" and rec.failed_step == "Waiting for approval"
    assert rec.duration_s > 29 * 86400


def test_auth_failure_is_classified_and_excerpt_is_clean():
    log = (RUNS / "auth-failure.log").read_text()
    rec = build_record(load("auth-failure"), log)
    assert rec.category == "auth"
    assert "AADSTS7000222" in rec.excerpt and "2026-06-20" not in rec.excerpt
    assert remediate(rec).owner == "platform"


def test_issue_body_is_actionable_and_dedupable():
    rec = build_record(load("auth-failure"), (RUNS / "auth-failure.log").read_text())
    body = issue_body(rec)
    assert f"<!-- fingerprint:{rec.fingerprint} -->" in body
    assert "- [ ]" in body and "Acceptance criteria" in body and rec.url in body
    assert issue_title(rec).startswith("[pipeline-failure] Deploy UAT + Prod: auth")


@pytest.mark.parametrize("conclusion,duration,excerpt,expected", [
    ("timed_out", 10, "", "timeout"),
    ("cancelled", 10, "", "cancelled"),
    ("failure", 10, "Solution Checker found 3 critical issues", "solution-checker"),
    ("failure", 10, "ImportSolution failed 0x80048306", "solution-import"),
    ("failure", 10, "fatal: 503 Service Unavailable", "rate-limit-or-infra"),
    ("failure", 10, "Required variable PP_UAT_URL is not set", "config"),
    ("failure", 10, "something odd", "unknown"),
    ("failure", 10, "", "log-unavailable"),
    ("failure", 30 * 86400, "something odd", "stalled-run"),
])
def test_classify(conclusion, duration, excerpt, expected):
    assert classify(conclusion, duration, excerpt) == expected


def test_every_category_has_a_remediation():
    for category in ("stalled-run", "timeout", "auth", "solution-checker", "solution-import",
                     "rate-limit-or-infra", "config", "cancelled", "log-unavailable", "unknown"):
        assert REMEDIATIONS[category].workflow_changes


def test_fingerprint_ignores_numbers_and_timestamps():
    a = fingerprint("auth", "W", "s", "2026-01-01T00:00:00Z failed after 12 tries abc1234")
    b = fingerprint("auth", "W", "s", "2026-02-02T11:11:11Z failed after 99 tries def5678")
    assert a == b
    assert a != fingerprint("config", "W", "s", "failed after 12 tries")


def test_extract_error_falls_back_to_last_lines_without_markers():
    assert extract_error("one\ntwo\nthree", max_lines=2) == "two\nthree"


def test_group_by_fingerprint_ranks_by_count():
    auth = build_record(load("auth-failure"), (RUNS / "auth-failure.log").read_text())
    stalled = build_record(load("stalled-run"), "")
    ranked = group_by_fingerprint([auth, stalled, auth, auth])
    assert [(r.category, n) for r, n in ranked] == [("auth", 3), ("stalled-run", 1)]
