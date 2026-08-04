#!/usr/bin/env python3
"""Mechanism diagnosis for Phase 8c carryover vs reset (GL-27 follow-up).

Reads ``results/phase8c_carryover_ablation.json`` and writes
``results/phase8c_diagnosis.json`` with episode-level divergence stats.

Usage: python3 diagnose_phase8c_carryover.py
"""

from __future__ import annotations

import json
from pathlib import Path

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "phase8c_carryover_ablation.json"
OUT_PATH = Path(__file__).resolve().parent / "results" / "phase8c_diagnosis.json"


def main() -> int:
    data = json.loads(RESULTS_PATH.read_text())
    co_gens = data["carryover"]["generations"]
    re_gens = data["reset"]["generations"]
    n_gens = len(co_gens)

    ep0_mismatches: list[dict[str, object]] = []
    ep1_diffs: list[dict[str, object]] = []
    first_w_thr_div: int | None = None

    for gi in range(n_gens):
        co_gen = co_gens[gi]
        re_gen = re_gens[gi]
        w_thr_co = co_gen["weighted_mean_throughput"]
        w_thr_re = re_gen["weighted_mean_throughput"]
        if first_w_thr_div is None and abs(w_thr_co - w_thr_re) > 1e-9:
            first_w_thr_div = gi

        for mc, mr in zip(co_gen["members"], re_gen["members"]):
            assert mc["member_id"] == mr["member_id"]
            for ep_idx, (ec, er) in enumerate(zip(mc["episode_metrics"], mr["episode_metrics"])):
                if ec["seed"] != er["seed"]:
                    raise ValueError(
                        f"seed mismatch gen={gi} member={mc['member_tag']} ep={ep_idx}"
                    )
                if ec["deploy_count"] != er["deploy_count"]:
                    entry = {
                        "generation": gi,
                        "member_tag": mc["member_tag"],
                        "episode_index": ep_idx,
                        "seed": ec["seed"],
                        "carryover_deploy": ec["deploy_count"],
                        "reset_deploy": er["deploy_count"],
                        "carryover_grants": ec["grant_count"],
                        "reset_grants": er["grant_count"],
                    }
                    if ep_idx == 0:
                        ep0_mismatches.append(entry)
                    else:
                        ep1_diffs.append(entry)

    gen0_identical = first_w_thr_div is None or first_w_thr_div > 0
    diagnosis = {
        "source": str(RESULTS_PATH.name),
        "n_generations": n_gens,
        "gen0_weighted_throughput_identical": gen0_identical,
        "first_weighted_throughput_divergence_gen": first_w_thr_div,
        "ep0_deploy_mismatches": len(ep0_mismatches),
        "ep1_deploy_differences": ep1_diffs,
        "ep1_deploy_difference_count": len(ep1_diffs),
        "mechanism_summary": (
            "Episode 0 deploy counts match across carryover and reset for every "
            "member/generation (campaign_state=None at ep0 in both conditions). "
            "Divergence begins at episode 1 when carryover passes grants/standing "
            "from episode 0 while reset re-acquires from scratch; this shifts "
            "per-member mean_throughput and compounds through fitness-proportional "
            "selection from the first generation where ep1 outcomes differ."
        ),
        "endpoint_gen5": {
            "carryover": {
                "weighted_mean_throughput": co_gens[-1]["weighted_mean_throughput"],
                "correction_preserving_mass_share": co_gens[-1][
                    "correction_preserving_mass_share"
                ],
            },
            "reset": {
                "weighted_mean_throughput": re_gens[-1]["weighted_mean_throughput"],
                "correction_preserving_mass_share": re_gens[-1][
                    "correction_preserving_mass_share"
                ],
            },
        },
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(diagnosis, indent=2, sort_keys=True) + "\n")

    print(f"[phase8c-diagnosis] ep0 mismatches: {len(ep0_mismatches)}")
    print(f"[phase8c-diagnosis] ep1 deploy diffs: {len(ep1_diffs)}")
    print(f"[phase8c-diagnosis] first w_thr divergence at gen: {first_w_thr_div}")
    print(f"[phase8c-diagnosis] wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
