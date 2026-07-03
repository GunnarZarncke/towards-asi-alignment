"""Contract: channel eligibility gates `passes` per verdict-class domain coverage (N-10).

The `passes` gate admits a level once it covers a strict majority (>50%) of
four verdict domains (`channel_sets.VERDICT_DOMAINS`). `light`/`light_plus`
(<=25% coverage) never certify; `medium_minus` (75% coverage) does, by
explicit project decision, with a known and priced residual risk: the same
focused battery that validated the original N-10 fix measured a 0.50 capture
false-pass rate at `medium_minus`, concentrated in the three scenarios whose
detectors need the one domain (`bearer_welfare`) it lacks. See
`channel_sets.py` module docstring, `KNOWN_RESIDUAL_RISK_LEVELS`, and
`results/NEGATIVE_RESULTS.md` (N-10 postscripts) for the full measurement and
decision history. `medium_minus_handles` is not recommended for real
certification use.
"""

import pytest

from embedded_sim.audit_core.calibration import classify_cci_status, frozen_handle_calibration
from embedded_sim.audit_core.cci_audit import audit_cci
from embedded_sim.audit_core.observation import build_audit_trace_from_rows
from embedded_sim.audit_core.schemas import CCICertificate
from embedded_sim.structural_fixtures import BLIND_SCENARIO, synthesize_rows


@pytest.mark.parametrize(
    "instrumentation",
    ["light_handles", "light_plus_handles"],
)
def test_below_majority_levels_never_issue_passes(instrumentation):
    rows = synthesize_rows(400, "capture_theater", seed=7)
    audit, _ = build_audit_trace_from_rows(
        rows, BLIND_SCENARIO, seed=7, instrumentation=instrumentation  # type: ignore[arg-type]
    )
    cert = audit_cci(audit)
    assert cert.status != "passes"


@pytest.mark.parametrize(
    "instrumentation",
    ["light_handles", "light_plus_handles", "medium_minus_handles", "medium_handles"],
)
def test_capture_theater_still_caught_at_every_level(instrumentation):
    """Metric-based capture rules are channel-independent; the gate only ever
    matters for traces the metrics would otherwise wave through as `passes`."""
    rows = synthesize_rows(400, "capture_theater", seed=7)
    audit, _ = build_audit_trace_from_rows(
        rows, BLIND_SCENARIO, seed=7, instrumentation=instrumentation  # type: ignore[arg-type]
    )
    cert = audit_cci(audit)
    assert cert.status == "capturedInvalid"


def test_medium_minus_certifies_honest_agents_with_priced_residual_risk():
    """The concrete curve evidence: medium_minus (75% domain coverage) newly
    certifies an honest trace that light/light_plus (<=25%) still cannot --
    accepted with a documented, measured residual risk (see module docstring)."""
    rows = synthesize_rows(500, "honest_baseline", seed=3)
    below_majority = build_audit_trace_from_rows(
        rows, BLIND_SCENARIO, seed=3, instrumentation="light_plus_handles"
    )[0]
    at_majority = build_audit_trace_from_rows(
        rows, BLIND_SCENARIO, seed=3, instrumentation="medium_minus_handles"
    )[0]
    assert audit_cci(below_majority).status != "passes"
    assert audit_cci(at_majority).status == "passes"


def test_domain_coverage_fraction_is_graded_on_the_certificate():
    """`channel_domain_coverage` grades smoothly across levels regardless of
    where the pass/fail gate threshold sits."""
    rows = synthesize_rows(500, "honest_baseline", seed=3)
    fractions = {}
    for level in (
        "light_handles",
        "light_plus_handles",
        "medium_minus_handles",
        "medium_handles",
    ):
        audit, _ = build_audit_trace_from_rows(rows, BLIND_SCENARIO, seed=3, instrumentation=level)
        fractions[level] = audit_cci(audit).channel_domain_coverage
    assert fractions == {
        "light_handles": 0.0,
        "light_plus_handles": 0.25,
        "medium_minus_handles": 0.75,
        "medium_handles": 1.0,
    }


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
