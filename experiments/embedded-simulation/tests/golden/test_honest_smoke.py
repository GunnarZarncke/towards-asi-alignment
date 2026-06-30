"""Smoke: one honest episode completes."""

from embedded_sim.pipeline import run_episode


def test_honest_episode_smoke():
    ep = run_episode("none", "honest", seed=7, T=400)
    assert ep.bridge == "none"
    assert ep.in_sim.cci_status in ("passes", "belowThreshold", "capturedInvalid")
    assert ep.outer.bridge_expected == "none"
