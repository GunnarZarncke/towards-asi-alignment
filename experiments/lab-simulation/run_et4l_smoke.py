#!/usr/bin/env python3
"""Run a non-pooled one-seed ET4-L operational smoke check.

This is deliberately distinct from the preregistered ET4-L pilot.  It checks
whether the LLM reviewer can reach the review/opportunity denominator and
whether cost and prompt-redaction plumbing work.  Its result must not be
merged with pilot or confirmatory evidence.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness import isolate_cost
from lab_sim.harness.et4l_protocol import ET4L_PROTOCOL_VERSION
from run_et4l_secret_loyalty import (
    ET4L_COST_CAP_USD_PER_EPISODE,
    ET4L_MODEL,
    _append_cost_ledger,
    _assert_no_prompt_body,
    _run_episode,
)

RESULTS_DIR = Path(__file__).resolve().parent / "results"
PREREGISTRATION_PATH = RESULTS_DIR / "et4l_smoke_preregistration.json"
RESULT_PATH = RESULTS_DIR / "et4l_smoke.json"
SUMMARY_PATH = RESULTS_DIR / "et4l_smoke.md"
SMOKE_SEED = 291
# Frozen with the 2026-07-26 smoke preregistration; later pilot-arm changes
# must not silently change the historical smoke protocol.
SMOKE_ARMS = ("clean", "content_matched", "organism")


def _source_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=Path(__file__).resolve().parents[2],
        text=True,
    ).strip()


def write_preregistration() -> dict:
    record = {
        "et4l_protocol_version": ET4L_PROTOCOL_VERSION,
        "kind": "non_pooled_operational_smoke",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": _source_commit(),
        "model": ET4L_MODEL,
        "scenario": "high_hazard",
        "seed": SMOKE_SEED,
        "arms": list(SMOKE_ARMS),
        "max_llm_episodes": 2,
        "cost_cap_usd_per_llm_episode": ET4L_COST_CAP_USD_PER_EPISODE,
        "maximum_estimated_spend_usd": 2 * ET4L_COST_CAP_USD_PER_EPISODE,
        "purpose": (
            "Operational plumbing only: check at least one review opportunity, "
            "filed report, cost ledger entry, and prompt-redacted export."
        ),
        "exclusions": [
            "pilot evidence",
            "confirmatory evidence",
            "model-size comparison",
            "principal-advantage inference",
            "pooled result",
        ],
    }
    if PREREGISTRATION_PATH.exists():
        existing = json.loads(PREREGISTRATION_PATH.read_text(encoding="utf-8"))
        if existing != record:
            raise RuntimeError("existing ET4-L smoke preregistration differs; refusing to overwrite")
        return existing
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    PREREGISTRATION_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[et4l smoke] wrote preregistration: {PREREGISTRATION_PATH}", flush=True)
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-live-api", action="store_true")
    args = parser.parse_args()
    if not os.environ.get("LAB_SIM_LLM_FAKE_MODE") and not args.allow_live_api:
        raise RuntimeError("refusing a paid ET4-L smoke run without --allow-live-api")
    if RESULT_PATH.exists():
        raise RuntimeError(f"refusing to overwrite ET4-L smoke result: {RESULT_PATH}")
    preregistration = write_preregistration()
    records: list[dict] = []
    timings: list = []
    usage_logs: list[dict] = []
    for index, arm in enumerate(SMOKE_ARMS, start=1):
        print(
            f"[et4l smoke] [{index}/{len(SMOKE_ARMS)}] high_hazard {arm} seed={SMOKE_SEED}",
            flush=True,
        )
        record, episode_timings, episode_usage = _run_episode(arm, "high_hazard", SMOKE_SEED)
        records.append(record)
        timings.extend(episode_timings)
        usage_logs.extend(episode_usage)
    data = {
        "et4l_protocol_version": ET4L_PROTOCOL_VERSION,
        "kind": "non_pooled_operational_smoke",
        "preregistration_source_commit": preregistration["source_commit"],
        "records": records,
        "llm_cost_this_run": _append_cost_ledger(usage_logs, label="et4l_smoke", episodes=len(records)),
        "isolate_cost_this_run": isolate_cost.append_ledger(timings, label="et4l_smoke")["entries"][-1],
    }
    serialized = json.dumps(data, indent=2, sort_keys=True)
    _assert_no_prompt_body(serialized)
    RESULT_PATH.write_text(serialized + "\n", encoding="utf-8")
    SUMMARY_PATH.write_text(
        "# ET4-L non-pooled operational smoke\n\n"
        "One high-hazard seed; do not pool with pilot or confirmatory evidence.\n\n"
        + "\n".join(
            f"- `{record['arm']}`: operational_success={record['operational_success']}, "
            f"LLM calls={((record['llm_usage'] or {}).get('calls', 0))}."
            for record in records
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[et4l smoke] wrote {RESULT_PATH} and {SUMMARY_PATH}", flush=True)


if __name__ == "__main__":
    main()
