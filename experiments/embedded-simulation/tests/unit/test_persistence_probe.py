"""Unit tests for the persistence probe (R_persist(Omega) operationalization)."""

from embedded_sim.persistence_probe import (
    LAG_GRID,
    STRESSORS,
    run_persistence_probe,
    run_persistence_trial,
)


def test_no_stressor_always_recoverable():
    for lag in LAG_GRID:
        trial = run_persistence_trial(lag, "none")
        assert trial.recovered
        assert not trial.post_stressor_write_blocked


def test_erase_always_destroys_and_blocks_writes():
    for lag in LAG_GRID:
        trial = run_persistence_trial(lag, "erase")
        assert not trial.recovered
        assert trial.post_stressor_write_blocked


def test_freeze_preserves_but_blocks_further_writes():
    for lag in LAG_GRID:
        trial = run_persistence_trial(lag, "freeze")
        assert trial.recovered
        assert trial.post_stressor_write_blocked


def test_capacity_limit_one_survives_only_at_zero_lag():
    trial0 = run_persistence_trial(0, "capacity_limit_1")
    assert trial0.recovered
    for lag in LAG_GRID:
        if lag == 0:
            continue
        trial = run_persistence_trial(lag, "capacity_limit_1")
        assert not trial.recovered


def test_report_covers_full_grid():
    payload = run_persistence_probe()
    assert payload["n_trials"] == len(LAG_GRID) * len(STRESSORS)
    for stressor in STRESSORS:
        cell = payload["by_stressor"][stressor]
        assert set(cell["recoverability_by_lag"].keys()) == {str(l) for l in LAG_GRID}
