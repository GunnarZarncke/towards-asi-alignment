# 2026-06-28 — ch19 split implementation

## Trigger

The user asked to implement the updated ch19 split plan after making a few changes to the plan.

## Done

- Split `chapters/ch19-tradeoffs-bundle-geometry.tex`.
  - ch19 now keeps the core geometry/tradeoff material through `Substrate Transfer`.
  - Added `What Geometry Gives Us`, a core-geometry WWCTV, and a new summary.
- Added `chapters/ch19b-measuring-stress-testing-bundle-geometry.tex`.
  - New title: `Measuring and Stress-Testing Bundle Geometry`.
  - Moved the measurement/comparison/stress-test material from `Comparing Geometries across Agents` through the original summary.
  - Preserved moved section labels such as `sec:measuring-bundle-geometry`, `sec:goodhart-bundle-geometry`, `sec:social-choice`, and `sec:wwctv-tradeoffs-bundle-geometry`.
- Updated Part IV input and gem signpost in `parts/part04-value-bundles.tex`.
- Updated `metadata/book.yml`, generated `tables/chapter-map.tex` and `tables/part-roadmap.tex`, and regenerated `metadata/book-stats.md`.
- Updated static chapter-count/status surfaces: `README.md`, `scripts/check_structure.py`, and `metadata/claims-ledger.md` now reflect 47 chapter entries.
- Updated reviewer/LLM/formal orientation surfaces:
  - `REVIEWING_FOR_AGENTS.md`
  - `llms.txt`
  - `formal/README.md`
  - `appendices/appH-research-program.tex`
- Updated `metadata/TODO.md`, `review/chapter-split-preferences-2026-06-28.md`, and `review/ch19-split-plan-2026-06-28.md` to mark the split as implemented.

## Decisions

- Used temporary `ch19b` rather than globally renumbering ch20+.
- Kept labels on moved sections stable to avoid cross-reference churn.
- Kept `Bundle Metrics` and `Contextual Weights and Their Failure Modes` in ch19 per the user's updated plan.
- No Lean code change was needed. `formal/README.md` now notes `Bundles.lean` spans ch15--23 including ch19b.

## Open / next

- Decide whether to execute the planned ch35 split.
- Later chapter-numbering cleanup should decide whether to keep `ch19b`/`ch25b`/`ch39b` or globally renumber.
- Optional future pass: review downstream prose in ch20--ch23 and ch37 for places where measurement/Goodhart claims should cite ch19b explicitly rather than only ch19.

## Key paths

- `chapters/ch19-tradeoffs-bundle-geometry.tex`
- `chapters/ch19b-measuring-stress-testing-bundle-geometry.tex`
- `parts/part04-value-bundles.tex`
- `metadata/book.yml`
- `tables/chapter-map.tex`
- `tables/part-roadmap.tex`
- `metadata/book-stats.md`
- `appendices/appH-research-program.tex`
- `review/ch19-split-plan-2026-06-28.md`

## Commits

- None.

## Verification

- `make check` passed.
- `./build.sh` passed.
- `python3 scripts/book_stats.py` regenerated `metadata/book-stats.md`.
- `book.log` scan found no undefined references or citations after the final build.
- Read lints reported no diagnostics for edited files.
