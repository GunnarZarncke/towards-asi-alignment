# 2026-10-20 — PostHog manual finish (game, site, Ch.1 demo)

kind: new-work  
uptake: local

## Trigger

User asked to finish PostHog without the PostHog installer after a partial wizard run.

## Done

- **content** — Companion site: `PostHogAnalytics.astro`, layout hook, impressum note, CI env, README; privacy-first init (no autocapture/session replay).
- **content** — Game: CSP connect-src assets host, env alias `POSTHOG_API_KEY`, soft-disable when unconfigured, shared privacy init.
- **content** — Ch.1 demo: `config.py` aliases, `POSTHOG_PRIVACY_MODE` default true, metadata-only `$ai_generation`, no debug crash when PostHog unset.
- **housekeeping** — Root/site/game `.env.example`; removed `.claude/skills/integration-fastapi` wizard skill tree.

## Verification

- `cd site && CI=true PUBLIC_POSTHOG_PROJECT_TOKEN=phc_test npx astro build` → `[build] Complete!`
- `.venv/bin/python -m py_compile demos/ch01-scaffold-misuse/app.py demos/ch01-scaffold-misuse/config.py` → exit 0

## Open

- Set GitHub secrets `PUBLIC_POSTHOG_PROJECT_TOKEN` (and optional `PUBLIC_POSTHOG_HOST`) for live site analytics.
- Exercise Ch.1 backend and game locally once to confirm events in PostHog UI.
