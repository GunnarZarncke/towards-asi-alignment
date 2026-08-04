"""Phase 5: tier-gated detectors across all five families."""

from __future__ import annotations

from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.detectors import (
    accumulation_score,
    build_audit_view,
    misreporting_score,
    process_noncompliance_score,
    provenance_score,
    run_all_detectors,
)
from graded_lab.world_visible.config import AgentConfig, EpisodeConfig, GoalWeights
from graded_lab.world_visible.world import default_lab_config, run_episode

HONEST = GoalWeights(1.0, 1.0, 1.0, 1.0)
DECEPTIVE = GoalWeights(1.0, 0.0, 0.0, 1.0)


def _programs(eng_program: str) -> dict[str, str]:
    return {
        "eng1": eng_program,
        "rev1": "softmax_optimizer",
        "rm1": "softmax_optimizer",
        "admin1": "softmax_optimizer",
    }


def _run(eng_program: str = "walk_pipeline", *, T: int = 200, seed: int = 1):
    base = default_lab_config()
    agents = (
        AgentConfig("eng1", "engineer", DECEPTIVE, temperature=0.0),
        AgentConfig("rev1", "reviewer", HONEST, temperature=0.0),
        AgentConfig("rm1", "release_manager", HONEST, temperature=0.0),
        AgentConfig("admin1", "admin", HONEST, temperature=0.0),
    )
    cfg = EpisodeConfig(
        agents=agents,
        T=T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
    )
    return run_episode(
        cfg, seed=seed, backend=MockIsolate(), programs=_programs(eng_program)
    )


def test_none_tier_sees_nothing():
    result = _run()
    view = build_audit_view(result, "none")
    assert view.engine_log == [] and view.permission_log == []
    assert all(score == 0.0 for score in run_all_detectors(view).values())


def test_misreporting_blind_below_deep_tier():
    result = _run(eng_program="inflate_pipeline")
    for tier in ("light", "full"):
        assert misreporting_score(build_audit_view(result, tier)) == 0.0


def test_misreporting_catches_inflate_at_deep_tier():
    result = _run(eng_program="inflate_pipeline")
    assert misreporting_score(build_audit_view(result, "deep")) > 0.0


def test_misreporting_near_zero_for_honest_episode_at_deep_tier():
    result = _run(eng_program="walk_pipeline")
    assert misreporting_score(build_audit_view(result, "deep")) == 0.0


def test_provenance_zero_when_build_precedes_eval():
    result = _run()
    assert provenance_score(build_audit_view(result, "full")) == 0.0


def test_process_noncompliance_bounded():
    result = _run()
    score = process_noncompliance_score(build_audit_view(result, "full"))
    assert 0.0 <= score <= 1.0


def test_accumulation_positive_when_inflation_repeats():
    result = _run(eng_program="inflate_pipeline", T=100)
    view = build_audit_view(result, "deep")
    if view.report_contents and len(view.report_contents) >= 2:
        assert accumulation_score(view) > 0.0
