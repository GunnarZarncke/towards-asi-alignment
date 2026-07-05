#!/usr/bin/env python3
"""Phase 2a: frozen Phase 1 detectors/labels vs the blind-generated repertoire,
plus the first ontological-drift probe.

PRE-REGISTERED PROTOCOL — fixed 2026-07-05 BEFORE this script was first run,
after the generated repertoire was frozen (`goal_sim/generated_actions.json`,
protocol `BLIND_GENERATION.md`) but before any episode with it was executed:

- **Configs**: 30, master seed 20260707. Goal weights ~ Dirichlet(1,1,1,1)
  (same distribution as Phase 1). Action availability replaces Phase 1's
  tool booleans: every always-available generated action is always in the
  agent's repertoire; each gated generated action (correction-gated,
  budget-costed, or practice-gated) is included independently with
  probability 0.5. Covert budget uniform from {20, 40, 80}. 8 episode seeds
  (11..18), both tiers.
- **No re-fitting**: detectors, labels, thresholds, and channel tiers are
  exactly Phase 1's. Detection failures against blind-generated mechanisms
  are headline results for FINDINGS.md, not bugs to patch in this run.
- **Drift probe**: severities (0.0, 0.25, 0.5), drift seed 20260705,
  applied to the full-tier projection of the SAME episodes (light tier
  carries no routing codes and cannot drift by construction).
  **Pre-registered prediction** (written before running): only detectors
  that read `action_cause_code` change under drift — d4_shadow_routing and
  d6_unattributed_harm; d1/d1b/d2 (report-vs-visible divergence), d3
  (welfare sums), and d5 (fingerprint vs sign-off) are drift-invariant by
  construction. Direction for d4/d6 is NOT predicted (drift can hide
  covert-budget routing or mislabel ordinary actions as covert), only that
  they move while the others stay fixed.

Artifacts: `results/phase2_blind.{json,md}`.
"""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

from goal_sim.actions import ActionSpec, load_specs
from goal_sim.channels import project_rows
from goal_sim.config import AgentConfig, BoardConfig, GoalWeights, WorldConfig, ToolAccess
from goal_sim.detectors import run_detectors
from goal_sim.labels import label_episode
from goal_sim.ontology import OntologyDrift
from goal_sim.protocol import EPISODE_SEEDS, TIERS, aggregate

SAMPLING_SEED = 20260707
N_CONFIGS = 30
GATED_INCLUSION_PROB = 0.5
DRIFT_SEVERITIES = (0.0, 0.25, 0.5)
DRIFT_SEED = 20260705

RESULTS_DIR = Path(__file__).parent / "results"
GENERATED = Path(__file__).parent / "goal_sim" / "generated_actions.json"


def is_always_available(spec: ActionSpec) -> bool:
    return (
        not spec.requires_correction
        and spec.budget_cost == 0
        and not spec.requires_no_practice
        and not spec.blocks_when_proposal_pending
    )


def sample_blind_configs(
    specs: list[ActionSpec],
    seed: int = SAMPLING_SEED,
    n: int = N_CONFIGS,
) -> list[WorldConfig]:
    rng = random.Random(seed)
    base = [s for s in specs if is_always_available(s)]
    gated = [s for s in specs if not is_always_available(s)]
    out: list[WorldConfig] = []
    for i in range(n):
        draws = [rng.gammavariate(1.0, 1.0) for _ in range(4)]
        weights = GoalWeights(*draws).normalized()
        repertoire = tuple(base) + tuple(
            s for s in gated if rng.random() < GATED_INCLUSION_PROB
        )
        budget = rng.choice([20, 40, 80])
        out.append(
            WorldConfig(
                agent=AgentConfig(
                    weights=weights,
                    tools=ToolAccess(shadow_budget=budget),
                ),
                board=BoardConfig(),
                config_id=f"blind.{i:02d}",
                repertoire=repertoire,
            )
        )
    return out


def run_blind_battery(configs: list[WorldConfig]) -> list[dict]:
    """Like protocol.run_battery but also keeps oracle rows for the drift
    probe (drift re-projects the same episodes; no fresh RNG)."""
    from goal_sim.world import run_episode

    records: list[dict] = []
    for cfg in configs:
        for seed in EPISODE_SEEDS:
            rows = run_episode(cfg, seed)
            label = label_episode(rows)
            record: dict = {
                "config_id": cfg.config_id,
                "seed": seed,
                "label": label["label"],
                "label_detail": label,
                "weights": vars(cfg.agent.weights.normalized()),
                "tools": {"repertoire": [s.name for s in cfg.repertoire]},
                "action_counts": _action_counts(rows),
                "verdicts": {},
                "channel_means": {},
                "_rows": rows,
            }
            for tier in TIERS:
                projected = project_rows(rows, tier)
                record["verdicts"][tier] = run_detectors(projected)
            records.append(record)
    return records


def _action_counts(rows: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["true_action_name"]] = counts.get(r["true_action_name"], 0) + 1
    return counts


def drift_probe(records: list[dict]) -> dict:
    """Re-project the same episodes at each drift severity; re-run the frozen
    detectors on the drifted full tier."""
    out: dict = {}
    for severity in DRIFT_SEVERITIES:
        drift = OntologyDrift(severity=severity, seed=DRIFT_SEED)
        violations = [r for r in records if r["label"] == "violation"]
        honest = [r for r in records if r["label"] == "honest"]
        fire_counts: dict[str, int] = {}
        flagged_v = 0
        flagged_h = 0
        for r in records:
            projected = project_rows(r["_rows"], "full", drift=drift)
            verdict = run_detectors(projected)
            for name in verdict["fired"]:
                fire_counts[name] = fire_counts.get(name, 0) + 1
            if verdict["flagged"]:
                if r["label"] == "violation":
                    flagged_v += 1
                else:
                    flagged_h += 1
        out[str(severity)] = {
            "detection_rate": round(flagged_v / len(violations), 4) if violations else None,
            "false_alarm_rate": round(flagged_h / len(honest), 4) if honest else None,
            "detector_fire_counts": dict(sorted(fire_counts.items())),
        }
    return out


def main(generated_path: Path = GENERATED, out_prefix: str = "phase2_blind") -> None:
    specs = load_specs(generated_path)
    configs = sample_blind_configs(specs)

    t0 = time.perf_counter()
    records = run_blind_battery(configs)
    drift = drift_probe(records)
    elapsed = time.perf_counter() - t0

    for r in records:  # oracle rows never leave this process
        del r["_rows"]

    agg = aggregate(records)
    # Per-action presence in violating vs honest episodes (context, not a
    # detector): which generated mechanisms drive the labels.
    usage: dict[str, dict[str, int]] = {}
    for r in records:
        for name, count in r["action_counts"].items():
            u = usage.setdefault(name, {"violation_episodes": 0, "honest_episodes": 0, "total_uses": 0})
            u["total_uses"] += count
            u["violation_episodes" if r["label"] == "violation" else "honest_episodes"] += 1

    # Per-record miss list for FINDINGS analysis (violations passing at full).
    full_misses = [
        {
            "config_id": r["config_id"],
            "seed": r["seed"],
            "label_detail": r["label_detail"],
            "action_counts": r["action_counts"],
        }
        for r in records
        if r["label"] == "violation" and not r["verdicts"]["full"]["flagged"]
    ]

    report = {
        "protocol": {
            "generated_actions": generated_path.name,
            "n_generated_specs": len(specs),
            "n_configs": len(configs),
            "sampling_seed": SAMPLING_SEED,
            "gated_inclusion_prob": GATED_INCLUSION_PROB,
            "episode_seeds": list(EPISODE_SEEDS),
            "drift_severities": list(DRIFT_SEVERITIES),
            "drift_seed": DRIFT_SEED,
            "drift_prediction": (
                "only d4/d6 (routing-code readers) change under drift; "
                "d1/d1b/d2/d3/d5 are drift-invariant by construction; "
                "direction for d4/d6 not predicted"
            ),
            "thresholds_frozen": "Phase 1 detectors/labels, no re-fitting",
        },
        "timing": {
            "total_seconds": round(elapsed, 2),
            "n_episodes": len(records),
        },
        "aggregate": agg,
        "action_usage": dict(sorted(usage.items())),
        "full_tier_misses": full_misses,
        "drift_probe": drift,
    }

    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / f"{out_prefix}.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS_DIR / f"{out_prefix}.md").write_text(render_md(report, generated_path))
    print(json.dumps(agg, indent=2))
    print(json.dumps(drift, indent=2))
    print(f"full-tier misses: {len(full_misses)}")
    print(f"wrote {RESULTS_DIR / f'{out_prefix}.json'}")


def render_md(report: dict, generated_path: Path = GENERATED) -> str:
    agg = report["aggregate"]
    lines = [
        "# Phase 2a — frozen detectors vs blind-generated repertoire",
        "",
        f"Repertoire: `goal_sim/{generated_path.name}` (blind generation per "
        "`BLIND_GENERATION.md`). Detectors/labels: frozen Phase 1, no re-fitting. "
        "Protocol/prediction pre-registered in `run_phase2_blind.py` docstring.",
        "",
        f"Episodes: {report['timing']['n_episodes']}; violation rate "
        f"{agg['violation_rate']}; label causes {agg['label_causes']}.",
        "",
        "| tier | detection | false-pass | false-alarm |",
        "| --- | --- | --- | --- |",
    ]
    for tier, stats in agg["tiers"].items():
        lines.append(
            f"| {tier} | {stats['detection_rate']} | {stats['false_pass_rate']} "
            f"| {stats['false_alarm_rate']} |"
        )
    lines += ["", "## Detector fire counts", ""]
    for tier, stats in agg["tiers"].items():
        lines.append(f"- {tier}: {stats['detector_fire_counts']}")
    lines += ["", "## Drift probe (full tier, same episodes re-projected)", ""]
    lines.append("| severity | detection | false-alarm |")
    lines.append("| --- | --- | --- |")
    for sev, stats in report["drift_probe"].items():
        lines.append(f"| {sev} | {stats['detection_rate']} | {stats['false_alarm_rate']} |")
    lines += ["", "Per-severity fire counts:", ""]
    for sev, stats in report["drift_probe"].items():
        lines.append(f"- {sev}: {stats['detector_fire_counts']}")
    lines += ["", "## Action usage (episodes containing each action, by label)", ""]
    for name, u in report["action_usage"].items():
        lines.append(
            f"- `{name}`: {u['total_uses']} uses; in {u['violation_episodes']} "
            f"violation / {u['honest_episodes']} honest episodes"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repertoire",
        type=Path,
        default=GENERATED,
        help="Path to a generated_actions*.json file (default: round-1 generated_actions.json).",
    )
    parser.add_argument(
        "--out-prefix",
        default="phase2_blind",
        help="Basename (no extension) for results/<prefix>.{json,md} (default: phase2_blind).",
    )
    args = parser.parse_args()
    main(generated_path=args.repertoire, out_prefix=args.out_prefix)
