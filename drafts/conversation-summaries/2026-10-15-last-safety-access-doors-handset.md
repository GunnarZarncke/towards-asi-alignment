# 2026-10-15 — Last Safety access gates, visitor doors, handset UX

kind: new-work
uptake: status

## Trigger
Tighten boundary-narrow difficulty (Justine reason, lunch commons, meetings); fix players walking into restricted rooms without access; show badge clearance on the handset, compact home notices, and note previews on hover.

Prompts: (session continuation — prior thread on access/doors; handset UI follow-up)

## Done
- content: Pack **access gates** (`lib/world/access-gates.mjs`, `boundary-narrow.mjs`) for wide Evaluation/People/Policies/Platform API paths until Ian intro or stated reason; in-room approver uses `walk_and_ask`.
- content: **Progressive door clearance** (`lib/world/visitor-clearance.mjs`): 0 pre–Lab Access, 1 hub after confirmation, 2 after intro or DM to Justine; People/Model edges require 2; specs updated (`engine.md`, `world.md`, `graphics-ui.md`, `access.md`).
- content: **NPC lunch** band (12:00–12:45), **meet** grammar, **accept_meeting** / Ian **introduce_justine** role rule; meeting held when player talks in commit room.
- content: Handset **Clearance** in status bar (`terminal-host.mjs` + `phone.js`); **compact notifications** and scroll stack; **Notes** hover/focus tooltip preview (touch: inline clamp).
- content: Tests — `access-gates.test.mjs`, `visitor-clearance.test.mjs`, floorplan/engine/helpers/incident updates; `npm run test:engine` 33/33 pass.

## Decisions
- Physical doors mirror trust predicates (intro or `told(justine,…)`) rather than a separate grant list — keeps handset gates and badge in sync.
- `startedSession()` helper asks Ian for Justine intro so scripted strategies still reach Platform.

## Open / next
- Optional: escort/host-walk narrative when player tries north spine at clearance 1; evaluation-only door set on Lab Access alone (SEC-ARCH assigned evaluator) if playtests feel too gated before Ian.

## Key paths
- `game/last-safety-autocomplete-prototype/lib/world/visitor-clearance.mjs`
- `game/last-safety-autocomplete-prototype/lib/world/access-gates.mjs`
- `game/last-safety-autocomplete-prototype/public/terminal/phone.js`

## Commits
- `9ab6fe59d` Last Safety: gate API access, progressive door clearance, handset UX.
