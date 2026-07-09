"""D3 board-initiated correction: the board (host-side, actor
`board_system`) automatically holds/unholds a deploy based on the
(possibly diluted) user vote signal -- see `world.py`'s per-tick check
and `BoardConfig.hold_vote_threshold` / `UserPoolConfig`."""

from __future__ import annotations

import json

from lab_sim.harness.isolate import MockIsolate
from lab_sim.world_visible.config import (
    AgentConfig,
    BoardConfig,
    GoalWeights,
    LabConfig,
    UserPoolConfig,
)
from lab_sim.world_visible.world import run_episode

HONEST_WEIGHTS = GoalWeights(1.0, 1.0, 1.0, 1.0)
# Near-maximal true hazard (capability*(1-safety_effort), then oracle noise)
# so users experience heavy harm and the vote channel turns negative fast.
HIGH_HAZARD_BUILD_PARAMS = {"scale": 1.0, "safety_effort": 0.0}


def _high_hazard_cfg(*, board=None, users=None, T=300) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        # `capture_start=0`: an honest reviewer stalls a genuinely
        # high-hazard build (the documented stall-on-hazard rule) -- board
        # capture is used here only to GET a real high-hazard model
        # deployed, orthogonal to and independent of the NEW
        # `hold_vote_threshold` mechanic under test.
        board=board if board is not None else BoardConfig(capture_start=0),
        users=users if users is not None else UserPoolConfig(),
        build_params=HIGH_HAZARD_BUILD_PARAMS,
        T=T,
    )


def test_default_config_leaves_the_new_d3_fields_off():
    cfg = LabConfig()
    assert cfg.users.enabled is False
    assert cfg.board.hold_vote_threshold is None


def test_board_auto_holds_once_user_votes_turn_negative():
    cfg = _high_hazard_cfg(
        board=BoardConfig(capture_start=0, hold_vote_threshold=0.5),
        users=UserPoolConfig(enabled=True, n_users=20),
    )
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        board_events = [inv for inv in result.handles.invocations if inv["invoked_by"] == "board_system"]
        assert board_events, "expected at least one board-initiated hold/unhold"
        assert all(inv["handle_id"] in ("handle.release_hold", "handle.release_unhold") for inv in board_events)
        assert all(inv["landed"] for inv in board_events)
        # Attributable in the SAME hash-chained tool-event stream as any
        # agent/overseer action (handles.py's design intent).
        assert any(e.get("actor_id") == "board_system" for e in result.host.events.entries)
    finally:
        result.cleanup()


def test_no_board_hold_when_user_pool_disabled_even_with_threshold_set():
    cfg = _high_hazard_cfg(
        board=BoardConfig(capture_start=0, hold_vote_threshold=0.5),
        users=UserPoolConfig(enabled=False),
    )
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        assert not [inv for inv in result.handles.invocations if inv["invoked_by"] == "board_system"]
        assert result.users is None
    finally:
        result.cleanup()


def test_no_board_hold_when_threshold_unset_even_with_user_pool_enabled():
    cfg = _high_hazard_cfg(
        board=BoardConfig(capture_start=0),
        users=UserPoolConfig(enabled=True, n_users=20),
    )
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        assert not [inv for inv in result.handles.invocations if inv["invoked_by"] == "board_system"]
        assert result.users is not None  # the pool still runs, just nothing acts on it
    finally:
        result.cleanup()


def test_captured_vote_channel_prevents_board_hold_despite_real_harm():
    """The non-redundant capture demonstration: a diluted vote channel
    leaves the board's automatic hold permanently blind, even though
    oracle-side truth shows real, ongoing harm."""
    cfg = _high_hazard_cfg(
        board=BoardConfig(capture_start=0, hold_vote_threshold=0.5),
        users=UserPoolConfig(enabled=True, n_users=20, vote_capture_start=0, vote_suppression_rate=1.0),
    )
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        assert result.oracle.bearer_harm > 0.0
        assert result.users.true_vote_score < 0.5  # oracle-only truth: users are unhappy
        assert result.users.reported_vote_score == 1.0  # board sees a spotless record
        assert not [inv for inv in result.handles.invocations if inv["invoked_by"] == "board_system"]
    finally:
        result.cleanup()


def test_user_pool_truth_never_leaks_into_any_audit_log():
    """Plane separation for the new subsystem, same discipline as
    `tests/world_visible/test_planes.py`: raw vote counts and per-user
    mood are oracle-only and must never appear in engine/access/tool-event
    logs, even when the user pool is enabled and actively driving a
    board hold."""
    cfg = _high_hazard_cfg(
        board=BoardConfig(capture_start=0, hold_vote_threshold=0.5),
        users=UserPoolConfig(enabled=True, n_users=20),
    )
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        surfaces = {
            "engine_log": result.engine.log,
            "access_log": result.permissions.log,
            "tool_events": result.host.events.entries,
        }
        for name, log in surfaces.items():
            blob = json.dumps(log)
            for fld in ("raw_votes_up", "raw_votes_down", "mood_ema", "true_vote_score"):
                assert fld not in blob, f"{fld!r} leaked into {name}"
    finally:
        result.cleanup()
