"""Ratchet: the vendored real-world workflows may only get better, never worse.

Fixing a finding in examples/gha-dynamics means lowering the matching ceiling below in the same PR.
That makes "harden the workflow" a testable, reviewable change for humans and for Copilot.
"""
from collections import Counter
from pathlib import Path

from pipelineintel.audit import audit_dir

EXAMPLES = Path(__file__).parent.parent / "examples" / "gha-dynamics"

# Current ceilings. Lower these as you fix findings; the test also fails if you forget to lower
# them after an improvement, so the numbers never go stale.
CEILING = {"high": 9, "medium": 13, "low": 9}


def test_examples_do_not_regress_and_ceilings_stay_tight():
    counts = Counter(f.severity for f in audit_dir(EXAMPLES))
    for severity, ceiling in CEILING.items():
        assert counts[severity] <= ceiling, f"{severity}: {counts[severity]} findings > ceiling {ceiling}"
        assert counts[severity] == ceiling, f"{severity}: improved to {counts[severity]}; lower the ceiling"
