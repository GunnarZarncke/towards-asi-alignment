# 2026-07-02 — Astro site: publication layer and session wrap

## Trigger
Continued Astro companion site work; end-of-session request to commit the whole site and report open items.

## Done
- **Worked example (Appendix D):** URL case fix (`/book/appd/`), BioShield callout on Generalist / Applied / Funder paths; `site-urls.ts` helpers.
- **Field-agenda subsumptions:** eight gem cards (`subsumption-*.md`), `FieldSubsumptionsTable`, Lean symbol + formula + bibliography links; graph + `/lean/` index.
- **Reference cards:** auto-generated from `.bib` + refsection cites (`sync-reference-cards.mjs`); chapter-grouped `/references/`; alphabetical `reference-index` card; publication links in card body.
- **Lean spine on web:** Graphviz SVG graphs, spine source snippets, playgrounds (P01/P15), overview diagram, node pages.
- **About / legal:** Impressum, author publications list; removed literature-review PDF from list; fixed UAD foundations paper link (book repo PDF, removed wrong TechRxiv preprint).
- **CI:** `.github/workflows/site.yml`; `serve-site.sh` / `serve-demos.sh` / demo backends.
- **Commit:** whole `site/` tree + supporting scripts, playgrounds, lean graph aliases (generated book/chapter/reference cards excluded via `site/.gitignore`).

## Decisions
- Generated content (`src/content/book/`, chapter/reference cards, `references.json`, lean graphs) stays gitignored; `npm run sync` before dev/build.
- Bib alias keys (`crossref`) merge to canonical entries; reference card filenames lowercased for Astro routes.
- Author publications live in `site/src/data/author-profile.json` (not manuscript).

## Open / next
- **Push:** branch is ahead of `origin/main` (15 commits after this one); user did not request push.
- **Not in site commit:** embedded-sim result JSON/MD churn, `src/demos/ch09-uad-coalition-board/index.html`, untracked experiment curves, `dist/` PDF, `book.bbl-SAVE-ERROR`.
- **Site deploy:** configure GitHub Pages base (`ASTRO_BASE=/towards-asi-alignment`) in workflow if not already verified on remote.
- **agency-detect PDFs:** many About-page paper links still point at `agency-detect` paths; several 404 — audit remaining entries.
- **appG on web:** Lean appendix prose not synced to book pages; field subsumptions link to PDF/repo only.
- **Manuscript:** conversation logs from 2026-07-01/02 site slices still untracked in drafts (optional to commit separately).

## Key paths
- `site/` — Astro app, sync scripts, cards, pages
- `serve-site.sh` — integrated dev server
- `context/lean_graph_node_aliases.json` — spine node → Lean decl map
- `formal/playgrounds/` — Lean 4 Web try-it-out snippets

## Commits
- *(this session commit — hash recorded after commit)*
