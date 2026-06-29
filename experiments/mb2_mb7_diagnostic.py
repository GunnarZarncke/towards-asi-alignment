#!/usr/bin/env python3
"""MB2/MB7 tuning prep: per-level cci_status_correct on held-out stress scenarios."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from multiresolution_alignment_sim.pipeline import run_one
from multiresolution_alignment_sim.schemas import INSTRUMENTATION_LEVELS, ScenarioName

SCENARIOS: tuple[ScenarioName, ...] = ("bundle_goodhart", "hidden_capability")
DEFAULT_SEEDS = (11, 12, 13)
DEFAULT_T = 1000


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="MB2/MB7 diagnostic sweep")
    parser.add_argument("--T", type=int, default=DEFAULT_T)
    parser.add_argument("--seeds", type=str, default="11,12,13")
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "results" / "mb2_mb7_diagnostic.json")
    args = parser.parse_args()
    seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]

    rows: list[dict[str, object]] = []
    for scenario in SCENARIOS:
        for level in INSTRUMENTATION_LEVELS:
            for seed in seeds:
                r = run_one(scenario, seed, args.T, instrumentation=level, bootstrap=False)
                ev = r["evaluation"]
                rows.append(
                    {
                        "scenario": scenario,
                        "instrumentation": level,
                        "seed": seed,
                        "cci_status": r["cci"]["status"],
                        "cci_status_correct": ev["cci_status_correct"],
                        "task_success": ev["task_success_proxy"],
                        "capability_slack": ev["capability_correction_slack"],
                        "bundle_geometry_spread": ev.get("bundle_geometry_spread", 0.0),
                        "bundle_reward_proxy_range": ev.get("bundle_reward_proxy_range", 0.0),
                        "hidden_memory_step_rate": ev.get("hidden_memory_step_rate", 0.0),
                        "tool_shadow_step_rate": ev.get("tool_shadow_step_rate", 0.0),
                        "hidden_capability_signal": r["cci"].get("hidden_capability_signal", False),
                        "grounding_gap_detected": r["cci"].get("grounding_gap_detected", False),
                    }
                )
                print(
                    f"{scenario}/{level}/seed{seed}: "
                    f"status={r['cci']['status']} correct={ev['cci_status_correct']} "
                    f"slack={ev['capability_correction_slack']:.2f}"
                )

    summary: dict[str, dict[str, float]] = {}
    for scenario in SCENARIOS:
        summary[scenario] = {}
        for level in INSTRUMENTATION_LEVELS:
            subset = [x for x in rows if x["scenario"] == scenario and x["instrumentation"] == level]
            correct = sum(1 for x in subset if x["cci_status_correct"]) / max(len(subset), 1)
            summary[scenario][level] = correct

    payload = {
        "T": args.T,
        "seeds": seeds,
        "scenarios": list(SCENARIOS),
        "summary_correct_rate": summary,
        "rows": rows,
        "tuning_notes": (
            "Tune sim drift/boost knobs only if medium+ fails expected belowThreshold; "
            "do not retune capture thresholds on these seeds."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out}")
    for scen, by_level in summary.items():
        print(f"{scen}: " + " ".join(f"{lv}={v:.2f}" for lv, v in by_level.items()))


if __name__ == "__main__":
    main()
