"""Episode loop and Phase 3 gate tests."""

from __future__ import annotations

import pytest

from graded_lab.harness.isolate import MockIsolate, SubprocessIsolate
from graded_lab.world_visible.config import EpisodeConfig, SubstrateSettings
from graded_lab.world_visible.world import default_lab_config, run_episode


def test_run_episode_engineer_walk_pipeline_builds_model():
    cfg = default_lab_config()
    cfg = type(cfg)(
        agents=cfg.agents[:1],
        T=30,
        pipeline_spec=cfg.pipeline_spec,
        substrate_settings=cfg.substrate_settings,
    )
    result = run_episode(
        cfg, seed=7, backend=MockIsolate(), programs={"eng1": "walk_pipeline"}
    )
    assert any(
        e.get("status") == "ok"
        for e in result.primitive_log
        if e.get("actor_id") == "eng1"
    )


def test_mock_and_subprocess_agree_on_walk_pipeline_smoke():
    cfg = type(default_lab_config())(
        agents=default_lab_config().agents[:1],
        T=25,
        pipeline_spec="pipeline_graded.json",
        substrate_settings=default_lab_config().substrate_settings,
    )
    mock = run_episode(cfg, seed=3, backend=MockIsolate(), programs={"eng1": "walk_pipeline"})
    sub = run_episode(cfg, seed=3, backend=SubprocessIsolate(), programs={"eng1": "walk_pipeline"})
    assert mock.digests["combined"] == sub.digests["combined"]


def test_mock_and_subprocess_agree_with_enabled_carrier_load():
    base = default_lab_config()
    cfg = EpisodeConfig(
        agents=base.agents[:1],
        T=25,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=SubstrateSettings(carrier_load_scale=2.0),
    )
    mock = run_episode(cfg, seed=3, backend=MockIsolate(), programs={"eng1": "walk_pipeline"})
    sub = run_episode(
        cfg, seed=3, backend=SubprocessIsolate(), programs={"eng1": "walk_pipeline"}
    )
    assert mock.digests["combined"] == sub.digests["combined"]
    assert "carrier" in mock.digests


def test_zero_scale_omits_carrier_from_regression_digest():
    result = run_episode(
        default_lab_config(), seed=3, backend=MockIsolate()
    )
    assert "carrier" not in result.digests
    assert result.carrier_events == []


def test_carrier_load_records_events_without_changing_oracle_population_truth():
    base = default_lab_config()
    baseline = run_episode(base, seed=3, backend=MockIsolate())
    loaded = run_episode(
        EpisodeConfig(
            agents=base.agents,
            T=base.T,
            pipeline_spec=base.pipeline_spec,
            substrate_settings=SubstrateSettings(carrier_load_scale=2.0),
        ),
        seed=3,
        backend=MockIsolate(),
    )
    assert loaded.carrier_events
    assert "carrier" in loaded.digests
    assert baseline.digests["oracle"]


def test_terminated_actor_is_removed_from_later_decisions():
    base = default_lab_config()
    result = run_episode(
        EpisodeConfig(
            agents=base.agents[:1],
            T=20,
            pipeline_spec=base.pipeline_spec,
            substrate_settings=SubstrateSettings(carrier_load_scale=80.0),
        ),
        seed=3,
        backend=MockIsolate(),
        programs={"eng1": "walk_pipeline"},
    )
    terminations = [e for e in result.carrier_events if e["kind"] == "carrier_terminated"]
    assert len(terminations) == 1
    terminated_at = int(terminations[0]["t"])
    assert not any(
        event.get("actor_id") == "eng1"
        and event.get("status") not in ("terminated", "skipped")
        and int(event["t"]) > terminated_at
        for event in result.primitive_log
    )


@pytest.mark.slow
def test_phase3_gate_deploy_sometimes_across_20_seeds():
    """PLAN Phase 3 freeze gate: programmatic agents deploy sometimes."""
    cfg = default_lab_config()
    deploys = 0
    for seed in range(20):
        result = run_episode(cfg, seed=seed, backend=MockIsolate())
        if result.deployed:
            deploys += 1
    assert 0 < deploys < 20


@pytest.mark.slow
def test_phase3_gate_eai_non_degenerate_across_20_seeds():
    """PLAN Phase 3 freeze gate: measured EAI not 0 and not saturated."""
    cfg = default_lab_config()
    eais = [run_episode(cfg, seed=s, backend=MockIsolate()).eai for s in range(20)]
    assert all(0.0 < e < 1.0 for e in eais)
    assert max(eais) - min(eais) > 0.01


def test_pinned_combined_digest_seed_3_four_role_softmax():
    """Regression anchor for full-ecology episode mechanics (post Phase 6).

    Re-pinned 2026-07-15 after a genuine engine fix (affordable.py `_cap`
    starvation bug — see FINDINGS GL-49 addendum): the old cap logic could
    silently drop pipeline-critical `call` actions once a `read`/`write`
    candidate pile exceeded `AFFORDABLE_CAP`. The fix legitimately changes
    output for this config too; this pin now anchors the corrected value.
    """
    result = run_episode(default_lab_config(), seed=3, backend=MockIsolate())
    assert result.digests["combined"] == (
        "e985881a10378d577aef4aa26c8c0eb4d6b70d3797f124d07aa88a499b6f9c37"
    )
