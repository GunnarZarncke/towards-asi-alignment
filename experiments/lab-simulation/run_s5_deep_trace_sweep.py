#!/usr/bin/env python3
"""S5 follow-up (user-directed, recorded 2026-07-07 -- "that trace is
much too light... we might want to record UAD at different depth to
determine probe scale... Run against multiple scenarios"): re-runs
`uad_mi.discovered_units_mi` at BOTH trace depths (`"shallow"`: the
original 2-vars/actor probe; `"deep"`: the widened 5-vars/actor probe
adding DM-receive, access-grant, access-deny, and a wider tool
vocabulary -- see `uad_mi.py`'s module docstring) against FIVE distinct
scenario ecologies, not just S4's `shared_slot_config` alone.

NOT a battery: same small-seed `MockIsolate` exploration status as
`run_s5_uad_core_port.py` (which this script complements, not
replaces -- that script's single-scenario `n_agents` sweep stays the
canonical S4 result; this one asks "does probe depth change detection
quality, and does S4's over-merge story generalize to other
ecologies").

SCENARIOS (one true non-singleton unit each, per `cfg.resolved_units()`):
  - dm_pair_config: {eng1, rm1} DM-coordinated pair.
  - covert_file_handoff_config(trusting=True): {eng1, rev1} file-share pair.
  - committee_with_informal_chatter_config: {rev1, rev2} (the review
    committee -- the "informal chatter" is a decoy signal from eng1, a
    NON-unit actor). NOTE: the first version of this script wrongly
    listed {eng1, rm1} as this scenario's true pair; caught during the
    G-26 diagnosis pass (the committee's `units=` literal in
    `ecology.py` is `("review_committee", reviewer_ids)`) and fixed.
  - build_loop_config: {eng1, rm1} multi-generation build loop (S1).
  - shared_slot_config: {eng1, eng2} shared-slot pair (S4, same episodes
    `run_s5_uad_core_port.py` already covers at `depth="deep"` only --
    reproduced here at BOTH depths for the depth comparison).

For each (scenario, depth, n_agents) cell: does the detector merge the
TRUE pair, and is that pair ISOLATED from every other playbook actor
(mirrors `run_s5_uad_core_port.py`'s `_eng1_eng2_isolated_from_rev_rm`,
generalized to any true pair) -- `uad_score` alone cannot distinguish
"found the true pair" from "merged everyone into one blob."
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
from lab_sim.oracle_only.uad_mi import discovered_units_mi
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"
SEEDS = tuple(range(1, 6))
DEPTHS = ("shallow", "deep")
N_AGENTS_SWEEP = (1, 2, 3, 4)
MAX_LAG = 3

# name -> (config_factory, true_pair) -- true_pair read off each
# ecology's own `units=` literal above, not derived at runtime, so a
# future edit to `ecology.py` that changes a unit's membership shows up
# here as a mismatch rather than silently tracking the new value.
SCENARIOS: dict[str, tuple] = {
    "dm_pair": (lambda: dm_pair_config(T=100), ("eng1", "rm1")),
    "covert_file_handoff": (lambda: covert_file_handoff_config(trusting=True, T=100), ("eng1", "rev1")),
    "committee_informal_chatter": (lambda: committee_with_informal_chatter_config(T=100), ("rev1", "rev2")),
    "build_loop": (lambda: build_loop_config(T=200), ("eng1", "rm1")),
    "shared_slot": (lambda: shared_slot_config(T=100), ("eng1", "eng2")),
}


def _cluster_containing(discovered: dict[str, tuple[str, ...]], actor: str) -> tuple[str, ...]:
    for members in discovered.values():
        if actor in members:
            return members
    return (actor,)


def _pair_merged_and_isolated(discovered: dict[str, tuple[str, ...]], pair: tuple[str, str]) -> tuple[bool, bool]:
    a, b = pair
    cluster = _cluster_containing(discovered, a)
    merged = b in cluster
    isolated = merged and set(cluster) == {a, b}
    return merged, isolated


def _run_cell(scenario_name: str, seed: int, depth: str) -> dict:
    factory, true_pair = SCENARIOS[scenario_name]
    cfg = factory()
    result = run_episode(cfg, seed=seed, backend=MockIsolate())
    try:
        heuristic = discovered_units(result)
        heuristic_score = uad_score(cfg.resolved_units(), heuristic)
        heuristic_merged, heuristic_isolated = _pair_merged_and_isolated(heuristic, true_pair)

        sweep = {}
        for n_agents in N_AGENTS_SWEEP:
            discovered = discovered_units_mi(result, n_agents=n_agents, max_lag=MAX_LAG, depth=depth)
            merged, isolated = _pair_merged_and_isolated(discovered, true_pair)
            sweep[n_agents] = {
                "discovered": {k: list(v) for k, v in discovered.items()},
                "true_pair_merged": merged,
                "true_pair_isolated": isolated,
                "uad_score": uad_score(cfg.resolved_units(), discovered),
            }
        return {
            "scenario": scenario_name,
            "true_pair": list(true_pair),
            "seed": seed,
            "depth": depth,
            "heuristic_uad_score": heuristic_score,
            "heuristic_true_pair_merged": heuristic_merged,
            "heuristic_true_pair_isolated": heuristic_isolated,
            "mi_sweep": sweep,
        }
    finally:
        result.cleanup()


def main() -> None:
    rows = [
        _run_cell(scenario_name, seed, depth)
        for scenario_name in SCENARIOS
        for depth in DEPTHS
        for seed in SEEDS
    ]

    summary: dict[str, dict] = {}
    for scenario_name in SCENARIOS:
        scenario_rows = [r for r in rows if r["scenario"] == scenario_name]
        summary[scenario_name] = {
            "true_pair": SCENARIOS[scenario_name][1],
            "heuristic_merge_rate": sum(1 for r in scenario_rows if r["heuristic_true_pair_merged"]) / len(scenario_rows),
            "by_depth": {
                depth: {
                    n_agents: {
                        "merge_rate": sum(
                            1
                            for r in scenario_rows
                            if r["depth"] == depth and r["mi_sweep"][n_agents]["true_pair_merged"]
                        )
                        / len(SEEDS),
                        "isolated_rate": sum(
                            1
                            for r in scenario_rows
                            if r["depth"] == depth and r["mi_sweep"][n_agents]["true_pair_isolated"]
                        )
                        / len(SEEDS),
                        "mean_uad_score": sum(
                            r["mi_sweep"][n_agents]["uad_score"] for r in scenario_rows if r["depth"] == depth
                        )
                        / len(SEEDS),
                    }
                    for n_agents in N_AGENTS_SWEEP
                }
                for depth in DEPTHS
            },
        }

    payload = {
        "code_version": CODE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seeds": SEEDS,
        "depths": DEPTHS,
        "n_agents_sweep": N_AGENTS_SWEEP,
        "max_lag": MAX_LAG,
        "rows": rows,
        "summary": summary,
    }
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "s5_deep_trace_sweep.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# S5 follow-up: deep vs. shallow UAD trace, across five scenarios",
        "",
        f"Generated {payload['generated_at']} at {CODE_VERSION}. NOT a battery -- see module",
        "docstring in `run_s5_deep_trace_sweep.py`.",
        "",
        f"Seeds: {SEEDS}, max_lag={MAX_LAG}. Each cell: isolated_rate/merge_rate averaged over",
        "seeds; mean_uad_score is `uad.uad_score` against oracle `resolved_units()`.",
        "",
    ]
    for scenario_name, info in summary.items():
        lines.append(f"## {scenario_name} (true pair: {info['true_pair']})")
        lines.append("")
        lines.append(f"Heuristic (`uad.discovered_units`) merge rate: {info['heuristic_merge_rate']:.2f}")
        lines.append("")
        lines.append("| depth | n_agents | merge rate | isolated rate | mean uad_score |")
        lines.append("|---|---|---|---|---|")
        for depth in DEPTHS:
            for n_agents in N_AGENTS_SWEEP:
                cell = info["by_depth"][depth][n_agents]
                lines.append(
                    f"| {depth} | {n_agents} | {cell['merge_rate']:.2f} | {cell['isolated_rate']:.2f} | "
                    f"{cell['mean_uad_score']:.2f} |"
                )
        lines.append("")
    (RESULTS_DIR / "s5_deep_trace_sweep.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(SCENARIOS)} scenarios x {len(DEPTHS)} depths x {len(N_AGENTS_SWEEP)} n_agents x {len(SEEDS)} seeds run.")
    for scenario_name, info in summary.items():
        print(f"{scenario_name}: heuristic_merge_rate={info['heuristic_merge_rate']:.2f}")
    print("Wrote results/s5_deep_trace_sweep.{json,md}")


if __name__ == "__main__":
    main()
