# 2026-06-28 — Chapter split plans

## Trigger

The user accepted the ch46 split plan and asked to add equivalent plans for the other chapters they want to split.

## Done

- Added `review/ch19-split-plan-2026-06-28.md`.
  - Proposed split: `Tradeoffs and Bundle Geometry` vs. `Measuring and Stress-Testing Bundle Geometry`.
  - Preferred boundary: end the first chapter after `Substrate Transfer`; begin the second at `Comparing Geometries across Agents`.
- Added `review/ch48-split-plan-2026-06-28.md`.
  - Proposed split: `The Alignment Attractor` vs. `Conductive Artifacts and Pivotal Processes`.
  - Preferred boundary: end the first chapter after `False Attractors`; begin the second at `Pivotal Process as Basin Transition`.
- Updated `review/chapter-split-preferences-2026-06-28.md` to point to detailed ch19/ch46/ch48 plans.
- Updated `metadata/TODO.md` to mark the split preference pass as plan-complete but implementation-open.

## Decisions

- Did not plan a ch46 split now; it remains possible but noncritical per the author's preference.
- Did not move manuscript text or edit `metadata/book.yml`; execution should wait for an explicit chapter-map / numbering decision.
- Recommended temporary `ch46` / `ch45` files only if the project wants to avoid global renumbering during the split.

## Open / next

- Decide whether to execute splits with temporary `b` chapters or in a global chapter-numbering cleanup pass.
- If executing, start with the new plan files and update part inputs, `metadata/book.yml`, generated tables, cross-references, and book stats.
- Run `make check`, `./build.sh`, and `python3 scripts/book_stats.py` after any actual manuscript split.

## Key paths

- `review/chapter-split-preferences-2026-06-28.md`
- `review/ch19-split-plan-2026-06-28.md`
- `review/ch46-split-plan-2026-06-28.md`
- `review/ch48-split-plan-2026-06-28.md`
- `metadata/TODO.md`

## Commits

- None.
