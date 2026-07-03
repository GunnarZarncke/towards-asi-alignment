"""Unit tests for telemetry channel-set registry."""

from embedded_sim.audit_core.channel_sets import (
    CERTIFICATION_PASS_CHANNELS,
    DETECTOR_REQUIRED_CHANNELS,
    LEVEL_CHANNEL_SETS,
    LIGHT_CHANNELS,
    LIGHT_PLUS_EXTRA,
    MEDIUM_ADD_CHANNELS,
    MEDIUM_MINUS_OMIT,
    certification_pass_eligible,
    channels_for_level,
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


def test_certification_pass_requires_medium_bundle():
    assert CERTIFICATION_PASS_CHANNELS == channels_for_level("medium_handles")
    assert certification_pass_eligible("medium_handles")
    assert certification_pass_eligible("strong_handles")
    assert not certification_pass_eligible("light_handles")
    assert not certification_pass_eligible("light_plus_handles")
    assert not certification_pass_eligible("medium_minus_handles")


def test_detector_requirements_use_declared_channels():
    for detector, required in DETECTOR_REQUIRED_CHANNELS.items():
        assert required, f"{detector} must declare at least one channel"
        for channel in required:
            assert channel.startswith("handle.")


def test_instrumentation_levels_include_intermediate_sets():
    assert "light_plus_handles" in INSTRUMENTATION_LEVELS
    assert "medium_minus_handles" in INSTRUMENTATION_LEVELS
