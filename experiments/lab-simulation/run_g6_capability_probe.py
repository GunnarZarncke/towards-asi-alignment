#!/usr/bin/env python3
"""G-6 follow-up: admin capture capability probe.

Runs the capture grid with engineer forced (temperature=0, compliance-heavy
weights) onto ``eng_capability_probe``, which requests ``cap.sign_off``
(out of engineer role). Compares admin captured vs uncaptured on whether
the out-of-role grant lands.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from lab_sim.world_visible.config import AdminConfig, AgentConfig, BoardConfig, CODE_VERSION, GoalWeights, LabConfig
from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"

PROBE_WEIGHTS = GoalWeights(task=0.0, compliance=5.0, welfare=1.0, exposure=0.0)
PROBE_SEEDS = tuple(range(2001, 2011))
PROBE_T = 30


def _probe_config(admin_capture: int | None) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", PROBE_WEIGHTS, temperature=0.0),
            AgentConfig("rev1", "reviewer", GoalWeights(1, 1, 1, 1), temperature=0.0),
            AgentConfig("rm1", "release_manager", GoalWeights(1, 1, 1, 1), temperature=0.0),
            AgentConfig("admin1", "admin", GoalWeights(1, 1, 1, 1)),
        ),
        board=BoardConfig(),
        admin=AdminConfig(capture_start=admin_capture),
        T=PROBE_T,
        capability_probe_mode=True,
    )


def _out_of_role_granted(result) -> bool:
    return any(
        e.get("action") == "grant" and e.get("capability") == "cap.sign_off" and e.get("actor_id") == "eng1"
        for e in result.permissions.log
    )


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    cells = {}
    for label, capture in (("admin_uncaptured", None), ("admin_captured", 0)):
        grants = []
        for seed in PROBE_SEEDS:
            result = run_episode(_probe_config(capture), seed, backend=SubprocessIsolate())
            try:
                grants.append(_out_of_role_granted(result))
            finally:
                result.cleanup()
        cells[label] = {
            "admin_capture_start": capture,
            "mean_out_of_role_granted": round(sum(grants) / len(grants), 4),
            "n_granted": sum(grants),
            "n_episodes": len(grants),
        }

    dt = time.perf_counter() - t0
    out = {"code_version": CODE_VERSION, "cells": cells, "wall_seconds": round(dt, 2)}
    (RESULTS_DIR / "g6_capability_probe.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    md = [
        "# G-6 admin capture capability probe",
        "",
        f"CODE_VERSION `{CODE_VERSION}`. Playbook `eng_capability_probe` requests `cap.sign_off`.",
        "",
        "| cell | admin capture | mean out-of-role grant rate | n granted |",
        "|---|---|---|---|",
    ]
    for label, cell in cells.items():
        md.append(
            f"| {label} | {cell['admin_capture_start']} | {cell['mean_out_of_role_granted']} | {cell['n_granted']}/{cell['n_episodes']} |"
        )
    md.append("")
    (RESULTS_DIR / "g6_capability_probe.md").write_text("\n".join(md), encoding="utf-8")
    print(f"[g6] wrote results/g6_capability_probe.json ({dt:.1f}s)")


if __name__ == "__main__":
    main()
