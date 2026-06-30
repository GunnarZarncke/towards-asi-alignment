#!/usr/bin/env python3
"""CLI entry for embedded LLM red-team."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from embedded_llm.__main__ import main

if __name__ == "__main__":
    main()
