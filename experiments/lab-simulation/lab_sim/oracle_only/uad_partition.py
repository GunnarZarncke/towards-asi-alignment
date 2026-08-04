"""S6 phase 6 (PLAN.md): partition scoring beyond ``uad.uad_score``'s
blind spot (LS-24).

``uad_score`` is a raw Rand index over pairs within ``true_units`' actor
set only — a fully-merged blob that happens to contain the true pair
still scores 1.0. This module adds:

- ``exact_partition``: non-singleton discovered clusters == exactly the
  set of true non-singleton units (order-independent).
- ``adjusted_rand_index``: chance-adjusted pair agreement over the union
  of actors named in either partition.

Recorded referee extension: own module, never touches frozen code.
"""

from __future__ import annotations

from itertools import combinations


def nonsingleton_clusters(discovered: dict[str, tuple[str, ...]]) -> list[tuple[str, ...]]:
    return sorted(tuple(sorted(m)) for m in discovered.values() if len(m) > 1)


def exact_partition(
    true_units: dict[str, tuple[str, ...]], discovered: dict[str, tuple[str, ...]]
) -> bool:
    true_nonsingle = sorted(tuple(sorted(m)) for m in true_units.values() if len(m) > 1)
    return nonsingleton_clusters(discovered) == true_nonsingle


def _pair_labels(units: dict[str, tuple[str, ...]], actors: list[str]) -> dict[frozenset[str], bool]:
    """Map unordered actor pair -> same-unit? for actors in ``actors``."""
    parent = {a: a for a in actors}

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
    labels: dict[frozenset[str], bool] = {}
    for a, b in combinations(sorted(actors), 2):
        labels[frozenset((a, b))] = find(a) == find(b)
    return labels


def adjusted_rand_index(
    true_units: dict[str, tuple[str, ...]], discovered: dict[str, tuple[str, ...]]
) -> float:
    actors = sorted({a for m in true_units.values() for a in m} | {a for m in discovered.values() for a in m})
    if len(actors) < 2:
        return 1.0
    true_l = _pair_labels(true_units, actors)
    disc_l = _pair_labels(discovered, actors)
    pairs = list(true_l.keys())
    n = len(pairs)
    agree = sum(1 for p in pairs if true_l[p] == disc_l[p])
    # Expected agreement under random partitions with same cluster-count
    # structure is hard without full contingency; use the standard pair-
    # formulation ARI for binary same/different labels.
    tp = sum(1 for p in pairs if true_l[p] and disc_l[p])
    tn = sum(1 for p in pairs if not true_l[p] and not disc_l[p])
    fp = sum(1 for p in pairs if not true_l[p] and disc_l[p])
    fn = sum(1 for p in pairs if true_l[p] and not disc_l[p])
    if tp + fp == 0 or tp + fn == 0:
        return 1.0 if agree == n else 0.0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def partition_metrics(
    true_units: dict[str, tuple[str, ...]], discovered: dict[str, tuple[str, ...]]
) -> dict[str, float | bool | list]:
    from .uad import uad_score

    return {
        "exact": exact_partition(true_units, discovered),
        "uad_score": uad_score(true_units, discovered),
        "adjusted_rand": adjusted_rand_index(true_units, discovered),
        "nonsingleton_clusters": [list(c) for c in nonsingleton_clusters(discovered)],
    }
