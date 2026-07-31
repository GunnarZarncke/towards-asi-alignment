# 2026-06-18 — Chapter 12 coordination bottleneck draft

## Trigger
User provided full draft for chapter 12 and asked to integrate into `chapters/ch12-boundary-expansion.tex`.

## Done
- Replaced stub with integrated draft: epigraph, chapter thesis, 20 sections (including subsections), seven coordination losses, coordination graph and $\kappa_{ij}$, percolation, mid-scale collapse, coordination forms, worked tool-service example, design principles, value-transport diagnostic, BibLaTeX references (~5,560 words).
- Fixed LaTeX from draft: `===` equation artifacts, `*` subscripts, `\MI` for mutual information, prose math delimiters, quote marks, `(b,p,\rho,c)` typo.
- Opening bridges from Chapter 11 (boundary expansion).
- Updated `metadata/book.yml` ch12 title/status.
- Renamed ch13 label to `ch:coordination-bottleneck-deferred`; ch13 stub marked reserved (content now in ch12).
- `./build.sh` succeeds.

## Decisions
- Placed **The Coordination Bottleneck** in `ch12-boundary-expansion.tex` per user file target (filename unchanged).
- ch13 stub retained as placeholder pending Part III renumbering (ch11/ch12 content vs. INSTRUCTIONS chapter list still misaligned).

## Open / next
- Renumber Part III: align filenames, `book.yml`, and `INSTRUCTIONS.md` (ch11 boundary expansion, ch12 coordination, retire or repurpose ch13 slot).
- Optional: add Wang/Szolnoki/Perc percolation cite when bib entry imported.

## Key paths
- `chapters/ch12-boundary-expansion.tex`
- `chapters/ch13-coordination-bottleneck.tex` (deferred stub)
- `metadata/book.yml`
