"""Plane separation: oracle-only truth never leaks into the audit plane.

Phase 0/1 scope covered the engine log only. Phase 5 adds the full-episode
check: across a real goal-driven run (engine log, access log, tool-call
event log), no ``ORACLE_ONLY_FIELDS`` entry — including ``goal_weights``,
which every agent legitimately knows about itself — may appear in any of
the three audit-plane logs.
"""

from __future__ import annotations

import json

from lab_sim.config import (
    ORACLE_ONLY_FIELDS,
    AdminConfig,
    AgentConfig,
    BoardConfig,
    GoalWeights,
    LabConfig,
    TierConfig,
)
from lab_sim.isolate import MockIsolate
from lab_sim.oracle import OracleWorld
from lab_sim.pipeline_engine import PipelineEngine
from lab_sim.pipeline_spec import load_spec
from lab_sim.workspace import Workspace
from lab_sim.world import run_episode


def _keys_recursive(obj: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.add(str(k))
            keys |= _keys_recursive(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            keys |= _keys_recursive(v)
    return keys


def test_engine_log_contains_no_oracle_only_fields():
    oracle = OracleWorld(seed=7)
    ws = Workspace()
    try:
        engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws)
        res = engine.trigger_step("a1", "submit_build", {"params": {"scale": 0.8}})
        mid = str(res.payload["model_id"])
        engine.trigger_step("a1", "run_eval", {"model_id": mid})
        engine.trigger_step("a1", "deploy", {"model_id": mid})  # denied
        leaked = _keys_recursive(engine.log) & set(ORACLE_ONLY_FIELDS)
        assert not leaked, f"oracle-only fields leaked into engine log: {leaked}"
        # Belt and suspenders: not even as substrings of the serialized log.
        blob = json.dumps(engine.log)
        for fld in ("true_capability", "true_hazard", "bearer_harm"):
            assert fld not in blob
    finally:
        ws.cleanup()


def test_eval_payload_is_measured_not_true():
    oracle = OracleWorld(seed=7)
    ws = Workspace()
    try:
        engine = PipelineEngine(load_spec("pipeline_default.json"), oracle, ws)
        res = engine.trigger_step("a1", "submit_build", {"params": {"scale": 0.8}})
        mid = str(res.payload["model_id"])
        ev = engine.trigger_step("a1", "run_eval", {"model_id": mid})
        model = oracle.models[mid]
        # Measured values exist and are not (except by measure-zero luck)
        # equal to oracle truth.
        assert "measured_capability" in ev.payload
        assert ev.payload["measured_capability"] != model.true_capability
    finally:
        ws.cleanup()


def test_units_ground_truth_is_config_side_and_defaults_to_singletons():
    agents = (
        AgentConfig("eng1", "engineer", GoalWeights(1, 1, 1, 1)),
        AgentConfig("rev1", "reviewer", GoalWeights(1, 1, 1, 1)),
    )
    cfg = LabConfig(agents=agents)
    assert cfg.resolved_units() == {"eng1": ("eng1",), "rev1": ("rev1",)}

    cfg2 = LabConfig(agents=agents, units=(("committee", ("eng1", "rev1")),))
    assert cfg2.resolved_units() == {"committee": ("eng1", "rev1")}


def test_units_reject_unknown_actor_ids():
    agents = (AgentConfig("eng1", "engineer", GoalWeights(1, 1, 1, 1)),)
    try:
        LabConfig(agents=agents, units=(("u", ("ghost",)),))
        raise AssertionError("expected ValueError for unknown actor_id in units")
    except ValueError:
        pass


def test_full_episode_leaks_no_oracle_only_fields_into_any_audit_log():
    cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", GoalWeights(1, 0, 0, 1), temperature=0.0),
            AgentConfig("rev1", "reviewer", GoalWeights(1, 0, 0, 0), temperature=0.0),
            AgentConfig("rm1", "release_manager", GoalWeights(1, 1, 1, 1), temperature=0.0),
            AgentConfig("admin1", "admin", GoalWeights(1, 1, 1, 1)),
        ),
        board=BoardConfig(capture_start=5),
        admin=AdminConfig(least_privilege=False),
        T=60,
    )
    result = run_episode(cfg, seed=3, backend=MockIsolate())
    try:
        surfaces = {
            "engine_log": result.engine.log,
            "access_log": result.permissions.log,
            "tool_events": result.host.events.entries,
        }
        for name, log in surfaces.items():
            leaked = _keys_recursive(log) & set(ORACLE_ONLY_FIELDS)
            assert not leaked, f"oracle-only fields leaked into {name}: {leaked}"
            blob = json.dumps(log)
            for fld in ("true_capability", "true_hazard", "bearer_harm", "board_captured", "admin_captured"):
                assert fld not in blob, f"{fld!r} leaked into {name}"
    finally:
        result.cleanup()


def test_config_validation():
    assert GoalWeights(2, 2, 2, 2).normalized() == GoalWeights(0.25, 0.25, 0.25, 0.25)
    assert GoalWeights(0, 0, 0, 0).normalized() == GoalWeights(0.25, 0.25, 0.25, 0.25)
    try:
        AgentConfig("x", "wizard", GoalWeights(1, 1, 1, 1))
        raise AssertionError("expected ValueError for unknown role")
    except ValueError:
        pass
    try:
        TierConfig(tier="ultra")
        raise AssertionError("expected ValueError for unknown tier")
    except ValueError:
        pass
    try:
        LabConfig(agents=(
            AgentConfig("a", "engineer", GoalWeights(1, 1, 1, 1)),
            AgentConfig("a", "reviewer", GoalWeights(1, 1, 1, 1)),
        ))
        raise AssertionError("expected ValueError for duplicate actor_id")
    except ValueError:
        pass
