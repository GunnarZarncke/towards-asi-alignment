import sys
from pathlib import Path

# Make the demo package importable as top-level `app` / `llm_client`.
DEMO_DIR = Path(__file__).resolve().parents[1]
if str(DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(DEMO_DIR))
