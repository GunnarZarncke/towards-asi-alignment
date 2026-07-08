#!/usr/bin/env python3
"""G-32 follow-up: pin down PRECISELY why S6 intervention missed the real
`{eng1, rm1}` pair (`run_llm_detector_stress_test.py`) with raw numbers,
not just the abstract "non-determinism" diagnosis.

Runs ONE probe triple (DM channel ablation targeting `eng1`) against the
SAME scenario/seed/briefings as the main stress test and prints the raw
per-actor action-code series plus the exact `ActorDiffSummary` fields
`compensation_score` is built from -- `compensation_codes` (code-set
novelty) and `tick_compensation_rate` (tick-aligned divergence). Not a
battery, not re-run automatically (real API spend each time; every call
draws a FRESH, independently-sampled triple -- see FINDINGS.md G-32's
"Root cause, pinned down" addendum for the specific numbers this script
produced on 2026-07-08 and why re-running it is expected to give
DIFFERENT numbers, which is itself the point).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.harness.llm_isolate import LLMSubprocessIsolate
from lab_sim.oracle_only.intervention_diff import action_series_from_result, cleanup_triple, diff_probe_triple, run_episode_triple
from lab_sim.oracle_only.intervention_probes import channel_ablation_probe
from run_llm_detector_stress_test import ENGINEER_BRIEFING, RELEASE_MANAGER_BRIEFING, SEED, _config

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def main() -> None:
    os.environ["LAB_SIM_LLM_MODEL"] = "gpt-4o-mini"
    os.environ["LAB_SIM_LLM_COST_BUDGET_USD"] = "0.30"
    os.environ["LAB_SIM_LLM_PROMPT_VARIANT"] = "discovery"
    os.environ["LAB_SIM_LLM_TASK_BRIEFINGS"] = json.dumps(
        {"engineer": ENGINEER_BRIEFING, "release_manager": RELEASE_MANAGER_BRIEFING}
    )

    cfg = _config()
    llm_backend = LLMSubprocessIsolate()
    agent_overrides = {"eng1": (llm_backend, "engineer"), "rm1": (llm_backend, "release_manager")}
    probe = channel_ablation_probe("dm", "eng1")

    triple = run_episode_triple(
        cfg, seed=SEED, probe=probe, backend=SubprocessIsolate(), agent_overrides=agent_overrides
    )
    report: dict = {"probe": probe.probe_id, "seed": SEED, "traces": {}, "diffs": {}}
    try:
        for label, ep in (("clean", triple.clean), ("intervened", triple.intervened), ("twin", triple.twin_control)):
            series = action_series_from_result(ep, ["eng1", "rm1"], horizon=cfg.T, depth="deep")
            report["traces"][label] = series

        diffs = diff_probe_triple(triple, probe)
        for actor in ("eng1", "rm1"):
            d = diffs[actor]
            report["diffs"][actor] = {
                "first_divergent_tick": d.first_divergent_tick,
                "post_baseline_codes": sorted(d.post_baseline_codes),
                "post_intervened_codes": sorted(d.post_intervened_codes),
                "post_twin_codes": sorted(d.post_twin_codes),
                "stall_codes": sorted(d.stall_codes),
                "compensation_codes": sorted(d.compensation_codes),
                "tick_compensation_rate": d.tick_compensation_rate,
                "compensation_score": d.compensation_score,
            }
        report["llm_cost_usd"] = round(
            sum((e.get("usage") or {}).get("estimated_usd", 0.0) for e in llm_backend.usage_log), 6
        )
    finally:
        cleanup_triple(triple)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / "llm_detector_root_cause_probe.json"
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
