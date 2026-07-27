#!/usr/bin/env python3
"""ET-3 Phase 1: run Phase 6 + D3 under each frozen stress cell.

Pre-registered: ``PLAN_ET3.md``, fixture ``external/ai2027/fixtures/schedule_et3.yaml``.
Outputs: ``results/et3_phase1_<cell>.{json,md}`` and ``results/et3_phase1_summary.{json,md}``.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runners._paths import EXTERNAL_DIR, LAB_SIM_ROOT, REPO_ROOT, RESULTS_DIR

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.external.ai2027_adapter import (
    ET3_PROTOCOL_VERSION,
    apply_d3_episode_t,
    d3_overrides_for_cell,
    get_stress_cell,
    list_cell_ids,
    sample_phase6_configs,
)
from lab_sim.harness import protocol
from lab_sim.harness.d3_population import (
    D3_N_GENERATIONS,
    D3_POPULATION_SIZE,
    run_population_loop,
    sample_initial_population,
    trajectory_to_dict,
)
from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.world_visible.config import CODE_VERSION

PHASE6_WALL_CEILING_S = 600.0
PHASE6_SUBSAMPLE_DISCOVERY = 12
PHASE6_SUBSAMPLE_HELD_OUT = 6


def _run_phase6_cell(cell_id: str, timings: list) -> dict:
    cell = get_stress_cell(cell_id)
    discovery, held_out = sample_phase6_configs(cell_id)
    n_pairs = (len(discovery) + len(held_out)) * len(protocol.EPISODE_SEEDS)
    print(
        f"[et3/p6/{cell_id}] {len(discovery)} discovery + {len(held_out)} held-out × "
        f"{len(protocol.EPISODE_SEEDS)} seeds = {n_pairs} pairs"
    )
    t0 = time.perf_counter()

    def _run_group(label: str, configs) -> list[dict]:
        records = protocol.run_battery(configs, seeds=protocol.EPISODE_SEEDS, isolate_ledger_records=timings)
        for r in records:
            r["group"] = label
            r["stress_cell"] = cell_id
        return records

    discovery_records = _run_group("discovery", discovery)
    held_out_records = _run_group("held_out", held_out)
    wall = time.perf_counter() - t0
    subsampled = False
    if wall > PHASE6_WALL_CEILING_S:
        print(f"[et3/p6/{cell_id}] wall {wall:.1f}s > ceiling — subsampling")
        subsampled = True
        discovery, held_out = sample_phase6_configs(
            cell_id,
            n_discovery=PHASE6_SUBSAMPLE_DISCOVERY,
            n_held_out=PHASE6_SUBSAMPLE_HELD_OUT,
        )
        discovery_records = _run_group("discovery", discovery)
        held_out_records = _run_group("held_out", held_out)
        wall = time.perf_counter() - t0

    all_records = discovery_records + held_out_records
    agg = {
        "discovery": protocol.aggregate(discovery_records),
        "held_out": protocol.aggregate(held_out_records),
        "all": protocol.aggregate(all_records),
    }
    print(f"[et3/p6/{cell_id}] done in {wall:.1f}s")
    return {
        "cell_id": cell_id,
        "ai2027_cue": cell.ai2027_cue,
        "wall_seconds": wall,
        "subsampled": subsampled,
        "n_discovery": len(discovery),
        "n_held_out": len(held_out),
        "aggregate": agg,
        "records": all_records,
    }


def _run_d3_cell(cell_id: str) -> dict:
    overrides = d3_overrides_for_cell(cell_id)
    cell = get_stress_cell(cell_id)
    configs = apply_d3_episode_t(sample_initial_population(), overrides["episode_t"])
    print(
        f"[et3/d3/{cell_id}] pop={D3_POPULATION_SIZE} gen={D3_N_GENERATIONS} "
        f"selection={overrides['selection_strength']} T={overrides['episode_t']}"
    )
    t0 = time.perf_counter()
    traj = run_population_loop(
        configs,
        n_generations=D3_N_GENERATIONS,
        backend_factory=SubprocessIsolate,
        selection_strength=overrides["selection_strength"],
    )
    wall = time.perf_counter() - t0
    payload = trajectory_to_dict(traj)
    gens = payload["generations"]
    print(
        f"[et3/d3/{cell_id}] done in {wall:.1f}s; "
        f"cp mass {gens[0]['correction_preserving_mass_share']:.3f} → "
        f"{gens[-1]['correction_preserving_mass_share']:.3f}"
    )
    payload["meta"] = {
        "stress_cell": cell_id,
        "ai2027_cue": cell.ai2027_cue,
        "wall_seconds": wall,
        "backend": "SubprocessIsolate",
    }
    return payload


def _phase6_md(cell_result: dict) -> str:
    agg = cell_result["aggregate"]["all"]
    lines = [
        f"# ET-3 Phase 6 — cell `{cell_result['cell_id']}`",
        "",
        f"cue: {cell_result['ai2027_cue']}. Wall: {cell_result['wall_seconds']:.1f}s.",
        "",
        "| tier | mean detector | Spearman vs oracle |",
        "|---|---:|---:|",
    ]
    for tier in protocol.TIERS:
        t = agg["tiers"][tier]
        lines.append(
            f"| {tier} | {t['mean_detector_composite']} | {t['spearman_vs_oracle_severity']} |"
        )
    return "\n".join(lines) + "\n"


def _d3_md(d3_result: dict) -> str:
    gens = d3_result["generations"]
    cell = d3_result["meta"]["stress_cell"]
    lines = [
        f"# ET-3 D3 — cell `{cell}`",
        "",
        f"Wall: {d3_result['meta']['wall_seconds']:.1f}s.",
        "",
        "| gen | correction-preserving mass | weighted severity |",
        "|---:|---:|---:|",
    ]
    for g in gens:
        lines.append(
            f"| {g['generation']} | {g['correction_preserving_mass_share']:.3f} | "
            f"{g['weighted_mean_severity']:.4f} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="ET-3 Phase 1 batteries")
    parser.add_argument(
        "--cells",
        nargs="*",
        default=list(list_cell_ids()),
        help="stress cells to run (default: all frozen cells)",
    )
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timings: list = []
    summary: dict = {
        "et3_protocol_version": ET3_PROTOCOL_VERSION,
        "code_version": CODE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cells": {},
    }

    for i, cell_id in enumerate(args.cells, start=1):
        print(f"[et3] [{i}/{len(args.cells)}] cell={cell_id}")
        p6 = _run_phase6_cell(cell_id, timings)
        d3 = _run_d3_cell(cell_id)
        cell_out = {"phase6": p6, "d3": d3}
        summary["cells"][cell_id] = {
            "phase6": {
                "wall_seconds": p6["wall_seconds"],
                "subsampled": p6["subsampled"],
                "deep_spearman": p6["aggregate"]["all"]["tiers"]["deep"]["spearman_vs_oracle_severity"],
                "light_spearman": p6["aggregate"]["all"]["tiers"]["light"]["spearman_vs_oracle_severity"],
            },
            "d3": {
                "wall_seconds": d3["meta"]["wall_seconds"],
                "cp_mass_first": d3["generations"][0]["correction_preserving_mass_share"],
                "cp_mass_last": d3["generations"][-1]["correction_preserving_mass_share"],
                "weighted_severity_last": d3["generations"][-1]["weighted_mean_severity"],
            },
        }
        json_path = RESULTS_DIR / f"et3_phase1_{cell_id}.json"
        json_path.write_text(json.dumps(cell_out, indent=2), encoding="utf-8")
        md_path = RESULTS_DIR / f"et3_phase1_{cell_id}.md"
        md_path.write_text(_phase6_md(p6) + "\n" + _d3_md(d3), encoding="utf-8")
        print(f"[et3] wrote {json_path.name}")

    summary_path = RESULTS_DIR / "et3_phase1_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (RESULTS_DIR / "et3_phase1_summary.md").write_text(
        f"# ET-3 Phase 1 summary\n\n```json\n{json.dumps(summary, indent=2)}\n```\n",
        encoding="utf-8",
    )
    print(f"[et3] summary -> {summary_path.name}")


if __name__ == "__main__":
    main()
