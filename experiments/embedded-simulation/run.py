#!/usr/bin/env python3
"""Run embedded audit simulation across all MB scenarios."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from embedded_sim.js_isolate import summarize_isolate_runs
from embedded_sim.pipeline import episode_to_dict, run_all_mbs

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def _write_report(results: list, out_json: Path, out_md: Path, *, wall_seconds: float | None = None, workers: int = 1) -> dict:
    all_isolate_runs = [r for ep in results for r in ep.isolate_runs]
    payload = {
        "n_episodes": len(results),
        "episodes": [episode_to_dict(r) for r in results],
        "summary": {
            "false_pass_count": sum(1 for r in results if r.outer.false_pass),
            "outer_certifies_count": sum(1 for r in results if r.outer.outer_certifies),
            "in_sim_correct_count": sum(1 for r in results if r.outer.in_sim_correct),
            "isolate_timing": summarize_isolate_runs(all_isolate_runs),
            "isolate_workers": workers,
            "wall_seconds": wall_seconds,
        },
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Embedded simulation report",
        "",
        f"Episodes: {len(results)}",
        "",
        "| Bridge | Substrate | Scenario | Red-team | In-sim | Outer certifies | False pass |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in results:
        lines.append(
            f"| {r.bridge} | {r.substrate} | {r.scenario} | {r.redteam_strategy} | "
            f"{r.in_sim.safety_decision}/{r.in_sim.cci_status} | "
            f"{r.outer.outer_certifies} | {r.outer.false_pass} |"
        )
    iso = payload["summary"].get("isolate_timing") or {}
    if iso.get("count", 0):
        lines.extend(
            [
                "",
                "## Isolate timing",
                "",
                f"Runs: {iso['count']}",
                f"Total: {iso['total_seconds']:.3f}s",
                f"Spawn: {iso['spawn_seconds']:.3f}s",
                f"IPC (Node wait): {iso['ipc_seconds']:.3f}s",
                f"Bridge (host): {iso['bridge_seconds']:.3f}s",
                f"Teardown: {iso['teardown_seconds']:.3f}s",
                f"Bridge calls: {iso['bridge_calls']}",
                "",
                f"Batch wall: {payload['summary'].get('wall_seconds', 0):.3f}s",
                f"Workers: {payload['summary'].get('isolate_workers', 1)}",
            ]
        )
    lines.extend(
        [
            "",
            f"False passes: {payload['summary']['false_pass_count']}",
            f"Outer certifies: {payload['summary']['outer_certifies_count']}",
            f"In-sim CCI correct: {payload['summary']['in_sim_correct_count']}",
        ]
    )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Embedded audit experiment runner")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--T", type=int, default=800)
    parser.add_argument("--instrumentation", default="medium_handles")
    parser.add_argument("--redteam", default="none", help="none or full_redteam")
    parser.add_argument(
        "--substrate",
        default="python",
        choices=("python", "js"),
        help="isolate substrate: python direct bridge or node JS isolate",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="parallel isolate workers per pipeline timestep (redteam, audit, eval waves)",
    )
    args = parser.parse_args()

    t0 = time.perf_counter()
    results = run_all_mbs(
        seed=args.seed,
        T=args.T,
        instrumentation=args.instrumentation,  # type: ignore[arg-type]
        redteam_strategy=args.redteam,
        substrate=args.substrate,  # type: ignore[arg-type]
        isolate_workers=args.workers,
    )
    wall_seconds = time.perf_counter() - t0
    payload = _write_report(
        results,
        RESULTS / "embedded_sim_report.json",
        RESULTS / "embedded_sim_report.md",
        wall_seconds=wall_seconds,
        workers=args.workers,
    )
    print(f"Wrote {RESULTS / 'embedded_sim_report.json'} ({len(results)} episodes)")
    if args.workers > 1:
        print(f"Wall clock: {wall_seconds:.3f}s with workers={args.workers}")
    iso = payload["summary"].get("isolate_timing") or {}
    if iso.get("count", 0):
        print(
            "Isolate timing: "
            f"total={iso['total_seconds']:.3f}s "
            f"spawn={iso['spawn_seconds']:.3f}s "
            f"ipc={iso['ipc_seconds']:.3f}s "
            f"bridge={iso['bridge_seconds']:.3f}s "
            f"calls={iso['bridge_calls']}"
        )


if __name__ == "__main__":
    main()
