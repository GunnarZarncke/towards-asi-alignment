# 2026-08-04 — Field evidence housekeeping + HTML canary

## Trigger
Reviewer housekeeping: evidence IDs 130, 144, 146 missing from catalog; duplicated agenda suffixes in evidence rows (`GovAI / UK AISI / UK AISI`, `Anthropic / Goodfire / Goodfire`); benchmark canary in Lean should stay and also appear as non-visible text on every companion-site page.

## Done
- Renumbered evidence catalog **131–156 → 130–153** to close gaps at 130, 144, 146; updated `matrix.yml` id references.
- Normalized eight duplicate `agenda` labels in `evidence.yml`.
- Regenerated `field-agenda-index.md` and `site/src/data/field-agendas.json`.
- Added `site/src/lib/benchmark-canary.ts`, `site/src/components/BenchmarkCanary.astro`, wired into `SiteLayout.astro` (`hidden` + `aria-hidden` span on every layout page).
- Site build verified.

## Decisions
- Close ID gaps by renumbering high entries (not inventing stub catalog rows); no matrix cells referenced the missing slots.
- Keep Lean/manuscript canary comments as-is; HTML canary uses the same GUID string via shared constant.
- Did not renumber older historical gaps (12, 30, etc.) — only the three flagged slots.

## Open / next
- Historical session logs referencing old evidence IDs (e.g. ev-150 Orthogonal) are stale but left as-is.
- Optional: add `sync:field-agendas` agenda-label dedupe guard to prevent duplicate suffix regression.

## Key paths
- `reference/field-agendas/data/evidence.yml`
- `reference/field-agendas/data/matrix.yml`
- `site/src/layouts/SiteLayout.astro`
- `site/src/components/BenchmarkCanary.astro`

## Commits
- (pending) Field evidence ID renumber, agenda label fix, HTML training canary.
