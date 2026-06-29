#!/usr/bin/env python3
"""Verify batch Phase 1 strategies match Phase 2 deployment API outcomes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llm_redteam.api import apply_deployment_agent, build_source_index
from llm_redteam.deployment_agents import DEPLOYMENT_AGENTS
from llm_redteam.episode_runner import audit_outcome_key, run_batch_episode, run_deployment_episode
from llm_redteam.harness import REDTEAM_SCENARIOS
from llm_redteam.protocol import DEPLOYMENT_MUTABLE_FIELDS
from llm_redteam.strategies import STRATEGIES
from multiresolution_alignment_sim.simulator import simulate

INSTRUMENTATION_LEVELS = ("light_handles", "medium_handles", "strong_handles")
DEFAULT_SEEDS = list(range(11, 21))
DEFAULT_T = 1000


def patched_mutable_fields(meta: list[dict]) -> list[dict[str, object]]:
    return [
        {k: row[k] for k in DEPLOYMENT_MUTABLE_FIELDS if k in row}
        for row in meta
    ]


def compare_patched_meta(
    batch_meta: list[dict],
    deploy_meta: list[dict],
) -> list[str]:
    """Return human-readable diffs on deployment-mutable fields only."""
    diffs: list[str] = []
    if len(batch_meta) != len(deploy_meta):
        return [f"length mismatch {len(batch_meta)} vs {len(deploy_meta)}"]
    for t, (brow, drow) in enumerate(zip(batch_meta, deploy_meta)):
        for key in DEPLOYMENT_MUTABLE_FIELDS:
            bv = brow.get(key)
            dv = drow.get(key)
            if bv != dv:
                diffs.append(f"step={t} {key}: batch={bv!r} deploy={dv!r}")
    return diffs


def run_equivalence_suite(
    seeds: list[int],
    T: int,
    scenarios: tuple[str, ...],
    strategies: tuple[str, ...],
    instrumentation_levels: tuple[str, ...],
) -> dict[str, object]:
    source_index = build_source_index()
    meta_mismatches: list[dict[str, object]] = []
    outcome_mismatches: list[dict[str, object]] = []
    n_checks = 0

    for strategy_name in strategies:
        batch_strategy = STRATEGIES[strategy_name]
        deploy_agent = DEPLOYMENT_AGENTS[strategy_name]
        for scenario in scenarios:
            for seed in seeds:
                micro, _ledger, raw_meta = simulate(scenario, seed, T=T)  # type: ignore[arg-type]
                del micro, _ledger
                batch_meta = batch_strategy.apply(raw_meta)
                deploy_meta = apply_deployment_agent(raw_meta, deploy_agent, source_index)

                meta_diffs = compare_patched_meta(batch_meta, deploy_meta)
                if meta_diffs:
                    meta_mismatches.append(
                        {
                            "strategy": strategy_name,
                            "scenario": scenario,
                            "seed": seed,
                            "diffs": meta_diffs[:20],
                            "n_diffs": len(meta_diffs),
                        }
                    )

                for level in instrumentation_levels:
                    n_checks += 1
                    batch = run_batch_episode(
                        scenario, seed, T, batch_strategy, instrumentation=level  # type: ignore[arg-type]
                    )
                    deploy = run_deployment_episode(
                        scenario, seed, T, deploy_agent, instrumentation=level  # type: ignore[arg-type]
                    )
                    bkey = audit_outcome_key(batch)
                    dkey = audit_outcome_key(deploy)
                    if bkey != dkey:
                        outcome_mismatches.append(
                            {
                                "strategy": strategy_name,
                                "scenario": scenario,
                                "seed": seed,
                                "instrumentation": level,
                                "batch": bkey,
                                "deploy": dkey,
                            }
                        )

    return {
        "T": T,
        "seeds": seeds,
        "scenarios": list(scenarios),
        "strategies": list(strategies),
        "instrumentation_levels": list(instrumentation_levels),
        "n_checks": n_checks,
        "meta_mismatch_count": len(meta_mismatches),
        "outcome_mismatch_count": len(outcome_mismatches),
        "passed": not meta_mismatches and not outcome_mismatches,
        "meta_mismatches": meta_mismatches,
        "outcome_mismatches": outcome_mismatches,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Batch vs deployment API equivalence")
    parser.add_argument("--T", type=int, default=DEFAULT_T)
    parser.add_argument("--seeds", type=str, default=",".join(str(s) for s in DEFAULT_SEEDS))
    parser.add_argument("--smoke", action="store_true", help="Quick check: 2 seeds, T=500")
    args = parser.parse_args()

    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    T = args.T
    if args.smoke:
        seeds = [11, 12]
        T = 500

    strategies = tuple(STRATEGIES.keys())
    payload = run_equivalence_suite(
        seeds,
        T,
        REDTEAM_SCENARIOS,
        strategies,
        INSTRUMENTATION_LEVELS,
    )

    out_path = Path(__file__).resolve().parent / "results" / "api_equivalence.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"verify_api_equivalence: {'PASS' if payload['passed'] else 'FAIL'}")
    print(f"  checks={payload['n_checks']} meta_mismatches={payload['meta_mismatch_count']} "
          f"outcome_mismatches={payload['outcome_mismatch_count']}")
    print(f"  wrote {out_path}")

    if not payload["passed"]:
        for item in payload["meta_mismatches"][:5]:
            print(f"  meta: {item['strategy']}/{item['scenario']}/seed{item['seed']} "
                  f"({item['n_diffs']} diffs)")
        for item in payload["outcome_mismatches"][:10]:
            print(
                f"  outcome: {item['strategy']}/{item['scenario']}/seed{item['seed']}/"
                f"{item['instrumentation']} batch={item['batch']} deploy={item['deploy']}"
            )
        sys.exit(1)


if __name__ == "__main__":
    main()
