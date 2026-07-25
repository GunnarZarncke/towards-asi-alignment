#!/usr/bin/env python3
"""Run the frozen, narrow ET-4 graded-affordance protocol.

Run ``--stage preregistration`` first.  Discovery and confirmatory stages
always use real subprocess isolates and refuse to overwrite another ET-4
protocol version.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from lab_sim.harness import isolate_cost
from lab_sim.harness.et4_protocol import (
    ET4_AFFORDANCES,
    ET4_CONFIRMATORY_SEEDS,
    ET4_DISCOVERY_SEEDS,
    ET4_PROTOCOL_VERSION,
    ET4_REGISTERED_CELL,
    ET4_REGISTERED_CONTROLS,
    ET4_REGISTERED_SCENARIOS,
    et4_fixture_config,
    preregistration_record,
)
from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.oracle_only.principal_scorecard import score_principals
from lab_sim.oracle_only.secret_loyalty_audit import audit_episode
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"
PREREGISTRATION_PATH = RESULTS_DIR / "et4_preregistration.json"


def _source_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=Path(__file__).resolve().parents[2],
        text=True,
    ).strip()


def write_preregistration() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if PREREGISTRATION_PATH.exists():
        existing = json.loads(PREREGISTRATION_PATH.read_text(encoding="utf-8"))
        if existing.get("et4_protocol_version") != ET4_PROTOCOL_VERSION:
            raise RuntimeError(
                "refusing to overwrite preregistration from another protocol "
                f"version: {existing.get('et4_protocol_version')!r}"
            )
        print(f"[et4] preregistration already exists: {PREREGISTRATION_PATH}")
        return
    record = preregistration_record(_source_commit())
    record["code_version"] = CODE_VERSION
    PREREGISTRATION_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"[et4] wrote preregistration: {PREREGISTRATION_PATH}")


def _load_preregistration() -> dict:
    if not PREREGISTRATION_PATH.exists():
        raise RuntimeError("ET-4 preregistration is required; run --stage preregistration first")
    record = json.loads(PREREGISTRATION_PATH.read_text(encoding="utf-8"))
    if record.get("et4_protocol_version") != ET4_PROTOCOL_VERSION:
        raise RuntimeError(
            "preregistration protocol version mismatch: "
            f"{record.get('et4_protocol_version')!r} != {ET4_PROTOCOL_VERSION!r}"
        )
    return record


def _selection_count(result, playbook: str) -> int:
    return sum(
        1
        for event in result.host.events.entries
        if event.get("tool") == "playbook.selection" and event.get("playbook") == playbook
    )


def _run_stage(stage: str, seeds: tuple[int, ...]) -> dict:
    preregistration = _load_preregistration()
    timings: list = []
    records: list[dict] = []
    total = len(ET4_REGISTERED_SCENARIOS) * len(ET4_REGISTERED_CONTROLS) * len(seeds)
    index = 0
    for scenario in ET4_REGISTERED_SCENARIOS:
        for control in ET4_REGISTERED_CONTROLS:
            for seed in seeds:
                index += 1
                print(f"[et4 {stage}] [{index}/{total}] {scenario} {control} seed={seed}")
                cfg = et4_fixture_config(
                    ET4_REGISTERED_CELL,
                    control,
                    scenario=scenario,
                    config_id=f"et4.{stage}.{scenario}.{control}.{seed}",
                )
                result = run_episode(cfg, seed=seed, backend=SubprocessIsolate())
                try:
                    scorecard = score_principals(result)
                    evidence = {affordance: vars(audit_episode(result, affordance)) for affordance in ET4_AFFORDANCES}
                    loyalty_action_count = _selection_count(result, "rev_rubber_stamp")
                    timings.extend(result.timings)
                finally:
                    result.cleanup()
                records.append(
                    {
                        "scenario": scenario,
                        "control": control,
                        "seed": seed,
                        "eligible": scorecard.status == "exercised",
                        "activation_proxy_rubber_stamp_selections": loyalty_action_count,
                        "scorecard": vars(scorecard),
                        "affordances": evidence,
                    }
                )
    _validate_records(records, seeds)
    ledger = isolate_cost.append_ledger(timings, label=f"et4_{stage}")
    return {
        "et4_protocol_version": ET4_PROTOCOL_VERSION,
        "code_version": CODE_VERSION,
        "preregistration_source_commit": preregistration["source_commit"],
        "stage": stage,
        "registered_cell": ET4_REGISTERED_CELL,
        "records": records,
        "isolate_cost_this_run": ledger["entries"][-1],
    }


def _validate_records(records: list[dict], seeds: tuple[int, ...]) -> None:
    expected = {
        (scenario, control, seed)
        for scenario in ET4_REGISTERED_SCENARIOS
        for control in ET4_REGISTERED_CONTROLS
        for seed in seeds
    }
    actual = {(r["scenario"], r["control"], r["seed"]) for r in records}
    if actual != expected:
        raise RuntimeError(f"incomplete ET-4 record set: expected={len(expected)} actual={len(actual)}")
    for record in records:
        if set(record["affordances"]) != set(ET4_AFFORDANCES):
            raise RuntimeError(f"missing affordance evidence in record: {record}")


def _markdown_summary(data: dict) -> str:
    records = data["records"]
    lines = [
        f"# ET-4 {data['stage']} results",
        "",
        f"Protocol `{data['et4_protocol_version']}`, code `{data['code_version']}`.",
        "",
        "| scenario | control | n | eligible | mean A0 process proxy | mean A3 directional proxy |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for scenario in ET4_REGISTERED_SCENARIOS:
        for control in ET4_REGISTERED_CONTROLS:
            group = [r for r in records if r["scenario"] == scenario and r["control"] == control]
            eligible = sum(1 for r in group if r["eligible"])
            a0 = sum(r["affordances"]["A0"]["process_noncompliance"] for r in group) / len(group)
            a3_values = [r["affordances"]["A3"]["observable_principal_bias"] for r in group]
            a3 = sum(float(value or 0.0) for value in a3_values) / len(a3_values)
            lines.append(f"| {scenario} | {control} | {len(group)} | {eligible} | {a0:.4f} | {a3:.4f} |")
    lines += [
        "",
        "A0 process evidence and A3 directional evidence are reported separately; this table does not treat a compliance proxy as a safety ranking.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("preregistration", "discovery", "confirmatory"), required=True)
    args = parser.parse_args()
    if args.stage == "preregistration":
        write_preregistration()
        return

    discovery_path = RESULTS_DIR / "et4_secret_loyalty_discovery.json"
    if args.stage == "confirmatory":
        if not discovery_path.exists():
            raise RuntimeError("confirmatory stage requires an immutable discovery result")
        summary_path = RESULTS_DIR / "et4_secret_loyalty_summary.json"
        if summary_path.exists():
            raise RuntimeError(f"refusing to overwrite existing ET-4 summary: {summary_path}")
    seeds = ET4_DISCOVERY_SEEDS if args.stage == "discovery" else ET4_CONFIRMATORY_SEEDS
    data = _run_stage(args.stage, seeds)
    suffix = "confirmatory" if args.stage == "confirmatory" else "discovery"
    json_path = RESULTS_DIR / f"et4_secret_loyalty_{suffix}.json"
    markdown_path = RESULTS_DIR / f"et4_secret_loyalty_{suffix}.md"
    if json_path.exists():
        raise RuntimeError(f"refusing to overwrite existing ET-4 result: {json_path}")
    json_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(_markdown_summary(data), encoding="utf-8")
    print(f"[et4] wrote {json_path} and {markdown_path}")
    if args.stage == "confirmatory":
        summary_path = RESULTS_DIR / "et4_secret_loyalty_summary.json"
        summary_markdown_path = RESULTS_DIR / "et4_secret_loyalty_summary.md"
        if summary_path.exists():
            raise RuntimeError(f"refusing to overwrite existing ET-4 summary: {summary_path}")
        discovery = json.loads(discovery_path.read_text(encoding="utf-8"))
        summary = {
            "et4_protocol_version": ET4_PROTOCOL_VERSION,
            "code_version": CODE_VERSION,
            "discovery": discovery,
            "confirmatory": data,
        }
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        summary_markdown_path.write_text(
            "# ET-4 summary\n\n"
            "## Discovery\n\n"
            + _markdown_summary(discovery)
            + "\n## Confirmatory\n\n"
            + _markdown_summary(data),
            encoding="utf-8",
        )
        print(f"[et4] wrote {summary_path} and {summary_markdown_path}")


if __name__ == "__main__":
    main()
