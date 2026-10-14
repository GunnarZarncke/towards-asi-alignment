# 2026-10-15 — Last Safety handset UI, photo viewer, notices

kind: new-work
uptake: status

## Trigger
Finish open work from the handset session: reliable orange notification clearing, room Photo embed and HUD/composer polish, Jun first-person dialogue fix, and photo viewing from Files.

Prompts: (paraphrase — prior thread summarized)

## Done
- content: Floating HUD chips (act left of clock/fuel); removed Cam/Play; composer “Show more” and placeholder hint; notebook drawer removed (earlier commit); Photo app uses main 3D room + shutter; `markNoticeTarget` and route-based seen marking for notifications; `/api/handset-file` + image viewer/thumbnails in Files; NPC work lines first-person (`npcs.mjs`, `llm.mjs`, glue test); specs `graphics-ui.md`, `terminal.md`.
- bookkeeping: Session log; HANDOFF/INDEX.

## Decisions
- Photo bytes stay in session; terminal projection and `file.read` use `href` to `/api/handset-file` so JSON and saves are not bloated.
- Notice read state stays client-side in the phone iframe; clearing follows target visit (file viewer, thread, calendar, API), not only tapping the stack row.

## Open / next
- Manual playtest: notification badges after Files-only open, photo retake if an old capture was truncated under the previous 200KB cap.

## Key paths
- `game/last-safety-autocomplete-prototype/public/terminal/phone.js`
- `game/last-safety-autocomplete-prototype/lib/world/terminal-host.mjs`
- `game/last-safety-autocomplete-prototype/public/app.js`

## Commits
- (this session)

## Verification
- `npm test` in `game/last-safety-autocomplete-prototype`: 97 pass.
