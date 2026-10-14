# 2026-10-15 — Last Safety room UI and mobile handset

kind: new-work
uptake: status

## Trigger
Room chat layout, completion latency investigation, Lab Access notification clarity, narrow-viewport phone dismiss and transcript collapse. User asked for end-of-session log and commit.

Prompts: (paraphrase-only — no prompt ids in transcript export)

## Done
- content: Room **transcript dock** — bottom-aligned column (not a HUD panel), grouped speaker tabs, stacked line boxes, narrow column (`--transcript-col`), full-height scroll.
- content: **Completions** — Hi opener, CLI `msg` tab-complete via API, phone Chat threads + grammar ranker; `scripts/bench-completions.mjs` documents debounce + LLM parse as latency budget.
- content: **Handset** — clearer activation notifications (human titles), New stack + app tile badges; embed **Close lab**, ×, swipe-down, Esc → room overlay.
- content: **Mobile room** — transcript history/suggestions/NPC chips hidden until composer focus; collapse on room/HUD taps; phone overlay z-index 50.
- housekeeping: Spec touches (`graphics-ui.md`, `grammar.md`, `terminal.md`, `text-console.md`, `contract.md`).
- bookkeeping: `npm test` in `game/last-safety-autocomplete-prototype` — 93 pass.

## Decisions
- Narrow layout uses `matchMedia('(max-width: 720px)')` aligned with existing CSS breakpoints.
- Phone unread UX: notifications stay engine-driven; UI makes unread point at Files/Calendar/Knowledge explicitly.

## Open / next
- Optional: lower parse debounce or interim `demoParse` on client while LLM pending (bench shows ~560 ms + 1–2 s live).
- Optional: note mobile transcript/phone dismiss in `spec/graphics-ui.md` / `spec/terminal.md` if normative.

## Key paths
- `game/last-safety-autocomplete-prototype/public/app.js`, `style.css`, `index.html`
- `game/last-safety-autocomplete-prototype/public/terminal/phone.js`, `phone.css`
- `game/last-safety-autocomplete-prototype/scripts/bench-completions.mjs`

## Commits
- `c0c0e9151` Last Safety: room transcript UX, mobile handset dismiss, and completion paths.
