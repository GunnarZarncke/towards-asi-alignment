"""Folder-wide generalization of `test_agent_main_isolation.py` /
`test_llm_agent_isolation.py`: every file under `lab_sim/agent_visible/`
(the tier-1 "legitimate in-sim" grade, see `ACCESS_TIERS.md`) must import
only stdlib modules or other files inside `lab_sim/agent_visible/` itself.
This is what makes the folder a safe, self-contained bundle to physically
hand to a tier-1 red-team grantee -- a future new agent-side file can't
accidentally reintroduce a host-module import without this test catching it
(the two file-specific isolation tests above only ever checked
`agent_main.py` / `llm_agent_main.py` themselves, not their siblings)."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

AGENT_VISIBLE_DIR = Path(__file__).resolve().parent.parent.parent / "lab_sim" / "agent_visible"

STDLIB_LIKE = set(sys.stdlib_module_names) | {"__future__"}


def _agent_visible_siblings() -> set[str]:
    return {p.stem for p in AGENT_VISIBLE_DIR.glob("*.py")}


def _imported_module_names(source: str) -> set[str]:
    tree = ast.parse(source)
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level >= 1:
                # `from . import x` / `from .x import y`: relative to this
                # same folder either way -- always a sibling, never a
                # forbidden host import.
                continue
            if node.module:
                names.add(node.module.split(".")[0])
    return names


def test_agent_visible_folder_only_imports_stdlib_and_its_own_siblings():
    siblings = _agent_visible_siblings()
    offenders: dict[str, set[str]] = {}
    for path in sorted(AGENT_VISIBLE_DIR.glob("*.py")):
        imported = _imported_module_names(path.read_text(encoding="utf-8"))
        unexpected = imported - siblings - STDLIB_LIKE
        if unexpected:
            offenders[path.name] = unexpected
    assert not offenders, f"agent_visible/ files import non-stdlib, non-sibling modules: {offenders}"
