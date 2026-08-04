"""Phase 7a: partition scoring for recovered units vs oracle ground truth."""

from __future__ import annotations

from itertools import combinations


def partition_clusters(units: dict[str, tuple[str, ...]]) -> frozenset[frozenset[str]]:
    return frozenset(frozenset(members) for members in units.values())


def full_partition_match(
    true_units: dict[str, tuple[str, ...]], discovered: dict[str, tuple[str, ...]]
) -> bool:
    """True when discovered clusters match oracle composites and singletons exactly."""
    return partition_clusters(true_units) == partition_clusters(discovered)


def nonsingleton_clusters(discovered: dict[str, tuple[str, ...]]) -> list[tuple[str, ...]]:
    return sorted(tuple(sorted(members)) for members in discovered.values() if len(members) > 1)


def exact_partition(
    true_units: dict[str, tuple[str, ...]], discovered: dict[str, tuple[str, ...]]
) -> bool:
    true_nonsingle = sorted(tuple(sorted(members)) for members in true_units.values() if len(members) > 1)
    return nonsingleton_clusters(discovered) == true_nonsingle


def _pair_labels(units: dict[str, tuple[str, ...]], actors: list[str]) -> dict[frozenset[str], bool]:
    parent = {actor: actor for actor in actors}

    def find(x: str) -> str:
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for members in units.values():
        for a, b in combinations(sorted(members), 2):
            if a in parent and b in parent:
                union(a, b)
    return {frozenset((a, b)): find(a) == find(b) for a, b in combinations(sorted(actors), 2)}


def adjusted_rand_index(
    true_units: dict[str, tuple[str, ...]], discovered: dict[str, tuple[str, ...]]
) -> float:
    actors = sorted(
        {actor for members in true_units.values() for actor in members}
        | {actor for members in discovered.values() for actor in members}
    )
    if len(actors) < 2:
        return 1.0
    true_labels = _pair_labels(true_units, actors)
    disc_labels = _pair_labels(discovered, actors)
    pairs = list(true_labels.keys())
    tp = sum(1 for pair in pairs if true_labels[pair] and disc_labels[pair])
    tn = sum(1 for pair in pairs if not true_labels[pair] and not disc_labels[pair])
    fp = sum(1 for pair in pairs if not true_labels[pair] and disc_labels[pair])
    fn = sum(1 for pair in pairs if true_labels[pair] and not disc_labels[pair])
    if tp + fp == 0 or tp + fn == 0:
        return 1.0 if tp + tn == len(pairs) else 0.0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)
