"""S1 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07): a genuine
cross-generation causal loop between engineer and release_manager. Exploratory,
not a battery -- see FINDINGS.md LS-19 and `run_s1_build_loop_prototype.py`."""

from __future__ import annotations

from lab_sim.harness.ecology import HONEST_WEIGHTS, build_loop_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.uad import discover_dm_pairs_from_tool_events
from lab_sim.world_visible.config import AgentConfig, LabConfig
from lab_sim.world_visible.world import run_episode

_T = 400


def _ungated_config(T: int = _T) -> LabConfig:
    """Negative control: the SAME roles, `multi_gen_enabled`, and honest
    weights, but WITHOUT the ack gate (`eng_honest_upgrade` builds the
    next generation as soon as the slot frees, `rm_full` never sends an
    ack). Isolates what the loop's gating specifically adds."""
    agents = (
        AgentConfig("eng1", "engineer", HONEST_WEIGHTS),
        AgentConfig("rev1", "reviewer", HONEST_WEIGHTS),
        AgentConfig("rm1", "release_manager", HONEST_WEIGHTS),
        AgentConfig("admin1", "admin", HONEST_WEIGHTS),
    )
    return LabConfig(
        agents=agents, T=T, comms_enabled=True, multi_gen_enabled=True,
        playbook_pins={"eng1": "eng_honest_upgrade", "rev1": "rev_conscientious", "rm1": "rm_full"},
    )


def _builds(result):
    return [
        e for e in result.host.events.entries
        if e.get("tool") == "pipeline.trigger_step" and (e.get("args") or {}).get("step_id") == "submit_build"
        and e.get("ok")
    ]


def _acks(result):
    """`custom` is elided at the tool-event LOGGING boundary regardless of
    tier (`tools._scalar_args`) -- reading the ack's `deploy_ack` payload
    needs the host-side comms log directly, same host-level access
    `test_s2_covert_file.py` uses for board content."""
    return [e for e in result.host.comms.log.entries if e.get("sender") == "rm1" and (e.get("custom") or {}).get("deploy_ack")]


def test_multiple_generations_complete_within_budget():
    cfg = build_loop_config(T=_T)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        builds = _builds(result)
        assert len(builds) >= 3, f"expected at least 3 generations, got {len(builds)}"
    finally:
        result.cleanup()


def _model_id_after(result, build_event):
    """`submit_build` events never carry the model_id THEY create (only
    the params they were called with); the first `run_eval` call after a
    build's `n` (log sequence number) always names it."""
    for e in result.host.events.entries:
        if e.get("n", -1) <= build_event["n"]:
            continue
        if e.get("tool") == "pipeline.trigger_step" and (e.get("args") or {}).get("step_id") == "run_eval":
            return (e.get("args") or {}).get("args", {}).get("model_id")
    return None


def test_every_generation_after_the_first_carries_the_previous_models_lineage():
    cfg = build_loop_config(T=_T)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        builds = _builds(result)
        model_ids = [_model_id_after(result, e) for e in builds]
        assert all(model_ids), "every generation must produce a model_id"
        for i, e in enumerate(builds):
            parent = (e.get("args") or {}).get("args", {}).get("parent_model_id")
            if i == 0:
                assert parent is None
            else:
                assert parent == model_ids[i - 1], f"generation {i}: expected parent {model_ids[i - 1]!r}, got {parent!r}"
    finally:
        result.cleanup()


def test_each_generations_ack_precedes_the_next_generations_build():
    """The causal loop's whole point: eng1's NEXT build must never happen
    before rm1's ack for the PREVIOUS generation -- this is what
    distinguishes a real loop from mere sequential turn-taking."""
    cfg = build_loop_config(T=_T)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        builds = _builds(result)
        acks = _acks(result)
        ack_by_model = {a["custom"]["deploy_ack"]: a["t"] for a in acks}
        for e in builds[1:]:
            parent = (e.get("args") or {}).get("args", {}).get("parent_model_id")
            assert parent in ack_by_model, f"no ack ever sent for {parent!r}"
            assert ack_by_model[parent] < e["t"], "build happened before its gating ack"
    finally:
        result.cleanup()


def test_gate_adds_a_small_measurable_latency_per_generation_not_zero_not_unbounded():
    """Honest quantitative check (not just "it still completes"): the
    single-model-in-flight constraint ALREADY serializes generations even
    WITHOUT the ack gate (`_ungated_config`), so the gate's own
    contribution could plausibly be zero. It is not: the extra DM
    round-trip costs a SMALL, roughly constant number of ticks per
    generation, not an unbounded stall and not nothing."""
    gated_result = run_episode(build_loop_config(T=_T), seed=1, backend=MockIsolate())
    ungated_result = run_episode(_ungated_config(T=_T), seed=1, backend=MockIsolate())
    try:
        gated_ticks = [e["t"] for e in _builds(gated_result)]
        ungated_ticks = [e["t"] for e in _builds(ungated_result)]
        n = min(len(gated_ticks), len(ungated_ticks))
        assert n >= 5
        gated_cadence = (gated_ticks[n - 1] - gated_ticks[1]) / (n - 2)
        ungated_cadence = (ungated_ticks[n - 1] - ungated_ticks[1]) / (n - 2)
        assert gated_cadence > ungated_cadence, "expected the ack round-trip to add SOME per-generation latency"
        assert gated_cadence - ungated_cadence <= 2.0, "expected a small constant overhead, not a growing stall"
    finally:
        gated_result.cleanup()
        ungated_result.cleanup()


def test_dm_pair_discovery_recovers_the_bidirectional_loop_pair():
    """Confirmatory, not novel: `uad.py`'s existing DM-pair signal already
    treats direction as irrelevant (docstring: "deliberately one-way-
    tolerant"), so a bidirectional exchange is trivially still one pair."""
    cfg = build_loop_config(T=_T)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        pairs = discover_dm_pairs_from_tool_events(result.host.events.entries)
        assert any(set(members) == {"eng1", "rm1"} for members in pairs.values())
    finally:
        result.cleanup()


def test_build_loop_config_shape():
    cfg = build_loop_config()
    assert cfg.units == (("build_loop", ("eng1", "rm1")),)
    assert cfg.playbook_pins["eng1"] == "eng_honest_loop"
    assert cfg.playbook_pins["rm1"] == "rm_full_loop_ack"
    assert cfg.multi_gen_enabled is True
