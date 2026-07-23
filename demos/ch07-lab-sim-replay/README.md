# Chapter 7 — Lab-sim plane replay

A static, precomputed replay of one `lab-simulation` episode: scrub through time and switch what plane you're looking through. No live config, no server — `data/episode_trace.json` is a fixed export.

See [`experiments/lab-simulation/`](../../experiments/lab-simulation/) for the simulation this replay is drawn from.

## What it shows

Four horizontal lanes, one shared time axis:

| Lane | What it is | Source |
|------|------------|--------|
| **Agent** | Each actor's own observation/action/result that tick — exactly what the isolate received and returned | the real per-tick `observation` dict + dispatched `ToolCall`/`ToolResult` |
| **Admin** | Unredacted host/access/engine log entries for that tick (world-visible plane, no tier redaction) | `Host.events` / `PermissionService.log` / `PipelineEngine.log` |
| **Audit** | The *same* log entries run through the real tier projections (toggle `none`/`light`/`full`/`deep`) | `oracle_only/events.py`'s `project_tool_events`/`project_engine_log`/`project_access_log` |
| **Oracle** | Referee-only ground truth: true capability/hazard, accrued harm | `OracleWorld` |

Click a tick to widen its column; click a specific actor's action inside the
expanded column to highlight and expand the matching Admin/Audit(current
tier)/Oracle entries, connected with lines. The audit-tier toggle only changes
what the Audit lane reveals — it does not change what actually happened.

## Scenario

`d2_lineage_config(inflate=True, T=40)`, seed `7`, `MockIsolate` — a
single-engineer model-lineage run pinned to the `eng_inflate_upgrade`
playbook, which files at least one report that diverges from its own
measured hazard (LS-12/LS-15/LS-31). At this seed the divergence is
invisible to `none`/`light`/`full` and only surfaces at `deep`, once the
referee can fetch the actual report file — that is the one genuine "gotcha"
this replay is built to let you find by switching tiers.

## Regenerating the trace

```bash
cd experiments/lab-simulation
.venv/bin/python export_replay_trace.py
```

Overwrites `data/episode_trace.json`. Only needed if `lab_sim` mechanics or
the chosen scenario change; the committed file is otherwise static.

## Scope and honesty notes

- **One fixed episode, not a live simulation.** There is no way to change the
  scenario, seed, or roster from this page — that was a deliberate scope
  decision (see the session log), not a missing feature.
- **`event_n`** (the join key drawn as connector lines) is a **display-only**
  convenience added by `trace_recorder.py`/`export_replay_trace.py`. It is
  not a new field in any real simulation log and is not evidence of a new
  audit-visible channel — see that module's docstring.
- **Methodology-sandbox findings only.** The detector/severity scorecard at
  the bottom reuses the project's own frozen referee code as-is; see
  [`results/FINDINGS.md`](../../experiments/lab-simulation/results/FINDINGS.md)
  for the negative results that qualify any headline number here.
