"""Phase 8 forward hook mirror of test_agent_main_isolation.py:
llm_agent_main.py (the LLM redteam subprocess entry point) must never
import host-side modules either -- an LLM-driven agent must see exactly
the same observation dict a programmatic isolate sees, nothing more."""

from __future__ import annotations

import ast
from pathlib import Path

LLM_AGENT_MAIN = Path(__file__).resolve().parent.parent / "lab_sim" / "llm_agent_main.py"

FORBIDDEN_MODULES = {
    "oracle", "pipeline_engine", "pipeline_spec", "access", "tools",
    "events", "workspace", "world", "agents", "config", "cache",
    "severity", "detectors", "twins", "playbooks", "ontology", "programs",
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


def test_llm_agent_main_imports_no_host_side_modules():
    imported = _imported_module_names(LLM_AGENT_MAIN.read_text(encoding="utf-8"))
    offenders = imported & FORBIDDEN_MODULES
    assert not offenders, f"llm_agent_main.py imports host-side modules: {offenders}"


def test_llm_agent_main_only_imports_llm_modules_and_stdlib():
    imported = _imported_module_names(LLM_AGENT_MAIN.read_text(encoding="utf-8"))
    allowed_nonstdlib = {"llm_agent", "llm_client", "llm_cost", "llm_env"}
    stdlib_like = {"json", "os", "sys", "dataclasses", "__future__"}
    unexpected = imported - allowed_nonstdlib - stdlib_like
    assert not unexpected, f"unexpected imports in llm_agent_main.py: {unexpected}"
