# 2026-10-15 — Last Safety /text.html browser fix

kind: correction
uptake: local

## Trigger
`/text.html` showed the input line but no log output (not even initial room text or `help`). User confirmed fix after follow-up.

## Done
- content: Moved browser-safe `utteranceSlice` / command verbs to `public/text-tab-slice.mjs`; stopped `text-input.mjs` importing non-public `lib/text/tab-complete.mjs`.
- content: Inlined kb debug helpers in `public/text-debug.mjs`; `lib/text/kb-debug.mjs` re-exports from public.
- content: `text.html` dynamic imports, API error surfacing, bootstrap error messages; `dev-ui` returns 503 for `/api/text` and `/api/tab-complete`.
- housekeeping: Added `tests/text-html-imports.test.mjs` to guard the public import graph.

## Decisions
- Keep engine tab-complete on the server; browser only needs slice detection plus `/api/tab-complete` for command lines — no widening `PUBLIC_LIB` to full `tab-complete.mjs` (pulls game/LLM).

## Open / next
- None for this bug.

## Key paths
- `game/the-last-safety-review/public/text.html`
- `game/the-last-safety-review/public/text-tab-slice.mjs`
- `game/the-last-safety-review/tests/text-html-imports.test.mjs`

## Verification
- `node --test tests/text-html-imports.test.mjs tests/text-console.test.mjs` — pass 8/8.

## Commits
- `39cd00262` Fix Last Safety browser text console (/text.html).
