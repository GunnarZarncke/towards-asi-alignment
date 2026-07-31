# 2026-07-24 — Site feedback: PDF, negative results, Graphviz sources, glossary cards

## Trigger
Companion-site reader feedback: PDF links failing via GitHub; experiment negative results only on GitHub; Lean Graphviz sources unavailable to bots; jargon on cards (boundary residual, value-bundle geometry) without accessible definitions.

## Done
- **PDF on site:** `copy-book-pdf.mjs` now falls back to `fetch-book-pdf-core.mjs` when local `dist/pdf/` is missing (CI and `SITE_FETCH_PDF=1`). Removed redundant CI fetch step; `CI=true` on build. Prominent **Download PDF** on Start Here and book map; FAQ answer links to on-site PDF.
- **Negative results:** New concept card `negative-results` + hub body with on-site ledger table. `sync-experiments.mjs` mirrors ledger markdown to `src/content/experiment-ledgers/` and `public/experiment-ledgers/`; rendered pages at `/experiments/ledgers/{lineId}/`. Experiments page, generalist path, homepage caveat row, and `evidence-and-uncertainty` / `experiment-methodology` cross-links updated.
- **Graphviz sources:** `sync-lean-spine.mjs` copies `.dot` files beside SVGs in `public/lean-graphs/`; unobtrusive download links on `LeanGraph`, `LeanOverviewDiagram`, and graph pages.
- **Glossary → cards:** Added glossary terms for **Boundary residual** and **Value-bundle geometry**; sharpened `boundary-residual` card summary. Nav **Glossary** link added.

## Decisions
- GitHub ledger URLs kept as secondary links; primary experiment ledger links are on-site.
- Raw ledger markdown exposed at `/experiment-ledgers/{id}.md` for agents; rendered HTML at `/experiments/ledgers/{id}/` for humans.

## Open / next
- Deploy and verify live PDF + ledger pages + `.dot` downloads after push to main.
- Optional: sync `llms.txt` with negative-results hub and ledger URLs.

## Key paths
- `site/scripts/copy-book-pdf.mjs`, `site/scripts/lib/fetch-book-pdf-core.mjs`
- `metadata/concepts.yml`, `metadata/concepts/bodies/negative-results.md`
- `site/scripts/sync-experiments.mjs`, `site/src/pages/experiments/ledgers/[id].astro`
- `site/scripts/sync-lean-spine.mjs`, `site/src/components/LeanGraph.astro`
- `.github/workflows/site.yml`

## Commits
- `566879a7` — Improve companion site PDF access, negative results, and Lean graph sources.
