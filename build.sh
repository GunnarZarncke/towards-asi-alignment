#!/usr/bin/env bash
set -euo pipefail

mkdir -p dist/pdf

latexmk -pdf -interaction=nonstopmode -halt-on-error book.tex

cp book.pdf dist/pdf/towards-superintelligence-alignments.pdf

echo "Built dist/pdf/towards-superintelligence-alignments.pdf"
