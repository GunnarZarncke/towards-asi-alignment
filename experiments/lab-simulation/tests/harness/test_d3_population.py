"""D3.1 population-over-configurations (PLAN.md MB6a cheapest tier)."""

from __future__ import annotations

import pytest

from lab_sim.harness.d3_population import (
    correction_integrity_score,
    episode_throughput,
    is_correction_preserving,
    make_member_config,
    sample_initial_population,
    update_deployment_mass,
)
from lab_sim.harness.isolate import MockIsolate
from lab_sim.world_visible.config import GoalWeights
from lab_sim.world_visible.world import run_episode


def test_is_correction_preserving_only_on_full_strict_structural_cell():
    strict = make_member_config(
        "strict",
        pipeline_spec="pipeline_default.json",
        board_capture_start=None,
        admin_least_privilege=True,
        admin_capture_start=None,
        eng_w=GoalWeights(1, 1, 1, 1),
        rev_w=GoalWeights(1, 1, 1, 1),
        rm_w=GoalWeights(1, 1, 1, 1),
    )
    shortcut = make_member_config(
        "shortcut",
        pipeline_spec="pipeline_shortcut.json",
        board_capture_start=None,
        admin_least_privilege=True,
        admin_capture_start=None,
        eng_w=GoalWeights(1, 1, 1, 1),
        rev_w=GoalWeights(1, 1, 1, 1),
        rm_w=GoalWeights(1, 1, 1, 1),
    )
    assert is_correction_preserving(strict)
    assert not is_correction_preserving(shortcut)
    assert correction_integrity_score(strict) == 1.0
    assert correction_integrity_score(shortcut) == pytest.approx(0.6)


def test_update_deployment_mass_favors_higher_throughput():
    masses = [0.25, 0.25, 0.25, 0.25]
    throughputs = [0.0, 1.0, 2.0, 0.5]
    new = update_deployment_mass(masses, throughputs, selection_strength=1.0, mass_floor=0.01)
    assert abs(sum(new) - 1.0) < 1e-9
    assert new[2] > new[0]
    assert new[2] > new[3]


def test_sample_initial_population_covers_structural_axes():
    configs = sample_initial_population(seed=1, population_size=8)
    assert len(configs) == 8
    pipelines = {c.pipeline_spec for c in configs}
    assert "pipeline_default.json" in pipelines
    assert "pipeline_shortcut.json" in pipelines


def test_episode_throughput_is_nonnegative_and_reflects_deploy_log():
    from lab_sim.harness.ecology import HONEST_WEIGHTS

    cfg = make_member_config(
        "deploy",
        pipeline_spec="pipeline_default.json",
        board_capture_start=None,
        admin_least_privilege=True,
        admin_capture_start=None,
        eng_w=HONEST_WEIGHTS,
        rev_w=HONEST_WEIGHTS,
        rm_w=HONEST_WEIGHTS,
        T=120,
        temperature=0.0,
    )
    result = run_episode(cfg, seed=3, backend=MockIsolate())
    try:
        t = episode_throughput(result)
        assert t >= 0.0
        deploys = sum(
            1 for e in result.engine.log if e.get("step_id") == "deploy" and e.get("status") == "ok"
        )
        assert t == float(deploys)
    finally:
        result.cleanup()


def test_run_population_loop_smoke():
    from lab_sim.harness.d3_population import run_population_loop

    configs = sample_initial_population(seed=99, population_size=4)
    traj = run_population_loop(configs, n_generations=2, n_episodes_per_member=1, backend_factory=MockIsolate)
    assert len(traj.generations) == 2
    for snap in traj.generations:
        assert 0.99 <= snap.correction_preserving_mass_share <= 1.01 or snap.correction_preserving_mass_share >= 0
        assert len(snap.members) == 4
        assert abs(sum(m.deployment_mass_after for m in snap.members) - 1.0) < 1e-6
