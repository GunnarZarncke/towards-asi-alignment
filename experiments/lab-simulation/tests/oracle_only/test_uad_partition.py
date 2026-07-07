"""S6 phase 6: partition scoring."""

from __future__ import annotations

from lab_sim.oracle_only.uad_partition import adjusted_rand_index, exact_partition, partition_metrics


def test_exact_partition_true_when_nonsingleton_clusters_match():
    true = {"u1": ("a", "b"), "c": ("c",)}
    disc = {"x": ("a", "b"), "c": ("c",)}
    assert exact_partition(true, disc)


def test_exact_partition_false_on_over_merge():
    true = {"u1": ("a", "b")}
    disc = {"x": ("a", "b", "c")}
    assert not exact_partition(true, disc)


def test_adjusted_rand_perfect_agreement():
    units = {"u1": ("a", "b"), "u2": ("c", "d")}
    assert adjusted_rand_index(units, units) == 1.0


def test_partition_metrics_includes_exact_and_uad_score():
    true = {"u1": ("a", "b")}
    disc = {"x": ("a", "b")}
    metrics = partition_metrics(true, disc)
    assert metrics["exact"] is True
    assert metrics["uad_score"] == 1.0
