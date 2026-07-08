#!/usr/bin/env python3
"""G-33 follow-up: 3+-actor LLM stress test for untargeted-probe ripple risk.

Uses ``committee_with_informal_chatter_config`` (eng1 + rev1/rev2 committee +
rm1): true unit ``{rev1, rev2}``; eng1 posts informal board chatter
(scripted); rm1 is a non-coordinating pipeline actor (scripted). Both LLM
reviewers coordinate via board; the question is whether channel-ablation
probes (especially board) falsely flag eng1/rm1 as compensators and whether
the frozen S6 ripple guard (``classify_ablation_compensators``) correctly
labels them.

Real OpenAI spend. Progress logged per seed/step (AGENTS.md).
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness.ecology import committee_with_informal_chatter_config
from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.harness.llm_isolate import LLMSubprocessIsolate
from lab_sim.oracle_only.intervention_stats import discovered_units_intervention_stats
from lab_sim.oracle_only.uad import discovered_units
from lab_sim.oracle_only.uad_intervention import discovered_units_intervention
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.world_visible.world import run_episode
from run_llm_detector_stress_test import _pair_metrics
from run_llm_discovery_committee import REVIEWER_BRIEFING
from run_llm_discovery_common import record_cost_ledger, total_cost_usd

RESULTS_DIR = Path(__file__).resolve().parent / "results"
MODEL = "gpt-4o-mini"
COST_BUDGET_USD_PER_EPISODE = "0.30"
K_CLEAN_REPLICATES = 4
SEED = 20003
T = 35
TRUE_PAIR = ("rev1", "rev2")


def _config():
    return committee_with_informal_chatter_config(T=T)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    os.environ["LAB_SIM_LLM_MODEL"] = MODEL
    os.environ["LAB_SIM_LLM_COST_BUDGET_USD"] = COST_BUDGET_USD_PER_EPISODE
    os.environ["LAB_SIM_LLM_PROMPT_VARIANT"] = "discovery"
    os.environ["LAB_SIM_LLM_TASK_BRIEFINGS"] = json.dumps({"reviewer": REVIEWER_BRIEFING})

    cfg = _config()
    llm_backend = LLMSubprocessIsolate()
    agent_overrides = {"rev1": (llm_backend, "reviewer"), "rev2": (llm_backend, "reviewer")}

    print(f"[committee-stress] seed={SEED} scenario=committee_informal_chatter true_pair={TRUE_PAIR}")
    t0 = datetime.now(timezone.utc)
    print("[committee-stress] [1/4] running real episode...")
    real = run_episode(cfg, seed=SEED, backend=SubprocessIsolate(), agent_overrides=agent_overrides)
    ablation_diagnostics: dict = {}
    stats_diagnostics: dict = {}
    try:
        print("[committee-stress] [2/4] heuristic discovery...")
        heuristic = discovered_units(real, tier="deep")
        print("[committee-stress] [3/4] frozen S6 intervention (+ ripple diagnostics)...")
        intervention = discovered_units_intervention(
            real, cfg, SEED,
            backend=SubprocessIsolate(),
            agent_overrides=agent_overrides,
            ablation_diagnostics=ablation_diagnostics,
        )
        print("[committee-stress] [4/4] noise-tolerant stats detector...")
        stats_detector = discovered_units_intervention_stats(
            real, cfg, SEED,
            backend=SubprocessIsolate(),
            agent_overrides=agent_overrides,
            k_clean_replicates=K_CLEAN_REPLICATES,
            diagnostics=stats_diagnostics,
        )

        report = {
            "code_version": CODE_VERSION,
            "generated_at": t0.isoformat(),
            "scenario": "committee_with_informal_chatter",
            "seed": SEED,
            "k_clean_replicates": K_CLEAN_REPLICATES,
            "true_units": {"review_committee": list(TRUE_PAIR),
                            "note": "eng1/rm1 are bystanders for ripple testing"},
            "heuristic_discovered": {k: list(v) for k, v in heuristic.items()},
            "heuristic_pair_metrics": _pair_metrics(heuristic, TRUE_PAIR),
            "intervention_discovered": {k: list(v) for k, v in intervention.items()},
            "intervention_pair_metrics": _pair_metrics(intervention, TRUE_PAIR),
            "ablation_diagnostics": ablation_diagnostics,
            "stats_detector_discovered": {k: list(v) for k, v in stats_detector.items()},
            "stats_detector_pair_metrics": _pair_metrics(stats_detector, TRUE_PAIR),
            "stats_diagnostics": stats_diagnostics,
            "n_llm_episodes_spawned": len(llm_backend.usage_log),
            "llm_cost_usd": total_cost_usd(llm_backend.usage_log),
        }
    finally:
        record_cost_ledger("llm_detector_committee_stress_test", llm_backend.usage_log, model=MODEL)
        real.cleanup()

    out_path = RESULTS_DIR / "llm_detector_committee_stress_test.json"
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    md = [
        "# LLM committee ripple stress test (G-33 follow-up)",
        "",
        f"Generated {report['generated_at']} at {report['code_version']}.",
        f"Seed {SEED}, `committee_with_informal_chatter`: LLM reviewers {list(TRUE_PAIR)},",
        "scripted eng1 (chatty) + rm1 (bystander).",
        "",
        f"Heuristic: {report['heuristic_pair_metrics']}",
        f"Frozen S6: {report['intervention_pair_metrics']}",
        f"Stats S6: {report['stats_detector_pair_metrics']}",
        "",
        f"Ripple diagnostics (frozen S6): {report['ablation_diagnostics']}",
        "",
        f"LLM episodes: {report['n_llm_episodes_spawned']}, cost ${report['llm_cost_usd']:.4f}.",
    ]
    (RESULTS_DIR / "llm_detector_committee_stress_test.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(
        f"[committee-stress] heuristic={report['heuristic_pair_metrics']} "
        f"intervention={report['intervention_pair_metrics']} "
        f"stats={report['stats_detector_pair_metrics']} "
        f"ripple={report['ablation_diagnostics']} "
        f"cost=${report['llm_cost_usd']:.4f}"
    )
    print(f"[committee-stress] wrote {out_path}")


if __name__ == "__main__":
    main()
