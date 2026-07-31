# 2026-07-08 — Lab-sim noise-tolerant S6 (null-calibrated statistical detector)

## Trigger

Direct follow-up to the same-day LLM-driven detector stress test session
(G-32): after an elaboration on "what was the intervention that was too
strict, what are our options", the user gave four explicit design points
and said "implement and run":

1. Make intervened-vs-clean divergence a RELATIVE rule against the
   measured quantile of clean-vs-clean replicate divergence, not a fixed
   threshold.
2. Address "freeze considerations" fully.
3. Re-base the compensation statistic on outcome/frequency-level
   observables (not per-tick action codes).
4. Choose a configurable replication `k` that "likely delivers signal but
   doesn't have to be guaranteed safe... it can be tightened later."

The user separately endorsed the general framing: "interventions choose
WHERE to look; nulls-at-the-right-coarse-graining determine WHETHER you
saw anything."

## Done

- Designed and implemented `lab_sim/oracle_only/intervention_stats.py`, a
  NEW module (does not edit `uad_intervention.py`/`uad_peel.py`/
  `uad_partition.py`/`uad_blind_v1.py` — the files DESIGN.md's "Freeze
  note 2" names as a recorded referee extension every existing battery
  depends on staying unchanged). Reuses `intervention_diff.py`/
  `intervention_probes.py` (S6 phases 1-2) via import only.
  - `code_histogram` + `total_variation_distance`: per-actor,
    per-post-intervention-window action-code FREQUENCY (order/timing-
    invariant), replacing S6's per-tick set-membership test.
  - `NullStats`/`calibrate_clean_null`: runs `k_clean_replicates`
    (default 4) independent CLEAN (no-probe) episodes of the identical
    (cfg, seed, `agent_overrides`), caches their action-code series, and
    computes pairwise divergence samples/quantile thresholds ON DEMAND
    per requested `from_tick` (channel probes fire at tick 0, actor
    probes at tick 8 — no extra episodes needed for both).
  - `probe_compensation_stats`/`directed_compensation_stats`: one
    intervened+twin triple per probe (twin never calls the LLM),
    `compensates = exceeds_null AND clears_twin_floor` (the null-
    calibrated half is the "relative rule"; the twin-floor half is a
    small fixed constant, `min_effect_vs_twin=0.05`, explicitly flagged
    as NOT yet calibrated the same way).
  - `compensation_matrix_stats`/`channel_compensation_stats`/
    `units_from_compensation_stats`/`discovered_units_intervention_stats`:
    same shapes, same union-find merge semantics, same candidate-edge
    seeding (`uad_intervention.candidate_edges_for_intervention`,
    imported not modified) as the frozen S6 entry point — deliberately
    WITHOUT porting G-28/G-29's masking-hardening (ripple-vs-intrinsic)
    apparatus for channel probes (recorded as a scope cut, not an
    oversight, in the module docstring).
  - Module docstring documents the principled framing (a real system's
    own stochasticity means no literal counterfactual is available; the
    null must be MEASURED, not assumed) and a "Pre-registration, not a
    freeze" note: the three new defaults (`k_clean_replicates=4`,
    `null_quantile_q=0.90`, `min_effect_vs_twin=0.05`) are explicit,
    recorded, and openly re-tunable — unlike `DEFAULT_MIN_COMPENSATION`.
- Wrote 12 new MockIsolate-based tests
  (`tests/oracle_only/test_intervention_stats.py`). The load-bearing
  ones are equivalence tests: `discovered_units_intervention_stats`
  reproduces the frozen `discovered_units_intervention`'s exact
  partitions BIT FOR BIT on `dm_pair_config`, `covert_file_handoff_
  config`, the `serial_pipeline_no_unit_config` negative control, and
  `shared_slot_config`'s documented miss — on a scripted backend, the
  null is verified to collapse to all-zero samples (byte-identical
  replicate replays), recovering S6's original "any nonzero divergence
  is signal" assumption exactly. Also spot-checked the real
  `SubprocessIsolate` boundary manually (not just `MockIsolate`) before
  spending real API money.
- Wrote `run_llm_detector_stats_validation.py`: reuses the EXACT
  scenario/briefings/seed as G-32's `run_llm_detector_stress_test.py`,
  running `discovered_units_intervention_stats` (`k_clean_replicates=4`)
  against it for a like-for-like before/after comparison. Smoke-tested
  with `LAB_SIM_LLM_FAKE_MODE` first (confirmed the "no candidate edge ->
  skip all replicate/probe work" short-circuit doesn't waste calls).
- Ran it for real: 20 LLM-actor spawns across 9 live-LLM episodes (4
  shared clean replicates + 2 actor-directed probes + 3 channel-ablation
  probes; twin runs never call the LLM), $0.0858 total spend, ~15 min
  wall time.
- **Result: exact partition recovered** — `discovered_units_
  intervention_stats` found `{eng1, rm1}`, where G-32's fixed-threshold
  detector returned all singletons on the same scenario/seed.
- **Read the full diagnostics before declaring success and found an
  important caveat**: the merge happened because BOTH `abl_board` and
  `abl_file` (untargeted, whole-channel-shutdown-from-tick-0 probes)
  flagged both actors as compensating by a wide margin (divergence
  0.6-0.9 vs. null thresholds ~0.27-0.33). The probe closest to "the
  actual coordination mechanism" (`abl_dm`) and the surgical
  actor-directed probes (capability_revoke/state_freeze) did NOT clear
  their own measured nulls — the same near-the-line pattern G-32 already
  documented. Recorded this honestly rather than reporting only the
  headline "exact partition recovered" — an untargeted probe's large
  effect on two core pipeline participants doesn't yet distinguish
  genuine coordination from shared-dependency ripple, which is exactly
  the risk G-28's masking hardening addresses for the frozen detector
  and which this module's first pass deliberately does not port.
- Recorded `results/FINDINGS.md` G-33 with the full write-up (design,
  what generalizes and how it was verified, the real run's numbers, the
  per-probe breakdown table, the caveat, and what's not done).
- Updated `DESIGN.md` (new "Noise-tolerant S6" section, explicit about
  why this is a new module and not a third freeze), `PLAN.md` (extended
  the "(b)" open design question entry with the built fallback + its
  caveat; new adjacent section mirroring the "LLM-driven detector stress
  test" one), `README.md` (status line, test count 414→426, new
  narrative paragraph, new run-script and file-tree entries),
  `metadata/experiments.yml` (role text + new headline finding + MB1
  crosswalk cell), `docs/EXPERIMENTS.md` (new narrative paragraph,
  negative-results ledger G-number, MB1 crosswalk row, "Lab sim" bullet,
  Run: line).

## Decisions

- New module, not an edit to `uad_intervention.py` — this IS "addressing
  freeze considerations fully": Freeze-note-2's covered files/defaults
  stay untouched, every existing battery is unaffected (confirmed: full
  suite 426 green, was 414, purely additive), and the new module's own
  defaults are explicitly marked "pre-registered, not frozen" per the
  user's own framing that `k` doesn't have to be "guaranteed safe."
- Chose total-variation distance over a per-actor code-frequency
  histogram as the outcome/frequency-level statistic — order/timing-
  invariant, bounded [0,1], and naturally collapses genuine stalls (same
  code-use distribution) to zero added divergence while genuine
  compensation (different distribution) shows up as nonzero, at a
  coarser, noise-robust grain than S6's per-tick test.
- Computed the null LAZILY from cached replicate traces (per requested
  `from_tick`) rather than once at a fixed offset — channel probes (tick
  0) and actor probes (tick 8) need different windows, and this avoids
  re-running replicate episodes per probe (a real cost concern for an
  LLM backend).
- Calibrated the null ONCE per scenario, shared across every probe
  (rather than once per probe) — live-LLM cost is `k_clean_replicates` +
  probe-count episodes, not their product; this made the real
  9-live-LLM-episode run cheaper than G-32's own 11-episode attempt.
- Did NOT port G-28/G-29's masking-hardening (ripple-vs-intrinsic
  classification) to the channel-probe path this round — scope cut,
  explicitly recorded, and the real run's own result (untargeted probes
  did the merging) makes this a concrete, not hypothetical, gap.
- Reported the real run's result with its full caveat rather than
  stopping at "exact partition recovered" — the headline number is real
  and worth recording, but which specific probe produced it changes what
  the result is evidence FOR (a validated relative-rule mechanism, not
  yet a validated instrument for this scenario's actual DM channel).
- No `CODE_VERSION` bump (no `world_visible/` change) and no edit to any
  Freeze-note-2-covered default.

## Open / next

- Masking hardening (ripple-vs-intrinsic classification) for this
  variant's channel probes — the real run's own result flags this as a
  live concern, not just a theoretical one.
- A 3+-actor LLM scenario (or `committee_with_informal_chatter_config`,
  or a purpose-built one) to test directly whether an untargeted,
  large-effect channel probe would ALSO wrongly flag a non-coordinating
  bystander actor as compensating — the concrete next step this session's
  own caveat points to.
- Calibrating `min_effect_vs_twin` against its own measured null rather
  than a fixed constant (it did not bind this run, but was never
  stress-tested at the margin).
- `discovered_units_blind` (S7)'s statistical analog was not attempted.
- Only one scenario/seed was tried (real API spend).
- Remaining medium-lift backlog (unchanged from before this session):
  report-mode-widening blind-generation round 2; D3 (extended ecology);
  manuscript integration; overdue `run_s7_blind_battery.py` re-run with
  the committee over-merge fix (cosmetic, already fully recorded).

## Key paths

- `experiments/lab-simulation/lab_sim/oracle_only/intervention_stats.py`
  — the new module, full design rationale in its own docstring.
- `experiments/lab-simulation/tests/oracle_only/test_intervention_stats.py`
  — load-bearing equivalence tests.
- `experiments/lab-simulation/run_llm_detector_stats_validation.py` —
  the real-LLM validation script.
- `experiments/lab-simulation/results/llm_detector_stats_validation.{json,md}`
  — real results, full diagnostics (null samples, per-probe matrix).
- `experiments/lab-simulation/results/FINDINGS.md` G-33 — full write-up,
  including the per-probe breakdown table and caveat.
- `experiments/lab-simulation/DESIGN.md` "Noise-tolerant S6" section.

## Commits

- (none yet — end-of-session commit not requested this turn)
