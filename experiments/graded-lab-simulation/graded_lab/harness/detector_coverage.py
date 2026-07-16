"""PLAN_v3 slice D item 6: frozen-detector coverage on v3 reference episodes.

Runs the five Phase-5 detector families on reference-battery episodes and
reports variance, saturation, and flag rates — no threshold retuning.

Pre-registration split (GL-63):
- ``honest_reference_sparse_detectors`` — report-only on the honest integrated
  reference battery (benign ``WEAK_AGENT``; expected silence on some families).
- ``machinery_transfer_verified`` — blocking for Q1 machinery-transfer claims;
  evaluated by ``evaluate_supplementary_detector_gate`` (GL-60), not this module.
"""

from __future__ import annotations

import statistics
from pathlib import Path
from typing import Any

from ..oracle_only.calibration import WEAK_AGENT
from ..oracle_only.detectors import DETECTOR_FAMILIES, build_audit_view, run_all_detectors
from ..world_visible.config import EpisodeConfig
from ..world_visible.substrate import load_substrate

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


def honest_reference_sparse_detectors(families: dict[str, dict[str, Any]]) -> bool:
    """Report-only: any family has zero variance or is always 0.0 on this battery.

    Expected on the honest integrated reference (benign ``WEAK_AGENT`` episodes).
    Does **not** mean frozen detectors fail to run on v3 — see
    ``machinery_transfer_verified`` in ``supplementary_detector_gate``.
    """
    for summary in families.values():
        if summary.get("zero_variance"):
            return True
        n = summary.get("n") or 0
        if n and summary.get("n_exact_zero") == n:
            return True
    return False


def run_detector_coverage_battery(
    ecology_path: Path | str,
    *,
    seeds: tuple[int, ...] | None = None,
    tier: str = DETECTOR_TIER,
    backend=None,
    progress: bool = True,
    programs: dict[str, str] | None = None,
    behavior_profiles: dict[str, dict[str, object]] | None = None,
    episode_config: EpisodeConfig | None = None,
) -> dict[str, Any]:
    """Score reference episodes; summarize each detector family."""
    from ..harness.isolate import MockIsolate
    from ..world_visible.ecology_agents import (
        programs_and_profiles_for_roster,
        reference_roster_from_ecology,
    )
    from ..world_visible.world import run_episode
    from .ecology_complexity import _reference_episode_config

    ecology_path = Path(ecology_path)
    if seeds is None:
        from .ecology_complexity import C3_SEEDS

        seeds = C3_SEEDS
    backend = backend or MockIsolate()
    ecology_data = load_substrate(ecology_path).data
    cfg = episode_config or _reference_episode_config(ecology_data, ecology_path=ecology_path)
    roster = reference_roster_from_ecology(ecology_data, agent_type=WEAK_AGENT, temperature=0.35)
    if programs is None:
        programs, profiles = programs_and_profiles_for_roster(
            roster, ecology_data=ecology_data
        )
    else:
        profiles = behavior_profiles if behavior_profiles is not None else {}
    results = []
    for i, seed in enumerate(seeds):
        if progress:
            print(f"[detector-coverage {i + 1}/{len(seeds)}] seed={seed}", flush=True)
        results.append(
            run_episode(cfg, seed, backend, programs=programs, behavior_profiles=profiles)
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
        "T": cfg.T,
        "tier": tier,
        "n_episodes": len(results),
        "seeds": list(seeds),
        "flag_threshold": DETECTOR_FLAG_THRESHOLD,
        "families": families,
        "n_families_zero_variance": n_zero_variance,
        "n_families_always_zero": n_always_zero,
        "honest_reference_sparse_detectors": honest_reference_sparse_detectors(families),
        "episodes": per_episode,
    }
