# 2026-07-10 — Graded lab Phase 0–1 review + bug fixes

## Trigger

User: "review the work that has been done in this new experiment against
the PLAN" (`experiments/graded-lab-simulation`), then: "Address the
findings (implement or comment if you disagree)."

## Done

Read-only review against `PLAN.md`/`DESIGN.md`, cross-checked with a
background subagent, then fixed the confirmed bugs:

- **Fixed inverted review/compliance polarity** in
  `graded_lab/world_visible/pipeline_engine.py`: `_effect_peer_review`
  passed on *high* hazard (`last_eval_mean > 0.45`) instead of low; swapped
  the two steps' numeric roles (`_REVIEW_HAZARD_CEILING=0.72` looser,
  `_COMPLIANCE_HAZARD_CEILING=0.45` stricter) so the intended "review
  passes, compliance blocks" ambiguous band lands on the correct (safe) side
  of hazard.
- **Fixed boolean-in-disguise `field_monitor` incident rate** in
  `graded_lab/oracle_only/oracle.py`: `tick()` now records every draw per
  model (`ModelArtifact.incident_ticks`, including zeros, not just positive
  incidents pooled globally); `field_monitor_sample` windows per model.
- **Wired the dead `safety_effort` build param** into
  `graded_lab/oracle_only/populations.draw_hazard_regions` via a
  `safety_scale` that shrinks Beta `alpha` (lower mean hazard), fixed before
  Phase 3 agents exist to exploit a no-op lever.
- **Added Tier-K `provenance` to `tier_k_snapshot()`/`world_digest()`**
  (DESIGN.md lists lineage as Tier-K; it was recorded but excluded).
- **Scheduler duration now uses `math.ceil`** (matches `DESIGN.md` decision
  #3, was `round`); updated `DESIGN.md` to state the IO half-weight term
  explicitly instead of diverging silently from its own pinned formula.
- **Episode cache key now hashes substrate content**, not just
  `substrate_version` + path (`graded_lab/harness/cache.py`).
- **Extended substrate structural validation** to cover
  `standing_mechanics`/`contention`/`eval_sampling`/`field_monitor_sampling`
  and per-role allowance sub-keys.
- Re-pinned `test_world_digest_pinned_seed_42` (safety_effort + provenance
  both move the digest); added 12 new regression tests (30 tests green, was
  18) covering all fixes plus `test_release_and_deploy_denied_without_both_tokens`.
- `results/FINDINGS.md` G-1 entry documents each fix and three items
  deliberately left unchanged with reasoning (see below); `README.md` phase
  table updated.

## Decisions

- **Disagreed with (did not implement) three review suggestions:**
  1. Direct deploy-time token re-check — already structurally guaranteed by
     `deploy`'s DAG `depends_on: [release_candidate]`, since a failed
     `release_candidate` (raises `_StepAbort`) is never added to
     `_completed`. Added a regression test instead of redundant code.
  2. Making `compliance_signoff` stochastic too — PLAN's ambiguous-band rule
     only requires *some* review/compliance gap, and ambiguity already comes
     from peer_review's own band plus `last_eval_mean` being a noisy finite
     sample; a second coin flip would be an unmotivated extra knob (against
     the PLAN's own emergent-ambiguity principle).
  3. Wiring `standing_mechanics` into `ResourceLedger` now — no episode loop
     exists yet to call `reset_tick_windows`; deciding how
     `broad_access_request_cost`/`unused_grant_penalty`/
     `admin_queue_penalty_threshold` are consumed is real Phase 2 design
     work, left as an open Phase 2 item rather than guessed at.
- Re-pinning the Phase 1 digest was judged acceptable (not a freeze
  violation) because `PLAN.md`/`README.md` both explicitly mark Phase 1 as
  "in progress," not frozen.
- Verified everything with a local venv (`/tmp/graded_lab_venv`, `pytest`)
  since the repo's default Python lacks `pytest`; no repo file changes for
  this (venv is outside the repo).

## Open / next

- Phase 2 (episode loop, pay-to-observe projector, `standing_mechanics`
  wiring) still not started.
- Phase 1 pipeline semantics still use hand-picked hazard-ceiling constants
  (`_REVIEW_HAZARD_CEILING`, `_COMPLIANCE_HAZARD_CEILING`) — PLAN's Phase 5
  freeze gate requires a written derivation from mechanics before these are
  load-bearing for any battery.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/world_visible/pipeline_engine.py`
- `experiments/graded-lab-simulation/graded_lab/oracle_only/oracle.py`
- `experiments/graded-lab-simulation/graded_lab/oracle_only/populations.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/scheduler.py`
- `experiments/graded-lab-simulation/graded_lab/harness/cache.py`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (G-1)
- `experiments/graded-lab-simulation/DESIGN.md`

## Commits

- None (user did not request a commit this session).
