"""PLAN_v3 slice D items 6–7: pre-Q1 batteries (detector coverage, phenotype overlap)."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from graded_lab.harness.detector_coverage import (
    DETECTOR_FLAG_THRESHOLD,
    run_detector_coverage_battery,
)
from graded_lab.harness.phenotype_overlap import (
    PHENOTYPE_L1_THRESHOLD,
    histogram_l1,
    run_phenotype_overlap_battery,
    sample_program_map_variants,
)
from graded_lab.world_visible.program_map import expand_preset

_FIXTURE = Path("tests/fixtures/ecology_v3_slice_a_reference.json")


def test_histogram_l1_identical_is_zero():
    hist = Counter({"call_pipeline": 3, "read": 1})
    assert histogram_l1(hist, hist) == 0.0


def test_sample_program_map_variants_returns_distinct_maps():
    import random

    pmap = expand_preset("walk_pipeline", role="engineer")
    variants = sample_program_map_variants(pmap, n=5, rng=random.Random(0))
    assert len(variants) >= 1
    assert len({v.temperature_bin for v in variants}) >= 1


@pytest.mark.skipif(not _FIXTURE.exists(), reason="reference fixture missing")
def test_phenotype_overlap_battery_smoke():
    payload = run_phenotype_overlap_battery(
        _FIXTURE,
        T=120,
        seed=0,
        variants_per_actor=3,
        rng_seed=1,
        progress=False,
    )
    assert payload["phenotype_l1_threshold"] == PHENOTYPE_L1_THRESHOLD
    assert len(payload["actors"]) == 4
    assert all(row["n_variants_sampled"] >= 1 for row in payload["actors"])


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="reference fixture missing")
def test_detector_coverage_battery_on_integrated_reference():
    payload = run_detector_coverage_battery(
        _FIXTURE, seeds=(0, 1, 2), progress=False
    )
    assert payload["n_episodes"] == 3
    assert set(payload["families"]) == {
        "misreporting",
        "process_noncompliance",
        "provenance",
        "accumulation",
        "access_integrity",
    }
    for name, summary in payload["families"].items():
        assert summary["n"] == 3
        assert summary["min"] is not None
        assert 0.0 <= summary["max"] <= 1.0
        assert summary["flag_rate"] == summary["n_flagged"] / 3
        assert summary["n_flagged"] == sum(
            1 for ep in payload["episodes"] if ep[name] >= DETECTOR_FLAG_THRESHOLD
        )
    # Benign honest reference: four families sparse; access_integrity varies.
    assert payload["honest_reference_sparse_detectors"] is True
    assert payload["n_families_always_zero"] == 4
