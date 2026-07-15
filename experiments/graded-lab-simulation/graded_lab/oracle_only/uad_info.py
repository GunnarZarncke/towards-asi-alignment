"""Discrete MI / CMI helpers for graded-lab UAD (GL-51).

Ported in spirit from ``lab_sim.oracle_only.attic.uad_cmi`` and
``agency_detect.markov_blanket`` — standalone so graded-lab does not import
sibling experiment packages. Plug-in estimators with optional Laplace
smoothing on CMI when alphabets are sparse.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Sequence


def entropy(keys: Sequence) -> float:
    counts = Counter(keys)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def mutual_info(x: Sequence, y: Sequence) -> float:
    if not (len(x) == len(y)) or len(x) == 0:
        return 0.0
    return max(0.0, entropy(x) + entropy(y) - entropy(list(zip(x, y))))


def conditional_mi(x: Sequence, y: Sequence, z: Sequence) -> float:
    """I(X;Y|Z) = H(X,Z) + H(Y,Z) - H(X,Y,Z) - H(Z)."""
    if not (len(x) == len(y) == len(z)) or len(x) == 0:
        return 0.0
    return max(
        0.0,
        entropy(list(zip(x, z)))
        + entropy(list(zip(y, z)))
        - entropy(list(zip(x, y, z)))
        - entropy(list(z)),
    )


def lagmax_mutual_info(x: Sequence, y: Sequence, *, max_lag: int) -> float:
    best = mutual_info(x, y)
    for tau in range(1, max_lag + 1):
        if tau >= len(x):
            break
        best = max(best, mutual_info(x[:-tau], y[tau:]))
        best = max(best, mutual_info(x[tau:], y[:-tau]))
    return best


def lagmax_conditional_mi(
    x: Sequence, y: Sequence, z: Sequence, *, max_lag: int
) -> float:
    """Max over lags τ ∈ [-max_lag, max_lag] of I(x_t; y_{t+τ} | z_t).

    Conditioning symbol is aligned to the earlier index (same approximation
    as lab-sim attic ``uad_cmi``; permutation nulls use the same alignment).
    """
    best = conditional_mi(x, y, z)
    for tau in range(1, max_lag + 1):
        if tau >= len(x):
            break
        best = max(best, conditional_mi(x[:-tau], y[tau:], z[:-tau]))
        best = max(best, conditional_mi(x[tau:], y[:-tau], z[tau:]))
    return best
