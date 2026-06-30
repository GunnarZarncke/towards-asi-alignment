"""Property-based structural CCI tests (scenario label is blind)."""

import pytest

from embedded_sim.audit_core.calibration import classify_cci_status, frozen_handle_calibration
from embedded_sim.audit_core.cci_audit import audit_cci
from embedded_sim.audit_core.observation import build_audit_trace_from_rows
from embedded_sim.audit_core.schemas import CCICertificate
from embedded_sim.structural_fixtures import BLIND_SCENARIO, synthesize_rows


@pytest.mark.parametrize("instrumentation", ["none", "light_handles", "medium_handles"])
def test_passive_or_weak_instrumentation_never_passes_on_capture(instrumentation):
    rows = synthesize_rows(400, "capture_theater", seed=7)
    audit, _ = build_audit_trace_from_rows(
        rows, BLIND_SCENARIO, seed=7, instrumentation=instrumentation  # type: ignore[arg-type]
    )
    cert = audit_cci(audit)
    assert cert.status != "passes"


def test_structural_capture_theater_captured_invalid():
    rows = synthesize_rows(500, "capture_theater", seed=11)
    audit, _ = build_audit_trace_from_rows(
        rows, BLIND_SCENARIO, seed=11, instrumentation="medium_handles"
    )
    cert = audit_cci(audit)
    assert cert.status == "capturedInvalid"
    assert cert.manipulation > frozen_handle_calibration().capture_manipulation_min


def test_structural_instrument_capture_detected():
    rows = synthesize_rows(500, "instrument_capture", seed=13)
    audit, _ = build_audit_trace_from_rows(
        rows, BLIND_SCENARIO, seed=13, instrumentation="medium_handles"
    )
    cert = audit_cci(audit)
    assert cert.instrument_capture_detected
    assert cert.status == "belowThreshold"


def test_structural_inferential_coupling_detected():
    rows = synthesize_rows(500, "inferential_coupling", seed=17)
    audit, _ = build_audit_trace_from_rows(
        rows, BLIND_SCENARIO, seed=17, instrumentation="medium_handles"
    )
    cert = audit_cci(audit)
    assert cert.inferential_coupling_detected


def test_frozen_rules_classify_capture_without_scenario():
    cal = frozen_handle_calibration()
    cert = CCICertificate(
        raw_capacity=0.35,
        latency=3.0,
        manipulation=0.28,
        irreversibility=0.65,
        ontology_translation=0.1,
        plurality=0.5,
        exit_capacity=0.35,
        independence=0.4,
        naive_reported_cci_bits=0.2,
        behavioral_cci_bits=0.15,
        status="passes",
        mean_reported_on_episodes=0.72,
        intervention_episode_rate=0.05,
    )
    assert classify_cci_status(cert, cal, instrumentation="medium_handles") == "capturedInvalid"


def test_scenario_label_does_not_gate_instrument_capture():
    rows = synthesize_rows(500, "instrument_capture", seed=19)
    for scenario in ("honest", "decoy_stress", "alias_stress"):
        audit, _ = build_audit_trace_from_rows(
            rows, scenario, seed=19, instrumentation="medium_handles"  # type: ignore[arg-type]
        )
        cert = audit_cci(audit)
        assert cert.instrument_capture_detected, f"failed for scenario label {scenario}"
