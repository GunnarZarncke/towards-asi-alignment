#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
paper="verifier-construction"

pdflatex -interaction=nonstopmode -halt-on-error "$paper.tex"
biber "$paper"
pdflatex -interaction=nonstopmode -halt-on-error "$paper.tex"
pdflatex -interaction=nonstopmode -halt-on-error "$paper.tex"

echo "Built $paper.pdf"
