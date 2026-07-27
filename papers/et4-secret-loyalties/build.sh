#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
paper="et4-hackathon-submission"

pdflatex -interaction=nonstopmode -halt-on-error "$paper.tex"

echo "Built $paper.pdf"
