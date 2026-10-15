# 2026-10-15 — Last Safety public-hosting hardening

kind: new-work
uptake: local

## Trigger
Prompts: paraphrase only (no prompt id). User asked for a safety review of the game for public hosting (audience: AI safety researchers, puzzle solvers; low load; expected jailbreak attempts), then picked fixes: 1 full; 2 = template history + untrusted label; README jailbreak note (not UI); 3 = per-session rate limit; 4 = session TTL + per-session limits; 5 + 6 full.

## Done
- content: `phrasingInput` sends no fact text for `withhold`/`deflect` moves (before: the withheld fact went to the NPC-voice model with only a prompt instruction against saying it).
- content: `rephraseLine` keeps `template`; model prompts (`promptHistory` in `lib/llm.mjs`) use templates for NPC rows; `clientState.previous` strips `template`. Both system prompts label player text as untrusted.
- content: Per-session model budget in `responsesRequest` (`LLM_CALLS_PER_MINUTE` 30, `LLM_CALLS_PER_SESSION` 600); over budget → toy parser / template. Reset and import keep `usage`.
- content: Idle session TTL (`SESSION_TTL_HOURS`, default 6) with a 10-minute sweep; `CONFIG.LIMITS` (photos 12, notes 60, note chars 20k, bytes written 16M, signatures per write 20, events 5000); refused `file.write` no longer logged; import rejects over-long or malformed `events`.
- content: Photos raster-only (jpeg/png/webp); `/api/handset-file` gets `CSP: default-src 'none'; sandbox`; site-wide CSP (inline scripts allowed by hash computed at startup), `nosniff`, `Referrer-Policy`.
- content: Catch-all errors return fixed messages (no paths or upstream text); details go to the server log.
- bookkeeping: README (jailbreak note, limits, env vars), `.env.example`, `spec/npcs.md` phrasing paragraph, `tests/hosting.test.mjs`.

## Decisions
- Jailbreaking is documented as allowed but not the game (README only, not UI).
- Not done (offered, not chosen): output moderation / novelty check, global or per-IP budget, max session count, smaller body limit, reverse proxy / `Secure` cookie. Per-session limits do not stop a script that drops its cookie; a hard OpenAI project budget is still the real cost cap.

## Open / next
- Before public deploy: dedicated OpenAI key with a monthly budget; deploy only the game directory (server also reads repo-root `.env`, which holds other keys); TLS proxy.
- CSP not checked with WebGL on (headless Chrome had no WebGL).

## Key paths
- `game/last-safety-autocomplete-prototype/lib/game.mjs`, `lib/llm.mjs`, `server.mjs`, `lib/world/config.mjs`, `lib/world/terminal-host.mjs`, `lib/photo-data.mjs`
- `game/last-safety-autocomplete-prototype/tests/hosting.test.mjs`

## Verification
- `npm test` — `ℹ tests 107` / `ℹ pass 107` / `ℹ fail 0`.
- Demo server on port 3917: `curl /nope.html` → `{"error":"Not found."}`; bad JSON POST → `{"error":"Bad request."}`; CSP header present. Headless Chrome loaded `/`, `/text.html`, `/terminal/index.html` with no CSP violations in the console log.

## Commits
- None (not asked).
