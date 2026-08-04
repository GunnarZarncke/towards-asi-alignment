# 2026-07-06 — Site experiments page (Tier 1–3)

## Trigger
Implement Tier 1–3 experiment surfacing on the companion site (`/experiments/`, coverage matrix, MB card evidence updates, `sync-experiments.mjs`) and resolve duplication between `docs/EXPERIMENTS.md` and structured data without template-generating the markdown.

## Done
- Added `metadata/experiments.yml` — machine-readable claim strength, build order, headline findings, coverage matrix, ledger links, how-to-read bullets.
- Added `site/scripts/sync-experiments.mjs` → `site/src/data/experiments.json`; `check-experiments.mjs` validates column/cell consistency.
- Added `/experiments/` page + `ExperimentCoverageTable.astro` component.
- Nav link, index callout, FAQ item, engineer-evals / researcher-applied path copy.
- Updated MB card `evidenceNotes` on mb1, mb4, mb6, mb7, mb8, mb9, mb10 with goal-agent + lab-sim pointers.
- `docs/EXPERIMENTS.md` top pointer to YAML (narrative stays canonical prose).
- Wired `sync:experiments` + `check:experiments` into `site/package.json`; added `js-yaml` dependency.
- Site build verified (`640` pages).

## Decisions
- **Option A (chosen):** YAML = structured facts for site sync; `EXPERIMENTS.md` = canonical narrative. Manual dual maintenance when tables/findings change — same pattern as `book.yml` / manuscript. No template generation of markdown.
- Coverage table lives only in YAML + site; EXPERIMENTS.md table kept for now (still the narrative doc's closing section) with cross-reference at top. Future option: replace md table with one-line pointer to YAML/site.

## Open / next
- User may want to strip duplicate coverage table from `EXPERIMENTS.md` once `/experiments/` is trusted.
- Commit when requested (site + metadata + docs + card updates; not lab-simulation drafts).

## Key paths
- `metadata/experiments.yml`
- `site/scripts/sync-experiments.mjs`
- `site/src/pages/experiments/index.astro`
- `site/src/components/ExperimentCoverageTable.astro`
- `docs/EXPERIMENTS.md`

## Commits
- Add experiments page with YAML sync and bridge evidence updates (this session).
