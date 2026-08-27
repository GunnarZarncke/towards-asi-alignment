# 2026-08-26 — Bot-orientation and entry-doc housekeeping

## Request

User asked to audit `llms.txt`, then apply the full housekeeping batch: orientation sync, bridge-range fixes, field counts, anti-pattern reconciliation, README doc links, `notation.md` appendix pointer, `meta.yml` counts.

## Shipped

- **`llms.txt`:** v1.5.0; field hub v2 counts (30/24/29 framing); `/field/coverage/`, negative-results, about; repo pointers (App B, `docs/EXPERIMENTS.md`, `papers/`); six-claim + MB8-retired thesis line; expanded formal-spine and empirical sections; anti-patterns aligned with review guide (+ context/ bullet kept).
- **`REVIEWING_FOR_AGENTS.md`:** typo fix; MB1–MB11 / MB8 retired; empirical pointers; unified anti-patterns.
- **`AGENTS.md`**, **`CONTRIBUTING.md`:** bridge ranges updated.
- **`README.md`:** doc table rows for `REVIEWING_FOR_AGENTS.md` and `llms.txt`.
- **`metadata/notation.md`:** formal predicates → `appG-lean-proof-spine.tex` (was wrongly Appendix I).
- **`reference/field-agendas/data/meta.yml`:** 24 matrix / 30 agenda records; regen via `npm run sync:field-agendas`.
- **`site/public/`:** `sync:bot-orientation` refreshed `llms.txt`, `reviewing-for-agents.md`, `llms-full.txt`.

## Not in scope

- App B MB11 row prose (still on TODO board).
- Full `formal/README.md` “nine MB1–MB9” packaging paragraph (accurate for `BridgeAssumptions`; left as-is).

## Verify

- `cd site && npm run sync:bot-orientation` — ok
- `cd site && npm run sync:field-agendas` — ok
