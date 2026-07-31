# 2026-07-13 — Graded lab Phase 7b: UAD-backed ecology-BIQ

## Trigger

Continuation of the same day's Phase 7a session ("continue with the next
phase"). Phase 7a (UAD + intervention trace validation) was already
committed; `PLAN.md` names Phase 7b (UAD-backed ecology-BIQ: discrete
MI/CMI, intervention-supported control, declared retained-state proxy,
held-out surprise, all over UAD-**inferred** units) as next.

## Done

- Pre-registered the Phase 7b estimator choices in `DESIGN.md` ("Phase 7b
  UAD-backed ecology-BIQ") **before** writing code: K-event reuse from
  the Phase-4 diagnostic list, a generic held-out plug-in MI/NLL
  estimator (add-1 smoothed, 60/40 tick-ordered train/test split, no
  external estimator library), a 5-seed intervention-supported control
  battery, an audit-accessible memory proxy, and `alpha=beta=gamma=1.0`.
- Implemented `graded_lab/oracle_only/unit_biq.py`:
  - `held_out_bits(...)` — generic discrete estimator, `mode="reduction"`
    (held-out bits saved by conditioning, an MI proxy) or `mode="nll"`
    (raw held-out NLL, for the surprise term).
  - `unit_prediction_bits` (`I_pred`, per K-event, on the unit's combined
    action-code signature).
  - `unit_control_bits` (`I_ctrl`, freezes every unit member to `noop`
    across a 5-seed battery, MI against a discretized `(deploy_count,
    bearer_harm)` outcome bucket).
  - `unit_memory_bits` (`H_mem`, `log2(1 + distinct paid-read artifact
    paths)` from the host-tracked `ObservationProjector` output).
  - `unit_self_surprise_bits` (`S_surp`, held-out NLL of the unit's own
    next action-code given its own previous code).
  - `unit_field_incident_bits` (across-seed battery statistic, `None` for
    single-episode calls) and `unit_ecology_biq` (composite report,
    every component always reported alongside `K_biq`).
- Added `tests/test_unit_biq.py` (10 tests: 4 estimator-mechanics tests
  on synthetic data, 2 `H_mem` unit tests, 2 `committee`-ecology
  integration tests for `I_pred`/`S_surp`, 2 `@pytest.mark.slow`
  end-to-end tests for `I_ctrl` and the full composite shape).
- Raised `tests/speed_limits.json` `suite_max_seconds` `165.0 → 190.0`,
  added per-test caps for the two new slow tests, and refreshed
  `tests/speed_baseline.json` (`--update-speed-baseline`). Full suite:
  134 tests, ~160–166s, green.
- Bumped `CODE_VERSION` `graded-lab-0.9.0 → 0.10.0`
  (`world_visible/config.py`, `tests/test_config.py`).
- Added `results/FINDINGS.md` G-13 documenting what worked and a genuine
  negative/confounding result (see Decisions).
- Updated `PLAN.md`/`README.md` status lines and phase tables to mark
  7b done, 7c not started.

## Decisions

- The user was asked (via the question tool, since the four-component
  build is substantial) whether to build a minimal `I_pred`+`I_ctrl`
  slice first or the full composite in one pass, and explicitly chose
  the **full composite** — all four terms were implemented together.
- Reused the Phase-4 K-event list (`next_primitive_denied`,
  `review_token_within_10_ticks`, `deploy_succeeds_within_40_ticks`,
  `field_incident_rate_above_median`) rather than re-picking one, per
  `PLAN.md`'s instruction that the list is fixed before this phase.
- `field_incident_rate_above_median` genuinely needs ≥2 episodes to
  define a median; single-episode calls report `None` rather than a
  fabricated n=1 statistic.
- **`I_ctrl` has a documented resource-contention confound**, found
  while validating rather than assumed: at seeds where `deploy_count`
  is nonzero, freezing the task-critical `eng1` *and* freezing the
  unrelated `admin1` **both** collapse deploy to 0 on `default_lab_config`
  — because removing any actor changes shared compute/model-slot
  contention for everyone else (echoes the `shared_model_id`/
  `three_way_nod` bystander-coupling finding from the same day's Phase
  7a-blind battery, G-12). `I_ctrl` as specified cannot yet separate
  "this unit is the task driver" from "this unit's removal changed
  contention for everyone." Left as a documented Phase 7c limitation
  (a contention-matched counterfactual would need its own
  pre-registration), not silently patched by redefining the term.
- At baseline substrate settings `deploy_count` is nonzero on roughly
  1-in-20 seeds, so with the default 5-seed control battery `I_ctrl` is
  frequently exactly `0.0` — reported as an honest absence of signal at
  this battery size, not an estimator bug; Phase 7c's wider substrate
  sweep is where this should resolve.
- Deliberately not attempted this pass (documented, not silently
  dropped): a bias-corrected MI estimator (Miller–Madow/NSB), a
  contention-matched control counterfactual, and cross-episode
  aggregation of `field_incident_rate_above_median` beyond a fixed
  battery.

## Follow-up: `I_ctrl`'s outcome vector was task-scoped — reframed and fixed

The user pushed back on the G-13 "resource-contention confound" being
framed as a limitation: an agent's control over shared resources *is*
real control, and should be measured, not treated as noise to eliminate.
Tracing this against Chapter 11's actual definition
(`I_{\mathrm{ctrl}}^X = \MI(\mathrm{do}(A^X_t); E^X_{t+1})`, over the
*full future external state*, chosen specifically to avoid importing a
task ontology) confirmed the user was right: the implementation's
outcome vector — `(deploy_count, bearer_harm)` alone, inherited from the
pre-existing Phase-4 diagnostic's `DEPLOY_CAP`/`HARM_CAP` constants for
convenience — silently reintroduced exactly the task-ontology dependence
Chapter 11 is designed to avoid, and `PLAN.md`'s own Phase 7b sketch
(naming a wider example vector) was under-realized.

- **Fixed:** widened `Y` to a 4-component discretized state
  `(deploy_bucket, harm_bucket, review_pass_bucket, contention_bucket)`,
  where `contention_bucket` counts denied primitives among actors
  outside the unit. Verified this distinguishes `frozen_eng1` from
  `frozen_admin1` at the G-13 seed (previously identical), while deploy/
  harm still collapse identically for both. Regression test added.
- **Checked `I_pred` for the same mistake:** found a smaller, distinct,
  *unresolved* concern (the 3 per-tick K events are boundary-relative
  but still arguably task-flavored, e.g. `deploy_succeeds`), but did
  **not** change them — they are the Phase-0/Phase-4 pre-registered,
  reused-verbatim K-event list, and re-picking them on suspicion alone
  (with no demonstrated confound, unlike `I_ctrl`) would violate this
  session's own freeze commitment. Logged as an open Phase 7c
  pre-registration question instead.
- Documented in `results/FINDINGS.md` G-14, `DESIGN.md` Phase 7b section
  updated in place, `CODE_VERSION` `0.10.0 → 0.11.0`. Full suite: 135
  tests, ~175s (still within the 190s cap), baseline refreshed.

## Open / next

- Phase 7c: ecology calibration battery (substrate-setting sweep ×
  `{programmatic_softmax, programmatic_2step, optional_llm_weak}` × 10
  seeds → measured EAI ~0.05–0.80), with the 4 pre-registered pass
  criteria in `PLAN.md` "Phase 7c calibration battery." This is the
  first place `I_ctrl`'s low-deploy-rate weak-signal issue and the
  resource-contention confound get real stress-tested across a wider
  substrate grid.
- Consider (Phase 7c-adjacent, needs its own pre-registration first): a
  contention-matched counterfactual for `I_ctrl` — e.g. replace the
  frozen unit with a resource-neutral stand-in that still "occupies" its
  contention footprint, rather than `noop`. Now partially superseded by
  the `Y`-widening fix above, but a matched-counterfactual layer would
  still be a cleaner causal design than a wider outcome vector alone.
- Open question registered for Phase 7c: is `I_pred`'s K-event list
  (`next_primitive_denied`/`review_token`/`deploy_succeeds`) still too
  task-scoped relative to Chapter 11's `S^X_{t+1}` (the unit's own
  future sensory stream)? Not resolved this session — no demonstrated
  confound, left frozen per the "reused verbatim" commitment.
- Chapter 11 also specifies a separate, declared attention/harm-
  weighting layer composed *on top of* the task-agnostic `K_X` for
  risk-relevant composites (not folded into the base measure) — not
  implemented; a candidate Phase 7c/8 backlog item if a harm-weighted
  composite is ever needed.

## Key paths

- `experiments/graded-lab-simulation/DESIGN.md` — "Phase 7b UAD-backed
  ecology-BIQ" pre-registration.
- `experiments/graded-lab-simulation/graded_lab/oracle_only/unit_biq.py`
  — the new estimator module.
- `experiments/graded-lab-simulation/tests/test_unit_biq.py`
- `experiments/graded-lab-simulation/results/FINDINGS.md` G-13
- `experiments/graded-lab-simulation/PLAN.md` (Phase 7c spec, next)

## Commits

- `d8ab097` Complete graded-lab Phase 7b: UAD-backed ecology-BIQ and I_ctrl fix.
