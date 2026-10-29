"""Solution registry loading and deploy ordering (mirrors GHA-Dynamics compute-solutions)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Solution:
    name: str
    depends_on: tuple[str, ...] = ()


def load_registry(path: str | Path) -> list[Solution]:
    data = json.loads(Path(path).read_text())
    return [
        Solution(name=s["name"], depends_on=tuple(s.get("dependsOn", [])))
        for s in data["solutions"]
    ]


def deploy_order(solutions: list[Solution]) -> list[str]:
    """Return solution names in dependency order (dependencies first)."""
    indegree = {s.name: len(s.depends_on) for s in solutions}
    ready = sorted(n for n, d in indegree.items() if d == 0)
    order: list[str] = []
    while ready:
        current = ready.pop(0)
        order.append(current)
        for s in solutions:
            if current in s.depends_on:
                indegree[s.name] -= 1
                if indegree[s.name] == 0:
                    ready.append(s.name)
                    ready.sort()
    return order
