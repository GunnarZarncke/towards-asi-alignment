"""CI guard: graded_lab must not import lab_sim."""

from __future__ import annotations

import ast
from pathlib import Path

_PKG = Path(__file__).resolve().parent.parent / "graded_lab"


def _imports_in_file(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module.split(".")[0])
    return found


def test_graded_lab_does_not_import_lab_sim():
    offenders: list[str] = []
    for path in _PKG.rglob("*.py"):
        if "lab_sim" in _imports_in_file(path):
            offenders.append(str(path.relative_to(_PKG.parent)))
    assert not offenders, f"lab_sim imports forbidden: {offenders}"
