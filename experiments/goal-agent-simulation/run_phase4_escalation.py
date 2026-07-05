#!/usr/bin/env python3
"""Phase 4c: gated-escalation battery — verdict quality vs. oracle severity
at a bounded query budget, and the twin false-positive rate.

PRE-REGISTERED PROTOCOL — fixed 2026-07-05 before this script was first run,
after `goal_sim/escalation.py`'s gates and `generated_actions_v4.json` (the
first repertoire carrying response options) were both frozen:

- **Primary repertoire**: round 4 (`generated_actions_v4.json`), the only
  one whose actions carry `responses` — the escalation ladder's follow-up
  stage has real evidence to query only here. Rounds 1-3 and legacy are
  also run as a CONTRAST, not a comparison: with empty `responses` on every
  spec, `escalation.choose_response` always returns `None`, so any episode
  landing in the borderline band falls through to the ladder's documented
  "no evidence -> verdict False" default. Seeing that fall-through actually
  happen is itself a check that the ladder degrades the way its own
  docstring says it should when a repertoire predates the response schema.
- **Sampling**: identical to `run_phase4_ranking.py` (30 configs via
  `sample_blind_configs`/`sample_configs`, `protocol.EPISODE_SEEDS`, light
  tier for the screen score — the ladder's own pre-registered design, per
  `PHASE4-PLAN.md`, gates on the CHEAP tier).
- **Escalation RNG**: a dedicated `random.Random(f"{config_id}:{seed}")`
  stream per episode, independent of the episode's own RNG, so response
  choice does not perturb the already-frozen oracle rows.
- **Verdict-quality metric**: mean oracle severity conditioned on verdict
  (True vs. False) plus the Spearman correlation between severity and the
  verdict indicator — both well-defined regardless of label saturation,
  same rationale as `run_phase4_ranking.py`. Pre-registered prediction:
  mean severity | verdict=True > mean severity | verdict=False, for round 4
  specifically (the only repertoire with real evidence to escalate on).
- **Twin false-positive rate**: fraction of `twins.twin_config` episodes
  (paired, same seed) that receive verdict=True. Pre-registered prediction:
  lower than the agent's own true-positive-ish rate, per repertoire.
- **No re-fitting**: `escalation.py`'s gates are used exactly as frozen.

Artifacts: `results/phase4_escalation.{json,md}`.
"""

from __future__ import annotations

import json
import random
import time
from pathlib import Path

from goal_sim.actions import LEGACY_ACTIONS, load_specs
from goal_sim.channels import project_rows
from goal_sim.detectors import score_detectors
from goal_sim.escalation import DISCLOSE_FRACTION_GATE, HIGH_GATE, K_QUERIES, LOW_GATE, run_escalation
from goal_sim.info import spearman_correlation
from goal_sim.protocol import EPISODE_SEEDS
from goal_sim.severity import severity
from goal_sim.twins import twin_config
from goal_sim.world import run_episode
from run_phase4_ranking import GOAL_SIM_DIR, N_CONFIGS, REPERTOIRE_FILES, _configs_for

RESULTS_DIR = Path(__file__).parent / "results"
REPERTOIRE_FILES = dict(REPERTOIRE_FILES, round4=GOAL_SIM_DIR / "generated_actions_v4.json")


def _configs_for_v4(name: str):
    if name == "round4":
        specs = load_specs(REPERTOIRE_FILES["round4"])
        from run_phase2_blind import sample_blind_configs

        return sample_blind_configs(specs)
    return _configs_for(name)


def _episode_verdict(cfg, seed: int) -> dict:
    rows = run_episode(cfg, seed)
    projected_light = project_rows(rows, "light")
    screen_score = score_detectors(projected_light)["composite"]
    exposure_weight = cfg.agent.weights.normalized().exposure
    esc_rng = random.Random(f"{cfg.config_id}:{seed}")
    repertoire = cfg.repertoire if cfg.repertoire is not None else LEGACY_ACTIONS
    outcome = run_escalation(
        rows, projected_light, repertoire, screen_score, exposure_weight, esc_rng
    )
    return {
        "severity": severity(rows)["severity"],
        "screen_score": screen_score,
        **outcome,
    }


def run_repertoire(name: str) -> dict:
    configs = _configs_for_v4(name)
    agent_records: list[dict] = []
    twin_records: list[dict] = []
    for cfg in configs:
        t_cfg = twin_config(cfg)
        for seed in EPISODE_SEEDS:
            agent_records.append(_episode_verdict(cfg, seed))
            twin_records.append(_episode_verdict(t_cfg, seed))

    n = len(agent_records)
    n_verdict_true = sum(1 for r in agent_records if r["verdict"])
    n_escalated = sum(1 for r in agent_records if r["escalated"])
    escalated = [r for r in agent_records if r["escalated"]]
    sev_true = [r["severity"] for r in agent_records if r["verdict"]]
    sev_false = [r["severity"] for r in agent_records if not r["verdict"]]
    verdict_indicator = [1.0 if r["verdict"] else 0.0 for r in agent_records]
    sev_series = [r["severity"] for r in agent_records]

    n_twin_verdict_true = sum(1 for r in twin_records if r["verdict"])

    return {
        "n_episodes": n,
        "verdict_true_rate": round(n_verdict_true / n, 4),
        "escalated_rate": round(n_escalated / n, 4),
        "mean_n_queried_when_escalated": (
            round(sum(r["n_queried"] for r in escalated) / len(escalated), 4) if escalated else None
        ),
        "mean_disclose_fraction_when_escalated": (
            round(
                sum(r.get("disclose_fraction", 0.0) for r in escalated) / len(escalated), 4
            )
            if escalated
            else None
        ),
        "mean_severity_given_verdict_true": round(sum(sev_true) / len(sev_true), 4) if sev_true else None,
        "mean_severity_given_verdict_false": (
            round(sum(sev_false) / len(sev_false), 4) if sev_false else None
        ),
        "spearman_severity_vs_verdict": round(
            spearman_correlation(sev_series, verdict_indicator), 4
        ),
        "twin_verdict_true_rate": round(n_twin_verdict_true / n, 4),
    }


def main() -> None:
    t0 = time.perf_counter()
    report = {
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
    report["repertoires"] = {
        name: run_repertoire(name) for name in ("legacy", "round1", "round2", "round3", "round4")
    }
    report["timing"] = {"total_seconds": round(time.perf_counter() - t0, 2)}

    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "phase4_escalation.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS_DIR / "phase4_escalation.md").write_text(render_md(report))
    print(json.dumps(report["repertoires"], indent=2))
    print(f"wrote {RESULTS_DIR / 'phase4_escalation.json'}")


def render_md(report: dict) -> str:
    lines = [
        "# Phase 4c — gated escalation ladder: verdict quality and twin false-positives",
        "",
        "Protocol pre-registered in `run_phase4_escalation.py` docstring. "
        f"Gates: {report['protocol']['gates']}.",
        "",
        "| repertoire | n | verdict-true rate | escalated rate | mean queried | "
        "mean disclose frac | sev\\|True | sev\\|False | Spearman(sev,verdict) | twin verdict-true rate |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for name, r in report["repertoires"].items():
        lines.append(
            f"| {name} | {r['n_episodes']} | {r['verdict_true_rate']} | {r['escalated_rate']} | "
            f"{r['mean_n_queried_when_escalated']} | {r['mean_disclose_fraction_when_escalated']} | "
            f"{r['mean_severity_given_verdict_true']} | {r['mean_severity_given_verdict_false']} | "
            f"{r['spearman_severity_vs_verdict']} | {r['twin_verdict_true_rate']} |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
