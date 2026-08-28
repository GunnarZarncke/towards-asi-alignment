# 2026-08-28 — Witness results in book and site

## Trigger
User asked to document Witness experimental results in the book and site, and to split the landing page into sims, external tests, and witness tests.

## Done
- Appendix I: host-trace synthesis paragraph; new § Witness tests with W-1–W-4; `W-` in ID list.
- `docs/EXPERIMENTS.md` three-class banner + Witness table.
- Site: `/experiments/` three sections; homepage three tiles (`#sims` / `#external` / `#witness`); coverage Kind column; `experiments.yml` kinds + ET-1–4 + witness line; sync 12 cards.
- Voice: chapter copy still omits the program name; App I and `/experiments/` may say witness tests.
- README, FAQ, experiment-methodology and ET cards updated.
- PDF rebuilt (`dist/pdf/towards-superintelligence-alignment.pdf`).

## Decisions
- External tests are first-class hub cards (stop/null/close summaries), not a fourth coverage-matrix column.
- Witness is an optional coverage column; missing cells read as —.
- W-findings indexed in App I with Manuscript `---` until a chapter cites them.

## Open / next
- Optional chapter cites of W-1–W-4.
- Phase 3 Witness (C-004 / C-007) still unpaid.

## Key paths
- `appendices/appN-experimental-evidence.tex`
- `site/src/pages/experiments/index.astro`
- `site/src/pages/index.astro`
- `metadata/experiments.yml`

## Commits
- pending (end of session)
