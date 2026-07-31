# 2026-07-02 — Embedded sim: AppD correction-trace schema (roadmap 1)

## Trigger

User: "Converge the correction-trace schema as suggested next step." (Review
roadmap item 1: adopt the Appendix D `bioshield.correction.jsonl` fields —
`pre/post_behavior_hash`, `behavioral_uplift`, `latency_to_effect_ms`,
`reversibility_window_ms` — giving correction events measurable "landed"
semantics instead of leaning on `reported_acceptance`.)

## What was done

1. **`embedded_sim/correction_schema.py` (new).**
   `annotate_correction_events` attaches the AppD fields to every correction
   event (evaluator probe or board request) on the *projected* rows:
   `correction_id`, `corrector_role`, `target_episode_id`, `requested_change`,
   `handle`, `pre_behavior_hash` (hash of visible actions over the 8 steps
   before), `post_behavior_hash` (3-step response window),
   `behavioral_uplift` (agreement-with-request delta post vs pre),
   `latency_to_effect_ms` (first post step matching the request, 100 ms/step;
   `None` = never landed), `reversibility_window_ms` (harm-dependent proxy
   until a bearer/outcome trace exists). All inputs are audit-visible —
   `visible_action`, `intervention_intent`, `correction_request`, `harm` —
   never oracle fields. Helpers: `correction_landed`,
   `acknowledged_not_landed` (the theater witness AppD describes).
2. **Emission** (`world.write_episode_logs`): project → annotate →
   hash-chain, so the signatures cover the annotation fields.
3. **Audit-side recompute** (`embedded_audit.py`): the fields are
   deterministic functions of the visible series, so
   `verify_correction_annotations` recomputes them instead of trusting stored
   values; any mismatch ⇒ `invalid_certificate` ("correction schema" note).
   This is independent of the hash chain.
4. **Red team** (`redteam.py`): new `consistent_forge` strategy that patches
   probe uptake/reports *and* re-runs `annotate_correction_events`, producing
   an internally coherent forged trace. Registered in `STRATEGIES`.
5. **Tests.** `tests/contract/test_correction_schema.py`: fields present on
   events (absent on non-events); landed/theater rates separate honest
   (landed ≈ 1.0, theater ≈ 0) from `capture_theater` (landed −0.2, theater
   ≥ 0.15); recompute flags a naive `visible_action` patch; annotation is
   deterministic. `test_audit_projection.py` updated: naive `full_redteam` is
   now caught **even unsigned** by the schema cross-check; the N-4 unsigned
   false pass requires `consistent_forge`; signed regime catches
   `consistent_forge` via the chain.

## Non-obvious decisions

- Annotation happens **after** projection (oracle fields already stripped) and
  **before** chaining (signatures cover the new fields).
- The recompute cross-check does not cover `reported_acceptance` — that field
  is a *report*, not derivable; per AppD it exists only to expose theater
  (`acknowledged_not_landed`), which behavioral CCI already penalizes.
- The N-4 negative result was **restated, not weakened** (postscript in
  `NEGATIVE_RESULTS.md`): derived consistency fields raise the forgery bar,
  but any deterministic function of forgeable inputs is itself forgeable —
  the unsigned regime still falls to a schema-aware forger, which is the
  argument for the external trust anchor (hash chain / `hardware_tag`).

## Verification

- Full suite: 118 passed (112 prior + 4 schema contract + 2 new forger
  regime tests), `.venv-test`; `smoke_oracle_separation.py` ok.

## Open / next

- Roadmap 2: first-class handle registry (owner, operation, anchor, latency
  bound, evasion story; `handle_invoked` workflow events) — the `handle` field
  currently points at `handle.correction_request` only.
- Roadmap 6 becomes cheap: `latency_to_effect_ms / reversibility_window_ms`
  tempo ratio is now computable per event.
- `reversibility_window_ms` is a proxy; replace when a bearer/outcome trace
  (AppD `bioshield.bearers.jsonl`) exists.
- Suite artifact regeneration still pending (now includes `consistent_forge`).

## Key paths

- `experiments/embedded-simulation/embedded_sim/correction_schema.py`
- `experiments/embedded-simulation/embedded_sim/world.py`,
  `embedded_audit.py`, `redteam.py`
- `experiments/embedded-simulation/tests/contract/test_correction_schema.py`,
  `test_audit_projection.py`
- `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md` (N-4 postscript)
- `appendices/appD-worked-example.tex` §"What is collected"
