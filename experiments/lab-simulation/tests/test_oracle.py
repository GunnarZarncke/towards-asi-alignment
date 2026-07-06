"""Oracle world: determinism, harm accrual, provenance lineage."""

from __future__ import annotations

import pytest

from lab_sim.oracle import OracleWorld


def test_model_truth_deterministic_given_seed():
    a = OracleWorld(seed=11)
    b = OracleWorld(seed=11)
    ma = a.create_model({"scale": 0.7, "safety_effort": 0.3})
    mb = b.create_model({"scale": 0.7, "safety_effort": 0.3})
    assert ma.true_capability == mb.true_capability
    assert ma.true_hazard == mb.true_hazard
    c = OracleWorld(seed=12)
    mc = c.create_model({"scale": 0.7, "safety_effort": 0.3})
    assert mc.true_capability != ma.true_capability


def test_eval_noise_deterministic_given_seed():
    a = OracleWorld(seed=11)
    b = OracleWorld(seed=11)
    ma = a.create_model({"scale": 0.5})
    mb = b.create_model({"scale": 0.5})
    assert a.run_eval(ma.model_id).measured_hazard == b.run_eval(mb.model_id).measured_hazard


def test_safety_effort_reduces_hazard_in_expectation():
    world = OracleWorld(seed=1)
    lo = [world.create_model({"scale": 0.8, "safety_effort": 0.1}).true_hazard for _ in range(20)]
    hi = [world.create_model({"scale": 0.8, "safety_effort": 0.9}).true_hazard for _ in range(20)]
    assert sum(lo) / len(lo) > sum(hi) / len(hi)


def test_harm_accrues_only_after_deploy():
    world = OracleWorld(seed=5)
    m = world.create_model({"scale": 0.9, "safety_effort": 0.0})
    for _ in range(10):
        world.tick()
    assert world.bearer_harm == 0.0
    world.deploy(m.model_id)
    for _ in range(10):
        world.tick()
    assert world.bearer_harm > 0.0


def test_lineage_recorded_and_unknown_parent_rejected():
    world = OracleWorld(seed=5)
    m1 = world.create_model({"scale": 0.5})
    m2 = world.create_model({"scale": 0.6}, parent_model_id=m1.model_id)
    assert m2.parent_model_id == m1.model_id
    with pytest.raises(KeyError):
        world.create_model({"scale": 0.5}, parent_model_id="m999")


def test_snapshot_round_trips_through_json():
    import json

    world = OracleWorld(seed=5)
    m = world.create_model({"scale": 0.5})
    world.run_eval(m.model_id)
    world.deploy(m.model_id)
    world.tick()
    snap = world.snapshot()
    assert json.loads(json.dumps(snap)) == json.loads(json.dumps(snap))
    assert snap["models"][m.model_id]["parent_model_id"] is None
