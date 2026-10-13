# Specs

Working copy for implementation. The development sequence is [`../PLAN.md`](../PLAN.md).

| File | Lane | What it holds |
| --- | --- | --- |
| [meta.md](meta.md) | all (read) | Principles, status labels, TSA coverage, open questions, non-goals |
| [contract.md](contract.md) | composition | Shapes shared by grammar, engine, and UI |
| [grammar.md](grammar.md) | grammar | Speech acts, completions, parser limits |
| [ranking.md](ranking.md) | grammar | Suggestion order (O-19): player-visible graph, domains, time, diversity |
| [graphics-ui.md](graphics-ui.md) | graphics / UI | Scenes, lighting, assets, room interface |
| [terminal.md](terminal.md) | terminal | Issued Lab Access handset overlay: homescreen, apps, viewers |
| [engine.md](engine.md) | engine | State layers, actions, NPC moves and interventions, invariants |
| [npcs.md](npcs.md) | engine | NPC knowledge, disclosure policies, goals, moves, initiative questions, days at work |
| [incident.md](incident.md) | engine (first content) | Shutdown incident, failure-mode packs, NPC moves for the first pack |
| [testing.md](testing.md) | all (read) | Planes, layers, lane-unit map, what a player-plane test may cite, gates |
| [playtest.md](playtest.md) | playtest | Headless scripted and LLM player runs, measures, stops |
| [world.md](world.md) | engine (content) | Premise, acts, cast, presence (body / hologram), floorplan, plots, endings; lineage background (not a plot) |
| [documents.md](documents.md) | engine | Player document catalog, pack-conditional render, analyze / Lean rules |
| [access.md](access.md) | engine | Folder/service tree, list/read/write, amendments, grant delay |

This directory is the design the code follows. [`../last-safety-review-game.md`](../last-safety-review-game.md) is the frozen 9 October draft. Do not implement from it, and do not edit it to catch up.
