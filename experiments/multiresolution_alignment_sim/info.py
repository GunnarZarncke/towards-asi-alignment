"""Discrete entropy, MI, and CMI estimators (stdlib only)."""

from __future__ import annotations

import math
from collections import Counter
from typing import Iterable, Sequence


def entropy_from_keys(keys: Iterable[tuple]) -> float:
    counts = Counter(keys)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def mutual_information(x: Sequence[int], y: Sequence[int]) -> float:
    if len(x) != len(y) or len(x) == 0:
        return 0.0
    keys_xy = list(zip(x, y, strict=True))
    return max(
        0.0,
        entropy_from_keys(x)
        + entropy_from_keys(y)
        - entropy_from_keys(keys_xy),
    )


def conditional_mutual_information(
    x: Sequence[int],
    y: Sequence[int],
    z_cols: Sequence[Sequence[int]],
) -> float:
    if len(x) == 0 or len(x) != len(y):
        return 0.0
    if not z_cols:
        return mutual_information(x, y)

    def join(*cols: Sequence[int]) -> list[tuple]:
        return list(zip(*cols, strict=True))

    xz = join(x, *z_cols)
    yz = join(y, *z_cols)
    z = join(*z_cols)
    xyz = join(x, y, *z_cols)
    return max(
        0.0,
        entropy_from_keys(xz)
        + entropy_from_keys(yz)
        - entropy_from_keys(z)
        - entropy_from_keys(xyz),
    )


def quantile_bin(series: Sequence[float], n_bins: int = 4) -> list[int]:
    if not series:
        return []
    sorted_vals = sorted(series)
    n = len(sorted_vals)

    def bin_one(v: float) -> int:
        rank = sum(1 for s in sorted_vals if s <= v)
        b = int((rank / n) * n_bins)
        return min(n_bins - 1, max(0, b))

    return [bin_one(v) for v in series]


def lagged_pair(
    x: Sequence[int], y: Sequence[int], lag: int = 1
) -> tuple[list[int], list[int]]:
    if lag <= 0 or len(x) <= lag:
        return [], []
    return list(x[:-lag]), list(y[lag:])


def pairwise_mi_matrix(binned: list[list[int]], lag: int = 1) -> list[list[float]]:
    n = len(binned)
    mat = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            xi, xj = lagged_pair(binned[i], binned[j], lag)
            if len(xi) < 10:
                continue
            mi = mutual_information(xi, xj)
            mat[i][j] = mat[j][i] = mi
    return mat
