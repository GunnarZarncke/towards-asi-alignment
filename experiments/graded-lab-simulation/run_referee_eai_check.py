#!/usr/bin/env python3
"""Referee-vantage EAI check (FINDINGS G-19 / DESIGN.md "EAI-referee").

Predict-then-measure companion to the G-18 decomposition: same episodes
(programmatic_softmax agent, 10 seeds x 5 `carrier_load_scale` cells,
`MockIsolate`), but reports the entropy component at the `light` audit
tier (referee vantage: `t`, `actor_id`, `status` only) alongside the
`full` tier (agent vantage, i.e. the EAI-v2 value already reported by
`run_phase7_calibration.py`).

Pre-registered prediction (DESIGN.md "EAI-referee", FINDINGS G-19):
the `light`-tier entropy component will be materially non-zero, even
though the `full`-tier one is ≈0 (FINDINGS G-18). Falsifiable failure
mode: if `light`-tier entropy is also ≈0, the "high band unreachable"
finding extends to the referee's own vantage, not just the agent's.

Usage:
  python3 run_referee_eai_check.py
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.calibration import (
    CALIBRATION_SEEDS,
    CARRIER_SCALES,
    NOMINAL_COMPUTE_SCALE,
    NOMINAL_SPREAD_SCALE,
    STRONG_AGENT,
    config_for_settings,
    programs_for,
)
from graded_lab.oracle_only.eai import eai_components_at_tier, tier_i_fraction_from_log
from graded_lab.world_visible.config import CODE_VERSION, SubstrateSettings
from graded_lab.world_visible.world import run_episode

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "referee_eai_check.json"
TIERS = ("full", "light")

# Two-sided 95% t critical value for df = len(CALIBRATION_SEEDS) - 1 = 9.
# No scipy dependency in this venv; hardcoded standard table value,
# valid only for n=10 seeds (checked below, not silently reused if the
# seed count ever changes).
T_CRIT_95_DF9 = 2.262


def _mean_std_se(values: list[float]) -> tuple[float, float, float]:
    n = len(values)
    mean = sum(values) / n
    if n < 2:
        return mean, 0.0, 0.0
    variance = sum((v - mean) ** 2 for v in values) / (n - 1)
    std = math.sqrt(variance)
    se = std / math.sqrt(n)
    return mean, std, se


def _ci95(values: list[float]) -> dict[str, float]:
    mean, std, se = _mean_std_se(values)
    half_width = T_CRIT_95_DF9 * se
    return {
        "mean": round(mean, 6),
        "std": round(std, 6),
        "se": round(se, 6),
        "ci95_low": round(mean - half_width, 6),
        "ci95_high": round(mean + half_width, 6),
    }


def _paired_diff_ci95(a: list[float], b: list[float]) -> dict[str, float]:
    """Paired difference a - b, paired by seed index (same seed set used
    at every cell). More power than an unpaired comparison here, since
    per-seed episode idiosyncrasies (FINDINGS G-16/G-17's "single seed
    flip" caveat) are common to both cells being compared."""
    diffs = [x - y for x, y in zip(a, b)]
    stats = _ci95(diffs)
    stats["zero_in_ci95"] = stats["ci95_low"] <= 0.0 <= stats["ci95_high"]
    return stats


def main() -> None:
    backend = MockIsolate()
    programs = programs_for(STRONG_AGENT)
    by_cell: dict[float, dict[str, dict[str, list[float]]]] = {}
    total = len(CARRIER_SCALES) * len(CALIBRATION_SEEDS)
    done = 0
    t0 = time.perf_counter()

    for carrier_load_scale in CARRIER_SCALES:
        settings = SubstrateSettings(
            compute_scale=NOMINAL_COMPUTE_SCALE,
            population_spread_scale=NOMINAL_SPREAD_SCALE,
            carrier_load_scale=carrier_load_scale,
        )
        cfg = config_for_settings(settings)
        by_tier: dict[str, dict[str, list[float]]] = {
            tier: {"entropy": [], "margin_density": [], "tier_i_load": [], "composite": []}
            for tier in TIERS
        }
        for seed in CALIBRATION_SEEDS:
            done += 1
            print(
                f"[referee-eai {done}/{total}] carrier_load={carrier_load_scale} "
                f"agent={STRONG_AGENT} seed={seed}"
            )
            result = run_episode(cfg, seed, backend, programs=programs)
            tier_i_fraction = tier_i_fraction_from_log(result.primitive_log)
            for tier in TIERS:
                components = eai_components_at_tier(
                    result.primitive_log, result.decision_margins, tier_i_fraction, tier,
                )
                for key, value in components.items():
                    by_tier[tier][key].append(value)
                by_tier[tier]["composite"].append(sum(components.values()) / 3.0)
        by_cell[carrier_load_scale] = by_tier

    wall = round(time.perf_counter() - t0, 2)
    assert len(CALIBRATION_SEEDS) == 10, (
        "T_CRIT_95_DF9 is hardcoded for n=10 seeds; update it if this changes"
    )

    def _stats_row(by_tier: dict[str, dict[str, list[float]]]) -> dict[str, dict[str, dict[str, float]]]:
        return {
            tier: {key: _ci95(values) for key, values in components.items()}
            for tier, components in by_tier.items()
        }

    # Paired (by-seed) differences in light-tier entropy between each
    # cell and the next, to check whether the non-monotonic dip at the
    # highest-stress cell could plausibly be seed noise (FINDINGS
    # G-20's open question, per this session's request).
    ordered_cells = sorted(by_cell)
    light_entropy_by_cell = {cell: by_cell[cell]["light"]["entropy"] for cell in ordered_cells}
    paired_diffs: dict[str, dict[str, float]] = {}
    for a, b in zip(ordered_cells, ordered_cells[1:]):
        paired_diffs[f"{a}->{b}"] = _paired_diff_ci95(
            light_entropy_by_cell[a], light_entropy_by_cell[b]
        )

    report = {
        "code_version": CODE_VERSION,
        "agent_type": STRONG_AGENT,
        "seeds": list(CALIBRATION_SEEDS),
        "carrier_load_scales": list(CARRIER_SCALES),
        "wall_seconds": wall,
        "raw_light_tier_entropy_by_cell": {
            str(cell): values for cell, values in light_entropy_by_cell.items()
        },
        "stats_by_tier_and_cell": {
            str(cell): _stats_row(by_tier) for cell, by_tier in by_cell.items()
        },
        "paired_diff_light_entropy_consecutive_cells": paired_diffs,
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"[referee-eai] wrote {RESULTS_PATH}")
    print(f"[referee-eai] wall {wall}s")
    print("[referee-eai] entropy component by cell, mean [95% CI] (full vs light tier):")
    for cell in CARRIER_SCALES:
        row = report["stats_by_tier_and_cell"][str(cell)]
        full = row["full"]["entropy"]
        light = row["light"]["entropy"]
        print(
            f"  carrier_load={cell}: "
            f"full={full['mean']} [{full['ci95_low']}, {full['ci95_high']}]  "
            f"light={light['mean']} [{light['ci95_low']}, {light['ci95_high']}]"
        )

    print("[referee-eai] paired (by-seed) consecutive-cell differences in light-tier entropy:")
    for pair, stats in paired_diffs.items():
        sig = "differs from 0 at p<0.05" if not stats["zero_in_ci95"] else "0 inside 95% CI — NOT distinguishable from noise"
        print(
            f"  {pair}: diff={stats['mean']} [{stats['ci95_low']}, {stats['ci95_high']}] -> {sig}"
        )

    full_entropy_max = max(row["full"]["entropy"]["mean"] for row in report["stats_by_tier_and_cell"].values())
    light_entropy_max = max(row["light"]["entropy"]["mean"] for row in report["stats_by_tier_and_cell"].values())
    light_composite_by_cell = {
        cell: sum(report["stats_by_tier_and_cell"][str(cell)]["light"][k]["mean"] for k in ("entropy", "margin_density", "tier_i_load")) / 3.0
        for cell in CARRIER_SCALES
    }
    light_composite_max = max(light_composite_by_cell.values())
    print(f"[referee-eai] full-tier entropy max across cells: {full_entropy_max}")
    print(f"[referee-eai] light-tier entropy max across cells: {light_entropy_max}")
    print(f"[referee-eai] light-tier composite EAI max across cells: {light_composite_max}")
    if light_entropy_max > 0.02:
        print("[referee-eai] PREDICTION HELD: light-tier entropy is materially non-zero.")
    else:
        print(
            "[referee-eai] PREDICTION FAILED: light-tier entropy is also ~0 — "
            "the referee's coarsest vantage sees a near-degenerate outcome "
            "distribution too. Report honestly, do not adjust the prediction "
            "after the fact."
        )


if __name__ == "__main__":
    main()
