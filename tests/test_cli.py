import json
from pathlib import Path

from solutionops.cli import main

SAMPLE = Path(__file__).parent.parent / "samples" / "solutions.json"


def test_order_prints_names(capsys):
    assert main(["order", str(SAMPLE)]) == 0
    assert capsys.readouterr().out.split() == ["CoreSolution", "ExtensionA", "ExtensionB"]


def test_lint_returns_nonzero_on_issues(tmp_path, capsys):
    f = tmp_path / "s.json"
    f.write_text(json.dumps({}))
    assert main(["lint", str(f), "--env", "dev"]) == 1
    assert "missing-key" in capsys.readouterr().out
