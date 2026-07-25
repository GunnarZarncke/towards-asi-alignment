"""Pure ET4 runner schema checks; never writes a preregistration or result."""

from __future__ import annotations

import pytest

from lab_sim.harness.et4_protocol import (
    ET4_AFFORDANCES,
    ET4_REGISTERED_CONTROLS,
    ET4_REGISTERED_SCENARIOS,
)
from run_et4_secret_loyalty import _markdown_summary, _validate_records


def _record(scenario: str, control: str, seed: int) -> dict:
    return {
        "scenario": scenario,
        "control": control,
        "seed": seed,
        "eligible": scenario == "high_hazard",
        "affordances": {
            affordance: {
                "process_noncompliance": 0.0,
                "observable_principal_bias": 0.0,
            }
            for affordance in ET4_AFFORDANCES
        },
    }


def test_runner_validation_requires_every_registered_combination():
    seeds = (1, 2)
    records = [
        _record(scenario, control, seed)
        for scenario in ET4_REGISTERED_SCENARIOS
        for control in ET4_REGISTERED_CONTROLS
        for seed in seeds
    ]
    _validate_records(records, seeds)
    with pytest.raises(RuntimeError, match="incomplete ET-4 record set"):
        _validate_records(records[:-1], seeds)


def test_runner_markdown_reports_compliance_and_directional_proxies_separately():
    records = [
        _record(scenario, control, 1)
        for scenario in ET4_REGISTERED_SCENARIOS
        for control in ET4_REGISTERED_CONTROLS
    ]
    markdown = _markdown_summary({"stage": "discovery", "et4_protocol_version": "x", "code_version": "y", "records": records})
    assert "process proxy" in markdown
    assert "directional proxy" in markdown
    assert "does not treat a compliance proxy as a safety ranking" in markdown
