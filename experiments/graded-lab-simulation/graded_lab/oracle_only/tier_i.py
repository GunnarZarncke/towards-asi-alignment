"""Tier-I estimators — referee infers some effects from finite draws."""

from __future__ import annotations

import math

DIVERGENCE_FLAG_Z = 2.0


def integrated_field_harm(incident_samples: list[float]) -> dict[str, float]:
    """Tier-I: exact sum over already-drawn incident severities."""
    if not incident_samples:
        return {"integrated_harm": 0.0, "n_incidents": 0, "se": 0.0}
    total = sum(incident_samples)
    n = len(incident_samples)
    mean = total / n
    if n < 2:
        return {"integrated_harm": total, "n_incidents": n, "se": 0.0}
    var = sum((x - mean) ** 2 for x in incident_samples) / (n - 1)
    se = (var ** 0.5) / math.sqrt(n)
    return {"integrated_harm": total, "n_incidents": n, "se": se}


def report_divergence_score(
    filed_mean_hazard: float,
    eval_sample_mean: float,
    eval_sample_se: float,
    eval_sample_n: int,
) -> dict[str, float | bool]:
    """Tier-I distribution-valued divergence."""
    if eval_sample_n <= 0:
        z = 0.0
    elif eval_sample_se <= 1e-12:
        z = abs(filed_mean_hazard - eval_sample_mean) * 100.0
    else:
        z = abs(filed_mean_hazard - eval_sample_mean) / eval_sample_se
    return {
        "divergence_z": z,
        "divergence_flag": z >= DIVERGENCE_FLAG_Z,
        "eval_sample_n": float(eval_sample_n),
        "eval_sample_se": eval_sample_se,
    }
