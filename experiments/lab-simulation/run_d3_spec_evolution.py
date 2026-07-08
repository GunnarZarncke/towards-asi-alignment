#!/usr/bin/env python3
"""D3.2 spec-evolution + selection battery (MB6b).

Pre-registered protocol: ``lab_sim/harness/d3_spec_evolution.py``.

Outputs: ``results/d3_spec_evolution.{json,md}``
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness.d3_spec_evolution import (
    D3_2_N_GENERATIONS,
    D3_2_POPULATION_SIZE,
    run_spec_evolution_loop,
    sample_d3_2_initial_population,
    trajectory_to_dict,
)
from lab_sim.harness.isolate import MockIsolate, SubprocessIsolate
from lab_sim.world_visible.config import CODE_VERSION

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def _markdown_report(payload: dict, *, wall_seconds: float, backend_label: str) -> str:
    gens = payload["generations"]
    proto = payload["protocol"]
    lines = [
        "# D3.2 spec-evolution + selection report",
        "",
        f"Generated {datetime.now(timezone.utc).isoformat()} at CODE_VERSION `{CODE_VERSION}`.",
        f"Backend: `{backend_label}`. Wall time: {wall_seconds:.1f}s.",
        "",
        "## Protocol",
        "",
        f"- mode: {proto['mode']}",
        f"- population: {proto['population_size']}, generations: {proto['n_generations']}",
        f"- mutation prob (above-median throughput): {proto['mutation_prob']}",
        f"- weakening chain: {proto['weakening_chain']}",
        "",
        "## Endogenous disempowerment curve",
        "",
        "| gen | preserving mass | integrity mass | shortcut mass | mutations | "
        "w. throughput | w. oracle harm | w. severity |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for g in gens:
        lines.append(
            f"| {g['generation']} | {g['correction_preserving_mass_share']:.3f} | "
            f"{g['correction_integrity_mass_share']:.3f} | "
            f"{g['shortcut_spec_mass_share']:.3f} | {g['spec_mutation_events']} | "
            f"{g['weighted_mean_throughput']:.3f} | {g['weighted_mean_oracle_harm']:.4f} | "
            f"{g['weighted_mean_severity']:.4f} |"
        )
    if len(gens) >= 2:
        d_p = gens[-1]["correction_preserving_mass_share"] - gens[0]["correction_preserving_mass_share"]
        d_s = gens[-1]["shortcut_spec_mass_share"] - gens[0]["shortcut_spec_mass_share"]
        lines += [
            "",
            f"Δ correction-preserving mass: **{d_p:+.3f}**",
            f"Δ shortcut-spec mass: **{d_s:+.3f}**",
        ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="D3.2 spec evolution battery")
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--generations", type=int, default=D3_2_N_GENERATIONS)
    parser.add_argument("--population", type=int, default=D3_2_POPULATION_SIZE)
    args = parser.parse_args()

    backend_factory = MockIsolate if args.mock else SubprocessIsolate
    backend_label = "MockIsolate" if args.mock else "SubprocessIsolate"
    configs = sample_d3_2_initial_population(population_size=args.population)

    print(
        f"[d3.2] population={args.population} generations={args.generations} "
        f"backend={backend_label}"
    )
    t0 = time.perf_counter()
    traj = run_spec_evolution_loop(
        configs,
        n_generations=args.generations,
        backend_factory=backend_factory,
    )
    wall = time.perf_counter() - t0
    payload = trajectory_to_dict(traj)
    payload["meta"] = {"code_version": CODE_VERSION, "backend": backend_label, "wall_seconds": wall}

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = RESULTS_DIR / "d3_spec_evolution.json"
    md_path = RESULTS_DIR / "d3_spec_evolution.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(_markdown_report(payload, wall_seconds=wall, backend_label=backend_label), encoding="utf-8")
    print(f"[d3.2] done in {wall:.1f}s -> {json_path.name}, {md_path.name}")
    g0, g1 = payload["generations"][0], payload["generations"][-1]
    print(
        f"[d3.2] preserving mass {g0['correction_preserving_mass_share']:.3f} -> "
        f"{g1['correction_preserving_mass_share']:.3f}; shortcut mass "
        f"{g0['shortcut_spec_mass_share']:.3f} -> {g1['shortcut_spec_mass_share']:.3f}"
    )


if __name__ == "__main__":
    main()
