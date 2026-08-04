"""Full-partition UAD scoring tests."""

from __future__ import annotations

from graded_lab.oracle_only.uad_partition import (
    exact_partition,
    full_partition_match,
    partition_clusters,
)


def test_full_partition_match_requires_singletons():
    true = {"pair": ("a", "b"), "c": ("c",)}
    assert full_partition_match(true, {"pair": ("a", "b"), "c": ("c",)})
    assert not full_partition_match(true, {"pair": ("a", "b")})


def test_exact_partition_ignores_singleton_labels():
    true = {"pair": ("a", "b"), "c": ("c",)}
    loose = {"x": ("a", "b"), "c": ("c",)}
    assert exact_partition(true, loose)
    assert partition_clusters(true) == partition_clusters(loose)
