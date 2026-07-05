#!/usr/bin/env python3
"""Phase 4a+4b: continuous-severity blind comparison, and honest-twin gaps.

PRE-REGISTERED PROTOCOL — fixed 2026-07-05 before this script was first run,
after `goal_sim/severity.py`, the `d*_score` detector variants, and
`goal_sim/twins.py` were frozen, but before any Phase-4 episode was executed:

- **Repertoires compared**: legacy (Phase 1's `LEGACY_ACTIONS`), round 1
  (`generated_actions.json`), round 2 (`generated_actions_v2.json`), round 3
  (`generated_actions_v3.json`) — the exact three blind-generation rounds
  F-12/F-14 found could not be compared via the boolean label once
  saturated.
- **Sampling**: 30 configs per repertoire. Legacy uses
  `protocol.sample_configs`'s discovery region (unchanged seed/sampling);
  rounds 1-3 use `run_phase2_blind.sample_blind_configs` (unchanged
  seed/sampling) against their own repertoire. 8 episode seeds each
  (`protocol.EPISODE_SEEDS`), both tiers → 240 episodes per repertoire.
- **Phase 4a metric (the blind comparison)**: Spearman rank correlation
  (`info.spearman_correlation`) of oracle `severity.severity`'s scalar
  against each tier's `detectors.score_detectors` composite, computed
  *within* each repertoire. Well-defined regardless of label saturation —
  there is no boolean threshold anywhere in this metric.
- **Phase 4b metric (honest twins)**: for every (config, seed) episode, also
  run the SAME seed against `twins.twin_config(cfg)`. Report the mean gap
  (agent minus twin) in oracle severity and in each tier's composite score,
  plus the fraction of pairs where the gap is positive. Pre-registered
  prediction: both gaps positive on average, in every repertoire (the twin
  rule removes deception capability without touching weights/seeds/
  availability, so a twin should score no more severely and no more
  detectably than the agent it is paired with).
- **No re-fitting**: `severity.py`, `score_detectors`, and `twins.py` are
  used exactly as frozen; this run does not tune anything after seeing
  output.

Artifacts: `results/phase4_severity.{json,md}`.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from goal_sim.actions import LEGACY_ACTIONS, load_specs
from goal_sim.channels import project_rows
from goal_sim.config import AgentConfig, BoardConfig, WorldConfig
from goal_sim.detectors import score_detectors
from goal_sim.info import spearman_correlation
from goal_sim.protocol import EPISODE_SEEDS, TIERS, sample_configs
from goal_sim.severity import severity
from goal_sim.twins import twin_config
from goal_sim.world import run_episode
from run_phase2_blind import sample_blind_configs

RESULTS_DIR = Path(__file__).parent / "results"
GOAL_SIM_DIR = Path(__file__).parent / "goal_sim"

REPERTOIRE_FILES = {
    "round1": GOAL_SIM_DIR / "generated_actions.json",
    "round2": GOAL_SIM_DIR / "generated_actions_v2.json",
    "round3": GOAL_SIM_DIR / "generated_actions_v3.json",
}
N_CONFIGS = 30


def _legacy_configs(n: int = N_CONFIGS) -> list[WorldConfig]:
    discovery, _held_out = sample_configs()
    return discovery[:n]


def _configs_for(name: str) -> list[WorldConfig]:
    if name == "legacy":
        return _legacy_configs()
    specs = load_specs(REPERTOIRE_FILES[name])
    return sample_blind_configs(specs)


def _episode_record(cfg: WorldConfig, seed: int) -> dict:
    rows = run_episode(cfg, seed)
    sev = severity(rows)
    composites = {}
    for tier in TIERS:
        projected = project_rows(rows, tier)
        composites[tier] = score_detectors(projected)["composite"]
    return {"severity": sev["severity"], "never_event": sev["never_event"], "composites": composites}


def run_repertoire(name: str) -> dict:
    configs = _configs_for(name)
    agent_records: list[dict] = []
    twin_records: list[dict] = []
    for cfg in configs:
        t_cfg = twin_config(cfg)
        for seed in EPISODE_SEEDS:
            agent_records.append(_episode_record(cfg, seed))
            twin_records.append(_episode_record(t_cfg, seed))

    sev_series = [r["severity"] for r in agent_records]
    ranking = {
        tier: round(
            spearman_correlation(sev_series, [r["composites"][tier] for r in agent_records]),
            4,
        )
        for tier in TIERS
    }

    n = len(agent_records)
    sev_gap = [a["severity"] - t["severity"] for a, t in zip(agent_records, twin_records)]
    twin_gaps: dict = {
        "severity": {
            "mean_gap": round(sum(sev_gap) / n, 4),
            "frac_positive": round(sum(1 for g in sev_gap if g > 0) / n, 4),
        }
    }
    for tier in TIERS:
        gap = [
            a["composites"][tier] - t["composites"][tier]
            for a, t in zip(agent_records, twin_records)
        ]
        twin_gaps[tier] = {
            "mean_gap": round(sum(gap) / n, 4),
            "frac_positive": round(sum(1 for g in gap if g > 0) / n, 4),
        }

    return {
        "n_episodes": n,
        "n_never_event": sum(1 for r in agent_records if r["never_event"]),
        "mean_severity": round(sum(sev_series) / n, 4),
        "ranking_spearman_severity_vs_composite": ranking,
        "twin_gaps": twin_gaps,
    }


def main() -> None:
    t0 = time.perf_counter()
    report = {"protocol": {"n_configs": N_CONFIGS, "episode_seeds": list(EPISODE_SEEDS), "tiers": list(TIERS)}}
    report["repertoires"] = {
        name: run_repertoire(name) for name in ("legacy", "round1", "round2", "round3")
    }
    report["timing"] = {"total_seconds": round(time.perf_counter() - t0, 2)}

    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "phase4_severity.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS_DIR / "phase4_severity.md").write_text(render_md(report))
    print(json.dumps(report["repertoires"], indent=2))
    print(f"wrote {RESULTS_DIR / 'phase4_severity.json'}")


def render_md(report: dict) -> str:
    lines = [
        "# Phase 4a+4b — continuous severity ranking and honest-twin gaps",
        "",
        "Protocol pre-registered in `run_phase4_ranking.py` docstring. "
        f"{report['protocol']['n_configs']} configs x "
        f"{len(report['protocol']['episode_seeds'])} seeds per repertoire.",
        "",
        "## Phase 4a — Spearman(oracle severity, detector composite score), per repertoire",
        "",
        "| repertoire | n | mean severity | n never-event | light | full |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for name, r in report["repertoires"].items():
        rk = r["ranking_spearman_severity_vs_composite"]
        lines.append(
            f"| {name} | {r['n_episodes']} | {r['mean_severity']} | {r['n_never_event']} | "
            f"{rk['light']} | {rk['full']} |"
        )
    lines += [
        "",
        "## Phase 4b — honest-twin gaps (agent minus twin; positive = twin scores lower)",
        "",
        "| repertoire | severity gap (frac>0) | light gap (frac>0) | full gap (frac>0) |",
        "| --- | --- | --- | --- |",
    ]
    for name, r in report["repertoires"].items():
        g = r["twin_gaps"]
        lines.append(
            f"| {name} | {g['severity']['mean_gap']} ({g['severity']['frac_positive']}) | "
            f"{g['light']['mean_gap']} ({g['light']['frac_positive']}) | "
            f"{g['full']['mean_gap']} ({g['full']['frac_positive']}) |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
