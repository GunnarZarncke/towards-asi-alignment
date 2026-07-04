"""Audit-side detectors and the discovery/held-out protocol."""

from goal_sim.channels import project_rows
from goal_sim.config import AgentConfig, GoalWeights, ToolAccess, WorldConfig
from goal_sim.detectors import run_detectors
from goal_sim.labels import label_episode
from goal_sim.protocol import (
    aggregate,
    in_held_out_region,
    mini_mi_scan,
    run_battery,
    sample_configs,
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
