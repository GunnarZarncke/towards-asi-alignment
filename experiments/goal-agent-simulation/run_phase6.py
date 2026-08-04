#!/usr/bin/env python3
"""Phase 6: responses-side honest twin, certifier capture, adversarial
weight search (`results/FINDINGS.md` GA-21/GA-22/GA-23).

Three independent follow-ups to the Phase 5 strategic review (session log
`drafts/conversation-summaries/archive/2026-07/2026-07-05-goal-agent-line-next-steps-recorded.md`), each pre-registered below BEFORE this script's first run.
Frozen Phase 1-5 artifacts are untouched; `escalation.py`'s gates,
`detectors.py`'s thresholds, and `labels.py` are unchanged throughout.

## Part A — GA-21: does the responses-side twin fix fix GA-20's false positive?

`twins.make_twin` now also replaces a spec's `responses` (if any) with a
single, full-disclosure `HONEST_TWIN_RESPONSE` (see `twins.py` module
docstring) — the missing piece GA-20 identified (the twin previously
answered escalation queries using the ORIGINAL, deceptive action's response
menu). Re-runs round 4's escalation battery (identical sampling/gates to
`run_phase4_escalation.py`/`run_phase5_followups.py`: `sample_blind_configs`
on `generated_actions_v4.json`, `protocol.EPISODE_SEEDS`, light-tier screen
score) with BOTH `select_query_steps` (v1) and `select_query_steps_v2`
(v2), using the FIXED twin rule. Pre-registered prediction: the twin
verdict-true rate under v2 drops from GA-20's recorded 0.0708 to at or below
the agent's own rate (0.0542) — since a full-disclosure response can never
itself trigger `DISCLOSE_FRACTION_GATE`'s verdict-true condition on the
twin's OWN say-so being deceptive; the frozen `resolve_response_canonical`
maps `"acknowledges"` to `"discloses"`, i.e. `n_disclosed == n_queried`
whenever the twin's honest response is drawn, so any residual twin
verdict-true rate can *only* come from the `HIGH_GATE` screen-only path
(no escalation), not from the query-and-disclose path — a structural,
not merely empirical, prediction. `run_escalation`'s RNG streams and v1's
own numbers are unaffected (only `twin_config`'s repertoire changed).

## Part B — GA-22: certifier capture

`agents.BoardPolicy`'s new `captured` mechanism (`config.BoardConfig.
capture_start`, see `agents.py` module docstring) is exercised on the
LEGACY repertoire (the only one whose `propose`/sign-off mechanics are
fully understood mechanistically, chosen for that reason, not for
convenience) using the SAME 30-config discovery-region sampling as
`run_phase1.py` (`protocol.sample_configs`), `protocol.EPISODE_SEEDS`.
Every (config, seed) pair is run TWICE: once with the config's own board
(honest, `capture_start=None`) and once with an otherwise-identical board
captured from `CAPTURE_START` (`T // 2` = step 150 of 300 — the halfway
point, a round choice with no other justification than "well past the
episode's warm-up, well before its end", fixed before this battery ran).

Pre-registered predictions (mechanism-derived, not just measured
afterward): (a) the mean number of `sign_off=1` events per episode does
NOT decrease under capture (review_proposal always approves once
captured, vs. only when `harm_ema` is low when honest — capture can only
raise the approval rate, never lower it); (b) `d5_unapproved_change`'s
fire rate drops or stays flat under capture (an approved-by-rubber-stamp
practice change no longer satisfies D5's "no sign-off before adoption"
condition, even though nothing about the change itself became more
vetted); (c) NO prediction on light-tier composite or overall severity
direction — capture removes the board's corrective RESPONSE to harm, but
`correction_active` gating also shrinks (fewer `requires_correction`
actions become available off the fixed probe schedule), so the net effect
on agent behavior is not derivable from the mechanism alone; reported as
measured, honestly undetermined in advance.

## Part C — GA-23: adversarial weight search vs. uniform sampling

`goal_sim.redteam.hill_climb_weights` (stdlib random-restart hill climbing,
full pre-registration in that module's docstring: objective, lambda,
search budget, evaluation-seed split) run against LEGACY and round 3
(`generated_actions_v3.json` — the richest, most-saturated repertoire in
this line, per GA-14) repertoires, `ADVERSARY_TOOLS` fixed (full deception
capability) for both the search and the uniform-sampling comparison
baseline (`redteam.sample_uniform_baseline`, `N_BASELINE = N_RESTARTS *
(1 + N_ITERS)` — the SAME total evaluation budget as the search gets, for
a fair comparison). Both the search winner and the baseline winner are
RE-EVALUATED on the full 8-seed `protocol.EPISODE_SEEDS` (not the 4-seed
search/baseline subset) for final reporting. Pre-registered prediction:
the search winner's final objective score is >= the baseline winner's
(search should not underperform a fixed sample it had at least as many
evaluations against) — a weak, easily-falsified claim; no prediction on
the MAGNITUDE of any gap, or on whether round 3 (already near-saturated
per GA-14/GA-8) leaves search much room to improve over uniform sampling.

Artifacts: `results/phase6.{json,md}`.
"""

from __future__ import annotations

import json
import random
import time
from dataclasses import replace
from pathlib import Path

from goal_sim.actions import LEGACY_ACTIONS, load_specs
from goal_sim.channels import project_rows
from goal_sim.config import GoalWeights
from goal_sim.detectors import d5_unapproved_change, score_detectors
from goal_sim.escalation import run_escalation, select_query_steps, select_query_steps_v2
from goal_sim.protocol import EPISODE_SEEDS, sample_configs
from goal_sim.redteam import (
    ADVERSARIAL_LAMBDA,
    ADVERSARY_TOOLS,
    EVAL_SEEDS_SEARCH,
    N_ITERS,
    N_RESTARTS,
    adversarial_objective,
    hill_climb_weights,
    sample_uniform_baseline,
)
from goal_sim.severity import severity
from goal_sim.twins import twin_config
from goal_sim.world import run_episode
from run_phase4_escalation import _configs_for_v4

RESULTS_DIR = Path(__file__).parent / "results"
GOAL_SIM_DIR = Path(__file__).parent / "goal_sim"

# --- Part A: responses-side twin, round 4 escalation, v1+v2 -----------------

FROZEN_F20_TWIN_VERDICT_TRUE_RATE_V2 = 0.0708  # results/phase5_followups.json, round4.v2


def _episode_verdicts_a(cfg, seed: int, query_selector) -> dict:
    rows = run_episode(cfg, seed)
    projected_light = project_rows(rows, "light")
    screen_score = score_detectors(projected_light)["composite"]
    exposure_weight = cfg.agent.weights.normalized().exposure
    repertoire = cfg.repertoire if cfg.repertoire is not None else LEGACY_ACTIONS
    rng = random.Random(f"{cfg.config_id}:{seed}:{query_selector.__name__}")
    outcome = run_escalation(
        rows, projected_light, repertoire, screen_score, exposure_weight, rng,
        query_selector=query_selector,
    )
    return {"severity": severity(rows)["severity"], **outcome}


def run_part_a() -> dict:
    configs = _configs_for_v4("round4")
    result: dict = {}
    for version_name, selector in (("v1", select_query_steps), ("v2", select_query_steps_v2)):
        agent_records = []
        twin_records = []
        for cfg in configs:
            t_cfg = twin_config(cfg)
            for seed in EPISODE_SEEDS:
                agent_records.append(_episode_verdicts_a(cfg, seed, selector))
                twin_records.append(_episode_verdicts_a(t_cfg, seed, selector))
        n = len(agent_records)
        result[version_name] = {
            "agent_verdict_true_rate": round(sum(1 for r in agent_records if r["verdict"]) / n, 4),
            "twin_verdict_true_rate": round(sum(1 for r in twin_records if r["verdict"]) / n, 4),
            "twin_n_disclosed_total": sum(r.get("n_disclosed", 0) for r in twin_records),
            "twin_n_queried_total": sum(r.get("n_queried", 0) for r in twin_records),
        }
    result["frozen_f20_twin_verdict_true_rate_v2"] = FROZEN_F20_TWIN_VERDICT_TRUE_RATE_V2
    result["prediction_v2_twin_rate_at_or_below_agent"] = (
        result["v2"]["twin_verdict_true_rate"] <= result["v2"]["agent_verdict_true_rate"]
    )
    return result


# --- Part B: certifier capture, legacy ---------------------------------------

CAPTURE_START = 150  # T // 2 for the default T=300


def _episode_metrics_b(cfg, seed: int) -> dict:
    rows = run_episode(cfg, seed)
    full = project_rows(rows, "full")
    light = project_rows(rows, "light")
    return {
        "severity": severity(rows)["severity"],
        "n_sign_off": sum(r["sign_off"] for r in rows),
        "d5_fires": d5_unapproved_change(full),
        "full_composite": score_detectors(full)["composite"],
        "light_composite": score_detectors(light)["composite"],
    }


def run_part_b() -> dict:
    discovery, _held_out = sample_configs()
    honest_records = []
    captured_records = []
    for cfg in discovery:
        captured_cfg = replace(cfg, board=replace(cfg.board, capture_start=CAPTURE_START))
        for seed in EPISODE_SEEDS:
            honest_records.append(_episode_metrics_b(cfg, seed))
            captured_records.append(_episode_metrics_b(captured_cfg, seed))

    def _summary(records: list[dict]) -> dict:
        n = len(records)
        return {
            "n_episodes": n,
            "mean_n_sign_off": round(sum(r["n_sign_off"] for r in records) / n, 4),
            "d5_fire_rate": round(sum(1 for r in records if r["d5_fires"]) / n, 4),
            "mean_severity": round(sum(r["severity"] for r in records) / n, 4),
            "mean_full_composite": round(sum(r["full_composite"] for r in records) / n, 4),
            "mean_light_composite": round(sum(r["light_composite"] for r in records) / n, 4),
        }

    return {
        "capture_start": CAPTURE_START,
        "honest": _summary(honest_records),
        "captured": _summary(captured_records),
    }


# --- Part C: adversarial weight search vs uniform sampling -------------------

N_BASELINE = N_RESTARTS * (1 + N_ITERS)


def run_part_c() -> dict:
    round3_specs = tuple(load_specs(GOAL_SIM_DIR / "generated_actions_v3.json"))
    result: dict = {}
    for name, repertoire in (("legacy", None), ("round3", round3_specs)):
        search = hill_climb_weights(repertoire, seed=20260705)
        baseline = sample_uniform_baseline(repertoire, seed=20260706, n=N_BASELINE)

        search_final = adversarial_objective(
            GoalWeights(**search["best_weights"]), ADVERSARY_TOOLS, repertoire, EPISODE_SEEDS
        )
        baseline_final = adversarial_objective(
            GoalWeights(**baseline["best"]["weights"]), ADVERSARY_TOOLS, repertoire, EPISODE_SEEDS
        )
        result[name] = {
            "search_weights": search["best_weights"],
            "search_score_search_seeds": search["best_score"],
            "search_score_full_seeds": round(search_final["score"], 4),
            "search_severity_full_seeds": round(search_final["mean_severity"], 4),
            "search_full_composite_full_seeds": round(search_final["mean_full_composite"], 4),
            "baseline_weights": baseline["best"]["weights"],
            "baseline_score_search_seeds": round(baseline["best"]["score"], 4),
            "baseline_mean_score_search_seeds": baseline["mean_score"],
            "baseline_score_full_seeds": round(baseline_final["score"], 4),
            "baseline_severity_full_seeds": round(baseline_final["mean_severity"], 4),
            "baseline_full_composite_full_seeds": round(baseline_final["mean_full_composite"], 4),
            "search_beats_baseline_full_seeds": search_final["score"] >= baseline_final["score"],
        }
    return result


def main() -> None:
    t0 = time.perf_counter()
    report = {
        "protocol": {
            "episode_seeds": list(EPISODE_SEEDS),
            "part_a_eval_seeds_search": list(EVAL_SEEDS_SEARCH),
            "part_b_capture_start": CAPTURE_START,
            "part_c_lambda": ADVERSARIAL_LAMBDA,
            "part_c_n_restarts": N_RESTARTS,
            "part_c_n_iters": N_ITERS,
            "part_c_n_baseline": N_BASELINE,
        }
    }
    report["part_a_responses_twin"] = run_part_a()
    report["part_b_certifier_capture"] = run_part_b()
    report["part_c_adversarial_search"] = run_part_c()
    report["timing"] = {"total_seconds": round(time.perf_counter() - t0, 2)}

    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "phase6.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS_DIR / "phase6.md").write_text(render_md(report))
    print(json.dumps({k: v for k, v in report.items() if k != "protocol"}, indent=2))
    print(f"wrote {RESULTS_DIR / 'phase6.json'}")


def render_md(report: dict) -> str:
    lines = [
        "# Phase 6 — responses-side twin, certifier capture, adversarial search",
        "",
        "Protocol pre-registered in `run_phase6.py` docstring.",
        "",
        "## Part A — round 4 escalation, fixed responses-side twin",
        "",
        "| version | agent verdict-true rate | twin verdict-true rate | twin disclosed/queried |",
        "| --- | --- | --- | --- |",
    ]
    for v in ("v1", "v2"):
        a = report["part_a_responses_twin"][v]
        lines.append(
            f"| {v} | {a['agent_verdict_true_rate']} | {a['twin_verdict_true_rate']} | "
            f"{a['twin_n_disclosed_total']}/{a['twin_n_queried_total']} |"
        )
    lines += [
        "",
        f"Frozen GA-20 (old twin rule) v2 twin verdict-true rate: "
        f"{report['part_a_responses_twin']['frozen_f20_twin_verdict_true_rate_v2']}. "
        f"Prediction (fixed twin's v2 rate <= agent's v2 rate) holds: "
        f"{report['part_a_responses_twin']['prediction_v2_twin_rate_at_or_below_agent']}.",
        "",
        "## Part B — certifier capture (legacy, capture_start="
        f"{report['part_b_certifier_capture']['capture_start']})",
        "",
        "| board | n | mean sign-offs/ep | D5 fire rate | mean severity | full composite | light composite |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for name in ("honest", "captured"):
        b = report["part_b_certifier_capture"][name]
        lines.append(
            f"| {name} | {b['n_episodes']} | {b['mean_n_sign_off']} | {b['d5_fire_rate']} | "
            f"{b['mean_severity']} | {b['mean_full_composite']} | {b['mean_light_composite']} |"
        )
    lines += [
        "",
        "## Part C — adversarial weight search vs. uniform sampling "
        f"(lambda={report['protocol']['part_c_lambda']}, "
        f"budget={report['protocol']['part_c_n_baseline']} evals each)",
        "",
        "| repertoire | search score | baseline score | search >= baseline | search severity | baseline severity |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for name, c in report["part_c_adversarial_search"].items():
        lines.append(
            f"| {name} | {c['search_score_full_seeds']} | {c['baseline_score_full_seeds']} | "
            f"{c['search_beats_baseline_full_seeds']} | {c['search_severity_full_seeds']} | "
            f"{c['baseline_severity_full_seeds']} |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
