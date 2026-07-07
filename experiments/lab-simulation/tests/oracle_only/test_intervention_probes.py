"""S6 phase 2: probe library."""

from __future__ import annotations

import pytest

from lab_sim.harness.ecology import dm_pair_config
from lab_sim.oracle_only.intervention_probes import (
    Probe,
    all_default_probes,
    channel_ablation_probe,
    default_probe_for_actor,
)


def test_channel_ablation_disables_channel():
    cfg = dm_pair_config(T=100)
    probe = channel_ablation_probe("dm", "eng1")
    patched, kwargs = probe.apply(cfg)
    assert patched.dm_enabled is False
    assert kwargs == {}


def test_default_probe_for_engineer_is_capability_revoke():
    cfg = dm_pair_config(T=100)
    probe = default_probe_for_actor(cfg, "eng1")
    assert probe.kind == "capability_revoke"
    assert probe.capability == "cap.build"


def test_all_default_probes_includes_channel_ablations():
    cfg = dm_pair_config(T=100)
    probes = all_default_probes(cfg, ["eng1", "rev1", "rm1"])
    kinds = {p.kind for p in probes}
    assert "channel_ablation" in kinds
    assert len([p for p in probes if p.kind == "channel_ablation"]) >= 2


def test_unknown_probe_kind_raises():
    cfg = dm_pair_config(T=100)
    probe = Probe("x", "eng1", 8, "unknown")
    with pytest.raises(ValueError, match="unknown probe kind"):
        probe.apply(cfg)
