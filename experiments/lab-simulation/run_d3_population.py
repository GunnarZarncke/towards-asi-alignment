#!/usr/bin/env python3
"""D3.1 population-over-configurations battery (MB6a).

Pre-registered protocol: ``lab_sim/harness/d3_population.py`` module
docstring. Runs the generation loop on ``SubprocessIsolate`` by default;
pass ``--mock`` for a fast smoke run.

Outputs: ``results/d3_population.{json,md}``
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness.d3_population import (
    D3_N_GENERATIONS,
    D3_POPULATION_SIZE,
    run_population_loop,
    sample_initial_population,
    trajectory_to_dict,
)
from lab_sim.harness.isolate import MockIsolate, SubprocessIsolate
from lab_sim.world_visible.config import CODE_VERSION

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def _markdown_report(payload: dict, *, wall_seconds: float, backend_label: str) -> str:
    gens = payload["generations"]
    proto = payload["protocol"]
    lines = [
        "# D3.1 population-over-configurations report",
        "",
        f"Generated {datetime.now(timezone.utc).isoformat()} at CODE_VERSION `{CODE_VERSION}`.",
        f"Backend: `{backend_label}`. Wall time: {wall_seconds:.1f}s.",
        "",
        "## Protocol",
        "",
        f"- population size: {proto['population_size']}",
        f"- generations: {proto['n_generations']}",
        f"- episodes/member/generation: {proto['episodes_per_member']}",
        f"- T={proto['episode_T']}, temperature={proto['temperature']}",
        f"- selection strength: {proto['selection_strength']}, mass floor: {proto['mass_floor']}",
        "",
        "## Basin curve (correction vs throughput selection)",
        "",
        "| gen | correction-preserving mass | correction-integrity mass | "
        "weighted throughput | weighted oracle harm | weighted severity |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for g in gens:
        lines.append(
            f"| {g['generation']} | {g['correction_preserving_mass_share']:.3f} | "
            f"{g['correction_integrity_mass_share']:.3f} | "
            f"{g['weighted_mean_throughput']:.3f} | "
            f"{g['weighted_mean_oracle_harm']:.4f} | {g['weighted_mean_severity']:.4f} |"
        )
    if len(gens) >= 2:
        d_cp = gens[-1]["correction_preserving_mass_share"] - gens[0]["correction_preserving_mass_share"]
        lines += [
            "",
            f"Δ correction-preserving mass (gen 0 → last): **{d_cp:+.3f}** "
            "(negative = throughput selection eroded correction-preserving share).",
        ]
    lines += [
        "",
        "## Final generation — member mass",
        "",
        "| member | mass (after) | throughput | preserving | pipeline | board cap | admin |",
        "|---|---:|---:|:---:|---|---:|---|",
    ]
    last = gens[-1]["members"]
    for m in sorted(last, key=lambda x: -x["deployment_mass_after"]):
        admin = f"lp={m['admin_least_privilege']}, cap={m['admin_capture_start']}"
        lines.append(
            f"| {m['member_id']} | {m['deployment_mass_after']:.3f} | "
            f"{m['mean_throughput']:.2f} | {m['correction_preserving']} | "
            f"{m['pipeline_spec']} | {m['board_capture_start']} | {admin} |"
        )
    lines += [
        "",
        "See `lab_sim/harness/d3_population.py` for structural tags and selection rule.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="D3.1 population selection battery")
    parser.add_argument("--mock", action="store_true", help="Use MockIsolate (fast smoke)")
    parser.add_argument("--generations", type=int, default=D3_N_GENERATIONS)
    parser.add_argument("--population", type=int, default=D3_POPULATION_SIZE)
    args = parser.parse_args()

    backend_factory = MockIsolate if args.mock else SubprocessIsolate
    backend_label = "MockIsolate" if args.mock else "SubprocessIsolate"

    configs = sample_initial_population(population_size=args.population)
    print(
        f"[d3.1] population={args.population} generations={args.generations} "
        f"backend={backend_label}"
    )
    t0 = time.perf_counter()
    traj = run_population_loop(
        configs,
        n_generations=args.generations,
        backend_factory=backend_factory,
    )
    wall = time.perf_counter() - t0
    payload = trajectory_to_dict(traj)
    payload["meta"] = {
        "code_version": CODE_VERSION,
        "backend": backend_label,
        "wall_seconds": wall,
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = RESULTS_DIR / "d3_population.json"
    md_path = RESULTS_DIR / "d3_population.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(_markdown_report(payload, wall_seconds=wall, backend_label=backend_label), encoding="utf-8")
    print(f"[d3.1] done in {wall:.1f}s -> {json_path.name}, {md_path.name}")
    g0 = payload["generations"][0]["correction_preserving_mass_share"]
    g1 = payload["generations"][-1]["correction_preserving_mass_share"]
    print(f"[d3.1] correction-preserving mass: {g0:.3f} -> {g1:.3f} (Δ {g1 - g0:+.3f})")


if __name__ == "__main__":
    main()
