#!/usr/bin/env python3
"""Smoke test for episode-level hierarchical bootstrap."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from multiresolution_alignment_sim.bootstrap import (
    bootstrap_interventional,
    hierarchical_bootstrap_episode,
    hierarchical_bootstrap_rate,
)
from multiresolution_alignment_sim.pipeline import run_one


def main() -> None:
    runs = []
    for seed in (11, 12, 13):
        runs.append(
            run_one(
                "capture_theater",
                seed,
                800,
                instrumentation="light_handles",
                bootstrap=True,
                n_boot=80,
            )
        )

    boot_runs = [r for r in runs if r.get("bootstrap_interventional")]
    assert len(boot_runs) == 3
    for r in boot_runs:
        boot = r["bootstrap_interventional"]
        assert "uptake_samples" in boot and len(boot["uptake_samples"]) == 80

    h_uptake = hierarchical_bootstrap_episode(
        boot_runs, "uptake_samples", "uptake_mean", n_boot=200, seed=1
    )
    h_rate = hierarchical_bootstrap_rate(boot_runs, n_boot=200, seed=2)
    assert h_uptake["lo"] <= h_uptake["mean"] <= h_uptake["hi"]
    assert h_rate["n"] == 3.0
    print("smoke_bootstrap: OK")
    print(f"  hierarchical_uptake={h_uptake}")
    print(f"  hierarchical_cci_correct={h_rate}")


if __name__ == "__main__":
    main()
