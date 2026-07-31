# 2026-06-17 — Scope chapter, Turchin audit, chapter merges

## Trigger
Structural update: add Assumptions/Scope chapter, fold multipolar/blackmail/paternalism/bearer topics into existing chapters, use Turchin as coverage audit only, revise thesis wording.

## Done
- Inserted `ch05-assumptions-scope-failure-coverage.tex` (scope, $C_{\text{corr}}^{\text{society}}$, Turchin audit table).
- Renumbered ch05–ch45 → ch06–ch48 (44 chapters total).
- **Removed from spine** (not standalone parts): Cooperation/Privacy/Opacity, Percolation of Cooperation, Merging With Artificial Entities, What Cannot Be Solved Technically.
- **Inserted** their material into `ch48-multi-agent-strategic-coupling.tex` (subsections) and `ch47-bearers-of-value.tex` (sections).
- Deferred originals in `drafts/chapter-notes/ch46-`, `ch48-`, `ch46-`, `ch48-*-deferred.tex`.
- Added **Coerced Correction** to `ch46-correction-channel-integrity.tex`.
- Added **The Paternalism Boundary** to `ch19-tradeoffs-bundle-geometry.tex`.
- AI-halting footnote in `ch48-certification-without-construction.tex`.
- Updated all `parts/*.tex`, `metadata/book.yml`, `tables/chapter-map.tex`, `README.md`, `INSTRUCTIONS.md`, `frontmatter/executive-overview.tex`, `scripts/check_structure.py`, `scripts/init_scaffold.py`, `metadata/terminology.md`.
- `./build.sh` and `make check` pass.

## Decisions
- Assumptions chapter placed as ch05 at end of Part I (after problem reframing).
- Part X reduced to 4 chapters; removed standalone `Merging With Artificial Entities` and `What Cannot Be Solved Technically`; inserted as sections in ch47.
- Turchin and Yudkowsky both used as audits/checklists, not book spines.

## Open / next
- `TODO[citation]` for Turchin failure-mode map in ch05.
- Fill stub sections in new/merged chapters.
- Review whether deferred tripwires content belongs in ch46 safety case.

## Key paths
- `chapters/ch05-assumptions-scope-failure-coverage.tex`
- `chapters/ch35-multi-agent-strategic-coupling.tex`
- `chapters/ch26-correction-channel-integrity.tex`
- `chapters/ch19-tradeoffs-bundle-geometry.tex`
- `chapters/ch47-bearers-of-value.tex`

## Commits
- (none)
