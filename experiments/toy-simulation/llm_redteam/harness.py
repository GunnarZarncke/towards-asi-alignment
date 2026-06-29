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


def _log_progress(msg: str) -> None:
    print(msg, flush=True)


def _count_planned_runs(
    scenarios: list[ScenarioName],
    seeds: list[int],
    strategy_names: list[str],
    instrumentation_levels: list[InstrumentationLevel],
) -> int:
    return len(instrumentation_levels) * len(strategy_names) * len(scenarios) * len(seeds)


def _run_redteam_grid(
    scenarios: list[ScenarioName],
    seeds: list[int],
    T: int,
    strategy_names: list[str],
    instrumentation_levels: list[InstrumentationLevel],
    *,
    label: str = "redteam",
    progress_every: int = 25,
) -> list[dict[str, object]]:
    """Run the full strategy × scenario × seed × level grid with progress logs."""
    total = _count_planned_runs(scenarios, seeds, strategy_names, instrumentation_levels)
    t0 = time.perf_counter()
    runs: list[dict[str, object]] = []
    false_pass_count = 0

    _log_progress(
        f"{label}: starting {total} runs "
        f"(T={T}, seeds={seeds[0]}–{seeds[-1]}, "
        f"{len(scenarios)} scenarios, {len(strategy_names)} strategies, "
        f"{len(instrumentation_levels)} levels)"
    )

    for level in instrumentation_levels:
        _log_progress(f"{label}: level={level}")
        for strategy_name in strategy_names:
            strategy = STRATEGIES[strategy_name]
            for scenario in scenarios:
                for seed in seeds:
                    run = run_redteam_one(
                        scenario,
                        seed,
                        T,
                        strategy,
                        instrumentation=level,
                    )
                    runs.append(run)
                    if run["false_pass"]:
                        false_pass_count += 1

                    n = len(runs)
                    if n == 1 or n == total or n % progress_every == 0:
                        elapsed = time.perf_counter() - t0
                        rate = n / elapsed if elapsed > 0 else 0.0
                        eta = (total - n) / rate if rate > 0 else 0.0
                        _log_progress(
                            f"{label}: [{n}/{total}] "
                            f"{level}/{strategy_name}/{scenario}/seed{seed} "
                            f"false_pass={false_pass_count} "
                            f"elapsed={elapsed:.0f}s eta={eta:.0f}s"
                        )

    elapsed = time.perf_counter() - t0
    _log_progress(
        f"{label}: finished {total} runs in {elapsed:.1f}s "
        f"({elapsed / 60:.1f} min), false_passes={false_pass_count}"
    )
    return runs


def format_battery_completion(
    payload: dict[str, object],
    *,
    mode: str = "battery",
) -> str:
    """Human-readable completion block for stdout and session logs."""
    runs = payload.get("runs", [])
    n_runs = len(runs) if isinstance(runs, list) else 0
    runtime = payload.get("runtime_seconds", 0)
    title = (
        "LLM RED-TEAM BATTERY COMPLETE"
        if mode == "battery"
        else "LLM RED-TEAM RUN COMPLETE"
    )
    lines = [
        "=" * 64,
        title,
        "=" * 64,
        f"Runtime: {runtime}s ({float(runtime) / 60:.1f} min)",
        f"Runs: {n_runs}",
        f"False passes: {payload.get('false_pass_count', 0)} "
        f"({float(payload.get('false_pass_rate', 0)):.2%})",
        "",
        "Configuration:",
        f"  T={payload.get('T')}",
        f"  seeds={payload.get('seeds')}",
        f"  scenarios={payload.get('scenarios')}",
        f"  strategies={payload.get('strategy_names')}",
        f"  levels={payload.get('instrumentation_levels')}",
        "",
        "By strategy:",
    ]
    for name, stats in payload.get("summary_by_strategy", {}).items():
        lines.append(
            f"  {name}: false_pass={stats['false_pass_rate']:.2%} "
            f"cci_correct={stats['mean_cci_correct']:.2%} n={stats['n_runs']}"
        )
    lines.extend(["", "By instrumentation:"])
    for level, stats in payload.get("summary_by_instrumentation", {}).items():
        lines.append(
            f"  {level}: false_pass={stats['false_pass_rate']:.2%} "
            f"cci_correct={stats['mean_cci_correct']:.2%} n={stats['n_runs']}"
        )
    lines.append("=" * 64)
    return "\n".join(lines)


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
    runs = _run_redteam_grid(
        scenarios,
        seeds,
        T,
        strategy_names,
        [instrumentation],
        label="redteam_suite",
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
    runs = _run_redteam_grid(
        scenarios,
        seeds,
        T,
        strategy_names,
        instrumentation_levels,
        label="redteam_battery",
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
