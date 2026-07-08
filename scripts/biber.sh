#!/usr/bin/env bash
# Regenerate manuscript .tex inputs, then run pdflatex → biber → pdflatex ×2.
# Use when biber stalls after "Found BibTeX data source ..." or the global
# bibliography looks stale. See docs/BUILD.md.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

./scripts/generate_manuscript_tex.sh

mkdir -p .biber-par-cache
export PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache"

rm -f references/*.bib.blg book.bbl-SAVE-ERROR*

pdflatex -interaction=nonstopmode -halt-on-error book.tex
biber book
pdflatex -interaction=nonstopmode -halt-on-error book.tex
pdflatex -interaction=nonstopmode -halt-on-error book.tex

echo "Biber bibliography pass complete."
