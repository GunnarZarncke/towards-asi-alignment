#!/usr/bin/env python3
"""CLI for LLM red-team scaffold (hand-written strategies until LLM wired)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from .harness import REDTEAM_SCENARIOS, run_redteam_battery, run_redteam_suite
from .report import build_report
from .strategies import STRATEGIES

ROOT = Path(__file__).resolve().parent.parent
RESULT_DIR = ROOT / "results"
LOG_DIR = ROOT / "logs"

BATTERY_STRATEGIES = list(STRATEGIES.keys())
BATTERY_LEVELS = ("light_handles", "medium_handles", "strong_handles")
BATTERY_SEEDS = list(range(11, 21))


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM red-team scaffold")
    parser.add_argument("--T", type=int, default=1000)
    parser.add_argument("--seeds", type=str, default="11,12")
    parser.add_argument(
        "--scenarios",
        type=str,
        default=",".join(REDTEAM_SCENARIOS),
    )
    parser.add_argument(
        "--strategies",
        type=str,
        default="none,theater_inflate,full_redteam",
        help=f"Comma-separated: {','.join(STRATEGIES)}",
    )
    parser.add_argument(
        "--instrumentation",
        type=str,
        default="medium_handles",
        choices=["light_handles", "medium_handles", "strong_handles"],
    )
    parser.add_argument(
        "--instrumentation-levels",
        type=str,
        default="",
        help="Comma-separated levels for multi-level runs (battery mode)",
    )
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument(
        "--battery",
        action="store_true",
        help="Phase 1 full battery: all strategies, held-out seeds 11–20, T=2000, 3 levels",
    )
    args = parser.parse_args()

    if args.smoke:
        args.T = 500
        args.seeds = "11"
        args.scenarios = "capture_theater,grounding_silent_gap"
        args.strategies = "none,full_redteam"

    if args.battery:
        args.T = max(args.T, 2000)
        args.seeds = ",".join(str(s) for s in BATTERY_SEEDS)
        args.scenarios = ",".join(REDTEAM_SCENARIOS)
        args.strategies = ",".join(BATTERY_STRATEGIES)
        if not args.instrumentation_levels:
            args.instrumentation_levels = ",".join(BATTERY_LEVELS)

    def parse_list(spec: str) -> list[str]:
        return [s.strip() for s in spec.split(",") if s.strip()]

    seeds = [int(s) for s in parse_list(args.seeds)]
    scenarios = parse_list(args.scenarios)  # type: ignore[assignment]
    strategies = parse_list(args.strategies)
    levels_spec = parse_list(args.instrumentation_levels)

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    if levels_spec:
        payload = run_redteam_battery(
            scenarios,
            seeds,
            args.T,
            strategies,
            instrumentation_levels=levels_spec,  # type: ignore[arg-type]
        )
        json_path = RESULT_DIR / "llm_redteam_battery.json"
        report_path = RESULT_DIR / "llm_redteam_report.md"
    else:
        payload = run_redteam_suite(
            scenarios,
            seeds,
            args.T,
            strategies,
            instrumentation=args.instrumentation,  # type: ignore[arg-type]
        )
        json_path = RESULT_DIR / "llm_redteam_scaffold.json"
        report_path = None

    stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    log_path = LOG_DIR / f"redteam-{stamp}.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        f"# Red-team {'battery' if levels_spec else 'scaffold'} {datetime.now().isoformat()}",
        "",
        f"- false_pass_rate: {payload['false_pass_rate']:.2f}",
        f"- strategies: {strategies}",
        "",
    ]
    for name, stats in payload["summary_by_strategy"].items():
        lines.append(
            f"- **{name}**: false_pass={stats['false_pass_rate']:.2f} "
            f"cci_correct={stats['mean_cci_correct']:.2f} n={stats['n_runs']}"
        )
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if report_path is not None:
        report_path.write_text(build_report(payload), encoding="utf-8")
        print(f"Wrote {report_path}")

    print(f"Wrote {json_path}")
    print(f"Log {log_path}")
    print(f"false_pass_rate={payload['false_pass_rate']:.2f}")
    for name, stats in payload["summary_by_strategy"].items():
        print(
            f"  {name}: false_pass={stats['false_pass_rate']:.2f} "
            f"cci_correct={stats['mean_cci_correct']:.2f}"
        )


if __name__ == "__main__":
    main()
