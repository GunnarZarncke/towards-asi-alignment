#!/usr/bin/env bash
set -euo pipefail

mkdir -p dist/pdf .biber-par-cache
export PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache"

./scripts/generate_manuscript_tex.sh
latexmk -pdf -interaction=nonstopmode -halt-on-error book.tex

cp book.pdf dist/pdf/towards-superintelligence-alignment.pdf

echo "Built dist/pdf/towards-superintelligence-alignment.pdf"
