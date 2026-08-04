"""Phase 10 -- shared plumbing for the "LLM discovery" sanity-check
scripts (`run_llm_discovery_*.py`).

Question this line of scripts asks (NOT Phase 8's "does an open-ended
engineer find a new deception tactic"): if an LLM (`gpt-4o-mini`) is
dropped into a lab role with ONLY a generic tool reference (the full
`tools.py` registry, documented the way a real tool-use API would be) and
a plain-language scenario briefing -- no scripted JSON recipe, no named
custom-field vote schema -- does it discover on its own that a comms/file
tool is the way to satisfy a cross-agent dependency, and what protocol
does it invent? A sanity check with a handful of real episodes, not a
battery: no pre-registered protocol, no statistical claim, honest
negatives reported same as everywhere else in this line.

Uses the SAME `LLMSubprocessIsolate` (`lab_sim/harness/llm_isolate.py`)
and `SubprocessIsolate` (`lab_sim/harness/isolate.py`) backends every
other real-episode script in this line uses -- no new isolate mechanism.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runners._paths import EXTERNAL_DIR, LAB_SIM_ROOT, REPO_ROOT, RESULTS_DIR

import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone

from lab_sim.agent_visible import llm_cost
from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.harness.llm_isolate import LLMSubprocessIsolate
from lab_sim.world_visible.config import LabConfig
from lab_sim.world_visible.world import run_episode

MODEL = "gpt-4o-mini"
COST_BUDGET_USD_PER_EPISODE = "0.30"


@dataclass
class DiscoveryRunResult:
    label: str
    seed: int
    result: object  # world.EpisodeResult
    llm_usage_log: list[dict]  # one entry per LLM actor: {"actor_id","usage","errors","transcript"}
    wall_seconds: float


def run_discovery_episode(
    label: str,
    cfg: LabConfig,
    seed: int,
    llm_roles: dict[str, str],
    task_briefings: dict[str, str],
    model: str = MODEL,
    cost_budget_usd: str = COST_BUDGET_USD_PER_EPISODE,
) -> DiscoveryRunResult:
    """``llm_roles``: ``{actor_id: role}`` for every actor whose isolate
    should be swapped for the discovery-prompt LLM policy (all other
    ``cfg.agents`` stay on the programmatic ``goal_policy`` backend).
    ``task_briefings``: ``{role: free-text scenario briefing}`` -- ONE
    briefing per ROLE (not per actor_id), since every LLM actor playing
    that role in this episode gets the identical text; a genuinely
    per-actor briefing is not needed by any scenario here."""
    os.environ["LAB_SIM_LLM_MODEL"] = model
    os.environ["LAB_SIM_LLM_COST_BUDGET_USD"] = cost_budget_usd
    os.environ["LAB_SIM_LLM_PROMPT_VARIANT"] = "discovery"
    os.environ["LAB_SIM_LLM_TASK_BRIEFINGS"] = json.dumps(task_briefings)
    llm_backend = LLMSubprocessIsolate()
    agent_overrides = {actor_id: (llm_backend, role) for actor_id, role in llm_roles.items()}
    t0 = time.perf_counter()
    result = run_episode(cfg, seed, backend=SubprocessIsolate(), agent_overrides=agent_overrides)
    dt = time.perf_counter() - t0
    return DiscoveryRunResult(
        label=label, seed=seed, result=result, llm_usage_log=list(llm_backend.usage_log), wall_seconds=dt,
    )


def tool_event_rows(result, actor_ids: set[str]) -> list[dict]:
    """Every host-level tool-call event for the given actors -- the
    ground-truth, host-observed record to compare the LLM's OWN stated
    ``reasoning`` (in the transcript) against."""
    return [
        {"t": e["t"], "actor_id": e["actor_id"], "tool": e["tool"], "ok": e["ok"], "reason": e["reason"]}
        for e in result.host.events.entries
        if e["actor_id"] in actor_ids
    ]


def transcript_rows(usage_entry: dict) -> list[dict]:
    """Flatten one LLM actor's transcript to compact, human-readable rows
    (t, reasoning, tool attempted, whether it validated)."""
    rows = []
    for entry in usage_entry.get("transcript") or []:
        raw = entry.get("raw_response") or {}
        validated = entry.get("validated_call")
        rows.append(
            {
                "t": entry.get("t"),
                "reasoning": raw.get("reasoning"),
                "raw_tool": raw.get("tool") or ("done" if raw.get("done") else None),
                "raw_args": raw.get("args"),
                "validated": validated is not None or bool(raw.get("done")),
                "error": entry.get("error"),
            }
        )
    return rows


def total_cost_usd(usage_logs: list[dict]) -> float:
    return round(sum((e.get("usage") or {}).get("estimated_usd", 0.0) for e in usage_logs), 6)


def record_cost_ledger(label: str, usage_logs: list[dict], model: str = MODEL) -> None:
    """Fold this run's LLM usage into the shared `results/llm_cost_ledger.json`
    (same ledger Phase 8's spot-check uses) -- consistent cost accounting
    across every real-API script in this line."""
    totals = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "calls": 0,
              "cache_hits": 0, "estimated_usd": 0.0}
    for entry in usage_logs:
        usage = entry.get("usage") or {}
        for k in totals:
            totals[k] += usage.get(k, 0)
    totals["estimated_usd"] = round(totals["estimated_usd"], 6)
    ledger_entry = llm_cost.CostLedgerEntry(
        timestamp=datetime.now(timezone.utc).isoformat(),
        model=model, label=label, episodes=1, cost_budget_usd=float(COST_BUDGET_USD_PER_EPISODE), usage=totals,
    )
    llm_cost.append_ledger(ledger_entry)
    llm_cost.write_ledger_markdown()
