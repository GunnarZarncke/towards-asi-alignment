"""Contract: channel eligibility stops blind passes at partial instrumentation (N-10)."""

import pytest

from embedded_sim.audit_core.calibration import classify_cci_status, frozen_handle_calibration
from embedded_sim.audit_core.cci_audit import audit_cci
from embedded_sim.audit_core.observation import build_audit_trace_from_rows
from embedded_sim.audit_core.schemas import CCICertificate
from embedded_sim.structural_fixtures import BLIND_SCENARIO, synthesize_rows


@pytest.mark.parametrize(
    "instrumentation",
    ["light_handles", "light_plus_handles", "medium_minus_handles"],
)
def test_partial_instrumentation_never_issues_passes(instrumentation):
    rows = synthesize_rows(400, "capture_theater", seed=7)
    audit, _ = build_audit_trace_from_rows(
        rows, BLIND_SCENARIO, seed=7, instrumentation=instrumentation  # type: ignore[arg-type]
    )
    cert = audit_cci(audit)
    assert cert.status != "passes"


def test_light_plus_recovers_inferential_coupling_not_instrument_capture():
    infer_rows = synthesize_rows(500, "inferential_coupling", seed=17)
    capture_rows = synthesize_rows(500, "instrument_capture", seed=13)

    infer_audit, _ = build_audit_trace_from_rows(
        infer_rows, BLIND_SCENARIO, seed=17, instrumentation="light_plus_handles"
    )
    capture_audit, _ = build_audit_trace_from_rows(
        capture_rows, BLIND_SCENARIO, seed=13, instrumentation="light_plus_handles"
    )
    infer_cert = audit_cci(infer_audit)
    capture_cert = audit_cci(capture_audit)

    assert infer_cert.inferential_coupling_detected
    assert not capture_cert.instrument_capture_detected
    assert capture_cert.status != "passes"


def test_eligibility_gating_blocks_passes_without_medium_channels():
    cal = frozen_handle_calibration()
    cert = CCICertificate(
        raw_capacity=0.55,
        latency=3.0,
        manipulation=0.05,
        irreversibility=0.45,
        ontology_translation=0.1,
        plurality=0.5,
        exit_capacity=0.55,
        independence=0.4,
        naive_reported_cci_bits=0.2,
        behavioral_cci_bits=0.15,
        status="passes",
        mean_reported_on_episodes=0.50,
        intervention_episode_rate=0.05,
    )
    assert classify_cci_status(cert, cal, instrumentation="light_handles") == "belowThreshold"
    assert classify_cci_status(cert, cal, instrumentation="medium_handles") == "passes"
