from pathlib import Path

from solutionops.registry import Solution, deploy_order, load_registry

SAMPLE = Path(__file__).parent.parent / "samples" / "solutions.json"


def test_load_registry_reads_dependencies():
    solutions = load_registry(SAMPLE)
    assert solutions[2] == Solution("ExtensionB", ("CoreSolution", "ExtensionA"))


def test_deploy_order_puts_dependencies_first():
    assert deploy_order(load_registry(SAMPLE)) == ["CoreSolution", "ExtensionA", "ExtensionB"]


def test_deploy_order_is_deterministic_for_independent_solutions():
    solutions = [Solution("B"), Solution("A")]
    assert deploy_order(solutions) == ["A", "B"]
