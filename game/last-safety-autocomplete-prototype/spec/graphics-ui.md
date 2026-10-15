# Graphics and UI

Lane: graphics / UI. Code: `public/index.html`, `public/style.css`, `public/app.js`, and later `public/render/`. Reads [world.md](world.md) for room and character identity. Reads [contract.md](contract.md) for what it may draw.

Rooms render as live Three.js scenes (`public/render/three-scene.mjs`). The CSS room in `public/render/scene-view.mjs` is the fallback when WebGL or the `three` package is missing.

## Confirmed picture

One fixed camera per room, drawn with Three.js. The player selects rooms, doors, people, and objects. There is no free-moving first-person body.

The player has a third-person body in the fixed camera. Clicking the floor walks the player there. Clicking another person in the room sets them as the default addressee for the next sentence (same as the addressee chips in the transcript dock). Clicking a door, record, or workstation walks the player to it, then performs the action. A walk does not change what anyone knows. It is still an event, clocked by fuel, so a recording can replay it (O-31, O-36).

Look: modern, architectural, moderately stylized, restrained color, readable on a desktop browser and a phone, ordinary lab rather than a military site or a science-fiction set. Glass, plants, daylight, computers, security gear, test equipment.

NORA has no body, face, or robot shell. Presence is screens, jobs, transcripts, and camera overlays.

Amara, when `presence` is `hologram`, uses the same procedural body and walk as staff. Draw her translucent, same silhouette, cooler tint — a 2027 visitor projector, not a science-fiction effect. She occupies Evaluation spots. Click-to-walk works inside that room. Door and exit hotspots do not path her. When `presence` is `absent`, draw no body. Evaluation has a **virtual projector** prop (`virtual_projector`). It is furniture, inspectable for the name; it is not a second conversation mode.

## Renderer (O-33 closed)

Stay with live Three.js. One fixed camera per room, weak perspective, act lighting as data (`public/render/lighting.mjs`), surveillance as a filter plus annotations on the same geometry and camera. Do not switch renderers.

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

Annotations are beliefs. They can be wrong. The UI must keep raw observation distinct from an annotation. A recording is this scene rebuilt by replaying stored events (O-36), including movement, at the fuel index the video app is showing. It is not a separate exported movie.

## Acts

Lighting and music change in steps. No day–night cycle. Every room uses the act preset, with local variation.

| Act | Light | Music |
| --- | --- | --- |
| I Welcome | Soft daylight plus ceiling panels; warm gray, muted green | Quiet electronic ambience, sparse melody |
| II Doubt | Cooler daylight, ceiling panels, screens matter more | Held rhythm, tension |
| III Decision | Invisible ceiling lights off; soft warm desk pools (not spot beams), dim room fill, bright screens | Sparse low tones, more silence |

Music waits until the story is set (O-37). Ship silence until then.

## Characters

Current procedural bodies and their walk, idle, and stand are enough (O-34, O-35). More detail, if it is added, is for conversations: a closer view of the same body, not a new character style. Facial capture and lip sync stay out. The longer pose list (sit, nod, interrupt, status stance) waits with that conversation detail. A hologram reuses that body with a material flag from `ClientState.actors[].presence`. Do not build a video-call overlay.

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

The room view fills the window. Everything else floats over it:

- floating overlay chips (not a full-width bar): room title; act then clock and fuel; Map, Lab Access, and menu (save, load, reset, text version);
- when the engine adds a new learned fact, a short dialog offers to copy it into the handset Notes app (doors, records, and the 3D room already cover navigation and evidence; only “what you know” needed this path);
- bottom transcript dock (no panel chrome): recent talk flush left above an auto-growing composer, addressee chips and suggestion chips just above the input, the More link when enabled; the scrollback and chips stay hidden until the composer is focused (tap the input or the dock to expand; a tap outside the dock—or keyboard focus leaving the dock—collapses it again, without hiding chips before a suggestion or Show more click lands);
- thought bubble and ending card near the top.

On a viewport narrower than the room (a phone held upright), the canvas is at least 1.5 × the viewport height wide and scrolls sideways. Each frame the renderer reports the player's screen position (`RoomRenderer.playerScreen()`, `onFrame`) and the page keeps the player near the middle. A manual swipe or wheel pauses the follow for a few seconds.

Debug panels show only in test mode: the parser inspector (structured meaning, construction trace, resolving “it”, API usage), the demo/live pill, and the parser indicator. Test mode is `?test=1` on the URL, and always on in `npm run dev:ui`. The handset's own Parser inspector setting ([terminal.md](terminal.md)) is separate and stays inside the phone.

The floorplan button opens the verified courtyard plan (`public/floorplan.svg`). The current room is marked. A click walks one door from `lib/floorplan.mjs`. The prototype badge is clearance 2, so the test bay and security control stay shut. The engine rejects any other move.

The player computer is an issued **Lab Access** handset overlay specified in [terminal.md](terminal.md). This lane does not edit `public/terminal/`. Graphics reserves a right-hand slot on desktop and a full-screen slot on a narrow viewport; the terminal lane draws the bezel, homescreen, and apps. Draw that overlay only when `ClientState.labAccessActive` is true. Before activation, reserve no launcher and do not blink. After activation, a room object of kind `terminal` may be the pocketed handset; tapping it, or a persistent launcher, opens the overlay. When the terminal says a notification is unread, that object blinks. The blink carries no text. The Photo app **is** the main room view: tapping Photo closes the handset overlay and hides all other room chrome. The player pans and pinches the live Three.js view; only a round shutter remains on screen. Shutter writes a centered portrait crop to `photos/` via `file.write`, then Lab Access reopens on the saved file. Esc cancels and restores the phone.

Later surfaces, still this lane visually and the engine for data: evidence reader and comparison of two records. Notes are the handset Notes app ([terminal.md](terminal.md), O-13). Save and load are local storage plus a JSON file (O-31); this lane only needs export and import controls. **TSA “More” link (O-41).** Controlled by the phone setting (default off). This lane draws a single line fixed to the bottom of the room view (not inside the phone bezel). Format: the literal prefix `More: `, then one underlined phrase — a very short summary from the concept card, not the full title. It is a normal link to the companion site card (`/cards/{slug}/` on the deployed site; absolute URL in production). The engine sends at most one `{ summary, href }` in `ClientState` (see [contract.md](contract.md)). If the setting is off, or the field is null, draw nothing. When several concepts become relevant in the same room, show only the last one triggered; keep showing that link until the player changes room, then clear until the next trigger. Do not stack multiple links.

**Thought bubble.** When `ClientState.thought` is set, draw one bubble on the room view. It stays until the player closes it (an ×) or copies it (a paper icon). Copy writes a private note through the engine and clears the bubble. The bubble is the player’s, including when other people are elsewhere. It is not dialogue. The lightbulb opening that produces it is specified in [grammar.md](grammar.md). Draw it only from `thought`. Do not invent the text.

Composer behavior to preserve:

- One action can be a tap, a partial type plus a completion, or free text.
- Composer placeholder carries the completion hint (after “Tap to speak…”): completions help say a question; they do not answer it.
- Parser indicator distinguishes local grammar from a model call.

Voice input is later, not this lane’s first job.

## Solo check

Load `fixtures/client-state.json` and a scene fixture with no `lib/game.mjs` and no model call. Required once `dev:ui` exists:

- Platform Operations readable at desktop width and a narrow phone width.
- Act lighting presets switch without a reload of game logic.
- Surveillance mode uses the same hotspots as play, plus annotation fields present in the fixture.
- An evidence row that the fixture marks unexamined cannot be presented as already read.
- Interactive objects in the fixture are visible and hit-testable; objects absent from the fixture are not.
