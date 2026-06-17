#!/usr/bin/env bash
set -euo pipefail

latexmk -C
rm -rf dist/pdf/*.pdf
rm -f *.bbl *.bcf *.run.xml *.toc *.lof *.lot *.idx *.ilg *.ind
