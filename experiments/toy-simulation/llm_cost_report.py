#!/usr/bin/env python3
"""Print LLM red-team cost ledger summary."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llm_redteam.llm_cost import DEFAULT_LEDGER, ledger_markdown, load_ledger

if __name__ == "__main__":
    print(ledger_markdown(DEFAULT_LEDGER))
