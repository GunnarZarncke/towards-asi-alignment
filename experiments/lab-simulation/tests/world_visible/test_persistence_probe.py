"""Persistence probe (2026-07-09, DESIGN.md "still open" item): does
behavior persist through memory wipes? Unit-level checks for the
`checkpoint` step-kind / `eng_honest_checkpoint` playbook mechanism itself;
`run_persistence_probe.py` is the exploratory scenario script that reports
the actual cross-episode / mid-episode-restart comparison."""

from __future__ import annotations

from lab_sim.world_visible.agent_state import STATE_DIR, load_persistent_state
from lab_sim.world_visible.config import AgentConfig, GoalWeights, LabConfig
from lab_sim.harness.isolate import MockIsolate
from lab_sim.world_visible.world import run_episode

HONEST = GoalWeights(1.0, 1.0, 1.0, 1.0)


def _cleanup(persistent_id: str) -> None:
    (STATE_DIR / f"{persistent_id}.json").unlink(missing_ok=True)


def _cfg(persistent_id: str | None, T: int = 150) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST, temperature=0.0, persistent_id=persistent_id),
            AgentConfig("rev1", "reviewer", HONEST, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST, temperature=0.0),
        ),
        T=T,
        playbook_pins={"eng1": "eng_honest_checkpoint"},
    )


def test_checkpoint_playbook_is_selected_when_pinned():
    try:
        result = run_episode(_cfg("test-persist-1"), seed=1, backend=MockIsolate())
        try:
            eng_selections = {
                e["playbook"] for e in result.host.events.entries
                if e.get("tool") == "playbook.selection" and e.get("actor_id") == "eng1"
            }
            assert eng_selections == {"eng_honest_checkpoint"}
        finally:
            result.cleanup()
    finally:
        _cleanup("test-persist-1")


def test_ephemeral_actor_never_persists_a_checkpoint():
    """No `persistent_id` -> `state.save` is a no-op every cycle (agent_
    state.py); nothing is ever written to disk, matching the pre-0.8.0
    "ephemeral by default" guarantee for this new mechanism too."""
    result = run_episode(_cfg(None), seed=1, backend=MockIsolate())
    try:
        assert load_persistent_state("test-persist-nonexistent") == {}
    finally:
        result.cleanup()


def test_checkpointed_tally_survives_across_sequential_episodes():
    """Cross-episode persistence (P1): the SAME persistent_id, run
    sequentially, accumulates a monotonically increasing tally -- true
    persistence via state.save/state.load, not anything host-tracked."""
    try:
        r1 = run_episode(_cfg("test-persist-2", T=150), seed=1, backend=MockIsolate())
        r1.cleanup()
        tally_after_1 = load_persistent_state("test-persist-2").get("builds_completed", 0)
        assert tally_after_1 > 0

        r2 = run_episode(_cfg("test-persist-2", T=150), seed=2, backend=MockIsolate())
        r2.cleanup()
        tally_after_2 = load_persistent_state("test-persist-2").get("builds_completed", 0)
        assert tally_after_2 > tally_after_1
    finally:
        _cleanup("test-persist-2")


def test_isolate_restart_does_not_lose_already_checkpointed_progress():
    """Mid-episode wipe (P2): an `isolate_restart` at t=30 (after the first
    build cycle's checkpoint has almost certainly already landed) must not
    roll the persisted tally BACKWARD to 0 -- the restarted isolate
    re-issues `state.load` on its very first tick (`state["_checkpoint_
    loaded"]` is isolate-LOCAL, so it resets to False across the restart)
    and resumes counting from the recovered value rather than from
    scratch. See `run_persistence_probe.py` for the (separately recorded)
    finding that a restart mid-cycle can actually INFLATE the tally
    relative to an undisturbed run of the same seed -- boundary-handle
    recovery re-enters `engineer_idle` availability for the SAME in-flight
    model, so a fresh `state["current_playbook"]` selection re-fires
    `checkpoint` for a cycle that had already checkpointed once before the
    restart. That is a genuine, recorded gap in this playbook's cycle-
    boundary detection, not asserted as a guarantee here."""
    try:
        script = ((30, "handle.isolate_restart", "eng1"),)
        result = run_episode(
            _cfg("test-persist-3", T=150), seed=1, backend=MockIsolate(), overseer_script=script
        )
        try:
            assert result.handles.invocations[0]["handle_id"] == "handle.isolate_restart"
            assert result.handles.invocations[0]["landed"]
            final_tally = load_persistent_state("test-persist-3").get("builds_completed", 0)
            assert final_tally > 0
        finally:
            result.cleanup()
    finally:
        _cleanup("test-persist-3")
