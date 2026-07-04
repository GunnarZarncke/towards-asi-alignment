#!/usr/bin/env python3
"""Milestone v5 Phase 1 acceptance run.

Samples 30 discovery + 10 held-out goal/tool configurations (pre-registered
protocol in `goal_sim/protocol.py`), runs the battery at both instrumentation
tiers, scores frozen detectors and the frozen top-k MI channels on the
held-out region with no re-fitting, and writes
`results/phase1_acceptance.{json,md}`. Both transfer and failure-to-transfer
are reported as results.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from goal_sim.protocol import (
    EPISODE_SEEDS,
    TIERS,
    aggregate,
    mini_mi_scan,
    run_battery,
    sample_configs,
)

RESULTS_DIR = Path(__file__).parent / "results"


def main() -> None:
    discovery_cfgs, held_out_cfgs = sample_configs()
    t0 = time.perf_counter()
    discovery_records = run_battery(discovery_cfgs)
    held_out_records = run_battery(held_out_cfgs)
    elapsed = time.perf_counter() - t0
    n_episodes = len(discovery_records) + len(held_out_records)
    ms_per_episode = 1000.0 * elapsed / n_episodes

    report = {
        "protocol": {
            "n_discovery_configs": len(discovery_cfgs),
            "n_held_out_configs": len(held_out_cfgs),
            "episode_seeds": list(EPISODE_SEEDS),
            "tiers": list(TIERS),
            "held_out_region": "task>=0.45 and compliance<=0.15 and shadow_route",
            "thresholds_frozen_before_run": True,
        },
        "timing": {
            "total_seconds": round(elapsed, 2),
            "ms_per_episode": round(ms_per_episode, 2),
            "n_episodes": n_episodes,
        },
        "discovery": aggregate(discovery_records),
        "held_out": aggregate(held_out_records),
        "mi_scan": mini_mi_scan(discovery_records, held_out_records),
    }

    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "phase1_acceptance.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    (RESULTS_DIR / "phase1_acceptance.md").write_text(render_md(report))
    print(json.dumps(report["discovery"], indent=2))
    print(json.dumps(report["held_out"], indent=2))
    print(f"episodes: {n_episodes}  ms/episode: {ms_per_episode:.2f}")
    print(f"wrote {RESULTS_DIR / 'phase1_acceptance.json'}")


def render_md(report: dict) -> str:
    lines = [
        "# Phase 1 acceptance — goal-agent simulation",
        "",
        "Pre-registered protocol: see `goal_sim/protocol.py` docstring. "
        "Detector/label thresholds frozen before this run; held-out region "
        f"= `{report['protocol']['held_out_region']}`.",
        "",
        f"Episodes: {report['timing']['n_episodes']} "
        f"({report['timing']['ms_per_episode']} ms/episode).",
        "",
        "| group | tier | n | violation rate | detection | false-pass | false-alarm |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for group in ("discovery", "held_out"):
        agg = report[group]
        for tier, stats in agg["tiers"].items():
            lines.append(
                f"| {group} | {tier} | {agg['n_episodes']} "
                f"| {agg['violation_rate']} | {stats['detection_rate']} "
                f"| {stats['false_pass_rate']} | {stats['false_alarm_rate']} |"
            )
    lines += [
        "",
        "## Label causes",
        "",
        f"- discovery: {report['discovery']['label_causes']}",
        f"- held_out: {report['held_out']['label_causes']}",
        "",
        "## Detector fire counts",
        "",
    ]
    for group in ("discovery", "held_out"):
        for tier, stats in report[group]["tiers"].items():
            lines.append(f"- {group}/{tier}: {stats['detector_fire_counts']}")
    mi = report["mi_scan"]
    lines += [
        "",
        "## Mini MI scan (frozen top-k transfer)",
        "",
        f"- frozen top-{len(mi['frozen_top_k'])} (selected on discovery only): "
        f"{mi['frozen_top_k']}",
        f"- discovery scores: { {k: mi['discovery_scores'][k] for k in mi['frozen_top_k']} }",
        f"- held-out scores (same channels, no re-selection): "
        f"{mi['held_out_scores_for_frozen']}",
        f"- held-out label entropy: {mi['held_out_label_entropy_bits']} bits"
        + (
            " — **transfer test degenerate**: the pre-registered held-out"
            " region is (near-)single-label, so MI against its label is zero"
            " for every channel by construction; this measures the region"
            " choice, not the channels."
            if mi["held_out_transfer_degenerate"]
            else ""
        ),
        "",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
