#!/usr/bin/env python3
"""Reference-battery sweep for slice-D freeze estimates (GL-52 follow-up).

Runs the integrated v3 reference fixture at a chosen horizon T and seed
range, reporting C1-v3 / C3 / C4 / C5-v3 / coupling-gate statistics with
Wilson-style deploy-rate CI (normal approx on proportion).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from graded_lab.harness.ecology_complexity import (  # noqa: E402
    C3_SEEDS,
    V3_REFERENCE_T,
    check_c3,
    check_c4,
)
from graded_lab.harness.isolate import MockIsolate  # noqa: E402
from graded_lab.oracle_only.calibration import WEAK_AGENT  # noqa: E402
from graded_lab.oracle_only.principal_scorecard import check_c1_v3  # noqa: E402
from graded_lab.world_visible.config import EpisodeConfig  # noqa: E402
from graded_lab.world_visible.ecology_agents import (  # noqa: E402
    programs_and_profiles_for_roster,
    reference_roster_from_ecology,
)
from graded_lab.world_visible.mechanism_exercise import (  # noqa: E402
    check_c5_v3,
    coupling_stimulus_recovered,
    live_coupling_ground_truth_units,
)
from graded_lab.world_visible.substrate import load_substrate  # noqa: E402
from graded_lab.world_visible.world import default_lab_config, run_episode  # noqa: E402

DEFAULT_FIXTURE = ROOT / "tests/fixtures/ecology_v3_slice_a_reference.json"


def _deploy_rate_ci(n_deploy: int, n: int, z: float = 1.96) -> dict[str, float]:
    if n == 0:
        return {"low": 0.0, "high": 0.0, "point": 0.0}
    p = n_deploy / n
    se = math.sqrt(max(p * (1 - p) / n, 0.0))
    return {"point": p, "low": max(0.0, p - z * se), "high": min(1.0, p + z * se)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument(
        "--T", type=int, default=V3_REFERENCE_T, help="episode horizon (frozen v3 default)"
    )
    parser.add_argument(
        "--seeds", type=int, default=50, help="number of seeds 0..n-1 (C3/C4 use 20)"
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / f"results/slice_d_reference_battery_T{V3_REFERENCE_T}_n50.json",
    )
    args = parser.parse_args()

    data = load_substrate(args.fixture).data
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    programs, profiles = programs_and_profiles_for_roster(roster, ecology_data=data)
    ground = live_coupling_ground_truth_units(data, roster)
    expected = set(next(iter(ground.values()))) if ground else set()

    base = default_lab_config()
    cfg = EpisodeConfig(
        agents=roster.agents,
        T=args.T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
        ecology_version="v3",
        ecology_override_path=args.fixture,
        record_contention=True,
    )
    backend = MockIsolate()
    n = args.seeds
    started = time.perf_counter()
    results = []
    coupling_scores: list[float] = []
    coupling_pass = 0

    for i, seed in enumerate(range(n)):
        t0 = time.perf_counter()
        result = run_episode(
            cfg, seed, backend, programs=programs, behavior_profiles=profiles
        )
        results.append(result)
        if expected:
            ok, det = coupling_stimulus_recovered(result, expected)
            coupling_pass += int(ok)
            scores = det.get("pair_scores") or {}
            if scores:
                coupling_scores.append(float(next(iter(scores.values()))))
        elapsed = time.perf_counter() - t0
        print(
            f"[{i + 1}/{n}] seed={seed} deployed={result.deployed} "
            f"coupling_ok={ok if expected else 'n/a'} ({elapsed:.1f}s)",
            flush=True,
        )

    c3_pass, c3_details = check_c3(results)
    c4_pass, c4_details = check_c4(results)
    c1_pass, c1_details = check_c1_v3(data, results)
    c5_pass, c5_details = check_c5_v3(data, results)
    n_deploy = sum(1 for r in results if r.deployed)

    payload = {
        "fixture": str(args.fixture),
        "T": args.T,
        "n_seeds": n,
        "wall_seconds": time.perf_counter() - started,
        "seconds_per_episode": (time.perf_counter() - started) / n if n else 0,
        "deploy_rate_ci": _deploy_rate_ci(n_deploy, n),
        "c3": {"passed": c3_pass, **c3_details},
        "c4": {"passed": c4_pass, **c4_details},
        "c1_v3": {"passed": c1_pass, **c1_details},
        "c5_v3": {"passed": c5_pass, **c5_details},
        "coupling_gate": {
            "passed_fraction": coupling_pass / n if n else 0.0,
            "n_pass": coupling_pass,
            "pair_cmi_bits": {
                "min": min(coupling_scores) if coupling_scores else None,
                "median": sorted(coupling_scores)[len(coupling_scores) // 2]
                if coupling_scores
                else None,
                "max": max(coupling_scores) if coupling_scores else None,
            },
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out}", flush=True)
    print(
        f"Summary: deploy={payload['deploy_rate_ci']['point']:.3f} "
        f"[{payload['deploy_rate_ci']['low']:.3f},{payload['deploy_rate_ci']['high']:.3f}] "
        f"C3={c3_pass} C4={c4_pass} C1-v3={c1_pass} C5-v3={c5_pass} "
        f"coupling={coupling_pass}/{n}",
        flush=True,
    )


if __name__ == "__main__":
    main()
