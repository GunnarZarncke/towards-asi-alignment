"""Focused, powered evaluation of the Part B channel-set eligibility fix (N-10).

Pre-registered predictions (see session log 2026-07-03-channel-sets-n10-eligibility):

1. No blind false passes: on capture/violation scenarios that light_handles
   previously certified, partial levels (light/light_plus/medium_minus) issue
   pass-rate 0 (eligibility gate -> belowThreshold).
2. Certification not broken: on honest scenarios, medium/strong still pass at a
   high rate; partial levels are uncertifiable (pass-rate 0) -- the priced cost.
3. Channel-resolved detection: light_plus (has action_arbitration) flags
   inferential_coupling but still cannot certify instrument_capture.

Focused matrix: 6 levels x 8 scenarios x 8 seeds = 384 episodes (~20 min).
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from embedded_sim.audit_core.schemas import INSTRUMENTATION_LEVELS
from embedded_sim.batch import _run_scenario_episode

CAPTURE_SCENARIOS = (
    "capture_theater",
    "capture_mild",
    "instrument_capture",
    "inferential_coupling",
    "grounding_silent_gap",
    "bearer_mismap",
)
HONEST_SCENARIOS = ("honest", "honest_successor")
SEEDS = tuple(range(11, 19))
T = 400


def _episode_status(scenario: str, seed: int, level: str) -> tuple[str, bool, bool]:
    run = _run_scenario_episode(
        scenario, seed, T=T, instrumentation=level, redteam_strategy="none", substrate="python"
    )
    status = str(run.get("in_sim", {}).get("cci_status", "unknown"))
    correct = bool(run.get("evaluation", {}).get("cci_status_correct"))
    false_pass = bool(run.get("outer", {}).get("false_pass"))
    return status, correct, false_pass


def _rate(items: list[bool]) -> float:
    return sum(items) / len(items) if items else 0.0


def main() -> None:
    t0 = time.perf_counter()
    by_level: dict[str, dict] = {}
    for level in INSTRUMENTATION_LEVELS:
        cap_false_pass: list[bool] = []
        cap_correct: list[bool] = []
        hon_pass: list[bool] = []
        hon_correct: list[bool] = []
        per_scenario: dict[str, dict] = {}
        for scenario in CAPTURE_SCENARIOS + HONEST_SCENARIOS:
            passes: list[bool] = []
            correct: list[bool] = []
            false_passes: list[bool] = []
            for seed in SEEDS:
                status, ok, fp = _episode_status(scenario, seed, level)
                passes.append(status == "passes")
                correct.append(ok)
                false_passes.append(fp)
            per_scenario[scenario] = {
                "pass_rate": _rate(passes),
                "correct_rate": _rate(correct),
                "false_pass_rate": _rate(false_passes),
                "n": len(SEEDS),
            }
            if scenario in CAPTURE_SCENARIOS:
                cap_false_pass += false_passes
                cap_correct += correct
            else:
                hon_pass += passes
                hon_correct += correct
        by_level[level] = {
            "capture_false_pass_rate": _rate(cap_false_pass),
            "capture_correct_rate": _rate(cap_correct),
            "honest_pass_rate": _rate(hon_pass),
            "honest_correct_rate": _rate(hon_correct),
            "per_scenario": per_scenario,
        }
        print(
            f"{level:>20}  cap_false_pass={by_level[level]['capture_false_pass_rate']:.3f}  "
            f"cap_correct={by_level[level]['capture_correct_rate']:.3f}  "
            f"honest_pass={by_level[level]['honest_pass_rate']:.3f}  "
            f"honest_correct={by_level[level]['honest_correct_rate']:.3f}",
            flush=True,
        )

    payload = {
        "mode": "channel_eligibility_eval",
        "T": T,
        "seeds": list(SEEDS),
        "capture_scenarios": list(CAPTURE_SCENARIOS),
        "honest_scenarios": list(HONEST_SCENARIOS),
        "runtime_seconds": round(time.perf_counter() - t0, 1),
        "by_level": by_level,
    }
    out = Path(__file__).resolve().parent / "results" / "channel_eligibility_eval.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nwrote {out} in {payload['runtime_seconds']}s")


if __name__ == "__main__":
    main()
