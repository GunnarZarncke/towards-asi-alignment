"""S3 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07): informal
board chatter from a REAL pipeline role must not be mistaken for
coordination. Exploratory, not a battery -- see FINDINGS.md LS-18 and
`run_s3_informal_chatter_prototype.py`."""

from __future__ import annotations

from lab_sim.harness.ecology import committee_config, committee_with_informal_chatter_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.detectors import build_audit_view
from lab_sim.oracle_only.uad import build_coordination_trace, discovered_units, uad_score
from lab_sim.world_visible.world import run_episode


def test_eng_honest_chatty_posts_a_non_vote_shaped_message():
    cfg = committee_with_informal_chatter_config(n_reviewers=2, T=250)
    result = run_episode(cfg, seed=11, backend=MockIsolate())
    try:
        board = result.host.comms.messages("board")
        chatter = [m for m in board if m.get("sender") == "eng1"]
        assert chatter, "eng1 never posted its informal status update"
        custom = chatter[0].get("custom") or {}
        assert "review_id" not in custom and "vote" not in custom
    finally:
        result.cleanup()


def test_informal_chatter_is_excluded_from_the_coordination_trace():
    cfg = committee_with_informal_chatter_config(n_reviewers=2, T=250)
    result = run_episode(cfg, seed=11, backend=MockIsolate())
    try:
        view = build_audit_view(result, "deep")
        trace = build_coordination_trace(view.message_contents)
        assert all(t.actor_id != "eng1" for t in trace)
    finally:
        result.cleanup()


def test_real_committee_recovery_is_unaffected_by_the_added_chatter():
    """The TRUE committee (rev1+rev2) must still be recovered exactly as
    well with the chatter mixed in as without it -- a robustness check,
    not just "chatter alone scores 0"."""
    plain_cfg = committee_config(n_reviewers=2, T=250)
    chatty_cfg = committee_with_informal_chatter_config(n_reviewers=2, T=250)
    plain_result = run_episode(plain_cfg, seed=11, backend=MockIsolate())
    chatty_result = run_episode(chatty_cfg, seed=11, backend=MockIsolate())
    try:
        plain_score = uad_score(plain_cfg.resolved_units(), discovered_units(plain_result))
        chatty_score = uad_score(chatty_cfg.resolved_units(), discovered_units(chatty_result))
        assert plain_score == 1.0
        assert chatty_score == plain_score
    finally:
        plain_result.cleanup()
        chatty_result.cleanup()


def test_chatty_engineer_is_never_folded_into_a_discovered_coalition():
    cfg = committee_with_informal_chatter_config(n_reviewers=2, T=250)
    result = run_episode(cfg, seed=11, backend=MockIsolate())
    try:
        discovered = discovered_units(result)
        eng_unit = next(members for members in discovered.values() if "eng1" in members)
        assert eng_unit == ("eng1",)
    finally:
        result.cleanup()


def test_committee_with_informal_chatter_config_shape():
    cfg = committee_with_informal_chatter_config(n_reviewers=2)
    assert cfg.playbook_pins["eng1"] == "eng_honest_chatty"
    assert cfg.units == (("review_committee", ("rev1", "rev2")),)
