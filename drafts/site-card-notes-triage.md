# Site card notes triage

Structured tracker migrated from `drafts/attic/tsa-notes-export-2026-08-15.txt` (Aug 15, 2026). Raw export archived; use this file for status.

**Legend:** `resolved` · `open` · `partial` · `deferred` · `phase N` (execution phase from plan)

---

## Group A — Site UX and navigation

| ID | Status | Phase | Note | Target |
|----|--------|-------|------|--------|
| A1 | **done** | 1 | Book nav before PDF on `/book/` hero | `site/src/pages/book/index.astro` |
| A2 | **done** | 1 | Remove Status / Formal density columns | `site/src/pages/book/index.astro` |
| A3 | open | deferred | “Also on the site” follows book material order | `metadata/TODO.md` § Site |
| A4 | open | deferred | Explicit part hub cards | `metadata/TODO.md` § Site |
| A5 | **done** | 1 | Standalone claims below Guided Tour on homepage | `site/src/pages/index.astro` |
| A6 | deferred | — | Review standalone claims publishability | `metadata/TODO.md` § Site |
| A7 | open | 6 | Chapter figures not cached (cross-origin GitHub raw URLs) | `tex-convert.mjs`, `sw.js` |
| A8 | open | 6 | Standard icons for page-notes panel | `PageNotes.astro` |
| A9 | partial | 6 | Mobile keyboard overlaps panel buttons | `PageNotes.astro` |
| A10 | open | 6 | Highlight marks need tap-to-open on mobile | `PageNotes.astro` |
| A11 | open | 6 | Expand panel weak on mobile | `PageNotes.astro` |
| A12 | open | 5 | Formulas overflow on narrow mobile | `global.css`, sync pipeline |
| A13 | **done** | 1 | Chapter `.tex` source → GitHub blob link | `site/src/pages/cards/[...slug].astro` |
| A14 | deferred | — | Submit notes to site (beyond localStorage) | `metadata/TODO.md` § Site |

---

## Group B / E4 — LaTeX→site sync bugs

| ID | Status | Phase | Note | Target |
|----|--------|-------|------|--------|
| B1 | open | 5 | Raw `\symboldef` / `\symbolref` in synced chapters | `tex-convert.mjs` |
| B2 | **done** | 1 | Titlepage `{ Towards Superintelligence Alignment}` literal braces | `tex-convert.mjs` (brace groups) |
| B3 | **done** | 1 | `\hyperref` → broken “as a for human-correctable” in part roadmap | `tex-convert.mjs` (`hyperref`, `gloss`) |
| B4 | open | 5 | ch10 “We distinguish three layers” — block below doesn’t render | `tex-convert.mjs` |
| B5 | open | 5 | ch10 formula label / symboldef leak | B1 + KaTeX |

---

## Group C — Frontmatter editorial

| ID | Status | Phase | Note | Target |
|----|--------|-------|------|--------|
| C1a | **done** | 2 | Remove “Many chapters are still drafts” (preface) | `frontmatter/preface.tex` |
| C1b | **done** | 2 | Remove “Many chapters are still first drafts” | `frontmatter/current-status.tex` |
| C1c | **done** | 2 | Update current-status maturity paragraph | `frontmatter/current-status.tex` |
| C2a | **done** | 2 | Remove “serious” from exec-overview safety case | `frontmatter/executive-overview.tex` |
| C2b | open | 2 | Remove fluff / magic-sentence passage | `introduction.tex` (not frontmatter Phase 2 scope) |
| C2c | **done** | 2 | Remove External Doom Arguments section + preface pointer | `executive-overview.tex`, `preface.tex` |
| C2d | **done** | 2 | Trim redundancy; general terms in “What This Book Tries to Establish” | `executive-overview.tex` |
| C2e | **done** | 2 | Related content → Part I (ch01) on frontmatter card | `sync-chapter-cards.mjs` |
| C3 | **resolved** | — | Six connected claims / TL;DR order (Krym Phase 1–2) | — |
| C4 | **done** | 2 | Verify-only terminology grep (non-intro frontmatter vs App E) | preface plain-first lead |
| C5a | **done** | 2 | Glossary link (manuscript + site) | preface, exec-overview |
| C5b | **done** | 2 | GI comparison: static alignment breaks before SI | `dynamical-guarantee.md`, ch01 |
| C5c | deferred | — | CIRIS end-to-end walkthrough | `metadata/TODO.md` Real worked example |

Frontmatter card terminology suggestions (value geometry, correction channels, etc.) — fold into C4 verify pass.

---

## Group D — Chapter 9 (`ch09-composite-agent.tex`)

Re-check anchors before editing (Krym / DAG pass may have partially addressed).

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

Additional ch09 notes: remove fluff (“philosophical subtlety”, “without relying on metaphor”); mobile UX → A9–A10.

---

## Group E — Chapter 10 (`ch10-strategic-opacity.tex`)

Re-check anchors before editing.

### E1 + E2 — Prose and ordering (Phase 4)

| ID | Status | Note |
|----|--------|------|
| E1a | open | Remove “usually” (bacterium) |
| E1b | open | Remove “serious” (alignment) |
| E1c | open | Remove “Examples help.” |
| E1d | open | Simplify opacity example sentences |
| E1e | open | Predict-O-Matic list wording |
| E1f | open | Inner-alignment-shaped failure readability |
| E1g | open | Add “therefore” after action-channel invariant |
| E1h | open | “Correct decomposition” vs boundary discovery overlap |
| E2a | open | Hubinger decomposition alignment |
| E2b | open | “filter-family coverage” first-use gloss |
| E2c | open | GLI / bundle-map preview length vs ch40 ordering |

### E3 — Cruxes (Phase 4)

| ID | Status | Note |
|----|--------|------|
| E3a | open | Oversight vs dangerous opacity — resolve or mark open |
| E3b | open | Correction channel overloaded — tie to correction capacity |
| E3c | open | Soften “We infer” latent continuity |

### E3 — Deferred TODOs

| ID | Status | Note |
|----|--------|------|
| E3d | deferred | Alignment-faking / sleeper agents experiment line |
| E3e | deferred | Chapter-end exercises + online quiz |

### E4 — Sync (Phase 5)

See Group B (formula render, three layers block).

---

## Resolved without action

| Note | Resolution |
|------|------------|
| Page notes overlay | Shipped 2026-08-07 |
| Offline SW resume | Shipped 2026-08-16 (figures still cross-origin) |
| Standalone claims hub card | Shipped 2026-07-25 |
| Concept-card KaTeX | Shipped 2026-07-19 |
| GitHub link indicators (↗) | Shipped 2026-07-25 |
| Six claims / bullet order | Krym Phase 1–2 |
| ch01 “breaks for superintelligence” | Anchor exists; GI clause → C5b |

---

## Homepage / concept cards (not frontmatter)

| Anchor | Status | Phase | Note |
|--------|--------|-------|------|
| dynamical-guarantee | open | 2 | “Already breaks for general intelligence” → C5b |
| ch01 researcher tends | open | 6 | Figure caching → A7 |

---

## Execution phases (remaining)

| Phase | Scope |
|-------|--------|
| **0** | **Done** — this tracker, attic export, `metadata/TODO.md` bullets |
| **1** | **Done** — A1, A2, A5, A13, B2, B3 |
| **2** | **Done** — frontmatter C1–C2, C4–C5 |
| **3** | **Done** — ch09 D1–D6 |
| **4** | ch10 E1–E2, E3 cruxes (verify anchors) |
| **5** | B1, B4, B5, A12 |
| **6** | A7–A11 mobile + assets |
