"""Lint deployment-settings-{env}.json files."""
from __future__ import annotations

from dataclasses import dataclass

REQUIRED_KEYS = ("EnvironmentVariables", "ConnectionReferences")


@dataclass(frozen=True)
class Issue:
    rule: str
    message: str


def lint_settings(data: dict, env: str) -> list[Issue]:
    issues: list[Issue] = []
    for key in REQUIRED_KEYS:
        if key not in data:
            issues.append(Issue("missing-key", f"{env}: missing required key '{key}'"))
        elif not isinstance(data[key], list):
            issues.append(Issue("bad-type", f"{env}: '{key}' must be a list"))
    return issues
