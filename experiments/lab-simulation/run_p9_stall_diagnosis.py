#!/usr/bin/env python3
"""Follow-up diagnosis for two `run_phase9.py` prediction misses (P9-A1/A4,
P9-B1) -- NOT a new battery, a reproducible root-cause check for two
specific (config, seed) pairs the battery flagged as anomalous.

Both anomalies trace to the SAME mechanic: `programs._resolve_step_kind`'s
documented "stall-on-hazard" rule (the same one `review_conscientious` and
`_resolve_review_committee`'s chair/solo branches share) firing as a
NATURAL eval-noise tail event under the Phase 0-6 DEFAULT build params
(`scale=0.6, safety_effort=0.5`, expected hazard ~0.35) -- not the
deliberately engineered high-hazard `build_params` Phase 7's capture grid
needed (DESIGN.md "Phase 7"). `run_eval`'s measured_hazard carries its own
oracle noise on top of the model's true_hazard; occasionally that pushes
the REPORTED value over `ontology.REVIEW_HAZARD_THRESHOLD` (0.5) even when
true_hazard itself is below it -- an honest, non-deceptive reviewer then
correctly declines to approve, and (since neither the committee mechanic
nor the D2 single-model-in-flight slot has a "reviewer rejected, retry with
a new build" fallback in the current repertoire) the pipeline stalls for
the rest of the episode. This is a real, useful negative about the
DEFAULT build-params regime's margin from `REVIEW_HAZARD_THRESHOLD`, not a
bug in the reviewer/committee mechanics -- both seeds below are re-run with
`MockIsolate` (cheap, deterministic-with-seed) purely to print the exact
oracle-side evidence FINDINGS.md's LS-14/LS-15 cite.
"""

from __future__ import annotations

import json
from pathlib import Path

from lab_sim.harness.ecology import committee_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.detectors import build_audit_view
from lab_sim.oracle_only.uad import build_coordination_trace
from lab_sim.world_visible.config import AgentConfig, GoalWeights, LabConfig
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def _diagnose_committee_board_seed_5015() -> dict:
    cfg = committee_config(n_reviewers=2, channel="board")
    result = run_episode(cfg, seed=5015, backend=MockIsolate())
    try:
        model = result.oracle.models["m001"]
        eval_events = [e for e in result.engine.log if e["step_id"] == "run_eval" and e["status"] == "ok"]
        measured_hazard = eval_events[0]["payload"]["measured_hazard"] if eval_events else None
        deep_view = build_audit_view(result, "deep")
        trace = build_coordination_trace(deep_view.message_contents)
        approve_review_events = [e for e in result.engine.log if e["step_id"] == "approve_review"]
        return {
            "config": "committee_board",
            "seed": 5015,
            "m001_true_hazard": model.true_hazard,
            "m001_measured_hazard_on_filed_report": measured_hazard,
            "review_hazard_threshold": 0.5,
            "votes_cast": [{"actor_id": v.actor_id, "vote": v.vote} for v in trace],
            "approve_review_attempts": len(approve_review_events),
        }
    finally:
        result.cleanup()


def _diagnose_d2_seed_6020() -> dict:
    h = GoalWeights(1.0, 1.0, 1.0, 1.0)
    cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", h, temperature=0.0),
            AgentConfig("rev1", "reviewer", h, temperature=0.0),
            AgentConfig("rm1", "release_manager", h, temperature=0.0),
        ),
        T=200, multi_gen_enabled=True, playbook_pins={"eng1": "eng_honest_upgrade"},
    )
    result = run_episode(cfg, seed=6020, backend=MockIsolate())
    try:
        model = result.oracle.models["m001"]
        eval_events = [e for e in result.engine.log if e["step_id"] == "run_eval" and e["status"] == "ok"]
        measured_hazard = eval_events[0]["payload"]["measured_hazard"] if eval_events else None
        approve_review_events = [e for e in result.engine.log if e["step_id"] == "approve_review"]
        return {
            "config": "d2_lineage",
            "seed": 6020,
            "n_models_built": len(result.oracle.models),
            "m001_true_hazard": model.true_hazard,
            "m001_measured_hazard_on_filed_report": measured_hazard,
            "review_hazard_threshold": 0.5,
            "approve_review_attempts": len(approve_review_events),
        }
    finally:
        result.cleanup()


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = {
        "purpose": (
            "Root-cause for run_phase9.py's P9-A1/A4 (committee_board seed 5015) and "
            "P9-B1 (d2_lineage seed 6020) prediction misses -- see FINDINGS.md LS-14/LS-15."
        ),
        "committee_board_seed_5015": _diagnose_committee_board_seed_5015(),
        "d2_lineage_seed_6020": _diagnose_d2_seed_6020(),
    }
    (RESULTS_DIR / "phase9_stall_diagnosis.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
