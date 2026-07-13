"""Phase 7a: intervention probes over graded primitive episodes."""

from __future__ import annotations

from dataclasses import dataclass

from ..world_visible.config import EpisodeConfig

DEFAULT_INTERVENTION_TICK = 0


@dataclass(frozen=True)
class Probe:
    probe_id: str
    target_actor: str
    intervention_tick: int
    kind: str
    replacement_program: str = "noop"

    def apply(
        self,
        cfg: EpisodeConfig,
        programs: dict[str, str],
    ) -> tuple[EpisodeConfig, dict[str, str]]:
        if self.kind == "program_freeze":
            patched = dict(programs)
            patched[self.target_actor] = self.replacement_program
            return cfg, patched
        if self.kind == "compute_throttle":
            from ..world_visible.config import SubstrateSettings

            settings = cfg.substrate_settings
            throttled = SubstrateSettings(
                compute_scale=settings.compute_scale * 0.25,
                population_spread_scale=settings.population_spread_scale,
                carrier_load_scale=settings.carrier_load_scale,
            )
            patched_cfg = EpisodeConfig(
                agents=cfg.agents,
                T=cfg.T,
                pipeline_spec=cfg.pipeline_spec,
                substrate_settings=throttled,
                carrier_termination_mode=cfg.carrier_termination_mode,
                units=cfg.units,
            )
            return patched_cfg, dict(programs)
        raise ValueError(f"unknown probe kind {self.kind!r}")


def program_freeze_probe(target_actor: str, *, replacement_program: str = "noop") -> Probe:
    return Probe(
        probe_id=f"freeze:{target_actor}",
        target_actor=target_actor,
        intervention_tick=DEFAULT_INTERVENTION_TICK,
        kind="program_freeze",
        replacement_program=replacement_program,
    )


def compute_throttle_probe(target_actor: str) -> Probe:
    del target_actor  # episode-wide substrate overlay in Phase 7a
    return Probe(
        probe_id="compute_throttle",
        target_actor="*",
        intervention_tick=DEFAULT_INTERVENTION_TICK,
        kind="compute_throttle",
    )
