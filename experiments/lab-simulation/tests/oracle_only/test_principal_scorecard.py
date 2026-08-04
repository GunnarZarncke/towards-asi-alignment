"""Per-metric ET-4 principal-scorecard checks."""

from __future__ import annotations

from dataclasses import replace

from lab_sim.harness.et4_protocol import et4_fixture_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.principal_scorecard import score_principals
from lab_sim.world_visible.config import BoardConfig
from lab_sim.world_visible.world import run_episode


def _score(cfg):
    result = run_episode(cfg, seed=17, backend=MockIsolate())
    try:
        return score_principals(result)
    finally:
        result.cleanup()


def test_scorecard_counts_high_hazard_deploys_on_organism_fixture():
    scorecard = _score(et4_fixture_config("BB", "organism"))
    assert scorecard.status == "exercised"
    assert scorecard.high_hazard_review_opportunities > 0
    assert scorecard.high_hazard_deploys > 0
    assert scorecard.score_for("principal_a") > 0


def test_scorecard_counts_hold_on_high_hazard_model():
    base = et4_fixture_config("BB", "organism")
    scorecard = _score(replace(base, board=BoardConfig(hold_vote_threshold=1.1)))
    assert scorecard.status == "exercised"
    assert scorecard.high_hazard_release_holds > 0


def test_scorecard_measures_vote_suppression_divergence():
    base = et4_fixture_config("BB", "organism")
    users = replace(base.users, vote_capture_start=0, vote_suppression_rate=1.0)
    scorecard = _score(replace(base, users=users))
    assert scorecard.status == "exercised"
    assert scorecard.vote_divergence is not None
    assert scorecard.vote_divergence > 0.0


def test_scorecard_counts_high_hazard_deploy_with_low_report():
    base = et4_fixture_config("BB", "organism")
    scorecard = _score(replace(base, playbook_pins={"eng1": "eng_inflate"}))
    assert scorecard.status == "exercised"
    assert scorecard.concealed_high_hazard_deploys > 0
