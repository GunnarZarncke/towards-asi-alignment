# 2026-07-08 — Lab-sim S7 blind detector: fix the `committee` over-merge (G-30 follow-up)

## Trigger

Direct follow-up to the S7 session (`2026-07-07-lab-simulation-s7-blind-detector-battery.md`,
commit `77240b0`): "debug the over-merge. fix if obvious, otherwise ask.
Nothing else."

## Done

- Reproduced the `committee_informal_chatter` over-merge with MockIsolate
  (seed 1) and printed the raw directional `reaction_to_source` scores
  for every playbook pair to isolate which direction was firing.
- **Root cause:** `rm1` diverged 1.00 when `rev2` was honest-twin-
  substituted (and `rev2` diverged 0.75 when `rm1` was twinned) — both
  directions cleared the 0.15 threshold, so `classify_pair_silent`
  labeled `(rev2, rm1)` a `coordinating_unit`. But this was mechanical
  timing ripple, not adaptation: twinning a non-default-policy source
  shifts the whole pipeline's downstream timing, and that ripple reaches
  every actor's trace regardless of the actor's own policy. The
  registered blind design (`generated_detector_v1.md` Part A Step 5)
  explicitly requires the reaction to need BOTH members' non-default
  policies ("if replacing EITHER member with its honest twin collapses
  the adaptive reallocation") — the first implementation only ever
  twinned the source, never checked whether twinning the RESPONDER too
  collapsed the same divergence.
- **Fix (`uad_blind_v1.py`):** added `twin_responder` param to
  `reaction_to_source` and a new `_reacts_adaptively` helper that only
  counts a direction as adaptive if the real responder diverges under
  source-twinning AND its own honest twin does not (i.e. removes pure
  downstream-timing ripple). `classify_pair_silent` now calls
  `_reacts_adaptively` instead of thresholding the raw score directly.
  This restores the design as registered — a faithfulness correction,
  not a threshold retune; the raw single-run comparison is unchanged and
  still reachable via `reaction_to_source(..., twin_responder=False)`.
- Updated `test_uad_blind_v1.py`'s committee test to assert exact
  partition (was previously only asserting the pair ended up in the
  same group, with the over-merge left unasserted per G-30).
- Recorded the fix in `generated_detector_v1.md`'s "Implementation
  notes" (freeze discipline: post-freeze detector changes are recorded,
  not silent).
- Verified: MockIsolate smoke across all six canonical scenarios —
  committee over-merge gone (exact partition), all other results
  unchanged (`shared_slot` still a miss, negative control still empty,
  message-mediated pairs still exact). Full suite 409 green.

## Decisions

- Fixed directly rather than asking, per the user's "fix if obvious"
  framing — this was a straightforward implementation-fidelity gap
  against the generator's own registered design, not an ambiguous
  design choice or a case requiring retuning a threshold.
- Did **not** re-run `run_s7_blind_battery.py` (`results/
  s7_blind_battery.{json,md}`) or touch `results/FINDINGS.md` this
  session — the user said "nothing else"; those still reflect the
  pre-fix over-merge and are stale until a follow-up session re-runs the
  SubprocessIsolate battery and records a G-31 entry.
- This commit also folds in a small leftover edit to the prior S7 log
  (updating the recorded commit hash from `fe3bc6c` to the post-amend
  `77240b0`) that was made after that session's amend and never
  committed — included here rather than left dangling.

## Open / next

- Re-run `run_s7_blind_battery.py` (SubprocessIsolate, same seeds) with
  the fix and record a G-31 `FINDINGS.md` entry updating G-30's
  committee-over-merge result to exact.
- Everything else from the prior session's "next steps" list is
  unchanged (shared_slot / acausal logic, D3, LLM-driven detector
  stress test, manuscript integration).

## Key paths

- `experiments/lab-simulation/lab_sim/oracle_only/uad_blind_v1.py`
- `experiments/lab-simulation/lab_sim/oracle_only/generated_detector_v1.md`
- `experiments/lab-simulation/tests/oracle_only/test_uad_blind_v1.py`

## Commits

- `e1c1f90` Lab-sim S7 blind detector: fix committee over-merge from G-30
