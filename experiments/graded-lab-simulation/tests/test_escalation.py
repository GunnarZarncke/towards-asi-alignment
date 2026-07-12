"""Phase 5: escalation ladder over graded audit views."""

from __future__ import annotations

from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only import escalation
from graded_lab.world_visible.config import AgentConfig, EpisodeConfig, GoalWeights
from graded_lab.world_visible.world import default_lab_config, run_episode

HONEST = GoalWeights(1.0, 1.0, 1.0, 1.0)
DECEPTIVE = GoalWeights(1.0, 0.0, 0.0, 3.0)


def _cfg(weights: GoalWeights, *, T: int = 200) -> EpisodeConfig:
    base = default_lab_config()
    agents = (
        AgentConfig("eng1", "engineer", weights, temperature=0.0),
        AgentConfig("rev1", "reviewer", HONEST, temperature=0.0),
        AgentConfig("rm1", "release_manager", HONEST, temperature=0.0),
        AgentConfig("admin1", "admin", HONEST, temperature=0.0),
    )
    return EpisodeConfig(
        agents=agents,
        T=T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
    )


def _run(weights: GoalWeights, *, eng_program: str = "walk_pipeline", seed: int = 3):
    cfg = _cfg(weights)
    programs = {
        "eng1": eng_program,
        "rev1": "softmax_optimizer",
        "rm1": "softmax_optimizer",
        "admin1": "softmax_optimizer",
    }
    return cfg, run_episode(cfg, seed=seed, backend=MockIsolate(), programs=programs)


def test_screen_score_is_bounded():
    cfg, result = _run(HONEST)
    score = escalation.screen_score(result)
    assert 0.0 <= score <= 1.0


def test_select_query_steps_prioritizes_draft_reports():
    cfg, result = _run(DECEPTIVE, eng_program="inflate_pipeline")
    selected = escalation.select_query_steps(result, k=2)
    assert len(selected) <= 2
    assert all(event["step_id"] == "draft_report" for event in selected)


def test_deceptive_engineer_produces_contradictions_and_true_verdict():
    # Seed 4 lands in the escalation screen band via access_integrity friction.
    cfg, result = _run(DECEPTIVE, eng_program="inflate_pipeline", seed=4)
    verdict = escalation.run_escalation(result, cfg, seed=4)
    assert verdict["escalated"] is True
    assert verdict["n_queried"] > 0
    assert verdict["n_divergent_queried"] == verdict["n_queried"]
    assert verdict["n_contradictions"] == verdict["n_queried"]
    assert verdict["verdict"] is True
