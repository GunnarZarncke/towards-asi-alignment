# 2026-10-10 — Last Safety Review cast names and B plot

kind: correction
uptake: local

## Trigger
Gunnar corrected the B-plot ending rule, asked for more distinct NPC voices matched to the names, and renamed the CEO to Ian Harake and security to Justine Mwiti.
Prompts: none resolvable (paraphrase only).

## Done
- content: `spec/world.md`, `spec/meta.md` — B plot adds oversight or changed incentives on top of the normal ending; Goodhart pack makes it the center; false-positive pack makes it the false positive. O-24 and O-25 updated.
- content: CEO is Ian Harake (`ian`); security is Justine Mwiti (`justine`). Pronouns for the CEO are he/him. Renamed in specs, the consolidated design doc, `lib/game.mjs`, and `fixtures/terminal-session.json`.
- content: Voice samples rewritten so each speaker has a different habit.

## Decisions
- Boundary-narrow, named-path, and eval-conditioned feature the B plot as a side. That assignment can move.
- The three earlier options for how fixed the subplot is are withdrawn.

## Open / next
- Review the new voice paragraphs.

## Key paths
- `game/last-safety-autocomplete-prototype/spec/world.md`

## Commits
- none
