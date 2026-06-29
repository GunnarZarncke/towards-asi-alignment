#!/usr/bin/env python3
"""MB3 bearer_mismap + MB8 legitimacy_theater diagnostic sweep."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from multiresolution_alignment_sim.pipeline import run_one
from multiresolution_alignment_sim.schemas import INSTRUMENTATION_LEVELS

SCENARIOS = ("bearer_mismap", "legitimacy_theater")
DEFAULT_SEEDS = tuple(range(11, 21))
DEFAULT_T = 1000


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="MB3/MB8 bridge diagnostic")
    parser.add_argument("--T", type=int, default=DEFAULT_T)
    parser.add_argument("--seeds", type=str, default="11,12,13,14,15,16,17,18,19,20")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).parent / "results" / "mb3_mb8_diagnostic.json",
    )
    args = parser.parse_args()
    seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]

    rows: list[dict] = []
    for scenario in SCENARIOS:
        for level in INSTRUMENTATION_LEVELS:
            for seed in seeds:
                r = run_one(scenario, seed, args.T, instrumentation=level)
                ev = r["evaluation"]
                cci = r["cci"]
                safety = r["safety"]
                rows.append(
                    {
                        "scenario": scenario,
                        "instrumentation": level,
                        "seed": seed,
                        "cci_status": cci["status"],
                        "cci_status_correct": ev["cci_status_correct"],
                        "failed_bridge": safety.get("failed_bridge"),
                        "bearer_mismatch_detected": cci.get("bearer_mismatch_detected", False),
                        "legitimacy_theater_detected": cci.get(
                            "legitimacy_theater_detected", False
                        ),
                        "grounding_gap_detected": cci.get("grounding_gap_detected", False),
                        "raw_capacity": cci["raw_capacity"],
                        "manipulation": cci["manipulation"],
                        "mean_reported": cci.get("mean_reported_on_episodes", 0.0),
                    }
                )
                print(
                    f"{scenario}/{level}/seed{seed}: status={cci['status']} "
                    f"correct={ev['cci_status_correct']} bridge={safety.get('failed_bridge')} "
                    f"mb3={cci.get('bearer_mismatch_detected')} "
                    f"mb8={cci.get('legitimacy_theater_detected')}"
                )

    summary: dict[str, dict[str, float]] = {}
    for scenario in SCENARIOS:
        summary[scenario] = {}
        for level in INSTRUMENTATION_LEVELS:
            subset = [
                x
                for x in rows
                if x["scenario"] == scenario and x["instrumentation"] == level
            ]
            summary[scenario][level] = sum(
                1 for x in subset if x["cci_status_correct"]
            ) / max(len(subset), 1)

    payload = {
        "T": args.T,
        "seeds": seeds,
        "summary_correct_rate": summary,
        "handle_integrity_note": (
            "Handles in these scenarios are truthfully logged from micro dynamics. "
            "Instrument capture (adversary writes handle.* directly) is the planned "
            "MB4/MB9 commutation scenario — not yet implemented. medium_handles "
            "certification assumes handles are protected transport of micro signals, "
            "not self-reporting theater channels."
        ),
        "rows": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out}")
    for scenario, levels in summary.items():
        print(f"{scenario}:", levels)


if __name__ == "__main__":
    main()
