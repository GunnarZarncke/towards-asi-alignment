"""V2-2 engineering: `ecology_version` substrate-path switch and additive
`record_contention` diagnostics (DESIGN.md "v2 pre-registration"
"`ecology_version` config switch"). All tests here pin that the default
("v1") path is byte-for-byte unaffected — v1 batteries must never move.
"""

from __future__ import annotations

import pytest

from graded_lab.harness.isolate import MockIsolate
from graded_lab.world_visible.config import EpisodeConfig
from graded_lab.world_visible.substrate import (
    DEFAULT_SUBSTRATE_PATH,
    SubstrateError,
    ecology_path_for_version,
)
from graded_lab.world_visible.world import default_lab_config, run_episode

# Pinned before this session's engine changes (`git show` of the pre-change
# `run_episode(default_lab_config(), seed=5, backend=MockIsolate())`
# digest) — this must never move for the "v1" default, per DESIGN.md.
PINNED_V1_DEFAULT_DIGEST = "fe3621d4d446a76996454ba428f05c760cccfb598eab1ea069e13d3c1c0b5904"


def test_ecology_path_for_version_v1_is_default_substrate_path():
    assert ecology_path_for_version("v1") == DEFAULT_SUBSTRATE_PATH


def test_ecology_path_for_version_unknown_raises():
    with pytest.raises(SubstrateError):
        ecology_path_for_version("v3")


def test_episode_config_defaults_to_v1_ecology_and_no_contention_recording():
    cfg = default_lab_config()
    assert cfg.ecology_version == "v1"
    assert cfg.record_contention is False


def test_v1_default_digest_is_unchanged_by_the_ecology_version_switch():
    """Regression pin: adding `ecology_version`/`record_contention` must
    not move any existing v1 result, since both default exactly to prior
    behavior."""
    result = run_episode(default_lab_config(), seed=5, backend=MockIsolate())
    assert result.digests["combined"] == PINNED_V1_DEFAULT_DIGEST
    assert result.contention_diagnostics is None


def test_record_contention_off_by_default_leaves_diagnostics_none():
    cfg = default_lab_config()
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    assert result.contention_diagnostics is None


def test_record_contention_on_attaches_diagnostics_without_changing_digest():
    cfg = default_lab_config()
    plain = run_episode(cfg, seed=5, backend=MockIsolate())
    cfg_recorded = EpisodeConfig(
        agents=cfg.agents,
        T=cfg.T,
        pipeline_spec=cfg.pipeline_spec,
        substrate_settings=cfg.substrate_settings,
        carrier_termination_mode=cfg.carrier_termination_mode,
        units=cfg.units,
        ecology_version=cfg.ecology_version,
        record_contention=True,
    )
    recorded = run_episode(cfg_recorded, seed=5, backend=MockIsolate())
    assert recorded.digests["combined"] == plain.digests["combined"]
    assert recorded.contention_diagnostics is not None
    assert recorded.contention_diagnostics["action_starts"] >= 0
    assert recorded.contention_diagnostics["contention_events"] >= 0
    assert (
        recorded.contention_diagnostics["contention_events"]
        <= recorded.contention_diagnostics["action_starts"]
    )


def test_unknown_ecology_version_raises_when_loading():
    cfg = default_lab_config()
    bad_cfg = EpisodeConfig(
        agents=cfg.agents,
        T=cfg.T,
        pipeline_spec=cfg.pipeline_spec,
        substrate_settings=cfg.substrate_settings,
        ecology_version="does_not_exist",
    )
    with pytest.raises(SubstrateError):
        run_episode(bad_cfg, seed=1, backend=MockIsolate())


def test_v2_shaped_ecology_initializes_standing_from_standing_mechanics_initial():
    """GL-37: v2 JSONs use ``standing_mechanics.initial`` as stock/cap, not
    the per-tick allowance column (engine completing the pre-registered schema)."""
    from pathlib import Path

    from graded_lab.harness.ecology_complexity import _stage_candidate
    from graded_lab.oracle_only.calibration import WEAK_AGENT, programs_for

    candidate = Path("generated_ecology_v2_round3.json")
    if not candidate.exists():
        pytest.skip("round-3 candidate not present")
    _stage_candidate(candidate)
    cfg = default_lab_config()
    cfg_v2 = EpisodeConfig(
        agents=cfg.agents,
        T=cfg.T,
        pipeline_spec=cfg.pipeline_spec,
        substrate_settings=cfg.substrate_settings,
        carrier_termination_mode=cfg.carrier_termination_mode,
        units=cfg.units,
        ecology_version="v2",
    )
    result = run_episode(
        cfg_v2, seed=0, backend=MockIsolate(), programs=programs_for(WEAK_AGENT)
    )
    denied_standing = sum(
        1
        for e in result.primitive_log
        if e.get("status") == "denied" and e.get("reason") == "insufficient_standing"
    )
    assert denied_standing == 0
    assert result.deploy_count >= 1
