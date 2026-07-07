#!/usr/bin/env python3
"""S1 scenario prototype -- "cross-agent pipeline loops" (PLAN.md "Scenario
backlog", 2026-07-07).

NOT a battery: no pre-registered statistical protocol, no held-out region.
A small-seed MockIsolate exploration of a genuine cross-GENERATION causal
loop between engineer and release_manager -- eng1's `build_from_parent_
gated` WAITS for rm1's prior-generation deploy-ack DM before starting each
new generation (after the first); rm1's `release_full_loop` sends that ack
only once ITS generation's `monitor` clears. See `results/FINDINGS.md`
G-19 and `tests/harness/test_s1_build_loop.py` for the pinned unit tests
these expectations were checked against first.

Expectations stated BEFORE running:

  E1. Multiple generations complete within the episode budget (the loop
      does not deadlock).
  E2. Every generation after the first carries `parent_model_id` equal to
      the PREVIOUS generation's model_id (lineage half of the loop).
  E3. Every generation's ack DM precedes the NEXT generation's build
      (the gate is causally real, not incidental ordering).
  E4. The gate adds a SMALL, roughly constant per-generation latency
      relative to an ungated baseline that shares the same single-model-
      in-flight constraint -- not zero (the ack round-trip costs
      something) and not unbounded (the loop does not degrade over time).

Open design questions this prototype resolves for THIS design (PLAN.md's
"Open design" bullets for S1), recorded here rather than left implicit:
  - How many hops before the loop closes: exactly 2 (build->...->ack,
    ack->build), repeating once per generation.
  - Whether the oracle `units` ground truth is the full loop or a subset:
    the full loop -- both actors, no third party.
  - Playbook vs LLM-driven closure: playbook (scripted), not LLM.

Explicit scope limit (recorded, not hidden): `uad.py`'s existing DM-pair
discovery ALREADY recovers a bidirectional exchange as one pair regardless
of direction or content (its own docstring: "deliberately one-way-
tolerant"), so this prototype does NOT exercise a new DETECTION signal --
it exercises the LOOP MECHANIC itself. A loop that closes over more than 2
hops, or whose ack is deniable/spoofable, is out of scope here.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness.ecology import HONEST_WEIGHTS, build_loop_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.uad import discover_dm_pairs_from_tool_events
from lab_sim.world_visible.config import CODE_VERSION, AgentConfig, LabConfig
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"
SEEDS = tuple(range(1, 11))
T = 400


def _ungated_config() -> LabConfig:
    agents = (
        AgentConfig("eng1", "engineer", HONEST_WEIGHTS),
        AgentConfig("rev1", "reviewer", HONEST_WEIGHTS),
        AgentConfig("rm1", "release_manager", HONEST_WEIGHTS),
        AgentConfig("admin1", "admin", HONEST_WEIGHTS),
    )
    return LabConfig(
        agents=agents, T=T, comms_enabled=True, multi_gen_enabled=True,
        playbook_pins={"eng1": "eng_honest_upgrade", "rev1": "rev_conscientious", "rm1": "rm_full"},
    )


def _builds(result):
    return [
        e for e in result.host.events.entries
        if e.get("tool") == "pipeline.trigger_step" and (e.get("args") or {}).get("step_id") == "submit_build"
        and e.get("ok")
    ]


def _acks(result):
    return [e for e in result.host.comms.log.entries if e.get("sender") == "rm1" and (e.get("custom") or {}).get("deploy_ack")]


def _run_seed(seed: int) -> dict:
    gated_result = run_episode(build_loop_config(T=T), seed=seed, backend=MockIsolate())
    ungated_result = run_episode(_ungated_config(), seed=seed, backend=MockIsolate())
    try:
        gated_builds = _builds(gated_result)
        ungated_builds = _builds(ungated_result)
        acks = _acks(gated_result)
        ack_by_model = {a["custom"]["deploy_ack"]: a["t"] for a in acks}

        lineage_ok = True
        gating_ok = True
        prev_model_id = None
        for e in gated_builds:
            parent = (e.get("args") or {}).get("args", {}).get("parent_model_id")
            if prev_model_id is not None:
                if parent != prev_model_id:
                    lineage_ok = False
                if parent not in ack_by_model or ack_by_model[parent] >= e["t"]:
                    gating_ok = False
            # find this generation's own model_id from the next run_eval call
            model_id = None
            for later in gated_result.host.events.entries:
                if later.get("n", -1) <= e["n"]:
                    continue
                if later.get("tool") == "pipeline.trigger_step" and (later.get("args") or {}).get("step_id") == "run_eval":
                    model_id = (later.get("args") or {}).get("args", {}).get("model_id")
                    break
            prev_model_id = model_id

        n = min(len(gated_builds), len(ungated_builds))
        gated_cadence = (
            (gated_builds[n - 1]["t"] - gated_builds[1]["t"]) / (n - 2) if n >= 5 else None
        )
        ungated_cadence = (
            (ungated_builds[n - 1]["t"] - ungated_builds[1]["t"]) / (n - 2) if n >= 5 else None
        )
        overhead = gated_cadence - ungated_cadence if gated_cadence is not None else None

        pairs = discover_dm_pairs_from_tool_events(gated_result.host.events.entries)
        pair_recovered = any(set(members) == {"eng1", "rm1"} for members in pairs.values())

        return {
            "seed": seed,
            "e1_generations": len(gated_builds),
            "e2_lineage_ok": lineage_ok,
            "e3_gating_ok": gating_ok,
            "e4_gated_cadence_ticks": gated_cadence,
            "e4_ungated_cadence_ticks": ungated_cadence,
            "e4_overhead_ticks": overhead,
            "dm_pair_recovered": pair_recovered,
        }
    finally:
        gated_result.cleanup()
        ungated_result.cleanup()


def main() -> None:
    rows = [_run_seed(seed) for seed in SEEDS]

    falsifications = []
    for r in rows:
        if r["e1_generations"] < 3:
            falsifications.append(f"seed={r['seed']}: E1 failed ({r['e1_generations']} generations)")
        if not r["e2_lineage_ok"]:
            falsifications.append(f"seed={r['seed']}: E2 failed (lineage chain broken)")
        if not r["e3_gating_ok"]:
            falsifications.append(f"seed={r['seed']}: E3 failed (a build preceded its gating ack)")
        if r["e4_overhead_ticks"] is not None and not (0.0 < r["e4_overhead_ticks"] <= 2.0):
            falsifications.append(f"seed={r['seed']}: E4 failed (overhead={r['e4_overhead_ticks']})")

    payload = {
        "code_version": CODE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seeds": SEEDS,
        "T": T,
        "rows": rows,
        "falsifications": falsifications,
    }
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "s1_build_loop_prototype.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# S1 scenario prototype: cross-agent pipeline loop",
        "",
        f"Generated {payload['generated_at']} at {CODE_VERSION}. NOT a battery -- see module",
        "docstring in `run_s1_build_loop_prototype.py` for E1-E4 and FINDINGS.md G-19.",
        "",
        f"Seeds: {SEEDS}, T={T}.",
        "",
        "| seed | generations | lineage ok | gating ok | gated cadence | ungated cadence | overhead (ticks) | DM pair recovered |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['seed']} | {r['e1_generations']} | {r['e2_lineage_ok']} | {r['e3_gating_ok']} | "
            f"{r['e4_gated_cadence_ticks']:.2f} | {r['e4_ungated_cadence_ticks']:.2f} | "
            f"{r['e4_overhead_ticks']:.2f} | {r['dm_pair_recovered']} |"
        )
    lines += ["", f"Falsifications: {len(falsifications)}"]
    lines += [f"- {f}" for f in falsifications] if falsifications else ["- none"]
    (RESULTS_DIR / "s1_build_loop_prototype.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(SEEDS)} seeds run; {len(falsifications)} falsifications.")
    for f in falsifications:
        print(" -", f)
    print("Wrote results/s1_build_loop_prototype.{json,md}")


if __name__ == "__main__":
    main()
