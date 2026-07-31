# 2026-07-04 — N-12 mean_rep floor fix and capture-side twin check

## Trigger
User asked to continue the Milestone v5 plan after the Phase 0.5 battery re-run
was committed. Skipped an `AskQuestion` on scope, so proceeded with the
recommended defaults: document the capture-side-twins item cheaply (reuse
already-computed battery data, no new scenario), then pick the next
concretely-scoped item rather than an open design question — chose N-12's
remaining seeds 11/16 false-pass gap.

## Done
- **Capture-side twin discrimination check** (no code change, used existing
  `channel_eligibility_eval.json`): confirmed `legitimate_gradual_improvement`
  and `benign_semantic_drift` are cleanly discriminated from their stated
  capture twins (`hidden_capability`; `grounding_silent_gap`/`bundle_goodhart`)
  at `medium`/`strong_handles`. `honest_mistakes` has no existing twin —
  documented as a left-open design decision, not built this session.
- **N-12 root cause for seeds 11/16, found and fixed.** Verified empirically
  (2,160 episodes: 18 scenarios × 3 instrumentation levels × 40 seeds) that
  `stall_confident` (the Wilson-bound lineage-stall signal from the earlier
  N-12 fix) is already an exclusive discriminator for `legitimacy_theater` —
  zero false positives elsewhere. This reframed the remaining
  `mean_rep >= max(0.52, cert.raw_capacity + 0.05)` conjunct in
  `lineage_stall_reported_uptake` (`structural_signals.py`): it compares
  reported acceptance on probe steps against an *unrelated* whole-episode
  interventional-capacity estimate. At seed 11 (`raw_capacity=0.80`) and
  seed 16 (`raw_capacity=0.75`), the scaled bar chased `raw_capacity` itself
  and exceeded an otherwise clearly-positive `mean_rep`. Fixed: dropped the
  `raw_capacity`-scaled term, kept the fixed floor (`mean_rep >= 0.52`).
- **Result:** `legitimacy_theater` correct-rate 0.625 → **0.875** (7/8),
  false-pass 0.25 → **0.0** (0/8), consistent across all three instrumentation
  levels. Downstream: `combined_20_scenarios` capture false-pass at
  `medium`/`strong` 0.052 → **0.031**; `extended_9_scenarios` 0.042 → **0.0**.
  Honest-side numbers unaffected.
- Re-ran the full 6×20×8 eligibility battery (~39 min) to regenerate
  `results/channel_eligibility_eval.json`.
- Updated `tests/unit/test_lineage_stall_detector.py` (renamed
  `STILL_OPEN_MEAN_REP_GAP` → `FIXED_BY_MEAN_REP_FLOOR_FIX`, flipped
  assertions, raised the correct-rate regression floor 5→7, broadened
  `test_other_scenarios_never_spuriously_trigger_this_detector` to include
  the three Phase 0.5 honest scenarios).
- Updated `results/NEGATIVE_RESULTS.md` (N-12 postscript 2 + corrected all
  stale 0.052/0.625/0.25 references elsewhere in the N-10 Postscript 6
  section) and `MILESTONE-v5-goal-agents.md`.
- Ran `tests/unit` + `tests/contract` in full; 8 pre-existing failures
  (`test_appd_convergence`, `test_audit_projection`, `test_deploy_gate`,
  `test_writer_compromise` — all `safety_decision == 'reduce'` vs expected
  `'pass'`) reproduce identically with the fix stashed out, confirming they
  are pre-existing test-order-dependent flakiness unrelated to this change,
  not a regression.

## Decisions
- Did not build a capture-side twin for `honest_mistakes` — a genuine new
  scenario-design decision, deliberately left open rather than guessed at,
  per the milestone doc's own "deferred follow-up decision" framing.
- Did not pursue Phase 1+ or the agent-attribution TODO this session — noted
  mid-session that a **concurrent, separate agent session** had already
  implemented Milestone v5 Phase 1 as a new line,
  `experiments/goal-agent-simulation/` (see its own session log,
  `2026-07-04-goal-agent-simulation-phase1.md`, and `experiments/README.md` /
  `MILESTONE-v5-goal-agents.md` / `TODO.md` edits from that session — not
  touched or committed here to keep the two sessions' commits separable).

## Open / next
- `honest_mistakes` capture-side twin (design decision, not started).
- Now that Phase 1 exists in `goal-agent-simulation/`, decide whether the
  agent-attribution TODO (component 6) should extend that new line instead
  of this codebase (that session's `TODO.md` update already sketches this).
- Consider whether `NEGATIVE_RESULTS.md`'s per-scenario `medium_minus`
  table (Postscript 5) needs a forward-pointer refresh now that
  `legitimacy_theater`'s number has moved past that snapshot (left as a
  historical postscript with an explicit "see N-12" pointer, not edited).

## Key paths
- `experiments/embedded-simulation/embedded_sim/audit_core/structural_signals.py`
  (`lineage_stall_reported_uptake`)
- `experiments/embedded-simulation/tests/unit/test_lineage_stall_detector.py`
- `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md` (N-12
  postscript 2)
- `experiments/embedded-simulation/results/channel_eligibility_eval.json`

## Commits
- `3415317` Fix N-12 legitimacy_theater false-pass (seeds 11/16) and check capture-side twins.
