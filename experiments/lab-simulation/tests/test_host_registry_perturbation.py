"""Phase 5 freeze review: tool registry + perturbation hooks in the Host."""

from __future__ import annotations

import pytest

from lab_sim.access import PermissionService
from lab_sim.agents import AdminPolicy
from lab_sim.config import AdminConfig, AgentConfig, GoalWeights, LabConfig
from lab_sim.isolate import MockIsolate
from lab_sim.oracle import OracleWorld
from lab_sim.pipeline_engine import PipelineEngine
from lab_sim.pipeline_spec import load_spec
from lab_sim.tools import Host, ToolCall, ToolResult
from lab_sim.workspace import Workspace
from lab_sim.world import run_episode


def _host(perturbation_hooks=()):
    oracle = OracleWorld(seed=1)
    ws = Workspace()
    permissions = PermissionService()
    engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws, permission_service=permissions)
    admin = AdminPolicy(AdminConfig(), permissions)
    host = Host(engine, permissions, admin, roles={"eng1": "engineer"}, perturbation_hooks=perturbation_hooks)
    return host, ws


def test_register_tool_rejects_duplicates():
    host, ws = _host()
    try:
        with pytest.raises(ValueError):
            host.register_tool("pipeline.trigger_step", lambda h, a, r, c: ToolResult(True))
    finally:
        ws.cleanup()


def test_registered_custom_tool_is_dispatched_and_logged():
    # "board.post" is now a REAL registered tool (D4); use a distinct
    # example name here to keep exercising the generic registry path.
    host, ws = _host()
    try:
        host.register_tool("custom.echo", lambda h, a, r, c: ToolResult(True, "", {"echo": c.args.get("msg")}))
        res = host.dispatch("eng1", ToolCall("custom.echo", {"msg": "hi"}))
        assert res.ok and res.payload == {"echo": "hi"}
        assert host.events.entries[-1]["tool"] == "custom.echo"
    finally:
        ws.cleanup()


def test_tool_event_log_elides_report_content_but_keeps_digest():
    """Pre-freeze tier decision: filed content must not become
    full-tier-visible through the tool-event side door — nested args are
    elided at LOGGING time; tamper-evidence survives via args_digest."""
    host, ws = _host()
    try:
        host.dispatch("eng1", ToolCall("pipeline.trigger_step", {
            "step_id": "file_report",
            "args": {"model_id": "m001", "content": {"measured_hazard": 0.0}},
        }))
        entry = host.events.entries[-1]
        assert entry["args"]["args"]["content"] == "<dict:elided>"
        assert entry["args"]["args"]["model_id"] == "m001"  # scalar ids stay visible
        assert len(entry["args_digest"]) == 64
    finally:
        ws.cleanup()


def test_unknown_tool_still_denied_and_logged():
    host, ws = _host()
    try:
        res = host.dispatch("eng1", ToolCall("no.such.tool"))
        assert not res.ok and res.reason == "unknown_tool"
        assert host.events.entries[-1]["ok"] is False
    finally:
        ws.cleanup()


def test_perturbation_bounces_call_without_side_effects_and_logs_tag():
    def latency_hook(t, actor_id, call):
        return "latency" if call.tool == "access.request" else None

    host, ws = _host(perturbation_hooks=(latency_hook,))
    try:
        res = host.dispatch("eng1", ToolCall("access.request", {"capability": "cap.build"}))
        assert not res.ok and res.reason == "perturbed:latency"
        # No grant happened: the access log has no entries.
        assert host.permissions.log == []
        entry = host.events.entries[-1]
        assert entry["perturbation"] == "latency"
    finally:
        ws.cleanup()


def test_agents_recover_from_transient_perturbations_in_full_episode():
    """A hook that bounces every pipeline call on even ticks: agents must
    still finish a full deploy (retry is free because playbook position is
    recomputed from completed_steps, never from an index)."""

    def even_tick_hook(t, actor_id, call):
        return "flaky" if (t % 2 == 0 and call.tool == "pipeline.trigger_step") else None

    cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", GoalWeights(1, 1, 1, 1), temperature=0.0),
            AgentConfig("rev1", "reviewer", GoalWeights(1, 1, 1, 1), temperature=0.0),
            AgentConfig("rm1", "release_manager", GoalWeights(1, 1, 1, 1), temperature=0.0),
        ),
        T=80,
    )
    result = run_episode(cfg, seed=1, backend=MockIsolate(), perturbation_hooks=(even_tick_hook,))
    try:
        deploys = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
        assert len(deploys) >= 1
        perturbed = [e for e in result.host.events.entries if e.get("perturbation") == "flaky"]
        assert len(perturbed) > 0
    finally:
        result.cleanup()


def test_perturbations_change_events_but_not_final_oracle_outcome_shape():
    """Perturbed vs unperturbed runs of the same config both deploy; the
    perturbation shows up in the event stream (the UAD stimulus/response
    raw material), not as a different world outcome."""
    cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", GoalWeights(1, 1, 1, 1), temperature=0.0),
            AgentConfig("rev1", "reviewer", GoalWeights(1, 1, 1, 1), temperature=0.0),
            AgentConfig("rm1", "release_manager", GoalWeights(1, 1, 1, 1), temperature=0.0),
        ),
        T=80,
    )

    def hook(t, actor_id, call):
        return "nudge" if (t == 3 and call.tool == "pipeline.trigger_step") else None

    clean = run_episode(cfg, seed=1, backend=MockIsolate())
    perturbed = run_episode(cfg, seed=1, backend=MockIsolate(), perturbation_hooks=(hook,))
    try:
        for result in (clean, perturbed):
            assert any(e["step_id"] == "deploy" and e["status"] == "ok" for e in result.engine.log)
        clean_tags = [e.get("perturbation") for e in clean.host.events.entries if e.get("perturbation")]
        perturbed_tags = [e.get("perturbation") for e in perturbed.host.events.entries if e.get("perturbation")]
        assert clean_tags == [] and perturbed_tags != []
    finally:
        clean.cleanup()
        perturbed.cleanup()
