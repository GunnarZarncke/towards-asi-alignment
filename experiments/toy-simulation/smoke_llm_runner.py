#!/usr/bin/env python3
"""Smoke test for Phase 3 LLM runner (mock, no API)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llm_redteam.llm_runner import make_planner, run_llm_episode, run_llm_suite
from llm_redteam.source_bundle import load_source_bundle


def main() -> None:
    bundle = load_source_bundle()
    assert len(bundle) == 6
    assert "classify_cci_status" in bundle[3].content or "audit_cci" in bundle[3].content
    print(f"source_bundle: {len(bundle)} modules, {sum(len(m.content) for m in bundle):,} chars")

    planner = make_planner(mock=True)
    one = run_llm_episode("capture_theater", 11, 200, planner)
    assert one["runner"] == "llm_episodic"
    assert one["strategy"] == "llm_mock"
    assert "cci_status" in one

    suite = run_llm_suite(
        ["capture_theater", "grounding_silent_gap"],
        [11],
        200,
        planner,
    )
    assert len(suite["runs"]) == 2
    assert len(suite["baseline_runs"]) == 2
    print("smoke_llm_runner: OK")
    print(f"  llm_false_pass_rate={suite['llm_false_pass_rate']:.2f}")
    print(f"  baseline_false_pass_rate={suite['baseline_false_pass_rate']:.2f}")


if __name__ == "__main__":
    main()
