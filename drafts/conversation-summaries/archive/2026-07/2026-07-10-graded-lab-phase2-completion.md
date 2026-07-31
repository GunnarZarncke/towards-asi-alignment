# 2026-07-10 — Graded lab Phase 2 completion (resource/cost substrate + scheduler)

## Trigger

User: "OK. continue with the next phase." (following the Phase 0–1 review +
bug-fix session earlier the same day).

## Done

Closed out Phase 2's deliverables and freeze gate exactly as scoped in
`PLAN.md` (ledger + scheduler + pay-to-observe projector, unit-tested; **no
episode loop** — explicitly deferred, see Decisions):

- **Fixed the standing-recovery bug** flagged-but-deferred in the prior
  session's G-1: `ResourceLedger.reset_tick_windows` read a
  `standing_recovery` key that never existed on
  `resource_allowances_per_tick[role]` (silently always 0.0). Now sourced
  from the frozen `standing_mechanics.recovery_per_idle_tick`, gated on a
  genuine per-window idle check via a new
  `ActorResources.standing_spent_this_window` field.
- **Made scheduler contention genuinely emergent.**
  `ActionScheduler.start()` no longer takes `queue_depth` as an external
  argument (a de facto delay-parameter risk); it now derives it internally
  from `len(self._in_flight)`, exposed as a `queue_depth` property.
  `duration_ticks()` stays a pure function with an explicit parameter for
  isolated formula tests.
- **Removed a second dead field**, `ResourceLedger.shared_queue_depth`
  (never written anywhere, same pattern as the prior session's dead
  `safety_effort` finding).
- **Added the pay-to-observe projector**
  (`graded_lab/world_visible/observation.py`, `ObservationProjector`): an
  actor's projection contains only artifacts it has explicitly
  `record_read` — no `observability` fraction, no cross-actor leakage.
- `CODE_VERSION` bumped `0.1.0` → `0.2.0` per `DESIGN.md`'s own rule
  (resource ledger/scheduler mechanics changed).
- 9 new tests (39 total, was 30); `results/FINDINGS.md` G-2 documents all
  of the above plus two items deliberately not built this pass.
- `README.md`/`PLAN.md`/`DESIGN.md` status lines updated to Phase 0–2.

## Decisions

- **Scoped Phase 2 to exclude the episode loop.** `PLAN.md`'s own
  "Immediate next steps" (step 5) explicitly says implement ledger/
  scheduler/projector "with unit tests... no episodes yet"; step 6 ("Only
  then: primitive-action optimizer policy + subprocess isolates") is where
  a multi-actor tick loop first has an agent policy to drive it. Building
  an orchestrator now would mean guessing at Phase 3's interface before it
  exists — deferred rather than improvised.
- **Left `broad_access_request_cost` / `unused_grant_penalty` /
  `admin_queue_penalty_threshold` unwired.** These are access-request
  costs tied to a `call(endpoint="access.request")` handler and
  `AdminPolicy`, neither of which exist as code yet (Phase 3 roster item,
  not Phase 2 resource-ledger scope).
- Verified with the same throwaway venv from the prior session
  (`/tmp/graded_lab_venv`, `pytest`) since the repo's default Python lacks
  `pytest`.

## Open / next

- Phase 3: affordable-primitive host API, optimizer `policy.py`, isolates
  (Mock/Subprocess equivalence), and — now that ledger/scheduler/projector
  all exist — the first real episode loop that couples them (`record_read`
  / `start()` only after `ResourceLedger` confirms affordability).
- Phase 2's hazard-ceiling constants from the prior session
  (`_REVIEW_HAZARD_CEILING`, `_COMPLIANCE_HAZARD_CEILING`) still await a
  written mechanics-derivation before Phase 5 freeze.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/world_visible/resource_ledger.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/scheduler.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/observation.py` (new)
- `experiments/graded-lab-simulation/results/FINDINGS.md` (G-2)

## Commits

- None (user did not request a commit this session).
