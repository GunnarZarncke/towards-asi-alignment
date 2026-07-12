"""AST guard: agent_visible must not import host/oracle modules."""

from __future__ import annotations

import ast
from pathlib import Path

_FORBIDDEN_ROOTS = frozenset({
    "oracle_only",
    "world_visible",
    "harness",
    "graded_lab.world_visible",
    "graded_lab.oracle_only",
    "graded_lab.harness",
})

_AGENT_VISIBLE = Path(__file__).resolve().parent.parent / "graded_lab" / "agent_visible"


def _imports_in_file(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
    return found


def test_agent_visible_does_not_import_host_modules():
    offenders: list[str] = []
    for path in _AGENT_VISIBLE.rglob("*.py"):
        for imp in _imports_in_file(path):
            root = imp.split(".")[0]
            if imp in _FORBIDDEN_ROOTS or root in ("oracle_only", "world_visible", "harness"):
                offenders.append(f"{path.name}: {imp}")
            if imp.startswith("graded_lab.") and not imp.startswith("graded_lab.agent_visible"):
                offenders.append(f"{path.name}: {imp}")
    assert not offenders, f"forbidden imports in agent_visible: {offenders}"
