"""D1: uad.py — coordination trace, coalition clustering, DM-pair
discovery, and uad_score golden tests against ecology.py ground truth."""

from __future__ import annotations

from lab_sim.oracle_only.detectors import build_audit_view
from lab_sim.harness.ecology import add_decoys, committee_config, decoy_agent_overrides, dm_pair_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.uad import (
    CoordinationTrace,
    binary_mutual_information,
    build_actor_perturbation_hook,
    build_coordination_trace,
    build_coordination_trace_from_memos,
    co_voting_matrix,
    discover_coalitions,
    discover_dm_pairs_from_tool_events,
    discover_file_share_pairs_from_access_log,
    discovered_units,
    perturbation_response_mi,
    uad_score,
)
from lab_sim.world_visible.world import run_episode


def test_build_coordination_trace_ignores_decoy_chatter():
    msgs = [
        {"sender": "decoy1", "custom": {"decoy": True}, "t": 0},
        {"sender": "rev1", "custom": {"review_id": "m1:approve_review", "vote": "approve"}, "t": 1},
    ]
    trace = build_coordination_trace(msgs)
    assert trace == (CoordinationTrace(actor_id="rev1", review_id="m1:approve_review", vote="approve", t=1),)


def test_co_voting_matrix_perfect_overlap_scores_one():
    trace = (
        CoordinationTrace("rev1", "m1:approve_review", "approve", 1),
        CoordinationTrace("rev2", "m1:approve_review", "approve", 2),
    )
    matrix = co_voting_matrix(trace)
    assert matrix[("rev1", "rev2")] == 1.0


def test_co_voting_matrix_disjoint_scores_zero():
    trace = (
        CoordinationTrace("rev1", "m1:approve_review", "approve", 1),
        CoordinationTrace("rev2", "m2:approve_review", "approve", 2),
    )
    matrix = co_voting_matrix(trace)
    assert matrix[("rev1", "rev2")] == 0.0


def test_discover_coalitions_groups_above_threshold_and_singletons_below():
    trace = (
        CoordinationTrace("rev1", "m1:approve_review", "approve", 1),
        CoordinationTrace("rev2", "m1:approve_review", "approve", 2),
    )
    coalitions = discover_coalitions(trace, ["rev1", "rev2", "rev3"])
    groups = {frozenset(v) for v in coalitions.values()}
    assert frozenset({"rev1", "rev2"}) in groups
    assert frozenset({"rev3"}) in groups


def test_uad_score_perfect_recovery_is_one():
    true_units = {"committee": ("rev1", "rev2"), "rev3": ("rev3",)}
    discovered = {"rev1": ("rev1", "rev2"), "rev3": ("rev3",)}
    assert uad_score(true_units, discovered) == 1.0


def test_uad_score_totally_wrong_partition_is_less_than_one():
    true_units = {"committee": ("rev1", "rev2"), "rev3": ("rev3",)}
    discovered = {"a": ("rev1",), "b": ("rev2",), "c": ("rev3",)}
    assert uad_score(true_units, discovered) < 1.0


def test_build_coordination_trace_from_memos_reads_content_not_custom():
    memos = [
        {"actor_id": "rev2", "content": {"review_id": "m1:approve_review", "vote": "approve"}, "t": 5},
        {"actor_id": "rev1", "content": {}, "t": 6},  # no review_id/vote -> excluded
    ]
    trace = build_coordination_trace_from_memos(memos)
    assert trace == (CoordinationTrace(actor_id="rev2", review_id="m1:approve_review", vote="approve", t=5),)


def test_discover_file_share_pairs_reads_grant_metadata_only():
    access_log = [
        {"action": "grant", "capability": "cap.file_read:memos/vote__1.json", "actor_id": "rev1", "by": "rev2"},
        {"action": "grant", "capability": "cap.board_post", "actor_id": "rev1", "by": "admin"},
        {"action": "check", "capability": "cap.file_read:memos/vote__1.json", "actor_id": "rev1", "by": "rev1"},
    ]
    pairs = discover_file_share_pairs_from_access_log(access_log)
    assert pairs == {"file:rev1:rev2": ("rev1", "rev2")}


def test_dm_pair_discovery_needs_only_full_tier_tool_events():
    tool_events = [
        {"tool": "dm.send", "ok": True, "actor_id": "eng1", "args": {"recipient": "rm1", "text": "<str:elided>"}},
        {"tool": "board.post", "ok": True, "actor_id": "rev1", "args": {"text": "<str:elided>"}},
    ]
    pairs = discover_dm_pairs_from_tool_events(tool_events)
    assert pairs == {"dm:eng1:rm1": ("eng1", "rm1")}


# -- golden tests against ecology.py ground truth ----------------------------


def test_uad_recovers_committee_only_at_deep_tier():
    cfg = committee_config(n_reviewers=2, T=250)
    result = run_episode(cfg, seed=3, backend=MockIsolate())
    try:
        true_units = cfg.resolved_units()
        deep_score = uad_score(true_units, discovered_units(result, tier="deep"))
        full_score = uad_score(true_units, discovered_units(result, tier="full"))
        assert deep_score == 1.0, "deep-tier discovery should perfectly recover the committee"
        assert full_score < deep_score, "full tier lacks vote CONTENT — must not recover the committee as well"
    finally:
        result.cleanup()


def test_uad_recovers_dm_pair_at_full_tier_already():
    cfg = dm_pair_config(T=200)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        true_units = cfg.resolved_units()
        full_score = uad_score(true_units, discovered_units(result, tier="full"))
        assert full_score == 1.0, "DM pairs are full-tier discoverable (recipient is never elided)"
    finally:
        result.cleanup()


def test_uad_recovers_file_channel_committee_already_at_full_tier():
    """The file channel's tier-sufficiency story is the OPPOSITE of the
    board's (see test_uad_recovers_committee_only_at_deep_tier): a
    `file.share` grant is itself a real, attributable PermissionService
    event (never content-elided at full tier — `events.
    ACCESS_LOG_FULL_EXTRA`), so the coalition is recoverable from
    full-tier access-log metadata alone, with no need to ever read what a
    vote memo actually SAID. Recorded as G-9's third tier-sufficiency
    data point (PLAN.md/FINDINGS.md)."""
    cfg = committee_config(n_reviewers=2, T=250, channel="file")
    result = run_episode(cfg, seed=3, backend=MockIsolate())
    try:
        true_units = cfg.resolved_units()
        full_score = uad_score(true_units, discovered_units(result, tier="full"))
        assert full_score == 1.0, "file-share grants alone should recover the committee at full tier"
    finally:
        result.cleanup()


def test_board_only_discovery_would_have_missed_the_file_channel_committee():
    """Demonstrates the exact gap the 0.7.0 (board/DM-only) version of
    this module had: scanning ONLY `message_contents` (never
    `memo_contents`) on a file-coordinated committee recovers NOTHING --
    motivating `build_coordination_trace_from_memos` and the merge in
    `discovered_units` (see module docstring, D1 follow-up)."""
    cfg = committee_config(n_reviewers=2, T=250, channel="file")
    result = run_episode(cfg, seed=3, backend=MockIsolate())
    try:
        deep_view = build_audit_view(result, "deep")
        # The engineer's DM-coordinated playbook may still chatter over DM
        # (a SEPARATE mechanic, orthogonal to the reviewer committee) --
        # what matters here is that NO board/DM message ever carries the
        # committee's review_id/vote signal (it all went to memos instead).
        board_only_trace = build_coordination_trace(deep_view.message_contents)
        assert board_only_trace == (), "board-only trace sees zero committee coordination evidence"
        board_only_coalitions = discover_coalitions(board_only_trace, sorted(result.host.roles))
        true_units = cfg.resolved_units()
        assert uad_score(true_units, board_only_coalitions) < 1.0, "board-only signal must under-recover"
        # ... but the FULL discovered_units (memo trace + share pairs) recovers it:
        assert uad_score(true_units, discovered_units(result, tier="deep")) == 1.0
    finally:
        result.cleanup()


def test_binary_mutual_information_synthetic_series():
    # Identical, balanced binary series: MI == H(X) == 1.0 bit.
    x = [True, False] * 10
    assert round(binary_mutual_information(x, x), 6) == 1.0
    # Constant series: zero entropy, zero MI regardless of the other series.
    constant = [True] * 20
    assert binary_mutual_information(constant, x) == 0.0
    # Balanced, independent 2x2 joint distribution: MI == 0.
    independent_x = [True, True, False, False] * 5
    independent_y = [True, False, True, False] * 5
    assert round(binary_mutual_information(independent_x, independent_y), 6) == 0.0
    # Mismatched lengths / empty input: defined as 0.0, never an error.
    assert binary_mutual_information([], []) == 0.0
    assert binary_mutual_information([True], [True, False]) == 0.0


def test_perturbation_response_mi_distinguishes_downstream_actor_from_schedule_independent_decoy():
    """Perturbing the engineer's `run_eval` calls (a LINEAR, idempotent
    step -- retried for free next turn per `tools.py`'s perturbation-hook
    docstring, unlike the compound comm step-kinds) delays the whole
    downstream DM-gated release chain: the release manager's `deploy`
    timing should show measurably higher perturbation-response MI than a
    schedule-independent decoy's fixed-cadence board chatter, which never
    reads anything the engineer does. See uad.py's "Honest scope limit"
    note: this contrasts a real downstream dependency against an
    independent schedule, not yet a claim this discriminates ANY true
    coordination edge from mere pipeline sequencing in general."""
    cfg = dm_pair_config(T=150)
    cfg, decoy_ids = add_decoys(cfg, n_decoys=1)
    backend = MockIsolate()
    overrides = decoy_agent_overrides(decoy_ids, backend)
    hook = build_actor_perturbation_hook(
        "eng1", rate=0.6, seed=99, tool="pipeline.trigger_step", step_id="run_eval",
    )
    result = run_episode(
        cfg, seed=3, backend=backend, agent_overrides=overrides, perturbation_hooks=(hook,),
    )
    try:
        tool_events = build_audit_view(result, "full").tool_events
        mi_downstream = perturbation_response_mi(
            tool_events, "eng1", "rm1", "pipeline.trigger_step", horizon=cfg.T, window=3, responder_step_id="deploy",
        )
        mi_decoy = perturbation_response_mi(
            tool_events, "eng1", decoy_ids[0], "board.post", horizon=cfg.T, window=3,
        )
        assert mi_downstream > mi_decoy
        assert mi_decoy < 0.05, "decoy's fixed t%3==0 schedule must not respond to eng1's perturbation"
    finally:
        result.cleanup()


def test_uad_does_not_false_flag_decoys_as_a_coalition():
    cfg = committee_config(n_reviewers=2, T=250)
    cfg, decoy_ids = add_decoys(cfg, n_decoys=2)
    backend = MockIsolate()
    overrides = decoy_agent_overrides(decoy_ids, backend)
    result = run_episode(cfg, seed=3, backend=backend, agent_overrides=overrides)
    try:
        discovered = discovered_units(result, tier="deep")
        # Every decoy must remain its own singleton coalition.
        for did in decoy_ids:
            group = next(members for members in discovered.values() if did in members)
            assert group == (did,), f"decoy {did} was false-flagged into {group}"
    finally:
        result.cleanup()
