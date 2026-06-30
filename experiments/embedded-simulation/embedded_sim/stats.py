"""Bootstrap and percentile helpers (toy-simulation parity)."""

from __future__ import annotations

import random


def _percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = p * (len(ordered) - 1)
    lo = int(idx)
    hi = min(lo + 1, len(ordered) - 1)
    frac = idx - lo
    return ordered[lo] * (1.0 - frac) + ordered[hi] * frac


def hierarchical_bootstrap_rate(
    runs: list[dict],
    field: str = "cci_status_correct",
    n_boot: int = 500,
    seed: int = 0,
) -> dict[str, float]:
    """Bootstrap CI for a binary/scalar rate nested by seed."""
    if not runs:
        return {"mean": 0.0, "lo": 0.0, "hi": 0.0, "n": 0.0}

    by_seed: dict[int, list[float]] = {}
    for run in runs:
        val = run.get("evaluation", {}).get(field, run.get(field))
        if val is None:
            continue
        by_seed.setdefault(int(run["seed"]), []).append(float(bool(val)))

    if not by_seed:
        return {"mean": 0.0, "lo": 0.0, "hi": 0.0, "n": 0.0}

    rng = random.Random(seed)
    seeds = list(by_seed.keys())
    samples: list[float] = []
    for _ in range(n_boot):
        chosen = [seeds[rng.randrange(len(seeds))] for _ in range(len(seeds))]
        vals: list[float] = []
        for s in chosen:
            bucket = by_seed[s]
            pick = bucket[rng.randrange(len(bucket))]
            vals.append(pick)
        samples.append(sum(vals) / len(vals))

    return {
        "mean": sum(samples) / len(samples),
        "lo": _percentile(samples, 0.025),
        "hi": _percentile(samples, 0.975),
        "n": float(len(runs)),
    }


def percentile_ci(values: list[float], lo: float = 0.025, hi: float = 0.975) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "lo": 0.0, "hi": 0.0, "n": 0.0}
    return {
        "mean": sum(values) / len(values),
        "lo": _percentile(values, lo),
        "hi": _percentile(values, hi),
        "n": float(len(values)),
    }
