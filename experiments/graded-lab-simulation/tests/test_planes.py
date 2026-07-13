"""Plane separation stubs — oracle truth must not appear in engine log."""

from __future__ import annotations

import json

from graded_lab.oracle_only.oracle import OracleWorld
from graded_lab.world_visible.config import ORACLE_ONLY_FIELDS
from graded_lab.world_visible.pipeline_engine import PipelineEngine
from graded_lab.world_visible.pipeline_spec import load_spec
from graded_lab.world_visible.substrate import load_substrate
from graded_lab.world_visible.workspace import Workspace
from graded_lab.harness.isolate import MockIsolate
from graded_lab.world_visible.world import default_lab_config, run_episode


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
    substrate = load_substrate()
    oracle = OracleWorld(seed=11, substrate_data=substrate.data)
    ws = Workspace()
    try:
        engine = PipelineEngine(load_spec("pipeline_graded.json"), oracle, ws)
        engine.trigger_step("eng1", "intake", {})
        build = engine.trigger_step(
            "eng1", "build", {"params": {"scale": 0.7, "safety_effort": 0.6}}
        )
        mid = str(build.payload["model_id"])
        engine.trigger_step("eng1", "eval", {"model_id": mid})
        leaked = _keys_recursive(engine.log) & set(ORACLE_ONLY_FIELDS)
        assert not leaked, f"oracle-only fields leaked: {leaked}"
        blob = json.dumps(engine.log)
        for fld in ("latent_hazard", "hazard_regions", "true_capability", "bearer_harm"):
            assert fld not in blob
    finally:
        ws.cleanup()


def test_eval_payload_is_sampled_not_tier_k_mean():
    substrate = load_substrate()
    oracle = OracleWorld(seed=11, substrate_data=substrate.data)
    ws = Workspace()
    try:
        engine = PipelineEngine(load_spec("pipeline_graded.json"), oracle, ws)
        engine.trigger_step("eng1", "intake", {})
        build = engine.trigger_step("eng1", "build", {"params": {"scale": 0.8}})
        mid = str(build.payload["model_id"])
        ev = engine.trigger_step("eng1", "eval", {"model_id": mid, "draws": 12})
        model = oracle.models[mid]
        assert "measured_hazard_mean" in ev.payload
        # Sample mean can coincide by luck but structure differs from Tier-K export.
        assert "hazard_regions" not in ev.payload
        assert model.latent_hazard_mean >= 0.0
    finally:
        ws.cleanup()


def test_isolate_boundary_observations_contain_no_oracle_fields():
    result = run_episode(default_lab_config(), seed=11, backend=MockIsolate())
    observed_keys = _keys_recursive(result.boundary_streams)
    leaked = observed_keys & set(ORACLE_ONLY_FIELDS)
    assert not leaked, f"oracle-only fields leaked into isolate observations: {leaked}"


def test_primitive_log_projection_excludes_oracle_attachment():
    result = run_episode(default_lab_config(), seed=11, backend=MockIsolate())
    blob = json.dumps(result.primitive_log)
    for fld in ("latent_hazard", "hazard_regions", "true_capability", "bearer_harm"):
        assert fld not in blob
