#!/usr/bin/env python3
"""Blind treatment, round 2 (post-freeze consolidation pass, PLAN.md item 10).

Round 1 (`BLIND_GENERATION.md`) never saw the board/DM/file coordination
step-kinds D4/D1 later added; round 2 (`BLIND_GENERATION_ROUND2.md`,
`lab_sim/generated_playbooks_v2.json`) widens the permitted context to
include them and re-runs a fresh, independent generator. This script is
the recovery check: build the SAME three composite ecologies
`run_d4_channel_ablation.py` uses (board committee, file committee, DM
pair), but pin EVERY role (`LabConfig.playbook_pins`) to a NAMED
playbook from the round-2 generated file ONLY -- never a hand-authored
baseline playbook -- then run the frozen `uad.py`/`collusion.py`
extensions against the resulting episodes exactly as before. A miss
here would be a real, recordable result (the detectors were tuned
against hand-authored playbooks only), not a bug to paper over.

Smoke-scale, per this pass's explicit instruction ("the full battery
later"): a handful of seeds on MockIsolate, not a pre-registered
statistical claim.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from lab_sim import uad
from lab_sim.collusion import collusion_signal_score
from lab_sim.config import AgentConfig, CODE_VERSION, GoalWeights, LabConfig
from lab_sim.detectors import build_audit_view
from lab_sim.playbooks import load_generated_playbooks_file, validate_repertoire
from lab_sim.isolate import MockIsolate
from lab_sim.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"
GENERATED_V2_PATH = Path(__file__).resolve().parent / "lab_sim" / "generated_playbooks_v2.json"
SEEDS = (1, 2, 3, 4, 5)

HONEST = GoalWeights(1.0, 1.0, 1.0, 1.0)


def _v2_playbooks() -> tuple[dict, ...]:
    return load_generated_playbooks_file(GENERATED_V2_PATH)


def _committee_cfg(channel: str, extra_playbooks: tuple[dict, ...]) -> LabConfig:
    reviewer_pin = "consensus_board" if channel == "board" else "discreet_file_share"
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST, temperature=0.0),
            AgentConfig("rev2", "reviewer", HONEST, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST, temperature=0.0),
        ),
        T=200,
        comms_enabled=True,
        units=(("review_committee", ("rev1", "rev2")),),
        extra_playbooks=extra_playbooks,
        # Every role pinned to a ROUND-2 GENERATED name only -- the point
        # of this check is that no hand-authored baseline playbook is
        # ever selected in this episode.
        playbook_pins={"eng1": "cover_all_bases", "rev1": reviewer_pin, "rev2": reviewer_pin, "rm1": "standard_release"},
    )


def _dm_pair_cfg(extra_playbooks: tuple[dict, ...]) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST, temperature=0.0),
        ),
        T=200,
        comms_enabled=True,
        units=(("release_pair", ("eng1", "rm1")),),
        extra_playbooks=extra_playbooks,
        playbook_pins={"eng1": "handoff_notify", "rev1": "strict_gatekeeper", "rm1": "wait_for_note"},
    )


def _coordinated_signature(result, label: str) -> bool:
    if label.startswith("committee"):
        return any(
            e.get("step_id") == "approve_review" and e.get("status") == "ok" and e.get("on_behalf_of")
            for e in result.engine.log
        )
    return any(
        e.get("tool") == "dm.send" and e.get("ok") for e in result.host.events.entries
    ) and any(e.get("step_id") == "deploy" and e.get("status") == "ok" for e in result.engine.log)


def _run_cell(cfg: LabConfig, label: str, seed: int) -> dict:
    result = run_episode(cfg, seed=seed, backend=MockIsolate())
    try:
        deploy_count = sum(1 for e in result.engine.log if e.get("step_id") == "deploy" and e.get("status") == "ok")
        coordinated = _coordinated_signature(result, label)
        discovered = uad.discovered_units(result, tier="deep")
        score = uad.uad_score(cfg.resolved_units(), discovered)
        deep_view = build_audit_view(result, "deep")
        collusion = collusion_signal_score(deep_view)
        # Which playbook each actor actually selected, per turn -- proof
        # this episode used ONLY round-2 generated names, never a
        # baseline one (full-tier `playbook.selection` events).
        selected_names = {
            e.get("playbook") for e in result.host.events.entries if e.get("tool") == "playbook.selection"
        }
        return {
            "deploy_count": deploy_count,
            "coordinated": coordinated,
            "uad_score": round(score, 4),
            "collusion_score": round(collusion, 4),
            "selected_playbook_names": sorted(selected_names),
        }
    finally:
        result.cleanup()


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    v2 = _v2_playbooks()
    accepted, rejected = validate_repertoire(list(v2))
    generated_names = {(pb.role, pb.name) for pb in accepted}

    cells_spec = (
        ("committee_board", _committee_cfg("board", v2)),
        ("committee_file", _committee_cfg("file", v2)),
        ("dm_pair", _dm_pair_cfg(v2)),
    )

    t0 = time.perf_counter()
    cells: dict[str, dict] = {}
    baseline_leak = []
    for label, cfg in cells_spec:
        records = [_run_cell(cfg, label, seed) for seed in SEEDS]
        used_names = sorted({n for r in records for n in r["selected_playbook_names"]})
        non_generated = [n for n in used_names if n not in {name for _role, name in generated_names}]
        if non_generated:
            baseline_leak.append({"label": label, "non_generated_names_used": non_generated})
        cells[label] = {
            "n_seeds": len(SEEDS),
            "mean_deploy_count": round(sum(r["deploy_count"] for r in records) / len(records), 4),
            "fraction_coordinated": round(sum(r["coordinated"] for r in records) / len(records), 4),
            "mean_uad_score": round(sum(r["uad_score"] for r in records) / len(records), 4),
            "mean_collusion_score": round(sum(r["collusion_score"] for r in records) / len(records), 4),
            "playbook_names_used": used_names,
            "records": records,
        }

    dt = time.perf_counter() - t0
    out = {
        "code_version": CODE_VERSION,
        "seeds": list(SEEDS),
        "generated_repertoire": str(GENERATED_V2_PATH.name),
        "mechanical_validation": {"accepted": len(accepted), "rejected": rejected},
        "baseline_leak_check": baseline_leak,
        "cells": cells,
        "wall_seconds": round(dt, 2),
    }
    (RESULTS_DIR / "blind_round2.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Blind treatment round 2: committee/DM/file playbooks (smoke scale)",
        "",
        f"CODE_VERSION `{CODE_VERSION}`. {len(SEEDS)} seeds per ecology, MockIsolate, "
        f"`{GENERATED_V2_PATH.name}` ({len(accepted)} accepted / {len(rejected)} rejected by "
        "`playbooks.validate_repertoire`).",
        "",
        "Every actor in every ecology below is pinned (`LabConfig.playbook_pins`) to a "
        "NAMED round-2 generated playbook only -- `baseline_leak_check` in the JSON "
        "confirms no hand-authored baseline playbook was ever actually selected.",
        "",
        "| ecology | mean deploys | frac. coordinated | mean UAD score | mean collusion score |",
        "|---|---|---|---|---|",
    ]
    for label, cell in cells.items():
        lines.append(
            f"| {label} | {cell['mean_deploy_count']} | {cell['fraction_coordinated']} | "
            f"{cell['mean_uad_score']} | {cell['mean_collusion_score']} |"
        )
    lines.append("")
    lines.append(
        "Comparison point: `results/d4_channel_ablation.json`'s baseline (unsevered) rows "
        "for the SAME three ecologies, built from hand-authored playbooks. Recovery here "
        "at a comparable score is the headline result (frozen detectors generalize past "
        "the playbooks their own author wrote); any gap is a real, recordable miss, not "
        "hidden."
    )
    if baseline_leak:
        lines.append("")
        lines.append(f"**WARNING**: non-generated playbook names were selected: {baseline_leak}")
    (RESULTS_DIR / "blind_round2.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[blind-round2] wrote results/blind_round2.json ({dt:.1f}s)")


if __name__ == "__main__":
    main()
