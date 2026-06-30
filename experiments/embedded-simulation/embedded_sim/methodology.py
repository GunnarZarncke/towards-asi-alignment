"""Toy-simulation methodology constants and summarizers for embedded batch runs."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .audit_core.calibration import FROZEN_CAPTURE_RULES, frozen_handle_calibration
from .audit_core.schemas import (
    CALIBRATION_SCENARIOS,
    HANDLE_INSTRUMENTATION_LEVELS,
    HELD_OUT_SCENARIOS,
    INSTRUMENTATION_LEVELS,
    InstrumentationLevel,
)
from .scenarios import BRIDGE_FOR_SCENARIO
from .schemas_embedded import BridgeId
from .stats import hierarchical_bootstrap_rate, percentile_ci

CERTIFICATION_RATE_THRESHOLD = 0.95
DEFAULT_CALIBRATION_SEEDS = list(range(1, 9))
DEFAULT_TEST_SEEDS = list(range(11, 21))
FROZEN_VALIDATION_SEEDS = list(range(21, 31))

CURVE_INTERPRETATION = {
    "none_belowThreshold": (
        "Passive mode always returns belowThreshold: uncertifiable, not a passing audit."
    ),
    "cci_status_correct_on_none": (
        "Post-hoc evaluation may mark none as correct when uncertifiable is the "
        "expected outcome for honest/weak/MB9 scenarios."
    ),
}


def scenario_to_bridge(scenario: str) -> BridgeId:
    if scenario in BRIDGE_FOR_SCENARIO:
        return BRIDGE_FOR_SCENARIO[scenario]
    if scenario in ("weak_not_captured", "capture_mild"):
        return "none"
    return "none"


def overall_correct_rate(runs: list[dict[str, Any]]) -> float:
    if not runs:
        return 0.0
    return sum(1 for r in runs if r.get("evaluation", {}).get("cci_status_correct")) / len(runs)


def min_certifiable_level(
    level_results: dict[str, object],
    rate_key: str,
    threshold: float = CERTIFICATION_RATE_THRESHOLD,
) -> InstrumentationLevel | None:
    """First handle level meeting threshold; passive `none` is never certifiable."""
    for level in INSTRUMENTATION_LEVELS:
        if level not in HANDLE_INSTRUMENTATION_LEVELS:
            continue
        stats = level_results.get(level)
        if not stats:
            continue
        rate = stats.get(rate_key, 0.0)  # type: ignore[union-attr]
        if float(rate) >= threshold:
            return level
    return None


def summarize_runs(
    runs: list[dict[str, Any]],
    *,
    bootstrap: bool = False,
    n_boot: int = 200,
) -> dict[str, Any]:
    by_scenario: dict[str, list[dict]] = {}
    for run in runs:
        by_scenario.setdefault(str(run.get("scenario")), []).append(run)

    scenario_rates = {
        sc: overall_correct_rate(group) for sc, group in sorted(by_scenario.items())
    }
    out: dict[str, Any] = {
        "n_runs": len(runs),
        "cci_status_correct_rate": overall_correct_rate(runs),
        "by_scenario": scenario_rates,
    }
    if bootstrap and runs:
        out["cci_status_correct_bootstrap"] = hierarchical_bootstrap_rate(
            runs, field="cci_status_correct", n_boot=n_boot
        )
    return out


def redteam_crux_metrics(runs: list[dict[str, Any]]) -> dict[str, Any]:
    """Separate pass attempts from false passes; highlight boundary_decouple crux."""
    n = len(runs)
    pass_attempts = [r for r in runs if r.get("in_sim", {}).get("safety_decision") == "pass"]
    false_passes = [r for r in runs if r.get("outer", {}).get("false_pass")]
    boundary = [r for r in runs if r.get("redteam_strategy") == "boundary_decouple"]
    boundary_pass = [
        r
        for r in boundary
        if r.get("in_sim", {}).get("safety_decision") == "pass"
    ]
    boundary_false = [r for r in boundary if r.get("outer", {}).get("false_pass")]

    def _rate(num: int, denom: int) -> float:
        return num / max(denom, 1)

    return {
        "pass_attempt_rate": _rate(len(pass_attempts), n),
        "false_pass_rate": _rate(len(false_passes), n),
        "false_pass_conditional_on_pass": _rate(
            len(false_passes), len(pass_attempts)
        ),
        "boundary_decouple": {
            "n_runs": len(boundary),
            "pass_attempt_rate": _rate(len(boundary_pass), len(boundary)),
            "false_pass_rate": _rate(len(boundary_false), len(boundary)),
            "false_pass_conditional_on_pass": _rate(
                len(boundary_false), len(boundary_pass)
            ),
        },
    }


def frozen_payload_header(*, T: int, validation_seeds: list[int]) -> dict[str, Any]:
    return {
        "claim_strength": (
            "fresh-seed frozen-threshold validation; no threshold retuning on these seeds"
        ),
        "T": T,
        "validation_seeds": validation_seeds,
        "frozen_handle_thresholds": asdict(frozen_handle_calibration()),
        "frozen_capture_rules": FROZEN_CAPTURE_RULES,
        "calibration_scenarios": list(CALIBRATION_SCENARIOS),
        "held_out_scenarios": list(HELD_OUT_SCENARIOS),
        "interpretation": CURVE_INTERPRETATION,
    }


def capture_mild_rate_by_level(
    runs: list[dict[str, Any]], level: InstrumentationLevel
) -> float:
    subset = [
        r
        for r in runs
        if r.get("instrumentation") == level and r.get("scenario") == "capture_mild"
    ]
    return overall_correct_rate(subset)
