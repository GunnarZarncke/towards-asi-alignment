"""Plug-in discrete MI, quantile binning, and a Wilson lower bound (stdlib
only; pattern ported from embedded_sim.audit_core.{info,structural_signals},
trimmed to what this line's mini channel scan and small-n detectors need)."""

from __future__ import annotations

import math
from collections import Counter
from statistics import NormalDist
from typing import Iterable, Sequence


def entropy_from_keys(keys: Iterable) -> float:
    counts = Counter(keys)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counts.values()) + 0.0


def mutual_information(x: Sequence[int], y: Sequence[int]) -> float:
    if len(x) != len(y) or len(x) == 0:
        return 0.0
    return max(
        0.0,
        entropy_from_keys(x)
        + entropy_from_keys(y)
        - entropy_from_keys(list(zip(x, y, strict=True))),
    )


def quantile_bin(series: Sequence[float], n_bins: int = 4) -> list[int]:
    if not series:
        return []
    sorted_vals = sorted(series)
    n = len(sorted_vals)

    def bin_one(v: float) -> int:
        rank = sum(1 for s in sorted_vals if s <= v)
        return min(n_bins - 1, max(0, int((rank / n) * n_bins)))

    return [bin_one(v) for v in series]


def saturating_ratio(raw: float, scale: float) -> float:
    """Monotone map [0, inf) -> [0, 1); `raw == scale` -> 0.5, asymptoting to
    1 as `raw` grows. Used (Phase 4, `severity.py` / `detectors.py` score
    variants) to bring an unbounded raw quantity (e.g. cumulative harm) onto
    a scale comparable to naturally-bounded components ([0, 1] rates), using
    only a pre-existing frozen constant as `scale` -- never a value fit from
    the data being scored."""
    x = max(0.0, raw) / scale if scale else 0.0
    return x / (1.0 + x)


def spearman_correlation(x: Sequence[float], y: Sequence[float]) -> float:
    """Spearman rank correlation (stdlib only; average ranks for ties). Used
    where the comparison target is an ordering (Phase 4: does a detector
    score rank episodes the way oracle severity does), which stays
    well-defined even when a binary label is fully saturated (`FINDINGS.md`
    GA-14) -- there is no "positive class" requirement, unlike detection
    rate or AUC against a boolean label."""
    n = len(x)
    if n != len(y) or n < 2:
        return 0.0

    def _ranks(values: Sequence[float]) -> list[float]:
        order = sorted(range(n), key=lambda i: values[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and values[order[j + 1]] == values[order[i]]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                ranks[order[k]] = avg_rank
            i = j + 1
        return ranks

    rx, ry = _ranks(x), _ranks(y)
    mean_rx, mean_ry = sum(rx) / n, sum(ry) / n
    cov = sum((a - mean_rx) * (b - mean_ry) for a, b in zip(rx, ry))
    var_x = sum((a - mean_rx) ** 2 for a in rx)
    var_y = sum((b - mean_ry) ** 2 for b in ry)
    denom = math.sqrt(var_x * var_y)
    return cov / denom if denom > 0 else 0.0


def bonferroni_alpha(family_alpha: float, n_tests: int) -> float:
    """Per-test alpha for a Bonferroni correction across `n_tests` simultaneous
    predictions, holding the family-wise error rate at `family_alpha`. Used
    where a pre-registered protocol tests the same prediction under more than
    one bracketed threshold (e.g. `run_phase3_blind.py`'s low/high L2
    thresholds) instead of picking one after seeing results."""
    if n_tests <= 0:
        raise ValueError("n_tests must be positive")
    return family_alpha / n_tests


def wilson_lower_bound(successes: int, n: int, confidence: float) -> float:
    """One-sided Wilson score lower bound on a true Bernoulli rate.

    Ported verbatim (pattern) from the embedded-simulation line's N-12 fix
    (`embedded_sim.audit_core.structural_signals._wilson_lower_bound`):
    stdlib normal approximation to the exact Jeffreys/Beta interval, used
    where a raw sample fraction against a fixed threshold is miscalibrated
    at small `n` (see `detectors.d1_probe_divergence_wilson`).
    """
    if n <= 0:
        return 0.0
    z = NormalDist().inv_cdf(confidence)
    p = successes / n
    denom = 1.0 + z * z / n
    center = p + z * z / (2 * n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (center - margin) / denom
