# 2026-10-20 — PostHog on chapter demos

kind: new-work  
uptake: status

## Trigger

Extend manual PostHog setup to all chapter demos (not only Ch. 1); fix CI markdown link failure from an INDEX entry pointing at an untracked session log; end-of-session commit.

Prompts: (paraphrase-only — no prompt id in transcript)

## Done

- **content** — Shared `demos/posthog.js`, `demo-boot.mjs`, `demo_posthog.py`; `serve.py` loads root `.env`, serves SDK/config routes, sets PYTHONPATH for backends.
- **content** — Browser boot + `trackDemo()` on static demos (appB, ch01, ch07, ch16, ch17, ch35) and demos landing; Ch. 9 server events via `demo_posthog.py`.
- **content** — `demos/package.json` + Vitest stub (`posthog.stub.js`, `vitest.config.mjs`); README documents env and privacy posture.
- **housekeeping** — Prior commit `e4e374586` added missing `2026-10-19-already-clean-field-news.md` so CI markdown links pass on clean checkout.

## Decisions

- One PostHog project remains sufficient; distinguish surfaces with `demo_slug`, `app: chapter_demo`, and event names (site uses build-time `PUBLIC_*` vars separately).

## Open / next

- Push commits ahead of `origin/main`; confirm GitHub Actions green after deploy.
- Optional: add explicit `app` / surface property on companion-site PostHog init for dashboard parity.

## Key paths

- `demos/serve.py`, `demos/posthog.js`, `demos/demo_posthog.py`, `demos/README.md`

## Verification

- `cd demos && npm run build && npm test` → 47 tests passed (2026-10-20).

## Commits

- (this session) Add PostHog analytics across chapter demos.
