# 2026-07-03 — README split, guided paths, Peter Kuhn review (site/README)

## Trigger
End-of-session commit: incorporate Peter Kuhn reviewer feedback on orientation (reading paths, hyperlinks, claim wording, chapter map); split long README; promote GitHub Pages site; add Kuhn humanism essay to bib for philosopher path (not cited in book yet).

## Done
- **README split:** short root [`README.md`](../README.md) with companion site first; detail in [`docs/BUILD.md`](../docs/BUILD.md), [`docs/MANUSCRIPT.md`](../docs/MANUSCRIPT.md), [`docs/EXPERIMENTS.md`](../docs/EXPERIMENTS.md).
- **CONTRIBUTING.md:** official site URL; no longer “no website yet.”
- **Site guided tour:** expanded path copy (what you learn, time, PDF steps); role diagram on [`site/src/pages/paths/index.astro`](../site/src/pages/paths/index.astro); new **Philosopher path**; homepage CTA order (guided tour first).
- **Bibliography:** `kuhn2025humanism` in [`references/philosophy.bib`](../references/philosophy.bib) + summary; linked from philosopher path only.
- **Manuscript front matter** (Peter Kuhn review): intro claims 2–3 reframed, executive overview wording, Current Status drops printed chapter map, preface audience paths — **left uncommitted** this session (book tex separate from this commit).

## Decisions
- Peter Kuhn humanism essay: bib + website only; no mention in book acknowledgements/intro yet (author request).
- Chapter map removed from PDF Current Status; `metadata/book.yml` + site book index are the outsider-facing chapter list.

## Open / next
- Commit or integrate uncommitted `frontmatter/*.tex` Peter Kuhn edits when ready for a book commit.
- Rebuild PDF after front matter commit; redeploy site after push.

## Key paths
- `README.md`, `docs/`, `site/src/content/paths/`, `site/src/pages/paths/index.astro`
- `references/philosophy.bib` (`kuhn2025humanism`)

## Commits
- (this session commit hash below)
