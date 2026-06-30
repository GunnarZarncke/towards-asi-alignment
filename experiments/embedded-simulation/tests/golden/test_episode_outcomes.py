"""Golden end-to-end episode outcomes (tiny T, fixed seeds)."""

import pytest

from embedded_sim.pipeline import run_episode


@pytest.mark.parametrize(
    "bridge,scenario",
    [
        ("none", "honest"),
        ("MB6", "selection_basin"),
        ("MB5", "successor_relabel"),
    ],
)
def test_episode_structural_outcomes(bridge, scenario):
    ep = run_episode(bridge, scenario, seed=42, T=300, substrate="python")
    assert ep.in_sim.unit is not None
    assert len(ep.in_sim.handles) >= 4
    assert ep.in_sim.read_anchors


def test_mb6_uad_coalition_or_high_score_unit():
    ep = run_episode("MB6", "selection_basin", seed=42, T=400, substrate="python")
    unit = ep.in_sim.unit
    assert unit is not None
    assert unit.score > 0
    ids = {u.candidate_id for u in [unit]}
    if unit.unit_type == "coalition":
        assert "coalition" in unit.candidate_id
    else:
        assert unit.member_ids


def test_mb5_referent_transport_failure():
    ep = run_episode("MB5", "successor_relabel", seed=42, T=400, substrate="python")
    assert ep.outer.referent_drift is not None
    assert ep.outer.referent_drift.transport_failure
