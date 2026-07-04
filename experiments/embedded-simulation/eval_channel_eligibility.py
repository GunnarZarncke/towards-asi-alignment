"""Focused, powered evaluation of the Part B channel-set eligibility fix (N-10).

Pre-registered predictions (see session log 2026-07-03-channel-sets-n10-eligibility):

1. No blind false passes: on capture/violation scenarios that light_handles
   previously certified, partial levels (light/light_plus/medium_minus) issue
   pass-rate 0 (eligibility gate -> belowThreshold).
2. Certification not broken: on honest scenarios, medium/strong still pass at a
   high rate; partial levels are uncertifiable (pass-rate 0) -- the priced cost.
3. Channel-resolved detection: light_plus (has action_arbitration) flags
   inferential_coupling but still cannot certify instrument_capture.

Original focused matrix: 6 levels x 8 scenarios x 8 seeds = 384 episodes (~20 min).

**Extension (2026-07-03, Milestone v5 Phase 0):** the original 8-scenario
battery leaves a real coverage gap -- of the four verdict domains
(`channel_sets.VERDICT_DOMAINS`), only `bearer_welfare` (three times:
`instrument_capture`, `grounding_silent_gap`, `bearer_mismap`) and `routing`
(once: `inferential_coupling`) are exercised by a scenario purpose-built to
trip their detector. `lineage` (`lineage_stall_reported_uptake`, whose target
scenario is `legitimacy_theater`) and `successor`
(`successor_epoch_witness`, whose target scenario is `successor_relabel`)
have never been scenario-tested by this battery, even though the
`medium_minus_handles` majority-gate false-pass measurement in
`results/NEGATIVE_RESULTS.md` (N-10 Postscript 3) is cited as if it covered
"capture" generally.

`EXTENDED_CAPTURE_SCENARIOS`/`EXTENDED_HONEST_SCENARIOS` below add the 9
scenarios in `audit_core.schemas.HELD_OUT_SCENARIOS` not previously used by
this battery (all already classified, per `evaluate.py`'s own oracle-based
correctness rule, not a label invented for this script -- see
`MILESTONE-v5-goal-agents.md` Phase 0). One classification nuance disclosed,
not hidden: `selection_basin`'s expected verdict is not a fixed scenario-level
label -- `evaluate.py` makes it conditional on whether basin percolation
actually crosses *within* that episode (`basin_percolation_crossed or
basin_capture_fraction_max >= 0.45`); "honest-typical" here means most seeds
do not cross that threshold, not that every episode is exempt from capture
scrutiny. `correct`/`false_pass` are computed by the real pipeline either way
(oracle-based, per-episode), so the aggregate rates below are exact regardless
of this nuance -- only the *bucket a scenario is pooled into for reporting*
is a simplification.

The original 8-scenario rates are kept as their own reported group
(`capture_*`/`honest_*`, unchanged in meaning from prior runs, so historical
comparisons in `NEGATIVE_RESULTS.md` remain valid) alongside the new
9-scenario group (`extended_*`) and the union of all 17 (`combined_*`) --
extending in place would silently change what "capture_false_pass_rate"
means without flagging it.

Full matrix: 6 levels x 17 scenarios x 8 seeds = 816 episodes (~40-45 min).
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

# The 9 `HELD_OUT_SCENARIOS` not previously exercised by this battery.
# Capture-like: expected verdict is not `passes` at good instrumentation.
# Honest-like: expected verdict is `passes` at good instrumentation (with the
# `selection_basin` per-episode-conditional caveat documented above).
EXTENDED_CAPTURE_SCENARIOS = (
    "boundary_alias",
    "bundle_goodhart",
    "hidden_capability",
    "basin_lock_in",
    "successor_relabel",
    "legitimacy_theater",
)
EXTENDED_HONEST_SCENARIOS = ("alias_stress", "decoy_stress", "selection_basin")

ALL_CAPTURE_SCENARIOS = CAPTURE_SCENARIOS + EXTENDED_CAPTURE_SCENARIOS
ALL_HONEST_SCENARIOS = HONEST_SCENARIOS + EXTENDED_HONEST_SCENARIOS

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
        per_scenario: dict[str, dict] = {}
        # Per group ("original" = prior 8-scenario battery, "extended" = the
        # 9 newly-wired scenarios), track capture-side and honest-side
        # outcomes separately so summary rates never need positional slicing.
        buckets: dict[str, dict[str, list[bool]]] = {
            "original": {"cap_false_pass": [], "cap_correct": [], "hon_pass": [], "hon_correct": []},
            "extended": {"cap_false_pass": [], "cap_correct": [], "hon_pass": [], "hon_correct": []},
        }

        for scenario in ALL_CAPTURE_SCENARIOS + ALL_HONEST_SCENARIOS:
            group = "original" if scenario in CAPTURE_SCENARIOS + HONEST_SCENARIOS else "extended"
            capture_side = scenario in ALL_CAPTURE_SCENARIOS
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
            if capture_side:
                buckets[group]["cap_false_pass"] += false_passes
                buckets[group]["cap_correct"] += correct
            else:
                buckets[group]["hon_pass"] += passes
                buckets[group]["hon_correct"] += correct

        def _summary(*groups: str) -> dict[str, float]:
            cap_fp = [v for g in groups for v in buckets[g]["cap_false_pass"]]
            cap_ok = [v for g in groups for v in buckets[g]["cap_correct"]]
            hon_p = [v for g in groups for v in buckets[g]["hon_pass"]]
            hon_ok = [v for g in groups for v in buckets[g]["hon_correct"]]
            return {
                "capture_false_pass_rate": _rate(cap_fp),
                "capture_correct_rate": _rate(cap_ok),
                "honest_pass_rate": _rate(hon_p),
                "honest_correct_rate": _rate(hon_ok),
            }

        original = _summary("original")
        extended = _summary("extended")
        combined = _summary("original", "extended")

        by_level[level] = {
            "original_8_scenarios": original,
            "extended_9_scenarios": extended,
            "combined_17_scenarios": combined,
            "per_scenario": per_scenario,
        }
        print(
            f"{level:>20}  orig_cap_false_pass={original['capture_false_pass_rate']:.3f}  "
            f"ext_cap_false_pass={extended['capture_false_pass_rate']:.3f}  "
            f"orig_honest_pass={original['honest_pass_rate']:.3f}  "
            f"ext_honest_pass={extended['honest_pass_rate']:.3f}",
            flush=True,
        )

    payload = {
        "mode": "channel_eligibility_eval",
        "T": T,
        "seeds": list(SEEDS),
        "capture_scenarios_original": list(CAPTURE_SCENARIOS),
        "honest_scenarios_original": list(HONEST_SCENARIOS),
        "capture_scenarios_extended": list(EXTENDED_CAPTURE_SCENARIOS),
        "honest_scenarios_extended": list(EXTENDED_HONEST_SCENARIOS),
        "runtime_seconds": round(time.perf_counter() - t0, 1),
        "by_level": by_level,
    }
    out = Path(__file__).resolve().parent / "results" / "channel_eligibility_eval.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nwrote {out} in {payload['runtime_seconds']}s")


if __name__ == "__main__":
    main()
