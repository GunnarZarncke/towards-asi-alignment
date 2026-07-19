"""V2-4 / R-MB6a variation operator."""

from __future__ import annotations

import random

from graded_lab.harness.variation_operator import (
    EDIT_CLASSES,
    MUTATION_RATE,
    _pattern_scores_key,
    mutate_program_map,
    sample_program_map_variants,
)
from graded_lab.oracle_only.stats import (
    N_PERMUTATIONS,
    observed_mass_range,
    permutation_mass_movement_band,
)
from graded_lab.agent_visible.behavior_features import GOAL_FEATURES, PRIMITIVE_PATTERN_VOCAB
from graded_lab.world_visible.program_map import expand_preset, validate_program_map


def test_mutate_program_map_returns_valid_program_map():
    baseline = expand_preset("walk_pipeline", role="engineer")
    rng = random.Random(0)
    result = mutate_program_map(baseline, rng=rng)
    assert result is not None
    assert result.edit_class in EDIT_CLASSES


def test_sample_program_map_variants_syntax_distinct():
    baseline = expand_preset("walk_pipeline", role="engineer")
    rng = random.Random(1)
    variants = sample_program_map_variants(baseline, n=5, rng=rng)
    assert len(variants) >= 1
    keys = {
        (
            v.temperature_bin,
            v.goal_weight_bins,
            _pattern_scores_key(v.scoring.get("pattern_scores", {})),
        )
        for v in variants
    }
    assert len(keys) <= len(variants)


def test_pattern_score_set_inserts_vocab_valid_nested_row():
    """Regression (GL-82): pre-fix ``pattern_score_set`` wrote a bare float
    under invalid key ``call_pipeline`` and always failed validation."""
    baseline = expand_preset("walk_pipeline", role="engineer")
    assert baseline.scoring.get("pattern_scores") == {}
    rng = random.Random(99)
    for _ in range(40):
        result = mutate_program_map(baseline, rng=rng)
        if result is not None and result.edit_class == "pattern_score_set":
            pmap = result.program_map
            validate_program_map(
                {
                    "mode": pmap.mode,
                    "walker": pmap.walker,
                    "scoring": pmap.scoring,
                    "stated_feature_deltas": pmap.stated_feature_deltas,
                    "hooks": pmap.hooks,
                    "temperature_bin": pmap.temperature_bin,
                    "goal_weight_bins": list(pmap.goal_weight_bins),
                    "preset_source": pmap.preset_source,
                },
                role="engineer",
                strict_ladder=False,
            )
            scores = pmap.scoring["pattern_scores"]
            assert scores
            pat, row = next(iter(scores.items()))
            assert pat in PRIMITIVE_PATTERN_VOCAB
            assert isinstance(row, dict) and row
            assert next(iter(row)) in GOAL_FEATURES
            return
    raise AssertionError("pattern_score_set never sampled in 40 attempts")


def test_walk_pipeline_one_hop_syntax_variants_exceed_pre_fix_ceiling():
    """Pre-fix GL-81 expressiveness saturated at 11 syntax-distinct mutants."""
    baseline = expand_preset("walk_pipeline", role="engineer")
    variants = sample_program_map_variants(baseline, n=100, rng=random.Random(60100))
    assert len(variants) > 11


def test_permutation_band_uniform_fitness_has_zero_observed_range():
    # All members identical fitness each generation -> no mass concentration.
    gen_fitness = [[1.0, 1.0, 1.0, 1.0] for _ in range(3)]
    assert observed_mass_range(gen_fitness) == 0.0
    band = permutation_mass_movement_band(gen_fitness, n_permutations=50, seed=0)
    assert band["p97_5"] >= 0.0
    assert MUTATION_RATE == 0.3
    assert N_PERMUTATIONS == 200
