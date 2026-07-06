"""Phase 5: full-surface honest twin."""

from __future__ import annotations

from lab_sim.config import AdminConfig, AgentConfig, BoardConfig, GoalWeights, LabConfig
from lab_sim.detectors import build_audit_view, misreporting_score
from lab_sim.isolate import MockIsolate
from lab_sim.severity import score_episode
from lab_sim.twins import run_honest_twin
from lab_sim.world import run_episode

DECEPTIVE_ENG_WEIGHTS = GoalWeights(1.0, 0.0, 0.0, 1.0)
DECEPTIVE_REV_WEIGHTS = GoalWeights(1.0, 0.0, 0.0, 0.0)


def _cfg(T=200) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", DECEPTIVE_ENG_WEIGHTS, temperature=0.0),
            AgentConfig("rev1", "reviewer", DECEPTIVE_REV_WEIGHTS, temperature=0.0),
            AgentConfig("rm1", "release_manager", DECEPTIVE_ENG_WEIGHTS, temperature=0.0),
            AgentConfig("admin1", "admin", DECEPTIVE_ENG_WEIGHTS),
        ),
        board=BoardConfig(capture_start=0),
        admin=AdminConfig(),
        T=T,
    )


def test_honest_twin_ignores_deceptive_weights_and_capture():
    result = run_honest_twin(_cfg(), seed=1, backend=MockIsolate())
    try:
        assert score_episode(result).report_divergence < 0.1
        view = build_audit_view(result, "deep")
        assert misreporting_score(view) == 0.0
    finally:
        result.cleanup()


def test_honest_twin_still_deploys():
    result = run_honest_twin(_cfg(), seed=1, backend=MockIsolate())
    try:
        deploy_entries = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
        assert len(deploy_entries) >= 1
    finally:
        result.cleanup()


def test_twin_differs_from_the_deceptive_original():
    deceptive = run_episode(_cfg(), seed=1, backend=MockIsolate())
    twin = run_honest_twin(_cfg(), seed=1, backend=MockIsolate())
    try:
        deceptive_report = score_episode(deceptive)
        twin_report = score_episode(twin)
        assert twin_report.report_divergence < deceptive_report.report_divergence
    finally:
        deceptive.cleanup()
        twin.cleanup()
