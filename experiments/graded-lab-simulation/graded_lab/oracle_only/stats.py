"""Tiny sample-statistics helpers shared by the calibration battery and
`run_referee_eai_check.py`. Uses `scipy.stats` for the Student-`t`
critical value (DESIGN.md "Phase 7c full battery, both vantages, with
confidence intervals"). Requires ``n >= 2`` for a non-degenerate CI.

R-MB6a / V2-4: ``permutation_mass_movement_band`` implements the
GL-25 noise-floor control for selection mass-share claims (DESIGN.md
"Variation-operator edit vocabulary", ``N_PERMUTATIONS = 200``).
"""

from __future__ import annotations

import math
import random

from scipy import stats

# --- V4-1 frozen constant (R-MB6a null harness, do not tune post-registration)
N_PERMUTATIONS = 200


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
    idiosyncrasy is shared across both samples (FINDINGS GL-16/GL-17's
    "single seed flip" caveat)."""
    if len(a) != len(b):
        raise ValueError(f"paired comparison needs equal-length samples, got {len(a)} vs {len(b)}")
    diffs = [x - y for x, y in zip(a, b)]
    stats_row = ci95(diffs)
    stats_row["zero_in_ci95"] = stats_row["ci95_low"] <= 0.0 <= stats_row["ci95_high"]
    return stats_row


def _mass_range_after_shuffle(
    generation_fitness: list[list[float]],
    *,
    rng: random.Random,
    selection_strength: float = 1.0,
    mass_floor: float = 0.01,
) -> float:
    """Simulate mass reallocation when per-member fitness values are
    reshuffled across members within each generation."""
    n = len(generation_fitness[0]) if generation_fitness else 0
    if n == 0:
        return 0.0
    masses = [1.0 / n] * n
    max_range = 0.0
    for fitness in generation_fitness:
        shuffled = list(fitness)
        rng.shuffle(shuffled)
        avg = sum(shuffled) / n if n else 1.0
        if avg <= 0:
            continue
        scaled = [(f / avg) ** selection_strength for f in shuffled]
        raw = [m * f for m, f in zip(masses, scaled)]
        floored = [max(mass_floor, r) for r in raw]
        total = sum(floored) or 1.0
        masses = [f / total for f in floored]
        max_range = max(max_range, max(masses) - min(masses))
    return max_range


def permutation_mass_movement_band(
    generation_fitness: list[list[float]],
    *,
    n_permutations: int = N_PERMUTATIONS,
    seed: int = 0,
    selection_strength: float = 1.0,
    mass_floor: float = 0.01,
) -> dict[str, float]:
    """[2.5, 97.5] percentile band of max mass-range under label shuffle.

    ``generation_fitness[g][i]`` is member ``i``'s realized fitness in
    generation ``g``. The band answers: "how much mass concentration could
    arise from attribution noise alone?"
    """
    if not generation_fitness or not generation_fitness[0]:
        return {"p2_5": 0.0, "p97_5": 0.0, "n_permutations": float(n_permutations)}
    rng = random.Random(seed)
    samples = [
        _mass_range_after_shuffle(
            generation_fitness,
            rng=rng,
            selection_strength=selection_strength,
            mass_floor=mass_floor,
        )
        for _ in range(n_permutations)
    ]
    samples.sort()
    lo_idx = max(0, int(0.025 * (len(samples) - 1)))
    hi_idx = min(len(samples) - 1, int(0.975 * (len(samples) - 1)))
    return {
        "p2_5": samples[lo_idx],
        "p97_5": samples[hi_idx],
        "n_permutations": float(n_permutations),
    }


def observed_mass_range(
    generation_fitness: list[list[float]],
    *,
    selection_strength: float = 1.0,
    mass_floor: float = 0.01,
) -> float:
    """Max (max_mass - min_mass) along the observed (unshuffled) trajectory."""
    n = len(generation_fitness[0]) if generation_fitness else 0
    if n == 0:
        return 0.0
    masses = [1.0 / n] * n
    max_range = 0.0
    for fitness in generation_fitness:
        avg = sum(fitness) / n if n else 1.0
        if avg <= 0:
            continue
        scaled = [(f / avg) ** selection_strength for f in fitness]
        raw = [m * f for m, f in zip(masses, scaled)]
        floored = [max(mass_floor, r) for r in raw]
        total = sum(floored) or 1.0
        masses = [f / total for f in floored]
        max_range = max(max_range, max(masses) - min(masses))
    return max_range
