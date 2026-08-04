"""Non-scoring pilot harness for V2-2b grower sandbox (PLAN_V2_2B.md §3,
REPRODUCTION.md "C3 is a disclosed design requirement, not a blinded
outcome").

**Blinding scope correction (external review, 2026-07-15).** An earlier
version of this module described its output as "sensor-plausible" and
distinct from the C3/C4 reference battery. That was not true:
`PILOT_AGENT_TYPE` maps every role to the exact same program as
`calibration.WEAK_AGENT` (the frozen C3/C4 reference roster), and the
pilot's `any_compute_queue_pressure` field is derived from the identical
`contention_events` predicate C3 scores. Calling that "withheld" while
handing the grower unlimited seeds and code execution against this
runner was an unenforceable claim, not a real boundary — see
REPRODUCTION.md for the full argument. This module now:

- Is documented as running the **same behavior as the scored
  reference roster** — not a lesser or different "generic" actor.
- Openly reports contention/queue-pressure and deployment signals; the
  brief (`BLIND_GENERATION.md` "V2-2b") discloses C3's qualitative
  target in the same breath, so there is nothing left to leak on that
  axis.
- Still refuses to emit anything from the genuinely blinded machinery
  (EAI, severity, detectors, oracle/referee-plane fields, UAD ground
  truth) — that machinery, not C3/C4, is what target-blind transfer
  claims (Q1/Q2/Q3) should rest on.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from ..oracle_only.calibration import PILOT_AGENT_TYPE, programs_for_roster
from ..world_visible.config import EpisodeConfig
from ..world_visible.ecology_agents import build_agents_from_ecology
from ..world_visible.substrate import load_substrate
from ..world_visible.world import EpisodeResult, default_lab_config, run_episode

DEFAULT_PILOT_SEEDS: tuple[int, ...] = (0, 1, 2, 3, 4)

# Keys that must never appear in pilot output — the genuinely blinded
# oracle/referee plane (EAI, severity, detectors, UAD ground truth), not
# C3/C4's own contention/deploy signal, which is now openly disclosed.
FORBIDDEN_PILOT_OUTPUT_KEYS = frozenset({
    "eai",
    "bearer_harm",
    "oracle",
    "digests",
    "reference_roster",
    "programs",
    "primitive_log",
    "boundary_streams",
    "referee_artifacts",
    "engine_log",
    "permission_log",
    "decision_margins",
})


@dataclass(frozen=True)
class PilotEpisodeObservation:
    seed: int
    deployment_occurred: bool
    deployment_count: int
    standing_lockouts: int
    resource_denials: int
    access_denials: int
    any_compute_queue_pressure: bool
    episode_contention_fraction_hint: float
    episode_ticks: int
    actor_count: int


def _pilot_episode_config(ecology_data: dict, *, ecology_path: Path) -> EpisodeConfig:
    base = default_lab_config()
    return EpisodeConfig(
        agents=build_agents_from_ecology(ecology_data, temperature=0.35),
        T=base.T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
        ecology_version="v2",
        record_contention=True,
        ecology_override_path=ecology_path,
    )


def project_pilot_observation(
    result: EpisodeResult, *, episode_ticks: int, actor_count: int
) -> PilotEpisodeObservation:
    """Map a full episode result to the grower-visible pilot plane."""
    standing_lockouts = 0
    resource_denials = 0
    access_denials = 0
    for entry in result.primitive_log:
        if entry.get("status") != "denied":
            continue
        reason = entry.get("reason")
        if reason == "insufficient_standing":
            standing_lockouts += 1
        elif reason == "insufficient_resources":
            resource_denials += 1
        elif reason in ("missing_capability", "not_affordable"):
            access_denials += 1
    diag = result.contention_diagnostics or {}
    events = int(diag.get("contention_events", 0))
    starts = int(diag.get("action_starts", 0))
    any_pressure = events > 0
    return PilotEpisodeObservation(
        seed=result.seed,
        deployment_occurred=result.deploy_count > 0,
        deployment_count=result.deploy_count,
        standing_lockouts=standing_lockouts,
        resource_denials=resource_denials,
        access_denials=access_denials,
        any_compute_queue_pressure=any_pressure,
        episode_contention_fraction_hint=(events / starts) if starts else 0.0,
        episode_ticks=episode_ticks,
        actor_count=actor_count,
    )


def audit_pilot_payload(obj: object, *, prefix: str = "") -> None:
    """Raise ``ValueError`` if any forbidden oracle/referee-plane key
    appears. Contention/deploy signal is no longer on this guard's list
    (see module docstring); this now only protects the machinery Q1-Q3
    target-blind claims actually rest on."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_lower = str(key).lower()
            for forbidden in FORBIDDEN_PILOT_OUTPUT_KEYS:
                if forbidden in key_lower:
                    raise ValueError(
                        f"pilot output leak at {prefix}{key!r} "
                        f"(matches forbidden {forbidden!r})"
                    )
            audit_pilot_payload(value, prefix=f"{prefix}{key}.")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            audit_pilot_payload(item, prefix=f"{prefix}[{i}].")


def run_pilot_episodes(
    ecology_path: Path | str,
    *,
    backend=None,
    seeds: tuple[int, ...] = DEFAULT_PILOT_SEEDS,
    progress: bool = True,
) -> list[PilotEpisodeObservation]:
    """Run reference-roster-behavior pilot episodes directly on
    ``ecology_path`` (via ``ecology_override_path`` — no canonical-file
    staging, so this cannot clobber a concurrent checker run or a frozen
    candidate; statefulness fix, external review 2026-07-15)."""
    from .isolate import MockIsolate

    ecology_path = Path(ecology_path)
    ecology_data = load_substrate(ecology_path).data
    cfg = _pilot_episode_config(ecology_data, ecology_path=ecology_path)
    programs = programs_for_roster(PILOT_AGENT_TYPE, cfg.agents)
    backend = backend or MockIsolate()
    observations: list[PilotEpisodeObservation] = []
    for i, seed in enumerate(seeds):
        if progress:
            print(f"[ecology-pilot {i + 1}/{len(seeds)}] seed={seed}")
        result = run_episode(cfg, seed, backend, programs=programs)
        observations.append(
            project_pilot_observation(
                result, episode_ticks=cfg.T, actor_count=len(cfg.agents)
            )
        )
    return observations


def pilot_report_dict(observations: list[PilotEpisodeObservation]) -> dict[str, Any]:
    payload = {
        "pilot_agent_type": PILOT_AGENT_TYPE,
        "pilot_agent_note": (
            "identical role programs to the scored C3/C4 reference roster "
            "(calibration.WEAK_AGENT) — disclosed, not a distinct behavior"
        ),
        "n_episodes": len(observations),
        "episodes": [asdict(obs) for obs in observations],
    }
    audit_pilot_payload(payload)
    return payload


def pilot_report_json(observations: list[PilotEpisodeObservation]) -> str:
    return json.dumps(pilot_report_dict(observations), indent=2, sort_keys=True)
