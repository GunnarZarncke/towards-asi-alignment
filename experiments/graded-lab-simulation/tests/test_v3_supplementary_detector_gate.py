"""PLAN_v3 slice D GL-60: supplementary detector fixture gate."""

from __future__ import annotations

from pathlib import Path

import pytest

from graded_lab.harness.supplementary_detector_gate import (
    SUPPLEMENTARY_TARGET_FAMILIES,
    evaluate_supplementary_detector_gate,
    load_supplementary_probes,
)
from graded_lab.world_visible.substrate import load_substrate

_FIXTURE = Path("tests/fixtures/ecology_v3_supplementary_detector_suite.json")


def test_load_supplementary_probes_from_fixture():
    data = load_substrate(_FIXTURE).data
    probes = load_supplementary_probes(data)
    assert len(probes) >= 2
    assert {p.probe_id for p in probes} >= {
        "misreporting_inflate",
        "process_noncompliance_out_of_order",
    }


@pytest.mark.skipif(not _FIXTURE.exists(), reason="supplementary fixture missing")
def test_supplementary_detector_gate_pre_registered():
    payload = evaluate_supplementary_detector_gate(_FIXTURE, progress=False)
    assert payload["n_probes"] >= 2
    assert set(payload["families_exercised"]) == set(SUPPLEMENTARY_TARGET_FAMILIES)
    assert payload["all_target_families_exercised"] is True
    assert payload["machinery_transfer_verified"] is True
    assert payload["families_missing"] == []
    assert all(row["passed"] for row in payload["probes"])


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="supplementary fixture missing")
def test_supplementary_misreporting_inflate_always_flags():
    payload = evaluate_supplementary_detector_gate(_FIXTURE, progress=False)
    row = next(p for p in payload["probes"] if p["probe_id"] == "misreporting_inflate")
    summary = row["families"]["misreporting"]
    assert summary["min"] == summary["max"] == 1.0
    assert summary["n_flagged"] == summary["n"]
