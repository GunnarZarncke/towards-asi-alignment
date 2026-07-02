# 2026-07-02 — Site card schema + MB1-MB10 bridge cards + Part I-II concept cards

## Trigger

User asked (in Plan mode) for a detailed plan breaking the book, `formal/`, `src/demos/`, and `experiments/` down into Astro site cards and "attached elements," treating formulas as attached elements rather than inline. After the plan was approved, the user said "build" — proceed with implementation.

## Done

- Extended the `card` content schema ([site/src/content.config.ts](../../site/src/content.config.ts)) with `bookSections`, `formulas`, `leanNodes`, `evidenceNotes`, `demos` — all optional arrays attached to a card, not new page types.
- Added [site/src/components/Formula.astro](../../site/src/components/Formula.astro), server-rendering LaTeX via `katex.renderToString` (new `katex` dependency); imported `katex/dist/katex.min.css` in `SiteLayout.astro`.
- Updated [site/src/pages/cards/[slug].astro](../../site/src/pages/cards/[slug].astro) to render `formulas` inline and `bookSections`/`leanNodes`/`evidenceNotes`/`demos` in the side panel.
- Split the single `bridge-assumptions` card into 10 bridge cards (`mb1-boundary-estimator-soundness` … `mb10-successor-forgeability`), each carrying the real Lean axiom name/module, the field crux from `appendices/appB-bridge-crosswalk.tex`, and matching evidence from `experiments/toy-simulation/results/NEGATIVE_RESULTS.md` (T-1..T-9) and `experiments/embedded-simulation/README.md`'s MB-coverage table. `bridge-assumptions.md` is now an index card linking to all ten.
- Authored 19 new concept/objection/artifact cards covering Part I (ch01-05) and Part II (ch06-10), grounded by reading the actual chapter LaTeX (not just section headers): `the-boundary-error`, `alignment-as-measurement`, `artificial-civilization`, `civilizational-correction-problem`, `dynamical-guarantee`, `static-target-trap`, `value-change-vs-corruption`, `scope-and-correction-capacity`, `turchin-coverage-audit`, `agent-without-anthropomorphism`, `agent-detection-to-alignment-target`, `boundary-residual`, `adversarial-boundary-discovery`, `conserved-properties-growth-split-merge`, `minimal-certification-schema`, `composite-agency` (with the `ch09-uad-coalition-board` demo attached), `detecting-composite-agents`, `strategic-opacity`, `adversarial-agency-tests`.
- Retrofitted existing seed cards: `grounding-viability` gained the ch03 conservative-abstraction/abstraction-gap-exploitation/reach-domain-grounding formulas and a `mb9-grounding-certificate` cross-link; `boundary-discovery` gained cross-links to the new chapter-level cards and `mb1`.
- Verified with `npm run build` after each batch (49 pages, 40 cards, no errors) and `ReadLints` (clean). Checked for dangling `related` slugs with a small Python pass and fixed one (removed a forward reference to a not-yet-written `unconscious-value-drift` card).

## Decisions

- Attached elements (formulas, Lean nodes, evidence, demos) are frontmatter arrays on existing cards, not a new content collection or new pages — keeps the "companion site, not a new knowledge platform" constraint.
- Only equations that define a named, reused quantity get promoted to a `formulas` entry; not every `\label{eq:...}` in a chapter.
- MB6 (6a/6b) and MB7 (7a-7d) are each represented as one card covering their sub-bridges together, rather than 6 separate cards, since the book and Lean module map already discuss them as linked groups.
- Where an experiment scenario exists in the MB-coverage table but has no dedicated negative-result writeup yet (MB6, MB7, MB10), the card says so explicitly (`finding: "open"`) rather than fabricating a result.
- New `evidence` array on cards was named `evidenceNotes` in the schema to avoid colliding with the pre-existing `evidence` string field (the card's "what would count as evidence?" callout).

## Open / next

- Full backlog (chapters 11-48, remaining appendix cards) is mapped in the plan file `/Users/GunnarZarncke/.cursor/plans/book_content_to_cards_breakdown_864a604f.plan.md` — not yet copied into a conversation-summary snapshot the way the Phase-0 plan was; worth doing if this plan is fully executed later.
- Remaining phases per that plan: Part III-VII concept/objection/artifact cards (ch11-32), then Part VIII-X (ch33-48) plus the "Open Issues Ledger" objection card and `appE` glossary cards.
- `value-change-vs-corruption` has a forward reference removed (to a future `unconscious-value-drift` card, ch46) — re-add when that chapter's cards are authored.
- No experiment yet red-teams MB10 (successor-audit forgeability) specifically; flagged as an open gap on the `mb10-successor-forgeability` card rather than invented.

## Key paths

- `site/src/content.config.ts` — schema
- `site/src/components/Formula.astro`, `site/src/pages/cards/[slug].astro` — rendering
- `site/src/content/cards/mb1-*.md` … `mb10-*.md` — bridge cards
- `formal/README.md`, `formal/AlignmentProofSpine/Core.lean`, `formal/AlignmentProofSpine/Forgeability.lean`, `appendices/appB-bridge-crosswalk.tex` — bridge source material
- `experiments/toy-simulation/results/NEGATIVE_RESULTS.md`, `experiments/embedded-simulation/README.md` — evidence source material

## Commits

- (none — not asked to commit)
