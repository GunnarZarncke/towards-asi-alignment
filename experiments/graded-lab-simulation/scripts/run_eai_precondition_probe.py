#!/usr/bin/env python3
"""Standalone R-MB6b EAI precondition probe (referee mid band at default load).

Compares referee/agent-vantage EAI on:
  - v1 default substrate (Phase 7 calibration ecology, no JSON fixture)
  - v3_grown (``generated_ecology_v3.json``, V2-3 reference roster/protocol)

Uses the same tiers, seeds, and carrier grid as ``machinery_transfer.py`` /
``run_referee_eai_check.py``. Does not retune thresholds or rerun the full
transfer battery.

Usage:
  cd experiments/graded-lab-simulation
  .venv/bin/python scripts/run_eai_precondition_probe.py
  .venv/bin/python scripts/run_eai_precondition_probe.py --smoke
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from graded_lab.harness.isolate import MockIsolate  # noqa: E402
from graded_lab.harness.machinery_transfer import (  # noqa: E402
    DEFAULT_CARRIER_LOAD,
    EAI_SEEDS,
    _aggregate_eai_cells,
    reference_bundle,
    score_eai_vantage_split,
)
from graded_lab.oracle_only.calibration import (  # noqa: E402
    CARRIER_SCALES,
    MID_EAI,
    NOMINAL_COMPUTE_SCALE,
    NOMINAL_SPREAD_SCALE,
    REFEREE_TIER,
    STRONG_AGENT,
    WEAK_AGENT,
    config_for_settings,
    programs_for,
)
from graded_lab.oracle_only.eai import eai_components_at_tier, tier_i_fraction_from_log  # noqa: E402
from graded_lab.world_visible.config import CODE_VERSION, SubstrateSettings  # noqa: E402
from graded_lab.world_visible.substrate import V3_GROWN_ECOLOGY_PATH  # noqa: E402
from graded_lab.world_visible.world import run_episode  # noqa: E402

RESULTS_DEFAULT = ROOT / "results" / "eai_precondition_probe.json"
AGENT_EAI_TIER = "full"


def _score_v1_eai_cell(
    seed: int,
    carrier_load_scale: float,
    *,
    agent_type: str,
    backend,
) -> tuple[float, int, float, float]:
    settings = SubstrateSettings(
        compute_scale=NOMINAL_COMPUTE_SCALE,
        population_spread_scale=NOMINAL_SPREAD_SCALE,
        carrier_load_scale=carrier_load_scale,
    )
    cfg = config_for_settings(settings)
    programs = programs_for(agent_type)
    result = run_episode(cfg, seed, backend, programs=programs)
    tier_i_fraction = tier_i_fraction_from_log(result.primitive_log)
    agent_parts = eai_components_at_tier(
        result.primitive_log, result.decision_margins, tier_i_fraction, AGENT_EAI_TIER
    )
    referee_parts = eai_components_at_tier(
        result.primitive_log,
        result.decision_margins,
        tier_i_fraction,
        REFEREE_TIER,
    )
    agent_c = sum(agent_parts.values()) / 3.0
    ref_c = sum(referee_parts.values()) / 3.0
    return carrier_load_scale, seed, agent_c, ref_c


def score_v1_eai_vantage_split(
    *,
    agent_type: str,
    seeds: tuple[int, ...],
    carrier_scales: tuple[float, ...],
    progress: bool = True,
) -> dict:
    backend = MockIsolate()
    cells: list[tuple[float, int, float, float]] = []
    total = len(carrier_scales) * len(seeds)
    done = 0
    for carrier_load_scale in carrier_scales:
        for seed in seeds:
            done += 1
            if progress:
                print(
                    f"[eai-probe v1/{agent_type} {done}/{total}] "
                    f"carrier={carrier_load_scale} seed={seed}",
                    flush=True,
                )
            cells.append(
                _score_v1_eai_cell(
                    seed, carrier_load_scale, agent_type=agent_type, backend=backend
                )
            )
    payload = _aggregate_eai_cells(cells, seeds=seeds, carrier_scales=carrier_scales)
    payload["substrate"] = "v1_default"
    payload["agent_type"] = agent_type
    return payload


def _precondition_verdict(eai: dict) -> dict:
    default = eai["by_carrier_load"].get(str(DEFAULT_CARRIER_LOAD), {})
    ref = default.get("referee_vantage", {})
    agent = default.get("agent_vantage", {})
    return {
        "referee_mean_at_default_load": ref.get("mean"),
        "referee_band_at_default_load": ref.get("band"),
        "agent_mean_at_default_load": agent.get("mean"),
        "agent_band_at_default_load": agent.get("band"),
        "mid_band": list(MID_EAI),
        "go_gate_referee_mid_at_default_load": eai.get(
            "go_gate_referee_mid_at_default_load", False
        ),
        "go_gate_referee_mid_any_carrier_cell": eai.get(
            "go_gate_referee_mid_any_carrier_cell", False
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture",
        type=Path,
        default=V3_GROWN_ECOLOGY_PATH,
        help="v3 ecology JSON (default: frozen v3 grown)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=RESULTS_DEFAULT,
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="2 seeds, carrier=1.0 only (~30 s)",
    )
    args = parser.parse_args()

    seeds = (0, 1) if args.smoke else EAI_SEEDS
    carrier_scales = (DEFAULT_CARRIER_LOAD,) if args.smoke else CARRIER_SCALES
    t0 = time.perf_counter()

    print(f"[eai-probe] CODE_VERSION={CODE_VERSION}", flush=True)
    print(f"[eai-probe] seeds={list(seeds)} carriers={list(carrier_scales)}", flush=True)

    v1_strong = score_v1_eai_vantage_split(
        agent_type=STRONG_AGENT, seeds=seeds, carrier_scales=carrier_scales
    )
    v1_weak = score_v1_eai_vantage_split(
        agent_type=WEAK_AGENT, seeds=seeds, carrier_scales=carrier_scales
    )

    ecology_data, _roster, _cfg, programs, profiles = reference_bundle(args.fixture)
    v3 = score_eai_vantage_split(
        ecology_data,
        args.fixture,
        programs,
        profiles,
        seeds=seeds,
        carrier_scales=carrier_scales,
    )
    v3["substrate"] = "v3_grown"
    v3["agent_type"] = WEAK_AGENT
    v3["ecology_path"] = str(args.fixture.resolve())

    wall = time.perf_counter() - t0
    report = {
        "code_version": CODE_VERSION,
        "battery": "eai_precondition_probe",
        "wall_seconds": wall,
        "seeds": list(seeds),
        "carrier_scales": list(carrier_scales),
        "precondition": (
            "referee-vantage EAI in mid band "
            f"{list(MID_EAI)} at default load (carrier={DEFAULT_CARRIER_LOAD})"
        ),
        "substrates": {
            "v1_default_strong_agent": {
                "eai": v1_strong,
                "verdict": _precondition_verdict(v1_strong),
            },
            "v1_default_weak_agent": {
                "eai": v1_weak,
                "verdict": _precondition_verdict(v1_weak),
            },
            "v3_grown_weak_reference": {
                "eai": v3,
                "verdict": _precondition_verdict(v3),
            },
        },
        "notes": (
            "v3 uses V2-3 reference roster (programmatic_2step / WEAK_AGENT). "
            "v1 strong_agent matches GL-20 referee-eai check; weak_agent for symmetry. "
            "R-MB6b precondition is scoped to this rig's substrate — v3 result is "
            "the direct read for declared-SKIP vs growth on v3_grown."
        ),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"\n[eai-probe] wall={wall:.1f}s wrote {args.out}", flush=True)
    for label, block in report["substrates"].items():
        v = block["verdict"]
        print(
            f"[eai-probe] {label}: referee@1.0 mean={v['referee_mean_at_default_load']:.4f} "
            f"band={v['referee_band_at_default_load']} "
            f"go_gate_default={v['go_gate_referee_mid_at_default_load']} "
            f"go_gate_any_carrier={v['go_gate_referee_mid_any_carrier_cell']}",
            flush=True,
        )


if __name__ == "__main__":
    main()
