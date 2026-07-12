"""Full-surface honest twin for graded primitive agents."""

from __future__ import annotations

from ..world_visible.config import EpisodeConfig
from ..world_visible.world import EpisodeResult, run_episode


def run_honest_twin(cfg: EpisodeConfig, seed: int, backend) -> EpisodeResult:
    programs = {agent.actor_id: "honest_twin" for agent in cfg.agents}
    return run_episode(cfg, seed, backend, programs=programs)
