#!/usr/bin/env python3
"""S6 first step — the custom actor-level conditional-MI detector
(`uad_cmi.discovered_units_cmi`, the G-26 "easy fixes") run against the
SAME five scenarios and metrics as `run_s5_deep_trace_sweep.py`, side
by side with the vendored detector it is meant to replace and the
frozen heuristic.

NOT a battery (same exploratory MockIsolate status as the S5 scripts).
Detector parameters are the module defaults, chosen before this sweep
was run (see `uad_cmi.py`'s pre-registration note) — whatever the
sweep yields is reported, including failures.

Success criterion per cell (stricter than S5's `merge_rate` alone,
because G-24/G-25 showed a fully-merged blob trivially "merges" any
pair): the discovered partition's non-singleton clusters are EXACTLY
{the true pair} — the true pair found, isolated, and nothing else
spuriously merged. Reported as `exact_rate`; `merge_rate`/
`isolated_rate` kept for comparability with the S5 tables.
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
    shared_slot_config,
)
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.uad import discovered_units, uad_score
from lab_sim.oracle_only.uad_cmi import discovered_units_cmi
from lab_sim.oracle_only.uad_mi import discovered_units_mi
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"
SEEDS = tuple(range(1, 6))
DEPTHS = ("shallow", "deep")
MAX_LAG = 3
VENDORED_N_AGENTS = 2  # representative mid-sweep value from S5 (result was identical 1-4)

SCENARIOS: dict[str, tuple] = {
    "dm_pair": (lambda: dm_pair_config(T=100), ("eng1", "rm1")),
    "covert_file_handoff": (lambda: covert_file_handoff_config(trusting=True, T=100), ("eng1", "rev1")),
    "committee_informal_chatter": (lambda: committee_with_informal_chatter_config(T=100), ("rev1", "rev2")),
    "build_loop": (lambda: build_loop_config(T=200), ("eng1", "rm1")),
    "shared_slot": (lambda: shared_slot_config(T=100), ("eng1", "eng2")),
}


def _metrics(discovered: dict[str, tuple[str, ...]], pair: tuple[str, str]) -> dict:
    nonsingleton = sorted(tuple(sorted(v)) for v in discovered.values() if len(v) > 1)
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
    result = run_episode(cfg, seed=seed, backend=MockIsolate())
    try:
        row: dict = {"scenario": scenario_name, "true_pair": list(true_pair), "seed": seed, "detectors": {}}
        heuristic = discovered_units(result)
        row["detectors"]["heuristic"] = {
            **_metrics(heuristic, true_pair),
            "uad_score": uad_score(cfg.resolved_units(), heuristic),
        }
        for depth in DEPTHS:
            vendored = discovered_units_mi(result, n_agents=VENDORED_N_AGENTS, max_lag=MAX_LAG, depth=depth)
            row["detectors"][f"vendored_mi_{depth}"] = {
                **_metrics(vendored, true_pair),
                "uad_score": uad_score(cfg.resolved_units(), vendored),
            }
            cmi = discovered_units_cmi(result, depth=depth, max_lag=MAX_LAG)
            row["detectors"][f"cmi_{depth}"] = {
                **_metrics(cmi, true_pair),
                "uad_score": uad_score(cfg.resolved_units(), cmi),
            }
        return row
    finally:
        result.cleanup()


def main() -> None:
    rows = [_run_cell(name, seed) for name in SCENARIOS for seed in SEEDS]
    detector_names = ["heuristic"] + [f"{d}_{depth}" for d in ("vendored_mi", "cmi") for depth in DEPTHS]

    summary: dict[str, dict] = {}
    for name in SCENARIOS:
        scenario_rows = [r for r in rows if r["scenario"] == name]
        summary[name] = {"true_pair": SCENARIOS[name][1]}
        for det in detector_names:
            cells = [r["detectors"][det] for r in scenario_rows]
            summary[name][det] = {
                "merge_rate": sum(c["merged"] for c in cells) / len(cells),
                "isolated_rate": sum(c["isolated"] for c in cells) / len(cells),
                "exact_rate": sum(c["exact"] for c in cells) / len(cells),
            }

    payload = {
        "code_version": CODE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seeds": SEEDS,
        "max_lag": MAX_LAG,
        "vendored_n_agents": VENDORED_N_AGENTS,
        "rows": rows,
        "summary": summary,
    }
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "s6_cmi_detector.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# S6 first step: custom actor-level conditional-MI detector vs. vendored vs. heuristic",
        "",
        f"Generated {payload['generated_at']} at {CODE_VERSION}. NOT a battery -- see module",
        "docstring in `run_s6_cmi_detector.py`. `exact` = non-singleton clusters are exactly",
        "{true pair} (found, isolated, nothing else spuriously merged).",
        "",
    ]
    for name, info in summary.items():
        lines.append(f"## {name} (true pair: {info['true_pair']})")
        lines.append("")
        lines.append("| detector | merge rate | isolated rate | exact rate |")
        lines.append("|---|---|---|---|")
        for det in detector_names:
            cell = info[det]
            lines.append(
                f"| {det} | {cell['merge_rate']:.2f} | {cell['isolated_rate']:.2f} | {cell['exact_rate']:.2f} |"
            )
        lines.append("")
    (RESULTS_DIR / "s6_cmi_detector.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(SCENARIOS)} scenarios x {len(SEEDS)} seeds run.")
    for name, info in summary.items():
        parts = ", ".join(f"{det}={info[det]['exact_rate']:.2f}" for det in detector_names)
        print(f"{name}: exact rates: {parts}")
    print("Wrote results/s6_cmi_detector.{json,md}")


if __name__ == "__main__":
    main()
