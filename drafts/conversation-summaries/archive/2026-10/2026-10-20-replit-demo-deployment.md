# 2026-10-20 — Replit unified demo deployment wired into site

kind: new-work  
uptake: status

## Trigger

User: demos deployed on Replit with server components; verify paths and wire into repo (example: `https://towards-asi-alignment.replit.app/ch01-scaffold-misuse/`).

Prompts: (paraphrase-only)

## Done

- **content** — `demos/deployment.json` (`liveBaseUrl`); `sync-demos.mjs` emits per-demo `liveUrl` and `liveBaseUrl` in `demos.json`.
- **content** — `site/src/lib/demo-urls.ts` + reading paths, `/demos/`, essays, card sidebars use Replit for backend/hybrid demos (Ch. 1 live LLM, Ch. 9 board).
- **content** — Ch. 1 `resolveBackendBase()` same-origin for `/ch01-scaffold-misuse/` on Replit; scaffold-misuse concept/card external URL updated.
- **housekeeping** — `demos/README.md` live deployment section; removed stale per-demo Replit URL from `ch01-scaffold-misuse/backend.json`.

## Verification

- Replit: `ch01-scaffold-misuse/api/health` → `available: true`; `ch09-uad-coalition-board/` loads board UI; `ch07` JSON assets under `data/` reachable.
- `cd demos && npm run build && npm test` → 47 passed.
- `cd site && node scripts/sync-demos.mjs && node scripts/sync-concepts.mjs` → OK.

## Open / next

- Run full `cd site && npm run build` before merge if not already green on CI.
