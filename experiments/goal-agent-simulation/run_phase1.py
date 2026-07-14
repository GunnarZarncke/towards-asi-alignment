#!/usr/bin/env python3
"""Milestone v5 Phase 1 acceptance run (+ GA-1/GA-6 follow-ups: regions 2 & 3).

Samples 30 discovery + 10 held-out-high-deception goal/tool configurations
(pre-registered protocol in `goal_sim/protocol.py`), runs the battery at both
instrumentation tiers, scores frozen detectors and the frozen top-k MI
channels on the held-out region with no re-fitting, and writes
`results/phase1_acceptance.{json,md}`. Both transfer and failure-to-transfer
are reported as results.

Also scores two more independently-sampled held-out regions against the
SAME frozen detector thresholds and the SAME frozen top-k channel selection
from region 1's run (no re-fitting on any region):

- **Region 2** ("subtle deception band"): pre-registered after region 1
  saturated at 100% violations (`results/FINDINGS.md` GA-1).
- **Region 3** ("compliance band"): pre-registered after region 2 *also*
  saturated, this time root-caused to a simplex-geometry effect (GA-6) —
  region 3 constrains `compliance` directly instead of letting it fall out
  incidentally from other constraints.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from goal_sim.protocol import (
    EPISODE_SEEDS,
    TIERS,
    aggregate,
    mi_transfer_on_frozen,
    mini_mi_scan,
    run_battery,
    sample_configs,
    sample_held_out_compliance_band,
    sample_held_out_subtle,
)

RESULTS_DIR = Path(__file__).parent / "results"

HELD_OUT_REGIONS = {
    "held_out_high_deception": (
        "task>=0.45 and compliance<=0.15 and shadow_route",
        sample_configs,  # special-cased below (also returns discovery)
    ),
    "held_out_subtle": (
        "0.30<=task<=0.45 and exposure>=0.35 and shadow_route (GA-1 follow-up)",
        sample_held_out_subtle,
    ),
    "held_out_compliance_band": (
        "0.20<=compliance<=0.35 and shadow_route (GA-6 follow-up)",
        sample_held_out_compliance_band,
    ),
}


def main() -> None:
    discovery_cfgs, held_out_cfgs = sample_configs()
    subtle_cfgs = sample_held_out_subtle()
    compliance_band_cfgs = sample_held_out_compliance_band()

    region_cfgs = {
        "held_out_high_deception": held_out_cfgs,
        "held_out_subtle": subtle_cfgs,
        "held_out_compliance_band": compliance_band_cfgs,
    }

    t0 = time.perf_counter()
    discovery_records = run_battery(discovery_cfgs)
    region_records = {
        name: run_battery(cfgs) for name, cfgs in region_cfgs.items()
    }
    elapsed = time.perf_counter() - t0
    n_episodes = len(discovery_records) + sum(
        len(r) for r in region_records.values()
    )
    ms_per_episode = 1000.0 * elapsed / n_episodes

    mi_scan = mini_mi_scan(
        discovery_records, region_records["held_out_high_deception"]
    )
    region_transfers = {
        name: mi_transfer_on_frozen(mi_scan["frozen_top_k"], records)
        for name, records in region_records.items()
        if name != "held_out_high_deception"
    }

    report = {
        "protocol": {
            "n_discovery_configs": len(discovery_cfgs),
            "region_descriptions": {
                name: desc for name, (desc, _) in HELD_OUT_REGIONS.items()
            },
            "n_configs_per_region": {
                name: len(cfgs) for name, cfgs in region_cfgs.items()
            },
            "episode_seeds": list(EPISODE_SEEDS),
            "tiers": list(TIERS),
            "thresholds_frozen_before_run": True,
        },
        "timing": {
            "total_seconds": round(elapsed, 2),
            "ms_per_episode": round(ms_per_episode, 2),
            "n_episodes": n_episodes,
        },
        "discovery": aggregate(discovery_records),
        **{name: aggregate(records) for name, records in region_records.items()},
        "mi_scan": mi_scan,
        "mi_scan_region_transfer": region_transfers,
    }

    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "phase1_acceptance.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    (RESULTS_DIR / "phase1_acceptance.md").write_text(render_md(report))
    for group in ["discovery", *region_records.keys()]:
        print(f"--- {group} ---")
        print(json.dumps(report[group], indent=2))
    print(f"episodes: {n_episodes}  ms/episode: {ms_per_episode:.2f}")
    print(f"wrote {RESULTS_DIR / 'phase1_acceptance.json'}")


def render_md(report: dict) -> str:
    region_names = list(report["protocol"]["region_descriptions"])
    groups = ["discovery", *region_names]
    lines = [
        "# Phase 1 acceptance — goal-agent simulation",
        "",
        "Pre-registered protocol: see `goal_sim/protocol.py` docstring. "
        "Detector/label thresholds frozen before this run.",
    ]
    for name, desc in report["protocol"]["region_descriptions"].items():
        lines.append(f"- `{name}`: `{desc}`")
    lines += [
        "",
        f"Episodes: {report['timing']['n_episodes']} "
        f"({report['timing']['ms_per_episode']} ms/episode).",
        "",
        "| group | tier | n | violation rate | detection | false-pass | false-alarm |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for group in groups:
        agg = report[group]
        for tier, stats in agg["tiers"].items():
            lines.append(
                f"| {group} | {tier} | {agg['n_episodes']} "
                f"| {agg['violation_rate']} | {stats['detection_rate']} "
                f"| {stats['false_pass_rate']} | {stats['false_alarm_rate']} |"
            )
    lines += ["", "## Label causes", ""]
    for group in groups:
        lines.append(f"- {group}: {report[group]['label_causes']}")
    lines += ["", "## Detector fire counts", ""]
    for group in groups:
        for tier, stats in report[group]["tiers"].items():
            lines.append(f"- {group}/{tier}: {stats['detector_fire_counts']}")
    mi = report["mi_scan"]
    lines += [
        "",
        "## Mini MI scan (frozen top-k, region 1 selection + transfer)",
        "",
        f"- frozen top-{len(mi['frozen_top_k'])} (selected on discovery only): "
        f"{mi['frozen_top_k']}",
        f"- discovery scores: { {k: mi['discovery_scores'][k] for k in mi['frozen_top_k']} }",
        f"- region 1 scores (same channels, no re-selection): "
        f"{mi['held_out_scores_for_frozen']}",
        f"- region 1 label entropy: {mi['held_out_label_entropy_bits']} bits"
        + (
            " — **transfer test degenerate**."
            if mi["held_out_transfer_degenerate"]
            else ""
        ),
        "",
        "## Mini MI scan — regions 2 & 3 transfer, same frozen top-k",
        "",
    ]
    for name, transfer in report["mi_scan_region_transfer"].items():
        lines.append(
            f"- {name}: scores {transfer['scores_for_frozen']}, "
            f"label entropy {transfer['label_entropy_bits']} bits"
            + (" (transfer test degenerate)" if transfer["transfer_degenerate"] else "")
        )
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
