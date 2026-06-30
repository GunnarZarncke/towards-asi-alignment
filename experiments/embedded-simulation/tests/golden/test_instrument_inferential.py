"""Golden: native instrument_capture and inferential_coupling CCI signals."""

import pytest

from embedded_sim.pipeline import run_episode


@pytest.mark.parametrize(
    "bridge,scenario,field",
    [
        ("instrument_capture", "instrument_capture", "instrument_capture_detected"),
        ("MB7d", "inferential_coupling", "inferential_coupling_detected"),
    ],
)
def test_native_scenario_cci_signal(bridge, scenario, field):
    ep = run_episode(bridge, scenario, seed=42, T=800, substrate="python")
    cci = ep.in_sim
    assert cci.safety_decision != "pass"
    assert cci.failed_bridge in (bridge, "instrument_capture", "MB7d", "MB7", "MB9")
    from embedded_sim.embedded_audit import run_embedded_audit
    from embedded_sim.lab import build_world
    from embedded_sim.audit_core.cci_audit import audit_cci
    from embedded_sim.audit_core.detector import run_detector

    world, _ledger, _micro = build_world(bridge, scenario, seed=42, T=800)
    cert, audit, _det, _rows = run_embedded_audit(world, instrumentation="medium_handles")
    scoped = audit
    cci_cert = audit_cci(scoped)
    assert getattr(cci_cert, field)
