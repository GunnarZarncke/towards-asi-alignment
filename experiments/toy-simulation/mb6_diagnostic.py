#!/usr/bin/env python3
"""MB6 selection_basin diagnostic sweep."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from multiresolution_alignment_sim.pipeline import run_one
from multiresolution_alignment_sim.schemas import INSTRUMENTATION_LEVELS

DEFAULT_SEEDS = (11, 12, 13)
DEFAULT_T = 1000


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="MB6 selection_basin diagnostic")
    parser.add_argument("--T", type=int, default=DEFAULT_T)
    parser.add_argument("--seeds", type=str, default="11,12,13")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).parent / "results" / "mb6_diagnostic.json",
    )
    args = parser.parse_args()
    seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]

    rows: list[dict] = []
    for level in INSTRUMENTATION_LEVELS:
        for seed in seeds:
            r = run_one("selection_basin", seed, args.T, instrumentation=level)
            ev = r["evaluation"]
            rows.append(
                {
                    "instrumentation": level,
                    "seed": seed,
                    "cci_status": r["cci"]["status"],
                    "cci_status_correct": ev["cci_status_correct"],
                    "basin_capture_fraction_max": ev["basin_capture_fraction_max"],
                    "basin_percolation_crossed": ev["basin_percolation_crossed"],
                    "basin_integrity_signal": r["cci"].get("basin_integrity_signal", False),
                    "manipulation": r["cci"]["manipulation"],
                    "raw_capacity": r["cci"]["raw_capacity"],
                }
            )
            print(
                f"{level}/seed{seed}: status={r['cci']['status']} "
                f"correct={ev['cci_status_correct']} "
                f"basin_max={ev['basin_capture_fraction_max']:.2f} "
                f"percolation={ev['basin_percolation_crossed']}"
            )

    summary = {
        level: sum(
            1
            for x in rows
            if x["instrumentation"] == level and x["cci_status_correct"]
        )
        / max(len(seeds), 1)
        for level in INSTRUMENTATION_LEVELS
    }
    payload = {"T": args.T, "seeds": seeds, "summary_correct_rate": summary, "rows": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out}")
    print("summary:", summary)


if __name__ == "__main__":
    main()
