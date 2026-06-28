# 2026-06-28 — ch25 split implementation

## Trigger

The user asked to implement the ch25 split plan and use `Correction Channels under Adversarial Pressure` as the title for chapter B.

## Done

- Split `chapters/ch25-correction-channel-integrity.tex`.
  - ch25 now keeps the certificate definition: valid reference process, trace bottlenecks, vector/status CCI, value-bundle correction, extrapolative boundary, directional transparency, certificate limitations, WWCTV, and summary.
- Added `chapters/ch25b-correction-channels-adversarial-pressure.tex`.
  - New title: `Correction Channels under Adversarial Pressure`.
  - Moved the stress-test material from ontology shift through safety-case/failure-mode sections, preserving existing section labels for cross-reference stability.
- Updated `parts/part06-correction-channels.tex`, `metadata/book.yml`, generated `tables/chapter-map.tex` and `tables/part-roadmap.tex`.
- Generalized `scripts/generate_tables.py` so any `chNNb` ID displays correctly, not only `ch39b`.
- Fixed `scripts/book_stats.py` to match TOC/page spans by chapter title instead of list index, preventing b-chapter insertions from shifting displayed stats titles.
- Updated counts/status references in `README.md`, `scripts/check_structure.py`, `metadata/claims-ledger.md`, and `metadata/book-stats.md`.
- Updated reviewer-facing pointers in `REVIEWING_FOR_AGENTS.md`, `llms.txt`, `appendices/appF-glossary.tex`, `formal/README.md`, and the ch25 split plan.
- Fixed a stale unrelated reference in `chapters/ch33-multi-agent-strategic-coupling.tex`: `ch:boundary-expansion` -> `ch:capability-growth-boundary-expansion`.

## Decisions

- Used temporary `ch25b` rather than globally renumbering ch26+.
- Kept moved section labels such as `sec:low-impact-not-invariant-ch25` and `sec:quantilization-trajectory-risk-ch25` unchanged to avoid cross-reference churn.
- Did not offload the safety-case template to Appendix D in this pass; the new B chapter remains coherent at about 20 pages.
- No Lean code change was needed. `formal/README.md` now notes that `Correction.lean` spans ch24--27 including ch25b.

## Open / next

- Decide whether to execute the planned ch19 and ch35 splits.
- Later chapter-numbering cleanup should decide whether to keep `ch25b`/`ch39b` or globally renumber.
- Optional future pass: consider moving reusable CCI audit templates into Appendix D.

## Key paths

- `chapters/ch25-correction-channel-integrity.tex`
- `chapters/ch25b-correction-channels-adversarial-pressure.tex`
- `parts/part06-correction-channels.tex`
- `metadata/book.yml`
- `tables/chapter-map.tex`
- `tables/part-roadmap.tex`
- `metadata/book-stats.md`
- `scripts/generate_tables.py`
- `scripts/book_stats.py`
- `review/ch25-split-plan-2026-06-28.md`

## Commits

- None.

## Verification

- `make check` passed.
- `./build.sh` passed.
- `python3 scripts/book_stats.py` regenerated `metadata/book-stats.md`.
- `book.log` scan found no undefined references or citations after the final build.
- Read lints reported no diagnostics for edited files.
