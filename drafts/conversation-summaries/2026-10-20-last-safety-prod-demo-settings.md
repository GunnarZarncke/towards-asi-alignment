# 2026-10-20 — Last Safety prod demo settings

kind: correction
uptake: local

## Trigger
Deployed game showed **Demo / no model** on in Lab Access Settings by default; user asked to omit demo mode from production settings.

Prompts: (paraphrase-only — no prompt id in transcript)

## Done
- content: `defaultSettings().demoMode` default **off** (was on).
- content: `visibleSettings()` hides `devOnly` rows (demo mode) on embedded engine handset (`engine && embed`).
- content: Settings hint for demo mode only when that row is visible (solo fixture).
- content: `spec/terminal.md` documents prod vs harness.
- content: `tests/terminal.test.mjs` regression for `visibleSettings`.

## Decisions
- Demo parsing stays server-side (`OPENAI_API_KEY`, `DEMO_MODE`); phone toggle remains fixture/solo harness only and does not drive the live parser.

## Open / next
- Redeploy game host so players get the updated phone bundle.

## Key paths
- `game/the-last-safety-review/public/terminal/project.mjs`
- `game/the-last-safety-review/public/terminal/phone.js`

## Commits
- `ed86a2ea6` Hide demo mode from Last Safety production handset Settings.

## Verification
- `cd game/the-last-safety-review && node --test tests/terminal.test.mjs` → `ℹ pass 11` `ℹ fail 0` (2026-10-20).
