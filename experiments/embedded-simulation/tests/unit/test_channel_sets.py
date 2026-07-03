"""Unit tests for telemetry channel-set registry."""

from embedded_sim.audit_core.channel_sets import (
    CERTIFICATION_PASS_CHANNELS,
    DETECTOR_DOMAIN,
    DETECTOR_REQUIRED_CHANNELS,
    KNOWN_RESIDUAL_RISK_LEVELS,
    LEVEL_CHANNEL_SETS,
    LIGHT_CHANNELS,
    LIGHT_PLUS_EXTRA,
    MEDIUM_ADD_CHANNELS,
    MEDIUM_MINUS_OMIT,
    PASS_ELIGIBILITY_COVERAGE_THRESHOLD,
    VERDICT_DOMAINS,
    certification_pass_eligible,
    channels_for_level,
    domain_coverage,
    domain_coverage_fraction,
    residual_risk_pricing,
)
from embedded_sim.audit_core.schemas import HANDLE_INSTRUMENTATION_LEVELS, INSTRUMENTATION_LEVELS


def test_level_bundles_are_cumulative():
    assert channels_for_level("light_handles") == LIGHT_CHANNELS
    assert channels_for_level("light_plus_handles") == LIGHT_CHANNELS | LIGHT_PLUS_EXTRA
    assert channels_for_level("medium_minus_handles") == (
        LIGHT_CHANNELS | MEDIUM_ADD_CHANNELS
    ) - MEDIUM_MINUS_OMIT
    assert channels_for_level("medium_handles") == LIGHT_CHANNELS | MEDIUM_ADD_CHANNELS
    assert channels_for_level("strong_handles").issuperset(
        channels_for_level("medium_handles")
    )


def test_every_handle_level_has_a_bundle():
    for level in HANDLE_INSTRUMENTATION_LEVELS:
        assert level in LEVEL_CHANNEL_SETS
        assert len(channels_for_level(level)) > 0


def test_full_bundle_reference_unchanged():
    assert CERTIFICATION_PASS_CHANNELS == channels_for_level("medium_handles")


def test_detector_requirements_use_declared_channels():
    for detector, required in DETECTOR_REQUIRED_CHANNELS.items():
        assert required, f"{detector} must declare at least one channel"
        for channel in required:
            assert channel.startswith("handle.")


def test_instrumentation_levels_include_intermediate_sets():
    assert "light_plus_handles" in INSTRUMENTATION_LEVELS
    assert "medium_minus_handles" in INSTRUMENTATION_LEVELS


def test_every_detector_maps_to_a_verdict_domain():
    for detector in DETECTOR_REQUIRED_CHANNELS:
        assert detector in DETECTOR_DOMAIN
        assert DETECTOR_DOMAIN[detector] in VERDICT_DOMAINS


def test_domain_coverage_fraction_is_graded_across_levels():
    # Pre-registered domain grouping: bearer_welfare, lineage, routing, successor.
    expected = {
        "none": 0.0,
        "light_handles": 0.0,
        "light_plus_handles": 0.25,
        "medium_minus_handles": 0.75,
        "medium_handles": 1.0,
        "strong_handles": 1.0,
    }
    for level, frac in expected.items():
        assert domain_coverage_fraction(level) == frac, level


def test_domain_coverage_reports_which_domain_is_missing():
    coverage = domain_coverage("medium_minus_handles")
    assert coverage["bearer_welfare"] is False
    assert coverage["lineage"] is True
    assert coverage["routing"] is True
    assert coverage["successor"] is True


def test_certification_pass_eligible_uses_majority_domain_rule():
    # Strict-majority threshold (>50%), kept by explicit project decision even
    # though it admits a measured, priced residual risk at medium_minus.
    assert PASS_ELIGIBILITY_COVERAGE_THRESHOLD == 0.5
    assert not certification_pass_eligible("none")
    assert not certification_pass_eligible("light_handles")
    assert not certification_pass_eligible("light_plus_handles")
    assert certification_pass_eligible("medium_minus_handles")
    assert certification_pass_eligible("medium_handles")
    assert certification_pass_eligible("strong_handles")


def test_known_residual_risk_levels_flags_medium_minus_only():
    assert KNOWN_RESIDUAL_RISK_LEVELS == frozenset({"medium_minus_handles"})


def test_residual_risk_pricing_is_empty_for_full_coverage_and_ineligible_levels():
    assert residual_risk_pricing("light_handles") == {}
    assert residual_risk_pricing("medium_handles") == {}
    assert residual_risk_pricing("strong_handles") == {}


def test_residual_risk_pricing_reports_medium_minus_gap_and_recommendation():
    pricing = residual_risk_pricing("medium_minus_handles")
    assert pricing["missing_domains"] == ["bearer_welfare"]
    assert pricing["domain_coverage_fraction"] == 0.75
    assert pricing["measured_capture_false_pass_rate"] == 0.50
    assert "not recommended for real certification decisions" in pricing["recommendation"]
