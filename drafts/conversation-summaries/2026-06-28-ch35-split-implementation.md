# 2026-06-28 — ch35 split implementation

## Trigger

The user asked to implement the updated ch48 split plan after making a few changes to the plan.

## Done

- Split `chapters/ch37-alignment-attractor.tex`.
  - ch48 now keeps the attractor-theory material through `False Attractors`.
  - Kept `Artifact Conductivity` in ch48 as the state-variable definition needed for the theory chapter.
  - Added `Why Attractor Theory Is Not Enough`, a theory-focused WWCTV, and a new summary.
- Added `chapters/ch38-conductive-artifacts-pivotal-processes.tex`.
  - New title: `Conductive Artifacts and Pivotal Processes`.
  - Moved the practical artifact/governance program from `Pivotal Process as Basin Transition` through the original summary.
  - Preserved moved section labels such as `sec:pivotal-process-ch48`, `sec:high-conductivity-artifact-ch48`, `sec:safety-case-view-ch48`, and `sec:wwctv-alignment-attractor`.
  - Removed the separate `Connection to Later Chapters` section and distributed those links into the summary, per the updated plan.
- Updated Part VIII input and gem/payoff signpost in `parts/part08-attractor-basins.tex`.
- Updated `metadata/book.yml`, generated `tables/chapter-map.tex` and `tables/part-roadmap.tex`, and regenerated `metadata/book-stats.md`.
- Updated static chapter-count/status surfaces: `README.md`, `scripts/check_structure.py`, and `metadata/claims-ledger.md` now reflect 48 chapter entries.
- Updated reviewer/LLM/formal/research-program surfaces:
  - `REVIEWING_FOR_AGENTS.md`
  - `llms.txt`
  - `formal/README.md`
  - `appendices/appF-research-program.tex`
- Updated `metadata/TODO.md`, `review/chapter-split-preferences-2026-06-28.md`, and `review/ch48-split-plan-2026-06-28.md` to mark the split as implemented.

## Decisions

- Used temporary `ch45` rather than globally renumbering ch46+.
- Kept labels on moved sections stable to avoid cross-reference churn.
- Did not move the short `Artifact Conductivity` definition wholesale; ch48 keeps it as the theory chapter's core state variable, while ch45 owns the practical artifact design program.
- No Lean code change was needed. `formal/README.md` now notes `Certification.lean` spans ch48 including ch45.

## Open / next

- Later chapter-numbering cleanup should decide whether to keep `ch46`/`ch48`/`ch45`/`ch47` or globally renumber.
- Optional future pass: review ch46/ch46/ch46/ch46/ch48 prose for places where artifact/governance references should cite ch45 explicitly.

## Key paths

- `chapters/ch37-alignment-attractor.tex`
- `chapters/ch38-conductive-artifacts-pivotal-processes.tex`
- `parts/part08-attractor-basins.tex`
- `metadata/book.yml`
- `tables/chapter-map.tex`
- `tables/part-roadmap.tex`
- `metadata/book-stats.md`
- `appendices/appF-research-program.tex`
- `review/ch48-split-plan-2026-06-28.md`

## Commits

- None.

## Verification

- `make check` passed.
- `./build.sh` passed.
- `python3 scripts/book_stats.py` regenerated `metadata/book-stats.md`.
- `book.log` scan found no undefined references or citations after the final build.
- Read lints reported no diagnostics for edited files.
