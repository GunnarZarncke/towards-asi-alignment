# 2026-11-15 — Dietz DCA and SPT on lens cards

kind: new-work
uptake: local

## Trigger
Add Florian Dietz’s Deliberative Credit Assignment and Split Personality Training as one-sentence examples on relevant lens cards, with bib refs and LW links. End-of-session commit.

Prompts: (no prompt id captured)

## Done
- content: **`lenses-data.mjs`** — example sentences on **control protocol** (SPT) and **additive route value** (DCA); external links.
- content: **`references/external-alignment.bib`** — `dietz2025dca`, `dietz2026spt`.
- content: **`bibliography-summaries.tex`** — matching `\bibsummary` lines.
- content: Synced lens cards; fixed `FieldLensGraph.astro` import path for `lenses-data.mjs`.
- bookkeeping: `sync-lenses`, `sync-lens-graph`; bibliography summary check passed (582 keys).

## Decisions
- Map SPT to control protocol (monitor evidence); DCA to additive route value (step credit), not separate cards.

## Open / next
- (none)

## Key paths
- `site/scripts/lib/lenses-data.mjs`
- `site/src/content/cards/lenses/control-protocol.md`
- `site/src/content/cards/lenses/additive-route-value.md`

## Commits
- (this session)