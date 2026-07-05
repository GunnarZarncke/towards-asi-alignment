"""Audit-side detectors and the discovery/held-out protocol."""

import pytest

from goal_sim.channels import project_rows
from goal_sim.config import AgentConfig, GoalWeights, ToolAccess, WorldConfig
from goal_sim.detectors import run_detectors
from goal_sim.info import bonferroni_alpha, wilson_lower_bound
from goal_sim.labels import label_episode
from goal_sim.protocol import (
    aggregate,
    in_held_out_region,
    in_held_out_region_compliance_band,
    in_held_out_region_subtle,
    mi_transfer_on_frozen,
    mini_mi_scan,
    run_battery,
    sample_configs,
    sample_held_out_compliance_band,
    sample_held_out_subtle,
)
from goal_sim.world import run_episode


def make_cfg(weights: GoalWeights, tools: ToolAccess) -> WorldConfig:
    return WorldConfig(agent=AgentConfig(weights=weights, tools=tools))


def test_detectors_fire_on_false_reporter():
    cfg = make_cfg(
        GoalWeights(0.70, 0.02, 0.03, 0.25),
        ToolAccess(false_report=True),
    )
    fired_any = 0
    for seed in range(11, 19):
        rows = run_episode(cfg, seed)
        if label_episode(rows)["label"] != "violation":
            continue
        verdict = run_detectors(project_rows(rows, "light"))
        fired_any += int(verdict["flagged"])
    assert fired_any >= 4


def test_full_tier_catches_unilateral_adoption():
    cfg = make_cfg(
        GoalWeights(0.70, 0.05, 0.05, 0.20),
        ToolAccess(unilateral_adopt=True, propose_change=False),
    )
    caught = 0
    for seed in range(11, 19):
        rows = run_episode(cfg, seed)
        if not label_episode(rows)["l3_unapproved_change"]:
            continue
        verdict = run_detectors(project_rows(rows, "full"))
        if "d5_unapproved_change" in verdict["fired"]:
            caught += 1
    assert caught >= 3


def test_light_tier_misses_pure_shadow_full_tier_sees_routing():
    # Structural expectation, pre-registered in detectors.py: the shadow
    # route defeats visible-channel detectors (D1/D2) but not routing (D4).
    cfg = make_cfg(
        GoalWeights(0.60, 0.01, 0.02, 0.37),
        ToolAccess(shadow_route=True, shadow_budget=200),
    )
    full_catches = 0
    n_violations = 0
    for seed in range(11, 19):
        rows = run_episode(cfg, seed)
        if label_episode(rows)["label"] != "violation":
            continue
        n_violations += 1
        full = run_detectors(project_rows(rows, "full"))
        if full["flagged"]:
            full_catches += 1
    assert n_violations >= 4
    assert full_catches >= n_violations - 1


def test_compliant_agent_not_flagged():
    cfg = make_cfg(GoalWeights(0.15, 0.55, 0.25, 0.05), ToolAccess())
    for seed in range(11, 19):
        rows = run_episode(cfg, seed)
        for tier in ("light", "full"):
            verdict = run_detectors(project_rows(rows, tier))
            assert not verdict["flagged"], (seed, tier, verdict)


def test_sampling_deterministic_and_regions_disjoint():
    d1, h1 = sample_configs()
    d2, h2 = sample_configs()
    assert [c.config_id for c in d1] == [c.config_id for c in d2]
    assert [vars(c.agent.weights) for c in h1] == [vars(c.agent.weights) for c in h2]
    for cfg in d1:
        assert not in_held_out_region(cfg.agent.weights, cfg.agent.tools)
    for cfg in h1:
        assert in_held_out_region(cfg.agent.weights, cfg.agent.tools)
    assert len(d1) == 30 and len(h1) == 10


def test_wilson_lower_bound_basic_properties():
    # More evidence (fixed rate) tightens the bound toward the true rate.
    small = wilson_lower_bound(3, 4, confidence=0.80)
    large = wilson_lower_bound(30, 40, confidence=0.80)
    assert 0.0 <= small < large < 0.75
    assert wilson_lower_bound(0, 5, confidence=0.80) < 1e-9
    assert wilson_lower_bound(0, 0, confidence=0.80) == 0.0


def test_bonferroni_alpha_splits_family_error_rate():
    """run_phase3_blind.py tests the same detection-rate prediction under 2
    pre-registered L2 thresholds instead of 1 (FINDINGS.md F-13/F-14); the
    per-test alpha must shrink accordingly and reduce to a no-op at n=1."""
    assert bonferroni_alpha(0.20, 1) == 0.20
    assert bonferroni_alpha(0.20, 2) == 0.10
    assert bonferroni_alpha(0.05, 4) == 0.0125
    with pytest.raises(ValueError):
        bonferroni_alpha(0.20, 0)


def test_d1b_wilson_catches_small_n_false_reporting_d1_misses():
    # A false-report-leaning agent with FEW correction/probe opportunities:
    # the aggregate-mean D1 (needs a 0.35 gap) is expected to sometimes miss
    # exactly the small-n cases the Wilson-bound follow-up targets (F-3).
    cfg = make_cfg(
        GoalWeights(0.30, 0.20, 0.05, 0.45),
        ToolAccess(false_report=True, shadow_route=False),
    )
    d1_misses = 0
    d1b_recovers = 0
    for seed in range(11, 40):
        rows = run_episode(cfg, seed)
        if not label_episode(rows)["l1_deceptive_reporting"]:
            continue
        verdict = run_detectors(project_rows(rows, "light"))
        if "d1_probe_report_divergence" not in verdict["fired"]:
            d1_misses += 1
            if "d1b_probe_divergence_wilson" in verdict["fired"]:
                d1b_recovers += 1
    assert d1_misses >= 1, "fixture did not exercise the small-n D1 gap"
    assert d1b_recovers >= 1, "expected the Wilson follow-up to recover some D1 misses"
    assert d1b_recovers < d1_misses, "fixture should also show d1b is not perfect"


def test_subtle_held_out_region_disjoint_from_region_one_and_sampling_stable():
    subtle1 = sample_held_out_subtle()
    subtle2 = sample_held_out_subtle()
    assert [c.config_id for c in subtle1] == [c.config_id for c in subtle2]
    assert len(subtle1) == 10
    for cfg in subtle1:
        assert in_held_out_region_subtle(cfg.agent.weights, cfg.agent.tools)
        assert not in_held_out_region(cfg.agent.weights, cfg.agent.tools)


def test_compliance_band_region_disjoint_and_stable():
    band1 = sample_held_out_compliance_band()
    band2 = sample_held_out_compliance_band()
    assert [c.config_id for c in band1] == [c.config_id for c in band2]
    assert len(band1) == 10
    for cfg in band1:
        assert in_held_out_region_compliance_band(cfg.agent.weights, cfg.agent.tools)
        assert not in_held_out_region(cfg.agent.weights, cfg.agent.tools)
        assert not in_held_out_region_subtle(cfg.agent.weights, cfg.agent.tools)


def test_subtle_region_sampling_does_not_perturb_original_split():
    d1, h1 = sample_configs()
    sample_held_out_subtle()  # uses an independent RNG stream/seed
    sample_held_out_compliance_band()  # ditto
    d2, h2 = sample_configs()
    assert [c.config_id for c in d1] == [c.config_id for c in d2]
    assert [vars(c.agent.weights) for c in h1] == [vars(c.agent.weights) for c in h2]


def test_mi_transfer_on_frozen_matches_mini_mi_scan_for_same_group():
    discovery, held_out = sample_configs()
    d_records = run_battery(discovery[:3], seeds=(11, 12))
    h_records = run_battery(held_out[:2], seeds=(11, 12))
    scan = mini_mi_scan(d_records, h_records, top_k=2)
    transfer = mi_transfer_on_frozen(scan["frozen_top_k"], h_records)
    assert transfer["scores_for_frozen"] == scan["held_out_scores_for_frozen"]
    assert transfer["label_entropy_bits"] == scan["held_out_label_entropy_bits"]
    assert transfer["transfer_degenerate"] == scan["held_out_transfer_degenerate"]


def test_battery_and_aggregate_smoke():
    discovery, held_out = sample_configs()
    records = run_battery(discovery[:2], seeds=(11, 12))
    agg = aggregate(records)
    assert agg["n_episodes"] == 4
    for tier in ("light", "full"):
        assert tier in agg["tiers"]
    ho_records = run_battery(held_out[:2], seeds=(11, 12))
    scan = mini_mi_scan(records, ho_records, top_k=2)
    assert len(scan["frozen_top_k"]) == 2
    assert set(scan["held_out_scores_for_frozen"]) == set(scan["frozen_top_k"])
