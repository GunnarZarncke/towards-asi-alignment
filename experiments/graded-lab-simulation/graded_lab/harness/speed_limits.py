"""Pytest duration policy: per-test ceilings and suite regression checks."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_LIMITS = _ROOT / "tests" / "speed_limits.json"
DEFAULT_BASELINE = _ROOT / "tests" / "speed_baseline.json"


@dataclass(frozen=True)
class SpeedLimits:
    suite_max_seconds: float
    fast_suite_max_seconds: float
    default_test_max_seconds: float
    regression_slack_ratio: float
    regression_slack_seconds: float
    per_test_max_seconds: dict[str, float]


def load_limits(path: Path = DEFAULT_LIMITS) -> SpeedLimits:
    data = json.loads(path.read_text(encoding="utf-8"))
    return SpeedLimits(
        suite_max_seconds=float(data["suite_max_seconds"]),
        fast_suite_max_seconds=float(
            data.get("fast_suite_max_seconds", data["suite_max_seconds"])
        ),
        default_test_max_seconds=float(data["default_test_max_seconds"]),
        regression_slack_ratio=float(data.get("regression_slack_ratio", 1.35)),
        regression_slack_seconds=float(data.get("regression_slack_seconds", 0.5)),
        per_test_max_seconds={
            str(key): float(value)
            for key, value in dict(data.get("per_test_max_seconds", {})).items()
        },
    )


def load_baseline(path: Path = DEFAULT_BASELINE) -> dict[str, object]:
    if not path.is_file():
        return {"tests": {}, "suite_total_seconds": 0.0}
    data = json.loads(path.read_text(encoding="utf-8"))
    tests = data.get("tests", {})
    return {
        "generated_on": data.get("generated_on"),
        "tests": {str(k): float(v) for k, v in tests.items()},
        "suite_total_seconds": float(data.get("suite_total_seconds", 0.0)),
    }


def save_baseline(
    durations: dict[str, float],
    *,
    path: Path = DEFAULT_BASELINE,
) -> dict[str, object]:
    from datetime import datetime, timezone

    payload = {
        "generated_on": datetime.now(timezone.utc).isoformat(),
        "tests": {key: round(value, 4) for key, value in sorted(durations.items())},
        "suite_total_seconds": round(sum(durations.values()), 4),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def check_speeds(
    durations: dict[str, float],
    limits: SpeedLimits,
    baseline: dict[str, object],
    *,
    suite_cap: float | None = None,
) -> list[str]:
    """Return human-readable violations (empty if within policy)."""
    violations: list[str] = []
    suite_total = sum(durations.values())
    cap = limits.suite_max_seconds if suite_cap is None else suite_cap
    if suite_total > cap:
        violations.append(
            f"suite total {suite_total:.2f}s exceeds limit {cap:.2f}s"
        )

    for nodeid, duration in sorted(durations.items()):
        hard = limits.per_test_max_seconds.get(
            nodeid, limits.default_test_max_seconds
        )
        if duration > hard:
            violations.append(
                f"{nodeid}: {duration:.2f}s exceeds hard cap {hard:.2f}s "
                "(new or unexpectedly slow test)"
            )
            continue

        recorded = dict(baseline.get("tests", {})).get(nodeid)
        if recorded is None:
            continue
        regression_cap = (
            float(recorded) * limits.regression_slack_ratio
            + limits.regression_slack_seconds
        )
        if duration > regression_cap:
            violations.append(
                f"{nodeid}: {duration:.2f}s exceeds regression cap "
                f"{regression_cap:.2f}s (baseline {float(recorded):.2f}s)"
            )
    return violations
