"""LLM token/cost tracking for Phase 3 red-team runs."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Rough USD per token (input, output). Estimates only — not billing-accurate.
MODEL_RATES: dict[str, tuple[float, float]] = {
    "gpt-4o-mini": (0.15 / 1_000_000, 0.60 / 1_000_000),
    "gpt-4o": (2.50 / 1_000_000, 10.0 / 1_000_000),
    "gpt-4.1-mini": (0.40 / 1_000_000, 1.60 / 1_000_000),
    "gpt-4.1": (2.0 / 1_000_000, 8.0 / 1_000_000),
}

DEFAULT_LEDGER = Path(__file__).resolve().parent.parent / "results" / "llm_cost_ledger.json"


def estimate_cost_usd(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    in_rate, out_rate = MODEL_RATES.get(model, (1.0 / 1_000_000, 3.0 / 1_000_000))
    return prompt_tokens * in_rate + completion_tokens * out_rate


def usage_dict(
    *,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    total_tokens: int,
    calls: int,
    estimated_usd: float,
) -> dict[str, Any]:
    return {
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "calls": calls,
        "estimated_usd": round(estimated_usd, 6),
        "rates_note": "estimated from MODEL_RATES in llm_cost.py; not OpenAI billing",
    }


@dataclass
class CostLedgerEntry:
    timestamp: str
    model: str
    planner: str
    result_file: str
    log_file: str
    episodes: int
    cost_budget_usd: float
    usage: dict[str, Any]
    llm_false_pass_rate: float


def load_ledger(path: Path = DEFAULT_LEDGER) -> dict[str, Any]:
    if not path.is_file():
        return {"entries": [], "cumulative_estimated_usd": 0.0}
    data = json.loads(path.read_text(encoding="utf-8"))
    if "entries" not in data:
        return {"entries": [], "cumulative_estimated_usd": 0.0}
    return data


def append_ledger(entry: CostLedgerEntry, path: Path = DEFAULT_LEDGER) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    ledger = load_ledger(path)
    ledger["entries"].append(asdict(entry))
    ledger["cumulative_estimated_usd"] = round(
        sum(e["usage"].get("estimated_usd", 0.0) for e in ledger["entries"]),
        6,
    )
    path.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    return ledger


def format_usage_summary(usage: dict[str, Any]) -> str:
    return (
        f"${usage.get('estimated_usd', 0):.4f} "
        f"({usage.get('calls', 0)} calls, "
        f"{usage.get('prompt_tokens', 0):,} in / "
        f"{usage.get('completion_tokens', 0):,} out tokens)"
    )


def ledger_markdown(path: Path = DEFAULT_LEDGER) -> str:
    ledger = load_ledger(path)
    lines = [
        "# LLM cost ledger",
        "",
        f"**Cumulative estimated spend:** ${ledger.get('cumulative_estimated_usd', 0):.4f}",
        "",
        "| When | Model | Episodes | Est. USD | Calls | Result |",
        "|------|-------|----------|----------|-------|--------|",
    ]
    for e in ledger.get("entries", []):
        u = e.get("usage", {})
        lines.append(
            f"| {e.get('timestamp', '')[:19]} | {e.get('model', '')} | "
            f"{e.get('episodes', 0)} | ${u.get('estimated_usd', 0):.4f} | "
            f"{u.get('calls', 0)} | `{e.get('result_file', '')}` |"
        )
    lines.append("")
    lines.append("_Estimates use `llm_cost.MODEL_RATES`; verify against OpenAI usage dashboard._")
    lines.append("")
    return "\n".join(lines)


def write_ledger_markdown(path: Path = DEFAULT_LEDGER) -> Path:
    md_path = path.with_suffix(".md")
    md_path.write_text(ledger_markdown(path), encoding="utf-8")
    return md_path
