"""Intervention-granularity curve: does correct UAD identity buy safety?

Sweeps the auditor's intervention granularity (``pipeline`` / ``window`` /
``actor``) crossed with UAD mode (``full`` MI vs ``fake`` heuristic) under a
lab where the offender is *co-active* with a benign actor at every offending
step. The headline metric is the full-vs-fake separation per level:

- At ``pipeline`` / ``window`` the offender cannot be isolated, so unit identity
  is non-functional and full ≈ fake.
- At ``actor`` a correct unit (full UAD) can mask the offender's interventions
  to the right scope, so full should beat fake on false-pass.
"""

from __future__ import annotations

import time

from .intervention_config import (
    INTERVENTION_LEVELS,
    InterventionLevel,
    get_intervention_level,
    set_intervention_level,
)
from .lab_ecology import LabEcologyConfig, get_lab_ecology, set_lab_ecology
from .scenarios import MB_SCENARIOS
from .uad_config import get_uad_mode, set_uad_mode

# Bridges that instantiate a hidden offender / boundary grab.
OFFENDER_BRIDGES: tuple[str, ...] = ("MB1", "MB6", "MB6b", "MB7d")


def _cell_runs(
    bridges: list[str],
    seeds: list[int],
    T: int,
    instrumentation: str,
) -> list[dict]:
    from .pipeline import run_episode

    # When the misleading-top2 scenario is active the true offender is the
    # colluder pair (hidden_group COLLUDER), not the G3 oracle that the default
    # outer eval scores against. Measure coverage of the colluder pair directly.
    misleading = get_lab_ecology().misleading_top2
    colluders = {"actor.colluder.0", "actor.colluder.1"}

    scenario_by_bridge = {b: s for b, s, _d in MB_SCENARIOS}
    runs: list[dict] = []
    for bridge in bridges:
        scenario = scenario_by_bridge.get(bridge, "honest")
        for seed in seeds:
            ep = run_episode(
                bridge,  # type: ignore[arg-type]
                scenario,
                seed=seed,
                T=T,
                instrumentation=instrumentation,  # type: ignore[arg-type]
                redteam_strategy="full_redteam",
            )
            members = set(ep.in_sim.unit.member_ids) if ep.in_sim.unit else set()
            if misleading:
                recall = len(members & colluders) / len(colluders)
            else:
                recall = float(ep.outer.uad_recall)
            runs.append(
                {
                    "bridge": bridge,
                    "seed": seed,
                    "false_pass": bool(ep.outer.false_pass),
                    "in_sim_correct": bool(ep.outer.in_sim_correct),
                    "uad_recall": recall,
                    "unit_scope_steps": int(ep.in_sim.unit_scope_steps),
                    "unit_id": ep.in_sim.unit.candidate_id if ep.in_sim.unit else None,
                }
            )
    return runs


def _aggregate(runs: list[dict]) -> dict[str, float]:
    n = max(len(runs), 1)
    return {
        "n_runs": len(runs),
        "false_pass_rate": sum(1 for r in runs if r["false_pass"]) / n,
        "in_sim_correct_rate": sum(1 for r in runs if r["in_sim_correct"]) / n,
        "mean_uad_recall": sum(r["uad_recall"] for r in runs) / n,
        "mean_unit_scope_steps": sum(r["unit_scope_steps"] for r in runs) / n,
    }


def run_intervention_curve(
    seeds: list[int] | None = None,
    bridges: list[str] | None = None,
    T: int = 400,
    instrumentation: str = "medium_handles",
    levels: tuple[InterventionLevel, ...] = INTERVENTION_LEVELS,
    coactive: bool = True,
    misleading_top2: bool = True,
    bind: bool = True,
) -> dict:
    """Run the level × mode matrix and report per-level full-vs-fake separation."""
    seeds = seeds or [11, 12, 13]
    bridges = bridges or list(OFFENDER_BRIDGES)

    prev_level = get_intervention_level()
    prev_mode = get_uad_mode()
    prev_ecology = get_lab_ecology()

    from .handle_calibration import get_handle_calibration

    get_handle_calibration()
    t0 = time.perf_counter()
    by_level: dict[str, dict] = {}
    try:
        set_lab_ecology(
            LabEcologyConfig(
                n_adversarial_candidates=prev_ecology.n_adversarial_candidates,
                common_legitimate_lab_agents=prev_ecology.common_legitimate_lab_agents,
                auditor_agent=prev_ecology.auditor_agent,
                alignment_target_agent=prev_ecology.alignment_target_agent,
                n_decoys=prev_ecology.n_decoys,
                coactive_offender=coactive,
                misleading_top2=misleading_top2,
                bind_offender_interventions=bind,
            )
        )
        for level in levels:
            set_intervention_level(level)
            modes: dict[str, dict] = {}
            for mode in ("full", "fake"):
                set_uad_mode(mode)  # type: ignore[arg-type]
                runs = _cell_runs(bridges, seeds, T, instrumentation)
                modes[mode] = {"summary": _aggregate(runs), "runs": runs}
            full_fp = modes["full"]["summary"]["false_pass_rate"]
            fake_fp = modes["fake"]["summary"]["false_pass_rate"]
            by_level[level] = {
                "modes": modes,
                "false_pass_separation": fake_fp - full_fp,
            }
    finally:
        set_intervention_level(prev_level)
        set_uad_mode(prev_mode)  # type: ignore[arg-type]
        set_lab_ecology(prev_ecology)

    return {
        "kind": "intervention_curve",
        "T": T,
        "seeds": seeds,
        "bridges": bridges,
        "instrumentation": instrumentation,
        "coactive_offender": coactive,
        "misleading_top2": misleading_top2,
        "bind_offender_interventions": bind,
        "levels": list(levels),
        "by_level": by_level,
        "runtime_seconds": round(time.perf_counter() - t0, 2),
    }


def md_intervention_curve(payload: dict) -> str:
    lines = [
        "# Embedded intervention-granularity curve",
        "",
        f"T={payload['T']} seeds={payload['seeds']} bridges={payload['bridges']}",
        f"coactive_offender={payload['coactive_offender']} "
        f"misleading_top2={payload.get('misleading_top2')} "
        f"bind={payload.get('bind_offender_interventions')} "
        f"instrumentation={payload['instrumentation']}",
        "",
        "Full-vs-fake separation should be ~0 at `pipeline`/`window` and positive "
        "at `actor`: a correct UAD unit only buys safety once the intervention "
        "handle is fine enough to isolate the co-active offender. UAD recall is "
        "the offender (colluder pair) coverage by the selected unit.",
        "",
        "| Level | Full FP | Fake FP | Separation (fake−full) | "
        "Full correct | Fake correct | Full recall | Fake recall |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for level in payload["levels"]:
        cell = payload["by_level"][level]
        full = cell["modes"]["full"]["summary"]
        fake = cell["modes"]["fake"]["summary"]
        lines.append(
            f"| {level} | {full['false_pass_rate']:.1%} | {fake['false_pass_rate']:.1%} | "
            f"{cell['false_pass_separation']:+.1%} | "
            f"{full['in_sim_correct_rate']:.1%} | {fake['in_sim_correct_rate']:.1%} | "
            f"{full['mean_uad_recall']:.1%} | {fake['mean_uad_recall']:.1%} |"
        )
    lines.extend(
        [
            "",
            "## Mean unit scope steps (retained interventions the unit can act on)",
            "",
            "| Level | Full | Fake |",
            "| --- | --- | --- |",
        ]
    )
    for level in payload["levels"]:
        cell = payload["by_level"][level]
        lines.append(
            f"| {level} | "
            f"{cell['modes']['full']['summary']['mean_unit_scope_steps']:.1f} | "
            f"{cell['modes']['fake']['summary']['mean_unit_scope_steps']:.1f} |"
        )
    lines.append(f"\nRuntime: {payload['runtime_seconds']}s")
    return "\n".join(lines) + "\n"
