# 2026-10-19 — Last Safety play telemetry

kind: new-work
uptake: local

## Trigger
Add tracking to the game using the companion site mechanism; record fuel, room id, NPC id, knowledge id, and act.

Prompts: (paraphrase-only — no telemetry id in thread)

## Done
- content: `lib/telemetry.mjs` — event row enrichment, `playTelemetry`, optional JSONL via `TELEMETRY_LOG`.
- content: `public/telemetry.mjs` — localStorage play history, `sendBeacon` to `/api/telemetry`, Cloudflare Web Analytics on non-localhost hosts.
- content: Engine `log()` / exported `logAction`; mutating API responses include `telemetry`; CSP + impressum disclosure; `spec/contract.md` updated.
- bookkeeping: `tests/telemetry.test.mjs` (5 tests).

## Decisions
- `fuel` in API telemetry is the spent index (`fuelSpent`), matching the save event log timeline; `room`/`act` come from session state; `npc`/`knowledge` are best-effort from the last event.
- Server JSONL is opt-in (`TELEMETRY_LOG`); client mirror uses `lsr-play-telemetry-v1` like site visit history.

## Open / next
- Mirror telemetry on `text.html` / phone iframe tool calls if headless play needs the same beacons.
- Add `telemetry/` to game `.gitignore` if operators keep JSONL on disk in deploy.

## Key paths
- `game/last-safety-autocomplete-prototype/lib/telemetry.mjs`
- `game/last-safety-autocomplete-prototype/public/telemetry.mjs`
- `game/last-safety-autocomplete-prototype/server.mjs`

## Verification
- `cd game/last-safety-autocomplete-prototype && node --test tests/telemetry.test.mjs` → `ℹ pass 5` / `ℹ fail 0`.

## Commits
- `ce16dd6f5` Last Safety: play telemetry aligned with companion site analytics.
