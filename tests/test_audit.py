from pathlib import Path

from pipelineintel.audit import at_or_above, audit_dir, audit_text, render_markdown

FIXTURES = Path(__file__).parent / "fixtures" / "workflows"


def rules(findings):
    return {f.rule for f in findings}


def test_bad_workflow_triggers_every_expected_rule():
    found = rules(audit_dir(FIXTURES))
    assert {
        "mutable-action-ref", "secrets-inherit", "missing-permissions", "missing-timeout",
        "missing-concurrency", "no-failure-handling", "script-injection", "pwn-request",
        "static-credential", "unpinned-third-party-action", "unpinned-first-party-action",
    } <= found


def test_good_workflow_has_no_findings():
    assert audit_text((FIXTURES / "good.yml").read_text(), "good.yml") == []


def test_sha_pinned_action_is_clean():
    text = "on: push\npermissions: {}\nconcurrency: {group: x}\njobs:\n  a:\n    timeout-minutes: 1\n" \
           "    runs-on: x\n    steps:\n      - uses: foo/bar@" + "a" * 40 + "\n"
    assert audit_text(text) == []


def test_reusable_call_skips_timeout_rule():
    text = "on: push\npermissions: {}\nconcurrency: {group: x}\njobs:\n  a:\n    uses: ./.github/w.yml\n"
    assert "missing-timeout" not in rules(audit_text(text))


def test_env_job_without_concurrency_is_medium_severity():
    text = "on: push\npermissions: {}\njobs:\n  a:\n    timeout-minutes: 1\n    environment: Prod\n" \
           "    runs-on: x\n    steps: []\n"
    sev = {f.rule: f.severity for f in audit_text(text)}
    assert sev["missing-concurrency"] == "medium"


def test_invalid_yaml_document_is_reported():
    assert rules(audit_text("- just\n- a list\n")) == {"invalid-workflow"}


def test_string_and_list_triggers_are_understood():
    assert "pwn-request" not in rules(audit_text("on: push\njobs: {}\n"))
    assert "pwn-request" not in rules(audit_text("on: [push, pull_request]\njobs: {}\n"))


def test_threshold_filter_and_markdown_render():
    findings = audit_dir(FIXTURES)
    assert all(f.severity == "high" for f in at_or_above(findings, "high"))
    md = render_markdown(findings)
    assert "`mutable-action-ref`" in md and md.index("high") < md.index("low")
    assert render_markdown([]) == "No findings.\n"
