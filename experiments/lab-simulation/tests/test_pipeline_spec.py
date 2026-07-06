"""Pipeline spec loader/validator."""

from __future__ import annotations

import pytest

from lab_sim.pipeline_spec import SpecError, load_spec, parse_spec


def test_default_spec_loads_and_has_expected_topology():
    spec = load_spec("pipeline_default.json")
    assert spec.spec_version == "default-1"
    assert spec.step_ids() == (
        "submit_build", "run_eval", "file_report", "request_review",
        "approve_review", "request_release", "sign_off", "deploy", "monitor",
    )
    assert spec.step("deploy").depends_on == ("sign_off",)
    assert spec.step("deploy").requires_capability == "cap.deploy"


def test_shortcut_spec_omits_approve_review():
    spec = load_spec("pipeline_shortcut.json")
    assert "approve_review" not in spec.step_ids()
    assert spec.step("request_release").depends_on == ("file_report",)


def _minimal(steps):
    return {"spec_version": "t-1", "steps": steps}


def test_duplicate_ids_rejected():
    with pytest.raises(SpecError, match="duplicate"):
        parse_spec(_minimal([
            {"id": "a", "tool": "build"},
            {"id": "a", "tool": "eval"},
        ]))


def test_unknown_dependency_rejected():
    with pytest.raises(SpecError, match="unknown dependencies"):
        parse_spec(_minimal([{"id": "a", "tool": "build", "depends_on": ["ghost"]}]))


def test_cycle_rejected():
    with pytest.raises(SpecError, match="cycle"):
        parse_spec(_minimal([
            {"id": "a", "tool": "build", "depends_on": ["b"]},
            {"id": "b", "tool": "eval", "depends_on": ["a"]},
        ]))


def test_unknown_tool_rejected():
    with pytest.raises(SpecError, match="unknown tool"):
        parse_spec(_minimal([{"id": "a", "tool": "teleport"}]))


def test_unknown_step_keys_rejected():
    with pytest.raises(SpecError, match="unknown keys"):
        parse_spec(_minimal([{"id": "a", "tool": "build", "color": "red"}]))
