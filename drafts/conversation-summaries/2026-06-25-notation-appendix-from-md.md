# 2026-06-25 — Notation appendix from notation.md

## Trigger
User asked to remove the notation table fragment, make chapters the canonical definition sites, build Appendix A as a collated index (no explanations), add "How to use this appendix", avoid glossary duplication, and keep all appendix content in `metadata/notation.md` only.

## Done
- Restructured `metadata/notation.md`: maintainer notes + `## Appendix index` tables (`Symbol | Definition | Home`).
- Added `scripts/generate_notation_appendix.py` → `metadata/notation-index.tex` (68 symbols, 9 sections).
- Wrote `appendices/appA-notation.tex` with "How to use this appendix" + `\input{metadata/notation-index.tex}`.
- Wired generator into `build.sh`; removed `tables/notation-table.tex`.
- Updated `INSTRUCTIONS.md` §5, `metadata/TODO.md`.
- `./build.sh` passes.

## Decisions
- Single edit surface: `notation.md` only; Appendix A is generated, not hand-maintained in LaTeX.
- Appendix entries: one-line definition + `Chapter~\ref{...}`; operational terms stay in Appendix F.
- Reconciliation / propagation notes live under Maintainer notes, not in the PDF index.

## Open / next
- Mark ⟳ symbols in Home column as propagation completes.
- Resolve $C_H$ vs $C^H_t$ and $\mathcal V$ vs $V_t$ in maintainer notes.

## Key paths
- `metadata/notation.md`, `metadata/notation-index.tex`, `appendices/appA-notation.tex`, `scripts/generate_notation_appendix.py`

## Commits
- none (not requested)
