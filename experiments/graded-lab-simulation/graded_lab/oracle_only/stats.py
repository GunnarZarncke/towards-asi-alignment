"""Tiny sample-statistics helpers shared by the calibration battery and
`run_referee_eai_check.py`. Uses `scipy.stats` for the Student-`t`
critical value (DESIGN.md "Phase 7c full battery, both vantages, with
confidence intervals"). Requires ``n >= 2`` for a non-degenerate CI.
"""

from __future__ import annotations

import math

from scipy import stats


def mean_std_se(values: list[float]) -> tuple[float, float, float]:
    n = len(values)
    mean = sum(values) / n
    if n < 2:
        return mean, 0.0, 0.0
    variance = sum((v - mean) ** 2 for v in values) / (n - 1)
    std = math.sqrt(variance)
    se = std / math.sqrt(n)
    return mean, std, se


def _t_crit_95(df: int) -> float:
    if df < 1:
        raise ValueError(f"95% t-critical requires df >= 1, got df={df}")
    return float(stats.t.ppf(0.975, df))


def ci95(values: list[float]) -> dict[str, float]:
    """Two-sided 95% CI on the sample mean. Requires ``len(values) >= 2``."""
    n = len(values)
    if n < 2:
        raise ValueError(f"95% CI requires n >= 2, got n={n}")
    df = n - 1
    mean, std, se = mean_std_se(values)
    half_width = _t_crit_95(df) * se
    return {
        "n": n,
        "mean": round(mean, 6),
        "std": round(std, 6),
        "se": round(se, 6),
        "ci95_low": round(mean - half_width, 6),
        "ci95_high": round(mean + half_width, 6),
    }


def paired_diff_ci95(a: list[float], b: list[float]) -> dict[str, float]:
    """Paired difference a - b, paired by index (e.g. same seed at two
    cells). More power than an unpaired comparison when per-seed
    idiosyncrasy is shared across both samples (FINDINGS G-16/G-17's
    "single seed flip" caveat)."""
    if len(a) != len(b):
        raise ValueError(f"paired comparison needs equal-length samples, got {len(a)} vs {len(b)}")
    diffs = [x - y for x, y in zip(a, b)]
    stats_row = ci95(diffs)
    stats_row["zero_in_ci95"] = stats_row["ci95_low"] <= 0.0 <= stats_row["ci95_high"]
    return stats_row
