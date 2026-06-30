#!/usr/bin/env python3
"""CLI for embedded LLM red-team."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from embedded_llm.llm_runner import LLM_BRIDGES, run_llm_suite  # noqa: E402

RESULTS = ROOT / "results"
LOGS = ROOT / "logs"


def main() -> None:
    parser = argparse.ArgumentParser(description="Embedded LLM red-team")
    parser.add_argument("--T", type=int, default=800)
    parser.add_argument("--seeds", type=str, default="11,12,13")
    parser.add_argument("--bridges", type=str, default=",".join(LLM_BRIDGES))
    parser.add_argument("--instrumentation", default="medium_handles")
    parser.add_argument("--mock", action="store_true", help="Offline mock planner (no API)")
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    if args.smoke:
        args.T = 400
        args.seeds = "11"
        args.bridges = "MB4,MB9"
        args.mock = True

    seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
    bridges = [b.strip() for b in args.bridges.split(",") if b.strip()]

    RESULTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    payload = run_llm_suite(
        bridges=bridges,
        seeds=seeds,
        T=args.T,
        instrumentation=args.instrumentation,  # type: ignore[arg-type]
        use_mock=args.mock,
        model=args.model,
    )
    payload["started_at"] = datetime.now(timezone.utc).isoformat()

    suffix = "mock" if args.mock else args.model.replace("/", "-")
    json_path = RESULTS / f"embedded_llm_redteam_{suffix}.json"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md_lines = [
        "# Embedded LLM red-team report",
        "",
        f"- planner: {payload['planner']}",
        f"- T: {payload['T']}",
        f"- false_pass_rate: {payload['llm_false_pass_rate']:.2%}",
        f"- in_sim_correct_rate: {payload['llm_mean_in_sim_correct']:.2%}",
        f"- runtime: {payload['runtime_seconds']}s",
        "",
        "| Bridge | Seed | False pass | Decision | CCI |",
        "| --- | --- | --- | --- | --- |",
    ]
    for run in payload["runs"]:
        md_lines.append(
            f"| {run['bridge']} | {run['seed']} | {run['false_pass']} | "
            f"{run['safety_decision']} | {run['cci_status']} |"
        )
    md_path = RESULTS / f"embedded_llm_redteam_{suffix}.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"llm_false_pass_rate={payload['llm_false_pass_rate']:.2%}")


if __name__ == "__main__":
    main()
