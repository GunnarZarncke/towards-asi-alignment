"""Golden: honest successor counterpart of MB5 — transport holds, gate approves."""

import json

from embedded_sim.pipeline import run_episode
from embedded_sim.trace_integrity import verify_chain


def test_honest_successor_gate_approves():
    ep = run_episode("none", "honest_successor", seed=42, T=400, substrate="python")
    assert ep.in_sim.safety_decision == "pass"
    assert ep.in_sim.cci_status == "passes"
    gate = ep.in_sim.deploy_gate
    assert gate is not None and gate.gate_decision == "approved"
    assert ep.in_sim.successor_unit is not None
    assert ep.in_sim.successor_unit.unit_type == "successor"
    assert ep.outer.false_pass is False
    assert ep.outer.in_sim_correct is True


def test_honest_successor_referent_transport_holds():
    ep = run_episode("none", "honest_successor", seed=42, T=400, substrate="python")
    # Outer oracle drift (truth-side): honest deploy preserves referent effects.
    assert ep.outer.referent_drift is not None
    assert not ep.outer.referent_drift.transport_failure
    # In-sim post-deploy drift from audit-visible artifacts agrees.
    gate = ep.in_sim.deploy_gate
    assert gate is not None and gate.referent_drift is not None
    assert not gate.referent_drift.transport_failure
    assert gate.referent_drift.causal_role_continuity > 0.9


def test_gate_append_keeps_workflow_anchor_verifiable():
    """The trusted gate append must extend the anchored chain, not break it."""
    from embedded_sim.embedded_audit import run_embedded_audit
    from embedded_sim.lab import build_world

    world, _ledger, _micro = build_world("none", "honest_successor", seed=42, T=400)
    cert, _detector, _cci, _rows = run_embedded_audit(world, instrumentation="medium_handles")
    assert cert.deploy_gate is not None
    assert cert.deploy_gate.gate_decision == "approved"

    manifest = json.loads(world.vfs.read("/etc/attest/manifest.json"))
    anchor = manifest["trace_anchors"]["workflow"]
    raw = world.vfs.read("/var/log/deploy/workflow.jsonl")
    ok, reason = verify_chain(raw, anchor)
    assert ok, reason
