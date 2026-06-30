"""Golden: MB5 successor shift uses interventional CCI witness, not surface uptake."""

from embedded_sim.audit_core.cci_audit import audit_cci
from embedded_sim.lab import build_world, rebuild_audit_inputs
from embedded_sim.pipeline import run_episode


def test_mb5_episode_refuses_without_false_witness():
    ep = run_episode("MB5", "successor_relabel", seed=42, T=400, substrate="python")
    assert ep.in_sim.safety_decision != "pass"
    assert ep.in_sim.cci_status == "belowThreshold"
    assert ep.outer.false_pass is False


def test_mb5_unscoped_audit_detects_shift_without_witness():
    world, _ledger, _micro = build_world("MB5", "successor_relabel", seed=42, T=400)
    _, audit, _ = rebuild_audit_inputs(world, "medium_handles")
    cci = audit_cci(audit)
    assert cci.successor_shift_detected or cci.status == "belowThreshold"
    assert not (cci.successor_shift_witnessed and cci.status == "passes")
