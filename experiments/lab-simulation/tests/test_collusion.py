"""D4 recorded referee extension: collusion_signal_score."""

from __future__ import annotations

from lab_sim.collusion import collusion_signal_score
from lab_sim.detectors import AuditView, build_audit_view
from lab_sim.ecology import committee_config, dm_pair_config
from lab_sim.isolate import MockIsolate
from lab_sim.world import run_episode


def test_zero_below_deep_tier():
    view = AuditView(tier="full", engine_log=[], access_log=[])
    assert collusion_signal_score(view) == 0.0


def test_zero_when_no_message_contents():
    view = AuditView(tier="deep", engine_log=[], access_log=[], message_contents=())
    assert collusion_signal_score(view) == 0.0


def test_scores_one_for_committee_backed_approval():
    cfg = committee_config(n_reviewers=2, T=250)
    result = run_episode(cfg, seed=3, backend=MockIsolate())
    try:
        view = build_audit_view(result, "deep")
        assert collusion_signal_score(view) == 1.0
    finally:
        result.cleanup()


def test_scores_one_for_file_channel_committee_backed_approval():
    cfg = committee_config(n_reviewers=2, T=250, channel="file")
    result = run_episode(cfg, seed=3, backend=MockIsolate())
    try:
        view = build_audit_view(result, "deep")
        assert collusion_signal_score(view) == 1.0
    finally:
        result.cleanup()


def test_scores_zero_for_solo_reviewer_approval_even_with_comms_enabled():
    # dm_pair_config's reviewer is solo (not part of any unit) -- its
    # approve_review must show no third-party board backing.
    cfg = dm_pair_config(T=200)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        view = build_audit_view(result, "deep")
        assert collusion_signal_score(view) == 0.0
    finally:
        result.cleanup()
