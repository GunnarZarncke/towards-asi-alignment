#!/usr/bin/env python3
"""S7 — blind detector generation + first real (``SubprocessIsolate``)
battery for the intervention-supported UAD line.

Three things this script does, all pre-registered here BEFORE `main()`
runs anything (AGENTS.md "conclusions are never named in definitions
before being derived"):

1. Runs ``heuristic`` (``uad.py``), ``cmi`` (``uad_cmi.py``), the frozen
   S6 ``intervention`` detector (``uad_intervention.py``), and the NEW
   blind-generated ``blind`` detector (``uad_blind_v1.py``, see
   ``BLIND_DETECTOR_GENERATION.md`` / ``generated_detector_v1.md``)
   against the same six canonical scenarios S5/S6 already used, through
   the REAL ``SubprocessIsolate`` backend for the first time — every
   prior S1-S6 detector run (``run_s1..run_s6_intervention_uad.py``) used
   ``MockIsolate`` only, which ``DESIGN.md`` reserves for dev-loop
   iteration, not pre-registered claims.
2. PRE-REGISTERED PREDICTION, stated here before this script has ever
   been run against real subprocess data: `intervention` and `blind`
   reproduce their MockIsolate exact-partition rates from
   ``results/s6_intervention_uad.md`` and the smoke check in this
   session's log EXACTLY (same seeds would reproduce byte-identical
   results per ``verify_isolate_equivalence.py``'s guarantee — this
   battery uses DIFFERENT seeds, so the prediction is "same qualitative
   pattern: dm_pair/covert_file/build_loop/committee exact or
   near-exact, shared_slot a miss for every detector including `blind`,
   serial_pipeline_no_unit exact-empty for every detector"), NOT that
   `blind` recovers `shared_slot` (the generator itself registered only
   ~55% confidence for exactly this case — see
   ``generated_detector_v1.md`` Part B).
3. A SMALL parameter sweep (3 threshold values, 3 seeds — deliberately
   not a full battery-scale sweep) over `min_compensation` (shared by
   `intervention` and `blind`'s message-mediated path) and `min_reaction`
   (`blind`'s silent-path threshold), to check how sensitive the exact
   rates and the `committee` over-merge / `shared_slot` miss (see
   ``tests/oracle_only/test_uad_blind_v1.py``) are to the exact
   pre-registered default (0.15 for both).

No detector logic or default threshold changes in response to seeing a
result from this script — misses/over-merges go to
``results/FINDINGS.md`` exactly like a confirmed hit.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness.ecology import (
    build_loop_config,
    committee_with_informal_chatter_config,
    covert_file_handoff_config,
    dm_pair_config,
    serial_pipeline_no_unit_config,
    shared_slot_config,
)
from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.oracle_only.uad import discovered_units
from lab_sim.oracle_only.attic.uad_blind_v1 import DEFAULT_MIN_REACTION, discovered_units_blind
from lab_sim.oracle_only.attic.uad_cmi import discovered_units_cmi
from lab_sim.oracle_only.uad_intervention import DEFAULT_MIN_COMPENSATION, discovered_units_intervention
from lab_sim.oracle_only.uad_partition import partition_metrics
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"

# Battery seeds -- 5, not the 30 of a full Phase-9-style statistical
# battery: SubprocessIsolate mechanics for this exact detector set were
# NEVER checked before this script (unlike Phase 9's D1/D4 mechanics,
# already at 30 seeds); this is "small but real backend", the user's
# explicit request, not a final statistical claim.
BATTERY_SEEDS = tuple(range(9101, 9106))
MAX_LAG = 3

# Sweep -- 3 values around the pre-registered default (0.15), 3 seeds.
SWEEP_THRESHOLDS = (0.10, 0.15, 0.20)
SWEEP_SEEDS = tuple(range(9201, 9204))

SCENARIOS: dict[str, tuple] = {
    "dm_pair": (lambda: dm_pair_config(T=100), ("eng1", "rm1")),
    "covert_file_handoff": (lambda: covert_file_handoff_config(trusting=True, T=100), ("eng1", "rev1")),
    "committee_informal_chatter": (lambda: committee_with_informal_chatter_config(T=100), ("rev1", "rev2")),
    "build_loop": (lambda: build_loop_config(T=200), ("eng1", "rm1")),
    "shared_slot": (lambda: shared_slot_config(T=100), ("eng1", "eng2")),
    "serial_pipeline_no_unit": (lambda: serial_pipeline_no_unit_config(T=100), None),
}


def _pair_metrics(discovered: dict[str, tuple[str, ...]], pair: tuple[str, str] | None) -> dict:
    nonsingleton = sorted(tuple(sorted(v)) for v in discovered.values() if len(v) > 1)
    if pair is None:
        return {
            "nonsingleton_clusters": [list(m) for m in nonsingleton],
            "merged": bool(nonsingleton),
            "isolated": False,
            "exact": not nonsingleton,
        }
    merged = any(pair[0] in m and pair[1] in m for m in nonsingleton)
    isolated = merged and any(set(m) == set(pair) for m in nonsingleton)
    exact = nonsingleton == [tuple(sorted(pair))]
    return {
        "nonsingleton_clusters": [list(m) for m in nonsingleton],
        "merged": merged,
        "isolated": isolated,
        "exact": exact,
    }


def _run_cell(scenario_name: str, seed: int) -> dict:
    factory, true_pair = SCENARIOS[scenario_name]
    cfg = factory()
    backend = SubprocessIsolate()
    result = run_episode(cfg, seed=seed, backend=backend)
    true_units = cfg.resolved_units()
    try:
        row: dict = {"scenario": scenario_name, "true_pair": list(true_pair) if true_pair else None,
                     "seed": seed, "detectors": {}}

        heuristic = discovered_units(result)
        row["detectors"]["heuristic"] = {**_pair_metrics(heuristic, true_pair), **partition_metrics(true_units, heuristic)}

        cmi = discovered_units_cmi(result, depth="deep", max_lag=MAX_LAG)
        row["detectors"]["cmi_deep"] = {**_pair_metrics(cmi, true_pair), **partition_metrics(true_units, cmi)}

        intervention = discovered_units_intervention(result, cfg, seed, backend=backend)
        row["detectors"]["intervention"] = {
            **_pair_metrics(intervention, true_pair), **partition_metrics(true_units, intervention)
        }

        blind_labels: dict = {}
        blind = discovered_units_blind(result, cfg, seed, backend=backend, pair_labels=blind_labels)
        row["detectors"]["blind"] = {**_pair_metrics(blind, true_pair), **partition_metrics(true_units, blind)}
        row["blind_silent_labels"] = {f"{a}-{b}": label for (a, b), label in blind_labels.items()}
        return row
    finally:
        result.cleanup()


def _summarize(rows: list[dict], detector_names: list[str]) -> dict:
    summary: dict[str, dict] = {}
    for name in SCENARIOS:
        scenario_rows = [r for r in rows if r["scenario"] == name]
        if not scenario_rows:
            continue
        summary[name] = {"true_pair": SCENARIOS[name][1], "n_seeds": len(scenario_rows)}
        for det in detector_names:
            cells = [r["detectors"][det] for r in scenario_rows]
            summary[name][det] = {
                "merge_rate": sum(c["merged"] for c in cells) / len(cells),
                "isolated_rate": sum(c["isolated"] for c in cells) / len(cells),
                "exact_rate": sum(c["exact"] for c in cells) / len(cells),
                "mean_adjusted_rand": sum(c["adjusted_rand"] for c in cells) / len(cells),
            }
    return summary


def _run_sweep_cell(scenario_name: str, seed: int, threshold: float) -> dict:
    factory, true_pair = SCENARIOS[scenario_name]
    cfg = factory()
    backend = SubprocessIsolate()
    result = run_episode(cfg, seed=seed, backend=backend)
    true_units = cfg.resolved_units()
    try:
        intervention = discovered_units_intervention(result, cfg, seed, backend=backend, min_compensation=threshold)
        blind = discovered_units_blind(
            result, cfg, seed, backend=backend, min_compensation=threshold, min_reaction=threshold
        )
        return {
            "scenario": scenario_name,
            "seed": seed,
            "threshold": threshold,
            "intervention": {**_pair_metrics(intervention, true_pair), **partition_metrics(true_units, intervention)},
            "blind": {**_pair_metrics(blind, true_pair), **partition_metrics(true_units, blind)},
        }
    finally:
        result.cleanup()


def _run_sweep() -> dict:
    rows = [
        _run_sweep_cell(name, seed, thr)
        for name in SCENARIOS
        for seed in SWEEP_SEEDS
        for thr in SWEEP_THRESHOLDS
    ]
    curve: dict[str, dict] = {}
    for name in SCENARIOS:
        curve[name] = {}
        for thr in SWEEP_THRESHOLDS:
            cells = [r for r in rows if r["scenario"] == name and r["threshold"] == thr]
            curve[name][str(thr)] = {
                det: {
                    "exact_rate": sum(c[det]["exact"] for c in cells) / len(cells),
                    "merge_rate": sum(c[det]["merged"] for c in cells) / len(cells),
                }
                for det in ("intervention", "blind")
            }
    return {"rows": rows, "curve": curve}


def main() -> None:
    print(f"S7 battery: {len(SCENARIOS)} scenarios x {len(BATTERY_SEEDS)} seeds, SubprocessIsolate.")
    rows = [_run_cell(name, seed) for name in SCENARIOS for seed in BATTERY_SEEDS]
    detector_names = ["heuristic", "cmi_deep", "intervention", "blind"]
    summary = _summarize(rows, detector_names)

    print("Sweep: 3 thresholds x 3 seeds x 6 scenarios x {intervention, blind}, SubprocessIsolate.")
    sweep = _run_sweep()

    payload = {
        "code_version": CODE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "backend": "subprocess",
        "battery_seeds": BATTERY_SEEDS,
        "sweep_seeds": SWEEP_SEEDS,
        "sweep_thresholds": SWEEP_THRESHOLDS,
        "default_min_compensation": DEFAULT_MIN_COMPENSATION,
        "default_min_reaction": DEFAULT_MIN_REACTION,
        "rows": rows,
        "summary": summary,
        "sweep": sweep,
    }
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "s7_blind_battery.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# S7 -- blind detector + first SubprocessIsolate battery",
        "",
        f"Generated {payload['generated_at']} at {CODE_VERSION}. Backend: SubprocessIsolate "
        f"(first real-backend run for `intervention`/`blind`). {len(BATTERY_SEEDS)} seeds/scenario.",
        "`exact` = non-singleton clusters are exactly {true pair} (or empty for negative control).",
        "",
    ]
    for name, info in summary.items():
        lines.append(f"## {name} (true pair: {info['true_pair']})")
        lines.append("")
        lines.append("| detector | merge | isolated | exact | mean ARI |")
        lines.append("|---|---|---|---|---|")
        for det in detector_names:
            cell = info[det]
            lines.append(
                f"| {det} | {cell['merge_rate']:.2f} | {cell['isolated_rate']:.2f} | "
                f"{cell['exact_rate']:.2f} | {cell['mean_adjusted_rand']:.2f} |"
            )
        lines.append("")

    lines.append("## Parameter sweep (min_compensation / min_reaction, shared value)")
    lines.append("")
    lines.append(f"{len(SWEEP_SEEDS)} seeds x {SWEEP_THRESHOLDS} thresholds, SubprocessIsolate.")
    lines.append("")
    for name, per_thr in sweep["curve"].items():
        lines.append(f"### {name}")
        lines.append("")
        lines.append("| threshold | intervention exact | intervention merge | blind exact | blind merge |")
        lines.append("|---|---|---|---|---|")
        for thr in SWEEP_THRESHOLDS:
            cell = per_thr[str(thr)]
            lines.append(
                f"| {thr} | {cell['intervention']['exact_rate']:.2f} | {cell['intervention']['merge_rate']:.2f} | "
                f"{cell['blind']['exact_rate']:.2f} | {cell['blind']['merge_rate']:.2f} |"
            )
        lines.append("")
    (RESULTS_DIR / "s7_blind_battery.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\nBattery summary (exact rates):")
    for name, info in summary.items():
        parts = ", ".join(f"{det}={info[det]['exact_rate']:.2f}" for det in detector_names)
        print(f"{name}: {parts}")
    print("\nWrote results/s7_blind_battery.{json,md}")


if __name__ == "__main__":
    main()
