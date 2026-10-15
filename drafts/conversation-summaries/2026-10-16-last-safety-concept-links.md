# 2026-10-16 — Last Safety O-41 concept links

kind: new-work
uptake: local

## Trigger
Per-fact optional TSA companion card links (O-41): phone setting, room footer line, persistence, more authored links where they fit; fix layout so More does not cover chat input.

## Done
- content: Optional `conceptSlug` / `conceptSummary` on facts; `scripts/compile-concepts.mjs` emits `fact:*` and extra `doc:*` triggers; `lib/world/concepts.generated.mjs` regenerated (29 keys).
- content: Engine `triggerFactConcepts`, learn + file.read note signatures; `roomConceptLastTrigger` restore when toggling setting on; `conceptLinksEnabled` on `terminalState`.
- content: Phone syncs setting from engine, awaits `/api/settings`, autosave on change; `More:` in file viewer when links on.
- content: Room UI — More line in transcript dock below composer (minimal one-line style); tests `tests/concepts.test.mjs`, O-41 cases in `tests/engine.test.mjs`.
- content: Spec/plan updates (`spec/engine.md`, `spec/contract.md`, `PLAN.md`).
- content: Additional fact/doc links (composite agency, certification, value bundle, think marks via notes) without blanket tagging.
- content: Door clearance LED strips (green/red) on 3D exit hotspots from session clearance (`public/render/`).
- bookkeeping: Session log, HANDOFF, INDEX.

## Decisions
- More link stays on room view (not in phone only); phone viewer duplicates when a read triggers a link.
- Think-mark concepts fire only when mark ids are on a note signature and the note is opened (not from bubble alone).

## Open / next
- Optional: reserve one empty line under composer when setting is on but no link yet (user asked for minimal — skipped).
- Run `node scripts/compile-concepts.mjs` after any `conceptSlug` or TRIGGERS edit.

## Key paths
- `game/last-safety-autocomplete-prototype/lib/world/facts.mjs`
- `game/last-safety-autocomplete-prototype/scripts/compile-concepts.mjs`
- `game/last-safety-autocomplete-prototype/public/app.js`, `public/terminal/phone.js`

## Verification
- `node scripts/compile-concepts.mjs` → 29 triggers
- `node --test tests/concepts.test.mjs tests/engine.test.mjs --test-name-pattern O-41` → pass

## Commits
- `5d94fd922` Last Safety: O-41 TSA concept links and door clearance signs.
