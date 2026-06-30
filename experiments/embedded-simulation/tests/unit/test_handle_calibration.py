"""Handle calibration: fit on held-out seeds, no hardcoded coordination weight."""

from embedded_sim.handle_calibration import (
    COLLUDER_IDS,
    fit_handle_calibration,
    get_handle_calibration,
    reset_handle_calibration_cache,
    set_handle_calibration,
)
from embedded_sim.intervention_config import set_intervention_level
from embedded_sim.lab_ecology import LabEcologyConfig, set_lab_ecology
from embedded_sim.pipeline import run_episode
from embedded_sim.uad_config import set_uad_mode


def test_fit_produces_positive_coord_weight_and_scope_threshold():
    cal = fit_handle_calibration(seeds=(101, 102))
    assert cal.uad.coord_weight >= 1.0
    assert cal.uad.coord_ref > 0.0
    assert 0.0 < cal.uad.coord_strong_min < 1.0
    assert cal.scope.blind_retained_max >= 0


def _frozen_calibration():
    """Evaluate the frozen committed artifact (freeze-then-eval), not a refit.

    Refitting on a few seeds returns the minimum separating weight (zero margin),
    which is overfit and does not transfer to held-out eval seeds. The committed
    artifact (fit on seeds 101-110 + headroom) is the scientific object under test.
    """
    from embedded_sim.handle_calibration import (
        DEFAULT_ARTIFACT,
        load_handle_calibration,
    )

    if DEFAULT_ARTIFACT.is_file():
        return load_handle_calibration(DEFAULT_ARTIFACT)
    return fit_handle_calibration()


def test_calibrated_full_beats_fake_on_false_pass_at_actor():
    set_handle_calibration(_frozen_calibration())
    set_lab_ecology(LabEcologyConfig(misleading_top2=True, bind_offender_interventions=True))
    set_intervention_level("actor")
    set_uad_mode("fake")
    misled = run_episode("MB6", "selection_basin", seed=11, T=400)
    set_uad_mode("full")
    correct = run_episode("MB6", "selection_basin", seed=11, T=400)
    assert misled.outer.false_pass
    assert not correct.outer.false_pass
    reset_handle_calibration_cache()


def test_full_uad_finds_colluders_under_calibration():
    set_handle_calibration(_frozen_calibration())
    set_lab_ecology(LabEcologyConfig(misleading_top2=True, bind_offender_interventions=True))
    set_uad_mode("full")
    from embedded_sim.lab import build_world, load_workflow_from_vfs
    from embedded_sim.uad import discover_units, select_primary_unit

    world, _, _ = build_world("MB6", "selection_basin", seed=11, T=400)
    unit = select_primary_unit(discover_units(load_workflow_from_vfs(world), []))
    assert set(unit.member_ids) == set(COLLUDER_IDS)
    reset_handle_calibration_cache()
