# 2026-10-12 — Player documents content home

kind: new-work
uptake: local

## Trigger
Move security architecture draft to a proper place; adapt plans for document sources and model representation.
Prompts: (this Cursor turn)

## Done
- content: Moved `drafts/security-concept.md` → `content/documents/sec-arch-04.md`; added `content/documents/README.md`, `spec/documents.md`, `lib/documents.mjs`, `tests/documents.test.mjs`.
- content: Updated PLAN, spec README, engine, contract, incident, `drafts/plans/last-safety-review.md`.

## Decisions
- Sources under `content/documents/`; catalog + `renderDocument(slug, pack)` in `lib/documents.mjs`; `PACK_ORDER` shared with incident pack ladder.
- Served file rows may carry optional `documentSlug`; `leanKnowledge: false` — reads do not add engine/Lean knowledge edges.
- Live `file.read` / analyze wiring deferred; render tested.

## Open / next
- Engine: grant SEC-ARCH-04 on access; render at read time; analyze using `analyzeHints`.
- Session `scenario` pack drives render.

## Key paths
- `game/last-safety-autocomplete-prototype/content/documents/sec-arch-04.md`
- `game/last-safety-autocomplete-prototype/spec/documents.md`
- `game/last-safety-autocomplete-prototype/lib/documents.mjs`

## Commits
- none
