# 2026-07-08 — Inline section index in table of contents

## Trigger
User asked to shorten the book TOC: keep chapter lines as-is, but render sections as a wrapped paragraph (`Title page · Title page · …`) with no section numbers.

## Done
- Added `metadata/toc-inline-sections.tex`: redefines `\l@section` for inline runs under each chapter; strips `\numberline`; sets `\settocdepth{section}` (subsections dropped from TOC); flushes paragraph on part/chapter boundaries and at TOC end.
- Wired it in `book.tex` immediately after `hyperref` so patches are not overwritten.
- Verified on a TOC-only compile: ~43-page TOC shrinks to ~13 pages; chapter 1 example shows wrapped section run with middle-dot separators.
- `dist/pdf/towards-superintelligence-alignment.pdf` was stale (Jul 7) because `./build.sh` failed at biber before the `cp` step; root `book.pdf` (Jul 8) had the new TOC — user should rerun `./build.sh` or `cp book.pdf dist/pdf/towards-superintelligence-alignment.pdf` after a green build.

## Decisions
- Subsections excluded from TOC via depth, not left as separate lines — necessary for the shortening goal.
- Separator: middle dot with spaces (` · `).
- Section block set in `\small` under each chapter line for visual hierarchy.

## Open / next
- Full `./build.sh` may still fail on biber in some environments; TOC change itself compiles under pdflatex.
- Refresh `dist/pdf/` after a successful build if the shipped PDF should match root `book.pdf`.

## Key paths
- `metadata/toc-inline-sections.tex`
- `book.tex` (line `\input{metadata/toc-inline-sections.tex}` after `\hypersetup`)

## Commits
- `33aed30` Render TOC sections as inline wrapped runs under each chapter.
