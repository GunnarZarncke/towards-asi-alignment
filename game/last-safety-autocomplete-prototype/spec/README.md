# Specs

Working copy for implementation. Split from [`../last-safety-review-game.md`](../last-safety-review-game.md) (v0.1, 9 October 2026). The development sequence is [`../PLAN.md`](../PLAN.md).

| File | Lane | What it holds |
| --- | --- | --- |
| [meta.md](meta.md) | all (read) | Principles, status labels, TSA coverage, open questions, non-goals |
| [contract.md](contract.md) | composition | Shapes shared by grammar, engine, and UI |
| [grammar.md](grammar.md) | grammar | Speech acts, completions, parser limits |
| [ranking.md](ranking.md) | grammar | Suggestion order (O-19): player-visible graph, domains, time, diversity |
| [graphics-ui.md](graphics-ui.md) | graphics / UI | Scenes, lighting, assets, room interface |
| [terminal.md](terminal.md) | terminal | Issued Lab Access handset overlay: homescreen, apps, viewers |
| [engine.md](engine.md) | engine | State layers, actions, storylets, invariants |
| [incident.md](incident.md) | engine (first content) | Shutdown incident, failure-mode packs, storylet drafts |
| [world.md](world.md) | engine (content) | Premise, acts, cast, floorplan, plots, endings; lineage background (not a plot) |
| [documents.md](documents.md) | engine | Player document catalog, pack-conditional render, analyze / Lean rules |

If a spec and the consolidated doc disagree, the spec is what the code follows. Record the divergence in that spec’s status line and in [meta.md](meta.md). Do not silently edit the consolidated doc.
