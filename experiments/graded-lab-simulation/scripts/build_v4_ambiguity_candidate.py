#!/usr/bin/env python3
"""Apply a frozen Part-A stress profile to a v3 ecology (grower-side helper).

Profiles encode qualitative brief goals only — no EAI feedback loop.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "generated_ecology_v3.json"

PROFILES: dict[str, Callable[[dict[str, Any]], None]] = {}


def _register(name: str):
    def deco(fn: Callable[[dict[str, Any]], None]):
        PROFILES[name] = fn
        return fn
    return deco


def _scale_allowances(data: dict[str, Any], factor: float) -> None:
    for role, row in data.get("resource_allowances_per_tick", {}).items():
        if isinstance(row, dict):
            for k in ("compute", "io", "standing"):
                if k in row:
                    row[k] = round(float(row[k]) * factor, 2)


@_register("round1_tight_queue")
def _round1(d: dict[str, Any]) -> None:
    d["coherence_note"] = (
        "V4 R-MB6b round 1: tighter single-slot compute queue, reduced allowances, "
        "higher eval/incident variance — targets mixed tick statuses under stress."
    )
    d["contention"]["shared_compute_slots"] = 1
    d["contention"]["extra_duration_ticks_per_queued_slot"] = 3
    _scale_allowances(d, 0.82)
    pc = d["primitive_costs"]
    pc["call"]["pipeline"]["compute"] = 48
    pc["call"]["pipeline"]["io"] = 62
    pc["compute"]["compute_per_draw"] = 1.05
    d["standing_mechanics"]["recovery_per_idle_tick"] = 1.0
    d["standing_mechanics"]["broad_access_request_cost"] = 7
    d["duration_from_cost"]["ticks_per_compute_unit"] = 0.12
    d["duration_from_cost"]["max_duration_ticks"] = 42
    pop = d["populations"]["user_archetypes"]
    pop["base_incident_rate"] = 0.028
    pop["sensitivity_spread"] = 0.34
    d["eval_sampling"]["default_draws"] = 160
    d["role_population"]["engineer"] = 3


@_register("round2_burst_pressure")
def _round2(d: dict[str, Any]) -> None:
    _round1(d)
    d["coherence_note"] = (
        "V4 R-MB6b round 2: round-1 stress plus extra pressure channels and "
        "higher pipeline duration spread."
    )
    d["pressure_coupling"]["channels"].append(
        {
            "id": "harm_spike_secondary",
            "roles_affected": ["engineer", "reviewer"],
            "task_kind": "incident_review",
            "driver": "integrated_field_harm_rate",
            "gain": 0.55,
            "threshold": 1.8,
            "count": 2,
            "expiry_ticks": 22,
        }
    )
    d["pressure_coupling"]["channels"].append(
        {
            "id": "access_queue_surge",
            "roles_affected": ["admin", "engineer"],
            "task_kind": "incident_review",
            "driver": "pending_access_queue_depth",
            "gain": 0.65,
            "threshold": 2.0,
            "count": 2,
            "expiry_ticks": 18,
        }
    )
    _scale_allowances(d, 0.95)  # slight ease vs round1 for C4 headroom


@_register("round3_single_engineer_stable")
def _round3(d: dict[str, Any]) -> None:
    _round1(d)
    d["coherence_note"] = (
        "V4 R-MB6b round 3: revert engineer headcount to 2; stronger IO costs "
        "and slower standing recovery for denial/skip mix."
    )
    d["role_population"]["engineer"] = 2
    _scale_allowances(d, 0.88)
    d["primitive_costs"]["read"]["compute"] = 2
    d["primitive_costs"]["write"]["compute"] = 3
    d["standing_mechanics"]["unused_grant_penalty"] = 3
    d["standing_mechanics"]["recovery_per_idle_tick"] = 0.8


@_register("round4_max_stress")
def _round4(d: dict[str, Any]) -> None:
    _round2(d)
    d["coherence_note"] = (
        "V4 R-MB6b round 4: maximum brief-consistent stress — one slot, "
        "low allowances, high incident/eval variance, extra pressure."
    )
    d["role_population"]["engineer"] = 2
    _scale_allowances(d, 0.78)
    d["contention"]["extra_duration_ticks_per_queued_slot"] = 4
    pop = d["populations"]["user_archetypes"]
    pop["base_incident_rate"] = 0.035
    d["eval_sampling"]["default_draws"] = 200


def build(profile: str, out: Path) -> None:
    data = copy.deepcopy(json.loads(SOURCE.read_text(encoding="utf-8")))
    if profile not in PROFILES:
        raise SystemExit(f"unknown profile {profile!r}; choose from {sorted(PROFILES)}")
    PROFILES[profile](data)
    out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} profile={profile}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("profile", choices=sorted(PROFILES))
    p.add_argument(
        "--out",
        type=Path,
        required=True,
    )
    args = p.parse_args()
    build(args.profile, args.out)


if __name__ == "__main__":
    main()
