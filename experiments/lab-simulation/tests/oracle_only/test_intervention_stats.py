"""Noise-tolerant S6 (PLAN.md open design question (b); FINDINGS.md
G-32/G-33): statistically-calibrated compensation test.

Equivalence tests below are the load-bearing ones: on a scripted
(`MockIsolate`) backend -- byte-identical replicate replays, zero-width
null -- this module must reproduce `uad_intervention.
discovered_units_intervention`'s FROZEN, battery-validated partition
results exactly. That is the check that the statistical rebasing
generalizes correctly instead of silently changing scripted-agent
behavior.
"""

from __future__ import annotations

import pytest

from lab_sim.harness.ecology import (
    covert_file_handoff_config,
    dm_pair_config,
    serial_pipeline_no_unit_config,
    shared_slot_config,
)
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.intervention_probes import channel_ablation_probe
from lab_sim.oracle_only.intervention_stats import (
    calibrate_clean_null,
    code_histogram,
    discovered_units_intervention_stats,
    outcome_divergence,
    probe_compensation_stats,
    total_variation_distance,
)
from lab_sim.oracle_only.uad_partition import exact_partition, nonsingleton_clusters
from lab_sim.world_visible.world import run_episode


def test_code_histogram_normalizes_to_frequencies():
    hist = code_histogram([1, 1, 2, 0, 0], from_tick=0)
    assert hist == {1: 0.4, 2: 0.2, 0: 0.4}


def test_code_histogram_respects_from_tick_window():
    hist = code_histogram([9, 9, 1, 1, 2], from_tick=2)
    assert hist == {1: 2 / 3, 2: 1 / 3}


def test_total_variation_distance_bounds_and_identity():
    assert total_variation_distance({1: 1.0}, {1: 1.0}) == 0.0
    assert total_variation_distance({1: 1.0}, {2: 1.0}) == 1.0
    assert 0.0 <= total_variation_distance({1: 0.5, 2: 0.5}, {1: 0.3, 3: 0.7}) <= 1.0


def test_outcome_divergence_zero_for_identical_series():
    series = [1, 2, 3, 1, 1, 0, 0]
    assert outcome_divergence(series, series, from_tick=0) == 0.0


def test_calibrate_clean_null_rejects_too_few_replicates():
    cfg = dm_pair_config(T=30)
    with pytest.raises(ValueError):
        calibrate_clean_null(cfg, 1, ["eng1", "rm1"], backend=MockIsolate(), k_replicates=1)


def test_calibrate_clean_null_is_zero_width_on_scripted_backend():
    """MockIsolate + same seed = byte-identical replays -- the null must
    collapse to all-zero samples, recovering S6's implicit "any nonzero
    divergence is signal" assumption for the regime it was built for."""
    cfg = dm_pair_config(T=30)
    null = calibrate_clean_null(cfg, 1, ["eng1", "rm1"], backend=MockIsolate(), k_replicates=3)
    for actor in ("eng1", "rm1"):
        samples = null.samples_at(actor, from_tick=0)
        assert samples == [0.0, 0.0, 0.0]
        assert null.threshold_at(actor, from_tick=0, q=0.90) == 0.0


def test_probe_compensation_stats_flags_dm_pair_on_scripted_backend():
    cfg = dm_pair_config(T=100)
    backend = MockIsolate()
    null = calibrate_clean_null(cfg, 1, ["eng1", "rm1"], backend=backend, k_replicates=2)
    probe = channel_ablation_probe("dm", "eng1")
    results = probe_compensation_stats(cfg, 1, probe, ["eng1", "rm1"], null, backend=backend)
    assert results["eng1"].compensates or results["rm1"].compensates


def _run_stats(factory, seed: int = 1, **kwargs):
    if factory is covert_file_handoff_config:
        cfg = factory(trusting=True, T=100)
    else:
        cfg = factory(T=100)
    backend = MockIsolate()
    result = run_episode(cfg, seed=seed, backend=backend)
    try:
        discovered = discovered_units_intervention_stats(
            result, cfg, seed, backend=backend, k_clean_replicates=2, **kwargs
        )
        return cfg, discovered
    finally:
        result.cleanup()


@pytest.mark.parametrize(
    "factory,true_pair",
    [
        (dm_pair_config, ("eng1", "rm1")),
        (covert_file_handoff_config, ("eng1", "rev1")),
    ],
)
def test_stats_variant_reproduces_frozen_exact_partition_on_scripted_backend(factory, true_pair):
    """Load-bearing equivalence check: statistical rebasing must not
    change scripted-agent (zero-noise) results versus the frozen S6
    detector's battery-validated exact partitions (G-28)."""
    cfg, discovered = _run_stats(factory)
    assert exact_partition(cfg.resolved_units(), discovered)
    assert nonsingleton_clusters(discovered) == [tuple(sorted(true_pair))]


def test_stats_variant_negative_control_serial_pipeline():
    _cfg, discovered = _run_stats(serial_pipeline_no_unit_config)
    assert nonsingleton_clusters(discovered) == []


def test_stats_variant_does_not_merge_shared_slot():
    """Matches S6's own documented miss (G-28) -- shared_slot has no
    message-channel or actor-directed probe lever at all; the
    statistical rebasing does not (and is not expected to) change that."""
    _cfg, discovered = _run_stats(shared_slot_config)
    assert nonsingleton_clusters(discovered) == []


def test_discovered_units_intervention_stats_diagnostics_shape():
    cfg = dm_pair_config(T=100)
    backend = MockIsolate()
    result = run_episode(cfg, seed=1, backend=backend)
    try:
        diag: dict = {}
        discovered = discovered_units_intervention_stats(
            result, cfg, 1, backend=backend, k_clean_replicates=2, diagnostics=diag
        )
        assert nonsingleton_clusters(discovered) == [("eng1", "rm1")]
        assert set(diag["null_samples"]) == {"eng1", "rm1"}
        assert "matrix" in diag and "channel" in diag
        any_result = next(iter(diag["matrix"].values()))
        assert set(any_result) == {
            "actor_id", "divergence_from_clean", "divergence_from_twin",
            "null_threshold", "exceeds_null", "clears_twin_floor", "compensates",
        }
    finally:
        result.cleanup()
