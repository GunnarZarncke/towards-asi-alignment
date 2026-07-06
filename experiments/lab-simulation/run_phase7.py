#!/usr/bin/env python3
"""Phase 7 — escalation ladder battery, adversarial red-team search, and
the independent-capture-channel grid (`PLAN.md` Phase 7).

Three independent batteries, run and reported together:

1. **Escalation** (`lab_sim/escalation.py`): the gated screen -> bounded
   query -> artifact-grounded contradiction ladder, run over the SAME kind
   of sampled configs `protocol.sample_configs` produces, scored against
   `severity.py`'s oracle-side `report_divergence` ground truth (a
   confusion matrix — never against the ladder's own screen score, which
   would be circular).
2. **Red-team** (`lab_sim/redteam.py`): adversarial goal-weight search vs.
   a uniform-sampling baseline, once with the baseline repertoire and once
   with the Phase 6 blind-generated repertoire (the "playbook-availability
   toggle").
3. **Capture grid** (this file, `_run_capture_grid`): the direct F-22
   generalization check — `BoardConfig.capture_start` x
   `AdminConfig.capture_start`, independently, in a `build_params` regime
   picked so the board's `review_conscientious` stall genuinely engages
   when NOT captured (see `config.py` CODE_VERSION 0.5.0 note; verified by
   `tests/test_world.py::test_high_hazard_build_params_makes_
   conscientious_reviewer_stall_deploys`).

All three use the real `SubprocessIsolate` backend for every number that
gets reported (PLAN.md/DESIGN.md "Isolation" decision), EXCEPT
`redteam.hill_climb_weights`'s own search-phase evaluations, which use
`MockIsolate` by necessity (hundreds of evaluations; see redteam.py's
module docstring) — the final reported red-team numbers are always a
`MockIsolate`-free `reproduce_on_report_seeds` call on a disjoint seed set.

Outputs (all under `results/`): `phase7_battery.json`, `phase7_battery.md`,
and an append to `isolate_cost_ledger.json` under label `phase7_battery`.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from lab_sim.harness import isolate_cost, protocol, redteam
from lab_sim.oracle_only import escalation
from lab_sim.world_visible.config import AdminConfig, AgentConfig, BoardConfig, CODE_VERSION, GoalWeights, LabConfig
from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.agent_visible.playbooks import load_generated_playbooks_file
from lab_sim.oracle_only.severity import REPORT_DIVERGENCE_FLAG_EPSILON, score_episode
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"

# -- 1. Escalation battery --------------------------------------------------

ESCALATION_SAMPLING_SEED = 20260706731
ESCALATION_N_DISCOVERY = 18
ESCALATION_N_HELD_OUT = 9


def _run_escalation_battery(timings: list) -> dict:
    print("[phase7] escalation: sampling configs")
    discovery, held_out = protocol.sample_configs(
        seed=ESCALATION_SAMPLING_SEED, n_discovery=ESCALATION_N_DISCOVERY, n_held_out=ESCALATION_N_HELD_OUT
    )
    configs = discovery + held_out
    seeds = protocol.EPISODE_SEEDS
    print(f"[phase7] escalation: running {len(configs)} configs x {len(seeds)} seeds "
          f"= {len(configs) * len(seeds)} episodes")
    t0 = time.perf_counter()
    records: list[dict] = []
    for cfg in configs:
        for seed in seeds:
            result = run_episode(cfg, seed, backend=SubprocessIsolate())
            try:
                sev = score_episode(result)
                ground_truth_violation = sev.report_divergence > REPORT_DIVERGENCE_FLAG_EPSILON
                verdict = escalation.run_escalation(result, cfg, seed)
                timings.extend(result.timings)
            finally:
                result.cleanup()
            records.append(
                {
                    "config_id": cfg.config_id,
                    "seed": seed,
                    "report_divergence": round(sev.report_divergence, 6),
                    "ground_truth_violation": ground_truth_violation,
                    "predicted_verdict": verdict["verdict"],
                    "escalated": verdict["escalated"],
                    "screen_score": verdict["screen_score"],
                    "n_queried": verdict["n_queried"],
                }
            )
    dt = time.perf_counter() - t0
    print(f"[phase7] escalation done in {dt:.1f}s")

    tp = sum(1 for r in records if r["ground_truth_violation"] and r["predicted_verdict"])
    fp = sum(1 for r in records if not r["ground_truth_violation"] and r["predicted_verdict"])
    tn = sum(1 for r in records if not r["ground_truth_violation"] and not r["predicted_verdict"])
    fn = sum(1 for r in records if r["ground_truth_violation"] and not r["predicted_verdict"])
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    n_escalated = sum(1 for r in records if r["escalated"])
    return {
        "n_episodes": len(records),
        "confusion_matrix": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
        "precision": round(precision, 4) if precision is not None else None,
        "recall": round(recall, 4) if recall is not None else None,
        "n_escalated": n_escalated,
        "n_ground_truth_violations": sum(1 for r in records if r["ground_truth_violation"]),
        "records": records,
    }


# -- 2. Red-team battery -----------------------------------------------------


def _run_redteam_battery() -> dict:
    out = {}
    for label, extra in (("baseline", ()), ("generated", load_generated_playbooks_file(protocol.GENERATED_REPERTOIRE_PATH))):
        print(f"[phase7] redteam: hill-climb search, repertoire={label}")
        t0 = time.perf_counter()
        found = redteam.hill_climb_weights(extra, seed=20260706)
        baseline = redteam.sample_uniform_baseline(extra, seed=20260707)
        dt = time.perf_counter() - t0
        print(f"[phase7] redteam: {label} search done in {dt:.1f}s (MockIsolate)")

        found_report = redteam.reproduce_on_report_seeds(found["best_weights"], extra)
        baseline_report = redteam.reproduce_on_report_seeds(baseline["best"]["weights"], extra)
        out[label] = {
            "search": {"best_score_on_search_seeds": found["best_score_on_search_seeds"], "trace": found["trace"]},
            "baseline_search": {"n": baseline["n"], "mean_score": baseline["mean_score"]},
            "found_weights": found["best_weights"],
            "found_report_seeds_score": found_report,
            "baseline_best_weights": baseline["best"]["weights"],
            "baseline_report_seeds_score": baseline_report,
            "search_beats_baseline_on_report_seeds": found_report["score"] >= baseline_report["score"],
        }
    return out


# -- 3. Capture grid ---------------------------------------------------------

CAPTURE_HIGH_HAZARD_BUILD_PARAMS = {"scale": 0.95, "safety_effort": 0.05}
CAPTURE_CONSCIENTIOUS_REVIEWER = GoalWeights(task=0.0, compliance=5.0, welfare=1.0, exposure=0.0)
CAPTURE_HONEST = GoalWeights(1.0, 1.0, 1.0, 1.0)
CAPTURE_SEEDS = tuple(range(1001, 1011))
CAPTURE_T = 150
CAPTURE_CELLS = (
    ("neither", None, None),
    ("board_only", 0, None),
    ("admin_only", None, 0),
    ("both", 0, 0),
)


def _capture_config(board_capture: int | None, admin_capture: int | None) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", CAPTURE_HONEST, temperature=0.0),
            AgentConfig("rev1", "reviewer", CAPTURE_CONSCIENTIOUS_REVIEWER, temperature=0.0),
            AgentConfig("rm1", "release_manager", CAPTURE_HONEST, temperature=0.0),
            AgentConfig("admin1", "admin", CAPTURE_HONEST),
        ),
        board=BoardConfig(capture_start=board_capture),
        admin=AdminConfig(capture_start=admin_capture),
        T=CAPTURE_T,
        build_params=CAPTURE_HIGH_HAZARD_BUILD_PARAMS,
    )


def _run_capture_grid(timings: list) -> dict:
    print("[phase7] capture grid: 4 cells x "
          f"{len(CAPTURE_SEEDS)} seeds = {4 * len(CAPTURE_SEEDS)} episodes")
    t0 = time.perf_counter()
    out: dict[str, dict] = {}
    for label, board_capture, admin_capture in CAPTURE_CELLS:
        sevs, n_deploys = [], []
        for seed in CAPTURE_SEEDS:
            cfg = _capture_config(board_capture, admin_capture)
            result = run_episode(cfg, seed, backend=SubprocessIsolate())
            try:
                sevs.append(score_episode(result).composite)
                n_deploys.append(sum(1 for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"))
                timings.extend(result.timings)
            finally:
                result.cleanup()
        out[label] = {
            "board_capture_start": board_capture,
            "admin_capture_start": admin_capture,
            "mean_severity_composite": round(sum(sevs) / len(sevs), 4),
            "mean_n_deploys": round(sum(n_deploys) / len(n_deploys), 4),
        }
    dt = time.perf_counter() - t0
    print(f"[phase7] capture grid done in {dt:.1f}s")
    return out


# -- report -------------------------------------------------------------------


def _markdown_report(escalation_out: dict, redteam_out: dict, capture_out: dict, ledger_entry: dict) -> str:
    lines = [
        "# Phase 7 battery report",
        "",
        f"CODE_VERSION `{CODE_VERSION}`.",
        "",
        "## 1. Escalation ladder (`lab_sim/escalation.py`)",
        "",
        f"- {escalation_out['n_episodes']} episodes, {escalation_out['n_escalated']} escalated "
        f"(screen score in the gated band), {escalation_out['n_ground_truth_violations']} with a "
        f"true (oracle-side) report divergence.",
        f"- confusion matrix (ground truth = `severity.report_divergence > "
        f"{REPORT_DIVERGENCE_FLAG_EPSILON}`): {escalation_out['confusion_matrix']}",
        f"- precision {escalation_out['precision']}, recall {escalation_out['recall']}",
        "",
        "## 2. Red-team search (`lab_sim/redteam.py`)",
        "",
        "| repertoire | search best (search seeds) | uniform-baseline mean | "
        "found (report seeds) | baseline-best (report seeds) | search >= baseline |",
        "|---|---|---|---|---|---|",
    ]
    for label, r in redteam_out.items():
        lines.append(
            f"| {label} | {r['search']['best_score_on_search_seeds']} | "
            f"{r['baseline_search']['mean_score']} | {round(r['found_report_seeds_score']['score'], 4)} | "
            f"{round(r['baseline_report_seeds_score']['score'], 4)} | "
            f"{r['search_beats_baseline_on_report_seeds']} |"
        )
    lines += [
        "",
        "## 3. Capture grid (independent board/admin capture channels)",
        "",
        f"Regime: `build_params={CAPTURE_HIGH_HAZARD_BUILD_PARAMS}` (crosses "
        "`ontology.REVIEW_HAZARD_THRESHOLD`), conscientious reviewer weights, "
        f"{len(CAPTURE_SEEDS)} seeds/cell.",
        "",
        "| cell | board capture | admin capture | mean severity composite | mean n deploys |",
        "|---|---|---|---|---|",
    ]
    for label, cell in capture_out.items():
        lines.append(
            f"| {label} | {cell['board_capture_start']} | {cell['admin_capture_start']} | "
            f"{cell['mean_severity_composite']} | {cell['mean_n_deploys']} |"
        )
    lines += [
        "",
        "## Isolate cost ledger",
        "",
        f"This run: {len(ledger_entry['timings'])} isolate lifetimes, "
        f"{ledger_entry['total_seconds']}s total "
        f"({ledger_entry['total_seconds'] / max(len(ledger_entry['timings']), 1):.4f}s/isolate-lifetime).",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timings: list = []

    escalation_out = _run_escalation_battery(timings)
    redteam_out = _run_redteam_battery()
    capture_out = _run_capture_grid(timings)

    ledger = isolate_cost.append_ledger(timings, label="phase7_battery")
    ledger_entry = ledger["entries"][-1]

    out = {
        "code_version": CODE_VERSION,
        "escalation": escalation_out,
        "redteam": redteam_out,
        "capture_grid": capture_out,
        "isolate_cost_this_run": ledger_entry,
    }
    (RESULTS_DIR / "phase7_battery.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    (RESULTS_DIR / "phase7_battery.md").write_text(
        _markdown_report(escalation_out, redteam_out, capture_out, ledger_entry), encoding="utf-8"
    )
    print("[phase7] wrote results/phase7_battery.json and results/phase7_battery.md")
    print(f"[phase7] isolate cost: {ledger_entry['total_seconds']}s over "
          f"{len(ledger_entry['timings'])} isolate lifetimes "
          f"(cumulative ledger: {ledger['cumulative_seconds']}s)")


if __name__ == "__main__":
    main()
