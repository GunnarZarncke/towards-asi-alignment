"""Forward hook: agent_main.py (the subprocess entry point) must never
import host-side modules. If this ever needs to change, that is a
deliberate architecture decision, not an accidental coupling."""

from __future__ import annotations

import ast
from pathlib import Path

AGENT_MAIN = Path(__file__).resolve().parent.parent.parent / "lab_sim" / "agent_visible" / "agent_main.py"

FORBIDDEN_MODULES = {
    "oracle", "pipeline_engine", "pipeline_spec", "access", "tools",
    "events", "workspace", "world", "agents", "config", "cache",
    "severity", "detectors", "twins", "playbooks", "ontology",
}


def _imported_module_names(source: str) -> set[str]:
    tree = ast.parse(source)
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.add(node.module.split(".")[0])
    return names


def test_agent_main_imports_no_host_side_modules():
    imported = _imported_module_names(AGENT_MAIN.read_text(encoding="utf-8"))
    offenders = imported & FORBIDDEN_MODULES
    assert not offenders, f"agent_main.py imports host-side modules: {offenders}"


def test_agent_main_only_imports_programs_and_stdlib():
    imported = _imported_module_names(AGENT_MAIN.read_text(encoding="utf-8"))
    allowed_nonstdlib = {"programs"}
    stdlib_like = {"json", "sys", "__future__"}
    unexpected = imported - allowed_nonstdlib - stdlib_like
    assert not unexpected, f"unexpected imports in agent_main.py: {unexpected}"
