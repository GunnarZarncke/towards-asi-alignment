#!/usr/bin/env python3
"""Regression smoke for ResourceGovernor (adapt_workers / max_workers)."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from multiresolution_alignment_sim.resources import ResourceGovernor, ResourceSnapshot


def _assert_int_workers(gov: ResourceGovernor, label: str) -> None:
    cap = gov.max_workers()
    assert isinstance(cap, int), f"{label}: max_workers() must return int, got {type(cap)}"
    w = gov.adapt_workers()
    assert isinstance(w, int), f"{label}: adapt_workers() must return int, got {type(w)}"
    assert 1 <= w <= cap, f"{label}: workers {w} not in [1, {cap}]"


def main() -> None:
    gov = ResourceGovernor(workers=4, cpu_target=0.80, throttle_enabled=True)
    _assert_int_workers(gov, "live snapshot")

    low = ResourceSnapshot(
        cpu_percent=10.0, gpu_percent=None, gpu_available=False, cpu_cores=8, workers=2
    )
    high = ResourceSnapshot(
        cpu_percent=95.0, gpu_percent=None, gpu_available=False, cpu_cores=8, workers=4
    )

    with patch.object(ResourceGovernor, "snapshot", return_value=low):
        gov.workers = 2
        before = gov.workers
        w = gov.adapt_workers()
        assert isinstance(w, int) and w >= before, "should scale up on low CPU"

    with patch.object(ResourceGovernor, "snapshot", return_value=high):
        gov.workers = 4
        w = gov.adapt_workers()
        assert w == 3, f"expected workers 3 after high CPU, got {w}"

    gov_off = ResourceGovernor(workers=5, throttle_enabled=False)
    assert gov_off.adapt_workers() == 5

    print("smoke_governor: OK")


if __name__ == "__main__":
    main()
