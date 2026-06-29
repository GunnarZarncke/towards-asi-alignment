"""Run patched episodes through blind audit; evaluate post-hoc only."""

from __future__ import annotations

import time
from dataclasses import asdict

from multiresolution_alignment_sim.calibration import frozen_handle_calibration
from multiresolution_alignment_sim.cci_audit import audit_cci
from multiresolution_alignment_sim.detector import run_detector
from multiresolution_alignment_sim.evaluate import evaluate, safety_decision
from multiresolution_alignment_sim.observation import build_audit_trace
from multiresolution_alignment_sim.schemas import (
    HANDLE_INSTRUMENTATION_LEVELS,
    InstrumentationLevel,
    ScenarioName,
)
from multiresolution_alignment_sim.simulator import simulate

from .protocol import RedTeamProtocol
from .strategies import AuditPatchStrategy, STRATEGIES

REDTEAM_SCENARIOS: tuple[ScenarioName, ...] = (
    "capture_theater",
    "capture_mild",
    "boundary_alias",
    "grounding_silent_gap",
    "hidden_capability",
    "selection_basin",
)


def run_redteam_one(
    scenario: ScenarioName,
    seed: int,
    T: int,
    strategy: AuditPatchStrategy,
    instrumentation: InstrumentationLevel = "medium_handles",
    proposal_k: int = 8,
) -> dict[str, object]:
    """Simulate, apply deployment patch, audit blind; oracle used only in evaluate()."""
    micro, ledger, episode_meta = simulate(scenario, seed, T=T)
    patched_meta = strategy.apply(episode_meta)
    audit, lineage = build_audit_trace(
        micro, scenario, seed, patched_meta, instrumentation=instrumentation
    )
    ledger.lineage = lineage

    cal = frozen_handle_calibration() if instrumentation in HANDLE_INSTRUMENTATION_LEVELS else None
    detector = run_detector(audit, proposal_k=proposal_k)
    cci = audit_cci(audit, calibration=cal)
    safety = safety_decision(cci, detector)
    ev = evaluate(ledger, lineage, detector, cci, audit, episode_meta)

    false_pass = cci.status == "passes" and not ev.cci_status_correct

    return {
        "scenario": scenario,
        "seed": seed,
        "T": T,
        "strategy": strategy.name,
        "instrumentation": instrumentation,
        "cci_status": cci.status,
        "safety_decision": safety.decision,
        "false_pass": false_pass,
        "cci_status_correct": ev.cci_status_correct,
        "capture_detected": ev.capture_detected,
        "oracle_judge_captured": ledger.judge_captured,
        "cci": asdict(cci),
        "safety": asdict(safety),
        "evaluation": asdict(ev),
    }


def _summarize_runs(runs: list[dict[str, object]]) -> dict[str, object]:
    false_passes = [r for r in runs if r["false_pass"]]
    by_strategy: dict[str, list[dict]] = {}
    by_level: dict[str, list[dict]] = {}
    for run in runs:
        by_strategy.setdefault(str(run["strategy"]), []).append(run)
        by_level.setdefault(str(run["instrumentation"]), []).append(run)

    return {
        "false_pass_count": len(false_passes),
        "false_pass_rate": len(false_passes) / max(len(runs), 1),
        "summary_by_strategy": {
            name: {
                "n_runs": len(strat_runs),
                "false_pass_rate": sum(1 for r in strat_runs if r["false_pass"])
                / max(len(strat_runs), 1),
                "mean_cci_correct": sum(
                    1 for r in strat_runs if r["cci_status_correct"]
                )
                / max(len(strat_runs), 1),
            }
            for name, strat_runs in by_strategy.items()
        },
        "summary_by_instrumentation": {
            level: {
                "n_runs": len(level_runs),
                "false_pass_rate": sum(1 for r in level_runs if r["false_pass"])
                / max(len(level_runs), 1),
                "mean_cci_correct": sum(
                    1 for r in level_runs if r["cci_status_correct"]
                )
                / max(len(level_runs), 1),
            }
            for level, level_runs in by_level.items()
        },
    }


def run_redteam_suite(
    scenarios: list[ScenarioName],
    seeds: list[int],
    T: int,
    strategy_names: list[str],
    instrumentation: InstrumentationLevel = "medium_handles",
    protocol: RedTeamProtocol | None = None,
) -> dict[str, object]:
    t0 = time.perf_counter()
    protocol = protocol or RedTeamProtocol()
    runs: list[dict[str, object]] = []

    for strategy_name in strategy_names:
        strategy = STRATEGIES[strategy_name]
        for scenario in scenarios:
            for seed in seeds:
                runs.append(
                    run_redteam_one(
                        scenario,
                        seed,
                        T,
                        strategy,
                        instrumentation=instrumentation,
                    )
                )

    stats = _summarize_runs(runs)

    return {
        "claim_strength": (
            "hand-written red-team scaffold; not frontier LLM evidence"
        ),
        "protocol": {
            "model": protocol.model,
            "may_read_source": protocol.may_read_source,
            "allowed_source_modules": list(protocol.allowed_source_modules),
            "forbidden_oracle_fields": list(protocol.forbidden_oracle_fields),
        },
        "T": T,
        "scenarios": scenarios,
        "seeds": seeds,
        "strategy_names": strategy_names,
        "instrumentation": instrumentation,
        "instrumentation_levels": [instrumentation],
        "runtime_seconds": round(time.perf_counter() - t0, 2),
        **stats,
        "runs": runs,
    }


def run_redteam_battery(
    scenarios: list[ScenarioName],
    seeds: list[int],
    T: int,
    strategy_names: list[str],
    instrumentation_levels: list[InstrumentationLevel],
    protocol: RedTeamProtocol | None = None,
) -> dict[str, object]:
    """Phase 1 battery across multiple instrumentation levels."""
    t0 = time.perf_counter()
    protocol = protocol or RedTeamProtocol()
    runs: list[dict[str, object]] = []

    for level in instrumentation_levels:
        for strategy_name in strategy_names:
            strategy = STRATEGIES[strategy_name]
            for scenario in scenarios:
                for seed in seeds:
                    runs.append(
                        run_redteam_one(
                            scenario,
                            seed,
                            T,
                            strategy,
                            instrumentation=level,
                        )
                    )

    stats = _summarize_runs(runs)

    return {
        "claim_strength": (
            "Phase 1 hand-written red-team battery; not frontier LLM evidence"
        ),
        "protocol": {
            "model": protocol.model,
            "may_read_source": protocol.may_read_source,
            "allowed_source_modules": list(protocol.allowed_source_modules),
            "forbidden_oracle_fields": list(protocol.forbidden_oracle_fields),
        },
        "T": T,
        "scenarios": scenarios,
        "seeds": seeds,
        "strategy_names": strategy_names,
        "instrumentation_levels": list(instrumentation_levels),
        "runtime_seconds": round(time.perf_counter() - t0, 2),
        **stats,
        "runs": runs,
    }
