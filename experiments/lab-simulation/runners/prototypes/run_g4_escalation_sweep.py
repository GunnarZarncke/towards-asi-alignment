#!/usr/bin/env python3
"""LS-4 follow-up: escalation query-budget sweep (K_QUERIES).

Re-runs the Phase 7 escalation battery configs at K in {1, 2, 3, 5, 7, 10}
and reports precision/recall vs oracle ``report_divergence``. Pre-registered
before run; does not change ``escalation.K_QUERIES`` default (still 3).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runners._paths import EXTERNAL_DIR, LAB_SIM_ROOT, REPO_ROOT, RESULTS_DIR

import json
import time
from pathlib import Path

from lab_sim.harness import protocol
from lab_sim.oracle_only import escalation
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.oracle_only.severity import REPORT_DIVERGENCE_FLAG_EPSILON, score_episode
from lab_sim.world_visible.world import run_episode


ESCALATION_SAMPLING_SEED = 20260706731
ESCALATION_N_DISCOVERY = 18
ESCALATION_N_HELD_OUT = 9
K_VALUES = (1, 2, 3, 5, 7, 10)


def _confusion(records: list[dict]) -> dict:
    tp = sum(1 for r in records if r["ground_truth_violation"] and r["verdict"])
    fn = sum(1 for r in records if r["ground_truth_violation"] and not r["verdict"])
    fp = sum(1 for r in records if not r["ground_truth_violation"] and r["verdict"])
    tn = sum(1 for r in records if not r["ground_truth_violation"] and not r["verdict"])
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    return {
        "tp": tp, "fn": fn, "fp": fp, "tn": tn,
        "precision": round(precision, 4) if precision is not None else None,
        "recall": round(recall, 4) if recall is not None else None,
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    discovery, held_out = protocol.sample_configs(
        seed=ESCALATION_SAMPLING_SEED,
        n_discovery=ESCALATION_N_DISCOVERY,
        n_held_out=ESCALATION_N_HELD_OUT,
    )
    configs = discovery + held_out
    seeds = protocol.EPISODE_SEEDS

    sweep: dict[str, dict] = {str(k): {"k": k, "records": []} for k in K_VALUES}
    t0 = time.perf_counter()
    for cfg in configs:
        for seed in seeds:
            result = run_episode(cfg, seed, backend=SubprocessIsolate())
            try:
                sev = score_episode(result)
                ground_truth = sev.report_divergence > REPORT_DIVERGENCE_FLAG_EPSILON
                for k in K_VALUES:
                    verdict = escalation.run_escalation(result, cfg, seed, k=k)
                    sweep[str(k)]["records"].append(
                        {"ground_truth_violation": ground_truth, "verdict": verdict["verdict"]}
                    )
            finally:
                result.cleanup()

    for k in K_VALUES:
        records = sweep[str(k)]["records"]
        sweep[str(k)] = {"k": k, "n_episodes": len(records), **_confusion(records)}

    dt = time.perf_counter() - t0
    out = {"code_version": CODE_VERSION, "k_values": list(K_VALUES), "sweep": sweep, "wall_seconds": round(dt, 2)}
    (RESULTS_DIR / "g4_escalation_sweep.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")

    n_episodes = sweep[str(K_VALUES[0])]["n_episodes"]
    lines = [
        "# LS-4 escalation query-budget sweep",
        "",
        f"CODE_VERSION `{CODE_VERSION}`. {n_episodes} episodes, K in {list(K_VALUES)}.",
        "",
        "| K | precision | recall | TP | FN | FP | TN |",
        "|---|---|---|---|---|---|---|",
    ]
    for k in K_VALUES:
        row = sweep[str(k)]
        lines.append(
            f"| {k} | {row['precision']} | {row['recall']} | {row['tp']} | {row['fn']} | {row['fp']} | {row['tn']} |"
        )
    lines.append("")
    (RESULTS_DIR / "g4_escalation_sweep.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[g4] wrote results/g4_escalation_sweep.json ({dt:.1f}s)")


if __name__ == "__main__":
    main()
