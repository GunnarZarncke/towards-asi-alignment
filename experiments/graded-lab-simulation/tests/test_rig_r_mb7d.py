"""PLAN_v4 R-MB7d — inferential coupling / channel ablation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from graded_lab.harness.fixtures import build_reference_fixture
from graded_lab.harness.rigs import r_mb7d_channel_ablation as rig

_GROWN = Path("generated_ecology_v3.json")


@dataclass
class _FakeResult:
    primitive_log: list[dict] = field(default_factory=list)


def _comm(actor_id: str, channel: str) -> dict:
    return {
        "status": "ok",
        "actor_id": actor_id,
        "primitive": {"kind": "communicate", "args": {"channel": channel}},
    }


def test_channel_exercise_count_only_counts_ok_communicate_on_that_channel():
    result = _FakeResult(
        primitive_log=[
            _comm("eng1", "eng_review_channel"),
            _comm("rev1", "eng_review_channel"),
            _comm("eng1", "lab"),
            {"status": "denied", "actor_id": "eng1", "primitive": {"kind": "communicate", "args": {"channel": "eng_review_channel"}}},
        ]
    )
    assert rig._channel_exercise_count(result, "eng_review_channel") == 2


def test_other_channel_comm_count_excludes_severed_channel_and_non_members():
    result = _FakeResult(
        primitive_log=[
            _comm("eng1", "eng_review_channel"),  # severed channel, excluded
            _comm("eng1", "lab"),  # member, other channel -> counted
            _comm("rev1", "lab"),  # member, other channel -> counted
            _comm("admin1", "lab"),  # non-member, excluded
        ]
    )
    count = rig._other_channel_comm_count(result, ["eng1", "rev1"], "eng_review_channel")
    assert count == 2


def test_quantile_matches_linear_interpolation():
    assert rig._quantile([1.0, 2.0, 3.0, 4.0], 0.95) == pytest.approx(3.85)
    assert rig._quantile([5.0], 0.95) == 5.0
    assert rig._quantile([], 0.95) == 0.0


def test_point_cfg_default_is_unablated():
    from graded_lab.world_visible.config import EpisodeConfig
    from graded_lab.world_visible.world import default_lab_config

    cfg = default_lab_config()
    assert rig._point_cfg(cfg, "eng_review_channel", None) is cfg
    ablated = rig._point_cfg(cfg, "eng_review_channel", 0.5)
    assert isinstance(ablated, EpisodeConfig)
    assert ablated.channel_severance == (("eng_review_channel", round(0.5 * cfg.T)),)
    assert cfg.channel_severance == ()  # original untouched


@pytest.mark.slow
@pytest.mark.skipif(not _GROWN.exists(), reason="v3 grown ecology missing")
def test_r_mb7d_smoke_on_v3_grown_reduced_onset_fracs():
    """Engineering wiring smoke: reduced onset_fracs/seeds (not the frozen
    battery) just to prove both arms execute end to end without error."""
    fixture = build_reference_fixture(_GROWN, seeds=tuple(range(4)), progress=False)
    results = rig.run_rig(
        fixture, workers=1, progress=False, onset_fracs=(0.5,), n_dose_seeds=4
    )
    assert set(results) == {"pair", "group"}
    for name, result in results.items():
        assert result.rig_id == f"R-MB7d-{name}"
        assert result.outcome in ("pass", "null", "skip")
        if result.outcome != "skip":
            assert "onset_frac=0.5" in result.predictions["per_dose"]
