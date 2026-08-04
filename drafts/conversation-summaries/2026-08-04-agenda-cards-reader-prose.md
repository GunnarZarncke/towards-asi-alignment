# 2026-08-04 — Agenda cards reader prose

## Trigger
User: review all field agenda cards on the site; many use technical fragment language. Keep semantic content; rewrite for readers with general AI-alignment knowledge; link terms and book concept cards; use glossary field nouns instead of MB*.

## Done
- Rewrote all agenda YAML under `reference/field-agendas/data/agendas/` to full-sentence prose with `/cards/...` links; no MB* or `⇏` in public prose fields.
- Added short `overview` on every card-generating agenda.
- Normalized `bookBridges` to clean keys (`MB1`, `MB4a`, …); fixed malformed CIRIS / Kosoy bridge lists.
- Updated `site/scripts/sync-field-agendas.mjs`: reader labels (“What they aim to do”, “Related field cruxes”, …); bridge nouns with links; strip markdown from summaries; omit manuscript hooks from public cards.
- Updated agenda card sidebar in `site/src/pages/cards/[...slug].astro` to show field nouns, not MB* keys.
- Regenerated cards + `field-agendas.json` + `field-agenda-index.md` (`npm run sync:field-agendas`; `--check` clean).
- **Term linking pass:** added `reference/field-agendas/data/term-links.yml` + `scripts/link-agenda-terms.py` (`--relink` / `--check`); applied across signatureVocabulary and other prose (bridge/concept cards + stable external URLs). Avg signature links rose from 0 → ~4; denser on research agendas.

## Decisions
- Keep MB* keys in YAML/frontmatter for matrix/sidebar lookup; display nouns only.
- Agent-facing `manuscriptHooks` stay in YAML/index but are not rendered on public cards.
- Training/field-building agendas with empty bridge lists still get overviews linking Field hub / concept cards.
- Term linking is dictionary-driven (not LLM); extend `term-links.yml` when new jargon appears. Prefer cards over external URLs when a card exists.

## Open / next
- Spot-check live Field hub / a few agenda pages after deploy.
- Optional: soften agent `field-agenda-index.md` inclusion prose the same way (still denser than cards).
- Optional: grow `term-links.yml` for remaining thin signatures (govai, conjecture) and wire `--check` into site CI.

## Key paths
- `reference/field-agendas/data/agendas/*.yml`
- `reference/field-agendas/data/term-links.yml`
- `reference/field-agendas/scripts/link-agenda-terms.py`
- `site/scripts/sync-field-agendas.mjs`
- `site/src/content/cards/field-agendas/`
- `site/src/pages/cards/[...slug].astro`

## Commits
- `87232b89` Rewrite field agenda cards for general alignment readers.

## End of session (2026-08-04)
- Term-link audit: `check-term-links.py`; fixed Vingean PDF URL, hard pause → MIRI 2024 strategy, precursor agents → PreDCA distilled post, TAI → Epoch.
- Relink pass on agenda YAML; cards regenerated.
