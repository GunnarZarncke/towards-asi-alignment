#!/usr/bin/env python3
"""S6 intervention-supported UAD — full sweep vs passive baselines.

Runs ``discovered_units_intervention`` (channel ablation + directed actor
probes, honest-twin control) against the same five S5/S6 scenarios plus
``serial_pipeline_no_unit_config`` negative control, side by side with
heuristic, vendored MI, and custom CMI detectors.

Pre-registered defaults in ``uad_intervention.py`` — report whatever the
sweep yields, including failures (shared_slot remains the hard case).
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
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.uad import discovered_units, uad_score
from lab_sim.oracle_only.uad_cmi import discovered_units_cmi
from lab_sim.oracle_only.uad_intervention import discovered_units_intervention
from lab_sim.oracle_only.uad_mi import discovered_units_mi
from lab_sim.oracle_only.uad_partition import partition_metrics
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"
SEEDS = tuple(range(1, 6))
MAX_LAG = 3
VENDORED_N_AGENTS = 2

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
    backend = MockIsolate()
    result = run_episode(cfg, seed=seed, backend=backend)
    true_units = cfg.resolved_units()
    try:
        row: dict = {
            "scenario": scenario_name,
            "true_pair": list(true_pair) if true_pair else None,
            "seed": seed,
            "detectors": {},
        }
        heuristic = discovered_units(result)
        row["detectors"]["heuristic"] = {
            **_pair_metrics(heuristic, true_pair),
            **partition_metrics(true_units, heuristic),
        }
        for depth in ("shallow", "deep"):
            vendored = discovered_units_mi(result, n_agents=VENDORED_N_AGENTS, max_lag=MAX_LAG, depth=depth)
            row["detectors"][f"vendored_mi_{depth}"] = {
                **_pair_metrics(vendored, true_pair),
                **partition_metrics(true_units, vendored),
            }
            cmi = discovered_units_cmi(result, depth=depth, max_lag=MAX_LAG)
            row["detectors"][f"cmi_{depth}"] = {
                **_pair_metrics(cmi, true_pair),
                **partition_metrics(true_units, cmi),
            }
        intervention = discovered_units_intervention(result, cfg, seed, backend=backend)
        row["detectors"]["intervention"] = {
            **_pair_metrics(intervention, true_pair),
            **partition_metrics(true_units, intervention),
        }
        return row
    finally:
        result.cleanup()


def main() -> None:
    rows = [_run_cell(name, seed) for name in SCENARIOS for seed in SEEDS]
    detector_names = (
        ["heuristic", "intervention"]
        + [f"{d}_{depth}" for d in ("vendored_mi", "cmi") for depth in ("shallow", "deep")]
    )

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
                "mean_adjusted_rand": sum(c["adjusted_rand"] for c in cells) / len(cells),
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
    (RESULTS_DIR / "s6_intervention_uad.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# S6 intervention-supported UAD vs passive baselines",
        "",
        f"Generated {payload['generated_at']} at {CODE_VERSION}. NOT a battery.",
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
    (RESULTS_DIR / "s6_intervention_uad.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(SCENARIOS)} scenarios x {len(SEEDS)} seeds run.")
    for name, info in summary.items():
        parts = ", ".join(f"{det}={info[det]['exact_rate']:.2f}" for det in detector_names)
        print(f"{name}: exact rates: {parts}")
    print("Wrote results/s6_intervention_uad.{json,md}")


if __name__ == "__main__":
    main()
