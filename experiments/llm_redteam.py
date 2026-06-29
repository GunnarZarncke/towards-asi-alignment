#!/usr/bin/env python3
"""CLI entry for LLM red-team scaffold."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llm_redteam.__main__ import main

if __name__ == "__main__":
    main()
