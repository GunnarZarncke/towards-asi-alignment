# 2026-10-20 — Last Safety folder rename and social replies

kind: correction
uptake: local

## Trigger
Rename game directory to match title; fix NPCs (especially Ian) repeating sentences in one response to simple Hi; end of session and commit.

Prompts: paraphrase only (no prompt id in transcript)

## Done
- content: **`game/the-last-safety-review/`** — Renamed from `last-safety-autocomplete-prototype`; npm package `the-last-safety-review`; repo path references updated (`AGENTS.md`, plans, session logs).
- content: **Social / small talk** — One line per turn (opening → mid → work); no stacked glue+work+initiative; Ian Lab Access brief once via `confirmLabAccess` return lines (`lib/game.mjs`, `lib/world/npcs.mjs`, `spec/npcs.md`, `tests/glue.test.mjs`).

## Decisions
- Substantive parses keep opening glue + engine response; only `social` / `unintelligible` use the single-line path.

## Open / next
- None for this thread.

## Key paths
- `game/the-last-safety-review/lib/game.mjs`, `lib/world/npcs.mjs`
- `game/the-last-safety-review/tests/glue.test.mjs`

## Verification
- `cd game/the-last-safety-review && DEMO_MODE=1 npm test` — 156 pass, 0 fail.

## Commits
- `13fa67b1a` — Last Safety: rename game folder and unify social NPC replies.
