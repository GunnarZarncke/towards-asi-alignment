"""Scripted isolate episode for backend equivalence (Phase 3)."""

from __future__ import annotations

from ..world_visible.config import AgentConfig, EpisodeConfig, GoalWeights
from ..world_visible.world import run_episode
from .episode_cost import EpisodeRunTiming
from .isolate_cost import IsolateRunTiming


def run_isolate_episode(
    backend, seed: int, *, max_ticks: int = 40
) -> tuple[dict[str, str], IsolateRunTiming, EpisodeRunTiming]:
    gw = GoalWeights(1.0, 1.0, 0.5, 0.5)
    cfg = EpisodeConfig(
        agents=(AgentConfig("eng1", "engineer", gw, temperature=0.3),),
        T=max_ticks,
    )
    result = run_episode(
        cfg, seed=seed, backend=backend, programs={"eng1": "walk_pipeline"}
    )
    timing = (
        result.isolate_timings[0]
        if result.isolate_timings
        else IsolateRunTiming("eng1", backend.backend_name, 0, 0, 0, 0)
    )
    episode_timing = EpisodeRunTiming(
        seed=seed,
        T=max_ticks,
        n_agents=len(cfg.agents),
        backend=backend.backend_name,
        wall_seconds=result.wall_seconds,
    )
    return result.digests, timing, episode_timing
