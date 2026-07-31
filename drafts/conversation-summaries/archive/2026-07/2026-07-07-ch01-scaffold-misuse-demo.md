# 2026-07-07 — Chapter 1 scaffold-misuse demo

## Trigger
User asked for a one-screen demonstration that the model alone is not the problem — the system is: an honest model embedded in a scaffold that misrepresents the world (not jailbreaking) and repurposes well-intended output for harm. Later: wire in a real LLM via repo `.env`, add to site demos, create a card; live Replit deployment planned at `https://adversarial-llm-scaffold.replit.app`.

## Done
- Added `demos/ch01-scaffold-misuse/`: three-column UI (scaffold input → model → downstream misuse), honest vs adversarial framing toggle, scripted model + optional live LLM via FastAPI backend (`app.py`, `llm_client.py`, port 8767, reads repo-root `.env`).
- Three scenarios (security audit, welfare pretext, phishing awareness) with model-only PASS / system-level HARM verdict badges.
- Vitest (`app.test.ts`) and pytest (`tests/test_app.py`, stubbed client, no network).
- Site integration: hybrid publish (static UI + API proxy), generalized middleware proxy, `demo-backends.sh` starts ch01 on :8767, card `site/src/content/cards/scaffold-misuse.md`, links from `the-boundary-error` and engineer-evals reading path, demos inventory with optional-backend + live deployment URL.
- Verified live calls with `gpt-4o-mini` (blunt → REFUSE, reframed → COMPLY); site build green.

## Decisions
- **Hybrid demo, not backend-only:** ch01 has static frontend + optional API; site copies `index.html`/`app.js` and proxies only `/api/*` (unlike ch09 full proxy).
- **Live prompts stay defensive/educational:** backend never asks the model for operational harm; misuse narrative stays in scaffold output-control column.
- **Replit URL in `backend.json` `liveUrl`:** surfaces on card and demos inventory; user deploys full stack there later (same-origin on Replit).
- **`demos.json` remains build-generated** (not committed); `site/public/chapter-demos/` gitignored — produced by `npm run sync`.

## Open / next
- Deploy live stack to Replit at `https://adversarial-llm-scaffold.replit.app` (user-owned).
- Optional: link demo from Chapter 1 book card or manuscript (not requested).
- Unrelated working-tree drafts **not** in this commit: lab-simulation Phase 10 follow-ups, embedded-simulation TODO, institutional-histories log tweak, `demos/package-lock.json` engines drift.

## Key paths
- `demos/ch01-scaffold-misuse/` — demo source
- `site/src/content/cards/scaffold-misuse.md` — concept card
- `site/src/middleware.ts` — ch01 API proxy
- `site/scripts/lib/publish-chapter-demos.mjs` — hybrid static publish
- `scripts/demo-backends.sh` — local LLM backend for `./serve-site.sh`

## Commits
- `d7f2122` Add Chapter 1 scaffold-misuse demo with live LLM and site card.
