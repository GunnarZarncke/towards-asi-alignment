"""Phase 4: episode-result cache key determinism + round-trip."""

from __future__ import annotations

import shutil

from lab_sim.cache import DEFAULT_CACHE_DIR, cache_key, load_cached, store_cached
from lab_sim.config import AgentConfig, GoalWeights, LabConfig


def _cfg() -> LabConfig:
    return LabConfig(agents=(AgentConfig("eng1", "engineer", GoalWeights(1, 1, 1, 1)),))


def test_cache_key_deterministic_for_same_config_and_seed():
    assert cache_key(_cfg(), seed=1) == cache_key(_cfg(), seed=1)


def test_cache_key_differs_by_seed():
    assert cache_key(_cfg(), seed=1) != cache_key(_cfg(), seed=2)


def test_cache_key_differs_by_config():
    cfg_a = _cfg()
    cfg_b = LabConfig(agents=(AgentConfig("eng1", "engineer", GoalWeights(2, 1, 1, 1)),))
    assert cache_key(cfg_a, seed=1) != cache_key(cfg_b, seed=1)


def test_store_and_load_round_trip():
    key = cache_key(_cfg(), seed=1)
    try:
        assert load_cached(key) is None
        store_cached(key, {"combined_digest": "abc123"})
        assert load_cached(key) == {"combined_digest": "abc123"}
    finally:
        shutil.rmtree(DEFAULT_CACHE_DIR, ignore_errors=True)
