"""LLM token/cost tracking for the Phase 8 exploratory LLM adapter.

Deliberately self-contained rather than importing `toy-simulation/
llm_redteam/llm_cost.py` directly (docs/EXPERIMENTS.md: this line
synthesizes disciplines from predecessors "without importing their code")
— but the SHAPE (rates table, ledger entry, markdown summary) is copied
verbatim from that module, PLAN.md's explicitly named precedent.

This ledger is entirely separate from `isolate_cost.py`'s OS-process ledger
(PLAN.md: "Phase 8 reuses the same primitives for a second, separate
LLM-call cost ledger") — isolate lifetimes and LLM tokens are different
resources with different unit economics, tracked in different files.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Rough USD per token (input, output). Estimates only -- not billing-accurate.
MODEL_RATES: dict[str, tuple[float, float]] = {
    "gpt-4o-mini": (0.15 / 1_000_000, 0.60 / 1_000_000),
    "gpt-4o": (2.50 / 1_000_000, 10.0 / 1_000_000),
    "gpt-4.1-mini": (0.40 / 1_000_000, 1.60 / 1_000_000),
    "gpt-4.1": (2.0 / 1_000_000, 8.0 / 1_000_000),
    "gpt-5.5": (5.0 / 1_000_000, 30.0 / 1_000_000),
}

DEFAULT_LEDGER = Path(__file__).resolve().parent.parent / "results" / "llm_cost_ledger.json"


def estimate_cost_usd(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    in_rate, out_rate = MODEL_RATES.get(model, (1.0 / 1_000_000, 3.0 / 1_000_000))
    return prompt_tokens * in_rate + completion_tokens * out_rate


@dataclass
class LLMUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    calls: int = 0
    cache_hits: int = 0
    estimated_usd: float = 0.0


@dataclass(frozen=True)
class CostLedgerEntry:
    timestamp: str
    model: str
    label: str
    episodes: int
    cost_budget_usd: float
    usage: dict[str, Any]


def load_ledger(path: Path = DEFAULT_LEDGER) -> dict[str, Any]:
    if not path.is_file():
        return {"entries": [], "cumulative_estimated_usd": 0.0}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("entries", [])
    data.setdefault("cumulative_estimated_usd", 0.0)
    return data


def append_ledger(entry: CostLedgerEntry, path: Path = DEFAULT_LEDGER) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    ledger = load_ledger(path)
    ledger["entries"].append(asdict(entry))
    ledger["cumulative_estimated_usd"] = round(
        sum(e["usage"].get("estimated_usd", 0.0) for e in ledger["entries"]), 6
    )
    path.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    return ledger


def format_usage_summary(usage: dict[str, Any]) -> str:
    return (
        f"${usage.get('estimated_usd', 0):.4f} "
        f"({usage.get('calls', 0)} calls, {usage.get('cache_hits', 0)} cache hits, "
        f"{usage.get('prompt_tokens', 0):,} in / {usage.get('completion_tokens', 0):,} out tokens)"
    )


def ledger_markdown(path: Path = DEFAULT_LEDGER) -> str:
    ledger = load_ledger(path)
    lines = [
        "# LLM cost ledger (Phase 8, exploratory only)",
        "",
        f"**Cumulative estimated spend:** ${ledger.get('cumulative_estimated_usd', 0):.4f}",
        "",
        "| When | Model | Label | Episodes | Est. USD | Calls | Cache hits |",
        "|---|---|---|---|---|---|---|",
    ]
    for e in ledger.get("entries", []):
        u = e.get("usage", {})
        lines.append(
            f"| {e.get('timestamp', '')[:19]} | {e.get('model', '')} | {e.get('label', '')} | "
            f"{e.get('episodes', 0)} | ${u.get('estimated_usd', 0):.4f} | {u.get('calls', 0)} | "
            f"{u.get('cache_hits', 0)} |"
        )
    lines += ["", "_Estimates use `llm_cost.MODEL_RATES`; verify against the provider's usage dashboard._", ""]
    return "\n".join(lines)


def write_ledger_markdown(path: Path = DEFAULT_LEDGER) -> Path:
    md_path = path.with_suffix(".md")
    md_path.write_text(ledger_markdown(path), encoding="utf-8")
    return md_path
