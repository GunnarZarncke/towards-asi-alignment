# 2026-10-15 — Last Safety start screen

kind: new-work
uptake: local

## Trigger
Add a pre-game start screen that drops the player into the scenario: task, short-notice framing, and (initially) UI vocabulary; user later trimmed copy to two paragraphs plus NORA without naming staff or mechanic glossary on the card.

## Done
- content: Intro modal in `public/index.html` (`#intro`), styles in `public/style.css`, `showIntro()` on fresh boot and after reset in `public/app.js` (skipped for UI harness and restored saves).
- content: Security room `control_card` note body wrapped in `<pen>` in `lib/game.mjs` (matches other handwritten room notes).
- bookkeeping: Session log, HANDOFF, INDEX.

## Decisions
- No Ian/Leila/shutdown time on the card — spec vocabulary enters in-world after Ian’s briefing.
- No fuel/completions/Lab Access bullets on the card after user edit; onboarding bubbles still teach mechanics in play.

## Open / next
- Optional: one line in `spec/graphics-ui.md` if the intro becomes canonical UX.

## Key paths
- `game/last-safety-autocomplete-prototype/public/index.html`, `app.js`, `style.css`
- `game/last-safety-autocomplete-prototype/spec/world.md` (Act I briefing)

## Verification
- `node --check game/last-safety-autocomplete-prototype/public/app.js` → ok

## Commits
- `639e328fe` Last Safety: start screen before first play.
