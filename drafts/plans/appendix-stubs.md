# Appendix stub retirement + App N expansions

Status: **implemented** (2026-09-07).

## Phase 1 — housekeeping

- [x] Delete `appendices/appH`–`appK` stub files (four-line placeholders, never in `book.tex`).
- [x] `scripts/check_structure.py`: `APPENDIX_COUNT` = 9.
- [x] `site/scripts/sync-chapters.mjs`: remove stub paths from `labelScanPaths`.
- [x] `scripts/init_scaffold.py`: wired appendices only (A, B, C, M, D, E, F, G, N).
- [x] `INSTRUCTIONS.md` §14: print-letter / source-file / `\label` table; drop H–L stub row.
- [x] `metadata/TODO.md`: remove Appendix follow-through block and appH–K leave-local bullet.
- [x] `docs/MANUSCRIPT.md`, `metadata/claims-ledger.md`, `metadata/assumptions-ledger.md`, `metadata/source-canon.md`, UAD funding card.

## Phase 2 — App N

- [x] `\section{How to read this appendix}` before chapter synthesis (`sec:appn-how-to-read`); repo paths only, three-class framing retained.
- [x] `\section{Safety-Case Readings on Host Traces}` after Witness table (`sec:appn-safety-case-readings`): W-9, W-3, W-4, W-10, W-11, W-1/W-8 (+ W-15 contrast).
- [x] ch42 pointer to `sec:appn-safety-case-readings`.

## Verification

- [x] `make check`
- [ ] `./build.sh` (optional full PDF)
