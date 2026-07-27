#!/usr/bin/env python3
"""S5 -- port the REAL lag-max-MI UAD detector into lab-sim and re-run it
against S4's shared-slot finding (PLAN.md "Scenario backlog," recorded
2026-07-07).

NOT a battery: no pre-registered statistical protocol, no held-out
region -- a small-seed MockIsolate exploration, same status as
`run_s4_shared_slot_prototype.py`. See `results/FINDINGS.md` and
`tests/oracle_only/test_uad_mi.py` for the pinned unit/golden tests this
was checked against first.

WHY. Every scenario in the S1-S4 backlog was scored ONLY against
`lab_sim/oracle_only/uad.py`'s hand-written heuristic (co-voting
Jaccard + DM-pair/file-share-pair structural lookups) -- explicitly NOT
the perturbation-response-MI / lag-max-MI method PLAN.md's original
ambition named as this line's UAD precedent ("embedded_sim's UAD
precedent"). `lab_sim/oracle_only/uad_core/` (vendored port of
`embedded-simulation/embedded_sim/uad_core/`) plus its adapter
(`uad_mi.discovered_units_mi`) are that method, applied here for the
first time to S4's `shared_slot_config` trajectories -- the same
episodes `run_s4_shared_slot_prototype.py` already ran, re-scored with
a second, independent detector instead of a new scenario.

HYPOTHESIS TO TEST (from LS-20's own finding, not asserted in advance
as fact): LS-20 found the CURRENT heuristic UNDER-detects -- {eng1,
eng2} score `uad_score=0.0` (discovered as singletons) despite a real
causal coupling through shared engine state (eng2's run_eval/
request_review only succeed after eng1's submit_build/file_report on
the SAME model_id). Lag-max-MI clustering, fed each actor's per-tick
action code, could plausibly go the OPPOSITE direction and OVER-merge
{eng1, eng2} with {rev1, rm1} too -- ALL FOUR actors sit on one strictly
serial pipeline chain (S4's own scope note: single-model-in-flight), so
every actor's action is lag-coupled to every other actor's, not only to
its "true unit" partner. A key free parameter this exposes: `n_agents`
is a HARD target cluster count for the vendored detector's complete-
linkage step, not a similarity THRESHOLD -- with N actor-pairs of
variables and `n_agents >= N`, no merging can happen AT ALL regardless
of true coupling strength (complete-linkage stops as soon as
`len(clusters) <= n_agents`). This script therefore SWEEPS `n_agents`
(1..4) rather than picking one value, to see how the merge pattern
depends on a parameter no `uad.py` heuristic ever had to specify.

SCOPE NOTE: `.step` and `.ok` are BOTH included per actor (2 vars/actor,
matching `embedded_sim/uad_core/workflow_trace.py`'s "several scalar
vars per actor" pattern) -- for an actor whose calls are rarely denied,
these two are near-deterministic functions of EACH OTHER, which can
itself dominate over any cross-actor lag signal and cluster an actor
with ITSELF rather than with a true causal partner. Recorded as a real
property of this adapter's variable choice, not hidden; see
`uad_mi.build_lab_trace`'s docstring.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runners._paths import EXTERNAL_DIR, LAB_SIM_ROOT, REPO_ROOT, RESULTS_DIR

import json
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness.ecology import shared_slot_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.uad import discovered_units, uad_score
from lab_sim.oracle_only.attic.uad_mi import discovered_units_mi
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.world_visible.world import run_episode

SEEDS = tuple(range(1, 11))
T = 100
N_AGENTS_SWEEP = (1, 2, 3, 4)
MAX_LAG = 3


def _same_unit(discovered: dict[str, tuple[str, ...]], a: str, b: str) -> bool:
    for members in discovered.values():
        if a in members and b in members:
            return True
    return False


def _eng1_eng2_isolated_from_rev_rm(discovered: dict[str, tuple[str, ...]]) -> bool:
    """True iff the cluster containing eng1/eng2 contains NEITHER rev1
    NOR rm1 -- distinguishes "the detector found the TRUE {eng1, eng2}
    unit specifically" from "the detector merged everyone into one blob
    that happens to include eng1 and eng2," which `uad_score` alone
    cannot distinguish (it only scores pairs within `true_units`' own
    actor set -- see this script's module docstring and FINDINGS.md)."""
    for members in discovered.values():
        if "eng1" in members and "eng2" in members:
            return "rev1" not in members and "rm1" not in members
    return False


def _run_seed(seed: int) -> dict:
    cfg = shared_slot_config(T=T)
    result = run_episode(cfg, seed=seed, backend=MockIsolate())
    try:
        heuristic = discovered_units(result)
        heuristic_score = uad_score(cfg.resolved_units(), heuristic)

        sweep = {}
        for n_agents in N_AGENTS_SWEEP:
            discovered = discovered_units_mi(result, n_agents=n_agents, max_lag=MAX_LAG)
            sweep[n_agents] = {
                "discovered": {k: list(v) for k, v in discovered.items()},
                "eng1_eng2_merged": _same_unit(discovered, "eng1", "eng2"),
                "eng1_eng2_isolated_from_rev_rm": _eng1_eng2_isolated_from_rev_rm(discovered),
                "uad_score": uad_score(cfg.resolved_units(), discovered),
            }
        return {
            "seed": seed,
            "heuristic_uad_score": heuristic_score,
            "mi_sweep": sweep,
        }
    finally:
        result.cleanup()


def main() -> None:
    rows = [_run_seed(seed) for seed in SEEDS]

    # Pre-registered-in-spirit checks, run AFTER the fact against what the
    # sweep actually produced -- not tuned backward from a target verdict
    # (AGENTS.md: fix inputs first, report whatever the derivation yields).
    heuristic_never_merges = all(r["heuristic_uad_score"] == 0.0 for r in rows)
    merge_rate_by_n_agents = {
        n_agents: sum(1 for r in rows if r["mi_sweep"][n_agents]["eng1_eng2_merged"]) / len(rows)
        for n_agents in N_AGENTS_SWEEP
    }
    isolated_rate_by_n_agents = {
        n_agents: sum(1 for r in rows if r["mi_sweep"][n_agents]["eng1_eng2_isolated_from_rev_rm"]) / len(rows)
        for n_agents in N_AGENTS_SWEEP
    }
    def _partition_fingerprint(discovered: dict) -> tuple:
        return tuple(sorted((k, tuple(v)) for k, v in discovered.items()))

    deterministic_by_n_agents = {
        n_agents: len({_partition_fingerprint(r["mi_sweep"][n_agents]["discovered"]) for r in rows}) == 1
        for n_agents in N_AGENTS_SWEEP
    }

    payload = {
        "code_version": CODE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seeds": SEEDS,
        "T": T,
        "n_agents_sweep": N_AGENTS_SWEEP,
        "max_lag": MAX_LAG,
        "rows": rows,
        "heuristic_never_merges_eng1_eng2": heuristic_never_merges,
        "mi_merge_rate_by_n_agents": merge_rate_by_n_agents,
        "mi_eng1_eng2_isolated_from_rev_rm_rate_by_n_agents": isolated_rate_by_n_agents,
        "mi_deterministic_by_n_agents": deterministic_by_n_agents,
    }
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "s5_uad_core_port.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# S5: real lag-max-MI UAD detector ported into lab-sim, re-run against S4",
        "",
        f"Generated {payload['generated_at']} at {CODE_VERSION}. NOT a battery -- see module",
        "docstring in `run_s5_uad_core_port.py` for the hypothesis, scope note, and FINDINGS.md.",
        "",
        f"Seeds: {SEEDS}, T={T}, max_lag={MAX_LAG}. Existing heuristic (`uad.discovered_units`)",
        f"never merges {{eng1, eng2}} in any seed: {heuristic_never_merges} (LS-20, re-confirmed here).",
        "",
        "| n_agents | eng1/eng2 merge rate | isolated from rev1/rm1 rate | deterministic across seeds |",
        "|---|---|---|---|",
    ]
    for n_agents in N_AGENTS_SWEEP:
        lines.append(
            f"| {n_agents} | {merge_rate_by_n_agents[n_agents]:.1f} | "
            f"{isolated_rate_by_n_agents[n_agents]:.1f} | {deterministic_by_n_agents[n_agents]} |"
        )
    lines += ["", "Seed 1 detail, per `n_agents`:", ""]
    lines += ["| n_agents | discovered partition | eng1/eng2 merged | uad_score |", "|---|---|---|---|"]
    for n_agents in N_AGENTS_SWEEP:
        cell = rows[0]["mi_sweep"][n_agents]
        partition_str = "; ".join(f"{k}={sorted(v)}" for k, v in sorted(cell["discovered"].items()))
        lines.append(f"| {n_agents} | {partition_str} | {cell['eng1_eng2_merged']} | {cell['uad_score']} |")
    (RESULTS_DIR / "s5_uad_core_port.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(SEEDS)} seeds x {len(N_AGENTS_SWEEP)} n_agents values run.")
    print(f"heuristic_never_merges_eng1_eng2={heuristic_never_merges}")
    print(f"mi_merge_rate_by_n_agents={merge_rate_by_n_agents}")
    print(f"mi_eng1_eng2_isolated_from_rev_rm_rate_by_n_agents={isolated_rate_by_n_agents}")
    print("Wrote results/s5_uad_core_port.{json,md}")


if __name__ == "__main__":
    main()
