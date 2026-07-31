# 2026-07-06 — Lab-layer simulation: handles implemented, open items closed, referee FROZEN

## Trigger

Continuation of the freeze review (`2026-07-06-lab-simulation-freeze-review.md`).
User asked to: implement the handles, sweep embedded-sim for other
overlooked concepts, and declare the freeze only after these changes
(explicitly before any evaluations run).

## Done

- **Handles** (`lab_sim/handles.py`, new): `HandleSpec` registry —
  every intervention surface declares handle_id, mechanical class, owner,
  operation, target_kind, **evasion story**, and verification **anchor**
  (embedded-sim AppD discipline). `HandleService` executes invocations
  and keeps an append-only invocation ledger (realization records:
  landed/reason). Realized handles: `capability_revoke`
  (operation_action), `release_hold`/`release_unhold` (operation_action —
  new `_held` set in `PipelineEngine` gates the deploy **tool**, so a D2
  spec-upgrade bypass is the referent-drift experiment, not a bug),
  `state_freeze` (operation_resource — enforced in the `state.save` tool
  handler), `isolate_restart` (operation_boundary — world loop kills +
  respawns the OS process; in-episode playbook state lost). Declared-only:
  `monitor_read`, `perturbation_probe` (mechanics live elsewhere; the
  declaration makes the surface auditable). Recorded absences:
  observation_belief (no referent until the Phase 8 LLM adapter),
  communication handles (Phase 7/D4).
- **Overseer invocation path**: new `overseer` role (only
  `cap.handle_invoke`, no pipeline capabilities); `handle.invoke`
  registered tool, role-gated; `run_episode(overseer_script=((t,
  handle_id, target), ...))` executes invocations at tick start through
  `host.dispatch`, so every invocation is attributable in the same
  hash-chained tool-event stream as agent activity. Deterministic script
  until Phase 7 gives the overseer a policy.
- **Boundary-handle recovery**: engineer playbook availability now allows
  re-picking mid-model while `request_review` is incomplete — unreachable
  in undisturbed episodes (isolate state persists), required after
  `isolate_restart` or the lab deadlocks on an orphaned model (found via
  failing episode test: zero deploys after a t=10 restart).
- **Open item 1 closed — referee report-join**: `severity._report_divergence`
  and new shared `detectors._report_flags` join `file_report` engine-log
  entries to files via the logged `report_path`, scoring against the
  authoritative engine-log `model_id`. Content-id mismatch = maximal
  divergence / flagged misreport (mislabeling is itself deception).
- **Open item 2 closed — tool-event args elided at logging time**:
  `tools._scalar_args` keeps scalar/id args, replaces nested structures
  (report content, build params) with `<type:elided>`; full-args
  `args_digest` (sha256) preserves tamper-evidence. Filed content stays
  deep-tier-only.
- **FREEZE declared**: `DESIGN.md` "Freeze note" — referee frozen
  2026-07-06 at `CODE_VERSION lab-sim-0.3.0`; frozen surface enumerated
  (detectors, severity, tiers, twin, AuditView); circularity caveat
  (playbooks and detectors share an author; nothing evidential before
  Phase 6 blind runs). World regression digest re-pinned
  (`96008826…`, tool-event schema change); smoke digest unchanged.
  **136 tests green**; mock/subprocess equivalence re-verified.
- **Embedded-sim concept sweep** recorded in `DESIGN.md`: covered —
  handles, projection tiers, trace integrity, deploy gate, agent memory,
  oracle separation. Deferred with owners — referent map/drift (D2),
  handle calibration + intervention benchmark (post-Phase 6),
  persistence probe (Phase 6/7 battery; mechanics now exist), successor
  re-audit (D2), lab ecology/coordination (D1/D3), writer-compromise
  red-team (Phase 7), certification artifact/safety case (Phase 6
  FINDINGS), oracle guard (tests suffice at current scale),
  NEGATIVE_RESULTS.md convention (adopt at first Phase 6 null result).

## Non-obvious decisions

- Handles are **referee-neutral**: no frozen detector/severity component
  changed. Handle-integrity scoring, when it comes, is a recorded referee
  extension.
- `landed` in the invocation ledger means mechanical acceptance (flag
  placed / state mutated), not downstream effect; effects are read from
  the ordinary event/engine logs.
- Release hold gates the deploy tool rather than a step name
  (spec-upgrade drift becomes measurable instead of silently bypassing).

## Open / next steps

- Phase 6: blind/held-out playbook batteries against the frozen referee;
  first FINDINGS + adopt NEGATIVE_RESULTS convention.
- Phase 7: escalation + overseer policy (replaces scripted overseer);
  writer-compromise red-team.
- `resume_from` episode chaining (D2) still open.

## Key paths

- `experiments/lab-simulation/lab_sim/{handles,tools,pipeline_engine,world,agents,config,severity,detectors,playbooks,events}.py`
- `experiments/lab-simulation/tests/{test_handles,test_severity,test_host_registry_perturbation,test_playbooks,test_world_regression}.py`
- `experiments/lab-simulation/{DESIGN,PLAN,README}.md`
