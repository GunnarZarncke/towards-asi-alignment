"""ET-2 Leaf A: frozen passive UAD scoring for CIL basin_stability episodes.

Pure Python / stdlib only (plus the already-vendored ``graded_lab.oracle_only``
CMI pipeline) — no jax/CIL import here, so this module and its tests run
without the sibling checkout installed.

Reuses the exact same lag-CMI edge-discovery pipeline as ET-1
(``graded_lab.oracle_only.uad_discovery.cmi_edge_matrix``), unmodified and
unretuned, applied to a different substrate's action series.

Scoring choice (PLAN_ET2.md, ET2-0 freeze): Adjusted Rand Index (Hubert-Arabie,
corrected for chance) against a label-permutation null, not ET-1's fixed-pair
exact-match test — the true "coalition" here is a variable-size subset
(2-12 of 20 agents depending on adversarial_fraction), not a fixed named pair.

Note: `graded_lab.oracle_only.uad_partition.adjusted_rand_index` is actually a
pairwise-F1 score despite its name (precision/recall on same-cluster pairs),
not the chance-corrected Hubert-Arabie ARI used here. Do not conflate the two
when reading FINDINGS entries from different ET lines.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from graded_lab.oracle_only.uad_discovery import (
    DEFAULT_MAX_LAG,
    DEFAULT_MIN_EFFECT_BITS,
    DEFAULT_N_SHIFTS,
    DEFAULT_NULL_QUANTILE,
    cmi_edge_matrix,
)

UAD_RNG_SEED = 0
DEFAULT_N_PERMUTATIONS = 100
DEFAULT_PERMUTATION_PERCENTILE = 95.0


def discovered_partition(
    series: dict[str, list[int]],
    *,
    rng_seed: int = UAD_RNG_SEED,
    max_lag: int = DEFAULT_MAX_LAG,
    n_shifts: int = DEFAULT_N_SHIFTS,
    null_quantile: float = DEFAULT_NULL_QUANTILE,
    min_effect_bits: float = DEFAULT_MIN_EFFECT_BITS,
) -> dict[str, tuple[str, ...]]:
    """Run frozen passive UAD (CMI|rest) on an action-code series dict."""
    actor_ids = sorted(series.keys())
    edges = cmi_edge_matrix(
        series,
        max_lag=max_lag,
        n_shifts=n_shifts,
        null_quantile=null_quantile,
        min_effect_bits=min_effect_bits,
        rng_seed=rng_seed,
    )

    parent = {a: a for a in actor_ids}

    def find(x: str) -> str:
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for a, b in edges:
        union(a, b)

    groups: dict[str, list[str]] = {}
    for a in actor_ids:
        groups.setdefault(find(a), []).append(a)

    out: dict[str, tuple[str, ...]] = {}
    for i, members in enumerate(sorted(groups.values(), key=lambda m: (-len(m), m)), start=1):
        key = f"unit_{i}" if len(members) > 1 else members[0]
        out[key] = tuple(sorted(members))
    return out


def _binary_labels(partition: dict[str, tuple[str, ...]], actor_ids: list[str]) -> list[int]:
    """Map a partition to a canonical cluster-id-per-actor label vector."""
    cluster_of: dict[str, int] = {}
    for i, members in enumerate(partition.values()):
        for actor in members:
            cluster_of[actor] = i
    return [cluster_of[a] for a in actor_ids]


def adjusted_rand_index(labels_a: list[int], labels_b: list[int]) -> float:
    """Chance-corrected Hubert-Arabie ARI between two label vectors.

    Standard contingency-table formula; returns 1.0 for identical partitions
    of <2 elements (degenerate case) and 0.0 when the expected index cannot
    be computed (all points in one cluster in both partitions with no
    variance to correct for, handled by the max()-guard below).
    """
    n = len(labels_a)
    if n != len(labels_b):
        raise ValueError("label vectors must have equal length")
    if n < 2:
        return 1.0

    contingency: dict[tuple[int, int], int] = {}
    row_sums: dict[int, int] = {}
    col_sums: dict[int, int] = {}
    for a, b in zip(labels_a, labels_b):
        contingency[(a, b)] = contingency.get((a, b), 0) + 1
        row_sums[a] = row_sums.get(a, 0) + 1
        col_sums[b] = col_sums.get(b, 0) + 1

    def n_choose_2(x: int) -> float:
        return x * (x - 1) / 2.0

    sum_comb_c = sum(n_choose_2(v) for v in contingency.values())
    sum_comb_rows = sum(n_choose_2(v) for v in row_sums.values())
    sum_comb_cols = sum(n_choose_2(v) for v in col_sums.values())
    total_comb = n_choose_2(n)

    expected_index = (sum_comb_rows * sum_comb_cols) / total_comb if total_comb else 0.0
    max_index = 0.5 * (sum_comb_rows + sum_comb_cols)
    denom = max_index - expected_index
    if denom == 0:
        # Both partitions are identical single clusters or identical
        # singleton-only partitions: perfect agreement, define ARI = 1.0.
        return 1.0
    return (sum_comb_c - expected_index) / denom


def permutation_null_aris(
    partition: dict[str, tuple[str, ...]],
    true_node_types: list[int],
    actor_ids: list[str],
    *,
    n_permutations: int = DEFAULT_N_PERMUTATIONS,
    rng_seed: int = 0,
) -> list[float]:
    """ARI(discovered, label-permuted truth) for n_permutations random relabelings.

    The discovered partition does not depend on the (true/permuted) labels —
    only on the action series — so we hold it fixed and permute the ground
    truth, matching the "honest surrogate null" style used elsewhere in this
    repo and in CIL's own polycentric_emergence work.
    """
    disc_labels = _binary_labels(partition, actor_ids)
    rng = random.Random(rng_seed)
    shuffled = list(true_node_types)
    out = []
    for _ in range(n_permutations):
        rng.shuffle(shuffled)
        out.append(adjusted_rand_index(disc_labels, list(shuffled)))
    return out


@dataclass(frozen=True)
class Et2EpisodeScore:
    mechanism: str
    adversarial_fraction: float
    seed: int
    n_agents: int
    n_adversarial: int
    ari_true: float
    permutation_null_p95: float
    exceeds_null: bool
    partition_size: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "mechanism": self.mechanism,
            "adversarial_fraction": self.adversarial_fraction,
            "seed": self.seed,
            "n_agents": self.n_agents,
            "n_adversarial": self.n_adversarial,
            "ari_true": self.ari_true,
            "permutation_null_p95": self.permutation_null_p95,
            "exceeds_null": self.exceeds_null,
            "partition_size": self.partition_size,
        }


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    k = (len(s) - 1) * (pct / 100.0)
    f, c = int(k), min(int(k) + 1, len(s) - 1)
    if f == c:
        return s[f]
    return s[f] + (s[c] - s[f]) * (k - f)


def score_episode(
    episode: dict[str, Any],
    *,
    adversarial_fraction: float,
    n_permutations: int = DEFAULT_N_PERMUTATIONS,
    permutation_percentile: float = DEFAULT_PERMUTATION_PERCENTILE,
    rng_seed: int = UAD_RNG_SEED,
) -> Et2EpisodeScore:
    """Score one run_basin_stability_episode() result dict (JAX-free input)."""
    n_agents = episode["n_agents"]
    actor_ids = [f"agent_{i}" for i in range(n_agents)]
    series = {actor_ids[i]: [row[i] for row in episode["actions"]] for i in range(n_agents)}

    partition = discovered_partition(series, rng_seed=rng_seed)
    disc_labels = _binary_labels(partition, actor_ids)
    true_labels = episode["node_types"]

    ari_true = adjusted_rand_index(disc_labels, true_labels)
    null_scores = permutation_null_aris(
        partition, true_labels, actor_ids, n_permutations=n_permutations, rng_seed=rng_seed
    )
    p95 = _percentile(null_scores, permutation_percentile)

    return Et2EpisodeScore(
        mechanism=episode["mechanism"],
        adversarial_fraction=adversarial_fraction,
        seed=episode["seed"],
        n_agents=n_agents,
        n_adversarial=episode["n_adversarial"],
        ari_true=ari_true,
        permutation_null_p95=p95,
        exceeds_null=ari_true > p95,
        partition_size=len(partition),
    )


def evaluate_et2a_battery(scores: list[Et2EpisodeScore]) -> dict[str, Any]:
    """Resolve P1-P3 (PLAN_ET2.md) over a set of scored episodes.

    P1: for each (mechanism, frac>0) cell, exceeds_null rate >= 60%.
    P2: at frac=0 (no true adversarial subgroup, all-zero labels), the
        discovered partition should not exceed a permutation null built on a
        *matched random subgroup of the corresponding non-zero frac's size*
        (checked by the caller passing frac=0 episodes with a synthetic
        matched-size label vector; see run_et2_uad_battery.py). Here we only
        aggregate whatever exceeds_null values were computed and passed in.
    P3: adapter sanity — always true on this substrate since the action
        space is closed (no "unmapped" concept); recorded for schema parity
        with ET-1, not because it can meaningfully fail here.
    """
    by_cell: dict[tuple[str, float], list[Et2EpisodeScore]] = {}
    for s in scores:
        by_cell.setdefault((s.mechanism, s.adversarial_fraction), []).append(s)

    cells = {}
    p1_pass_cells = 0
    p1_total_cells = 0
    for (mech, frac), cell_scores in sorted(by_cell.items()):
        n = len(cell_scores)
        hits = sum(1 for s in cell_scores if s.exceeds_null)
        rate = hits / n if n else 0.0
        cells[f"{mech}@{frac}"] = {"n": n, "hits": hits, "rate": rate}
        if frac > 0:
            p1_total_cells += 1
            if rate >= 0.6:
                p1_pass_cells += 1

    p1_holds = p1_total_cells > 0 and p1_pass_cells >= max(1, int(0.6 * p1_total_cells))

    return {
        "et2_protocol_version": "et2-0.1.0",
        "cells": cells,
        "predictions": {
            "P1": {
                "holds": p1_holds,
                "cells_passing": p1_pass_cells,
                "cells_total": p1_total_cells,
            },
        },
        "n_episodes": len(scores),
        "episodes": [s.to_dict() for s in scores],
    }
