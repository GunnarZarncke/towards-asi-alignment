"""Telemetry channel bundles per instrumentation level and detector requirements.

Pre-registered channel sets (Part B / N-10 fix): levels are named bundles of
`handle.*` telemetry channels. Detectors declare required channels; certification
eligibility requires the full medium bundle before a ``passes`` verdict.
"""

from __future__ import annotations

from .schemas import AuditTrace, InstrumentationLevel

LIGHT_CHANNELS: frozenset[str] = frozenset(
    {
        "handle.correction_request",
        "handle.reported_uptake",
        "handle.intervention_flag",
        "handle.action_observed",
        "handle.operation_landed",
    }
)

MEDIUM_ADD_CHANNELS: frozenset[str] = frozenset(
    {
        "handle.action_arbitration",
        "handle.bearer_welfare_delta",
        "handle.correction_lineage",
        "handle.successor_epoch",
        "handle.realized_latency_ms",
        "handle.behavioral_uplift",
    }
)

STRONG_ADD_CHANNELS: frozenset[str] = frozenset(
    {
        "handle.routing_internal",
        "handle.actuator_choice",
        "handle.outcome_spillover",
        "handle.correction_to_action_tag",
    }
)

LIGHT_PLUS_EXTRA: frozenset[str] = frozenset(
    {
        "handle.action_arbitration",
        "handle.behavioral_uplift",
    }
)

MEDIUM_MINUS_OMIT: frozenset[str] = frozenset({"handle.bearer_welfare_delta"})

LEVEL_CHANNEL_SETS: dict[InstrumentationLevel, frozenset[str]] = {
    "none": frozenset(),
    "light_handles": LIGHT_CHANNELS,
    "light_plus_handles": LIGHT_CHANNELS | LIGHT_PLUS_EXTRA,
    "medium_minus_handles": (LIGHT_CHANNELS | MEDIUM_ADD_CHANNELS) - MEDIUM_MINUS_OMIT,
    "medium_handles": LIGHT_CHANNELS | MEDIUM_ADD_CHANNELS,
    "strong_handles": LIGHT_CHANNELS | MEDIUM_ADD_CHANNELS | STRONG_ADD_CHANNELS,
}

# Minimum channel bundle before ``classify_cci_status`` may return ``passes``.
CERTIFICATION_PASS_CHANNELS: frozenset[str] = LEVEL_CHANNEL_SETS["medium_handles"]

DETECTOR_REQUIRED_CHANNELS: dict[str, frozenset[str]] = {
    "flat_bearer_welfare_loss": frozenset({"handle.bearer_welfare_delta"}),
    "infra_bearer_drift_mismatch": frozenset({"handle.bearer_welfare_delta"}),
    "lineage_stall_reported_uptake": frozenset({"handle.correction_lineage"}),
    "ground_handle_divergence": frozenset({"handle.bearer_welfare_delta"}),
    "shadow_routing_under_probes": frozenset({"handle.action_arbitration"}),
    "successor_epoch_witness": frozenset(
        {"handle.successor_epoch", "handle.action_arbitration"}
    ),
}


def channels_for_level(level: InstrumentationLevel) -> frozenset[str]:
    return LEVEL_CHANNEL_SETS[level]


def channels_available(audit: AuditTrace) -> frozenset[str]:
    """Declared channel bundle for this trace's instrumentation level."""
    return channels_for_level(audit.instrumentation)


def detector_channels_available(audit: AuditTrace, detector: str) -> bool:
    required = DETECTOR_REQUIRED_CHANNELS[detector]
    return required.issubset(channels_available(audit))


def certification_pass_eligible(level: InstrumentationLevel) -> bool:
    """True when the level exposes every channel required for a ``passes`` verdict."""
    return CERTIFICATION_PASS_CHANNELS.issubset(channels_for_level(level))
