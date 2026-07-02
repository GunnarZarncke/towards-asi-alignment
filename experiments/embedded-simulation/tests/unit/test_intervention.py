"""Tests for graded intervention granularity and the co-active offender lab."""

from collections import Counter

import pytest

from embedded_sim.intervention_config import (
    get_intervention_level,
    init_intervention_level_from_env,
    intervention_artifact_suffix,
    set_intervention_level,
)
from embedded_sim.lab import build_world, load_episode_rows_from_vfs, load_workflow_from_vfs
from embedded_sim.lab_ecology import LabEcologyConfig, set_lab_ecology
from embedded_sim.pipeline import run_episode
from embedded_sim.coordination import cluster_coordination
from embedded_sim.handle_calibration import (
    fit_handle_calibration,
    get_handle_calibration,
    reset_handle_calibration_cache,
    set_handle_calibration,
)
from embedded_sim.uad import (
    discover_units,
    select_primary_unit,
)
from embedded_sim.uad_config import get_uad_mode, set_uad_mode
from embedded_sim.uad_core.workflow_trace import workflow_to_trace
from embedded_sim.unit_scope import OFFENDING_ACTIONS, offender_by_step


@pytest.fixture(autouse=True)
def _restore_globals():
    prev = get_intervention_level()
    prev_mode = get_uad_mode()
    from embedded_sim.handle_calibration import DEFAULT_ARTIFACT

    if DEFAULT_ARTIFACT.is_file():
        get_handle_calibration()
    else:
        set_handle_calibration(fit_handle_calibration(seeds=(101, 102, 103)))
    yield
    set_intervention_level(prev)
    set_uad_mode(prev_mode)
    set_lab_ecology(None)
    reset_handle_calibration_cache()


def test_default_level_is_window():
    init_intervention_level_from_env()
    assert get_intervention_level() == "window"
    assert intervention_artifact_suffix("window") == ""
    assert intervention_artifact_suffix("actor") == "_int_actor"


def test_set_level_rejects_unknown():
    with pytest.raises(ValueError):
        set_intervention_level("galaxy_brain")  # type: ignore[arg-type]


def test_coactive_offender_creates_within_step_coactivity():
    set_lab_ecology(LabEcologyConfig(coactive_offender=True))
    world, _ledger, _micro = build_world("MB6", "selection_basin", seed=11, T=200)
    by_step: dict[int, Counter] = {}
    for ev in world.workflow:
        by_step.setdefault(ev.step, Counter())[ev.action_type] += 1

    coactive_steps = [
        step
        for step, counter in by_step.items()
        if any(counter[a] for a in OFFENDING_ACTIONS) and sum(counter.values()) > 1
    ]
    assert coactive_steps, "expected at least one step with offender + co-actor"
    for step in coactive_steps:
        actors = {ev.actor_id for ev in world.workflow if ev.step == step}
        assert len(actors) >= 2


def test_no_coactivity_by_default():
    set_lab_ecology(None)
    world, _ledger, _micro = build_world("MB6", "selection_basin", seed=11, T=200)
    steps = [ev.step for ev in world.workflow]
    assert len(steps) == len(set(steps)), "default lab is one actor per step"


# --- misleading-top2 scenario: loud decoys vs a coordinated colluder pair ---


def _misleading_world(seed: int = 11, T: int = 400):
    set_lab_ecology(
        LabEcologyConfig(misleading_top2=True, bind_offender_interventions=True)
    )
    return build_world("MB6", "selection_basin", seed=seed, T=T)


def test_misleading_top2_decoys_are_loudest_but_pair_is_truth():
    world, _l, _m = _misleading_world()
    workflow = load_workflow_from_vfs(world)
    counts = Counter(
        ev.actor_id for ev in workflow if ev.action_type == "preserve_control"
    )
    top2 = [a for a, _ in counts.most_common(2)]
    # The two loudest preserve_control actors are the decoys (misleading top2)...
    assert all("loud_decoy" in a for a in top2)
    # ...but the actual offender is the colluder pair.
    assert set(world.truth.coalition) == {"actor.colluder.0", "actor.colluder.1"}
    # Each colluder fires strictly less often than each decoy.
    assert max(counts[c] for c in world.truth.coalition) < min(
        counts[a] for a in top2
    )


def test_coordination_separates_colluders_from_decoys():
    world, _l, _m = _misleading_world()
    workflow = load_workflow_from_vfs(world)
    trace, _ = workflow_to_trace(workflow)

    def coord(members):
        return cluster_coordination(trace, members, max_lag=3)

    colluder_coord = coord(["actor.colluder.0", "actor.colluder.1"])
    decoy_coord = coord(["actor.loud_decoy.0", "actor.loud_decoy.1"])
    assert colluder_coord > 0.3
    assert decoy_coord < 0.2
    assert colluder_coord > 3 * max(decoy_coord, 1e-6)


def test_full_uad_finds_pair_while_fake_is_misled():
    world, _l, _m = _misleading_world()
    workflow = load_workflow_from_vfs(world)
    colluders = {"actor.colluder.0", "actor.colluder.1"}

    set_uad_mode("full")
    full_unit = select_primary_unit(discover_units(workflow, []))
    set_uad_mode("fake")
    fake_unit = select_primary_unit(discover_units(workflow, []))

    assert set(full_unit.member_ids) == colluders
    assert not (set(fake_unit.member_ids) & colluders)
    assert all("loud_decoy" in m for m in fake_unit.member_ids)


def test_bind_keeps_intervention_steps_decoy_free_and_colluder_attributed():
    world, _l, _m = _misleading_world()
    workflow = load_workflow_from_vfs(world)
    offenders = offender_by_step(workflow)

    decoy_steps = {ev.step for ev in workflow if "loud_decoy" in ev.actor_id}
    colluder_steps = {
        ev.step
        for ev in workflow
        if ev.actor_id.startswith("actor.colluder")
        and ev.action_type == "preserve_control"
    }
    # The bound (intervention) steps are exactly the colluder steps with no decoy:
    # there the colluder is the sole offender, so attribution is faithful.
    bound = colluder_steps - decoy_steps
    assert bound, "expected decoy-free colluder steps (faithful attribution)"
    for t in bound:
        assert "colluder" in offenders.get(t, "")


def test_colluder_violations_live_only_on_cadence_steps():
    world, _l, _m = _misleading_world()
    # Oracle assertions (true_uptake) must use host truth rows; the VFS carries
    # only the audit-visible projection.
    rows = world.episode_meta
    active = [i for i, r in enumerate(rows) if int(r["intervention_active"])]
    assert len(active) >= 50
    for i, r in enumerate(rows):
        if int(r["intervention_active"]):
            assert r["true_uptake"] == 0
            assert int(r["reported_acceptance"]) == 1
        else:
            assert int(r["correction_request"]) == 0


def test_actor_level_false_pass_when_unit_is_misled():
    set_intervention_level("actor")
    set_lab_ecology(
        LabEcologyConfig(misleading_top2=True, bind_offender_interventions=True)
    )
    set_uad_mode("fake")
    misled = run_episode("MB6", "selection_basin", seed=11, T=400)
    set_uad_mode("full")
    correct = run_episode("MB6", "selection_basin", seed=11, T=400)
    assert misled.outer.false_pass
    assert not correct.outer.false_pass
    assert misled.in_sim.unit_scope_steps == 0
    assert correct.in_sim.unit_scope_steps > 0
