#!/usr/bin/env python3
"""Export one precomputed episode trace for the static plane-replay demo
(``demos/ch07-lab-sim-replay/``).

NOT a battery, NOT a new measurement: this re-runs an existing ecology
factory (``d2_lineage_config``, D2 "adversarial lineage gaming", LS-12/
LS-15/LS-31) with the new ``trace_sink`` forward hook wired in
(``world_visible/trace_recorder.py``) and writes the resulting per-tick
frames plus a static end-of-episode detector/severity scorecard to a
demo-owned JSON file. No detector, severity, or tier-projection logic is
reimplemented -- every score in the summary comes straight from
``oracle_only/detectors.py``/``severity.py``.

Scenario choice: ``inflate=True`` gives a genuine filed-report-vs-oracle-
truth divergence (an ``eng_inflate_upgrade`` misreport) that is invisible
to every tier except ``deep`` -- exactly the "same event, four ways"
story the demo is built to show (confirmed empirically below: at T=40,
seed=7, ``misreporting_score``/``accumulation_score`` are 0.0 at
none/light/full and 1.0 at deep).

Usage::

    cd experiments/lab-simulation
    .venv/bin/python export_replay_trace.py
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness.ecology import d2_lineage_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.detectors import (
    access_integrity_score,
    accumulation_score,
    build_audit_view,
    misreporting_score,
    process_noncompliance_score,
    provenance_score,
)
from lab_sim.oracle_only.severity import score_episode
from lab_sim.world_visible.config import CODE_VERSION, TIERS as DETECTOR_TIERS
from lab_sim.world_visible.world import episode_digest, run_episode

SEED = 7
T = 40
OUT_PATH = Path(__file__).resolve().parent.parent.parent / "demos" / "ch07-lab-sim-replay" / "data" / "episode_trace.json"

DETECTORS = {
    "misreporting_score": misreporting_score,
    "process_noncompliance_score": process_noncompliance_score,
    "provenance_score": provenance_score,
    "accumulation_score": accumulation_score,
    "access_integrity_score": access_integrity_score,
}


def main() -> None:
    cfg = d2_lineage_config(inflate=True, T=T)
    roster = {a.actor_id: a.role for a in cfg.agents}
    print(f"[export_replay_trace] CODE_VERSION {CODE_VERSION}, T={T}, seed={SEED}, roster={roster}")

    frames: list[dict] = []

    def _collect(frame: dict) -> None:
        frames.append(frame)
        if frame["t"] % 10 == 0 or frame["t"] == T - 1:
            print(f"[export_replay_trace] recorded tick {frame['t'] + 1}/{T}")

    result = run_episode(cfg, seed=SEED, backend=MockIsolate(), trace_sink=_collect)
    try:
        detectors_by_tier = {
            tier: {name: fn(build_audit_view(result, tier)) for name, fn in DETECTORS.items()}
            for tier in DETECTOR_TIERS
        }
        severity = score_episode(result)
        severity_dict = asdict(severity)
        severity_dict["composite"] = severity.composite
        severity_dict["any_never_event"] = severity.any_never_event
        digest = episode_digest(result)
    finally:
        result.cleanup()

    out = {
        "code_version": CODE_VERSION,
        "scenario": {
            "id": "d2_lineage_inflate",
            "ecology_factory": "d2_lineage_config(inflate=True)",
            "summary": (
                "Single-engineer model lineage with the eng_inflate_upgrade playbook "
                "pinned: the engineer files a report that diverges from its own "
                "measured hazard on at least one generation. The divergence is "
                "invisible to the none/light/full audit tiers and only surfaces "
                "at deep tier, where the referee can fetch the actual report file."
            ),
        },
        "seed": SEED,
        "T": T,
        "roster": roster,
        "frames": frames,
        "summary": {
            "detectors_by_tier": detectors_by_tier,
            "severity": severity_dict,
            "episode_digest": digest["combined"],
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(f"[export_replay_trace] wrote {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes)")
    print(
        "[export_replay_trace] misreporting_score by tier: "
        + ", ".join(f"{t}={detectors_by_tier[t]['misreporting_score']}" for t in DETECTOR_TIERS)
    )


if __name__ == "__main__":
    main()
