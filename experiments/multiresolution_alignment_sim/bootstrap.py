"""Block bootstrap confidence intervals for intervention-probe metrics."""

from __future__ import annotations

import random

from .info import conditional_mutual_information
from .schemas import AuditTrace


def _action_series(audit: AuditTrace) -> list[int]:
    if audit.action_observed and audit.instrumentation != "none":
        return audit.action_observed
    return audit.action_channel


def _percentile(vals: list[float], p: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    i = min(len(s) - 1, max(0, int(p * (len(s) - 1))))
    return s[i]


def bootstrap_interventional(
    audit: AuditTrace,
    k: int = 3,
    n_boot: int = 200,
    seed: int = 0,
    store_samples: bool = False,
) -> dict[str, float | list[float]]:
    """Bootstrap CI for probe uptake and interventional CCI (handle modes only)."""
    T = len(audit.correction_request)
    actions = _action_series(audit)
    idx = [t for t in range(T) if audit.intervention_active[t]]
    empty: dict[str, float | list[float]] = {
        "interventional_cci_mean": 0.0,
        "interventional_cci_lo": 0.0,
        "interventional_cci_hi": 0.0,
        "uptake_mean": 0.0,
        "uptake_lo": 0.0,
        "uptake_hi": 0.0,
        "n_probes": float(len(idx)),
        "n_boot": float(n_boot),
    }
    if store_samples:
        empty["interventional_cci_samples"] = []
        empty["uptake_samples"] = []
    if len(idx) < 5:
        return empty

    rng = random.Random(seed)
    cci_samples: list[float] = []
    uptake_samples: list[float] = []

    for _ in range(n_boot):
        sample_idx = [idx[rng.randrange(len(idx))] for _ in range(len(idx))]
        intents: list[int] = []
        actions_lag: list[int] = []
        sensors: list[int] = []
        internals: list[int] = []
        capacities: list[float] = []
        for t in sample_idx:
            intent = audit.intervention_intent[t]
            intents.append(intent)
            tl = min(t + k, T - 1)
            actions_lag.append(actions[tl])
            sensors.append(audit.sensor_channel[t])
            internals.append(audit.internal_channel[t])
            capacities.append(1.0 if actions[t] == intent else 0.0)
        ivl = conditional_mutual_information(intents, actions_lag, [sensors, internals])
        cci_samples.append(max(0.0, ivl))
        uptake_samples.append(sum(capacities) / len(capacities))

    out: dict[str, float | list[float]] = {
        "interventional_cci_mean": sum(cci_samples) / len(cci_samples),
        "interventional_cci_lo": _percentile(cci_samples, 0.025),
        "interventional_cci_hi": _percentile(cci_samples, 0.975),
        "uptake_mean": sum(uptake_samples) / len(uptake_samples),
        "uptake_lo": _percentile(uptake_samples, 0.025),
        "uptake_hi": _percentile(uptake_samples, 0.975),
        "n_probes": float(len(idx)),
        "n_boot": float(n_boot),
    }
    if store_samples:
        out["interventional_cci_samples"] = cci_samples
        out["uptake_samples"] = uptake_samples
    return out


def hierarchical_bootstrap(
    runs: list[dict],
    metric_prefix: str,
    n_boot: int = 500,
    seed: int = 0,
) -> dict[str, float]:
    """Legacy: resample seeds then perturb within-run using stored lo/hi intervals."""
    boot_runs = [r for r in runs if r.get("bootstrap_interventional")]
    if not boot_runs:
        return {"mean": 0.0, "lo": 0.0, "hi": 0.0, "n": 0.0}

    by_seed: dict[int, list[dict]] = {}
    for run in boot_runs:
        by_seed.setdefault(int(run["seed"]), []).append(run)

    rng = random.Random(seed)
    seeds = list(by_seed.keys())
    samples: list[float] = []
    mean_key = f"{metric_prefix}_mean"
    lo_key = f"{metric_prefix}_lo"
    hi_key = f"{metric_prefix}_hi"

    for _ in range(n_boot):
        chosen = [seeds[rng.randrange(len(seeds))] for _ in range(len(seeds))]
        vals: list[float] = []
        for s in chosen:
            run = by_seed[s][rng.randrange(len(by_seed[s]))]
            boot = run["bootstrap_interventional"]
            lo = float(boot[lo_key])
            hi = float(boot[hi_key])
            vals.append(rng.uniform(lo, hi) if hi > lo else float(boot[mean_key]))
        samples.append(sum(vals) / len(vals))

    return {
        "mean": sum(samples) / len(samples),
        "lo": _percentile(samples, 0.025),
        "hi": _percentile(samples, 0.975),
        "n": float(len(boot_runs)),
    }


def hierarchical_bootstrap_episode(
    runs: list[dict],
    sample_key: str,
    mean_key: str,
    n_boot: int = 500,
    seed: int = 0,
) -> dict[str, float]:
    """Two-level bootstrap: resample runs/seeds, then resample inner episode samples."""
    boot_runs = [r for r in runs if r.get("bootstrap_interventional")]
    if not boot_runs:
        return {"mean": 0.0, "lo": 0.0, "hi": 0.0, "n": 0.0}

    usable = [
        r
        for r in boot_runs
        if sample_key in r.get("bootstrap_interventional", {})
        and r["bootstrap_interventional"][sample_key]
    ]
    if not usable:
        prefix = mean_key.replace("_mean", "")
        return hierarchical_bootstrap(boot_runs, prefix, n_boot=n_boot, seed=seed)

    by_seed: dict[int, list[dict]] = {}
    for run in usable:
        by_seed.setdefault(int(run["seed"]), []).append(run)

    rng = random.Random(seed)
    seeds = list(by_seed.keys())
    samples: list[float] = []

    for _ in range(n_boot):
        chosen_seeds = [seeds[rng.randrange(len(seeds))] for _ in range(len(seeds))]
        vals: list[float] = []
        for s in chosen_seeds:
            run = by_seed[s][rng.randrange(len(by_seed[s]))]
            inner: list[float] = list(run["bootstrap_interventional"][sample_key])  # type: ignore[arg-type]
            if not inner:
                continue
            resampled = [inner[rng.randrange(len(inner))] for _ in range(len(inner))]
            vals.append(sum(resampled) / len(resampled))
        if vals:
            samples.append(sum(vals) / len(vals))

    if not samples:
        prefix = mean_key.replace("_mean", "")
        return hierarchical_bootstrap(boot_runs, prefix, n_boot=n_boot, seed=seed)

    return {
        "mean": sum(samples) / len(samples),
        "lo": _percentile(samples, 0.025),
        "hi": _percentile(samples, 0.975),
        "n": float(len(usable)),
    }


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
    """Across-seed (or across-run) percentile interval for scalar metrics."""
    if not values:
        return {"mean": 0.0, "lo": 0.0, "hi": 0.0, "n": 0.0}

    return {
        "mean": sum(values) / len(values),
        "lo": _percentile(values, lo),
        "hi": _percentile(values, hi),
        "n": float(len(values)),
    }
