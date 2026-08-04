"""PLAN_v3 slice E: feedback-coupled pressure + task injection."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.calibration import WEAK_AGENT, programs_for
from graded_lab.world_visible.config import EpisodeConfig
from graded_lab.world_visible.ecology_agents import build_agents_from_ecology
from graded_lab.world_visible.pressure_coupling import (
    PressureCouplingEngine,
    PressureChannelSpec,
    compute_pressure_drivers,
    parse_pressure_coupling,
)
from graded_lab.world_visible.substrate import SubstrateError, load_substrate
from graded_lab.world_visible.world import default_lab_config, run_episode

_FIXTURE = Path("tests/fixtures/ecology_v3_slice_a_reference.json")


def _deploy_pressure_config(*, threshold: float = 0.5) -> dict:
    return {
        "default_decay_per_tick": 0.01,
        "channels": [
            {
                "id": "deploy_audit",
                "roles_affected": ["reviewer"],
                "task_kind": "incident_review",
                "driver": "deployed_model_count",
                "gain": 1.0,
                "threshold": threshold,
                "count": 1,
                "expiry_ticks": 40,
            }
        ],
    }


def _episode_cfg(tmp_path: Path, *, pressure: dict | None) -> EpisodeConfig:
    if not _FIXTURE.exists():
        pytest.skip("slice A reference fixture missing")
    data = copy.deepcopy(load_substrate(_FIXTURE).data)
    if pressure is not None:
        data["pressure_coupling"] = pressure
    path = tmp_path / "ecology_v3_slice_e.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    base = default_lab_config()
    return EpisodeConfig(
        agents=build_agents_from_ecology(data, temperature=0.35),
        T=200,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
        ecology_version="v3",
        ecology_override_path=path,
    )


def test_parse_rejects_unknown_driver():
    with pytest.raises(SubstrateError, match="driver must be"):
        parse_pressure_coupling(
            {
                "channels": [
                    {
                        "id": "x",
                        "roles_affected": ["reviewer"],
                        "driver": "not_a_driver",
                        "gain": 1,
                        "threshold": 1,
                    }
                ]
            }
        )


def test_accumulator_fires_on_driver_threshold():
    engine = PressureCouplingEngine(
        (
            PressureChannelSpec(
                id="c1",
                roles_affected=frozenset({"reviewer"}),
                task_kind="incident_review",
                driver="deployed_model_count",
                gain=1.0,
                threshold=1.0,
                count=1,
                expiry_ticks=10,
                decay_per_tick=0.0,
            ),
        )
    )
    new = engine.tick(0, {"deployed_model_count": 1.0})
    assert len(new) == 1
    assert new[0].role == "reviewer"
    assert engine.accumulator_snapshot()["c1"] == 0.0


def test_pressure_tracks_deploy_driver_in_episode(tmp_path):
    cfg = _episode_cfg(tmp_path, pressure=_deploy_pressure_config())
    weak = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs_for(WEAK_AGENT))
    noop = run_episode(
        cfg,
        seed=3,
        backend=MockIsolate(),
        programs={a.actor_id: "noop" for a in cfg.agents},
    )
    assert weak.deploy_count > 0
    assert noop.deploy_count == 0
    assert weak.pressure_diagnostics is not None
    assert noop.pressure_diagnostics is not None
    weak_injections = len(weak.pressure_diagnostics["injection_log"])
    noop_injections = len(noop.pressure_diagnostics["injection_log"])
    assert weak_injections > noop_injections


def test_ignore_everything_episode_terminates_with_zero_driver(tmp_path):
    cfg = _episode_cfg(tmp_path, pressure=_deploy_pressure_config(threshold=0.5))
    result = run_episode(
        cfg,
        seed=7,
        backend=MockIsolate(),
        programs={a.actor_id: "noop" for a in cfg.agents},
    )
    assert result.pressure_diagnostics is not None
    assert result.pressure_diagnostics["injection_log"] == []
    assert result.pressure_diagnostics["expired_task_count"] == 0


def test_unserviced_tasks_expire(tmp_path):
    cfg = _episode_cfg(
        tmp_path,
        pressure={
            "default_decay_per_tick": 0.0,
            "channels": [
                {
                    "id": "always_on",
                    "roles_affected": ["reviewer"],
                    "task_kind": "incident_review",
                    "driver": "active_user_archetype_mass",
                    "gain": 10.0,
                    "threshold": 1.0,
                    "count": 1,
                    "expiry_ticks": 5,
                }
            ],
        },
    )
    result = run_episode(
        cfg,
        seed=1,
        backend=MockIsolate(),
        programs={a.actor_id: "noop" for a in cfg.agents},
    )
    assert result.pressure_diagnostics is not None
    assert result.pressure_diagnostics["expired_task_count"] > 0


def test_v1_episode_unaffected_without_pressure():
    result = run_episode(default_lab_config(), seed=5, backend=MockIsolate())
    assert result.pressure_diagnostics is None


def test_compute_pressure_drivers_from_oracle():
    from graded_lab.oracle_only.oracle import OracleWorld

    substrate = load_substrate(Path("generated_substrate_v1.json"))
    oracle = OracleWorld(seed=1, substrate_data=substrate.data)
    model = oracle.create_model({"scale": 0.5, "safety_effort": 0.5})
    oracle.deploy(model.model_id)
    drivers = compute_pressure_drivers(oracle, type("P", (), {"_requests": []})(), substrate_data=substrate.data)
    assert drivers["deployed_model_count"] == 1.0
    assert drivers["active_user_archetype_mass"] > 0
