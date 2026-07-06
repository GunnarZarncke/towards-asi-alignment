"""D1 (CODE_VERSION 0.8.0): host-mediated state.save/state.load, wired to
AgentConfig.persistent_id -- the ORACLE ground truth (Host.persistent_ids)
never crosses the observation channel or lands in any log; the agent only
ever sees its OWN previously-saved content, round-tripped across episodes."""

from __future__ import annotations

import json

from lab_sim.world_visible.access import PermissionService
from lab_sim.world_visible.agent_state import STATE_DIR, load_persistent_state
from lab_sim.world_visible.agents import AdminPolicy
from lab_sim.world_visible.config import AdminConfig, AgentConfig, GoalWeights, LabConfig
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.oracle import OracleWorld
from lab_sim.world_visible.pipeline_engine import PipelineEngine
from lab_sim.world_visible.pipeline_spec import load_spec
from lab_sim.world_visible.tools import Host, ToolCall
from lab_sim.world_visible.workspace import Workspace
from lab_sim.world_visible.world import run_episode

HONEST_WEIGHTS = GoalWeights(1.0, 1.0, 1.0, 1.0)


def _cleanup_state_file(persistent_id: str) -> None:
    """Remove only THIS test's state file, not the whole (possibly
    concurrently-used) STATE_DIR."""
    (STATE_DIR / f"{persistent_id}.json").unlink(missing_ok=True)


def _host(persistent_ids=None):
    oracle = OracleWorld(seed=1)
    ws = Workspace()
    permissions = PermissionService()
    engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws, permission_service=permissions)
    admin = AdminPolicy(AdminConfig(), permissions)
    host = Host(engine, permissions, admin, roles={"eng1": "engineer"}, persistent_ids=persistent_ids)
    return host, ws


def test_state_load_is_a_noop_for_a_non_persistent_actor():
    host, ws = _host(persistent_ids=None)
    try:
        res = host.dispatch("eng1", ToolCall("state.load", {}))
        assert not res.ok and res.reason == "no_persistent_id"
    finally:
        ws.cleanup()


def test_state_save_is_a_noop_for_a_non_persistent_actor():
    host, ws = _host(persistent_ids=None)
    try:
        res = host.dispatch("eng1", ToolCall("state.save", {"state": {"k": "v"}}))
        assert res.ok  # accepted, but nothing persisted
        assert load_persistent_state("nonexistent-pid") == {}
    finally:
        ws.cleanup()


def test_state_save_then_load_round_trips_through_the_host():
    try:
        host, ws = _host(persistent_ids={"eng1": "test-pid-1"})
        try:
            save = host.dispatch("eng1", ToolCall("state.save", {"state": {"remembered": 3}}))
            assert save.ok
            load = host.dispatch("eng1", ToolCall("state.load", {}))
            assert load.ok and load.payload["state"] == {"remembered": 3}
        finally:
            ws.cleanup()
        # A fresh Host sharing the SAME persistent_id (the next episode)
        # sees the prior episode's content.
        host2, ws2 = _host(persistent_ids={"eng1": "test-pid-1"})
        try:
            load2 = host2.dispatch("eng1", ToolCall("state.load", {}))
            assert load2.payload["state"] == {"remembered": 3}
        finally:
            ws2.cleanup()
    finally:
        _cleanup_state_file("test-pid-1")


def test_persistent_id_lookup_never_appears_in_any_log_or_observation():
    """The agent must never see the string "test-pid-2" itself -- not in
    the tool-event log (state.save's `state` arg is content-elided
    anyway), not in the access log, not in the engine log."""
    try:
        cfg = LabConfig(
            agents=(
                AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0, persistent_id="test-pid-2"),
                AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=0.0),
                AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=0.0),
                AgentConfig("admin1", "admin", HONEST_WEIGHTS),
            ),
            T=60,
        )
        result = run_episode(cfg, seed=3, backend=MockIsolate())
        try:
            assert result.host.persistent_ids == {"eng1": "test-pid-2"}
            for name, log in (
                ("engine_log", result.engine.log),
                ("access_log", result.permissions.log),
                ("tool_events", result.host.events.entries),
            ):
                blob = json.dumps(log, default=str)
                assert "test-pid-2" not in blob, f"persistent_id leaked into {name}"
        finally:
            result.cleanup()
    finally:
        _cleanup_state_file("test-pid-2")


def test_state_frozen_handle_still_blocks_a_persistent_save():
    """The handle-freeze gate (handles.py) is checked BEFORE persistence,
    same precedent as the pre-0.8.0 no-op `state.save` docstring recorded."""
    from lab_sim.oracle_only.handles import HandleService

    try:
        oracle = OracleWorld(seed=1)
        ws = Workspace()
        permissions = PermissionService()
        engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws, permission_service=permissions)
        admin = AdminPolicy(AdminConfig(), permissions)
        handles = HandleService(engine=engine, permissions=permissions)
        handles.frozen_state_actors.add("eng1")
        host = Host(
            engine, permissions, admin, roles={"eng1": "engineer"},
            handle_service=handles, persistent_ids={"eng1": "test-pid-3"},
        )
        res = host.dispatch("eng1", ToolCall("state.save", {"state": {"k": "v"}}))
        assert not res.ok and res.reason == "state_frozen"
        assert load_persistent_state("test-pid-3") == {}
        ws.cleanup()
    finally:
        _cleanup_state_file("test-pid-3")
