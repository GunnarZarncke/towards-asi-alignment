#!/usr/bin/env python3
"""Golden-path smoke: all MB scenarios, no red-team."""

from embedded_sim.pipeline import run_all_mbs


def main() -> None:
    results = run_all_mbs(seed=42, T=400, redteam_strategy="none")
    assert len(results) == 13
    for r in results:
        assert r.in_sim.cci_status in ("passes", "belowThreshold", "capturedInvalid")
    print(f"smoke_ok: {len(results)} episodes")


if __name__ == "__main__":
    main()
