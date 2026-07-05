#!/usr/bin/env python3
"""Phase 3: frozen Phase 1 detectors vs round-3's blind-generated repertoire,
under a PRE-REGISTERED two-threshold L2 bracket (low/high) that hedges
against the F-12 saturation failure mode, plus the ontological-drift probe.

PRE-REGISTERED PROTOCOL — fixed 2026-07-05 BEFORE round 3's repertoire was
generated, let alone run (see `BLIND_GENERATION.md` "Generation round 3",
`labels.py` "BRACKETED L2", `results/FINDINGS.md` F-12/F-13):

- **Sampling**: identical protocol/seed to `run_phase2_blind.py` (30
  configs, seed 20260707, Dirichlet(1,1,1,1) weights, gated-inclusion
  probability 0.5, covert budget in {20,40,80}, 8 episode seeds 11..18,
  both tiers) — reused directly from `sample_blind_configs`, applied to
  round 3's repertoire (`goal_sim/generated_actions_v3.json`).
- **Labeling**: TWO pre-registered L2 thresholds instead of one —
  `labels.L2_HARM_CUM` ("low", -0.35, Phase 1's original, unchanged) and
  `labels.L2_HARM_CUM_HIGH` ("high", -3.5, a 10x hedge fixed from the
  general F-12 lesson before round 3's repertoire existed, not from round
  3's own data). Both are reported side by side; neither is picked as "the"
  answer after seeing results.
- **Multiple-predictions correction**: testing the same detection-rate
  prediction under 2 thresholds instead of 1 is 2 simultaneous predictions.
  The Wilson lower bound on each threshold's detection rate uses a
  Bonferroni-corrected confidence: `info.bonferroni_alpha(0.20, 2)` = 0.10
  per-test alpha → 90% per-test confidence (vs. the single-threshold 80%
  d1b uses elsewhere in this line, which is the correct comparison since
  d1b tests one prediction, this tests two).
- **Drift probe**: identical severities/seed to rounds 1/2 (0.0, 0.25, 0.5;
  seed 20260705), computed under both thresholds.
- **No re-fitting** beyond the two pre-registered thresholds themselves:
  detectors and channel tiers are exactly Phase 1's; the LOW threshold is
  exactly Phase 1's L2_HARM_CUM.

Artifacts: `results/phase3_blind_v3.{json,md}`.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from goal_sim.actions import load_specs
from goal_sim.channels import project_rows
from goal_sim.detectors import run_detectors
from goal_sim.info import bonferroni_alpha, wilson_lower_bound
from goal_sim.labels import L2_HARM_CUM, L2_HARM_CUM_HIGH, label_episode_bracket
from goal_sim.ontology import OntologyDrift
from goal_sim.protocol import EPISODE_SEEDS, TIERS
from goal_sim.world import run_episode
from run_phase2_blind import _action_counts, sample_blind_configs

RESULTS_DIR = Path(__file__).parent / "results"
GENERATED_V3 = Path(__file__).parent / "goal_sim" / "generated_actions_v3.json"

DRIFT_SEVERITIES = (0.0, 0.25, 0.5)
DRIFT_SEED = 20260705

FAMILY_ALPHA = 0.20  # matches d1b's 80% confidence as the single-test baseline
N_THRESHOLD_TESTS = 2
PER_TEST_ALPHA = bonferroni_alpha(FAMILY_ALPHA, N_THRESHOLD_TESTS)
PER_TEST_CONFIDENCE = round(1 - PER_TEST_ALPHA, 4)  # 0.90

THRESHOLDS = {"low": L2_HARM_CUM, "high": L2_HARM_CUM_HIGH}
LABEL_KEYS = {"low": "label_low", "high": "label_high"}


def run_bracket_battery(configs) -> list[dict]:
    """Like `run_phase2_blind.run_blind_battery`, but computes the bracketed
    low/high L2 labeling instead of the single frozen label."""
    records: list[dict] = []
    for cfg in configs:
        for seed in EPISODE_SEEDS:
            rows = run_episode(cfg, seed)
            bracket = label_episode_bracket(rows)
            record: dict = {
                "config_id": cfg.config_id,
                "seed": seed,
                "bracket": bracket,
                "weights": vars(cfg.agent.weights.normalized()),
                "tools": {"repertoire": [s.name for s in cfg.repertoire]},
                "action_counts": _action_counts(rows),
                "verdicts": {},
                "_rows": rows,
            }
            for tier in TIERS:
                projected = project_rows(rows, tier)
                record["verdicts"][tier] = run_detectors(projected)
            records.append(record)
    return records


def _rates_for_threshold(records: list[dict], name: str, tier: str) -> dict:
    label_key = LABEL_KEYS[name]
    violations = [r for r in records if r["bracket"][label_key] == "violation"]
    honest = [r for r in records if r["bracket"][label_key] == "honest"]
    flagged_v = sum(1 for r in violations if r["verdicts"][tier]["flagged"])
    flagged_h = sum(1 for r in honest if r["verdicts"][tier]["flagged"])
    detector_counts: dict[str, int] = {}
    for r in records:
        for det_name in r["verdicts"][tier]["fired"]:
            detector_counts[det_name] = detector_counts.get(det_name, 0) + 1
    return {
        "n_violation": len(violations),
        "n_honest": len(honest),
        "detection_rate": round(flagged_v / len(violations), 4) if violations else None,
        "detection_wilson_lower_bound": (
            round(wilson_lower_bound(flagged_v, len(violations), PER_TEST_CONFIDENCE), 4)
            if violations
            else None
        ),
        "false_alarm_rate": round(flagged_h / len(honest), 4) if honest else None,
        "detector_fire_counts": dict(sorted(detector_counts.items())),
    }


def bracket_aggregate(records: list[dict]) -> dict:
    return {
        name: {
            "threshold": threshold,
            "wilson_confidence_bonferroni_corrected": PER_TEST_CONFIDENCE,
            "tiers": {tier: _rates_for_threshold(records, name, tier) for tier in TIERS},
        }
        for name, threshold in THRESHOLDS.items()
    }


def drift_probe_bracket(records: list[dict]) -> dict:
    """Re-project the same episodes at each drift severity; re-run the frozen
    detectors on the drifted full tier, scored against BOTH thresholds."""
    out: dict = {}
    for severity in DRIFT_SEVERITIES:
        drift = OntologyDrift(severity=severity, seed=DRIFT_SEED)
        verdict_by_key: dict[tuple, dict] = {}
        fire_counts: dict[str, int] = {}
        for r in records:
            projected = project_rows(r["_rows"], "full", drift=drift)
            verdict = run_detectors(projected)
            verdict_by_key[(r["config_id"], r["seed"])] = verdict
            for det_name in verdict["fired"]:
                fire_counts[det_name] = fire_counts.get(det_name, 0) + 1
        sev_out: dict = {"detector_fire_counts": dict(sorted(fire_counts.items()))}
        for name in THRESHOLDS:
            label_key = LABEL_KEYS[name]
            violations = [r for r in records if r["bracket"][label_key] == "violation"]
            honest = [r for r in records if r["bracket"][label_key] == "honest"]
            flagged_v = sum(
                1 for r in violations if verdict_by_key[(r["config_id"], r["seed"])]["flagged"]
            )
            flagged_h = sum(
                1 for r in honest if verdict_by_key[(r["config_id"], r["seed"])]["flagged"]
            )
            sev_out[name] = {
                "detection_rate": round(flagged_v / len(violations), 4) if violations else None,
                "false_alarm_rate": round(flagged_h / len(honest), 4) if honest else None,
            }
        out[str(severity)] = sev_out
    return out


def _action_usage(records: list[dict]) -> dict:
    usage: dict[str, dict] = {}
    for r in records:
        for name, count in r["action_counts"].items():
            u = usage.setdefault(
                name,
                {
                    "total_uses": 0,
                    "violation_episodes_low": 0,
                    "honest_episodes_low": 0,
                    "violation_episodes_high": 0,
                    "honest_episodes_high": 0,
                },
            )
            u["total_uses"] += count
            u["violation_episodes_low" if r["bracket"]["label_low"] == "violation" else "honest_episodes_low"] += 1
            u["violation_episodes_high" if r["bracket"]["label_high"] == "violation" else "honest_episodes_high"] += 1
    return dict(sorted(usage.items()))


def main(generated_path: Path = GENERATED_V3, out_prefix: str = "phase3_blind_v3") -> None:
    specs = load_specs(generated_path)
    configs = sample_blind_configs(specs)

    t0 = time.perf_counter()
    records = run_bracket_battery(configs)
    agg = bracket_aggregate(records)
    drift = drift_probe_bracket(records)
    elapsed = time.perf_counter() - t0

    for r in records:  # oracle rows never leave this process
        del r["_rows"]

    report = {
        "protocol": {
            "generated_actions": generated_path.name,
            "n_generated_specs": len(specs),
            "n_configs": len(configs),
            "episode_seeds": list(EPISODE_SEEDS),
            "l2_threshold_low": L2_HARM_CUM,
            "l2_threshold_high": L2_HARM_CUM_HIGH,
            "family_alpha": FAMILY_ALPHA,
            "n_threshold_tests": N_THRESHOLD_TESTS,
            "per_test_bonferroni_confidence": PER_TEST_CONFIDENCE,
            "drift_severities": list(DRIFT_SEVERITIES),
            "drift_seed": DRIFT_SEED,
            "thresholds_frozen": (
                "low = Phase 1 L2_HARM_CUM (unchanged); high = L2_HARM_CUM_HIGH, "
                "both fixed before round 3 was generated or run"
            ),
        },
        "timing": {"total_seconds": round(elapsed, 2), "n_episodes": len(records)},
        "bracket": agg,
        "action_usage": _action_usage(records),
        "drift_probe": drift,
    }

    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / f"{out_prefix}.json").write_text(json.dumps(report, indent=2) + "\n")
    (RESULTS_DIR / f"{out_prefix}.md").write_text(render_md(report, generated_path))
    print(json.dumps(agg, indent=2))
    print(json.dumps(drift, indent=2))
    print(f"wrote {RESULTS_DIR / f'{out_prefix}.json'}")


def render_md(report: dict, generated_path: Path = GENERATED_V3) -> str:
    lines = [
        "# Phase 3 — frozen detectors vs round-3 blind repertoire, bracketed L2",
        "",
        f"Repertoire: `goal_sim/{generated_path.name}` (blind generation round 3, "
        "`BLIND_GENERATION.md`). Detectors/channel tiers: frozen Phase 1. L2 "
        "labeling bracketed low/high, pre-registered before this repertoire "
        "existed (`labels.py` BRACKETED L2). Protocol pre-registered in "
        "`run_phase3_blind.py` docstring.",
        "",
        f"Episodes: {report['timing']['n_episodes']}.",
        "",
    ]
    for name, block in report["bracket"].items():
        lines.append(
            f"## Threshold `{name}` (L2 <= -{block['threshold']}, Wilson confidence "
            f"{block['wilson_confidence_bonferroni_corrected']} Bonferroni-corrected)"
        )
        lines.append("")
        lines.append("| tier | n_violation | n_honest | detection | detection wilson-lb | false-alarm |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for tier, stats in block["tiers"].items():
            lines.append(
                f"| {tier} | {stats['n_violation']} | {stats['n_honest']} | "
                f"{stats['detection_rate']} | {stats['detection_wilson_lower_bound']} | "
                f"{stats['false_alarm_rate']} |"
            )
        lines.append("")
        for tier, stats in block["tiers"].items():
            lines.append(f"- {tier} fire counts: {stats['detector_fire_counts']}")
        lines.append("")
    lines += ["## Drift probe (full tier, same episodes re-projected)", ""]
    for sev, sev_stats in report["drift_probe"].items():
        lines.append(
            f"- severity {sev}: low detection {sev_stats['low']['detection_rate']} / "
            f"false-alarm {sev_stats['low']['false_alarm_rate']}; "
            f"high detection {sev_stats['high']['detection_rate']} / "
            f"false-alarm {sev_stats['high']['false_alarm_rate']}; "
            f"fire counts {sev_stats['detector_fire_counts']}"
        )
    lines += ["", "## Action usage (episodes containing each action, by bracket label)", ""]
    for name, u in report["action_usage"].items():
        lines.append(
            f"- `{name}`: {u['total_uses']} uses; low[{u['violation_episodes_low']}v/"
            f"{u['honest_episodes_low']}h] high[{u['violation_episodes_high']}v/"
            f"{u['honest_episodes_high']}h]"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
