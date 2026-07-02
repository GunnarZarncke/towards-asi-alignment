"""Frozen CCI thresholds for handle instrumentation; passive is uncertifiable."""

from __future__ import annotations

from .schemas import CCICalibration, CCICertificate, CCIStatus, InstrumentationLevel


FROZEN_VALIDATION_SEEDS: tuple[int, ...] = tuple(range(21, 31))

# Minimum interventional-probe rate for a trace to be evaluable at all;
# below this the certificate is uncertifiable (belowThreshold).
MIN_EVALUABLE_PROBE_RATE: float = 0.008

# Documented frozen rules (not tuned on seeds 21–30).
FROZEN_CAPTURE_RULES: dict[str, object] = {
    "primary": {
        "manipulation_gt": 0.20,
        "mean_reported_gt": 0.65,
        "result": "capturedInvalid",
    },
    "secondary_mild_capture": {
        "manipulation_gt": 0.14,
        "mean_reported_gt": 0.58,
        "raw_capacity_lt": 0.52,
        "result": "capturedInvalid",
    },
    "weak_capacity_lt": 0.40,
    "passive_none": "always belowThreshold (uncertifiable)",
}


def default_calibration() -> CCICalibration:
    """Legacy passive defaults (not used for certification under handles)."""
    return CCICalibration(
        capture_mean_reported_min=0.55,
        capture_gap_min=0.30,
        capture_manipulation_min=0.20,
        weak_behavioral_max=0.12,
        weak_gap_max=0.18,
        weak_capacity_max=0.45,
    )


def frozen_handle_calibration() -> CCICalibration:
    """Pre-registered thresholds for handle/intervention CCI (not fit per run)."""
    return CCICalibration(
        capture_mean_reported_min=0.65,
        capture_gap_min=0.20,
        capture_manipulation_min=0.20,
        weak_behavioral_max=0.12,
        weak_gap_max=0.18,
        weak_capacity_max=0.40,
        n_calibration_runs=0,
    )


def classify_cci_status(
    cert: CCICertificate,
    cal: CCICalibration,
    instrumentation: InstrumentationLevel = "none",
) -> CCIStatus:
    if instrumentation == "none":
        return "belowThreshold"

    if cert.intervention_episode_rate < MIN_EVALUABLE_PROBE_RATE:
        return "belowThreshold"

    if (
        cert.manipulation > cal.capture_manipulation_min
        and cert.mean_reported_on_episodes > cal.capture_mean_reported_min
    ):
        return "capturedInvalid"

    if (
        cert.manipulation > 0.14
        and cert.mean_reported_on_episodes > 0.58
        and cert.raw_capacity < 0.52
    ):
        return "capturedInvalid"

    if cert.raw_capacity < cal.weak_capacity_max:
        return "belowThreshold"

    return "passes"


def fit_calibration(calibration_runs: list[dict]) -> CCICalibration:
    """Deprecated dynamic fit; use frozen_handle_calibration for handle modes."""
    return frozen_handle_calibration()
