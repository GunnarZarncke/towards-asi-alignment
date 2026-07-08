"""D3.2 spec evolution + selection (PLAN.md MB6b)."""

from __future__ import annotations

import random

from lab_sim.harness.d3_spec_evolution import (
    apply_generation_spec_mutations,
    apply_spec_weakening,
    make_d3_2_member_config,
    next_weakened_spec,
    run_spec_evolution_loop,
    sample_d3_2_initial_population,
    spec_weakening_steps,
)
from lab_sim.harness.isolate import MockIsolate
from lab_sim.world_visible.config import GoalWeights


def test_all_d3_2_starts_on_default_strict_spec():
    configs = sample_d3_2_initial_population(population_size=4, seed=1)
    assert all(c.pipeline_spec == "pipeline_default.json" for c in configs)
    assert all(c.multi_gen_enabled for c in configs)
    assert all(c.spec_upgrade_target == "pipeline_shortcut.json" for c in configs)
    assert all(c.board.capture_start is None for c in configs)


def test_spec_weakening_chain_one_step():
    assert next_weakened_spec("pipeline_default.json") == "pipeline_shortcut.json"
    assert next_weakened_spec("pipeline_shortcut.json") is None


def test_apply_spec_weakening_clears_upgrade_target():
    cfg = make_d3_2_member_config(
        "x",
        eng_w=GoalWeights(1, 1, 1, 1),
        rev_w=GoalWeights(1, 1, 1, 1),
        rm_w=GoalWeights(1, 1, 1, 1),
    )
    weakened = apply_spec_weakening(cfg, "pipeline_shortcut.json")
    assert weakened.pipeline_spec == "pipeline_shortcut.json"
    assert weakened.spec_upgrade_target is None
    assert spec_weakening_steps(weakened) == 1


def test_mutations_only_for_above_median_throughput():
    configs = sample_d3_2_initial_population(population_size=3, seed=2)
    throughputs = [0.0, 5.0, 10.0]
    rng = random.Random(0)
    new_configs, events = apply_generation_spec_mutations(
        configs, throughputs, rng=rng, mutation_prob=1.0
    )
    assert events == 2  # median is 5.0; members with 5.0 and 10.0 qualify
    assert new_configs[0].pipeline_spec == "pipeline_default.json"
    assert new_configs[1].pipeline_spec == "pipeline_shortcut.json"
    assert new_configs[2].pipeline_spec == "pipeline_shortcut.json"


def test_run_spec_evolution_loop_smoke():
    configs = sample_d3_2_initial_population(population_size=4, seed=3)
    traj = run_spec_evolution_loop(
        configs, n_generations=3, n_episodes_per_member=1, backend_factory=MockIsolate
    )
    assert len(traj.generations) == 3
    assert traj.generations[0].correction_preserving_mass_share == 1.0
    assert traj.generations[-1].shortcut_spec_mass_share >= traj.generations[0].shortcut_spec_mass_share
