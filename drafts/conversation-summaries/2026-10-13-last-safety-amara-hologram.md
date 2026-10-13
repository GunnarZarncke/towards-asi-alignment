# 2026-10-13 — Last Safety Amara hologram

kind: new-work
uptake: rule

## Trigger
Gunnar: Amara stays remote but appears as a hologram in the room (walk and talk like other NPCs, cannot leave, only disappear), avoiding a remote-interaction mode; virtual projector in docs; contacts once added, then ask to join. Then end of session and commit.
Prompts: paraphrase-only (no prompt id resolved)

## Done
- content: Presence model in `spec/world.md` (`body` / `hologram` / absent). Evaluation suite is the only projector room. Same composer; no video-call UI.
- content: `spec/npcs.md` Amara join/drop; Leila hosts on the projector. Hologram-bound invariant.
- content: Contract `actors.presence` and `contacts.joinable`. Grammar `request`+`join`. Terminal Contacts add-by-engine and Ask to join. Graphics hologram material; O-23 updated.
- content: SEC-ARCH-11 asset row and wiki glossary **Virtual projector**. Glossary test asserts the heading.
- bookkeeping: Engine, ranking, testing, documents, spec README pointers.
- Check: `npm test` in `game/last-safety-autocomplete-prototype` → `ℹ pass 33` / `ℹ fail 0`.

## Decisions
- One projector, Evaluation only. Asking to join from another room still places her there; she does not follow the player through doors.
- Contacts stay engine-authored; the player cannot invent Amara.

## Open / next
- Graphics: projector prop in `layouts.mjs` and hologram material flag (not in this pass).
- Engine: `presence` on session actors; enumerate `go` illegal for hologram.

## Key paths
- `game/last-safety-autocomplete-prototype/spec/world.md`
- `game/last-safety-autocomplete-prototype/spec/npcs.md`
- `game/last-safety-autocomplete-prototype/spec/contract.md`

## Commits
- `63e9a3657` Specify Last Safety testing layers and Amara as an Evaluation hologram.
