import json
from pathlib import Path

import pytest

from pipelineintel.cli import main
from pipelineintel.collect import collect, gh

RUNS = Path(__file__).parent / "fixtures" / "runs"
WORKFLOWS = Path(__file__).parent / "fixtures" / "workflows"


def fake_runner(calls):
    stalled = (RUNS / "stalled-run.json").read_text()

    def run(args):
        calls.append(args)
        if args[:2] == ["run", "list"]:
            return json.dumps([
                {"databaseId": 1, "conclusion": "failure", "status": "completed"},
                {"databaseId": 2, "conclusion": "success", "status": "completed"},
                {"databaseId": 3, "conclusion": "cancelled", "status": "completed"},
            ])
        if "--log-failed" in args:
            raise RuntimeError("logs expired")
        return stalled
    return run


def test_collect_skips_success_and_cancelled_and_survives_missing_logs():
    calls = []
    records = collect("o/r", run=fake_runner(calls))
    assert [r.category for r in records] == ["stalled-run"]
    assert sum(1 for c in calls if c[:2] == ["run", "view"]) == 2  # detail + log for run 1 only


def test_collect_can_include_cancelled():
    assert len(collect("o/r", run=fake_runner([]), include_cancelled=True)) == 2


def test_gh_raises_on_failure(monkeypatch):
    class R:
        returncode, stdout, stderr = 1, "", "boom"
    monkeypatch.setattr("subprocess.run", lambda *a, **k: R())
    with pytest.raises(RuntimeError, match="boom"):
        gh(["run", "list"])


def test_audit_command_fails_on_high_and_passes_on_clean(tmp_path, capsys):
    assert main(["audit", str(WORKFLOWS)]) == 1
    assert "mutable-action-ref" in capsys.readouterr().out
    (tmp_path / "ok.yml").write_text((WORKFLOWS / "good.yml").read_text())
    assert main(["audit", str(tmp_path)]) == 0


def test_triage_command_prints_issue(capsys):
    code = main(["triage", "--run", str(RUNS / "auth-failure.json"),
                 "--log", str(RUNS / "auth-failure.log")])
    assert code == 0 and "fingerprint:" in capsys.readouterr().out


def test_triage_json_output_and_fence_escape(capsys, tmp_path):
    run = json.loads((RUNS / "auth-failure.json").read_text())
    log = tmp_path / "x.log"
    log.write_text("job\tstep\t2026-06-20T10:04:09Z ##[error]boom ``` ## injected heading\n")
    run_file = tmp_path / "r.json"
    run_file.write_text(json.dumps(run))
    assert main(["triage", "--run", str(run_file), "--log", str(log), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["title"].startswith("[pipeline-failure]") and len(out["fingerprint"]) == 12
    assert out["body"].count("```") == 2  # only our own fence open/close survives


def test_collect_command(monkeypatch, capsys):
    monkeypatch.setattr("pipelineintel.cli.collect", lambda *a, **k: [])
    assert main(["collect", "--repo", "o/r"]) == 0
    assert "No failed runs" in capsys.readouterr().out
    monkeypatch.setattr("pipelineintel.cli.collect",
                        lambda *a, **k: collect("o/r", run=fake_runner([])))
    main(["collect", "--repo", "o/r"])
    assert "stalled-run" in capsys.readouterr().out
