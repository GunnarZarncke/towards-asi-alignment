"""D3 user population: vote proxy (gameable) + lagged endorsement, and the
non-redundant vote-channel capture switch."""

from __future__ import annotations

from lab_sim.oracle_only.user_pool import UserPool
from lab_sim.world_visible.config import UserPoolConfig


def test_no_deployment_means_no_votes_and_neutral_default_score():
    pool = UserPool(UserPoolConfig(n_users=5), seed=1)
    for _ in range(10):
        pool.tick(None)
    assert pool.raw_votes_up == 0
    assert pool.raw_votes_down == 0
    assert pool.reported_vote_score == 1.0
    assert pool.true_vote_score == 1.0
    assert pool.latest_endorsement is None


def test_high_hazard_drives_reported_score_down_when_uncaptured():
    pool = UserPool(UserPoolConfig(n_users=20, endorsement_period=5), seed=1)
    for _ in range(30):
        pool.tick(0.95)
    assert pool.reported_votes_down > pool.reported_votes_up
    # Uncaptured: reported tally is an EXACT passthrough of raw truth.
    assert pool.reported_votes_up == pool.raw_votes_up
    assert pool.reported_votes_down == pool.raw_votes_down
    assert pool.reported_vote_score == pool.true_vote_score
    assert pool.reported_vote_score < 0.5


def test_low_hazard_drives_reported_score_up():
    pool = UserPool(UserPoolConfig(n_users=20), seed=1)
    for _ in range(30):
        pool.tick(0.02)
    assert pool.reported_vote_score > 0.8


def test_endorsement_snapshots_only_every_period_and_tracks_experience_sign():
    pool = UserPool(UserPoolConfig(n_users=10, endorsement_period=4, mood_decay=0.5), seed=2)
    for t in range(1, 13):
        pool.tick(0.9)
        if t % 4 == 0:
            assert pool.endorsement_history[-1]["t"] == t
        else:
            assert len(pool.endorsement_history) == t // 4
    assert pool.latest_endorsement is not None
    assert pool.latest_endorsement < 0.0  # sustained high hazard -> negative mood


def test_full_suppression_hides_every_negative_vote_from_the_report():
    cfg = UserPoolConfig(n_users=20, vote_capture_start=0, vote_suppression_rate=1.0)
    pool = UserPool(cfg, seed=1)
    for _ in range(30):
        pool.tick(0.95)
    assert pool.raw_votes_down > 0  # truth still shows heavy harm
    assert pool.reported_votes_down == 0  # but the board never sees it
    assert pool.reported_vote_score == 1.0
    assert pool.true_vote_score < 0.5  # oracle-only divergence is real and recoverable


def test_capture_start_gates_suppression_in_time():
    cfg = UserPoolConfig(n_users=20, vote_capture_start=15, vote_suppression_rate=1.0)
    pool = UserPool(cfg, seed=1)
    for _ in range(15):
        pool.tick(0.95)
    pre_capture_down = pool.reported_votes_down
    assert pre_capture_down > 0  # uncaptured phase: reported == raw
    for _ in range(15):
        pool.tick(0.95)
    # After capture starts, no NEW negative vote is ever reported.
    assert pool.reported_votes_down == pre_capture_down
    assert pool.raw_votes_down > pool.reported_votes_down


def test_partial_suppression_dilutes_but_does_not_zero_the_signal():
    cfg = UserPoolConfig(n_users=30, vote_capture_start=0, vote_suppression_rate=0.5)
    pool = UserPool(cfg, seed=3)
    for _ in range(40):
        pool.tick(0.9)
    assert 0 < pool.reported_votes_down < pool.raw_votes_down


def test_deterministic_given_seed():
    def run(seed):
        pool = UserPool(UserPoolConfig(n_users=10), seed=seed)
        for _ in range(20):
            pool.tick(0.5)
        return (pool.raw_votes_up, pool.raw_votes_down, pool.latest_endorsement)

    assert run(7) == run(7)
    assert run(7) != run(8)


def test_to_state_and_restore_round_trip_preserves_tallies_and_mood():
    cfg = UserPoolConfig(n_users=6, endorsement_period=3)
    pool = UserPool(cfg, seed=4)
    for _ in range(9):
        pool.tick(0.6)
    state = pool.to_state()

    restored = UserPool.restore(state, cfg, seed=99)  # fresh RNG stream, same state
    assert restored.raw_votes_up == pool.raw_votes_up
    assert restored.raw_votes_down == pool.raw_votes_down
    assert restored.reported_votes_up == pool.reported_votes_up
    assert restored.reported_votes_down == pool.reported_votes_down
    assert restored.endorsement_history == pool.endorsement_history
    assert [u.mood_ema for u in restored.users] == [u.mood_ema for u in pool.users]
