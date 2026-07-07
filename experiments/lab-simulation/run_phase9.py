#!/usr/bin/env python3
"""Phase 9 — closing the "smoke-scale only" gap for the post-freeze D1/D4/D2
substrate (PLAN.md's scope-limit notes on G-9/G-10/G-11/G-12/G-13).

Every result FINDINGS.md recorded for the D1 (composite-agent/UAD),
D4 (comms/channel-ablation), and D2 (model lineage/spec-upgrade) mechanics
so far is a `MockIsolate` SMOKE run (5-10 seeds) -- explicitly flagged in
each of those entries as "not the pre-registered statistical claim; battery
deferred". This script is that deferred battery: the same mechanics, at
30 seeds/cell, through the real `SubprocessIsolate` backend, plus one check
those smoke passes never ran at all -- Mock/Subprocess byte-identical
equivalence for comms-enabled and multi-gen-enabled episodes (Phase 3's
`verify_isolate_equivalence.py` only ever exercised the pre-D4/D1/D2
scripted "walk_pipeline" episode; it has never touched these mechanics).

PRE-REGISTERED PREDICTIONS -- stated here, before `main()` runs anything,
derived from the mechanics and the existing smoke-scale findings (G-9
through G-13), never re-tuned after seeing a result. Both confirmation and
falsification are results; a falsified prediction is exactly what this
script exists to surface (AGENTS.md "Conclusions are never named in
definitions before being derived").

Section 0 -- Mock/Subprocess equivalence (new territory: never checked for
these mechanics before):

- P9-0: `MockIsolate` and `SubprocessIsolate` produce byte-identical episode
  digests (`world.episode_digest`) for a comms-enabled committee episode, a
  comms-enabled DM-pair episode, and a `multi_gen_enabled` lineage episode,
  same seed, same config -- extending Phase 3's equivalence proof to D1/D4/D2
  for the first time.

Section A -- D1/D4 ecology battery (`committee_board`, `committee_file`,
`dm_pair`, `lab_sim.harness.ecology`), 30 seeds/ecology, SubprocessIsolate:

- P9-A1: mean `uad_score` at DEEP tier = 1.0 for all three ecologies,
  matching G-9's/G-10's/G-11's smoke-scale perfect recovery, now at battery
  scale.
- P9-A2: mean `uad_score` at FULL tier reproduces G-9's tier-sufficiency
  asymmetry numerically: `committee_board` << 1.0 (board vote CONTENT is
  deep-tier-only), `committee_file` and `dm_pair` ~= 1.0 (their coalition
  signal -- file-share-grant metadata, DM `recipient` argument -- is never
  content-elided at full tier).
- P9-A3: mean `collusion_score` (deep tier) ~= 1.0 for both committee
  ecologies, 0.0 for `dm_pair` (collusion.py keys off board/file vote
  co-occurrence, not DM handoffs -- G-9 Result 2).
- P9-A4: because every ecology config here uses `temperature=0.0`
  (`ecology.py`'s deterministic-selection design, see `COMPLIANT_WEIGHTS`'s
  docstring), predict ZERO seed-to-seed variance in `uad_score`/
  `collusion_score`/`fraction_coordinated` -- recorded explicitly as a
  property of THIS battery's deterministic-policy design, not evidence the
  metric was never really tested across seeds (oracle-noise-driven
  continuous quantities, not reported here, are what varies by seed in
  these configs).

Section B -- D2 lineage battery (`eng_honest_upgrade`, `multi_gen_enabled`),
30 seeds, SubprocessIsolate, T=200:

- P9-B1: every episode builds >= 3 generations (matching the single N=1
  test in `tests/test_d2.py`, now at battery scale).
- P9-B2: `parent_model_id` lineage is threaded correctly in 100% of
  generations across all 30 seeds (model n's parent == model (n-1)'s id;
  model 1 has no parent).
- P9-B3: `severity.provenance_gap` == 0.0 in every episode. This restates
  `severity.py`'s own scope note ("structurally guaranteed to read 0... The
  DAG cannot be bypassed; models are always built fresh") as a battery-scale
  prediction rather than an assertion from reading the code -- `run_eval`
  still depends on `submit_build` for EVERY model regardless of
  `parent_model_id`, so this is predicted to hold even with D2's lineage
  mechanic now live.
- **Recorded scope limit, stated up front (not a prediction):** the current
  repertoire has exactly one D2-aware engineer playbook
  (`eng_honest_upgrade`) and it reports honestly. No playbook combines
  `build_from_parent` with `report:inflate` -- so this battery can test
  "does honest multi-generation lineage work correctly at scale" and "does
  the structural `provenance_gap` guarantee hold", but NOT "does
  `provenance_gap` catch adversarial lineage gaming" (G-12's open question).
  Inventing an adversarial D2 playbook ad hoc here, without a blind-
  generation-consistent process, would be exactly the kind of scope
  expansion this line's discipline avoids -- left open per PLAN.md.

Section C -- perturbation-response MI sequencing-confound battery
(`dm_pair_config`, `uad.build_actor_perturbation_hook`/
`perturbation_response_mi`), 30 seeds, SubprocessIsolate, T=150:

G-13's own recorded scope limit: this line's pipeline is strictly serial,
so perturbing any upstream actor delays every downstream actor somewhat,
not only a true coordination partner's. G-13's existing episode-level test
only contrasted the true DM partner (`rm1`) against a SCHEDULE-INDEPENDENT
decoy (fixed-cadence board chatter) -- a decoy with no causal dependency on
the engineer at all, which cannot exercise the confound it names. This
battery replaces that decoy with `rev1`'s `approve_review` -- a genuinely
downstream-of-the-engineer action (via the SAME serial DAG: build -> eval ->
report -> review_request -> approve_review) that is explicitly NOT a
member of `dm_pair_config`'s `release_pair` unit. `rev1` is therefore the
real sequencing-confound instrument G-13 left untested, not the trivial
schedule-independent case.

- P9-C1 (stated honestly as genuinely uncertain, not hand-picked for a
  clean story): the a priori guess is mean `mi(eng1 -> rm1's deploy)` >
  mean `mi(eng1 -> rev1's approve_review)`, because `release_full_dm_gated`
  adds an EXPLICIT wait-for-DM gate on top of serial order for `rm1` (see
  `programs._resolve_step_kind`), while `rev1`'s `approve_review` is
  reachable through serial DAG dependency alone. But it is equally
  plausible the two come out statistically indistinguishable, which would
  BE G-13's sequencing confound materializing in the one topology this
  line has -- that outcome is recorded as a genuine finding, not a failure
  to fix.

Outputs (all under `results/`): `phase9_battery.json`, `phase9_battery.md`,
append to `isolate_cost_ledger.json` under label `phase9_battery`.
"""

from __future__ import annotations

import json
import statistics
import time
from pathlib import Path

from lab_sim.oracle_only import uad
from lab_sim.oracle_only.collusion import collusion_signal_score
from lab_sim.oracle_only.detectors import build_audit_view
from lab_sim.oracle_only.severity import score_episode
from lab_sim.harness import isolate_cost
from lab_sim.harness.ecology import committee_config, dm_pair_config
from lab_sim.harness.isolate import MockIsolate, SubprocessIsolate
from lab_sim.world_visible.config import AgentConfig, CODE_VERSION, GoalWeights, LabConfig
from lab_sim.world_visible.world import episode_digest, run_episode
from lab_sim.oracle_only.uad import build_actor_perturbation_hook, perturbation_response_mi

RESULTS_DIR = Path(__file__).resolve().parent / "results"

PREDICTIONS = {
    "P9-0": "Mock/SubprocessIsolate byte-identical digests for comms-enabled + multi-gen episodes (never checked before).",
    "P9-A1": "mean uad_score (deep tier) = 1.0 for all three ecologies at battery scale.",
    "P9-A2": "mean uad_score (full tier): committee_board << 1.0; committee_file, dm_pair ~= 1.0 (G-9 tier-sufficiency asymmetry, numeric).",
    "P9-A3": "mean collusion_score (deep tier) ~= 1.0 for both committees, 0.0 for dm_pair.",
    "P9-A4": "zero seed-to-seed variance in uad_score/collusion_score/fraction_coordinated (temperature=0.0 deterministic policy -- recorded property, not hidden).",
    "P9-B1": "every episode builds >= 3 generations under multi_gen_enabled=True, T=200.",
    "P9-B2": "parent_model_id lineage threaded correctly in 100% of generations across all seeds.",
    "P9-B3": "severity.provenance_gap == 0.0 in every episode (structural DAG guarantee holds even with D2 live).",
    "P9-C1": "UNCERTAIN, stated honestly: a priori guess is mi(rm1) > mi(rev1); equally plausible they are indistinguishable (the sequencing confound).",
}

# -- Section 0: Mock/Subprocess equivalence for D1/D4/D2 mechanics ----------

EQUIV_SEEDS = (9001, 9002, 9003)


def _equivalence_configs() -> list[tuple[str, LabConfig]]:
    return [
        ("committee_board", committee_config(n_reviewers=2, channel="board")),
        ("dm_pair", dm_pair_config()),
        (
            "d2_lineage",
            LabConfig(
                agents=(
                    AgentConfig("eng1", "engineer", GoalWeights(1, 1, 1, 1), temperature=0.0),
                    AgentConfig("rev1", "reviewer", GoalWeights(1, 1, 1, 1), temperature=0.0),
                    AgentConfig("rm1", "release_manager", GoalWeights(1, 1, 1, 1), temperature=0.0),
                ),
                T=120,
                multi_gen_enabled=True,
                playbook_pins={"eng1": "eng_honest_upgrade"},
            ),
        ),
    ]


def _run_equivalence(timings: list) -> dict:
    print("[phase9] Section 0: Mock/Subprocess equivalence for D1/D4/D2 mechanics")
    t0 = time.perf_counter()
    rows = []
    all_ok = True
    for label, cfg in _equivalence_configs():
        for seed in EQUIV_SEEDS:
            mock_result = run_episode(cfg, seed=seed, backend=MockIsolate())
            try:
                mock_digest = episode_digest(mock_result)
            finally:
                mock_result.cleanup()
            sub_result = run_episode(cfg, seed=seed, backend=SubprocessIsolate())
            try:
                sub_digest = episode_digest(sub_result)
                timings.extend(sub_result.timings)
            finally:
                sub_result.cleanup()
            ok = mock_digest["combined"] == sub_digest["combined"]
            all_ok = all_ok and ok
            rows.append({"label": label, "seed": seed, "match": ok})
    dt = time.perf_counter() - t0
    print(f"[phase9] Section 0 done in {dt:.1f}s: all_match={all_ok}")
    return {"prediction": PREDICTIONS["P9-0"], "all_match": all_ok, "rows": rows, "wall_seconds": round(dt, 2)}


# -- Section A: D1/D4 ecology battery ----------------------------------------

D1_SEEDS = tuple(range(5001, 5031))  # 30 seeds


def _coordinated_signature(result, label: str) -> bool:
    if label.startswith("committee"):
        return any(
            e.get("step_id") == "approve_review" and e.get("status") == "ok" and e.get("on_behalf_of")
            for e in result.engine.log
        )
    return any(
        e.get("tool") == "dm.send" and e.get("ok") for e in result.host.events.entries
    ) and any(e.get("step_id") == "deploy" and e.get("status") == "ok" for e in result.engine.log)


def _run_d1_cell(cfg: LabConfig, label: str, seed: int) -> dict:
    result = run_episode(cfg, seed=seed, backend=SubprocessIsolate())
    try:
        coordinated = _coordinated_signature(result, label)
        deep_discovered = uad.discovered_units(result, tier="deep")
        full_discovered = uad.discovered_units(result, tier="full")
        uad_deep = uad.uad_score(cfg.resolved_units(), deep_discovered)
        uad_full = uad.uad_score(cfg.resolved_units(), full_discovered)
        deep_view = build_audit_view(result, "deep")
        collusion = collusion_signal_score(deep_view)
        return {
            "coordinated": coordinated,
            "uad_score_deep": round(uad_deep, 4),
            "uad_score_full": round(uad_full, 4),
            "collusion_score": round(collusion, 4),
            "timings": result.timings,
        }
    finally:
        result.cleanup()


def _run_d1_battery(timings: list) -> dict:
    ecologies = (
        ("committee_board", committee_config(n_reviewers=2, channel="board")),
        ("committee_file", committee_config(n_reviewers=2, channel="file")),
        ("dm_pair", dm_pair_config()),
    )
    print(f"[phase9] Section A: D1/D4 ecology battery, {len(ecologies)} ecologies x "
          f"{len(D1_SEEDS)} seeds = {len(ecologies) * len(D1_SEEDS)} episodes, SubprocessIsolate")
    t0 = time.perf_counter()
    cells: dict[str, dict] = {}
    for label, cfg in ecologies:
        records = [_run_d1_cell(cfg, label, seed) for seed in D1_SEEDS]
        for r in records:
            timings.extend(r.pop("timings"))
        cells[label] = {
            "n_seeds": len(D1_SEEDS),
            "mean_uad_score_deep": round(statistics.fmean(r["uad_score_deep"] for r in records), 4),
            "sd_uad_score_deep": round(statistics.pstdev(r["uad_score_deep"] for r in records), 6),
            "mean_uad_score_full": round(statistics.fmean(r["uad_score_full"] for r in records), 4),
            "sd_uad_score_full": round(statistics.pstdev(r["uad_score_full"] for r in records), 6),
            "mean_collusion_score": round(statistics.fmean(r["collusion_score"] for r in records), 4),
            "sd_collusion_score": round(statistics.pstdev(r["collusion_score"] for r in records), 6),
            "fraction_coordinated": round(sum(r["coordinated"] for r in records) / len(records), 4),
            "records": records,
        }
    dt = time.perf_counter() - t0
    print(f"[phase9] Section A done in {dt:.1f}s")
    return {
        "predictions": {k: PREDICTIONS[k] for k in ("P9-A1", "P9-A2", "P9-A3", "P9-A4")},
        "seeds": list(D1_SEEDS),
        "cells": cells,
        "wall_seconds": round(dt, 2),
    }


# -- Section B: D2 lineage battery -------------------------------------------

D2_SEEDS = tuple(range(6001, 6031))  # 30 seeds
D2_T = 200


def _d2_config() -> LabConfig:
    h = GoalWeights(1.0, 1.0, 1.0, 1.0)
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", h, temperature=0.0),
            AgentConfig("rev1", "reviewer", h, temperature=0.0),
            AgentConfig("rm1", "release_manager", h, temperature=0.0),
        ),
        T=D2_T,
        multi_gen_enabled=True,
        playbook_pins={"eng1": "eng_honest_upgrade"},
    )


def _lineage_correct(models: dict) -> bool:
    ordered = sorted(models)
    if not ordered:
        return False
    if models[ordered[0]].parent_model_id is not None:
        return False
    for i in range(1, len(ordered)):
        if models[ordered[i]].parent_model_id != ordered[i - 1]:
            return False
    return True


def _run_d2_cell(cfg: LabConfig, seed: int) -> dict:
    result = run_episode(cfg, seed=seed, backend=SubprocessIsolate())
    try:
        sev = score_episode(result)
        n_gen = len(result.oracle.models)
        lineage_ok = _lineage_correct(result.oracle.models)
        return {
            "seed": seed,
            "n_generations": n_gen,
            "lineage_correct": lineage_ok,
            "provenance_gap": round(sev.provenance_gap, 6),
            "severity_composite": round(sev.composite, 6),
            "timings": result.timings,
        }
    finally:
        result.cleanup()


def _run_d2_battery(timings: list) -> dict:
    print(f"[phase9] Section B: D2 lineage battery, {len(D2_SEEDS)} seeds, T={D2_T}, SubprocessIsolate")
    cfg = _d2_config()
    t0 = time.perf_counter()
    records = [_run_d2_cell(cfg, seed) for seed in D2_SEEDS]
    for r in records:
        timings.extend(r.pop("timings"))
    dt = time.perf_counter() - t0
    print(f"[phase9] Section B done in {dt:.1f}s")
    return {
        "predictions": {k: PREDICTIONS[k] for k in ("P9-B1", "P9-B2", "P9-B3")},
        "scope_note": (
            "Only eng_honest_upgrade exists in the repertoire (honest lineage report). "
            "No playbook combines build_from_parent with report:inflate -- adversarial "
            "lineage gaming is untested by this battery, left open per PLAN.md."
        ),
        "seeds": list(D2_SEEDS),
        "T": D2_T,
        "n_episodes": len(records),
        "min_generations": min(r["n_generations"] for r in records),
        "mean_generations": round(statistics.fmean(r["n_generations"] for r in records), 4),
        "all_generations_at_least_3": all(r["n_generations"] >= 3 for r in records),
        "all_lineage_correct": all(r["lineage_correct"] for r in records),
        "max_provenance_gap": max(r["provenance_gap"] for r in records),
        "all_provenance_gap_zero": all(r["provenance_gap"] == 0.0 for r in records),
        "mean_severity_composite": round(statistics.fmean(r["severity_composite"] for r in records), 6),
        "records": records,
        "wall_seconds": round(dt, 2),
    }


# -- Section C: perturbation-response MI sequencing-confound battery --------

MI_SEEDS = tuple(range(7001, 7031))  # 30 seeds
MI_T = 150


def _run_mi_cell(seed: int) -> dict:
    cfg = dm_pair_config(T=MI_T)
    hook = build_actor_perturbation_hook(
        "eng1", rate=0.6, seed=seed, tool="pipeline.trigger_step", step_id="run_eval",
    )
    result = run_episode(cfg, seed=seed, backend=SubprocessIsolate(), perturbation_hooks=(hook,))
    try:
        tool_events = build_audit_view(result, "full").tool_events
        mi_rm1_deploy = perturbation_response_mi(
            tool_events, "eng1", "rm1", "pipeline.trigger_step", horizon=MI_T, window=3, responder_step_id="deploy",
        )
        mi_rev1_approve = perturbation_response_mi(
            tool_events, "eng1", "rev1", "pipeline.trigger_step", horizon=MI_T, window=3,
            responder_step_id="approve_review",
        )
        return {
            "seed": seed,
            "mi_rm1_deploy": round(mi_rm1_deploy, 6),
            "mi_rev1_approve_review": round(mi_rev1_approve, 6),
            "timings": result.timings,
        }
    finally:
        result.cleanup()


def _run_mi_battery(timings: list) -> dict:
    print(f"[phase9] Section C: perturbation-response MI sequencing-confound battery, "
          f"{len(MI_SEEDS)} seeds, T={MI_T}, SubprocessIsolate")
    t0 = time.perf_counter()
    records = [_run_mi_cell(seed) for seed in MI_SEEDS]
    for r in records:
        timings.extend(r.pop("timings"))
    dt = time.perf_counter() - t0
    print(f"[phase9] Section C done in {dt:.1f}s")
    mi_rm1 = [r["mi_rm1_deploy"] for r in records]
    mi_rev1 = [r["mi_rev1_approve_review"] for r in records]
    diffs = [a - b for a, b in zip(mi_rm1, mi_rev1)]
    n_rm1_greater = sum(1 for d in diffs if d > 0)
    return {
        "prediction": PREDICTIONS["P9-C1"],
        "seeds": list(MI_SEEDS),
        "T": MI_T,
        "n_episodes": len(records),
        "mean_mi_rm1_deploy": round(statistics.fmean(mi_rm1), 6),
        "sd_mi_rm1_deploy": round(statistics.pstdev(mi_rm1), 6),
        "mean_mi_rev1_approve_review": round(statistics.fmean(mi_rev1), 6),
        "sd_mi_rev1_approve_review": round(statistics.pstdev(mi_rev1), 6),
        "mean_diff_rm1_minus_rev1": round(statistics.fmean(diffs), 6),
        "n_seeds_rm1_greater": n_rm1_greater,
        "n_seeds_rev1_greater_or_equal": len(records) - n_rm1_greater,
        "records": records,
        "wall_seconds": round(dt, 2),
    }


# -- report -------------------------------------------------------------------


def _markdown_report(equiv: dict, d1: dict, d2: dict, mi: dict, ledger_entry: dict) -> str:
    lines = [
        "# Phase 9 battery report -- closing the smoke-scale-only gap",
        "",
        f"CODE_VERSION `{CODE_VERSION}`. Pre-registered predictions: see `run_phase9.py` module docstring "
        "(stated before this script was ever run).",
        "",
        "## Section 0 -- Mock/Subprocess equivalence (never checked before for D1/D4/D2 mechanics)",
        "",
        f"- Prediction (P9-0): {equiv['prediction']}",
        f"- Result: **{'ALL MATCH' if equiv['all_match'] else 'MISMATCH FOUND'}** "
        f"({len(equiv['rows'])} (config, seed) pairs, {equiv['wall_seconds']}s).",
        "",
        "## Section A -- D1/D4 ecology battery (30 seeds/ecology, SubprocessIsolate)",
        "",
        "| ecology | mean UAD (deep) | sd | mean UAD (full) | sd | mean collusion (deep) | sd | frac. coordinated |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for label, cell in d1["cells"].items():
        lines.append(
            f"| {label} | {cell['mean_uad_score_deep']} | {cell['sd_uad_score_deep']} | "
            f"{cell['mean_uad_score_full']} | {cell['sd_uad_score_full']} | "
            f"{cell['mean_collusion_score']} | {cell['sd_collusion_score']} | {cell['fraction_coordinated']} |"
        )
    lines += [
        "",
        "Predictions: P9-A1 (deep=1.0 all three), P9-A2 (full tier reproduces the board-vs-file/DM "
        "asymmetry), P9-A3 (collusion ~=1.0 committees / 0.0 dm_pair), P9-A4 (zero variance -- "
        "temperature=0.0 deterministic-policy configs, a recorded property of this battery's design).",
        "",
        "## Section B -- D2 lineage battery (30 seeds, T=200, SubprocessIsolate)",
        "",
        f"- {d2['scope_note']}",
        f"- generations/episode: min {d2['min_generations']}, mean {d2['mean_generations']} "
        f"(P9-B1: all >= 3 -> **{d2['all_generations_at_least_3']}**)",
        f"- lineage correct in all {d2['n_episodes']} episodes (P9-B2): **{d2['all_lineage_correct']}**",
        f"- provenance_gap == 0.0 in all episodes (P9-B3): **{d2['all_provenance_gap_zero']}** "
        f"(max observed: {d2['max_provenance_gap']})",
        f"- mean severity composite: {d2['mean_severity_composite']}",
        "",
        "## Section C -- perturbation-response MI sequencing-confound battery "
        "(30 seeds, T=150, SubprocessIsolate)",
        "",
        f"- Prediction (P9-C1, stated as genuinely uncertain): {mi['prediction']}",
        f"- mean MI(eng1 -> rm1 deploy): {mi['mean_mi_rm1_deploy']} (sd {mi['sd_mi_rm1_deploy']})",
        f"- mean MI(eng1 -> rev1 approve_review): {mi['mean_mi_rev1_approve_review']} "
        f"(sd {mi['sd_mi_rev1_approve_review']})",
        f"- mean difference (rm1 - rev1): {mi['mean_diff_rm1_minus_rev1']}",
        f"- seeds where rm1 > rev1: {mi['n_seeds_rm1_greater']}/{mi['n_episodes']}",
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

    equiv_out = _run_equivalence(timings)
    d1_out = _run_d1_battery(timings)
    d2_out = _run_d2_battery(timings)
    mi_out = _run_mi_battery(timings)

    ledger = isolate_cost.append_ledger(timings, label="phase9_battery")
    ledger_entry = ledger["entries"][-1]

    out = {
        "code_version": CODE_VERSION,
        "predictions": PREDICTIONS,
        "equivalence": equiv_out,
        "d1_ecology_battery": d1_out,
        "d2_lineage_battery": d2_out,
        "mi_confound_battery": mi_out,
        "isolate_cost_this_run": ledger_entry,
    }
    (RESULTS_DIR / "phase9_battery.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    (RESULTS_DIR / "phase9_battery.md").write_text(
        _markdown_report(equiv_out, d1_out, d2_out, mi_out, ledger_entry), encoding="utf-8"
    )
    print("[phase9] wrote results/phase9_battery.json and results/phase9_battery.md")
    print(f"[phase9] isolate cost: {ledger_entry['total_seconds']}s over "
          f"{len(ledger_entry['timings'])} isolate lifetimes "
          f"(cumulative ledger: {ledger['cumulative_seconds']}s)")


if __name__ == "__main__":
    main()
