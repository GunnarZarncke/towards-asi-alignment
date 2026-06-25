# 2026-06-25 — UAD papers context import

## Trigger
User asked to copy three new UAD papers from sibling `agency-detect` into `context/` and extract content in the usual way.

## Done
- Copied PDFs from `../agency-detect/docs/papers/`:
  - `access-uad/access-uad.pdf` → `context/access-uad.pdf`
  - `smooth-uad/smooth-uad.pdf` → `context/smooth-uad.pdf`
  - `stealth-capability-bounds/stealth-capability-bounds.pdf` → `context/stealth-capability-bounds.pdf`
- Ran `scripts/extract_pdf_to_md.py` → `context/extracts/{access-uad,smooth-uad,stealth-capability-bounds}.md` (11, 8, 10 pages).
- Updated `metadata/source-canon.md` source map with TeX/PDF paths.
- Updated `INSTRUCTIONS.md` §3.2 agent-boundary table.
- Added `zarncke2026access`, `zarncke2026smoothing`, `zarncke2026stealth` to `scripts/import_source_map_refs.py` and regenerated `references/internal-project-sources.bib`.

## Decisions
- Sibling repo is `agency-detect` (user said "agent-discovery"); three new papers are access-uad, smooth-uad, stealth-capability-bounds per `agency-detect/docs/papers/README.md`.
- `zarncke2026access` bib key added manually (no standalone entry in agency-detect `refs.bib` yet); smoothing/stealth keys match agency-detect.

## Open / next
- Wire new papers into relevant chapters (ch06–ch07 measurement/adversarial UAD; ch10 stealth/opacity; ch36 passive observation vs handle tests).
- Optional: add `zarncke2026access` to agency-detect `refs.bib` for cross-repo consistency.

## Follow-up (2026-06-25)
- Fixed duplicate bib keys: `uad2025`/`biq2025`/`eis2025`/`abc2025` are now `crossref` aliases to canonical `zarncke2025*` entries; restored `zarncke2026value-bottleneck`; updated `scripts/import_source_map_refs.py` dedup logic.

## Key paths
- `context/extracts/access-uad.md` — handle-aware access-model UAD; impossibility under access equivalence; intervention-value criterion.
- `context/extracts/smooth-uad.md` — observation-channel distortion \(\delta_K\), effective sample size \(T_{\mathrm{eff}}\), recoverability bound.
- `context/extracts/stealth-capability-bounds.md` — stealth–capability tradeoff; multi-resolution UAD; hidden-policy bound.
- `metadata/source-canon.md` — durable source map.

## Commits
- `bc62549` — Import three new UAD papers into context and deduplicate internal bib keys.
