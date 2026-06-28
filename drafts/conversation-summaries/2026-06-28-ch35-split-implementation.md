# 2026-06-28 — ch35 split implementation

## Trigger

The user asked to implement the updated ch35 split plan after making a few changes to the plan.

## Done

- Split `chapters/ch35-alignment-attractor.tex`.
  - ch35 now keeps the attractor-theory material through `False Attractors`.
  - Kept `Artifact Conductivity` in ch35 as the state-variable definition needed for the theory chapter.
  - Added `Why Attractor Theory Is Not Enough`, a theory-focused WWCTV, and a new summary.
- Added `chapters/ch35b-conductive-artifacts-pivotal-processes.tex`.
  - New title: `Conductive Artifacts and Pivotal Processes`.
  - Moved the practical artifact/governance program from `Pivotal Process as Basin Transition` through the original summary.
  - Preserved moved section labels such as `sec:pivotal-process-ch35`, `sec:high-conductivity-artifact-ch35`, `sec:safety-case-view-ch35`, and `sec:wwctv-alignment-attractor`.
  - Removed the separate `Connection to Later Chapters` section and distributed those links into the summary, per the updated plan.
- Updated Part VIII input and gem/payoff signpost in `parts/part08-attractor-basins.tex`.
- Updated `metadata/book.yml`, generated `tables/chapter-map.tex` and `tables/part-roadmap.tex`, and regenerated `metadata/book-stats.md`.
- Updated static chapter-count/status surfaces: `README.md`, `scripts/check_structure.py`, and `metadata/claims-ledger.md` now reflect 48 chapter entries.
- Updated reviewer/LLM/formal/research-program surfaces:
  - `REVIEWING_FOR_AGENTS.md`
  - `llms.txt`
  - `formal/README.md`
  - `appendices/appH-research-program.tex`
- Updated `metadata/TODO.md`, `review/chapter-split-preferences-2026-06-28.md`, and `review/ch35-split-plan-2026-06-28.md` to mark the split as implemented.

## Decisions

- Used temporary `ch35b` rather than globally renumbering ch36+.
- Kept labels on moved sections stable to avoid cross-reference churn.
- Did not move the short `Artifact Conductivity` definition wholesale; ch35 keeps it as the theory chapter's core state variable, while ch35b owns the practical artifact design program.
- No Lean code change was needed. `formal/README.md` now notes `Certification.lean` spans ch35 including ch35b.

## Open / next

- Later chapter-numbering cleanup should decide whether to keep `ch19b`/`ch25b`/`ch35b`/`ch39b` or globally renumber.
- Optional future pass: review ch32/ch34/ch36/ch39/ch40 prose for places where artifact/governance references should cite ch35b explicitly.

## Key paths

- `chapters/ch35-alignment-attractor.tex`
- `chapters/ch35b-conductive-artifacts-pivotal-processes.tex`
- `parts/part08-attractor-basins.tex`
- `metadata/book.yml`
- `tables/chapter-map.tex`
- `tables/part-roadmap.tex`
- `metadata/book-stats.md`
- `appendices/appH-research-program.tex`
- `review/ch35-split-plan-2026-06-28.md`

## Commits

- None.

## Verification

- `make check` passed.
- `./build.sh` passed.
- `python3 scripts/book_stats.py` regenerated `metadata/book-stats.md`.
- `book.log` scan found no undefined references or citations after the final build.
- Read lints reported no diagnostics for edited files.
