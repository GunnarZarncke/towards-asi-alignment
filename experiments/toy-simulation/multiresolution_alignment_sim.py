#!/usr/bin/env python3
"""CLI entry for multiresolution alignment simulation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from multiresolution_alignment_sim.__main__ import main

if __name__ == "__main__":
    main()
