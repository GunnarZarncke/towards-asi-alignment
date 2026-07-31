# 2026-07-07 — Institutional histories site overview hub

## Trigger

Follow-up to the institutional histories appendix site cards: user wanted Appendix M (`appM`) as an overview hub listing case-study cards (not embedded full LaTeX), wired into guided tours; then restore on-site full appendix text with clear links from the overview page.

## Done

- **`overviewOnly` appendix pattern:** `sync-chapter-cards.mjs` marks `appM` with `overviewOnly: true`; `[...slug].astro` skips synced book body on the hub and renders intro + `CardSection` grid of 11 mechanism cards.
- **Full text route:** `/cards/chapters/appM/full/` via extra static path; renders synced LaTeX body with “Case study overview” back-link. `bookFullHref()` added in `site-urls.ts`.
- **Overview links:** Full appendix linked from top buttons, inline intro markdown, sidebar “Full appendix” section, and bottom button row.
- **Tex link fix:** `tex-convert.mjs` relative links corrected for `/cards/chapters/{id}/` depth (sibling appendices, concept cards, references, PDF); `BOOK_CHAPTER_PDF_HREF` updated.
- **Cards:** Removed duplicate `institutional-genesis-and-decay.md` artifact; case cards now `related: chapters/appM`.
- **Guided tours:** `funder-policy.md` note updated; `philosopher.md` adds `appM` after attractor-control.
- **Book map:** `book/index.astro` lists Appendix M.
- Site build verified (`npm run build`).

## Decisions

- Overview hub stays canonical at `/cards/chapters/appM/`; full synced text at `/full/` subpath (reusable for any future `overviewOnly` appendix).
- PDF remains linked alongside on-site full text; overview intro uses relative markdown links (`full/`, PDF path).

## Open / next

- Unrelated lab-simulation work remains unstaged in the working tree.
- `appM` chapter thesis in synced markdown still contains `\ref{appj-institutional-translation}` (pre-existing label mismatch in TeX).

## Key paths

- `site/scripts/sync-chapter-cards.mjs`, `site/src/pages/cards/[...slug].astro`, `site/scripts/lib/tex-convert.mjs`
- `site/src/content/cards/institutional-*.md`, `site/src/content/reading-paths/funder-policy.md`, `philosopher.md`

## Commits

- `3507532` Add Appendix M site overview hub with full-text subroute.
