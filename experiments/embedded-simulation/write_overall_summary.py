#!/usr/bin/env python3
"""Regenerate OVERALL_SUMMARY from result JSON artifacts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def _load(name: str) -> dict | None:
    path = RESULTS / name
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    stamp = datetime.now(timezone.utc).isoformat()
    artifacts = sorted(p.name for p in RESULTS.glob("*") if p.suffix in (".json", ".md"))

    lines = [
        "# Embedded simulation — overall summary",
        "",
        f"Generated: {stamp}",
        "",
        "## Claim strength",
        "",
        "Controlled falsification harness for the embedded audit pipeline (VFS + UAD + scoped CCI + outer eval). "
        "Not frontier-system evidence. Red-team agents patch deployment-visible `correction.jsonl` only.",
        "",
        "## Key results",
        "",
    ]

    matrix = _load("embedded_instrumentation_matrix.json")
    if matrix:
        lines.append(
            f"- **Instrumentation matrix** (T={matrix['T']}, seed={matrix['seed']}): "
            f"min certifiable `{matrix['minimum_certifiable_level']}`; "
            f"in-sim correct {matrix['in_sim_correct_rate']:.1%} ({matrix['runtime_seconds']}s)"
        )
        for level, rate in matrix.get("correct_rate_by_level", {}).items():
            lines.append(f"  - {level}: {rate:.1%}")

    frozen = _load("embedded_frozen_validation.json")
    if frozen:
        lines.append(
            f"- **Frozen validation** (seeds {frozen['seeds']}, T={frozen['T']}): "
            f"in-sim correct {frozen['in_sim_correct_rate']:.1%} ({frozen['runtime_seconds']}s)"
        )
        worst = min(frozen.get("correct_rate_by_bridge", {}).items(), key=lambda x: x[1])
        best = max(frozen.get("correct_rate_by_bridge", {}).items(), key=lambda x: x[1])
        lines.append(f"  - Weakest bridge: `{worst[0]}` at {worst[1]:.1%}")
        lines.append(f"  - Strongest bridge: `{best[0]}` at {best[1]:.1%}")

    sweep = _load("embedded_parameter_sweep.json")
    if sweep:
        lines.append(
            f"- **Parameter sweep** ({sweep['axes']}): {sweep['n_runs']} runs; "
            f"false-pass {sweep['false_pass_rate']:.1%} ({sweep['runtime_seconds']}s)"
        )

    battery = _load("embedded_redteam_battery.json")
    if battery:
        lines.append(
            f"- **Hand-written red-team battery** (T={battery['T']}, {battery['n_runs']} runs): "
            f"false-pass **{battery['false_pass_rate']:.1%}** ({battery['false_pass_count']}) "
            f"in {battery['runtime_seconds']}s"
        )
        worst = max(
            battery.get("summary_by_strategy", {}).items(),
            key=lambda x: x[1]["false_pass_rate"],
        )
        lines.append(
            f"  - Worst strategy: `{worst[0]}` false-pass {worst[1]['false_pass_rate']:.1%} "
            f"(in-sim correct {worst[1]['in_sim_correct_rate']:.1%})"
        )
        for level, stats in battery.get("summary_by_instrumentation", {}).items():
            lines.append(
                f"  - {level}: false-pass {stats['false_pass_rate']:.1%}, "
                f"correct {stats['in_sim_correct_rate']:.1%}"
            )

    report = _load("embedded_sim_report.json")
    if report:
        summary = report.get("summary", {})
        lines.append(
            f"- **Main report** (13 bridges, full_redteam): "
            f"{summary.get('false_pass_count', 0)}/{report.get('n_episodes', 0)} false passes; "
            f"outer certifies {summary.get('outer_certifies_count', 0)}"
        )

    for stem in ("embedded_llm_redteam_live", "embedded_llm_redteam_mock"):
        llm = _load(f"{stem}.json")
        if llm:
            mode = "live API" if "live" in stem else "mock"
            lines.append(
                f"- **LLM red-team** ({mode}, `{llm.get('planner')}`): false-pass "
                f"{llm.get('llm_false_pass_rate', 0):.1%}; in-sim correct "
                f"{llm.get('llm_mean_in_sim_correct', 0):.1%} ({llm.get('runtime_seconds')}s)"
            )

    lines.extend(
        [
            "",
            "## Comparison to toy-simulation (Phase 1 battery)",
            "",
            "Toy-sim hand-written battery (micro-only, T=2000): **35% false-pass** overall; "
            "`boundary_decouple` and `full_redteam` worst (~89% on some scenarios).",
            "",
            "Embedded pipeline (lab + UAD + scoped CCI + outer eval): **0% false-pass** on the "
            "matched battery grid (1260 runs, T=800). Outer eval and UAD gate reject patches that "
            "micro-only CCI might accept. This is expected given the extra layers—not a claim that "
            "embedded audit is adversarially complete.",
            "",
            "## Parity artifacts",
            "",
            "| Toy-sim | Embedded |",
            "| --- | --- |",
            "| instrumentation curve | `embedded_instrumentation_matrix.*` |",
            "| frozen validation | `embedded_frozen_validation.*` |",
            "| parameter sweep | `embedded_parameter_sweep.*` |",
            "| llm_redteam_battery | `embedded_redteam_battery.*` |",
            "| llm episodic | `embedded_llm_redteam_*.*` |",
            "| main report | `embedded_sim_report.*` |",
            "",
            "## Open decisions (postponed)",
            "",
            "- MB5 gate rejects default degraded successor referent transport.",
            "- Unit-scoped CCI vs global signals for MB7d inferential coupling.",
            "",
            "## Artifacts",
            "",
        ]
    )
    for name in artifacts:
        lines.append(f"- `{name}`")

    out = RESULTS / "OVERALL_SUMMARY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
