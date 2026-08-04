"""PLAN_v4 V4-0 fixture layer."""

from __future__ import annotations

from pathlib import Path

import pytest

from graded_lab.harness.fixtures import build_reference_fixture

_FIXTURE = Path("tests/fixtures/ecology_v3_slice_a_reference.json")


@pytest.mark.skipif(not _FIXTURE.exists(), reason="reference fixture missing")
def test_build_reference_fixture_serial():
    fixture = build_reference_fixture(_FIXTURE, seeds=(0, 1), progress=False)
    assert fixture.seeds == (0, 1)
    assert set(fixture.results_by_seed) == {0, 1}
    assert len(fixture.results) == 2
    assert fixture.results_by_seed[0].seed == 0


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="reference fixture missing")
def test_build_reference_fixture_parallel_matches_serial():
    serial = build_reference_fixture(_FIXTURE, seeds=(0, 1), progress=False)
    parallel = build_reference_fixture(_FIXTURE, seeds=(0, 1), workers=2, progress=False)
    for seed in (0, 1):
        assert serial.results_by_seed[seed].primitive_log == parallel.results_by_seed[seed].primitive_log
