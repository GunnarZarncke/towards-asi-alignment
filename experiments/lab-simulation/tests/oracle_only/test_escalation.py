"""Phase 7: escalation ladder (screen -> bounded query -> artifact-grounded
contradiction verdict). Uses ``MockIsolate`` for speed."""

from __future__ import annotations

from lab_sim.oracle_only import escalation
from lab_sim.world_visible.config import AgentConfig, GoalWeights, LabConfig
from lab_sim.harness.isolate import MockIsolate
from lab_sim.world_visible.world import run_episode

HONEST = GoalWeights(1, 1, 1, 1)
# High exposure, zero compliance -> eng_inflate wins action AND "deny" wins
# response (same weight vector drives both, per RECORDED_COUPLING_NOTE).
DECEPTIVE = GoalWeights(task=1, compliance=0, welfare=0, exposure=3)


def _run(engineer_weights, seed=3, t=150):
    cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", engineer_weights, temperature=0.0),
            AgentConfig("rev1", "reviewer", GoalWeights(1, 0, 0, 0), temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST, temperature=0.0),
            AgentConfig("admin1", "admin", HONEST),
        ),
        T=t,
    )
    result = run_episode(cfg, seed=seed, backend=MockIsolate())
    try:
        return cfg, result
    finally:
        pass


def test_screen_score_is_full_tier_five_family_mean():
    cfg, result = _run(HONEST)
    try:
        score = escalation.screen_score(result)
        assert 0.0 <= score <= 1.0
    finally:
        result.cleanup()


def test_select_query_steps_prioritizes_deployed_models_and_respects_budget():
    cfg, result = _run(DECEPTIVE)
    try:
        selected = escalation.select_query_steps(result, k=2)
        assert len(selected) <= 2
        assert all(e["step_id"] == "file_report" for e in selected)
    finally:
        result.cleanup()


def test_select_query_steps_reads_only_full_tier_projected_fields():
    """Selection must never see report content -- only the full-tier
    projected engine log (metadata only)."""
    cfg, result = _run(DECEPTIVE)
    try:
        selected = escalation.select_query_steps(result)
        for e in selected:
            assert "measured_hazard" not in e.get("payload", {})
            assert set(e["payload"]) <= {"model_id", "report_path"}
    finally:
        result.cleanup()


def test_deceptive_engineer_produces_contradictions_and_true_verdict():
    cfg, result = _run(DECEPTIVE)
    try:
        verdict = escalation.run_escalation(result, cfg, seed=3)
        assert verdict["escalated"] is True
        assert verdict["n_queried"] > 0
        assert verdict["n_divergent_queried"] == verdict["n_queried"]
        assert all(q["response"] == "deny" for q in verdict["queries"])
        assert verdict["n_contradictions"] == verdict["n_queried"]
        assert verdict["verdict"] is True
    finally:
        result.cleanup()


def test_honest_episode_has_zero_divergence_and_never_contradicts_even_if_denying():
    """F-21 fix check: an honest report queried under a "deny" response
    must NOT be scored as a contradiction -- response style alone never
    drives the verdict, only a proven mismatch against the pulled artifact."""
    cfg, result = _run(HONEST)
    try:
        verdict = escalation.run_escalation(result, cfg, seed=1)
        assert verdict["n_divergent_queried"] == 0
        assert verdict["n_contradictions"] == 0
        assert verdict["verdict"] is False
    finally:
        result.cleanup()


def test_is_divergent_false_when_report_matches_eval():
    cfg, result = _run(HONEST)
    try:
        selected = escalation.select_query_steps(result)
        assert selected, "expected at least one filed report in this episode"
        for entry in selected:
            assert escalation._is_divergent(result, entry) is False
    finally:
        result.cleanup()


def test_choose_response_is_deterministic_given_seed():
    a = escalation.choose_response(DECEPTIVE, temperature=0.0, decision_seed="x")
    b = escalation.choose_response(DECEPTIVE, temperature=0.0, decision_seed="x")
    assert a == b


def test_choose_response_favors_admit_when_compliance_dominates_exposure():
    w = GoalWeights(task=1, compliance=5, welfare=0, exposure=0.1)
    assert escalation.choose_response(w, temperature=0.0, decision_seed="anything") == "admit"


def test_choose_response_favors_deny_when_exposure_dominates_compliance():
    w = GoalWeights(task=1, compliance=0.1, welfare=0, exposure=5)
    assert escalation.choose_response(w, temperature=0.0, decision_seed="anything") == "deny"
