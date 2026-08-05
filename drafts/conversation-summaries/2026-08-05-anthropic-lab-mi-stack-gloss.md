# 2026-08-05 — Anthropic lab MI stack gloss

## Trigger
User flagged the Anthropic / Goodfire field agenda card: title says "MI stack" but the page did not explain or link the abbreviation.

## Done
- `reference/field-agendas/data/agendas/anthropic-lab.yml` — intro defines **MI stack** with em-dash link to [mechanistic interpretability](https://www.anthropic.com/research) and names Goodfire, Transluce, Neuronpedia; `type` field spelled out; "DeepMind MI lineage" in contributes now links to the same research index.
- Regenerated `site/src/content/cards/field-agendas/anthropic-lab.md`, `site/src/data/field-agendas.json`, `reference/field-agendas/field-agenda-index.md` via `sync:field-agendas`.

## Decisions
- Keep compact **MI stack** in the agenda title (field jargon); gloss on first use in the intro rather than spelling out the full phrase in the H1.

## Open / next
- Deploy companion site for live card update at `/cards/field-agendas/anthropic-lab/`.

## Key paths
- `reference/field-agendas/data/agendas/anthropic-lab.yml`
- `site/src/content/cards/field-agendas/anthropic-lab.md`

## Commits
- (this session)
