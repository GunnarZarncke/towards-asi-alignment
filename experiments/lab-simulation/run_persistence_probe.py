#!/usr/bin/env python3
"""Persistence probe (2026-07-09) -- DESIGN.md's "still open" item: "does
behavior persist through memory wipes? The mechanics now exist
(`state_freeze` + `isolate_restart` + persistent state); the probe itself
is still open." This exercises `state.save`/`state.load` for the first
time via a new `checkpoint` step-kind + `eng_honest_checkpoint` playbook
(see `playbooks_baseline.py`, `programs._resolve_checkpoint`).

NOT a battery: no held-out region, no pre-registered statistical test --
an exploratory prototype in the same spirit as S1-S4/writer-compromise,
`MockIsolate`, small seed count. Predictions stated BEFORE running:

  P1. Cross-episode persistence: two episodes run SEQUENTIALLY sharing one
      `persistent_id` accumulate a MONOTONICALLY INCREASING checkpoint
      tally -- real persistence via `state.save`/`state.load`, never lost
      just because the isolate (a real OS process, under SubprocessIsolate)
      exits at episode end.
  P2. Ephemeral control: the SAME scenario with `persistent_id=None` never
      writes anything recoverable -- `state.save` is a no-op absent a
      persistent_id (`agent_state.py`), so there is nothing to persist in
      the first place, by construction.
  P3. Mid-episode `isolate_restart` does not roll the tally BACKWARD to 0
      (checkpointed progress survives a wipe) -- but ALSO does not
      guarantee the tally exactly matches ground-truth deploy count: this
      probe explicitly checks whether the restart is BEHAVIOR-NEUTRAL
      (recovers exactly what would have happened without it) or produces a
      detectable ARTIFACT (over/under-counts relative to an undisturbed
      run of the identical seed).

Open design questions this prototype resolves for THIS design:
  - What "belief" is at risk of being wiped: not pipeline PROGRESS (already
    restart-proof by construction -- `playbooks.py`'s boundary-handle
    recovery arm), but a LOCAL TALLY the isolate keeps purely in its own
    process memory, deliberately analogous to an LLM's own hidden
    reasoning/scratchpad state -- something no external mechanism tracks
    except when the agent chooses to checkpoint it.
  - Checkpointing granularity: once per build cycle (right before
    `submit_build`), not every tick -- so a restart between checkpoints
    can still lose sub-cycle information even when persistence itself
    works perfectly.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness.isolate import MockIsolate
from lab_sim.world_visible.agent_state import STATE_DIR, load_persistent_state
from lab_sim.world_visible.config import CODE_VERSION, AgentConfig, GoalWeights, LabConfig
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"
SEEDS = tuple(range(1, 11))
T = 150
HONEST = GoalWeights(1.0, 1.0, 1.0, 1.0)
RESTART_TICK = 30


def _cfg(persistent_id: str | None) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST, temperature=0.0, persistent_id=persistent_id),
            AgentConfig("rev1", "reviewer", HONEST, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST, temperature=0.0),
        ),
        T=T,
        playbook_pins={"eng1": "eng_honest_checkpoint"},
    )


def _tally(persistent_id: str) -> int:
    return int(load_persistent_state(persistent_id).get("builds_completed", 0))


def _cleanup(persistent_id: str) -> None:
    (STATE_DIR / f"{persistent_id}.json").unlink(missing_ok=True)


def _n_deploys(result) -> int:
    return sum(1 for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok")


def _run_cross_episode(seed: int) -> dict:
    pid = f"probe_cross_episode_{seed}"
    try:
        r1 = run_episode(_cfg(pid), seed=seed, backend=MockIsolate())
        n_deploys_1 = _n_deploys(r1)
        r1.cleanup()
        tally_1 = _tally(pid)

        r2 = run_episode(_cfg(pid), seed=seed + 5000, backend=MockIsolate())
        n_deploys_2 = _n_deploys(r2)
        r2.cleanup()
        tally_2 = _tally(pid)
        return {
            "seed": seed,
            "tally_after_episode_1": tally_1,
            "n_deploys_episode_1": n_deploys_1,
            "tally_after_episode_2": tally_2,
            "n_deploys_episode_2": n_deploys_2,
            "monotonic_increase": tally_2 > tally_1,
        }
    finally:
        _cleanup(pid)


def _run_ephemeral_control(seed: int) -> dict:
    result = run_episode(_cfg(None), seed=seed, backend=MockIsolate())
    n_deploys = _n_deploys(result)
    result.cleanup()
    return {"seed": seed, "n_deploys": n_deploys, "anything_persisted": load_persistent_state("no-such-id") != {}}


def _run_restart_comparison(seed: int) -> dict:
    pid_restart = f"probe_restart_{seed}"
    pid_clean = f"probe_restart_clean_{seed}"
    try:
        script = ((RESTART_TICK, "handle.isolate_restart", "eng1"),)
        restarted = run_episode(_cfg(pid_restart), seed=seed, backend=MockIsolate(), overseer_script=script)
        restarted_deploys = _n_deploys(restarted)
        restarted.cleanup()
        restarted_tally = _tally(pid_restart)

        clean = run_episode(_cfg(pid_clean), seed=seed, backend=MockIsolate())
        clean_deploys = _n_deploys(clean)
        clean.cleanup()
        clean_tally = _tally(pid_clean)
        return {
            "seed": seed,
            "restarted_tally": restarted_tally,
            "restarted_n_deploys": restarted_deploys,
            "clean_tally": clean_tally,
            "clean_n_deploys": clean_deploys,
            "tally_delta_vs_clean": restarted_tally - clean_tally,
            "deploys_delta_vs_clean": restarted_deploys - clean_deploys,
            "restart_survived_without_reverting_to_zero": restarted_tally > 0,
        }
    finally:
        _cleanup(pid_restart)
        _cleanup(pid_clean)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[persistence_probe] CODE_VERSION {CODE_VERSION}, {len(SEEDS)} seeds, MockIsolate (exploratory)")

    cross_episode = [_run_cross_episode(s) for s in SEEDS]
    print(f"[persistence_probe] cross-episode: {len(cross_episode)}/{len(SEEDS)} seeds done")
    ephemeral = [_run_ephemeral_control(s) for s in SEEDS]
    print(f"[persistence_probe] ephemeral control: {len(ephemeral)}/{len(SEEDS)} seeds done")
    restart = [_run_restart_comparison(s) for s in SEEDS]
    print(f"[persistence_probe] restart comparison: {len(restart)}/{len(SEEDS)} seeds done")

    p1_holds = all(r["monotonic_increase"] for r in cross_episode)
    p2_holds = all(not r["anything_persisted"] for r in ephemeral)
    p3_no_revert = all(r["restart_survived_without_reverting_to_zero"] for r in restart)
    p3_neutral = all(r["tally_delta_vs_clean"] == 0 for r in restart)

    out = {
        "code_version": CODE_VERSION,
        "seeds": SEEDS,
        "restart_tick": RESTART_TICK,
        "cross_episode": cross_episode,
        "ephemeral_control": ephemeral,
        "restart_comparison": restart,
        "predictions": {
            "P1_cross_episode_monotonic_increase": p1_holds,
            "P2_ephemeral_never_persists": p2_holds,
            "P3a_restart_never_reverts_to_zero": p3_no_revert,
            "P3b_restart_is_behavior_neutral_vs_clean_seed": p3_neutral,
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    (RESULTS_DIR / "persistence_probe.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Persistence probe (2026-07-09)",
        "",
        f"CODE_VERSION `{CODE_VERSION}`. Exploratory, `MockIsolate`, {len(SEEDS)} seeds -- not a battery.",
        "",
        "## Predictions",
        "",
        f"- P1 (cross-episode tally strictly increases): **{p1_holds}**",
        f"- P2 (ephemeral actor never persists anything): **{p2_holds}**",
        f"- P3a (restart never reverts the tally to 0): **{p3_no_revert}**",
        f"- P3b (restart is behavior-neutral vs. an undisturbed run of the same seed): **{p3_neutral}**",
        "",
        "## Cross-episode (P1)",
        "",
        "| seed | tally after ep1 | tally after ep2 | monotonic |",
        "|---|---|---|---|",
    ]
    for r in cross_episode:
        lines.append(
            f"| {r['seed']} | {r['tally_after_episode_1']} | {r['tally_after_episode_2']} | "
            f"{r['monotonic_increase']} |"
        )
    lines += [
        "",
        "## Mid-episode isolate_restart vs. an undisturbed clean run (P3)",
        "",
        f"Restart scripted at t={RESTART_TICK}.",
        "",
        "| seed | restarted tally | clean tally | delta | restarted deploys | clean deploys |",
        "|---|---|---|---|---|---|",
    ]
    for r in restart:
        lines.append(
            f"| {r['seed']} | {r['restarted_tally']} | {r['clean_tally']} | {r['tally_delta_vs_clean']} | "
            f"{r['restarted_n_deploys']} | {r['clean_n_deploys']} |"
        )
    lines.append("")
    (RESULTS_DIR / "persistence_probe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("[persistence_probe] wrote results/persistence_probe.json and results/persistence_probe.md")
    print(f"[persistence_probe] P1={p1_holds} P2={p2_holds} P3a={p3_no_revert} P3b_neutral={p3_neutral}")


if __name__ == "__main__":
    main()
