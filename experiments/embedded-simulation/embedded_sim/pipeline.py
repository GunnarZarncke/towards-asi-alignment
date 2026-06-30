"""Single-episode pipeline: world → red-team → embedded audit → outer eval."""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass

from .audit_core.cci_audit import audit_cci
from .audit_core.detector import run_detector
from .audit_core.schemas import MicroVariable, TruthLedger
from .embedded_audit import run_embedded_audit
from .isolate_pool import default_isolate_workers, run_timestep
from .js_isolate import summarize_isolate_runs
from .lab import build_world, rebuild_audit_inputs
from .outer_eval import outer_evaluate
from .redteam import run_redteam
from .schemas_embedded import BridgeId, EpisodeResult, InstrumentationLevel, SubstrateKind
from .scenarios import MB_SCENARIOS
from .world import EmbeddedWorld


@dataclass
class _EpisodeState:
    bridge: BridgeId
    scenario: str
    world: EmbeddedWorld
    ledger: TruthLedger
    micro: list[MicroVariable]
    started_at: float
    audit_out: tuple | None = None


def run_episode(
    bridge: BridgeId,
    scenario: str,
    seed: int = 42,
    T: int = 800,
    instrumentation: InstrumentationLevel = "medium_handles",
    redteam_strategy: str = "none",
    substrate: SubstrateKind = "python",
    *,
    isolate_workers: int = 1,
) -> EpisodeResult:
    t0 = time.perf_counter()
    world, ledger, _micro = build_world(bridge, scenario, seed, T=T)
    run_redteam(
        world,
        redteam_strategy,
        substrate=substrate,
        timestep="redteam",
        parallel=isolate_workers > 1,
    )
    cert, audit, detector, rows = run_embedded_audit(
        world,
        instrumentation,
        substrate=substrate,
        timestep="audit",
        parallel=isolate_workers > 1,
    )
    return _finish_episode(
        bridge,
        scenario,
        seed,
        instrumentation,
        redteam_strategy,
        substrate,
        world,
        ledger,
        cert,
        audit,
        detector,
        rows,
        started_at=t0,
    )


def _finish_episode(
    bridge: BridgeId,
    scenario: str,
    seed: int,
    instrumentation: InstrumentationLevel,
    redteam_strategy: str,
    substrate: SubstrateKind,
    world,
    ledger: TruthLedger,
    cert,
    audit,
    detector,
    rows: list[dict],
    *,
    started_at: float,
) -> EpisodeResult:
    _rows2, audit2, lineage = rebuild_audit_inputs(world, instrumentation)
    cci = audit_cci(audit2)
    outer = outer_evaluate(world, ledger, lineage, detector, audit2, rows, cert, cci)
    elapsed = time.perf_counter() - started_at
    return EpisodeResult(
        scenario=scenario,
        bridge=bridge,
        seed=seed,
        instrumentation=instrumentation,
        redteam_strategy=redteam_strategy,
        substrate=substrate,
        in_sim=cert,
        outer=outer,
        tool_calls=list(world.truth.tool_calls),
        runtime_seconds=elapsed,
        isolate_runs=list(world.truth.isolate_runs),
    )


def run_all_mbs(
    seed: int = 42,
    T: int = 800,
    instrumentation: InstrumentationLevel = "medium_handles",
    redteam_strategy: str = "none",
    substrate: SubstrateKind = "python",
    *,
    isolate_workers: int | None = None,
) -> list[EpisodeResult]:
    workers = isolate_workers if isolate_workers is not None else default_isolate_workers()
    if workers <= 1 or len(MB_SCENARIOS) <= 1:
        return [
            run_episode(
                bridge,
                scenario,
                seed=seed,
                T=T,
                instrumentation=instrumentation,
                redteam_strategy=redteam_strategy,
                substrate=substrate,
                isolate_workers=1,
            )
            for bridge, scenario, _desc in MB_SCENARIOS
        ]

    states: list[_EpisodeState] = []
    for bridge, scenario, _desc in MB_SCENARIOS:
        t_build = time.perf_counter()
        world, ledger, micro = build_world(bridge, scenario, seed, T=T)
        states.append(
            _EpisodeState(
                bridge,
                scenario,
                world,
                ledger,
                micro,
                started_at=t_build,
            )
        )

    run_timestep(
        states,
        lambda s: _timestep_redteam(s, redteam_strategy, substrate, workers),
        workers=workers,
        label="redteam",
    )
    audit_outputs = run_timestep(
        states,
        lambda s: _timestep_audit(s, instrumentation, substrate, workers),
        workers=workers,
        label="audit",
    )
    for state, audit_out in zip(states, audit_outputs, strict=True):
        state.audit_out = audit_out

    results = run_timestep(
        states,
        lambda s: _timestep_finish(
            s,
            seed,
            instrumentation,
            redteam_strategy,
            substrate,
        ),
        workers=workers,
        label="eval",
    )
    return results


def _timestep_redteam(
    state: _EpisodeState,
    redteam_strategy: str,
    substrate: SubstrateKind,
    workers: int,
) -> None:
    run_redteam(
        state.world,
        redteam_strategy,
        substrate=substrate,
        timestep="redteam",
        parallel=workers > 1,
    )


def _timestep_audit(
    state: _EpisodeState,
    instrumentation: InstrumentationLevel,
    substrate: SubstrateKind,
    workers: int,
) -> tuple:
    return run_embedded_audit(
        state.world,
        instrumentation,
        substrate=substrate,
        timestep="audit",
        parallel=workers > 1,
    )


def _timestep_finish(
    state: _EpisodeState,
    seed: int,
    instrumentation: InstrumentationLevel,
    redteam_strategy: str,
    substrate: SubstrateKind,
) -> EpisodeResult:
    assert state.audit_out is not None
    cert, audit, detector, rows = state.audit_out
    return _finish_episode(
        state.bridge,
        state.scenario,
        seed,
        instrumentation,
        redteam_strategy,
        substrate,
        state.world,
        state.ledger,
        cert,
        audit,
        detector,
        rows,
        started_at=state.started_at,
    )


def episode_to_dict(ep: EpisodeResult) -> dict:
    return {
        "scenario": ep.scenario,
        "bridge": ep.bridge,
        "seed": ep.seed,
        "instrumentation": ep.instrumentation,
        "redteam_strategy": ep.redteam_strategy,
        "substrate": ep.substrate,
        "runtime_seconds": ep.runtime_seconds,
        "in_sim": {
            "cci_status": ep.in_sim.cci_status,
            "safety_decision": ep.in_sim.safety_decision,
            "failed_bridge": ep.in_sim.failed_bridge,
            "unit_id": ep.in_sim.unit.candidate_id if ep.in_sim.unit else None,
            "unit_score": ep.in_sim.unit.score if ep.in_sim.unit else None,
            "unit_scope_steps": ep.in_sim.unit_scope_steps,
            "gate_decision": ep.in_sim.deploy_gate.gate_decision if ep.in_sim.deploy_gate else None,
            "successor_unit": (
                ep.in_sim.successor_unit.candidate_id if ep.in_sim.successor_unit else None
            ),
            "notes": ep.in_sim.notes,
        },
        "outer": asdict(ep.outer),
        "evaluation": {"cci_status_correct": ep.outer.in_sim_correct},
        "tool_calls": len(ep.tool_calls),
        "isolate_runs": [asdict(r) for r in ep.isolate_runs],
        "isolate_timing": summarize_isolate_runs(ep.isolate_runs),
    }
