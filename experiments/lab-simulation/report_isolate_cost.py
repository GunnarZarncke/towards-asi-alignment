#!/usr/bin/env python3
"""Print the isolate cost ledger summary (markdown table)."""

from lab_sim.harness.isolate_cost import DEFAULT_LEDGER, ledger_markdown, load_ledger

if __name__ == "__main__":
    print(ledger_markdown(load_ledger(DEFAULT_LEDGER)))
