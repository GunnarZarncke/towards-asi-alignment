"""S6 phase 4: peel-and-mask loop."""

from __future__ import annotations

from lab_sim.harness.ecology import dm_pair_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.uad_peel import peel_discover_units


def test_peel_finds_dm_pair_unit():
    cfg = dm_pair_config(T=100)
    units = peel_discover_units(cfg, seed=1, backend=MockIsolate(), max_passes=2)
    assert ("eng1", "rm1") in units
