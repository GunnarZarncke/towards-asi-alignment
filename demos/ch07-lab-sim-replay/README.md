# Chapter 7 — Lab-sim plane replay

A static, precomputed replay of `lab-simulation` episodes: scrub through time and switch what plane you're looking through. No live config, no server — JSON under `data/` is fixed export output.

See [`experiments/lab-simulation/`](../../experiments/lab-simulation/) for the simulation this replay is drawn from.

## Modes

Open via the local demo server (`cd demos && python3 serve.py`):

| URL | Mode |
|-----|------|
| `/ch07-lab-sim-replay/` | Hub: **ET-4 case brief** (default) + classic D2 replay tabs |
| `/ch07-lab-sim-replay/?mode=et4` | ET-4 hackathon case brief only |
| `/ch07-lab-sim-replay/?mode=classic` | Original D2 lineage replay only |

### ET-4 case brief (Secret Loyalties hackathon)

Three variants on one preregistered seed (201, BB high-hazard cell):

| Variant | What it shows |
|---------|----------------|
| **Organism** | Pipeline-embedded secret loyalty → loyal reviewer approvals and directional deploys |
| **Content-matched control** | Same private profile structure, loyalty disabled → stalls at review |
| **Remediation** | Audit-visible deploy hold from filed report hazard only |

The UI adds:

- Confirmatory aggregate strip (frozen `et4-0.1.0` means)
- Evidence anchor cards with one-click jump to tick + actor
- ET-4 episode scorecard (principal-A + A0/A3 affordances) alongside the frozen detector table

Private prompt bodies are **not** exported — only audit-plane projections and precomputed summaries.

### Classic D2 replay

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

## Regenerating traces

**Classic D2 lineage:**

```bash
cd experiments/lab-simulation
python3 export_replay_trace.py
```

**ET-4 case brief (organism / control / remediation):**

```bash
cd experiments/lab-simulation
python3 export_et4_replay_traces.py
```

Overwrites `data/episode_trace.json` or `data/et4_case_brief.json` respectively. Only needed if `lab_sim` mechanics or the chosen scenario/seed change; the committed files are otherwise static.

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
