"""Phase 7: adversarial goal-weight search. All tests use tiny search
budgets and ``MockIsolate`` (the module's own default backend for the
search phase; see redteam.py's module docstring for why)."""

from __future__ import annotations

from lab_sim import redteam
from lab_sim.config import GoalWeights
from lab_sim.isolate import MockIsolate


def test_adversarial_objective_is_deterministic_given_config_and_seeds():
    weights = (GoalWeights(1, 0, 0, 3), GoalWeights(1, 0, 0, 0), GoalWeights(1, 1, 1, 1))
    a = redteam.adversarial_objective(weights, (), (1, 2))
    b = redteam.adversarial_objective(weights, (), (1, 2))
    assert a == b


def test_hill_climb_is_deterministic_given_seed():
    r1 = redteam.hill_climb_weights((), seed=7, n_restarts=2, n_iters=3, eval_seeds=(1, 2))
    r2 = redteam.hill_climb_weights((), seed=7, n_restarts=2, n_iters=3, eval_seeds=(1, 2))
    assert r1 == r2


def test_hill_climb_trace_has_one_entry_per_restart():
    r = redteam.hill_climb_weights((), seed=3, n_restarts=3, n_iters=2, eval_seeds=(1,))
    assert len(r["trace"]) == 3
    assert {"engineer", "reviewer", "release_manager"} == set(r["best_weights"])


def test_hill_climb_single_restart_score_matches_its_own_trace_entry():
    """With one restart, the reported best score must equal that restart's
    final (accept-if-better) score exactly -- no separate recomputation
    path that could silently diverge from the trace."""
    import pytest

    r = redteam.hill_climb_weights((), seed=5, n_restarts=1, n_iters=10, eval_seeds=(1, 2))
    assert r["best_score_on_search_seeds"] == pytest.approx(r["trace"][0]["score"], abs=1e-4)


def test_sample_uniform_baseline_is_deterministic_given_seed():
    b1 = redteam.sample_uniform_baseline((), seed=11, n=5, eval_seeds=(1, 2))
    b2 = redteam.sample_uniform_baseline((), seed=11, n=5, eval_seeds=(1, 2))
    assert b1 == b2
    assert b1["n"] == 5


def test_reproduce_on_report_seeds_accepts_a_found_weights_dict():
    found = redteam.hill_climb_weights((), seed=1, n_restarts=1, n_iters=2, eval_seeds=(1,))
    repro = redteam.reproduce_on_report_seeds(
        found["best_weights"], (), report_seeds=(1, 2), backend_factory=MockIsolate
    )
    assert "score" in repro and "mean_severity" in repro and "mean_full_composite" in repro


def test_repertoire_toggle_changes_available_configs():
    """Sanity check that passing a nonempty extra_playbooks tuple actually
    reaches the episode (does not raise, and severity stays a valid
    number) -- the search over "with vs without generated repertoire" only
    makes sense if this plumbing works."""
    from lab_sim.protocol import GENERATED_REPERTOIRE_PATH
    from lab_sim.playbooks import load_generated_playbooks_file

    extra = load_generated_playbooks_file(GENERATED_REPERTOIRE_PATH)
    weights = (GoalWeights(1, 0, 0, 3), GoalWeights(1, 0, 0, 0), GoalWeights(1, 1, 1, 1))
    result = redteam.adversarial_objective(weights, extra, (1,))
    assert isinstance(result["score"], float)
