# 2026-06-17 — Book structure: lethality stress-test chapter

## Trigger
Revise book structure so Yudkowsky-style lethalities are a single late stress-test chapter, not the organizing frame. Add pivotal-process framing, inferential coupling in multipolar section, and Part IX restructure.

## Done
- Renamed `ch40-safety-case.tex` → `ch39-safety-case.tex`; moved `ch39-tripwires` to `drafts/chapter-notes/ch39-tripwires-stop-conditions-deferred.tex`.
- Added `chapters/ch40-lethality-stress-test-open-issues.tex` (lethality table, open problem ledger, Yudkowsky absence-of-structure framing, epistemic-status section, required TODOs).
- Updated `parts/part09-adversarial-measurement.tex`: Part title → Safety Cases, Adversaries, and Open Cruxes; order ch36–38, ch39 safety case, ch40 lethality.
- Updated multipolar stubs: `ch33-cooperation-percolation.tex` ($\tilde{\kappa}_{ij}$, ICI, key claims); `ch35-alignment-attractor.tex` (pivotal process / basin transition); `ch32` cross-ref.
- Updated `metadata/book.yml`, `tables/chapter-map.tex`, `tables/artifacts-table.tex`, `metadata/terminology.md`, `metadata/open-problems.md`, `README.md`, `INSTRUCTIONS.md` (Part IX, §6.12 pivotal process), `frontmatter/executive-overview.tex`, `scripts/init_scaffold.py`.
- `./build.sh` and `make check` pass.

## Decisions
- Tripwires chapter deferred (not deleted); removed from Part IX spine per user spec—may merge into safety-case later.
- Kept part file name `part09-adversarial-measurement.tex` (repo convention); only part *title* and includes changed.
- Inferential coupling formalization placed in ch33 (Percolation of Cooperation); pivotal process in ch35 (Alignment Attractor).

## Open / next
- Fill ch40 prose beyond checklist stub; add Yudkowsky lethalities citations (`TODO[citation]`).
- Formalize ICI and pivotal-process conditions (`TODO[formalize]` in ch33, ch35, ch40).
- Decide fate of deferred tripwires chapter (merge into ch39 or ch30).

## Key paths
- `chapters/ch40-lethality-stress-test-open-issues.tex`
- `parts/part09-adversarial-measurement.tex`
- `chapters/ch33-cooperation-percolation.tex`
- `chapters/ch35-alignment-attractor.tex`
- `INSTRUCTIONS.md` §7 Part IX

## Commits
- (none — user did not request commit)
