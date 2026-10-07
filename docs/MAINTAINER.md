# Maintainer checklists

Action → follow-up rules for common repo changes. Extracted from session logs (especially CI failures), `make check`, and site sync scripts.

**Always:** run `make check` before push. Use `.venv/bin/python` or wrapper scripts — bare macOS `python3` lacks PyYAML (`docs/BUILD.md`).

**Site-visible changes:** `cd site && npm run sync` (full chain) or the narrower `sync:*` scripts listed below. Never `npm install` from repo root.

**Deep docs (do not duplicate here):** [`docs/BUILD.md`](BUILD.md) · [`docs/MANUSCRIPT.md`](MANUSCRIPT.md) · [`site/README.md`](../site/README.md) · [`references/README.md`](../references/README.md) · [`metadata/symbol-census/README.md`](../metadata/symbol-census/README.md) · [`INSTRUCTIONS.md`](../INSTRUCTIONS.md) · [`AGENTS.md`](../AGENTS.md)

---

## Field news

Every `field-news-*` slug in `metadata/field-news.yml` **must** have a matching quiz takeaway or `make check` fails.

| Step | Action |
|------|--------|
| 1 | Add row to [`metadata/field-news.yml`](../metadata/field-news.yml) (`slug`, `title`, `hook`, `summary`, `bookChapters`, `bridges`, `body`, `order`) |
| 2 | Write body [`metadata/field-news/bodies/YYYY-MM-slug.md`](../metadata/field-news/bodies/) |
| 3 | Optional meme: [`scripts/meme_workflow/`](../scripts/meme_workflow/) → embed in body → `site/public/field-news/memes/{basename}.jpg` |
| 4 | Sync: `cd site && npm run sync:field-news-memes && npm run sync:field-news` |
| 5 | **Quiz takeaway (required):** id `news-takeaway-{slug without field-news- prefix}` in [`site/src/content/quiz/questions.yml`](../site/src/content/quiz/questions.yml). Helper: add `Q(...)` to [`scripts/attic/write_news_takeaway_quiz.py`](../scripts/attic/write_news_takeaway_quiz.py), run it, copy into `questions.yml`. **`appearOn` must be `chapter:*` only** — never a news card. |
| 6 | Optional: `\autocite{}` in chapters; new `.bib` key if sources cited (see Bibliography) |
| 7 | Verify: `make check` (quiz bank row); spot-check `/news/` and the card page locally |

**Example:** slug `field-news-ward-monitoring-oct-2026` → quiz id `news-takeaway-ward-monitoring-oct-2026`.

**CI history:** `2026-09-19`, `2026-09-24`, `2026-10-07` — news card landed without quiz item.

---

## New symbol or formula

| Step | Action |
|------|--------|
| 1 | Check [`metadata/notation.md`](../metadata/notation.md) and [`metadata/symbol-census/symbol-contribution-audit.md`](../metadata/symbol-census/symbol-contribution-audit.md) for collisions |
| 2 | Define at first use in manuscript: `\symboldef` / `\symbolref`; add `\label{sec:...}` if glossary-linked |
| 3 | Add row(s) to `metadata/notation.md` |
| 4 | Regenerate: `make generate` (runs `extract_symbol_formula_graph.py`, `build_section_reference_graph.py`, `build_chapter_symbol_dependency.py`) |
| 5 | Optional SVG render: [`metadata/symbol-census/graphs/README.md`](../metadata/symbol-census/graphs/README.md) |
| 6 | If glossary term: add `bookLabels: [sec:...]` on concept in [`metadata/concepts.yml`](../metadata/concepts.yml) |
| 7 | Sync site notation: `cd site && npm run sync:notation` |
| 8 | Verify: `make check` (generate + structure) |

**Rules:** Part I (ch01–ch05) must not `\eqref` equations defined after ch05 (`scripts/check_structure.py`). Missing glossary anchors fail the **generate** step (`2026-09-25`: VFS/BIQ/EAI needed `sec:experimental-methodology-shorthand` + concept `bookLabels`).

---

## Predictions / Appendix H market

| Step | Action |
|------|--------|
| 1 | Edit print canon [`appendices/appP-bridge-predictions.tex`](../appendices/appP-bridge-predictions.tex) |
| 2 | Update [`metadata/predictions.yml`](../metadata/predictions.yml) (`shortTitle`, `longTitle`, `listingStatus`, `outcomes`, versions) |
| 3 | Update [`metadata/safety-case-model.yml`](../metadata/safety-case-model.yml) if PRA nodes change |
| 4 | Sync: `cd site && npm run sync:predictions && npm run sync:safety-case-model && npm run sync:chapters` |
| 5 | Verify PDF: `./build.sh`; verify sync guard (fine print must repeat Common rules verbatim — `site/scripts/sync-predictions.mjs`) |
| 6 | Verify: `make check`; site lib tests include safety-case demo |

**Invariants:** market IDs 01–18 are not renumbered; YES/NO/OTHER semantics; Common qualification block repeated in every market fine print (Markets 14, 19, 20 have documented exceptions). See `INSTRUCTIONS.md` §14.

**External listing (when ready):** sibling repo `ai-safety-claims` — see [`drafts/plans/predictions/eval-registry-split.md`](../drafts/plans/predictions/eval-registry-split.md).

---

## Bibliography / citation

| Step | Action |
|------|--------|
| 1 | Add BibTeX entry to appropriate [`references/*.bib`](../references/) file |
| 2 | Add `\bibsummary{key}{One sentence.}` in [`references/bibliography-summaries.tex`](../references/bibliography-summaries.tex) (alphabetical by key) |
| 3 | Cite in manuscript with `\autocite{key}` / `\cite{key}` |
| 4 | Verify: `make check` (citations + bibliography summaries rows) |

Do not put summaries in `.bib` files — see [`references/README.md`](../references/README.md).

Reference cards on the site regenerate via `cd site && npm run sync:reference-cards` (included in full `npm run sync`).

---

## Concept / bridge / projection card

| Step | Action |
|------|--------|
| 1 | Edit roster + body: [`metadata/concepts.yml`](../metadata/concepts.yml) + [`metadata/concepts/bodies/`](../metadata/concepts/bodies/) (same pattern for `bridges.yml`, `projections.yml`) |
| 2 | Optional `bookLabels: [sec:...]` for chapter cross-refs and glossary audit |
| 3 | Optional `claimId` — must match `## Claim ID: C-...` in [`metadata/claims-ledger.md`](../metadata/claims-ledger.md) |
| 4 | Sync: `cd site && npm run sync:concepts` (and/or `sync:bridges`, `sync:projections`, `sync:lean-checks`) |
| 5 | Bridge / field hub changes often also need `sync:bridge-graph`, `sync:field-agendas`, `sync:field-v2` |
| 6 | Verify: `cd site && npm run check:concepts`; `make check` |

**Card preview images:** see table in [`AGENTS.md`](../AGENTS.md) (concept / chapter / field-news / hand-authored).

Hand-authored cards: [`site/src/content/cards/*.md`](../site/src/content/cards/) with explicit `previewImage` or first in-body image.

---

## Chapter or appendix edit

| Step | Action |
|------|--------|
| 1 | Read module map [`formal/README.md`](../formal/README.md); skim matching `formal/AlignmentProofSpine/*.lean` |
| 2 | Calibrate claim strength: proof / counterexample / bridge — never “Lean proves ASI alignment” |
| 3 | Field comparisons: use [`appendices/appB-bridge-crosswalk.tex`](../appendices/appB-bridge-crosswalk.tex) |
| 4 | Process: [`INSTRUCTIONS.md`](../INSTRUCTIONS.md) §11 (WWCTV, worked example, counterexample) |
| 5 | New chapter/appendix: update [`metadata/book.yml`](../metadata/book.yml), `book.tex`, counts in `scripts/check_structure.py` |
| 6 | Build + check: `./build.sh && make check` |
| 7 | Site text: `cd site && npm run sync:chapters && npm run sync:chapter-cards` |
| 8 | New symbols: follow **New symbol or formula** above |
| 9 | Cursor/bash writes under `chapters/`, `appendices/`, `site/src/`: `python3 scripts/hooks/declare_edits.py '<glob>'` first |

---

## Experiment or backtest finding

| Step | Action |
|------|--------|
| 1 | Record in `experiments/{line}/results/FINDINGS.md` or `NEGATIVE_RESULTS.md` |
| 2 | Update [`docs/EXPERIMENTS.md`](EXPERIMENTS.md) and [`metadata/experiments.yml`](../metadata/experiments.yml) (backtests: [`metadata/experiments-backtests.yml`](../metadata/experiments-backtests.yml)) |
| 3 | Honor freeze / preregistration: [`docs/METHODOLOGY.md`](METHODOLOGY.md) |
| 4 | Sync: `cd site && npm run sync:experiments` |
| 5 | Verify: `cd site && npm run check:experiments`; `make lean` if Lean adapters changed |

Negatives are first-class — do not bury them. One rig, one results file, one FINDINGS entry per battery.

---

## Release / version bump

| Step | Action |
|------|--------|
| 1 | Add section to [`RELEASE_NOTES.md`](../RELEASE_NOTES.md) (newest first; fill `Commit:` hash after tag cut) |
| 2 | Bump release rows in [`README.md`](../README.md) and [`docs/MANUSCRIPT.md`](MANUSCRIPT.md) |
| 3 | Add `release-vX-Y-Z.md` to [`site/.gitignore`](../site/.gitignore) if new |
| 4 | Sync: `cd site && npm run sync:releases` |
| 5 | Gate: `make check` on the release cut |
| 6 | Annotated tag `vX.Y.Z` on the hash-fill commit |

Generated release cards stay gitignored; `/updates/` reads from `RELEASE_NOTES.md`.

---

## Field hub / matrix

| Step | Action |
|------|--------|
| 1 | Edit source YAML under [`reference/field-agendas/data/`](../reference/field-agendas/data/) |
| 2 | Sync: `cd site && npm run sync:field-agendas` |
| 3 | Field v2 JSON: `cd site && npm run sync:field-v2` (`make check` runs `sync:field-v2 --check`) |
| 4 | Evidence stance: edit stance YAML; `make check` runs `check-evidence-stance.py` |

---

## Quiz bank (non-news)

Essays and chapters also need takeaway-tagged questions with `appearOn: essay:*` or `chapter:chNN`. Gate: [`scripts/check_quiz_bank.py`](../scripts/check_quiz_bank.py).

| Constraint | Floor / cap |
|------------|-------------|
| Per bridge (MB1–MB11) | ≥ 2 questions |
| Multi-correct | ≥ 5% of bank |
| People/org prompts | ≤ 20% |
| Length tell | [`scripts/check_quiz_length_tell.py`](../scripts/check_quiz_length_tell.py) |

Draft batches live under [`site/src/content/quiz/drafts/`](../site/src/content/quiz/drafts/); merge with [`scripts/merge_quiz_drafts.py`](../scripts/merge_quiz_drafts.py) when adding batches.

---

## `make check` gate map

What each row enforces (`scripts/check.sh`):

| Check | Script / command |
|-------|------------------|
| generate | `generate_manuscript_tex.sh` — fragments, symbol/concept graphs |
| structure | `check_structure.py` — counts, Part I eqref rule |
| markdown links | `check_markdown_links.py` |
| citations | `check_citations.py` |
| bibliography summaries | `check_bibliography_summaries.py` |
| claim spine | `check_claim_spine.py` |
| evidence stance | `reference/field-agendas/scripts/check-evidence-stance.py` |
| open spine interfaces | `formal/scripts/check_open_spine_interfaces.py` |
| specify/construct instances | `formal/scripts/check_specify_construct_instances.py` |
| field-v2 sync | `npm run sync:field-v2 -- --check` |
| quiz bank | `check_quiz_bank.py` — **includes field-news takeaways** |
| quiz length | `check_quiz_length_tell.py` |
| field matrix tests | `reference/field-agendas/scripts/matrix-cell.test.mjs` |
| site lib tests | quiz, predictions demo, visit history, etc. |

**Separate CI:** `.github/workflows/lean.yml` (`make lean`); `.github/workflows/site.yml` (full Astro build).

`make check` does **not** build PDF, Lean, or the full site.

---

## CI failure quick reference

| Symptom | Likely fix | Session log |
|---------|------------|-------------|
| `missing news-takeaway-*` | Add quiz item; `appearOn: chapter:*` | 2026-09-19, 2026-09-24, 2026-10-07 |
| Generate step exit 1; missing glossary anchors | `\label{sec:...}` + concept `bookLabels` | 2026-09-25 |
| Markdown links fail on CI, pass locally | Run `make generate`; do not link untracked files | 2026-09-23, 2026-10-05 |
| `Expected N appendix files, found M` | Update `book.tex` / `check_structure.py` | 2026-06-26 |
| `sync:field-v2 --check` fails | `cd site && npm run sync:field-v2` | 2026-09-30 |
| PyYAML / yaml import error | `.venv` setup (`docs/BUILD.md`) | 2026-10-06 |
| Market fine print sync guard | Align App P with Common rules block | 2026-10-06 |
| Astro `Invalid Unicode escape` | LaTeX in `String.raw` frontmatter, not inline HTML | 2026-08-07 |
| Missing `\bibsummary` or cite key | `.bib` + summary line | various |
| Biber silent failure | `./clean.sh && make biber` | 2026-07-08 |

Full incident index: [`drafts/conversation-summaries/archive/`](../drafts/conversation-summaries/archive/) monthly INDEX files.

---

## Session logging (agents and humans)

After load-bearing changes: per-session log in [`drafts/conversation-summaries/`](../drafts/conversation-summaries/), update [`HANDOFF.md`](../drafts/conversation-summaries/HANDOFF.md) when open work shifts. Template: [`drafts/conversation-summaries/README.md`](../drafts/conversation-summaries/README.md).

Open work boards live in [`metadata/TODO.md`](../metadata/TODO.md) — not duplicated in HANDOFF.
