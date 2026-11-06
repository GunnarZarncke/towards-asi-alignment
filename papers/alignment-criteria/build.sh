#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
paper="alignment-criteria"

# Generated inputs: Lean statement extracts (Appendix A) and the criteria map.
python3 scripts/lean_extracts.py
./scripts/render_figure.sh

lualatex -interaction=nonstopmode -halt-on-error "$paper.tex"
biber "$paper"
lualatex -interaction=nonstopmode -halt-on-error "$paper.tex"
lualatex -interaction=nonstopmode -halt-on-error "$paper.tex"

echo "Built $paper.pdf"
