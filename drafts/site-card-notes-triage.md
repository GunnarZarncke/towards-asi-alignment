# Site card notes triage

**Status: CLOSED** (2026-08-17). Execution phases 0–6 shipped; commits `e91799b2` (Phases 0–3), `ceff7e97` (Phases 4–6).

Structured tracker migrated from `drafts/attic/tsa-notes-export-2026-08-15.txt` (Aug 15, 2026). Raw export archived. **Do not reopen as an active plan** — use `metadata/TODO.md` § Site for deferred follow-ups.

**Legend:** `resolved` · `done` · `deferred` · `phase N` (execution phase, all complete)

---

## Group A — Site UX and navigation

| ID | Status | Phase | Note | Target |
|----|--------|-------|------|--------|
| A1 | **done** | 1 | Book nav before PDF on `/book/` hero | `site/src/pages/book/index.astro` |
| A2 | **done** | 1 | Remove Status / Formal density columns | `site/src/pages/book/index.astro` |
| A3 | deferred | — | “Also on the site” follows book material order | `metadata/TODO.md` § Site |
| A4 | deferred | — | Explicit part hub cards | `metadata/TODO.md` § Site |
| A5 | **done** | 1 | Standalone claims below Guided Tour on homepage | `site/src/pages/index.astro` |
| A6 | deferred | — | Review standalone claims publishability | `metadata/TODO.md` § Site |
| A7 | **done** | 6 | Chapter figures not cached (cross-origin GitHub raw URLs) | `tex-convert.mjs`, `sw.js`, `site/public/figures/` |
| A8 | **done** | 6 | Standard icons for page-notes panel | `PageNotes.astro` |
| A9 | **done** | 6 | Mobile keyboard overlaps panel buttons | `PageNotes.astro` |
| A10 | **done** | 6 | Highlight marks need tap-to-open on mobile | `PageNotes.astro` |
| A11 | **done** | 6 | Expand panel weak on mobile | `PageNotes.astro` |
| A12 | **done** | 5 | Formulas overflow on narrow mobile | `global.css`, sync pipeline |
| A13 | **done** | 1 | Chapter `.tex` source → GitHub blob link | `site/src/pages/cards/[...slug].astro` |
| A14 | deferred | — | Submit notes to site (beyond localStorage) | `metadata/TODO.md` § Site |

---

## Group B / E4 — LaTeX→site sync bugs

| ID | Status | Phase | Note | Target |
|----|--------|-------|------|--------|
| B1 | **done** | 5 | Raw `\symboldef` / `\symbolref` in synced chapters | `tex-convert.mjs` |
| B2 | **done** | 1 | Titlepage `{ Towards Superintelligence Alignment}` literal braces | `tex-convert.mjs` (brace groups) |
| B3 | **done** | 1 | `\hyperref` → broken “as a for human-correctable” in part roadmap | `tex-convert.mjs` (`hyperref`, `gloss`) |
| B4 | **done** | 5 | ch10 “We distinguish three layers” — block below doesn’t render | `tex-convert.mjs` |
| B5 | **done** | 5 | ch10 formula label / symboldef leak | B1 + KaTeX |

---

## Group C — Frontmatter editorial

| ID | Status | Phase | Note | Target |
|----|--------|-------|------|--------|
| C1a | **done** | 2 | Remove “Many chapters are still drafts” (preface) | `frontmatter/preface.tex` |
| C1b | **done** | 2 | Remove “Many chapters are still first drafts” | `frontmatter/current-status.tex` |
| C1c | **done** | 2 | Update current-status maturity paragraph | `frontmatter/current-status.tex` |
| C2a | **done** | 2 | Remove “serious” from exec-overview safety case | `frontmatter/executive-overview.tex` |
| C2b | deferred | — | Remove fluff / magic-sentence passage | `frontmatter/introduction.tex` (optional editorial) |
| C2c | **done** | 2 | Remove External Doom Arguments section + preface pointer | `executive-overview.tex`, `preface.tex` |
| C2d | **done** | 2 | Trim redundancy; general terms in “What This Book Tries to Establish” | `executive-overview.tex` |
| C2e | **done** | 2 | Related content → Part I (ch01) on frontmatter card | `sync-chapter-cards.mjs` |
| C3 | **resolved** | — | Six connected claims / TL;DR order (Krym Phase 1–2) | — |
| C4 | **done** | 2 | Verify-only terminology grep (non-intro frontmatter vs App E) | preface plain-first lead |
| C5a | **done** | 2 | Glossary link (manuscript + site) | preface, exec-overview |
| C5b | **done** | 2 | GI comparison: static alignment breaks before SI | `dynamical-guarantee.md`, ch01 |
| C5c | deferred | — | CIRIS end-to-end walkthrough | `metadata/TODO.md` Real worked example |

---

## Group D — Chapter 9 (`ch09-composite-agent.tex`)

| ID | Status | Phase | Note |
|----|--------|-------|------|
| D1 | **done** | 3 | Rephrase “This preservation program” thesis |
| D2 | **done** | 3 | Forward ref: plain terms for correction / value formation / bearer maps |
| D3 | **done** | 3 | Illustrative example before abstract composite claim |
| D4 | **done** | 3 | Motivate formalism before “Let the observed world at time t…” |
| D5 | **done** | 3 | Lightcone footnote on “No real boundary is perfect” |
| D6 | **done** | 3 | Optimizer spread + model self-model (Kulveit/Zarncke cites) |
| D7 | deferred | — | Add site to Substack → `metadata/TODO.md` § Outreach |
| D8 | deferred | — | Notes submittable → A14 |

---

## Group E — Chapter 10 (`ch10-strategic-opacity.tex`)

### E1 + E2 — Prose and ordering (Phase 4)

| ID | Status | Note |
|----|--------|------|
| E1a–E1h | **done** | Prose trims, examples, action-channel invariant, decomposition cross-ref |
| E2a–E2c | **done** | Hubinger alignment, filter-family gloss, trimmed bundle preview |

### E3 — Cruxes (Phase 4)

| ID | Status | Note |
|----|--------|------|
| E3a–E3c | **done** | Oversight vs dangerous opacity; correction capacity; soften “We infer” |

### Deferred

| ID | Status | Note |
|----|--------|------|
| E3d | deferred | Alignment-faking / sleeper agents experiment line → `metadata/TODO.md` § Site |
| E3e | deferred | Chapter-end exercises + online quiz → `metadata/TODO.md` § Site |

---

## Resolved without action

| Note | Resolution |
|------|------------|
| Page notes overlay | Shipped 2026-08-07 |
| Offline SW resume | Shipped 2026-08-16; figures same-origin 2026-08-17 (A7) |
| Standalone claims hub card | Shipped 2026-07-25 |
| Concept-card KaTeX | Shipped 2026-07-19 |
| GitHub link indicators (↗) | Shipped 2026-07-25 |
| Six claims / bullet order | Krym Phase 1–2 |
| ch01 “breaks for superintelligence” | GI clause → C5b |
| dynamical-guarantee GI clause | → C5b |
| ch01 figure caching | → A7 |

---

## Execution phases (all complete)

| Phase | Scope | Commit / log |
|-------|--------|--------------|
| 0 | Tracker, attic export, `metadata/TODO.md` deferred bullets | `e91799b2` · phase0-1 log |
| 1 | Book/homepage IA, GitHub source links, tex-convert B2/B3 | `e91799b2` · phase0-1 log |
| 2 | Frontmatter C1–C2, C4–C5 | `e91799b2` · phase2 log |
| 3 | ch09 D1–D6 | `e91799b2` · phase3 log |
| 4 | ch10 E1–E3 cruxes | `ceff7e97` · phase4 log |
| 5 | B1/B4/B5, A12 sync/math | `ceff7e97` · phase5 log |
| 6 | A7–A11 mobile UX + local illustrations | `ceff7e97` · phase6 log |

**Deferred items** (not part of this plan): `metadata/TODO.md` § Site bullets A3, A4, A6, A14, E3d, E3e; outreach Substack (D7); CIRIS walkthrough (C5c); optional intro fluff pass (C2b).
