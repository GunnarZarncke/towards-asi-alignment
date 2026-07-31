# 2026-07-08 — Coined-term demotion, glossary expansion, site sweep, v1.1.0 release notes

## Trigger
Follow-up to the "subsumption → crosswalk" session. User asked to demote/reframe a batch of coined terms (selection handle, fitness, deployment/control mass, correction parasite, preservation envelope, selection environment), pair alignment-basin first-uses with plain paraphrases, add Grounding Viability and expand the glossary; then sweep the Astro site for parity; then write release notes and commit.

## Done
- **Glossary (`appendices/appE-glossary.tex`) rewritten and ~2.5× expanded.** Paraphrase-first entries with a *nearest field term* delta and a concrete (often non-AI) example. Added **Grounding Viability**, **Transport** (semantic/bundle/bearer/correction/successor), **Conserved Properties**; demoted selection handle / deployment leverage(mass) / deployment growth rate(fitness) / preservation conditions(envelope); removed the "selection environment" headword; added the correction-audit-evasion entry (parasite = metaphor).
- **ch34 definitions demoted plain-first** (symbols/equations unchanged): "point of control over deployment" (selection handle), "deployment leverage" / `μ_E`, "deployment growth rate" / `Fit_E`, "preservation conditions" `Π⃗`; replaced "selection environment" → "deployment environment" (4×) and "preservation envelope" → "preservation conditions" (3×) in-chapter.
- **notation** source `metadata/notation.md` + generated `metadata/notation-index.tex` relabeled (`μ_E`, `Fit_E`, `Π⃗`, section heading, `C_X`/`A_Y` criterion lines).
- **"correction parasite" → "correction-audit evasion"** as the operational term: ch36 thesis + operational-definition intro (metaphor kept explicit), `book.yml` part08 summary, generated `part-roadmap.tex`, `part08` opener. Chapter title/file/label kept.
- **alignment-basin first-use paraphrases** added in ch03, ch35, ch37.
- **Astro site sweep:** `site/src/content/cards/attractor-control.md` and `mb6-selection-and-basin-stability.md` glossed to lead plain. Left the real publication title in `author-profile.json` ("…Parasite Persistence") and the ELK "parasitic on capability" sense in `certification-under-manipulation.md` untouched. Site already had a `grounding-viability.md` card and used "deployment environment".
- **`RELEASE_NOTES.md`:** promoted the stale "Unreleased" block into a dated **v1.1.0 — 2026-07-08** entry (legibility pass + crosswalk reframe + institutional-histories appendix + companion site + four empirical lines + housekeeping).
- `make check` green (structure, citations, bibliography summaries); no lint errors on edited files.

## Decisions
- **"Demote" = plain-first at the definitional home + glossary + notation, not a global find/replace.** Downstream established-term uses left intact; symbols, equations, `\label`s, and Lean predicate names never renamed.
- **Parasite handled term-only (user choice).** Renamed the operational term everywhere it acted as canonical vocabulary but kept ch36's host/parasite metaphor prose and the chapter title/filename/labels — a blanket swap would break grammar and lose the "exploits host" meaning that "evasion" doesn't carry.
- **v1.1.0 (MINOR).** New appendix + framework-object clarifications + companion site since v1.0.0; no renumbering, so cross-ref targets stay stable. Tag left for the user to create (git safety).

## Open / next
- **Did NOT tag** v1.1.0 — run `git tag -a v1.1.0` on the release commit when ready.
- Optional deeper demotion: many downstream appendix occurrences of deployment-mass / selection-environment (appC, appG, appD, appF) still use the coined shorthand; acceptable but could be glossed if a fuller pass is wanted.
- Site full build not run this session (only string edits in existing frontmatter/body; `make check` covers the manuscript).

## Key paths
- `appendices/appE-glossary.tex`, `chapters/ch34-selection-environment.tex`, `chapters/ch36-parasites-correction-system.tex`, `metadata/notation.md`, `RELEASE_NOTES.md`.

## Commits
- (this session's commit hash to be recorded after commit)

## Not staged (left in working tree, not this task)
- Unrelated pre-existing changes: `chapters/ch07-finding-boundary.tex`, `chapters/ch08-grow-split-merge.tex`, `demos/package-lock.json`, `metadata/global-nocite.tex`, several `drafts/conversation-summaries/*.md`, and `experiments/**` (lab-sim/embedded). These belong to other work and were deliberately not committed.
