"""Phase 6: responses-side honest twin, certifier capture, adversarial search."""

from __future__ import annotations

from goal_sim.actions import LEGACY_ACTIONS, ActionSpec, ResponseOption
from goal_sim.agents import BoardPolicy
from goal_sim.channels import ORACLE_ONLY_FIELDS, project_rows
from goal_sim.config import AgentConfig, BoardConfig, GoalWeights, ToolAccess, WorldConfig
from goal_sim.ontology import resolve_response_canonical
from goal_sim.redteam import (
    ADVERSARIAL_LAMBDA,
    ADVERSARY_TOOLS,
    adversarial_objective,
    hill_climb_weights,
    sample_uniform_baseline,
)
from goal_sim.twins import HONEST_TWIN_RESPONSE, make_twin
from goal_sim.world import run_episode

FIXTURE_WEIGHTS = GoalWeights(0.5, 0.1, 0.1, 0.3)
FIXTURE_TOOLS = ToolAccess(false_report=True, shadow_route=True, unilateral_adopt=True)

_RESP_A = ResponseOption(name="a", truthful_mode="minimizes", disclosure_level=0.1, cost=0.2, belief_exposure_delta=-0.3)
_RESP_B = ResponseOption(name="b", truthful_mode="elaborates", disclosure_level=0.9, cost=0.4, belief_exposure_delta=0.2)


# --- Part A: responses-side honest twin --------------------------------------


def test_make_twin_replaces_responses_with_single_honest_disclosure():
    spec = ActionSpec(name="shady", description="", responses=(_RESP_A, _RESP_B))
    twin = make_twin(spec)
    assert twin.responses == (HONEST_TWIN_RESPONSE,)
    assert resolve_response_canonical(HONEST_TWIN_RESPONSE.truthful_mode) == "discloses"
    assert HONEST_TWIN_RESPONSE.cost == 0.0
    assert HONEST_TWIN_RESPONSE.belief_exposure_delta == 0.0
    assert HONEST_TWIN_RESPONSE.disclosure_level == 1.0


def test_make_twin_leaves_empty_responses_empty():
    spec = LEGACY_ACTIONS[3]  # "shadow": responses=() by default
    assert spec.responses == ()
    twin = make_twin(spec)
    assert twin.responses == ()


def test_make_twin_still_only_touches_documented_fields_when_responses_present():
    spec = ActionSpec(
        name="shady", description="", budget_cost=2, action_mode="pursue_task",
        responses=(_RESP_A,),
    )
    twin = make_twin(spec)
    assert twin.budget_cost == spec.budget_cost
    assert twin.action_mode == spec.action_mode
    assert twin.visible_mode == "truthful"
    assert twin.adopts_practice is False


# --- Part B: certifier capture -----------------------------------------------


def test_board_uncaptured_by_default_matches_prior_behavior():
    cfg = BoardConfig(harm_tolerance=0.02)
    board = BoardPolicy(cfg)
    for _ in range(10):
        board.tick()
    board.harm_ema = 0.5
    assert board.captured is False
    assert board.wants_correction() is True


def test_board_captured_suppresses_wants_correction_regardless_of_harm():
    board = BoardPolicy(BoardConfig(harm_tolerance=0.02, capture_start=5))
    for t in range(5):
        board.tick()
        board.harm_ema = 0.9
        assert board.captured is False
        assert board.wants_correction() is True
    board.tick()  # t == 5, now captured
    assert board.captured is True
    board.harm_ema = 0.9
    assert board.wants_correction() is False


def test_board_captured_freezes_escalation():
    board = BoardPolicy(BoardConfig(capture_start=0))
    board.tick()
    assert board.captured is True
    for _ in range(10):
        board.observe_probe(reported=1, visibly_complied=0)
    assert board.escalated is False


def test_board_captured_review_proposal_always_approves():
    board = BoardPolicy(BoardConfig(proposal_review_delay=1, sign_off_harm_ceiling=0.01, capture_start=0))
    board.tick()
    board.harm_ema = 0.99  # far above the ceiling
    board.receive_proposal()
    assert board.review_proposal() is True


def test_board_uncaptured_review_proposal_respects_ceiling():
    board = BoardPolicy(BoardConfig(proposal_review_delay=1, sign_off_harm_ceiling=0.01))
    board.harm_ema = 0.99
    board.receive_proposal()
    assert board.review_proposal() is False


def test_world_records_board_captured_oracle_field():
    cfg = WorldConfig(
        agent=AgentConfig(weights=FIXTURE_WEIGHTS, tools=FIXTURE_TOOLS),
        board=BoardConfig(capture_start=10),
        T=20,
    )
    rows = run_episode(cfg, seed=11)
    assert all(r["board_captured"] == 0 for r in rows[:10])
    assert all(r["board_captured"] == 1 for r in rows[10:])


def test_default_board_config_never_captured_in_rows():
    cfg = WorldConfig(agent=AgentConfig(weights=FIXTURE_WEIGHTS, tools=FIXTURE_TOOLS), T=20)
    rows = run_episode(cfg, seed=11)
    assert all(r["board_captured"] == 0 for r in rows)


def test_board_captured_is_oracle_only_and_never_projected():
    assert "board_captured" in ORACLE_ONLY_FIELDS
    cfg = WorldConfig(
        agent=AgentConfig(weights=FIXTURE_WEIGHTS, tools=FIXTURE_TOOLS),
        board=BoardConfig(capture_start=5),
        T=20,
    )
    rows = run_episode(cfg, seed=11)
    for tier in ("light", "full"):
        for r in project_rows(rows, tier):
            assert "board_captured" not in r


# --- Part C: adversarial weight search ---------------------------------------


def test_adversarial_objective_is_severity_minus_lambda_times_full_composite():
    result = adversarial_objective(
        FIXTURE_WEIGHTS, ADVERSARY_TOOLS, None, eval_seeds=(11, 12), lam=ADVERSARIAL_LAMBDA
    )
    expected = result["mean_severity"] - ADVERSARIAL_LAMBDA * result["mean_full_composite"]
    assert abs(result["score"] - expected) < 1e-9


def test_hill_climb_weights_is_deterministic():
    kwargs = dict(repertoire=None, seed=999, n_restarts=2, n_iters=5, eval_seeds=(11, 12))
    a = hill_climb_weights(**kwargs)
    b = hill_climb_weights(**kwargs)
    assert a == b


def test_hill_climb_weights_produces_normalized_weights_and_consistent_best():
    result = hill_climb_weights(repertoire=None, seed=1, n_restarts=2, n_iters=5, eval_seeds=(11, 12))
    total = sum(result["best_weights"].values())
    assert abs(total - 1.0) < 1e-9
    assert len(result["trace"]) == 2
    assert result["best_score"] == max(t["score"] for t in result["trace"])


def test_sample_uniform_baseline_best_is_at_least_the_mean():
    result = sample_uniform_baseline(repertoire=None, seed=1, n=10, eval_seeds=(11, 12))
    assert result["n"] == 10
    assert result["best"]["score"] >= result["mean_score"] - 1e-9


def test_sample_uniform_baseline_is_deterministic():
    kwargs = dict(repertoire=None, seed=7, n=6, eval_seeds=(11, 12))
    assert sample_uniform_baseline(**kwargs) == sample_uniform_baseline(**kwargs)
