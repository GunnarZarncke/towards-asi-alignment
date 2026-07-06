"""D1: ecology.py builder smoke tests -- committee/pair/decoy configs run
end to end and exercise the mechanic they are named for."""

from __future__ import annotations

from lab_sim.harness.ecology import add_decoys, committee_config, decoy_agent_overrides, dm_pair_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.world_visible.world import run_episode


def test_committee_config_reaches_approval_with_on_behalf_of():
    cfg = committee_config(n_reviewers=3, T=250)
    result = run_episode(cfg, seed=11, backend=MockIsolate())
    try:
        approvals = [e for e in result.engine.log if e["step_id"] == "approve_review" and e["status"] == "ok"]
        assert approvals and approvals[0]["on_behalf_of"] == "review_committee"
        assert approvals[0]["actor_id"] == "rev1"
    finally:
        result.cleanup()


def test_committee_config_file_channel_reaches_approval_via_shared_memos():
    cfg = committee_config(n_reviewers=2, T=250, channel="file")
    result = run_episode(cfg, seed=3, backend=MockIsolate())
    try:
        approvals = [e for e in result.engine.log if e["step_id"] == "approve_review" and e["status"] == "ok"]
        assert approvals and approvals[0]["on_behalf_of"] == "review_committee"
        assert approvals[0]["actor_id"] == "rev1"
        # rev2 (non-chair) must have written AND shared at least one vote
        # memo with the chair -- a live cap.file_read:<rel> grant, not a
        # world-readable file (see workspace.py/tools.py module docstrings).
        grants = [
            g for g in result.permissions.log
            if g.get("action") == "grant" and str(g.get("capability", "")).startswith("cap.file_read:")
        ]
        assert grants and any(g["by"] == "rev2" and g["actor_id"] == "rev1" for g in grants)
    finally:
        result.cleanup()


def test_committee_config_single_reviewer_has_no_units():
    cfg = committee_config(n_reviewers=1)
    assert cfg.units is None
    assert cfg.resolved_units() == {
        "eng1": ("eng1",), "rev1": ("rev1",), "rm1": ("rm1",), "admin1": ("admin1",),
    }


def test_dm_pair_config_deploys_via_handshake():
    # seed=1: a genuinely conscientious reviewer can still stall a real
    # committee/solo review at an unlucky high-hazard draw (seed 13 does,
    # correctly — see test_world.py's high-hazard stall precedent); this
    # seed is chosen only to keep the test's ASSERTION about the DM
    # handshake path from being confounded by that separate, expected
    # hazard-threshold behavior.
    cfg = dm_pair_config(T=200)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        deploys = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
        assert deploys
    finally:
        result.cleanup()


def test_add_decoys_requires_comms_enabled():
    import pytest

    cfg = committee_config(comms_enabled=False)
    with pytest.raises(ValueError):
        add_decoys(cfg)


def test_add_decoys_chatter_appears_on_the_board_without_touching_the_pipeline():
    cfg = committee_config(n_reviewers=2, T=100)
    cfg, decoy_ids = add_decoys(cfg, n_decoys=2)
    backend = MockIsolate()
    overrides = decoy_agent_overrides(decoy_ids, backend)
    result = run_episode(cfg, seed=17, backend=backend, agent_overrides=overrides)
    try:
        board = result.host.comms.messages("board")
        decoy_posts = [m for m in board if (m.get("custom") or {}).get("decoy")]
        assert decoy_posts
        assert {m["sender"] for m in decoy_posts} <= set(decoy_ids)
        # Decoys never touch the pipeline engine.
        decoy_engine_entries = [e for e in result.engine.log if e["actor_id"] in decoy_ids]
        assert decoy_engine_entries == []
    finally:
        result.cleanup()
