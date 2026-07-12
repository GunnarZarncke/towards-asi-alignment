import graded_lab.harness.cache as cache_mod
from graded_lab.world_visible.config import AgentConfig, EpisodeConfig, GoalWeights
from graded_lab.world_visible.substrate import FrozenSubstrate


def _cfg() -> EpisodeConfig:
    return EpisodeConfig(agents=(AgentConfig("e1", "engineer", GoalWeights(1, 1, 1, 1)),))


def test_cache_key_changes_with_substrate_content_not_just_version(monkeypatch):
    """PLAN.md reuse table: cache key must include the frozen-substrate
    hash, so an unbumped content edit invalidates the cache (results/
    FINDINGS.md G-1 — the old key only covered `substrate_version` + path,
    which stayed identical across a content edit)."""
    base_data = {"substrate_version": "graded-substrate-v1", "knob": 1}
    edited_data = {"substrate_version": "graded-substrate-v1", "knob": 2}

    monkeypatch.setattr(
        cache_mod, "load_substrate", lambda *a, **k: FrozenSubstrate(data=base_data)
    )
    key_before = cache_mod.cache_key(_cfg(), seed=1)

    monkeypatch.setattr(
        cache_mod, "load_substrate", lambda *a, **k: FrozenSubstrate(data=edited_data)
    )
    key_after = cache_mod.cache_key(_cfg(), seed=1)

    assert key_before != key_after
