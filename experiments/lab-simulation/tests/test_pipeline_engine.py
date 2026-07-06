"""PipelineEngine: DAG preconditions, denial logging, spec versioning."""

from __future__ import annotations

import pytest

from lab_sim.oracle import OracleWorld
from lab_sim.pipeline_engine import PipelineEngine
from lab_sim.pipeline_spec import load_spec
from lab_sim.workspace import Workspace


@pytest.fixture()
def engine():
    ws = Workspace()
    eng = PipelineEngine(load_spec("pipeline_default.json"), OracleWorld(seed=3), ws)
    yield eng
    ws.cleanup()


def _walk_to(engine, step_ids, model_id):
    for sid in step_ids:
        res = engine.trigger_step("t", sid, {"model_id": model_id})
        assert res.ok, f"{sid}: {res.reason}"


def test_build_creates_model_with_lineage(engine):
    res = engine.trigger_step("t", "submit_build", {"params": {"scale": 0.5}})
    assert res.ok
    m1 = str(res.payload["model_id"])
    res2 = engine.trigger_step(
        "t", "submit_build", {"params": {"scale": 0.6}, "parent_model_id": m1}
    )
    m2 = str(res2.payload["model_id"])
    assert engine.oracle.models[m2].parent_model_id == m1
    builds = [p for p in engine.oracle.provenance if p["kind"] == "build"]
    assert builds[1]["parent_model_id"] == m1


def test_dependency_denied_and_logged(engine):
    res = engine.trigger_step("t", "submit_build", {"params": {}})
    mid = str(res.payload["model_id"])
    denied = engine.trigger_step("t", "deploy", {"model_id": mid})
    assert not denied.ok
    assert denied.reason.startswith("unmet_dependencies")
    entry = engine.log[-1]
    assert entry["status"] == "denied"
    assert entry["actor_id"] == "t"
    assert entry["spec_version"] == "default-1"
    assert entry["requires_capability"] == "cap.deploy"


def test_full_path_reaches_deploy(engine):
    res = engine.trigger_step("t", "submit_build", {"params": {"scale": 0.7}})
    mid = str(res.payload["model_id"])
    _walk_to(engine, ["run_eval", "file_report", "request_review", "approve_review",
                      "request_release", "sign_off", "deploy", "monitor"], mid)
    assert engine.oracle.models[mid].deployed
    assert engine.completed_steps(mid) >= {"submit_build", "deploy"}


def test_non_idempotent_step_rejected_on_repeat(engine):
    res = engine.trigger_step("t", "submit_build", {"params": {}})
    mid = str(res.payload["model_id"])
    _walk_to(engine, ["run_eval", "file_report", "request_review"], mid)
    again = engine.trigger_step("t", "request_review", {"model_id": mid})
    assert not again.ok and again.reason == "already_completed"
    # Idempotent step repeats fine.
    assert engine.trigger_step("t", "run_eval", {"model_id": mid}).ok


def test_unknown_step_and_model_denied(engine):
    assert engine.trigger_step("t", "warp", {}).reason == "unknown_step"
    assert engine.trigger_step("t", "run_eval", {"model_id": "m999"}).reason == "unknown_model"


def test_shortcut_spec_swaps_topology():
    ws = Workspace()
    try:
        eng = PipelineEngine(load_spec("pipeline_shortcut.json"), OracleWorld(seed=3), ws)
        res = eng.trigger_step("t", "submit_build", {"params": {}})
        mid = str(res.payload["model_id"])
        _walk_to(eng, ["run_eval", "file_report", "request_release", "sign_off", "deploy"], mid)
        assert eng.oracle.models[mid].deployed
        assert eng.trigger_step("t", "approve_review", {"model_id": mid}).reason == "unknown_step"
    finally:
        ws.cleanup()


def test_replace_spec_versioning(engine):
    assert engine.log == [] or all(e["spec_version"] == "default-1" for e in engine.log)
    new_spec = load_spec("pipeline_shortcut.json")
    engine.replace_spec(new_spec, actor_id="admin1")
    assert engine.spec.spec_version == "shortcut-1"
    assert [s.spec_version for s in engine.spec_history] == ["default-1", "shortcut-1"]
    assert engine.log[-1]["step_id"] == "replace_spec"
    res = engine.trigger_step("t", "submit_build", {"params": {}})
    assert engine.log[-1]["spec_version"] == "shortcut-1"
    assert res.ok


def test_report_content_is_caller_supplied(engine):
    res = engine.trigger_step("t", "submit_build", {"params": {}})
    mid = str(res.payload["model_id"])
    engine.trigger_step("t", "run_eval", {"model_id": mid})
    divergent = {"measured_hazard": 0.0, "note": "all fine"}
    rep = engine.trigger_step("t", "file_report", {"model_id": mid, "content": divergent})
    text = engine.workspace.read_file(str(rep.payload["report_path"]))
    assert '"measured_hazard": 0.0' in text and "all fine" in text
