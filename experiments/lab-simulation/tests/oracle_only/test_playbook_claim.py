"""Tests for playbook claim/behavior gap detector (LS-3 extension)."""

from __future__ import annotations

import json

from lab_sim.world_visible.config import AdminConfig, AgentConfig, BoardConfig, GoalWeights, LabConfig
from lab_sim.oracle_only.detectors import AuditView, build_audit_view
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.playbook_claim import playbook_claim_gap_score
from lab_sim.agent_visible.playbooks import merged_repertoire, playbook_by_name
from lab_sim.harness.protocol import GENERATED_REPERTOIRE_PATH
from lab_sim.world_visible.world import run_episode


def _cfg(extra_playbooks=(), T=80) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", GoalWeights(1.0, 1.0, 1.0, 1.0), temperature=0.0),
            AgentConfig("rev1", "reviewer", GoalWeights(1.0, 1.0, 1.0, 1.0), temperature=0.0),
            AgentConfig("rm1", "release_manager", GoalWeights(1.0, 1.0, 1.0, 1.0), temperature=0.0),
            AgentConfig("admin1", "admin", GoalWeights(1, 1, 1, 1)),
        ),
        board=BoardConfig(),
        admin=AdminConfig(),
        T=T,
        extra_playbooks=extra_playbooks,
    )


def test_playbook_selection_events_logged_at_full_tier():
    result = run_episode(_cfg(), seed=1, backend=MockIsolate())
    try:
        view = build_audit_view(result, "full")
        selections = [e for e in (view.tool_events or []) if e.get("tool") == "playbook.selection"]
        assert selections
        assert "feature_deltas" in selections[0]
        assert "step_kinds" in selections[0]
    finally:
        result.cleanup()


def test_playbook_claim_gap_detects_quick_approver_facade():
    data = json.loads(GENERATED_REPERTOIRE_PATH.read_text(encoding="utf-8"))
    facade = next(p for p in data["playbooks"] if p["name"] == "quick_approver_facade")
    rep = merged_repertoire((facade,))
    pb = playbook_by_name("reviewer", "quick_approver_facade", repertoire=rep)
    view = AuditView(
        tier="full",
        engine_log=[],
        access_log=[],
        tool_events=[
            {
                "tool": "playbook.selection",
                "feature_deltas": pb.feature_deltas,
                "step_kinds": list(pb.step_kinds),
            }
        ],
    )
    assert playbook_claim_gap_score(view) == 1.0


def test_playbook_claim_gap_blind_below_full_tier():
    result = run_episode(_cfg(), seed=1, backend=MockIsolate())
    try:
        assert playbook_claim_gap_score(build_audit_view(result, "light")) == 0.0
    finally:
        result.cleanup()
