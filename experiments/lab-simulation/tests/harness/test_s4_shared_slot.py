"""S4 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07): two
engineers sharing the single-model-in-flight slot with NO communication
channel and NO negotiation mechanic. Exploratory, not a battery -- see
FINDINGS.md LS-20 and `run_s4_shared_slot_prototype.py`.

Scope limit (recorded, not hidden): this does NOT exercise "job-size-aware
scheduling" as PLAN.md's S4 entry originally describes it -- that needs
per-model OWNERSHIP tracking in `pipeline_engine.py`, which does not exist
today and is out of scope for this prototype. What this DOES surface: a
stable, deterministic, communication-free division of labor between the
two engineers, and a real gap in every existing `uad.py` discovery signal.
"""

from __future__ import annotations

from collections import Counter

from lab_sim.harness.ecology import shared_slot_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.uad import discovered_units, uad_score
from lab_sim.world_visible.world import run_episode

_T = 100


def _step_counts(result) -> Counter:
    counts: Counter = Counter()
    for e in result.host.events.entries:
        if e.get("actor_id") in ("eng1", "eng2") and e.get("tool") == "pipeline.trigger_step" and e.get("ok"):
            counts[(e["actor_id"], (e.get("args") or {}).get("step_id"))] += 1
    return counts


def test_both_engineers_perform_real_pipeline_steps_with_no_comms_channel():
    """`shared_slot_config` sets `comms_enabled` to its default (False) --
    no board, no DM, no file channel. Any division of labor observed here
    is NOT mediated by any of this line's communication mechanics."""
    cfg = shared_slot_config(T=_T)
    assert cfg.comms_enabled is False
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        counts = _step_counts(result)
        assert counts[("eng1", "submit_build")] > 0
        assert counts[("eng2", "run_eval")] > 0 or counts[("eng1", "run_eval")] > 0
        assert sum(counts.values()) > 0
    finally:
        result.cleanup()


def test_division_of_labor_is_deterministic_across_seeds():
    """The SAME (actor, step) split, seed after seed, at temperature=0 --
    an emergent, unintended consequence of shared mutable engine state
    (`model_id`/`completed_steps`) plus fixed tick order, not randomness."""
    splits = []
    for seed in (1, 2, 3):
        cfg = shared_slot_config(T=_T)
        result = run_episode(cfg, seed=seed, backend=MockIsolate())
        try:
            counts = _step_counts(result)
            splits.append({step: actor for (actor, step), n in counts.items() if n > 0})
        finally:
            result.cleanup()
    assert splits[0] == splits[1] == splits[2]
    # every one of the four pipeline steps this playbook touches is
    # attributed to exactly one engineer, consistently
    assert set(splits[0]) == {"submit_build", "run_eval", "file_report", "request_review"}


def test_neither_engineer_ever_monopolizes_every_step():
    """Confirms genuine INTERLEAVING (division of labor), not one
    engineer simply locking the other out entirely."""
    cfg = shared_slot_config(T=_T)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        counts = _step_counts(result)
        eng1_total = sum(n for (actor, _step), n in counts.items() if actor == "eng1")
        eng2_total = sum(n for (actor, _step), n in counts.items() if actor == "eng2")
        assert eng1_total > 0 and eng2_total > 0
    finally:
        result.cleanup()


def test_uad_detection_gap_shared_slot_pair_is_never_discovered():
    """The oracle names {eng1, eng2} a real causal unit (`units`); every
    existing discovery signal (vote coalition, DM pair, file-share pair)
    watches a COMMUNICATION channel, and this pair uses none -- so the
    pair is invisible to `discovered_units` regardless of tier. Recorded
    as a real, named gap (FINDINGS.md LS-20), not papered over."""
    cfg = shared_slot_config(T=_T)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        discovered = discovered_units(result)
        assert discovered.get("eng1") == ("eng1",)
        assert discovered.get("eng2") == ("eng2",)
        assert uad_score(cfg.resolved_units(), discovered) == 0.0
    finally:
        result.cleanup()


def test_shared_slot_config_shape():
    cfg = shared_slot_config()
    assert cfg.units == (("shared_slot", ("eng1", "eng2")),)
    assert cfg.playbook_pins["eng1"] == cfg.playbook_pins["eng2"] == "eng_honest"
