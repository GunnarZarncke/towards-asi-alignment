"""V2-2b exogenous workload engine."""

from __future__ import annotations

import pytest

from graded_lab.world_visible.exogenous_workload import ExogenousWorkloadEngine
from graded_lab.world_visible.substrate import SubstrateError, load_substrate


def _periodic_event(**overrides: object) -> dict:
    base = {
        "id": "incident_wave",
        "roles_affected": ["reviewer", "release_manager"],
        "duration_ticks": 3,
        "resource_demand_scale": {"compute": 2.0, "io": 1.5},
        "trigger": {"kind": "periodic", "period_ticks": 5, "phase_offset_ticks": 0},
    }
    base.update(overrides)
    return base


def test_periodic_surge_applies_cost_scale_during_window():
    engine = ExogenousWorkloadEngine({"events": [_periodic_event()]}, seed=1)
    engine.tick(0)
    cs, ios = engine.cost_scale_for("reviewer")
    assert cs == 2.0
    assert ios == 1.5
    assert engine.cost_scale_for("engineer") == (1.0, 1.0)


def test_surge_expires_after_duration():
    engine = ExogenousWorkloadEngine({"events": [_periodic_event(duration_ticks=2)]}, seed=1)
    engine.tick(0)
    assert engine.cost_scale_for("reviewer")[0] == 2.0
    engine.tick(1)
    assert engine.cost_scale_for("reviewer")[0] == 2.0
    engine.tick(2)
    assert engine.cost_scale_for("reviewer") == (1.0, 1.0)


def test_load_substrate_validates_exogenous_workload_on_v2_json(tmp_path):
    round3 = "generated_ecology_v2_round3.json"
    try:
        substrate = load_substrate(round3)
    except FileNotFoundError:
        pytest.skip("round-3 candidate not present")
    data = dict(substrate.data)
    data["exogenous_workload"] = {"events": [_periodic_event()]}
    path = tmp_path / "ecology_with_workload.json"
    import json

    path.write_text(json.dumps(data), encoding="utf-8")
    loaded = load_substrate(path)
    assert "exogenous_workload" in loaded.data


def test_invalid_exogenous_workload_rejected(tmp_path):
    round3 = "generated_ecology_v2_round3.json"
    try:
        substrate = load_substrate(round3)
    except FileNotFoundError:
        pytest.skip("round-3 candidate not present")
    data = dict(substrate.data)
    data["exogenous_workload"] = {"events": [{"id": "bad", "trigger": {"kind": "periodic"}}]}
    path = tmp_path / "bad_workload.json"
    import json

    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(SubstrateError):
        load_substrate(path)
