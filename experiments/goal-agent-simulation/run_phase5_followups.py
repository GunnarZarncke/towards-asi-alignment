#!/usr/bin/env python3
"""Phase 5: GA-16/GA-17 follow-ups (see `results/FINDINGS.md`).

PRE-REGISTERED PROTOCOL — fixed 2026-07-05 before this script was first run,
after `detectors.light_deception_composite` and `escalation.
select_query_steps_v2` were both frozen, but before any Phase 5 episode was
executed. Nothing below is tuned after seeing output; both parts report
whatever comes out, including a null or reversed result.

## Part A — GA-16: does the negative light-tier twin gap trace to d2?

GA-16 found the light-tier composite's honest-twin gap runs NEGATIVE in 3/4
repertoires (round1/round2/round3) and attributed this, from mechanism
reasoning, to `d2_probe_noncompliance` firing on the twin's own *visible*
defiance rather than to any failure of the reporting-divergence detectors
(`d1`/`d1b`). This part tests that diagnosis instead of just asserting it:

- **Repertoires / sampling**: identical to `run_phase4_ranking.py`'s Phase
  4b (legacy, round1, round2, round3; 30 configs x 8 `protocol.
  EPISODE_SEEDS`, `twins.twin_config` paired by seed).
- **Metric**: per-detector twin gap (agent minus twin) for `d1_score`,
  `d1b_score`, `d2_score`, and the new `light_deception_composite`
  (equal-weight mean of `d1_score`/`d1b_score` only), each with mean gap
  and fraction-positive, same reporting shape as Phase 4b.
- **Pre-registered prediction**: the negative light-tier composite gap is
  driven by `d2` (its own gap negative); `d1`/`d1b` gaps, and therefore
  `light_deception_composite`'s gap, are non-negative on average in every
  one of the four repertoires. A negative `light_deception_composite` gap
  in any repertoire falsifies the diagnosis for that repertoire.
- **No re-fitting**: `d1_score`/`d1b_score`/`d2_score`/
  `light_deception_composite` are used exactly as frozen.

## Part B — GA-17: does a broader query-selection signal fix the blind spot?

GA-17 found the escalation ladder's query-and-disclose pathway was never
once decisive in the Phase 4c battery: rounds 1-3 predate the response
schema by design (contrast condition), and round 4's own deceptive
mechanisms never tripped v1's single structural signal
(`escalation.select_query_steps`), so `mean_n_queried_when_escalated` was
exactly 0.0 for round 4. This part re-runs the SAME battery with
`select_query_steps_v2` (three signals in a fixed priority order, see
`escalation.py` module docstring) alongside the frozen v1, side by side:

- **Repertoires / sampling**: identical to `run_phase4_escalation.py`
  (legacy, round1-4; 30 configs x 8 seeds, light-tier screen score, gates
  `LOW_GATE`/`HIGH_GATE`/`K_QUERIES`/`DISCLOSE_FRACTION_GATE` UNCHANGED).
- **Queryability diagnostic**: per repertoire, the fraction of (agent)
  episodes with >= 1 queryable step under v1 and under v2, computed
  independently of the screen-score gate (i.e. "does this repertoire have
  anything to ask about at all") — the pre-check GA-17 said was missing.
- **RNG**: v1 uses the SAME seed string as Phase 4c
  (`f"{config_id}:{seed}"`, so v1's verdicts here reproduce Phase 4c's
  frozen numbers exactly, as a cross-check); v2 uses an independent stream
  (`f"{config_id}:{seed}:v2"`) so its response draws never perturb v1's.
- **Pre-registered predictions** (round 4 specifically): (a) v2 gets a
  nonzero `mean_n_queried_when_escalated` where v1 got 0.0; (b) mean
  severity | verdict=True > mean severity | verdict=False under v2; (c)
  twin verdict-true rate stays at or below the agent's own rate under v2.
- **No re-fitting**: `escalation.py`'s gates, `select_query_steps`, and
  `select_query_steps_v2` are used exactly as frozen; v1's own numbers are
  not touched (`run_phase4_escalation.py`'s artifacts are not overwritten).

Artifacts: `results/phase5_followups.{json,md}`.
"""

from __future__ import annotations

import json
import random
import time
from pathlib import Path

from goal_sim.actions import LEGACY_ACTIONS
from goal_sim.channels import project_rows
from goal_sim.detectors import (
    d1_score,
    d1b_score,
    d2_score,
    light_deception_composite,
    score_detectors,
)
from goal_sim.escalation import (
    DISCLOSE_FRACTION_GATE,
    HIGH_GATE,
    K_QUERIES,
    LOW_GATE,
    run_escalation,
    select_query_steps,
    select_query_steps_v2,
)
from goal_sim.info import spearman_correlation
from goal_sim.protocol import EPISODE_SEEDS
from goal_sim.severity import severity
from goal_sim.twins import twin_config
from goal_sim.world import run_episode
from run_phase4_escalation import _configs_for_v4
from run_phase4_ranking import N_CONFIGS, _configs_for

RESULTS_DIR = Path(__file__).parent / "results"

PART_A_REPERTOIRES = ("legacy", "round1", "round2", "round3")
PART_B_REPERTOIRES = ("legacy", "round1", "round2", "round3", "round4")
DETECTOR_KEYS = ("d1", "d1b", "d2", "light_deception")


# --- Part A: per-detector twin-gap decomposition ---------------------------


def _episode_detector_record(cfg, seed: int) -> dict:
    rows = run_episode(cfg, seed)
    projected = project_rows(rows, "light")
    return {
        "d1": d1_score(projected),
        "d1b": d1b_score(projected),
        "d2": d2_score(projected),
        "light_deception": light_deception_composite(projected),
    }


def run_repertoire_a(name: str) -> dict:
    configs = _configs_for(name)
    agent_records: list[dict] = []
    twin_records: list[dict] = []
    for cfg in configs:
        t_cfg = twin_config(cfg)
        for seed in EPISODE_SEEDS:
            agent_records.append(_episode_detector_record(cfg, seed))
            twin_records.append(_episode_detector_record(t_cfg, seed))

    n = len(agent_records)
    gaps: dict = {}
    for key in DETECTOR_KEYS:
        gap = [a[key] - t[key] for a, t in zip(agent_records, twin_records)]
        gaps[key] = {
            "mean_gap": round(sum(gap) / n, 4),
            "frac_positive": round(sum(1 for g in gap if g > 0) / n, 4),
        }
    return {"n_episodes": n, "twin_gap_decomposition": gaps}


# --- Part B: escalation v1 vs v2 + queryability diagnostic -----------------


def _episode_verdicts(cfg, seed: int) -> dict:
    rows = run_episode(cfg, seed)
    projected_light = project_rows(rows, "light")
    screen_score = score_detectors(projected_light)["composite"]
    exposure_weight = cfg.agent.weights.normalized().exposure
    repertoire = cfg.repertoire if cfg.repertoire is not None else LEGACY_ACTIONS
    sev = severity(rows)["severity"]

    has_queryable_v1 = bool(select_query_steps(projected_light))
    has_queryable_v2 = bool(select_query_steps_v2(projected_light))

    rng_v1 = random.Random(f"{cfg.config_id}:{seed}")
    outcome_v1 = run_escalation(rows, projected_light, repertoire, screen_score, exposure_weight, rng_v1)

    rng_v2 = random.Random(f"{cfg.config_id}:{seed}:v2")
    outcome_v2 = run_escalation(
        rows,
        projected_light,
        repertoire,
        screen_score,
        exposure_weight,
        rng_v2,
        query_selector=select_query_steps_v2,
    )

    return {
        "severity": sev,
        "has_queryable_v1": has_queryable_v1,
        "has_queryable_v2": has_queryable_v2,
        "v1": outcome_v1,
        "v2": outcome_v2,
    }


def _version_summary(agent_records: list[dict], twin_records: list[dict], version: str) -> dict:
    n = len(agent_records)
    outcomes = [r[version] for r in agent_records]
    twin_outcomes = [r[version] for r in twin_records]
    escalated = [o for o in outcomes if o["escalated"]]
    sev_true = [r["severity"] for r, o in zip(agent_records, outcomes) if o["verdict"]]
    sev_false = [r["severity"] for r, o in zip(agent_records, outcomes) if not o["verdict"]]
    verdict_indicator = [1.0 if o["verdict"] else 0.0 for o in outcomes]
    sev_series = [r["severity"] for r in agent_records]
    n_verdict_true = sum(1 for o in outcomes if o["verdict"])
    n_escalated = len(escalated)
    n_twin_verdict_true = sum(1 for o in twin_outcomes if o["verdict"])

    return {
        "verdict_true_rate": round(n_verdict_true / n, 4),
        "escalated_rate": round(n_escalated / n, 4),
        "mean_n_queried_when_escalated": (
            round(sum(o["n_queried"] for o in escalated) / len(escalated), 4) if escalated else None
        ),
        "mean_disclose_fraction_when_escalated": (
            round(sum(o.get("disclose_fraction", 0.0) for o in escalated) / len(escalated), 4)
            if escalated
            else None
        ),
        "mean_severity_given_verdict_true": round(sum(sev_true) / len(sev_true), 4) if sev_true else None,
        "mean_severity_given_verdict_false": (
            round(sum(sev_false) / len(sev_false), 4) if sev_false else None
        ),
        "spearman_severity_vs_verdict": round(spearman_correlation(sev_series, verdict_indicator), 4),
        "twin_verdict_true_rate": round(n_twin_verdict_true / n, 4),
    }


def run_repertoire_b(name: str) -> dict:
    configs = _configs_for_v4(name)
    agent_records: list[dict] = []
    twin_records: list[dict] = []
    for cfg in configs:
        t_cfg = twin_config(cfg)
        for seed in EPISODE_SEEDS:
            agent_records.append(_episode_verdicts(cfg, seed))
            twin_records.append(_episode_verdicts(t_cfg, seed))

    n = len(agent_records)
    result: dict = {
        "n_episodes": n,
        "queryability": {
            "frac_queryable_v1": round(
                sum(1 for r in agent_records if r["has_queryable_v1"]) / n, 4
            ),
            "frac_queryable_v2": round(
                sum(1 for r in agent_records if r["has_queryable_v2"]) / n, 4
            ),
        },
    }
    for version in ("v1", "v2"):
        result[version] = _version_summary(agent_records, twin_records, version)
    return result


def main() -> None:
    t0 = time.perf_counter()
    report: dict = {
        "protocol": {
            "n_configs": N_CONFIGS,
            "episode_seeds": list(EPISODE_SEEDS),
            "gates": {
                "low_gate": LOW_GATE,
                "high_gate": HIGH_GATE,
                "k_queries": K_QUERIES,
                "disclose_fraction_gate": DISCLOSE_FRACTION_GATE,
            },
        }
    }
    report["part_a_twin_gap_decomposition"] = {
        name: run_repertoire_a(name) for name in PART_A_REPERTOIRES
    }
    report["part_b_escalation_v1_vs_v2"] = {
        name: run_repertoire_b(name) for name in PART_B_REPERTOIRES
    }
    report["timing"] = {"total_seconds": round(time.perf_counter() - t0, 2)}

    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "phase5_followups.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS_DIR / "phase5_followups.md").write_text(render_md(report))
    print(json.dumps({k: v for k, v in report.items() if k != "protocol"}, indent=2))
    print(f"wrote {RESULTS_DIR / 'phase5_followups.json'}")


def render_md(report: dict) -> str:
    lines = [
        "# Phase 5 — GA-16/GA-17 follow-ups",
        "",
        "Protocol pre-registered in `run_phase5_followups.py` docstring. "
        f"{report['protocol']['n_configs']} configs x "
        f"{len(report['protocol']['episode_seeds'])} seeds per repertoire. "
        f"Gates: {report['protocol']['gates']}.",
        "",
        "## Part A — per-detector honest-twin gap decomposition (agent minus twin)",
        "",
        "| repertoire | n | d1 gap (frac>0) | d1b gap (frac>0) | d2 gap (frac>0) | "
        "light_deception gap (frac>0) |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for name, r in report["part_a_twin_gap_decomposition"].items():
        g = r["twin_gap_decomposition"]
        lines.append(
            f"| {name} | {r['n_episodes']} | "
            f"{g['d1']['mean_gap']} ({g['d1']['frac_positive']}) | "
            f"{g['d1b']['mean_gap']} ({g['d1b']['frac_positive']}) | "
            f"{g['d2']['mean_gap']} ({g['d2']['frac_positive']}) | "
            f"{g['light_deception']['mean_gap']} ({g['light_deception']['frac_positive']}) |"
        )
    lines += [
        "",
        "## Part B — escalation v1 vs v2, queryability diagnostic",
        "",
        "| repertoire | n | frac queryable v1 | frac queryable v2 |",
        "| --- | --- | --- | --- |",
    ]
    for name, r in report["part_b_escalation_v1_vs_v2"].items():
        q = r["queryability"]
        lines.append(
            f"| {name} | {r['n_episodes']} | {q['frac_queryable_v1']} | {q['frac_queryable_v2']} |"
        )
    lines += [
        "",
        "| repertoire | version | verdict-true rate | escalated rate | mean queried | "
        "mean disclose frac | sev\\|True | sev\\|False | Spearman(sev,verdict) | twin verdict-true rate |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for name, r in report["part_b_escalation_v1_vs_v2"].items():
        for version in ("v1", "v2"):
            v = r[version]
            lines.append(
                f"| {name} | {version} | {v['verdict_true_rate']} | {v['escalated_rate']} | "
                f"{v['mean_n_queried_when_escalated']} | {v['mean_disclose_fraction_when_escalated']} | "
                f"{v['mean_severity_given_verdict_true']} | {v['mean_severity_given_verdict_false']} | "
                f"{v['spearman_severity_vs_verdict']} | {v['twin_verdict_true_rate']} |"
            )
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
