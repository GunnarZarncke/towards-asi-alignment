"""Phase 0.5 honest scenarios — structural sanity and oracle smoke tests."""

from __future__ import annotations

import pytest

from embedded_sim.audit_core.cci_audit import audit_cci
from embedded_sim.audit_core.observation import build_audit_trace_from_rows
from embedded_sim.audit_core.simulator import scenario_config, simulate
from embedded_sim.audit_core.structural_signals import (
    ground_handle_divergence,
    lineage_stall_reported_uptake,
)
from embedded_sim.batch import _run_scenario_episode
from embedded_sim.lab import build_world, load_episode_rows_from_vfs

PHASE_0_5_SCENARIOS = (
    "honest_mistakes",
    "legitimate_gradual_improvement",
    "benign_semantic_drift",
)


def _audit_and_cert(scenario: str, seed: int, instrumentation: str = "strong_handles"):
    world, _ledger, episode_meta = build_world("none", scenario, seed, T=400)  # type: ignore[arg-type]
    rows = load_episode_rows_from_vfs(world)
    audit, _lineage = build_audit_trace_from_rows(
        rows, scenario, seed, instrumentation=instrumentation  # type: ignore[arg-type]
    )
    cert = audit_cci(audit)
    return audit, cert, episode_meta


@pytest.mark.parametrize("scenario", PHASE_0_5_SCENARIOS)
def test_phase_0_5_scenario_runs_through_certification_pipeline(scenario):
    run = _run_scenario_episode(
        scenario, 13, T=400, instrumentation="medium_handles", redteam_strategy="none", substrate="python"
    )
    assert run.get("in_sim", {}).get("cci_status") in ("passes", "belowThreshold", "capturedInvalid")


def test_honest_mistakes_uses_bursty_dips_not_theater():
    cfg = scenario_config("honest_mistakes")
    assert cfg.mistake_burst_prob > 0
    assert cfg.judge_capture is False
    assert cfg.legitimacy_theater is False
    _micro, _ledger, rows = simulate("honest_mistakes", seed=42, T=400)
    misses = [r for r in rows if r["correction_request"] and not r["true_uptake"]]
    assert len(misses) >= 5
    for r in misses[:20]:
        assert r["reported_acceptance"] == int(r["true_uptake"])


def test_legitimate_gradual_improvement_ramps_responsiveness():
    cfg = scenario_config("legitimate_gradual_improvement")
    assert cfg.responsiveness_ramp_start is not None
    assert cfg.responsiveness_ramp_start < cfg.responsiveness
    _micro, _ledger, rows = simulate("legitimate_gradual_improvement", seed=7, T=400)
    early_eff = sum(float(r["effective_responsiveness"]) for r in rows[:80]) / 80
    late_eff = sum(float(r["effective_responsiveness"]) for r in rows[-80:]) / 80
    assert late_eff > early_eff
    assert rows[0]["effective_responsiveness"] == pytest.approx(cfg.responsiveness_ramp_start, abs=0.02)
    assert rows[-1]["effective_responsiveness"] == pytest.approx(cfg.responsiveness, abs=0.02)


def test_benign_semantic_drift_is_visible_and_harmless():
    cfg = scenario_config("benign_semantic_drift")
    assert cfg.silent_ground_drift
    assert cfg.display_bearer_inertia < 0.5
    _micro, _ledger, rows = simulate("benign_semantic_drift", seed=11, T=400)
    ground = [float(r["true_ground_valence"]) for r in rows]
    display = [float(r["display_bearer"]) for r in rows]
    assert max(ground) - min(ground) > 0.10
    assert max(display) - min(display) > 0.10
    assert sum(int(r.get("silent_harm", 0)) for r in rows) == 0
    assert ground[-1] > 0.42


@pytest.mark.parametrize("scenario", PHASE_0_5_SCENARIOS)
def test_capture_specific_detectors_do_not_fire_on_phase_0_5_honest(scenario):
    audit, cert, _meta = _audit_and_cert(scenario, seed=13)
    assert lineage_stall_reported_uptake(audit, cert) is False
    assert ground_handle_divergence(audit, cert) is False


def test_phase_0_5_honest_pass_rate_floor_at_medium_handles():
    """Regression floor once measured — honest scenarios should mostly pass."""
    passes = 0
    for scenario in PHASE_0_5_SCENARIOS:
        for seed in range(11, 19):
            run = _run_scenario_episode(
                scenario,
                seed,
                T=400,
                instrumentation="medium_handles",
                redteam_strategy="none",
                substrate="python",
            )
            if run.get("in_sim", {}).get("cci_status") == "passes":
                passes += 1
    # 3 scenarios x 8 seeds = 24; allow some false negatives near the boundary.
    assert passes >= 12
