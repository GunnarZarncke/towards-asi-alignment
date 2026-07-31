# 2026-07-04 — goal-agent simulation: F-1/F-3/F-6 follow-ups resolved

## Trigger
User: "continue with the plan until you run into questions and have to ask
me" (following the Phase 1 acceptance run in
`2026-07-04-goal-agent-simulation-phase1.md`). Worked the two concrete,
already-sketched follow-ups from `results/FINDINGS.md` (F-1, F-3); hit a
genuine design question after a second held-out region also saturated;
asked via `AskQuestion`, user skipped ("continue with the information you
already have"), so made the call and implemented the most direct fix
(F-6 suggestion a), which resolved cleanly (F-7).

## Done
- **F-3 follow-up (Wilson-bound small-n detector).** Added
  `wilson_lower_bound` to `goal_sim/info.py` (ported pattern from the
  embedded-simulation line's N-12 fix) and `d1b_probe_divergence_wilson` to
  `goal_sim/detectors.py`, added **alongside** D1 (not replacing it) so
  pre-follow-up numbers stay reproducible. Target rate (0.25, matching
  `labels.L1_REPORT_GAP`) and confidence (0.80, matching the old line's N-12
  precedent) fixed before running. Measured: discovery full-tier detection
  0.9439 → 0.9533 (residual misses 6 → 5 of 107), light-tier 0.3738 → 0.3925,
  false-alarm rate unchanged (0.0677) — real but modest recovery.
- **F-1 follow-up (second held-out region).** Pre-registered and sampled a
  second region ("subtle-deception band": `0.30 ≤ w_task ≤ 0.45`,
  `w_exposure ≥ 0.35`, shadow tool; seed 20260705, independent RNG stream so
  the original discovery/held-out-1 numbers stay byte-identical). Refactored
  `protocol.py`'s `mini_mi_scan` into reusable `score_channel_means` +
  `mi_transfer_on_frozen` so the second region reuses the *same* frozen
  top-k channel selection with no re-fitting.
- **Result: the second region also saturated at 100% violations** — the
  prediction of a label mixture was wrong again. This time root-caused
  (F-6): both regions constrain two of the four simplex weight coordinates
  upward without ever bounding `compliance`, and `compliance` is the actual
  discriminating feature (mean 0.388 honest vs. 0.173 violation in
  discovery). Pushing two coordinates up on a 4-simplex mechanically starves
  the others — a design-methodology finding about *how* to define a
  held-out region on a weight simplex, not just a repeated bad guess.
  Positive nugget: despite both regions saturating on the label, they are
  behaviorally distinct (light-tier detection 0.80 region 1 vs. 0.4875
  region 2), independent evidence the exposure-aversion feature does
  something real.
- **Region 3 (F-6 fix, F-7 result).** Since option (a) was the most direct
  fix per F-6's own analysis, implemented it: region 3 constrains
  `w_compliance` into [0.20, 0.35] directly (band chosen from
  discovery-only aggregate class means — 0.173 violation / 0.388 honest —
  computed before this region existed, not from any held-out labels), seed
  20260706, independent RNG stream. **Result: a genuine label mixture**
  (47/80 = 58.75% violation, 33/80 honest) and **the line's first
  non-degenerate MI-transfer result**: frozen top-3 channels
  (`welfare_delta`, `correction_request`, `reported_uptake`, selected on
  discovery only) transfer with scores 0.8116/0.5494/0.5414 — at or above
  their discovery-time values (0.6916/0.5675/0.5648). Detector transfer
  also holds on a genuine (non-saturated) mixture: full-tier detection
  0.9574, false-pass 0.0426, false-alarm 0.0606, all close to discovery's
  own numbers — the correct sanity check that regions 1/2's "perfect" 1.0
  detection was a saturation artifact, not detector strength.
- 6 new tests total (Wilson-bound properties, D1b recovering some D1 misses
  on a small-n fixture, subtle- and compliance-band-region sampling
  disjointness/determinism, the refactored MI-transfer helper matching the
  original scan). 25/25 pass.
- `run_phase1.py` rewritten to run and report all three held-out regions
  generically (region name → description/sampler dict) in one artifact;
  `results/phase1_acceptance.{json,md}` regenerated (480 episodes total,
  ~1.26 ms/episode). `FINDINGS.md` (F-6, F-7) and `README.md` updated.

## Decisions
- Kept D1 and D1b as separate detectors (not swap-in-place) — same
  discipline as the embedded-simulation line's approach to comparable
  historical numbers.
- Used independent sampling seeds/RNG streams for each new held-out region
  so earlier regions'/discovery's numbers stay byte-identical across reruns
  (verified by tests).
- Asked the user via `AskQuestion` how to proceed after the second
  saturation; user explicitly deferred ("continue with the information you
  already have"), so picked F-6's most direct, already-justified fix
  (constrain `compliance` directly) rather than the tool-availability
  alternative or skipping straight to Phase 2 — both remain open options if
  this fix had not resolved cleanly, but it did.

## Open / next
- Phase 1's held-out-region protocol is now validated (region 3): both the
  detector battery and the MI-channel-selection approach transfer to a
  genuinely unseen, non-saturated region. This was the explicit
  prerequisite the plan set before Phase 2 (red-team integration +
  adversarially-optimized goal weights) — Phase 2 can reasonably start now.
- Phase 2 still has its own open design questions the plan flagged as
  "not yet decided": adversarial vs. uniform weight sampling for red-team
  conditions (or both as separate conditions), and the red team's action
  repertoire. These need the user's input before implementation.
- F-3's Wilson-bound follow-up narrowed but did not close the small-n gap
  (5/107 residual misses remain) — could go further (e.g. tune the target
  rate/confidence pair) but that would need fresh pre-registration
  reasoning, not outcome-fitting.
- Old-line TODOs remain open (capture-side twins, N-12 seeds 11/16,
  MI-scan split stability) — untouched this session.

## Key paths
- `experiments/goal-agent-simulation/goal_sim/{info,detectors,protocol}.py`
- `experiments/goal-agent-simulation/run_phase1.py`
- `experiments/goal-agent-simulation/results/{phase1_acceptance.json,phase1_acceptance.md,FINDINGS.md}`
- `experiments/goal-agent-simulation/tests/test_detectors_and_protocol.py`

## Commits
- None yet (not requested this turn).
