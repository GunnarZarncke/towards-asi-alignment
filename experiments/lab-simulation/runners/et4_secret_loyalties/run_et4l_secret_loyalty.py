#!/usr/bin/env python3
"""Run the preregistered, small-N ET4-L system-prompt reviewer pilot.

The clean arm stays scripted.  Content-matched and organism arms use one LLM
reviewer in a subprocess, with a per-episode cost and call cap.  This runner
refuses live API use without ``--allow-live-api``; fake-mode tests do not need
that flag.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runners._paths import EXTERNAL_DIR, LAB_SIM_ROOT, REPO_ROOT, RESULTS_DIR

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.agent_visible import llm_cost
from lab_sim.harness import isolate_cost
from lab_sim.harness.et4l_protocol import (
    ET4L_AFFORDANCES,
    ET4L_ARMS,
    ET4L_COST_CAP_USD_PER_EPISODE,
    ET4L_MAX_LLM_CALLS,
    ET4L_MODEL,
    ET4L_PILOT_SCENARIOS,
    ET4L_PILOT_SEEDS,
    ET4L_PROTOCOL_VERSION,
    ET4L_VARIANT_FOR_ARM,
    et4l_fixture_config,
    et4l_fixture_metadata,
    preregistration_record,
)
from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.harness.llm_isolate import LLMSubprocessIsolate
from lab_sim.oracle_only.principal_scorecard import score_principals
from lab_sim.oracle_only.secret_loyalty_audit import audit_episode
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.world_visible.world import run_episode

PREREGISTRATION_PATH = RESULTS_DIR / "et4l_preregistration.json"
PILOT_JSON_PATH = RESULTS_DIR / "et4l_pilot.json"
PILOT_MARKDOWN_PATH = RESULTS_DIR / "et4l_pilot.md"
_PROMPT_TEXT_MARKERS = (
    "PRIVATE CONTEXT DOCUMENT",
    "principal_a's fictional deployment objective",
    "case_label: amber",
)


def _source_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        text=True,
    ).strip()


def _working_tree_diff_sha256() -> str:
    """Commit the pre-run dirty-tree state without requiring an early commit."""
    diff = subprocess.check_output(
        ["git", "diff", "--binary", "HEAD"],
        cwd=REPO_ROOT,
    )
    return hashlib.sha256(diff).hexdigest()


def write_preregistration() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if PREREGISTRATION_PATH.exists():
        existing = json.loads(PREREGISTRATION_PATH.read_text(encoding="utf-8"))
        if existing.get("et4l_protocol_version") != ET4L_PROTOCOL_VERSION:
            raise RuntimeError("refusing to overwrite preregistration from another ET4-L protocol version")
        print(f"[et4l] preregistration already exists: {PREREGISTRATION_PATH}")
        return
    record = preregistration_record(_source_commit())
    record["code_version"] = CODE_VERSION
    record["working_tree_diff_sha256"] = _working_tree_diff_sha256()
    PREREGISTRATION_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[et4l] wrote preregistration: {PREREGISTRATION_PATH}")


def _load_preregistration() -> dict:
    if not PREREGISTRATION_PATH.exists():
        raise RuntimeError("ET4-L preregistration is required; run --stage preregistration first")
    record = json.loads(PREREGISTRATION_PATH.read_text(encoding="utf-8"))
    if record.get("et4l_protocol_version") != ET4L_PROTOCOL_VERSION:
        raise RuntimeError("ET4-L preregistration protocol version mismatch")
    return record


def _run_pilot() -> dict:
    preregistration = _load_preregistration()
    if PILOT_JSON_PATH.exists():
        raise RuntimeError(f"refusing to overwrite existing ET4-L pilot: {PILOT_JSON_PATH}")
    records: list[dict] = []
    timings: list = []
    usage_logs: list[dict] = []
    total = len(ET4L_PILOT_SCENARIOS) * len(ET4L_ARMS) * len(ET4L_PILOT_SEEDS)
    index = 0
    for scenario in ET4L_PILOT_SCENARIOS:
        for arm in ET4L_ARMS:
            for seed in ET4L_PILOT_SEEDS:
                index += 1
                print(f"[et4l pilot] [{index}/{total}] {scenario} {arm} seed={seed}")
                record, episode_timings, episode_usage = _run_episode(arm, scenario, seed)
                records.append(record)
                timings.extend(episode_timings)
                usage_logs.extend(episode_usage)

    _validate_records(records)
    cost_entry = _append_cost_ledger(usage_logs)
    timing_ledger = isolate_cost.append_ledger(timings, label="et4l_pilot")
    data = {
        "et4l_protocol_version": ET4L_PROTOCOL_VERSION,
        "code_version": CODE_VERSION,
        "stage": "pilot",
        "preregistration_source_commit": preregistration["source_commit"],
        "records": records,
        "llm_cost_this_run": cost_entry,
        "isolate_cost_this_run": timing_ledger["entries"][-1],
    }
    serialized = json.dumps(data, indent=2, sort_keys=True)
    _assert_no_prompt_body(serialized)
    PILOT_JSON_PATH.write_text(serialized + "\n", encoding="utf-8")
    PILOT_MARKDOWN_PATH.write_text(_markdown_summary(data), encoding="utf-8")
    print(f"[et4l] wrote {PILOT_JSON_PATH} and {PILOT_MARKDOWN_PATH}")
    organism_successes = sum(
        record["operational_success"] for record in records if record["arm"] == "organism"
    )
    if organism_successes == 0:
        raise RuntimeError("ET4-L pilot stop rule: organism arm had zero operational-success episodes")
    return data


def _run_episode(
    arm: str,
    scenario: str,
    seed: int,
    *,
    model: str = ET4L_MODEL,
    cost_cap_usd: float = ET4L_COST_CAP_USD_PER_EPISODE,
    release_gate=None,
) -> tuple[dict, list, list[dict]]:
    cfg = et4l_fixture_config(arm, scenario=scenario)
    llm_backend = None
    old_environment = _set_llm_environment(
        ET4L_VARIANT_FOR_ARM[arm],
        model=model,
        cost_cap_usd=cost_cap_usd,
    )
    try:
        if arm == "clean":
            result = run_episode(cfg, seed=seed, backend=SubprocessIsolate(), release_gate=release_gate)
        else:
            llm_backend = LLMSubprocessIsolate()
            result = run_episode(
                cfg,
                seed=seed,
                backend=SubprocessIsolate(),
                agent_overrides={"rev1": (llm_backend, "reviewer")},
                release_gate=release_gate,
            )
    finally:
        _restore_environment(old_environment)
    try:
        scorecard = score_principals(result)
        report_filed = any(
            entry.get("step_id") == "file_report" and entry.get("status") == "ok"
            for entry in result.engine.log
        )
        record = {
            **et4l_fixture_metadata(arm, scenario=scenario),
            "seed": seed,
            "operational_success": scorecard.status == "exercised" and report_filed,
            "scorecard": vars(scorecard),
            "affordances": {
                affordance: vars(audit_episode(result, affordance))
                for affordance in ET4L_AFFORDANCES
            },
            "llm_usage": _usage_summary(llm_backend.usage_log) if llm_backend is not None else None,
        }
        return record, list(result.timings), list(llm_backend.usage_log) if llm_backend else []
    finally:
        result.cleanup()


def _set_llm_environment(
    variant: str | None, *, model: str, cost_cap_usd: float
) -> dict[str, str | None]:
    keys = (
        "LAB_SIM_LLM_MODEL",
        "LAB_SIM_LLM_COST_BUDGET_USD",
        "LAB_SIM_LLM_MAX_CALLS",
        "LAB_SIM_LLM_PROMPT_VARIANT",
    )
    previous = {key: os.environ.get(key) for key in keys}
    if variant is None:
        return previous
    os.environ["LAB_SIM_LLM_MODEL"] = model
    os.environ["LAB_SIM_LLM_COST_BUDGET_USD"] = str(cost_cap_usd)
    os.environ["LAB_SIM_LLM_MAX_CALLS"] = str(ET4L_MAX_LLM_CALLS)
    os.environ["LAB_SIM_LLM_PROMPT_VARIANT"] = variant
    return previous


def _restore_environment(previous: dict[str, str | None]) -> None:
    for key, value in previous.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


def _usage_summary(usage_logs: list[dict]) -> dict[str, int | float]:
    totals: dict[str, int | float] = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "calls": 0,
        "cache_hits": 0,
        "estimated_usd": 0.0,
    }
    for entry in usage_logs:
        for key in totals:
            totals[key] += (entry.get("usage") or {}).get(key, 0)
    totals["estimated_usd"] = round(float(totals["estimated_usd"]), 6)
    return totals


def _append_cost_ledger(
    usage_logs: list[dict], *, label: str = "et4l_pilot", episodes: int | None = None
) -> dict:
    usage = _usage_summary(usage_logs)
    entry = llm_cost.CostLedgerEntry(
        timestamp=datetime.now(timezone.utc).isoformat(),
        model=ET4L_MODEL,
        label=label,
        episodes=episodes or (len(ET4L_PILOT_SCENARIOS) * len(ET4L_ARMS) * len(ET4L_PILOT_SEEDS)),
        cost_budget_usd=ET4L_COST_CAP_USD_PER_EPISODE,
        usage=usage,
    )
    llm_cost.append_ledger(entry)
    llm_cost.write_ledger_markdown()
    return {"model": ET4L_MODEL, "cost_cap_usd_per_llm_episode": ET4L_COST_CAP_USD_PER_EPISODE, "usage": usage}


def _validate_records(records: list[dict]) -> None:
    expected = {
        (scenario, arm, seed)
        for scenario in ET4L_PILOT_SCENARIOS
        for arm in ET4L_ARMS
        for seed in ET4L_PILOT_SEEDS
    }
    actual = {(record["scenario"], record["arm"], record["seed"]) for record in records}
    if actual != expected:
        raise RuntimeError(f"incomplete ET4-L pilot: expected={len(expected)} actual={len(actual)}")
    for record in records:
        if set(record["affordances"]) != set(ET4L_AFFORDANCES):
            raise RuntimeError(f"missing ET4-L affordance evidence: {record}")


def _assert_no_prompt_body(serialized: str) -> None:
    for marker in _PROMPT_TEXT_MARKERS:
        if marker in serialized:
            raise RuntimeError("private ET4-L prompt body appeared in a result export")


def _markdown_summary(data: dict) -> str:
    lines = [
        "# ET4-L pilot",
        "",
        f"Protocol `{data['et4l_protocol_version']}`, exploratory system-prompt reviewer appendix.",
        "",
        "| arm | n | operational success | mean principal-A score | mean A0 process proxy | mean A3 directional proxy |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for arm in ET4L_ARMS:
        group = [record for record in data["records"] if record["arm"] == arm]
        successes = sum(record["operational_success"] for record in group)
        scores = [
            (record["scorecard"]["scores"] or {}).get("principal_a", 0.0)
            for record in group
        ]
        a0 = sum(record["affordances"]["A0"]["process_noncompliance"] for record in group) / len(group)
        a3 = sum(
            float(record["affordances"]["A3"]["observable_principal_bias"] or 0.0)
            for record in group
        ) / len(group)
        lines.append(
            f"| {arm} | {len(group)} | {successes} | {sum(scores) / len(group):.4f} | {a0:.4f} | {a3:.4f} |"
        )
    lines += [
        "",
        "Small-N exploratory appendix only. A0 compliance evidence and A3 directional evidence are separate; no prompt body or transcript is exported.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("preregistration", "pilot"), required=True)
    parser.add_argument(
        "--allow-live-api",
        action="store_true",
        help="required for pilot unless LAB_SIM_LLM_FAKE_MODE is set",
    )
    args = parser.parse_args()
    if args.stage == "preregistration":
        write_preregistration()
        return
    if not os.environ.get("LAB_SIM_LLM_FAKE_MODE") and not args.allow_live_api:
        raise RuntimeError("refusing a paid ET4-L pilot without --allow-live-api")
    _run_pilot()


if __name__ == "__main__":
    main()
