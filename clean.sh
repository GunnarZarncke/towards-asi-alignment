#!/usr/bin/env bash
set -euo pipefail

latexmk -C
rm -rf dist/pdf/*.pdf .biber-par-cache
rm -f dist/towards-superintelligence-alignment.pdf
rm -f *.bbl *.bcf *.run.xml *.toc *.lof *.lot *.idx *.ilg *.ind
