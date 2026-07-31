# 2026-07-01 — Astro site thin slice

## Trigger

User asked to build a static Astro website for *Towards Superintelligence Alignment* using GitHub Actions, then iterated the plan toward a simpler companion site inspired by LessWrong tag/wiki pages and sequences. User explicitly asked to implement the plan and save a copy of the plan as part of the conversation log.

## Done

- Added a standalone Astro site under `site/`.
- Added a small LessWrong-inspired light theme with warm background, card surfaces, badges, readable typography, and static-first layout.
- Added one generic card content model with `type` and `status` fields.
- Added 10 seed cards:
  - `value-bundle-transport`
  - `bearer-persistence`
  - `correction-channel-integrity`
  - `successor-stability`
  - `attractor-control`
  - `boundary-discovery`
  - `bridge-assumptions`
  - `what-not-claiming`
  - `evidence-and-uncertainty`
  - `deployment-gate`
- Added four fixed audience paths:
  - `generalist`
  - `researcher`
  - `engineer-evals`
  - `funder-policy`
- Added static pages:
  - `/`
  - `/cards/`
  - `/cards/[slug]/`
  - `/paths/`
  - `/paths/[slug]/`
  - `/faq/`
  - `/book/`
- Added `scripts/sync-book-yml.mjs`, which reads the subset of `metadata/book.yml` needed for the Book Map without parsing LaTeX-heavy YAML fields.
- Added `.github/workflows/site.yml` for GitHub Pages deployment from `main` and PR build checks.
- Installed Astro dependencies in `site/` and generated `site/package-lock.json`.
- Verified `cd site && npm run build` succeeds and emits 20 static pages.
- Checked IDE diagnostics for `site/`; no linter errors were reported.

## Decisions

- Keep the site as a companion, not a platform or wiki.
- Keep the PDF as canonical long-form.
- Launch with one generic card model instead of separate systems for concepts, bridges, objections, artifacts, and glossary.
- Launch with four fixed audience paths instead of a dynamic prerequisite graph.
- Defer Pagefind search until there are enough pages to search.
- Defer dark mode, full glossary import, full bridge database, objection library, artifact library, translations, and TeX-to-web chapter conversion.
- Keep Lean, experiments, demos, and negative results as later in-context annotations, not standalone top-level sections.
- Disable Astro telemetry via npm scripts so local builds do not try to write outside the workspace.
- Use a line-oriented `book.yml` subset reader because the Node YAML parser rejects existing LaTeX backslashes in double-quoted `summary_latex` fields.

## Open / next

- Review the public copy and decide whether the first 10 seed cards are the right starting set.
- Add Pagefind only after the card set is large enough to justify search.
- Add a visual pass after seeing the deployed page in a browser.
- Add bridge-specific cards only if the bridge overview card becomes too dense.
- Add artifact cards for procurement questions and deployment gates if the engineer/policy paths feel useful.

## Key paths

- `site/package.json`
- `site/astro.config.mjs`
- `site/src/content.config.ts`
- `site/src/content/cards/`
- `site/src/content/paths/`
- `site/src/pages/`
- `site/src/styles/global.css`
- `site/scripts/sync-book-yml.mjs`
- `.github/workflows/site.yml`
- `metadata/book.yml`
- `.cursor/plans/astro_static_site_accbe1b0.plan.md` (source plan outside repo; snapshot below)

## Plan snapshot

### Overview

Build a small static Astro companion site under `site/` for one authored framework. The first version proves the reader experience with Start Here, fixed audience paths, a small FAQ, a few canonical cards, and the PDF. Search, richer proof/evidence annotations, objections, artifacts, glossary, translations, and chapter web are later layers.

### Thin public slice

The first version should be a minimum durable companion site, not a miniature platform. It should answer: can a new reader understand the thesis, pick a path, find a term, read a short card, and get to the PDF?

Build only:

- Start Here
- Four fixed audience paths
- One reusable card template
- A small FAQ
- A compact Book Map
- PDF and GitHub links
- GitHub Pages deployment

Everything else is a later layer: full glossary, bridge database, objection library, artifact library, Lean panels, experiment panels, demos, translations, dark mode, chapter HTML, and discussion integration.

### Design principles

- Companion, not platform.
- Solo-maintainable.
- Fixed paths before clever navigation.
- Graceful failure: static HTML, canonical URLs, PDF download, and plain citations survive if interactive layers break.
- Clarified positions, not hosted debates.
- Optimize for understanding and decisions.
- Steelman critic boxes over social rationality.
- No core social features.
- Integrate outward to LessWrong, Alignment Forum, EA Forum, Substack, or GitHub issues rather than recreating those platforms.
- Answer concrete questions.
- Use FAQ as the first question-led entry point.
- Prefer one good card template over many page types.
- Prefer four strong audience paths over eight weak ones.
- Prefer hand-curated seed content over premature import/conversion pipelines.
- Add automation only after the manual version proves the shape.

### LessWrong-inspired UI

- Borrow tag/wiki pages, sequences, epistemic status markers, content-first layout, concept indexes, resource blocks, readable typography, warm neutral backgrounds.
- Do not borrow comments, karma, voting, recommendation tabs, logged-in personalization, heavy SPA behavior, or discussion pages.
- Use a calm, investigative, institutional tone.
- Use a light warm grey background, white card surfaces, muted text, restrained teal links, and soft status pills.

### MVP surfaces

- Start Here: one thesis, five failure modes, one diagram-in-words, one caveat box.
- Paths: four fixed audience routes.
- Cards: one generic template with a `type` badge.
- FAQ: 10-15 seed questions, hand-curated.
- Book: compact Book Map plus PDF download.

### Launch paths

- Generalist: Start Here, key cards, caveat, PDF Part I pointer.
- Alignment researcher: bridge overview, core cards, Lean/open-problem pointers.
- Safety engineer / eval builder: correction, boundary, evidence, and artifact cards.
- Funder / policy: decision triggers, scope assumptions, institutional translation, artifacts.

### Seed cards

- Value-bundle transport
- Bearer persistence
- Correction-channel integrity
- Successor stability
- Socio-technical attractor control
- Bridge axioms overview
- What this book is not claiming
- Correction-channel evidence
- Safety-case artifact / deployment gate

### Phases

Phase 0: thin public slice.

- Scaffold Astro, Pages config, canonical URL scheme.
- Simple LessWrong-inspired light theme, readable typography, one card template.
- Start Here page.
- 8-12 seed cards.
- Four audience paths.
- PDF download and Book Map shell from `book.yml`.
- FAQ page with 10-15 seed questions.
- GitHub Actions deploy workflow.

Phase 1: make it useful.

- Add Pagefind once there are enough pages to search.
- Add outbound discussion links.
- Add 5-10 more cards based on what feels missing.
- Add one or two artifact cards.

Phase 2: bridge and evidence layer.

- Add bridge cards for `MB1`-`MB9` if the bridge overview card is too dense.
- Add lightweight related-link panels for Lean nodes, experiment summaries, negative results, and demos.
- Keep Formal Spine, Experiments, and Demos as in-context links, not standalone hubs.

Phase 3: objections and reference depth.

- Add objection cards from review feedback and WWCTV / uncertainty ledger.
- Expand artifact cards.
- Expand FAQ.
- Add glossary index if card search is not enough.

Later:

- Dark mode.
- Full glossary import from `terminology.md`.
- Bibliography browse.
- Chapter summaries or TeX-to-web conversion.
- Translations.
- Optional community contribution docs.

## Commits

- None.
