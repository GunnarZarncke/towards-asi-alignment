# 2026-06-17 — Session end: structure + INSTRUCTIONS sync

## Trigger
Multi-turn structural revision of book scaffold (lethality stress-test, scope/Turchin audit, chapter merges/removals) and final INSTRUCTIONS.md sync; user ended session.

## Done

### Book structure (44 chapters)
- **Part I:** added ch05 Assumptions, Scope, and Failure Coverage.
- **Part VIII:** ch33 Multi-Agent Strategic Coupling; removed standalone Cooperation/Privacy/Opacity and Percolation chapters—material **inserted as subsections** in ch33.
- **Part IX:** ch39 safety case, ch40 lethality stress-test; tripwires deferred.
- **Part X:** ch43 The Bearers of Value; removed standalone Merging and What Cannot Be Solved Technically—material **inserted as sections** in ch43.
- Subsections added: Coerced Correction (ch25), Paternalism Boundary (ch19).
- Renumbered ch05–ch45 → ch06–ch44; `scripts/check_structure.py` → 44 chapters.
- Deferred stubs in `drafts/chapter-notes/` (ch32, ch33, ch39, ch42, ch44).

### Docs & metadata
- `README.md`, `metadata/book.yml`, `tables/chapter-map.tex`, `frontmatter/executive-overview.tex`, `scripts/init_scaffold.py`, `metadata/terminology.md`.
- **`INSTRUCTIONS.md`** fully synced: §0 thesis/organizing frame, §4.1 consolidation table, §6.14–6.17, §7 chapter list with file paths, milestones 44-chapter criteria.

### Builds
- `./build.sh` and `make check` pass throughout.

## Decisions
- Yudkowsky lethalities = Ch 40 checklist only; Turchin = Ch 5 coverage audit only.
- Removed chapters are not standalone parts; content lives in ch33/ch43 subsections/sections.
- Part file `part09-adversarial-measurement.tex` kept (filename); part title is Safety Cases, Adversaries, and Open Cruxes.

## Open / next
- `TODO[citation]`: Turchin map (ch05), Yudkowsky lethalities (ch40).
- `TODO[formalize]` / `TODO[empirical-test]`: ICI, pivotal process, coalition tests.
- Draft stub prose in ch05, ch19, ch25, ch33, ch40, ch43.
- Tripwires deferred content: merge into ch39 or drop.
- Optional: README parity check (user declined in last turn).

## Key paths
- `INSTRUCTIONS.md` §4, §7
- `chapters/ch05-assumptions-scope-failure-coverage.tex`
- `chapters/ch33-multi-agent-strategic-coupling.tex`
- `chapters/ch40-lethality-stress-test-open-issues.tex`
- `chapters/ch43-bearers-of-value.tex`
- `drafts/conversation-summaries/INDEX.md`

## Commits
- (none — user did not request commit)
