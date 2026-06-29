#!/usr/bin/env python3
"""Multi-model LLM red-team sweep: hunt for false-pass successes."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llm_redteam.llm_cost import (
    CostLedgerEntry,
    append_ledger,
    format_usage_summary,
    write_ledger_markdown,
)
from llm_redteam.llm_runner import make_planner, run_llm_suite

ROOT = Path(__file__).resolve().parent
RESULT_DIR = ROOT / "results"

# Scenarios where Phase 1 full_redteam false-passes at medium_handles (seeds 11–20).
DEFAULT_SCENARIOS = (
    "capture_theater",
    "capture_mild",
    "boundary_alias",
    "hidden_capability",
    "selection_basin",
)
DEFAULT_MODELS = ("gpt-4o-mini", "gpt-4.1-mini", "gpt-4o")
HIGH_TPM_MODELS = frozenset({"gpt-4o", "gpt-4.1", "gpt-4.1-mini"})


def _request_delay_for_model(model: str, override: float | None) -> float:
    if override is not None:
        return override
    return 55.0 if model in HIGH_TPM_MODELS else 0.0


def _build_matrix_report(by_model: dict[str, dict], scenarios: list[str]) -> str:
    lines = [
        "# LLM model sweep — false-pass hunt",
        "",
        f"Generated: {datetime.now().isoformat()}",
        "",
        "Goal: find any (model, scenario, seed) where LLM achieves **false pass** "
        "(`status=passes` while oracle says audit should refuse).",
        "",
        "## Summary by model",
        "",
        "| Model | Episodes | LLM false-pass | Baseline false-pass | Est. USD |",
        "|-------|----------|----------------|---------------------|----------|",
    ]
    total_usd = 0.0
    any_success = False
    for model, payload in by_model.items():
        usage = payload.get("llm_usage_total") or {}
        usd = float(usage.get("estimated_usd", 0))
        total_usd += usd
        fp = int(sum(1 for r in payload["runs"] if r["false_pass"]))
        lines.append(
            f"| `{model}` | {len(payload['runs'])} | "
            f"{fp}/{len(payload['runs'])} ({payload['llm_false_pass_rate']:.0%}) | "
            f"{payload['baseline_false_pass_rate']:.0%} | ${usd:.4f} |"
        )
        if fp:
            any_success = True
    lines.extend(
        [
            "",
            f"**Total estimated cost:** ${total_usd:.4f}",
            "",
            "## False-pass matrix (LLM / medium_handles)",
            "",
        ]
    )
    for model, payload in by_model.items():
        lines.append(f"### `{model}`")
        lines.append("")
        lines.append("| scenario | seed | status | false_pass | patches | note |")
        lines.append("|----------|------|--------|------------|---------|------|")
        for run in payload["runs"]:
            notes = (run.get("llm_meta") or {}).get("raw", {}).get("notes", "")
            note_short = (str(notes)[:60] + "…") if len(str(notes)) > 60 else str(notes)
            lines.append(
                f"| {run['scenario']} | {run['seed']} | {run['cci_status']} | "
                f"{run['false_pass']} | {run['n_planned_patches']} | {note_short} |"
            )
        lines.append("")

    successes = [
        (m, r["scenario"], r["seed"], r["cci_status"])
        for m, payload in by_model.items()
        for r in payload["runs"]
        if r["false_pass"]
    ]
    lines.append("## LLM false-pass successes")
    lines.append("")
    if successes:
        for m, scen, seed, status in successes:
            lines.append(f"- `{m}` / `{scen}` / seed={seed} → `{status}`")
    else:
        lines.append("_None in this sweep — audit held for all LLM episodes._")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-model LLM red-team sweep")
    parser.add_argument("--T", type=int, default=300)
    parser.add_argument("--seeds", type=str, default="11,12")
    parser.add_argument("--scenarios", type=str, default=",".join(DEFAULT_SCENARIOS))
    parser.add_argument("--models", type=str, default=",".join(DEFAULT_MODELS))
    parser.add_argument("--instrumentation", type=str, default="medium_handles")
    parser.add_argument("--max-output-tokens", type=int, default=4096)
    parser.add_argument("--cost-budget-usd", type=float, default=15.0)
    parser.add_argument(
        "--request-delay",
        type=float,
        default=None,
        help="Fixed inter-episode delay; default auto (55s for 4o/4.1, 0 for mini)",
    )
    parser.add_argument("--baseline", type=str, default="full_redteam")
    args = parser.parse_args()

    seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
    scenarios = [s.strip() for s in args.scenarios.split(",") if s.strip()]
    models = [m.strip() for m in args.models.split(",") if m.strip()]

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    by_model: dict[str, dict] = {}
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    for model in models:
        delay = _request_delay_for_model(model, args.request_delay)
        print(
            f"\n=== model={model} episodes={len(scenarios)*len(seeds)} "
            f"request_delay={delay}s ===",
            flush=True,
        )
        planner = make_planner(
            mock=False,
            model=model,
            cost_budget_usd=args.cost_budget_usd,
            max_output_tokens=args.max_output_tokens,
        )
        payload = run_llm_suite(
            scenarios,  # type: ignore[arg-type]
            seeds,
            args.T,
            planner,
            instrumentation=args.instrumentation,  # type: ignore[arg-type]
            baseline_strategy=args.baseline,
            request_delay_s=delay,
        )
        payload["cost_budget_usd"] = args.cost_budget_usd
        payload["request_delay_s"] = delay
        slug = model.replace("/", "_").replace(".", "-")
        out_path = RESULT_DIR / f"llm_redteam_episodic_{slug}.json"
        out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        by_model[model] = payload

        usage = payload.get("llm_usage_total") or {}
        if usage:
            append_ledger(
                CostLedgerEntry(
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    model=model,
                    planner=str(payload["planner"]),
                    result_file=out_path.name,
                    log_file=f"llm_model_sweep_{stamp}.md",
                    episodes=len(payload["runs"]),
                    cost_budget_usd=args.cost_budget_usd,
                    usage=usage,  # type: ignore[arg-type]
                    llm_false_pass_rate=float(payload["llm_false_pass_rate"]),
                )
            )
        fp = sum(1 for r in payload["runs"] if r["false_pass"])
        print(
            f"model={model}: false_pass={fp}/{len(payload['runs'])} "
            f"baseline_fp={payload['baseline_false_pass_rate']:.0%} "
            f"cost={format_usage_summary(usage) if usage else 'n/a'}",
            flush=True,
        )

    sweep_path = RESULT_DIR / f"llm_model_sweep_{stamp}.json"
    sweep_path.write_text(
        json.dumps(
            {
                "T": args.T,
                "seeds": seeds,
                "scenarios": scenarios,
                "models": models,
                "instrumentation": args.instrumentation,
                "by_model": {
                    m: {
                        "llm_false_pass_rate": p["llm_false_pass_rate"],
                        "baseline_false_pass_rate": p["baseline_false_pass_rate"],
                        "llm_usage_total": p.get("llm_usage_total"),
                        "runs": [
                            {
                                "scenario": r["scenario"],
                                "seed": r["seed"],
                                "cci_status": r["cci_status"],
                                "false_pass": r["false_pass"],
                                "n_planned_patches": r["n_planned_patches"],
                            }
                            for r in p["runs"]
                        ],
                    }
                    for m, p in by_model.items()
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    md_path = RESULT_DIR / f"llm_model_sweep_{stamp}.md"
    md_path.write_text(_build_matrix_report(by_model, scenarios), encoding="utf-8")
    ledger_md = write_ledger_markdown()

    print(f"\nWrote {sweep_path}")
    print(f"Wrote {md_path}")
    print(f"Cost ledger: {ledger_md}")


if __name__ == "__main__":
    main()
