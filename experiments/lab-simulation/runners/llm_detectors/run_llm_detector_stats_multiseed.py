#!/usr/bin/env python3
"""Multi-seed real-LLM validation for ``discovered_units_intervention_stats``.

Same dm_coordinated_pair scenario as LS-32/LS-33; pre-registered seeds below.
Reports per-seed exact/merge rates and which channel probe drove merges.

Real OpenAI spend. Progress logged per seed (AGENTS.md).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runners._paths import EXTERNAL_DIR, LAB_SIM_ROOT, REPO_ROOT, RESULTS_DIR

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
from runners.llm_detectors.run_llm_detector_stress_test import (
    ENGINEER_BRIEFING,
    RELEASE_MANAGER_BRIEFING,
    TRUE_PAIR,
    _config,
    _pair_metrics,
)
from runners.llm_discovery.common import record_cost_ledger, total_cost_usd

MODEL = "gpt-4o-mini"
COST_BUDGET_USD_PER_EPISODE = "0.30"
K_CLEAN_REPLICATES = 4
SEEDS = (20002, 20004, 20006, 20008, 20010)


def _channel_merge_drivers(diagnostics: dict) -> dict[str, list[str]]:
    """Which actors cleared compensates on each channel probe."""
    channel = diagnostics.get("channel") or {}
    out: dict[str, list[str]] = {}
    for probe_id, actors in channel.items():
        out[probe_id] = sorted(a for a, d in actors.items() if d.get("compensates"))
    return out


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    os.environ["LAB_SIM_LLM_MODEL"] = MODEL
    os.environ["LAB_SIM_LLM_COST_BUDGET_USD"] = COST_BUDGET_USD_PER_EPISODE
    os.environ["LAB_SIM_LLM_PROMPT_VARIANT"] = "discovery"
    os.environ["LAB_SIM_LLM_TASK_BRIEFINGS"] = json.dumps(
        {"engineer": ENGINEER_BRIEFING, "release_manager": RELEASE_MANAGER_BRIEFING}
    )

    cfg = _config()
    t0 = datetime.now(timezone.utc)
    per_seed: list[dict] = []
    total_episodes = 0
    total_cost = 0.0

    for i, seed in enumerate(SEEDS, start=1):
        print(f"[stats-multiseed] [{i}/{len(SEEDS)}] seed={seed} starting...")
        llm_backend = LLMSubprocessIsolate()
        agent_overrides = {"eng1": (llm_backend, "engineer"), "rm1": (llm_backend, "release_manager")}
        real = run_episode(cfg, seed=seed, backend=SubprocessIsolate(), agent_overrides=agent_overrides)
        diagnostics: dict = {}
        try:
            heuristic = discovered_units(real, tier="deep")
            stats_detector = discovered_units_intervention_stats(
                real, cfg, seed,
                backend=SubprocessIsolate(),
                agent_overrides=agent_overrides,
                k_clean_replicates=K_CLEAN_REPLICATES,
                diagnostics=diagnostics,
            )
            row = {
                "seed": seed,
                "heuristic_pair_metrics": _pair_metrics(heuristic, TRUE_PAIR),
                "stats_detector_pair_metrics": _pair_metrics(stats_detector, TRUE_PAIR),
                "channel_merge_drivers": _channel_merge_drivers(diagnostics),
                "n_llm_episodes": len(llm_backend.usage_log),
                "llm_cost_usd": total_cost_usd(llm_backend.usage_log),
            }
        finally:
            record_cost_ledger(f"llm_detector_stats_multiseed_seed{seed}", llm_backend.usage_log, model=MODEL)
            real.cleanup()

        total_episodes += row["n_llm_episodes"]
        total_cost += row["llm_cost_usd"]
        per_seed.append(row)
        print(
            f"[stats-multiseed] [{i}/{len(SEEDS)}] seed={seed} "
            f"exact={row['stats_detector_pair_metrics']['exact']} "
            f"drivers={row['channel_merge_drivers']} cost=${row['llm_cost_usd']:.4f}"
        )

    exact_rate = sum(1 for r in per_seed if r["stats_detector_pair_metrics"]["exact"]) / len(per_seed)
    heuristic_exact_rate = sum(1 for r in per_seed if r["heuristic_pair_metrics"]["exact"]) / len(per_seed)

    report = {
        "code_version": CODE_VERSION,
        "generated_at": t0.isoformat(),
        "scenario": "dm_coordinated_pair",
        "seeds": list(SEEDS),
        "k_clean_replicates": K_CLEAN_REPLICATES,
        "true_pair": list(TRUE_PAIR),
        "per_seed": per_seed,
        "summary": {
            "heuristic_exact_rate": heuristic_exact_rate,
            "stats_detector_exact_rate": exact_rate,
            "total_llm_episodes": total_episodes,
            "total_llm_cost_usd": round(total_cost, 6),
        },
    }

    out_path = RESULTS_DIR / "llm_detector_stats_multiseed.json"
    out_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    md = [
        "# LLM stats-detector multi-seed validation",
        "",
        f"Generated {report['generated_at']} at {report['code_version']}.",
        f"Seeds {list(SEEDS)}, k_clean_replicates={K_CLEAN_REPLICATES}.",
        "",
        f"Heuristic exact rate: {heuristic_exact_rate:.2f}",
        f"Stats detector exact rate: {exact_rate:.2f}",
        "",
        f"Total LLM episodes: {total_episodes}, cost ${total_cost:.4f}.",
    ]
    (RESULTS_DIR / "llm_detector_stats_multiseed.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[stats-multiseed] summary exact_rate={exact_rate:.2f} total_cost=${total_cost:.4f}")
    print(f"[stats-multiseed] wrote {out_path}")


if __name__ == "__main__":
    main()
