#!/usr/bin/env python3
"""Write metadata/claims-base.tex from predictions.yml registrySite.

The manuscript uses \\claimsbase and \\claimspage{market-NN}{K}.
Change the public host by editing registrySite only, then regenerate.
"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
raw = yaml.safe_load((ROOT / "metadata" / "predictions.yml").read_text())
base = str(raw["registrySite"]).rstrip("/")
out = ROOT / "metadata" / "claims-base.tex"
out.write_text(
    "% Generated from metadata/predictions.yml (registrySite). Do not edit.\n"
    f"\\newcommand{{\\claimsbase}}{{{base}}}\n"
    "\\newcommand{\\claimspage}[2]{%\n"
    "  \\href{\\claimsbase/markets/#1/v#2/}{claims registry (contract~v#2)}%\n"
    "}\n"
)
print(f"[generate] metadata/claims-base.tex -> {base}")
