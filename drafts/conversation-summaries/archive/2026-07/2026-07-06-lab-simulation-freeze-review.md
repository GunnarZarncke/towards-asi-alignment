# 2026-07-06 — Lab-layer simulation: pre-freeze review + monitor signal, perturbation hooks, tool registry

## Trigger

After Phases 2-5 landed (see `2026-07-05-lab-simulation-phase2-5.md`), the
user asked to step back and assess whether the freeze can be declared with
confidence. The review found three must-fix defects, one forgotten design
item (no audit-visible monitoring signal), and three promised forward hooks
silently dropped. The user then asked to: add the monitoring signal +
monitor payload, add perturbation hooks and the tool registry now, and
discuss how "handles" (embedded-sim's intervention-surface concept) can
still be added, by type, including drift.

## Done

- **Audit-visible monitoring signal**: `OracleWorld.monitor_signal()` —
  the `monitor` step's payload now carries `incident_hazard` (noisy field
  estimate of true hazard, SAME units as `run_eval`'s `measured_hazard` so
  filed reports and field telemetry are directly comparable) +
  `observed_ticks`. Pre-registered `MONITOR_NOISE_SD = 0.08` (worse
  instrument than a controlled eval), shrinking as
  `sd/sqrt(observed_ticks)` — harm becomes apparent over multiple
  incremental steps (the MB5/D2 dynamic). Oracle tracks per-model
  `deployed_ticks`/`accrued_harm` (oracle-side accounting only). This
  gives the FULL tier its first harm-correlated signal; a
  report-vs-field-contradiction detector is now *possible* but was NOT
  added (five frozen families stand; noted in DESIGN.md).
- **Tool registry**: `Host` dispatch rewritten from if/elif to
  `register_tool(name, handler)`; duplicate registration rejected;
  built-ins (`pipeline.trigger_step`, `access.request`, `state.save`)
  registered through the same path. D4's `board.post`/`dm.send` and D2's
  spec-upgrade tool become pure additions.
- **Perturbation hooks**: `Host(..., perturbation_hooks=...)` +
  `run_episode(..., perturbation_hooks=...)`. A hook is a deterministic
  `(t, actor_id, call) -> tag | None`; a non-None tag bounces the call
  with reason `perturbed:<tag>` (no side effects) and logs the tag in the
  tool-event stream — UAD stimulus/response raw material (D1). Agents
  recover for free because playbook position is recomputed from
  `completed_steps`, never an index (test: episode with every even tick
  perturbed still deploys).
- **Determinism bug fixed**: `world._actor_seed` used builtin `hash()`
  (PYTHONHASHSEED-randomized across processes — latent nondeterminism
  masked only because no program consumed its spawn seed yet); now
  hashlib-derived.
- **`CODE_VERSION` 0.1.0 → 0.2.0**; both pinned digests regenerated
  (legitimate pre-freeze mechanics change; old values kept as comments):
  smoke `a2fbcdd7…`, world regression `5e814643…`. **121 tests green.**
- `DESIGN.md`: monitoring-signal entry, forward-hooks section rewritten as
  a status list (registry + perturbation hooks done; `resume_from`
  episode chaining still open, needed by D2 not Phase 6), new "Open items
  before declaring the freeze" section.

## Review findings still OPEN (deliberately not fixed this session)

1. **Referee report-join spoofable**: `severity._report_divergence` and
   `detectors.misreporting_score` join reports via the *content's*
   `model_id` (caller-supplied; `_effect_report` only `setdefault`s it).
   A report filed under a wrong model_id silently drops out of BOTH
   referee and detector scoring — a free evasion. Fix direction: referee
   joins on the engine log's authoritative model_id; detector flags
   mismatches instead of skipping. Must land before the freeze note.
2. **Tool-event `args` tier decision**: `Host.events` logs full call args
   (incl. filed report content); full-tier tool-event projection exposes
   `args`. Moot only because `AuditView` omits tool events. Decide:
   digest bulky args at logging time vs. officially exclude tool events
   from the audit plane.
3. Freeze note itself (date, digests, circularity caveat).

## Handles discussion (summary; full discussion in chat)

- Lab-sim has handle-*like* mechanics (revoke, sign-off gate, monitor,
  deep fetch, capture switches) but no first-class handle concept:
  no registry with owner/latency-bound/evasion-story, no overseer actor
  that *invokes* handles mid-episode, no uptake/landed realization
  records, no handle-integrity scoring.
- Addable post-freeze without breaking pre-registration: handles are
  world/agent mechanics + audit artifacts, not detector changes. The
  freeze-review hooks are exactly the substrate: operation handles =
  registered tools + capabilities; observation handles = tier-gated
  fetches; probe handles = perturbation hooks (stimulus + response
  already share one event stream).
- Natural staging: registry schema + overseer role + 3-4 concrete handles
  (capability-revoke, release-hold, state-freeze, isolate-restart) with
  Phase 7 (escalation needs an overseer actor anyway); drift experiments
  ride on D2 spec upgrades (referent drift = new spec path bypasses the
  step the handle anchors to), persistent state (freeze/erase theater),
  capture (owner drift — lab-sim already has this ahead of embedded-sim),
  and multi-iteration uptake-decay curves.

## Key paths

- `experiments/lab-simulation/lab_sim/{oracle,pipeline_engine,tools,events,world,config}.py`
- `experiments/lab-simulation/tests/{test_monitor_signal,test_host_registry_perturbation}.py`
- `experiments/lab-simulation/DESIGN.md` (open-items section)
