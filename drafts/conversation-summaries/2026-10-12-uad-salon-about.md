# 2026-10-12 — UAD salon on the about page

kind: new-work
uptake: local

## Trigger
Add the UAD talk to the publications list on the about page.
Prompts: paraphrase-only (no telemetry prompt id in this session)

## Done
- content: `site/src/data/author-profile.json` — “Finding Agency in Real-World Data” (2026 · talk · Foresight AI Salon, Berlin, 8 July). Main link: YouTube recording; sublinks: Google Slides deck, Luma event.
- bookkeeping: `drafts/slides/ai-salon-uad-demo-slides.md` — pointer to delivered deck.

## Decisions
- Main link is `https://www.youtube.com/watch?v=5ezlG3l6iNw`. Event stays a sublink.
- Slides: Google Slides deck linked from the about page (`slides` sublink). `drafts/slides/ai-salon-uad-demo-slides.md` remains internal speaker notes.
- The on-screen QR (from about 3:03 to the end) encodes `https://gunnarzarncke.github.io/towards-asi-alignment/`, which 301s to the companion site.

## Open / next
- none

## Key paths
- `site/src/data/author-profile.json`
- `site/src/pages/about/index.astro`

## Commits
- `5a61182b7` Add UAD Foresight salon talk to the about-page publications list.
- `70c885a76` Link UAD salon talk on about page to video, slides, and event.
