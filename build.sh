#!/usr/bin/env bash
set -euo pipefail

mkdir -p dist/pdf

python3 scripts/generate_tables.py
python3 scripts/generate_global_nocite.py
python3 scripts/generate_notation_appendix.py
python3 scripts/generate_assumptions_appendix.py
latexmk -pdf -interaction=nonstopmode -halt-on-error book.tex

cp book.pdf dist/pdf/towards-superintelligence-alignment.pdf

echo "Built dist/pdf/towards-superintelligence-alignment.pdf"
