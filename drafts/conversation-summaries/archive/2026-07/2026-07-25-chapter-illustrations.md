# 2026-07-25 — Chapter-opening illustrations (ch01–ch16)

## Trigger

User provided 16 genAI illustrations (`illustrations/`) plus a combined ChatGPT
prompt/caption transcript for chapters 1–16, and asked to: split the prompt
transcript into one file per chapter, title each illustration, rename the
image files, insert the illustrations into the chapters (title-only caption),
and add them to the site with the title linking to an otherwise-unlisted card
showing the full generation prompt. Mid-session the user recovered fuller
per-chapter illustration specifications (concept name, full compositional
brief, condensed generation prompt) and asked to fold those in where
appropriate.

## Done

- Split `illustrations_1-16_prompt.md` into `drafts/illustrations/prompts/chNN.md`
  (frontmatter: `chapter`, `title`, `image`); deleted the original combined file.
- Moved/renamed the 16 source PNGs into `figures/illustrations/ch<NN>_<slug>.png`.
- Added a `\begin{figure}...\end{figure}` block (title-only caption) into each
  of `chapters/ch01-*.tex`–`ch16-*.tex`, right after `\label{ch:...}`.
- Added `scripts/generate_web_illustrations.py` to produce compressed,
  web-sized JPEGs into `figures/illustrations/web/` (site uses these; PDF
  keeps the original PNGs).
- Added a new Astro `illustrations` content collection
  (`site/src/content.config.ts`) with `chapterId`, `title`, `image`, `alt`;
  authored `site/src/content/illustrations/chNN.md` for all 16 chapters.
- Added `site/src/pages/illustrations/[id].astro` — an unlisted, `noindex`
  page rendering the illustration (web JPEG) and its full generation prompt,
  linked back to the chapter.
- Excluded `/illustrations/` from the sitemap (`site/astro.config.mjs`).
- Extended `site/scripts/lib/tex-convert.mjs`: figures under
  `figures/illustrations/` render with the web JPEG, get an `alt` from the
  matching illustration frontmatter (`loadIllustrationAlts`), and their
  caption links to the `/illustrations/<chapterId>/` card
  (`webIllustrationPath`, `relIllustrationHref`). `sync-chapters.mjs` wires
  `illustrationAlts` into the conversion context.
- **Second pass (this session's main new work):** user recovered full
  per-chapter specs (a named concept, full composition brief, condensed
  generation prompt) and added them into the body of each
  `drafts/illustrations/prompts/chNN.md`, replacing the placeholder/caption-only
  content for ch01–ch15 (ch16 already had the full spec from the first pass).
  For each chapter: extracted the new recommended title (e.g. ch01 caption
  "Connection of Science and Network" → concept title "The System Outside
  the Glass Box"), and propagated it to (a) the `title:` frontmatter of the
  drafts prompt file, (b) the chapter's LaTeX `\caption{}`, and (c) a
  regenerated `site/src/content/illustrations/chNN.md` (new `title`, new
  hand-written `alt` text summarizing the new brief, full spec body). Image
  filenames were deliberately **not** renamed to match the new titles (see
  Decisions).
- Verified via `npm run sync` (chapter + illustration content sync, no
  errors), `npm run build` (745 pages, clean), and `make check` (structure /
  citation / bibliography-summary checks, all passing).

## Decisions

- Did not rename the 16 PNG/JPG asset files to match the newly recovered
  titles. The frontmatter `title` is independent of the filename slug;
  renaming would have required touching every `.tex` include, the web-JPEG
  pipeline, and re-verifying file identity for no functional benefit — pure
  churn against the surgical-changes rule.
- Site illustration-prompt pages are `noindex` and excluded from the sitemap
  by design (they're meant to be reachable only via the in-chapter caption
  link, not indexed or browsable).
- Kept the original high-resolution PNGs for LaTeX/PDF output and generated a
  separate compressed JPEG line for the site, rather than compressing the
  PDF-facing images.

## Open / next

- None outstanding for this task. If further illustration specs surface for
  chapters beyond 16, or the book gains illustrations for later chapters,
  follow the same split/rename/figure-insert/site-collection pattern.

## Key paths

- `drafts/illustrations/prompts/chNN.md` — source specs (title + full brief).
- `figures/illustrations/` (PNG, PDF-facing) and `figures/illustrations/web/`
  (JPEG, site-facing).
- `site/src/content/illustrations/chNN.md` + `site/src/pages/illustrations/[id].astro`.
- `site/scripts/lib/tex-convert.mjs` (`webIllustrationPath`,
  `loadIllustrationAlts`, `convertFigure`).
- `scripts/generate_web_illustrations.py`.

## Commits

- (pending — see commit created at end of this session)
