#!/usr/bin/env python3
"""Mechanical ET-3 reverse smoke: oversight_drag adds calendar days per phase.

Uses fixed gap/speed samples (n_sims=100) and the same post-patch calendar rule
as ``takeoff/forecasting_takeoff.py`` — no upstream Monte Carlo sampling required.
"""

from __future__ import annotations

import json
import statistics
from datetime import datetime, timedelta
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent.parent / "results"
N_SIMS = 100
START = datetime(2027, 3, 31)
GAPS_DAYS = {"SC to SAR": 1825.0, "SAR to SIAR": 730.0, "SIAR to ASI": 3650.0}
SPEEDS = {"SC": 5, "SAR": 25, "SIAR": 250, "ASI": 2000}


def run_phase_simulation(gap: float, start_speed: float, end_speed: float) -> float:
    dt = 1
    calendar_time = 0
    progress = 0
    while progress < gap:
        progress_ratio = progress / gap if gap else 0
        current_speedup = start_speed * (end_speed / start_speed) ** progress_ratio
        progress += current_speedup * dt
        calendar_time += dt
    return calendar_time


def median_sar_year(oversight_drag_years: float) -> float:
    milestones = ["SC", "SAR", "SIAR", "ASI"]
    sar_years: list[float] = []
    for _ in range(N_SIMS):
        current = START
        for i, milestone in enumerate(milestones[:-1]):
            nxt = milestones[i + 1]
            pair = f"{milestone} to {nxt}"
            gap = GAPS_DAYS[pair]
            calendar_days = run_phase_simulation(gap, SPEEDS[milestone], SPEEDS[nxt])
            calendar_days += oversight_drag_years * 365
            current = current + timedelta(days=calendar_days)
            if milestone == "SC":
                sar_years.append(current.year + current.timetuple().tm_yday / 365.0)
                break
    return statistics.median(sar_years)


def main() -> None:
    med0 = median_sar_year(0.0)
    med1 = median_sar_year(1.0)
    passed = med1 > med0
    payload = {
        "n_sims": N_SIMS,
        "oversight_drag_values": [0.0, 1.0],
        "median_sar_year": {"drag_0": med0, "drag_1": med1},
        "assertion_passed": passed,
        "mode": "mechanical_fixed_samples",
        "note": "Validates patched calendar-drag rule; not full upstream Monte Carlo.",
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = RESULTS_DIR / "et3_reverse_smoke.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
