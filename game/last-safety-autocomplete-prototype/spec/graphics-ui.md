# Graphics and UI

Lane: graphics / UI. Code: `public/index.html`, `public/style.css`, `public/app.js`, and later `public/render/`. Reads [world.md](world.md) for room and character identity. Reads [contract.md](contract.md) for what it may draw.

Rooms render as live Three.js scenes (`public/render/three-scene.mjs`). The CSS room in `public/render/scene-view.mjs` is the fallback when WebGL or the `three` package is missing.

## Confirmed picture

Fixed-perspective 2.5D. The player selects rooms, doors, people, and objects. There is no free-moving first-person body.

Working (10 October 2026, on request): the player has a third-person body in the fixed camera. Clicking the floor walks the selected person there. Clicking a person selects them. Clicking a door, record, or workstation walks the player to it, then performs the action. Positions inside a room are presentation only. They are not engine state and do not change what anyone knows.

Look: modern, architectural, moderately stylized, restrained color, readable on a desktop browser and a phone, ordinary lab rather than a military site or a science-fiction set. Glass, plants, daylight, computers, security gear, test equipment.

NORA has no body, face, or robot shell. Presence is screens, jobs, transcripts, and camera overlays.

## Renderer (O-33 closed)

Selected: live Three.js scenes, one fixed camera per room, weak perspective, act lighting as data (`public/render/lighting.mjs`), surveillance as a filter plus annotations on the same geometry and camera.

Still recommended, not selected: glTF assets from one shared low-poly kit. Until the kit is chosen, furniture and bodies are procedural primitives (`public/render/kit.mjs`, `public/render/person.mjs`). Room layouts are data (`public/render/layouts.mjs`). Do not download packs before the kit choice.

Screen textures are abstract (bars, charts, the NORA name). They must not show incident facts, which would leak evidence the player has not examined.

The player experience constraint is the fixed camera, not the renderer.

## Scene the renderer may assume

Per location, once gate 2 starts:

- Stable room id from [world.md](world.md).
- Dimensions, architectural template, camera.
- Asset instances (position, rotation, id).
- Character spots and interaction points.
- Clickable objects and restricted passages.
- Lighting overrides.
- Surveillance camera id.

Assets are shared across rooms. Missing ids fail a check; they are not replaced with a lookalike at runtime.

Hotspots come from the scene view in the contract. A prop that is only art is not an inspect target.

## Surveillance

Same room geometry and, preferably, the same camera as play.

Overlay: grayscale or strongly desaturated image; red tracking rectangles; name or inferred identity; confidence; inferred activity; other retrieved fields; camera id and timestamp.

Annotations are beliefs. They can be wrong. The UI must keep raw observation distinct from an annotation. A recording shows an earlier scene state (O-36: live rebuild versus exported video, open).

## Acts

Lighting and music change in steps. No day–night cycle. Every room uses the act preset, with local variation.

| Act | Light | Music |
| --- | --- | --- |
| I Welcome | Soft daylight plus ceiling panels; warm gray, muted green | Quiet electronic ambience, sparse melody |
| II Doubt | Cooler daylight, ceiling panels, screens matter more | Held rhythm, tension |
| III Decision | Invisible ceiling lights off; soft warm desk pools (not spot beams), dim room fill, bright screens | Sparse low tones, more silence |

Music assets are undecided (O-37). Ship silence until a licensed set is named.

## Characters

Reusable bodies: sit, stand, walk, turn, idle, nod, interrupt, open and closed posture, a few expressions, high-status and low-status stance. Conversation may cut to a portrait from the same model. Facial capture and lip sync are out of the first version (O-35).

Status may change posture and timing. It does not change the facts on screen.

## Asset check (9 October 2026)

Nothing is vendored. Packs still published, marked CC0 on their pages:

| Pack | Use | Note |
| --- | --- | --- |
| Kenney Furniture Kit | Interior props | CC0. Official files are OBJ, not glTF. |
| KayKit Furniture Bits | Interior props | CC0, includes glTF. Different proportions and color from Kenney. |
| Quaternius Universal Base Characters | Bodies | Page says CC0 and glTF. Site also has a Quaternius Asset License that forbids redistributing the raw pack. Safe to use inside a build; do not commit the upstream zip to this public repo until the download’s license is confirmed. |
| Quaternius Universal Animation Library | Motion | Same license caution. Free listing emphasizes FBX; confirm glTF on the file you take. |
| Poly Haven | Light and materials | CC0. HDRI lighting can serve a stylized scene. Photoscanned materials fight the stylized rule. |
| Kenney UI Pack, Interface Sounds | Chrome and clicks | CC0. Not the act music. |

Use one furniture kit. Do not mix Kenney and KayKit in one lab. Custom work the packs will not cover: clothes that read as this staff, test-bay equipment, NORA’s UI, a few hero objects.

## Interface

The shell already has: room list, evidence list, known entities, conversation, composer, suggestion row, parse inspector, construction trace, token usage.

The player computer is a **phone overlay** specified in [terminal.md](terminal.md). This lane does not edit `public/terminal/`. Graphics reserves a right-hand slot on desktop and a full-screen slot on a narrow viewport; the terminal lane draws the bezel, homescreen, and apps. A room object of kind `terminal` is optional chrome (a desk phone or a pocketed handset). Tapping it, or a persistent launcher, opens the overlay. The Photo app needs a still (or live texture) of the current room camera, pan/zoom inside the phone only; capture is a file write, not a change to the room camera.

Later surfaces, still this lane visually and the engine for data: evidence reader, comparison of two records, hypothesis notes (representation is O-13), save/load chrome (format is O-31).

Composer behavior to preserve:

- One action can be a tap, a partial type plus a completion, or free text.
- Suggestion caption: completions help say a question; they do not answer it.
- Parser indicator distinguishes local grammar from a model call.

Voice input is later, not this lane’s first job.

## Solo check

Load `fixtures/client-state.json` and a scene fixture with no `lib/game.mjs` and no model call. Required once `dev:ui` exists:

- Platform Operations readable at desktop width and a narrow phone width.
- Act lighting presets switch without a reload of game logic.
- Surveillance mode uses the same hotspots as play, plus annotation fields present in the fixture.
- An evidence row that the fixture marks unexamined cannot be presented as already read.
- Interactive objects in the fixture are visible and hit-testable; objects absent from the fixture are not.
