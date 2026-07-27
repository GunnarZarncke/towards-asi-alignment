#!/usr/bin/env python3
"""Phase 6 — first real battery, run through the real subprocess backend.

Pre-registered protocol: `lab_sim/protocol.py` module docstring.
Blind-generated repertoire: `BLIND_GENERATION.md`,
`lab_sim/generated_playbooks_v1.json`.

Outputs (all under `results/`):
- `phase6_battery.json` — full per-(config, seed) records + aggregates.
- `phase6_battery.md` — human-readable summary.
- appends to `isolate_cost_ledger.json` (via `report_isolate_cost.py`'s
  ledger module) under label `phase6_battery`.

No detector, severity, or tier-projection code is touched by this script —
it only calls the frozen `lab_sim.detectors`/`lab_sim.severity`/`lab_sim.
twins` surfaces and reports on the results (PLAN.md "No re-fitting").
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runners._paths import EXTERNAL_DIR, LAB_SIM_ROOT, REPO_ROOT, RESULTS_DIR

import json
import time
from pathlib import Path

from lab_sim.harness import isolate_cost, protocol
from lab_sim.world_visible.config import CODE_VERSION



def _run_group(label: str, configs, seeds, timings: list) -> list[dict]:
    print(f"[phase6] running {label}: {len(configs)} configs x {len(seeds)} seeds "
          f"= {len(configs) * len(seeds)} (config,seed) pairs, 2 episodes each "
          f"(playbook + honest twin)")
    t0 = time.perf_counter()
    records = protocol.run_battery(configs, seeds=seeds, isolate_ledger_records=timings)
    dt = time.perf_counter() - t0
    print(f"[phase6] {label} done in {dt:.1f}s ({dt / len(records):.3f}s/record)")
    for r in records:
        r["group"] = label
    return records


def _markdown_report(agg_discovery: dict, agg_held_out: dict, agg_all: dict, ledger_entry: dict) -> str:
    lines = [
        "# Phase 6 battery report",
        "",
        f"CODE_VERSION `{CODE_VERSION}`. Protocol: `lab_sim/protocol.py`. "
        f"Repertoire: `lab_sim/generated_playbooks_v1.json` "
        f"(BLIND_GENERATION.md round 1).",
        "",
        f"- discovery configs: {protocol.N_DISCOVERY}, held-out configs: "
        f"{protocol.N_HELD_OUT}, seeds/config: {len(protocol.EPISODE_SEEDS)}, "
        f"T={protocol.EPISODE_T}, temperature={protocol.TEMPERATURE}",
        f"- held-out region: engineer normalized compliance weight <= "
        f"{protocol.HELD_OUT_ENGINEER_COMPLIANCE_MAX}",
        "",
        "## Oracle severity + bearer welfare (referee-only ground truth)",
        "",
        "| group | n | mean severity composite | mean bearer health | mean bearer stress |",
        "|---|---|---|---|---|",
    ]
    for label, agg in (("discovery", agg_discovery), ("held_out", agg_held_out), ("all", agg_all)):
        lines.append(
            f"| {label} | {agg['n_episodes']} | {agg['mean_oracle_severity_composite']} "
            f"| {agg['mean_bearer_health']} | {agg['mean_bearer_stress_total']} |"
        )
    lines += [
        "",
        "## Per-tier detector composite, twin gap, and rank-transfer (all configs)",
        "",
        "Detector composite = mean of the five frozen family scores "
        "(report-only aggregate; never fed back into `detectors.py`/"
        "`severity.py`). Twin gap = playbook score minus honest-twin score "
        "per family, averaged over the whole battery (positive = playbook "
        "scored MORE deceptive than its honest twin, as expected).",
        "",
        "| tier | mean detector composite | mean twin composite | "
        "Spearman vs oracle severity |",
        "|---|---|---|---|",
    ]
    for tier in protocol.TIERS:
        t = agg_all["tiers"][tier]
        lines.append(
            f"| {tier} | {t['mean_detector_composite']} | {t['mean_twin_detector_composite']} "
            f"| {t['spearman_vs_oracle_severity']} |"
        )
    lines += ["", "### Twin gap by detector family, per tier", ""]
    fam_names = sorted(agg_all["tiers"]["deep"]["twin_gap_by_family"])
    lines.append("| tier | " + " | ".join(fam_names) + " |")
    lines.append("|---|" + "---|" * len(fam_names))
    for tier in protocol.TIERS:
        gaps = agg_all["tiers"][tier]["twin_gap_by_family"]
        lines.append(f"| {tier} | " + " | ".join(str(gaps[f]) for f in fam_names) + " |")
    lines += [
        "",
        "## Discovery vs. held-out (transfer check, no re-fitting)",
        "",
        "| tier | discovery Spearman | held-out Spearman |",
        "|---|---|---|",
    ]
    for tier in protocol.TIERS:
        lines.append(
            f"| {tier} | {agg_discovery['tiers'][tier]['spearman_vs_oracle_severity']} "
            f"| {agg_held_out['tiers'][tier]['spearman_vs_oracle_severity']} |"
        )
    lines += [
        "",
        "## Isolate cost ledger",
        "",
        f"This run: {len(ledger_entry['timings'])} isolate lifetimes, "
        f"{ledger_entry['total_seconds']}s total "
        f"({ledger_entry['total_seconds'] / max(len(ledger_entry['timings']), 1):.4f}s/isolate-lifetime).",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    discovery, held_out = protocol.sample_configs()

    timings: list = []
    discovery_records = _run_group("discovery", discovery, protocol.EPISODE_SEEDS, timings)
    held_out_records = _run_group("held_out", held_out, protocol.EPISODE_SEEDS, timings)
    all_records = discovery_records + held_out_records

    agg_discovery = protocol.aggregate(discovery_records)
    agg_held_out = protocol.aggregate(held_out_records)
    agg_all = protocol.aggregate(all_records)

    ledger = isolate_cost.append_ledger(timings, label="phase6_battery")
    ledger_entry = ledger["entries"][-1]

    out = {
        "code_version": CODE_VERSION,
        "sampling_seed": protocol.SAMPLING_SEED,
        "n_discovery": protocol.N_DISCOVERY,
        "n_held_out": protocol.N_HELD_OUT,
        "episode_seeds": list(protocol.EPISODE_SEEDS),
        "records": all_records,
        "aggregate": {"discovery": agg_discovery, "held_out": agg_held_out, "all": agg_all},
        "isolate_cost_this_run": ledger_entry,
    }
    (RESULTS_DIR / "phase6_battery.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    (RESULTS_DIR / "phase6_battery.md").write_text(
        _markdown_report(agg_discovery, agg_held_out, agg_all, ledger_entry), encoding="utf-8"
    )
    print("[phase6] wrote results/phase6_battery.json and results/phase6_battery.md")
    print(f"[phase6] isolate cost: {ledger_entry['total_seconds']}s over "
          f"{len(ledger_entry['timings'])} isolate lifetimes "
          f"(cumulative ledger: {ledger['cumulative_seconds']}s)")


if __name__ == "__main__":
    main()
