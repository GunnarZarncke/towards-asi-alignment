#!/usr/bin/env python3
"""Print isolate and episode cost ledger summaries (markdown tables)."""

from __future__ import annotations

from graded_lab.harness.episode_cost import (
    DEFAULT_LEDGER as EPISODE_LEDGER,
    ledger_markdown as episode_markdown,
    load_ledger as load_episode_ledger,
)
from graded_lab.harness.isolate_cost import (
    DEFAULT_LEDGER as ISOLATE_LEDGER,
    ledger_markdown as isolate_markdown,
    load_ledger as load_isolate_ledger,
)

if __name__ == "__main__":
    print("## Isolate IPC ledger\n")
    print(isolate_markdown(load_isolate_ledger(ISOLATE_LEDGER)))
    print("\n## Episode wall-time ledger\n")
    print(episode_markdown(load_episode_ledger(EPISODE_LEDGER)))
