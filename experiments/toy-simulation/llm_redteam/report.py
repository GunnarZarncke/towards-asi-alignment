"""Markdown report for Phase 1 red-team battery results."""

from __future__ import annotations

from datetime import datetime
from typing import Any


def _cell(runs: list[dict[str, Any]], key: str) -> str:
    if not runs:
        return "—"
    n = len(runs)
    fp = sum(1 for r in runs if r.get("false_pass"))
    correct = sum(1 for r in runs if r.get("cci_status_correct"))
    return f"{fp}/{n} fp ({correct / n:.0%} ok)"


def build_report(payload: dict[str, Any]) -> str:
    runs: list[dict[str, Any]] = payload.get("runs", [])
    strategies: list[str] = payload.get("strategy_names", [])
    scenarios: list[str] = payload.get("scenarios", [])
    levels: list[str] = payload.get(
        "instrumentation_levels", [payload.get("instrumentation", "medium_handles")]
    )
    seeds: list[int] = payload.get("seeds", [])

    lines = [
        "# LLM red-team Phase 1 battery report",
        "",
        f"Generated: {datetime.now().isoformat()}",
        "",
        f"**Claim strength:** {payload.get('claim_strength', 'n/a')}",
        "",
        "## Run configuration",
        "",
        f"- T={payload.get('T')}",
        f"- seeds={seeds}",
        f"- scenarios={scenarios}",
        f"- strategies={strategies}",
        f"- instrumentation_levels={levels}",
        f"- runtime_seconds={payload.get('runtime_seconds')}",
        "",
        "## Summary",
        "",
        f"- **Overall false-pass rate:** {payload.get('false_pass_rate', 0):.2%} "
        f"({payload.get('false_pass_count', 0)} / {len(runs)})",
        "",
    ]

    summary = payload.get("summary_by_strategy", {})
    if summary:
        lines.extend(["### By strategy", ""])
        for name, stats in summary.items():
            lines.append(
                f"- `{name}`: false_pass={stats['false_pass_rate']:.2%}, "
                f"cci_correct={stats['mean_cci_correct']:.2%}, n={stats['n_runs']}"
            )
        lines.append("")

    summary_level = payload.get("summary_by_instrumentation", {})
    if summary_level:
        lines.extend(["### By instrumentation", ""])
        for level, stats in summary_level.items():
            lines.append(
                f"- `{level}`: false_pass={stats['false_pass_rate']:.2%}, "
                f"cci_correct={stats['mean_cci_correct']:.2%}, n={stats['n_runs']}"
            )
        lines.append("")

    lines.extend(["## False-pass matrix (scenario × strategy)", ""])
    for level in levels:
        lines.append(f"### `{level}`")
        lines.append("")
        header = "| scenario | " + " | ".join(strategies) + " |"
        sep = "|---|" + "|".join(["---"] * len(strategies)) + "|"
        lines.extend([header, sep])
        for scen in scenarios:
            cells = []
            for strat in strategies:
                subset = [
                    r
                    for r in runs
                    if r["scenario"] == scen
                    and r["strategy"] == strat
                    and r["instrumentation"] == level
                ]
                cells.append(_cell(subset, "false_pass"))
            lines.append(f"| {scen} | " + " | ".join(cells) + " |")
        lines.append("")

    false_passes = [r for r in runs if r.get("false_pass")]
    if false_passes:
        lines.extend(["## False-pass episodes", ""])
        for r in false_passes[:50]:
            lines.append(
                f"- `{r['strategy']}` / `{r['scenario']}` / seed={r['seed']} / "
                f"`{r['instrumentation']}` → status={r['cci_status']}"
            )
        if len(false_passes) > 50:
            lines.append(f"- … and {len(false_passes) - 50} more")
        lines.append("")
    else:
        lines.extend(["## False-pass episodes", "", "_None — audit resisted all hand-written patches._", ""])

    lines.extend(
        [
            "## Interpretation",
            "",
            "- **false pass:** audit `passes` while post-hoc oracle scoring says the certificate "
            "should not pass (`cci_status_correct=False`).",
            "- Hand-written patches target deployment-visible fields only; oracle labels are "
            "never visible to the audit path.",
            "- Minimum certifiable instrumentation on held-out suite: **`medium_handles`** "
            "(see `multiresolution_instrumentation_curve.json`).",
            "",
        ]
    )
    return "\n".join(lines)
