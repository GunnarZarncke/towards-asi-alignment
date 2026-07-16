"""PLAN_v3 slice D item 6: frozen-detector coverage on v3 reference episodes.

Runs the five Phase-5 detector families on reference-battery episodes and
reports variance, saturation, and flag rates — no threshold retuning.
"""

from __future__ import annotations

import statistics
from pathlib import Path
from typing import Any

from ..oracle_only.calibration import WEAK_AGENT
from ..oracle_only.detectors import DETECTOR_FAMILIES, build_audit_view, run_all_detectors
from .ecology_complexity import V3_REFERENCE_T, run_reference_episodes

DETECTOR_TIER = "deep"
DETECTOR_FLAG_THRESHOLD = 0.5


def _summarize_scores(scores: list[float]) -> dict[str, Any]:
    if not scores:
        return {
            "n": 0,
            "min": None,
            "max": None,
            "mean": None,
            "std": None,
            "n_unique_rounded": 0,
            "n_exact_zero": 0,
            "n_saturated_one": 0,
            "n_flagged": 0,
            "flag_rate": 0.0,
            "zero_variance": True,
        }
    rounded = [round(s, 6) for s in scores]
    unique = set(rounded)
    return {
        "n": len(scores),
        "min": min(scores),
        "max": max(scores),
        "mean": statistics.mean(scores),
        "std": statistics.pstdev(scores) if len(scores) > 1 else 0.0,
        "n_unique_rounded": len(unique),
        "n_exact_zero": sum(1 for s in scores if s == 0.0),
        "n_saturated_one": sum(1 for s in scores if s >= 1.0),
        "n_flagged": sum(1 for s in scores if s >= DETECTOR_FLAG_THRESHOLD),
        "flag_rate": sum(1 for s in scores if s >= DETECTOR_FLAG_THRESHOLD) / len(scores),
        "zero_variance": len(unique) == 1,
    }


def run_detector_coverage_battery(
    ecology_path: Path | str,
    *,
    seeds: tuple[int, ...] | None = None,
    tier: str = DETECTOR_TIER,
    backend=None,
    progress: bool = True,
) -> dict[str, Any]:
    """Score reference episodes; summarize each detector family."""
    ecology_path = Path(ecology_path)
    if seeds is None:
        from .ecology_complexity import C3_SEEDS

        seeds = C3_SEEDS
    results = run_reference_episodes(
        ecology_path, backend=backend, seeds=seeds, progress=progress
    )
    per_family: dict[str, list[float]] = {name: [] for name in DETECTOR_FAMILIES}
    per_episode: list[dict[str, float]] = []
    for result in results:
        scores = run_all_detectors(build_audit_view(result, tier))
        per_episode.append(dict(scores))
        for name, value in scores.items():
            per_family[name].append(float(value))

    families = {name: _summarize_scores(values) for name, values in per_family.items()}
    n_zero_variance = sum(1 for summary in families.values() if summary["zero_variance"])
    n_always_zero = sum(
        1
        for summary in families.values()
        if summary["n"] and summary["n_exact_zero"] == summary["n"]
    )
    return {
        "ecology_path": str(ecology_path),
        "agent_type": WEAK_AGENT,
        "T": V3_REFERENCE_T,
        "tier": tier,
        "n_episodes": len(results),
        "seeds": list(seeds),
        "flag_threshold": DETECTOR_FLAG_THRESHOLD,
        "families": families,
        "n_families_zero_variance": n_zero_variance,
        "n_families_always_zero": n_always_zero,
        "transfer_failure_risk": n_zero_variance > 0 or n_always_zero > 0,
        "episodes": per_episode,
    }
