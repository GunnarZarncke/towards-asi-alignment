#!/usr/bin/env python3
"""Entry point for Phase 3 LLM episodic red-team."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llm_redteam.llm_cli import main

if __name__ == "__main__":
    main()
