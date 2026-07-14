#!/usr/bin/env python3
"""LS-32 follow-up (FINDINGS.md LS-33): does the noise-tolerant, null-
calibrated `intervention_stats.discovered_units_intervention_stats`
detect the real `{eng1, rm1}` DM-coordinated pair where the frozen,
fixed-threshold S6 `discovered_units_intervention` missed it (LS-32)?

Reuses the EXACT scenario, briefings, and seed as
`run_llm_detector_stress_test.py` (itself reused from
`run_llm_discovery_dm_pair.py`, LS-21) -- same episode conditions,
different (statistically rebased) detector, for a like-for-like
before/after comparison.

Cost/scope, stated up front: this is ONE scenario, ONE seed, with
`k_clean_replicates=4` (pre-registered but NOT battery-validated --
see `intervention_stats.py`'s module docstring, "Pre-registration, not
a freeze"). Real OpenAI spend: `k_clean_replicates` (shared null,
4 episodes) + 5 probe episodes (2 actor-directed + 3 channel-ablation;
twin runs never call the LLM) = 9 total live-LLM episodes, versus the
original stress test's 11 -- fewer, because the null is computed once
and shared across every probe instead of one triple per probe.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.harness.llm_isolate import LLMSubprocessIsolate
from lab_sim.oracle_only.intervention_stats import discovered_units_intervention_stats
from lab_sim.oracle_only.uad import discovered_units
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.world_visible.world import run_episode
from run_llm_detector_stress_test import ENGINEER_BRIEFING, RELEASE_MANAGER_BRIEFING, SEED, TRUE_PAIR, _config, _pair_metrics
from run_llm_discovery_common import record_cost_ledger, total_cost_usd

RESULTS_DIR = Path(__file__).resolve().parent / "results"
MODEL = "gpt-4o-mini"
COST_BUDGET_USD_PER_EPISODE = "0.30"
K_CLEAN_REPLICATES = 4


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    os.environ["LAB_SIM_LLM_MODEL"] = MODEL
    os.environ["LAB_SIM_LLM_COST_BUDGET_USD"] = COST_BUDGET_USD_PER_EPISODE
    os.environ["LAB_SIM_LLM_PROMPT_VARIANT"] = "discovery"
    os.environ["LAB_SIM_LLM_TASK_BRIEFINGS"] = json.dumps(
        {"engineer": ENGINEER_BRIEFING, "release_manager": RELEASE_MANAGER_BRIEFING}
    )

    cfg = _config()
    llm_backend = LLMSubprocessIsolate()
    agent_overrides = {"eng1": (llm_backend, "engineer"), "rm1": (llm_backend, "release_manager")}

    t0 = datetime.now(timezone.utc)
    real = run_episode(cfg, seed=SEED, backend=SubprocessIsolate(), agent_overrides=agent_overrides)
    diagnostics: dict = {}
    try:
        heuristic = discovered_units(real, tier="deep")
        stats_detector = discovered_units_intervention_stats(
            real, cfg, SEED,
            backend=SubprocessIsolate(),
            agent_overrides=agent_overrides,
            k_clean_replicates=K_CLEAN_REPLICATES,
            diagnostics=diagnostics,
        )

        report = {
            "code_version": CODE_VERSION,
            "generated_at": t0.isoformat(),
            "scenario": "dm_coordinated_pair (reused from run_llm_detector_stress_test.py / LS-21 / LS-32)",
            "seed": SEED,
            "k_clean_replicates": K_CLEAN_REPLICATES,
            "true_units": {"release_pair": list(TRUE_PAIR)},
            "heuristic_discovered": {k: list(v) for k, v in heuristic.items()},
            "heuristic_pair_metrics": _pair_metrics(heuristic, TRUE_PAIR),
            "stats_detector_discovered": {k: list(v) for k, v in stats_detector.items()},
            "stats_detector_pair_metrics": _pair_metrics(stats_detector, TRUE_PAIR),
            "diagnostics": diagnostics,
            "n_llm_episodes_spawned": len(llm_backend.usage_log),
            "llm_cost_usd": total_cost_usd(llm_backend.usage_log),
        }
    finally:
        record_cost_ledger("llm_detector_stats_validation", llm_backend.usage_log, model=MODEL)
        real.cleanup()

    out_path = RESULTS_DIR / "llm_detector_stats_validation.json"
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    md_lines = [
        "# LLM detector stats validation (LS-32 follow-up, LS-33)",
        "",
        f"Generated {report['generated_at']} at {report['code_version']}. Same scenario/seed as",
        "`run_llm_detector_stress_test.py` (LS-32); noise-tolerant `discovered_units_intervention_stats`",
        f"in place of the frozen fixed-threshold S6 detector. k_clean_replicates={K_CLEAN_REPLICATES}.",
        "",
        f"Heuristic (`uad.py`, passive): {report['heuristic_pair_metrics']}",
        "",
        f"Noise-tolerant S6 (`intervention_stats`): {report['stats_detector_pair_metrics']}",
        "",
        f"LLM episodes spawned: {report['n_llm_episodes_spawned']}, total cost ${report['llm_cost_usd']:.4f}.",
    ]
    (RESULTS_DIR / "llm_detector_stats_validation.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(
        f"[llm-detector-stats-validation] heuristic={report['heuristic_pair_metrics']} "
        f"stats_detector={report['stats_detector_pair_metrics']} "
        f"episodes={report['n_llm_episodes_spawned']} cost=${report['llm_cost_usd']:.4f}"
    )
    print(f"[llm-detector-stats-validation] wrote {out_path}")


if __name__ == "__main__":
    main()
