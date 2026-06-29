#!/usr/bin/env python3
"""CLI for Phase 3 LLM episodic red-team."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from .llm_runner import PHASE3_SCENARIOS, make_planner, run_llm_suite

ROOT = Path(__file__).resolve().parent.parent
RESULT_DIR = ROOT / "results"
LOG_DIR = ROOT / "logs"


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM episodic red-team (Phase 3)")
    parser.add_argument("--T", type=int, default=1000)
    parser.add_argument("--seeds", type=str, default="11,12")
    parser.add_argument(
        "--scenarios",
        type=str,
        default=",".join(PHASE3_SCENARIOS),
    )
    parser.add_argument(
        "--instrumentation",
        type=str,
        default="medium_handles",
        choices=["light_handles", "medium_handles", "strong_handles"],
    )
    parser.add_argument("--model", type=str, default="gpt-4o-mini")
    parser.add_argument("--cost-budget-usd", type=float, default=5.0)
    parser.add_argument("--max-output-tokens", type=int, default=2048)
    parser.add_argument(
        "--baseline",
        type=str,
        default="full_redteam",
        help="Hand-written deployment agent for comparison",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Offline mock planner (mirrors full_redteam, no API)",
    )
    parser.add_argument(
        "--no-source",
        action="store_true",
        help="Omit full source bodies from LLM prompt (hash index only)",
    )
    parser.add_argument(
        "--source-max-chars",
        type=int,
        default=0,
        help="Truncate each source module (0 = no limit; full ~55k chars total)",
    )
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    if args.smoke:
        args.T = 300
        args.seeds = "11"
        args.scenarios = "capture_theater,grounding_silent_gap"
        args.mock = True

    seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
    scenarios = [s.strip() for s in args.scenarios.split(",") if s.strip()]

    planner = make_planner(
        mock=args.mock,
        model=args.model,
        cost_budget_usd=args.cost_budget_usd,
        max_output_tokens=args.max_output_tokens,
        include_source=not args.no_source,
        max_chars_per_module=args.source_max_chars or None,
    )

    payload = run_llm_suite(
        scenarios,  # type: ignore[arg-type]
        seeds,
        args.T,
        planner,
        instrumentation=args.instrumentation,  # type: ignore[arg-type]
        baseline_strategy=args.baseline,
    )

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    json_path = RESULT_DIR / "llm_redteam_episodic.json"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    stamp = datetime.now().isoformat()
    log_path = LOG_DIR / f"llm-redteam-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.md"
    log_lines = [
        f"# LLM episodic red-team {stamp}",
        "",
        f"- planner: {payload['planner']}",
        f"- llm_false_pass_rate: {payload['llm_false_pass_rate']:.2f}",
        f"- baseline_false_pass_rate: {payload['baseline_false_pass_rate']:.2f}",
        f"- llm_mean_cci_correct: {payload['llm_mean_cci_correct']:.2f}",
        "",
    ]
    for run in payload["runs"]:
        log_lines.append(
            f"- {run['scenario']}/seed{run['seed']}: status={run['cci_status']} "
            f"false_pass={run['false_pass']} patches={run['n_planned_patches']}"
        )
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Log {log_path}")
    print(f"planner={payload['planner']}")
    print(f"llm_false_pass_rate={payload['llm_false_pass_rate']:.2f}")
    print(f"baseline_false_pass_rate={payload['baseline_false_pass_rate']:.2f}")
    print(f"llm_mean_cci_correct={payload['llm_mean_cci_correct']:.2f}")


if __name__ == "__main__":
    main()
