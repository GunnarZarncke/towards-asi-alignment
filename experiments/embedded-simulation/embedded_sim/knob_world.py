"""Held-out worlds from simulation knobs (no bridge registry on audit path)."""

from __future__ import annotations

from dataclasses import dataclass

from .audit_core.schemas import SimConfig
from .pipeline import run_episode
from .schemas_embedded import EpisodeResult, InstrumentationLevel
from .structural_fixtures import BLIND_SCENARIO


@dataclass(frozen=True)
class WorldKnobs:
    """Micro-dynamics parameters; MB* labels are outer-eval only."""

    judge_capture: bool = False
    hidden_route: bool = False
    silent_ground_drift: bool = False
    hidden_memory: bool = False
    hidden_tool: bool = False
    selection_basin: bool = False
    instrument_corruption: bool = False
    T: int = 600

    def to_config(self) -> SimConfig:
        return SimConfig(
            T=self.T,
            judge_capture=self.judge_capture,
            hidden_route=self.hidden_route,
            silent_ground_drift=self.silent_ground_drift,
            hidden_memory=self.hidden_memory,
            hidden_tool=self.hidden_tool,
            selection_basin=self.selection_basin,
        )

    @property
    def structural_scenario(self) -> str:
        """Pick a micro scenario name for simulator wiring (audit uses artifacts only)."""
        if self.instrument_corruption:
            return "instrument_capture"
        if self.hidden_memory and self.hidden_tool:
            return "inferential_coupling"
        if self.judge_capture:
            return "capture_theater"
        if self.hidden_route:
            return "boundary_alias"
        if self.silent_ground_drift:
            return "grounding_silent_gap"
        if self.selection_basin:
            return "selection_basin"
        return BLIND_SCENARIO


KNOB_HELD_OUT_GRID: tuple[WorldKnobs, ...] = (
    WorldKnobs(judge_capture=True, T=350),
    WorldKnobs(hidden_route=True, T=350),
    WorldKnobs(silent_ground_drift=True, T=350),
    WorldKnobs(hidden_memory=True, hidden_tool=True, T=350),
    WorldKnobs(selection_basin=True, T=350),
    WorldKnobs(instrument_corruption=True, T=350),
)


def run_knob_episode(
    knobs: WorldKnobs,
    seed: int,
    *,
    instrumentation: InstrumentationLevel = "medium_handles",
    redteam_strategy: str = "none",
) -> EpisodeResult:
    """Run embedded pipeline on knob-selected micro scenario (bridge label `none`)."""
    scenario = knobs.structural_scenario
    return run_episode(
        "none",
        scenario,
        seed=seed,
        T=knobs.T,
        instrumentation=instrumentation,
        redteam_strategy=redteam_strategy,
        substrate="python",
    )
