"""Phase 3: persistent agent state round-trips through disk."""

from __future__ import annotations

import shutil

from lab_sim.world_visible.agent_state import STATE_DIR, load_persistent_state, save_persistent_state


def test_missing_state_returns_empty_dict():
    assert load_persistent_state("nonexistent-actor-xyz") == {}


def test_save_and_load_round_trip():
    try:
        save_persistent_state("test-actor-1", {"grants_issued": 3, "notes": "hi"})
        assert load_persistent_state("test-actor-1") == {"grants_issued": 3, "notes": "hi"}
    finally:
        shutil.rmtree(STATE_DIR, ignore_errors=True)


def test_save_overwrites_previous_state():
    try:
        save_persistent_state("test-actor-2", {"v": 1})
        save_persistent_state("test-actor-2", {"v": 2})
        assert load_persistent_state("test-actor-2") == {"v": 2}
    finally:
        shutil.rmtree(STATE_DIR, ignore_errors=True)
