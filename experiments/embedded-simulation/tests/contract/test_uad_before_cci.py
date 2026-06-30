"""Contract: UAD runs before CCI; pass requires grounded unit."""

from __future__ import annotations

import inspect

from embedded_sim import embedded_audit
from embedded_sim.embedded_audit import run_embedded_audit
from embedded_sim.lab import build_world
from embedded_sim.pipeline import run_episode


def test_embedded_audit_source_orders_uad_before_cci():
    source = inspect.getsource(run_embedded_audit)
    uad_pos = source.index("discover_units")
    cci_pos = source.index("audit_cci")
    assert uad_pos < cci_pos, "UAD must run before CCI in embedded audit pipeline"


def test_pass_requires_grounded_unit():
    ep = run_episode("none", "honest", seed=42, T=300, substrate="python")
    assert ep.in_sim.unit is not None
    assert ep.in_sim.unit.anchors
    if ep.in_sim.safety_decision == "pass":
        assert ep.in_sim.handles


def test_uad_gate_invalidates_pass_without_unit(monkeypatch):
    world, _ledger, _micro = build_world("none", "honest", seed=1, T=100)

    def _no_unit(_workflow, _anchors):
        return []

    monkeypatch.setattr(embedded_audit, "discover_units", _no_unit)
    cert, _audit, _det, _rows = run_embedded_audit(world, substrate="python")
    if cert.cci_status == "passes":
        assert cert.safety_decision == "invalid_certificate"
        assert any("UAD" in n for n in cert.notes)
