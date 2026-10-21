# 2026-10-21 — PostHog deploy fixes

kind: correction  
uptake: status

## Trigger

User: deployed sites not sending PostHog events; inspect live instances; then apply fixes and end-of-session commit.

Prompts: (paraphrase-only)

## Done

- **content** — Companion site: `PostHogAnalytics.astro` uses bundled module script (no `define:vars` + bare `import`); `app: companion_site`.
- **content** — Game: pageview/pageleave on; `app: last_safety_review`; text console metadata events (`text_console_loaded`, `text_command_sent`, `review_completed` with `surface: text`).
- **housekeeping** — `demos/README.md` Replit redeploy smoke checklist after PostHog/HTML pulls.

## Verification

- `cd site && CI=true PUBLIC_POSTHOG_PROJECT_TOKEN=phc_test npm run build` → `[build] Complete!`; `dist/index.html` loads `/_astro/PostHogAnalytics.*.js` (no bare `import posthog` in HTML).

## Open / next

- Push `main` for GitHub Pages; redeploy game host and Replit demo stack from current `main` (`npm ci && npm run build` in `demos/`).
- Live Replit still served stale demo HTML without PostHog boot until redeploy (server `/posthog-config.js` was already wired).

## Key paths

- `site/src/components/PostHogAnalytics.astro`
- `game/the-last-safety-review/public/posthog.js`, `public/text.html`
- `demos/README.md` (Live deployment)

## Commits

- `dd56696f1` Fix PostHog on companion site, game, and demo deploy docs.

## Not staged (other working-tree edits)

- Field-agenda sync, CIRIS card, campaign plans, concept-graph audits, and untracked drafts/assets — left out of this commit.
