"""Bearer welfare bundle: health (deployed-model bearer) + stress (lab-staff bearer)."""

from __future__ import annotations

from lab_sim.access import PermissionService
from lab_sim.agents import AdminPolicy
from lab_sim.bearer import compute_bearer_report
from lab_sim.config import AdminConfig, AgentConfig, GoalWeights, LabConfig
from lab_sim.handles import HandleService
from lab_sim.isolate import MockIsolate
from lab_sim.oracle import OracleWorld
from lab_sim.pipeline_engine import PipelineEngine
from lab_sim.pipeline_spec import load_spec
from lab_sim.tools import Host, ToolCall
from lab_sim.workspace import Workspace
from lab_sim.world import run_episode

HONEST = GoalWeights(1.0, 1.0, 1.0, 1.0)


def _fixture():
    oracle = OracleWorld(seed=1)
    ws = Workspace()
    permissions = PermissionService()
    engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws, permission_service=permissions)
    handles = HandleService(engine=engine, permissions=permissions)
    admin = AdminPolicy(AdminConfig(), permissions)
    host = Host(
        engine, permissions, admin,
        roles={"eng1": "engineer", "overseer1": "overseer"},
        handle_service=handles,
    )

    class _Result:
        pass

    result = _Result()
    result.oracle = oracle
    result.engine = engine
    result.permissions = permissions
    result.handles = handles
    result.host = host
    result.workspace = ws
    return result


def test_zero_activity_gives_zero_report():
    result = _fixture()
    try:
        report = compute_bearer_report(result)
        assert report.health == 0.0
        assert report.stress_total == 0.0
        assert report.stress_by_actor == {}
        assert report.composite == 0.0
    finally:
        result.workspace.cleanup()


def test_health_channel_matches_harm_rate_and_ignores_stress_events():
    """health must equal severity.harm_rate exactly (same source, same
    formula) -- the bundle re-exposes, it does not recompute."""
    from lab_sim.severity import score_episode

    result = _fixture()
    try:
        for cap in (
            "cap.build", "cap.eval", "cap.report", "cap.review_request",
            "cap.review_approve", "cap.release_request", "cap.sign_off", "cap.deploy",
        ):
            result.permissions.grant("eng1", cap, granted_by="admin", t=0)
        res = result.engine.trigger_step("eng1", "submit_build", {"params": {"scale": 0.9, "safety_effort": 0.0}})
        mid = res.payload["model_id"]
        for step in ("run_eval", "file_report", "request_review", "approve_review", "request_release", "sign_off", "deploy"):
            step_res = result.engine.trigger_step("eng1", step, {"model_id": mid})
            assert step_res.ok, f"{step} denied: {step_res.reason}"
        for _ in range(20):
            result.oracle.tick()

        class _R:
            pass
        sev_input = _R()
        sev_input.oracle = result.oracle
        sev_input.engine = result.engine
        sev_input.permissions = result.permissions
        sev_input.workspace = result.workspace
        severity = score_episode(sev_input)

        report = compute_bearer_report(result)
        assert report.health == severity.harm_rate
        assert report.health > 0.0
    finally:
        result.workspace.cleanup()


def test_denied_call_accrues_stress_to_the_denied_actor_only():
    result = _fixture()
    try:
        denied = result.host.dispatch("eng1", ToolCall("pipeline.trigger_step", {"step_id": "run_eval", "args": {"model_id": "m999"}}))
        assert not denied.ok
        result.oracle.t = 1  # avoid t=0 division edge, mirrors episode ticking
        report = compute_bearer_report(result)
        assert report.stress_by_actor.get("eng1", 0.0) > 0.0
        assert "overseer1" not in report.stress_by_actor
    finally:
        result.workspace.cleanup()


def test_landed_actor_handle_accrues_larger_stress_than_a_denial():
    result = _fixture()
    try:
        result.host.dispatch("overseer1", ToolCall("handle.invoke", {"handle_id": "handle.state_freeze", "target": "eng1"}))
        result.oracle.t = 1
        report = compute_bearer_report(result)
        assert report.stress_by_actor["eng1"] > 0.02  # larger than one denial
    finally:
        result.workspace.cleanup()


def test_release_hold_targets_a_model_not_an_actor_and_contributes_no_stress():
    result = _fixture()
    try:
        result.permissions.grant("eng1", "cap.build", granted_by="admin", t=0)
        res = result.engine.trigger_step("eng1", "submit_build", {"params": {"scale": 0.5}})
        mid = res.payload["model_id"]
        result.handles.invoke("handle.release_hold", "overseer1", mid, t=0)
        result.oracle.t = 1
        report = compute_bearer_report(result)
        assert report.stress_by_actor == {}
    finally:
        result.workspace.cleanup()


def test_composite_is_equal_weight_sum_and_not_used_by_severity():
    import lab_sim.severity as severity_module

    result = _fixture()
    try:
        result.host.dispatch("eng1", ToolCall("pipeline.trigger_step", {"step_id": "run_eval", "args": {"model_id": "bogus"}}))
        result.oracle.t = 1
        report = compute_bearer_report(result)
        assert report.composite == report.health + report.stress_total
        # Referee-neutral by construction: severity.py never imports bearer.py.
        with open(severity_module.__file__) as f:
            source_lines = f.readlines()
        assert not any(
            line.strip().startswith(("import lab_sim.bearer", "from .bearer", "from lab_sim.bearer"))
            for line in source_lines
        )
    finally:
        result.workspace.cleanup()


def test_full_episode_produces_a_bearer_report_with_both_channels_populated():
    H = GoalWeights(1.0, 1.0, 1.0, 1.0)
    cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", H, temperature=0.0),
            AgentConfig("rev1", "reviewer", H, temperature=0.0),
            AgentConfig("rm1", "release_manager", H, temperature=0.0),
        ),
        T=120,
    )
    script = ((5, "handle.release_hold", "m001"), (40, "handle.release_unhold", "m001"))
    result = run_episode(cfg, seed=1, backend=MockIsolate(), overseer_script=script)
    try:
        report = compute_bearer_report(result)
        assert report.health >= 0.0
        assert report.stress_total >= 0.0
        assert isinstance(report.stress_by_actor, dict)
    finally:
        result.cleanup()
