import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

AGENCY_DETECT = ROOT.parents[3].parent / "agency-detect"
if AGENCY_DETECT.is_dir() and str(AGENCY_DETECT) not in sys.path:
    sys.path.insert(0, str(AGENCY_DETECT))
