# 2026-07-14 — Experimental evidence appendix, global IDs, site sync

## Trigger
Session arc: (1) add Appendix I with curated experimental findings and chapter cross-cites; (2) eliminate colliding finding IDs (`G-`/`F-`/`N-` across lines); (3) widen landscape bridge tables; (4) update companion site.

## Done
- **Appendix I** (`appendices/appN-experimental-evidence.tex`, untracked): curated findings by experiment line (positive/negative/ambiguous), section-level manuscript backrefs, experiment descriptions, landscape bridge/feature coverage matrix (`pdflscape`). Chapter cites in ch07/ch11/ch33/ch34 use `finding:<global-id>` labels.
- **Global finding IDs** (`docs/FINDING_IDS.md`, `scripts/migrate_finding_ids.py`): prefixes `AD-`/`TS-`/`ES-`/`GA-`/`LS-`/`GL-` per line; ~171 files migrated in ledgers and shared docs. Appendix curated rows use **ledger global IDs** (`GL-11` not `GL-1`; `LS-28`/`LS-30`/`LS-32`/`LS-33`; `GA-9`/`GA-16`/`GA-22`). Removed erroneous appendix `LS-6` row (collided with ledger board-capture finding).
- **Manuscript/docs:** `metadata/claims-ledger.md`, `metadata/experiments.yml` (`findingIdPrefix` per line), `docs/EXPERIMENTS.md`, `book.tex` (`pdflscape` + `\input{appN}`), `scripts/check_structure.py` (`APPENDIX_COUNT = 14`).
- **Landscape tables:** bridge/feature matrix columns span full `\linewidth` (~30% wider effective cell width); `\LTleft`/`\LTright` zeroed; shared `\appnbridgecols` column spec.
- **Site:** registered `appN` in `site/scripts/sync-chapters.mjs` and `sync-chapter-cards.mjs` (fixes unresolved `finding:gl-*` / `appn-experimental-evidence` labels); `npm run build` clean — 55 book pages/cards, `experiments.json` + 6 experiment cards.
- `make check` clean.

## Decisions
- Appendix curated index **reuses ledger numbers** — one ID (`GL-11`) everywhere. Toy line keeps `TS-1`…`TS-3` as appendix-only until a numbered ledger exists.
- Cross-line historical refs in experiment `PLAN.md`/`DESIGN.md` prose (`F-22`, `N-10`, etc.) left for optional follow-up; load-bearing ledgers and manuscript cites are migrated.
- Session logs retain deprecated `G-`/`F-`/`N-` as historical record.

## Open / next
- **Commit** when ready — large uncommitted tree (appendix, migration, site sync, experiment ledgers). Do not stage unrelated drafts (`foresight-*`, `ai-salon-*`, older conversation logs) unless intended.
- Rebuild PDF (`./build.sh`) if `dist/pdf/` should match latest appendix layout; root `book.pdf` may be newer than `dist/pdf/`. Remove stale `book.bcf-SAVE-ERROR` after a clean build if present.
- Optional: bulk-update cross-line citations in experiment design docs (`F-*`→`GA-*`, `N-*`→`ES-*`).
- Embedded `TODO.md` `G-1` is a **task** id, not a finding.

## Key paths
- `appendices/appN-experimental-evidence.tex`
- `docs/FINDING_IDS.md`, `scripts/migrate_finding_ids.py`
- `metadata/experiments.yml`, `metadata/claims-ledger.md`
- `site/scripts/sync-chapters.mjs`, `site/scripts/sync-chapter-cards.mjs`
- `experiments/*/results/FINDINGS.md` or `NEGATIVE_RESULTS.md`

## Commits
- (none this session)
