# 2026-10-15 — Last Safety impressum link

kind: new-work
uptake: local

## Trigger
Add a small bottom-right Impressum/About link on the game room UI with minimal German imprint (TSA companion site), UI credits, and AI-generated content notice. End-of-session commit.

Prompts: (paraphrase-only — no telemetry id in thread)

## Done
- content: `public/index.html` — fixed “Impressum / About” control opens native `<dialog>` with aintelope UG provider block (§ 5 DDG, § 18 MStV), bilingual KI/fiction disclaimer, three.js / Inter / optional OpenAI credits.
- content: `public/style.css` — bottom-right link and dialog styling (z-index above dock).

## Decisions
- Room view only (`index.html`); text console and phone iframe unchanged.
- Minimal imprint (provider + register + contact), not full TSA Haftung/Urheberrecht blocks.
- Cited DDG instead of TMG for provider identification (TMG still on site impressum).

## Open / next
- Optionally mirror link on `text.html` if that surface is public-hosted.
- Align site `impressum.astro` TMG → DDG wording when editing legal pages.

## Key paths
- `game/last-safety-autocomplete-prototype/public/index.html`
- `site/src/pages/impressum.astro` (full TSA imprint reference)

## Commits
- `6e0fc9570` Last Safety: Impressum / About link on room UI.
