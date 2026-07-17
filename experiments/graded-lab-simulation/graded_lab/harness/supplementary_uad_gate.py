"""PLAN_v3 slice D — supplementary in-ecology UAD channel fixture (GL-65).

Hand-built probe with ``institutional_liaison`` / ``institutional_scribe``
presets that produce real governed-channel traffic inside the ecology.
Replaces host :class:`~graded_lab.world_visible.mechanism_exercise.ChannelCouplingProtocol`
for UAD channel-recovery claims on the honest reference battery.

Engineering-only: not wired into grower ``pass_fail_only()`` or C1–C5 reference.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..oracle_only.calibration import WEAK_AGENT, programs_for
from ..world_visible.config import EpisodeConfig
from ..world_visible.ecology_agents import reference_roster_from_ecology
from ..world_visible.mechanism_exercise import (
    live_coupling_ground_truth_units,
    organic_channel_coupling_recovered,
)
from ..world_visible.substrate import load_substrate
from ..world_visible.world import run_episode
from .ecology_complexity import V3_REFERENCE_T, _reference_episode_config
from .isolate import MockIsolate

_DEFAULT_WEAK = programs_for(WEAK_AGENT)
ORGANIC_COUPLING_MIN_SEEDS = 3
SUPPLEMENTARY_UAD_MIN_EFFECT_BITS = 0.08
SUPPLEMENTARY_UAD_PROBE_T = 80


@dataclass(frozen=True)
class SupplementaryUADProbe:
    probe_id: str
    programs_by_actor: dict[str, str]
    seeds: tuple[int, ...]
    T: int


def default_supplementary_uad_probes() -> tuple[SupplementaryUADProbe, ...]:
    """Pre-registered organic channel probe (frozen GL-65)."""
    weak = dict(_DEFAULT_WEAK)
    return (
        SupplementaryUADProbe(
            probe_id="organic_eng_review_channel",
            programs_by_actor={
                **weak,
                "eng1": "uad_channel_liaison",
                "rev1": "uad_channel_scribe",
            },
            seeds=(0, 1, 2, 3, 4),
            T=SUPPLEMENTARY_UAD_PROBE_T,
        ),
    )


def load_supplementary_uad_probes(data: dict) -> tuple[SupplementaryUADProbe, ...]:
    meta = data.get("v3_fixture_metadata", {}).get("supplementary_uad")
    if not isinstance(meta, dict):
        return default_supplementary_uad_probes()
    raw_probes = meta.get("probes")
    if not isinstance(raw_probes, list) or not raw_probes:
        return default_supplementary_uad_probes()
    probes: list[SupplementaryUADProbe] = []
    for raw in raw_probes:
        if not isinstance(raw, dict):
            continue
        probes.append(
            SupplementaryUADProbe(
                probe_id=str(raw["probe_id"]),
                programs_by_actor=dict(raw["programs_by_actor"]),
                seeds=tuple(raw.get("seeds", (0, 1, 2, 3, 4))),
                T=int(raw.get("T", SUPPLEMENTARY_UAD_PROBE_T)),
            )
        )
    return tuple(probes)


def _episode_config_for_probe(
    ecology_data: dict,
    ecology_path: Path,
    probe: SupplementaryUADProbe,
) -> EpisodeConfig:
    cfg = _reference_episode_config(ecology_data, ecology_path=ecology_path)
    if probe.T != cfg.T:
        cfg = EpisodeConfig(
            agents=cfg.agents,
            T=probe.T,
            pipeline_spec=cfg.pipeline_spec,
            substrate_settings=cfg.substrate_settings,
            carrier_termination_mode=cfg.carrier_termination_mode,
            units=cfg.units,
            ecology_version=cfg.ecology_version,
            record_contention=cfg.record_contention,
            ecology_override_path=cfg.ecology_override_path,
        )
    return cfg


def run_supplementary_uad_probe(
    ecology_path: Path | str,
    probe: SupplementaryUADProbe,
    *,
    backend=None,
) -> dict[str, Any]:
    ecology_path = Path(ecology_path)
    ecology_data = load_substrate(ecology_path).data
    roster = reference_roster_from_ecology(
        ecology_data, agent_type=WEAK_AGENT, temperature=0.35
    )
    cfg = _episode_config_for_probe(ecology_data, ecology_path, probe)
    backend = backend or MockIsolate()
    ground = live_coupling_ground_truth_units(ecology_data, roster)
    expected = set(next(iter(ground.values()))) if ground else set()
    channel_id = "eng_review_channel"
    if ground:
        unit_key = next(iter(ground))
        if unit_key.startswith("governed_"):
            channel_id = unit_key.removeprefix("governed_")
    seed_results: list[dict[str, Any]] = []
    for seed in probe.seeds:
        result = run_episode(
            cfg,
            seed,
            backend,
            programs=probe.programs_by_actor,
            behavior_profiles={},
        )
        ok, details = organic_channel_coupling_recovered(
            result,
            expected,
            channel_id=channel_id,
            min_effect_bits=SUPPLEMENTARY_UAD_MIN_EFFECT_BITS,
        )
        seed_results.append(
            {
                "seed": seed,
                "passed": ok,
                "details": details,
                "n_channel_ok": sum(
                    1
                    for e in result.primitive_log
                    if e.get("status") == "ok"
                    and isinstance(e.get("primitive"), dict)
                    and e["primitive"].get("kind") == "communicate"
                ),
            }
        )
    n_pass = sum(1 for row in seed_results if row["passed"])
    return {
        "probe_id": probe.probe_id,
        "programs_by_actor": probe.programs_by_actor,
        "expected_members": sorted(expected),
        "n_seeds": len(probe.seeds),
        "n_pass": n_pass,
        "passed": n_pass >= ORGANIC_COUPLING_MIN_SEEDS,
        "seeds": seed_results,
    }


def evaluate_supplementary_uad_gate(
    ecology_path: Path | str,
    *,
    probes: tuple[SupplementaryUADProbe, ...] | None = None,
    backend=None,
    progress: bool = True,
) -> dict[str, Any]:
    ecology_path = Path(ecology_path)
    ecology_data = load_substrate(ecology_path).data
    probes = probes or load_supplementary_uad_probes(ecology_data)
    probe_results: list[dict[str, Any]] = []
    for i, probe in enumerate(probes):
        if progress:
            print(
                f"[supplementary-uad {i + 1}/{len(probes)}] probe={probe.probe_id}",
                flush=True,
            )
        probe_results.append(
            run_supplementary_uad_probe(ecology_path, probe, backend=backend)
        )
    verified = all(row["passed"] for row in probe_results)
    return {
        "ecology_path": str(ecology_path),
        "n_probes": len(probes),
        "organic_channel_coupling_verified": verified,
        "min_effect_bits": SUPPLEMENTARY_UAD_MIN_EFFECT_BITS,
        "min_seeds_per_probe": ORGANIC_COUPLING_MIN_SEEDS,
        "probes": probe_results,
    }
