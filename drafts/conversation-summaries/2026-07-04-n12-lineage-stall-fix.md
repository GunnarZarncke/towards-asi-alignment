# 2026-07-04 — N-12 `legitimacy_theater` lineage-stall detector fix

## Trigger

Follow-up to 2026-07-03 Milestone v5 Phase 0, which discovered N-12: the
`legitimacy_theater` scenario's structural detector had a ~25% false-pass
rate even at full instrumentation, flat across all instrumentation levels.
User asked "what is your guess as to the issue?", then, after a root-cause
walkthrough, suggested the fix direction: "we need either longer horizons
aka more samples, event-based analysis or bayesian evidence."

## Done

- Root-caused N-12 to **two independent problems** in
  `lineage_stall_reported_uptake` (`embedded_sim/audit_core/structural_signals.py`):
  1. **Off-by-one bug.** `t=0` is always an eligible probe step (the
     intervention schedule always considers it as a candidate), and was
     correctly excluded from the stall-count *numerator* (no valid `t-1`
     predecessor — Python would otherwise silently wrap to `lineage[-1]`)
     but was still counted in the *denominator*. This capped the
     achievable `stall_frac` at `(n-1)/n` regardless of how consistently
     the mechanism actually stalls — verified live: every non-`t=0` probe
     step in all 8 diagnostic seeds showed a perfect stall, yet the old
     fraction read 0.75-0.889 against a 0.85 threshold.
  2. **Miscalibrated fixed-fraction threshold at small n.** This scenario
     produces only 3-9 probe steps per 400-step episode by construction. A
     raw fraction against a fixed threshold is statistically fragile at
     that n (8/9=0.889 clears 0.85, 4/5=0.80 doesn't, despite 5 trials
     being much weaker evidence than 9).
- Fixed (1) directly (denominator now matches numerator's eligible set).
- Fixed (2) per the user's explicit direction: replaced the raw-fraction
  test with a one-sided **Wilson score lower bound** (added
  `_wilson_lower_bound()`, stdlib-only via `statistics.NormalDist` — no
  scipy in this codebase, as a substitute for the exact Jeffreys/Beta
  interval) at **80% confidence** against a round **0.70** target rate:
  "are we 80% confident the true stall rate exceeds 70%?" instead of "does
  the raw fraction already clear 85%?". Confidence level and target were
  fixed as round, conventional numbers *before* checking which seeds they
  flip (AGENTS.md: "conclusions never named before being derived").
  Deliberately did *not* pursue the "longer horizons" option (increasing
  `intervention_interval`/`intervention_prob` density for this scenario)
  since it would touch the shared `SimConfig` defaults, force another full
  re-measurement of N-10/MI-scan numbers, and expand scope beyond what a
  same-session fix should carry — left as a documented alternative.
- Verified safety from new false positives: `lineage_stall_under_intervention`
  is exclusive to `legitimacy_theater` — checked directly that every other
  scenario's lineage increments on essentially every probe step by
  construction, so this detector's raw stall fraction is ~0 regardless of
  the new methodology (pinned as a test).
- Added `tests/unit/test_lineage_stall_detector.py` (9 tests): Wilson-bound
  sanity properties, regression pins for the 4 seeds now correctly
  detected, regression pins for the 2 seeds where the *separate* residual
  gap remains open (not silently absorbed), a correct-rate floor, and a
  no-new-false-positives check across 5 other scenarios.
- Re-ran the full 6-level x 17-scenario x 8-seed eligibility battery
  (`eval_channel_eligibility.py`, ~34 min) to regenerate
  `results/channel_eligibility_eval.json` with the fix. Confirmed exactly
  the predicted effect: `legitimacy_theater` correct rate 0.25 → 0.625 at
  `medium_minus`/`medium`/`strong_handles`; false-pass rate unchanged at
  0.25 (all other scenarios' aggregate false-pass/honest-pass numbers
  reproduced bit-for-bit, confirming the detector is scenario-exclusive as
  expected).
- Full test suite: 241 passed, 1 skipped (was 232 passed before the new
  file).
- Updated `results/NEGATIVE_RESULTS.md` N-12 with a full postscript (root
  cause, fix, what's still open) and `MILESTONE-v5-goal-agents.md`'s Phase
  0 task entry with a condensed version.

## Decisions

- Fixed the off-by-one unconditionally (a correctness bug, not a
  calibration choice) but treated the threshold-methodology change as a
  genuine design decision requiring pre-registered, round parameters
  (0.80 confidence / 0.70 target) rather than values reverse-fit to flip
  specific seeds — consistent with the project's explicit anti-pattern
  rule about baking conclusions into definitions.
- Left the `mean_rep >= max(0.52, cert.raw_capacity + 0.05)` condition
  (which still blocks seeds 11/16) untouched this session — it's a
  separate calibration question (apparently tuned against other, honest
  scenarios to avoid false-triggering there) that deserves its own
  investigation, not an opportunistic same-session tweak riding on the
  stall-frac fix. This is now explicitly tracked as the open remainder of
  N-12, not silently merged into "fixed."
- Did not touch scenario mechanics (`intervention_interval`/`prob`) to
  avoid re-triggering a second full N-10/MI-scan re-measurement cycle in
  the same session; noted as a valid complementary alternative if the
  residual mean_rep gap turns out to also be an n-starvation artifact.

## Open / next

- **N-12 partially open:** seeds 11/16 still false-pass via the
  `mean_rep`/`raw_capacity` condition. Needs its own investigation before
  touching (why was `+0.05` chosen; what would break in other scenarios if
  loosened).
- Part C (writer attestation on `handle.hardware_tag`, N-9) — still not
  started, is the next item in the original Part A/B/C plan.
- `MILESTONE-v5-goal-agents.md` Phase 1+ (goal-driven agent MVP) is next
  in the plan's own ordering once Part C and any remaining Phase 0
  follow-ups are closed.
- Recorded TODOs from the prior session remain open: adversarial-setup
  implications of MI-scan-as-discovery, no stability check on the
  exploration/validation seed split itself, `alias_stress`/`decoy_stress`
  capping at 0.875 honest-pass.

## Key paths

- `embedded_sim/audit_core/structural_signals.py` —
  `lineage_stall_reported_uptake`, `_wilson_lower_bound`.
- `tests/unit/test_lineage_stall_detector.py` — new regression tests.
- `results/NEGATIVE_RESULTS.md` — N-12 postscript with full derivation.
- `results/channel_eligibility_eval.json` — regenerated with the fix.
- `MILESTONE-v5-goal-agents.md` — Phase 0 task entry, condensed update.

## Commits

- `0f948e5` Wire in held-out scenarios (Phase 0) and fix N-12 lineage-stall
  detector (bundled with the 2026-07-03 Phase 0 commit in the same
  session-end commit; result artifacts were regenerated once, after this
  fix, so an intermediate Phase-0-only artifact state was not preserved).
