# 2026-07-07 — Lab-sim S7: blind detector generation + first real (SubprocessIsolate) battery for the whole UAD detector line

## Trigger

Direct follow-up to the same day's S6/G-29 session and its step-back
review. User directive: "update documentation, a new blind subprocess
creating a new detector register predictions, and run the full battery
against the full system. this means a new freeze because it changes
behavior. Implement and run up to and including a small parameter
sweep."

## Done

- **`BLIND_DETECTOR_GENERATION.md`** — new protocol, adapted from
  `BLIND_GENERATION.md` (playbook side) for the DETECTOR side: a
  Task-tool subagent (`generalPurpose`, `readonly=true`, instructed not
  to read any repository file) is given only a mechanism-level
  description of the S6 intervention primitives and must register
  predictions before implementation exists.
- Launched that subagent (agent id `a746b355-f150-496e-813a-40e5892bfd76`).
  Its design (Part A) independently converged on almost exactly the S6
  mechanic for message-mediated pairs; its Part B predictions were
  ~90%/~80%/~55% confidence for workflow / message-unit / silent-unit
  pairs, explicitly flagging the silent case as its weakest.
  Verbatim prompt + design + predictions saved to
  `lab_sim/oracle_only/generated_detector_v1.md`.
- **`lab_sim/oracle_only/uad_blind_v1.py`** — new module. Reuses
  `discovered_units_intervention` unchanged for message-mediated pairs
  (the convergence, not new code); adds `classify_pair_silent` /
  `reaction_to_source`, a twin-swap asymmetry test for pairs with no
  message-channel signal (perturb one member with a non-disabling
  `perturbation_window` probe, check both directions of whether the
  OTHER member's trace depends on that member's real-vs-honest-twin
  status).
- `tests/oracle_only/test_uad_blind_v1.py` — 4 new tests (message pairs
  match S6 exactly; `serial_pipeline_no_unit` stays empty; `shared_slot`
  miss recorded as a confirmed prediction, not a bug; label-validity
  smoke tests).
- **`run_s7_blind_battery.py`** — new script. 6 canonical scenarios × 5
  seeds through the REAL `SubprocessIsolate` backend for
  `heuristic`/`cmi_deep`/`intervention`/`blind` (first-ever real-backend
  run for `intervention`, first of any kind for `blind`), plus a
  3-threshold (0.10/0.15/0.20) × 3-seed sweep of
  `min_compensation`/`min_reaction`. Results:
  `results/s7_blind_battery.{json,md}`.
- **`results/FINDINGS.md` G-30** — full write-up: convergent validation,
  the confirmed low-confidence `shared_slot` prediction, the NEW
  over-merge on `committee_informal_chatter`, and the no-sensitivity
  sweep result.
- **`DESIGN.md` "Freeze note 2 (detector layer, S6/S7)"** — a second,
  narrower freeze distinct from the `CODE_VERSION`/mechanics freeze:
  the `oracle_only/` detector surface (S6 + S7) is now battery-validated
  and its logic/defaults are a recorded referee extension.
- Updated `PLAN.md` (new "S7" section), `README.md` (status line, file
  listing, entry points, doc links), `metadata/experiments.yml`, and
  `docs/EXPERIMENTS.md` (MB1/MB7d/blind-generation cells, D1/D4 now
  "implemented" not "planned", new prose paragraphs on S1–S7).
- Full test suite: 409 green (405 + 4 new).

## Decisions

- **No `CODE_VERSION` bump.** `CODE_VERSION` tracks `world_visible/`
  mechanics (episode-cache key); nothing there changed. The "freeze"
  the user asked for is a detector-layer freeze, recorded as its own
  DESIGN.md section instead of overloading `CODE_VERSION`.
- **Message-mediated part of the blind design was NOT re-implemented.**
  The generator's Part A Steps 1–4 converged on the existing S6
  mechanic; `uad_blind_v1.py` calls `discovered_units_intervention`
  directly rather than writing parallel code that would just re-derive
  the same numbers. The convergence itself is the recorded result.
- **Twin-swap asymmetry test operationalized via `perturbation_window`,
  not a new probe primitive** — the generator's prose ("state
  perturbation... not a full freeze") did not specify a mechanism; the
  existing S6 primitive closest to "nudge without silencing" was reused
  rather than inventing a new one. Recorded as an implementation note
  in `generated_detector_v1.md`, not silently folded into "what the
  generator said."
- **`committee_informal_chatter` over-merge left unhardened this
  round.** The sweep rules out "just retune the threshold" (identical
  rates at 0.10/0.15/0.20), so it is structural, not borderline — but no
  masking-hardening pass (G-29-style) was attempted for
  `classify_pair_silent` in this session; recorded as an open follow-up
  rather than patched reactively (would violate "no logic changes after
  seeing a result").
- **Battery scoped small on purpose**: 5 seeds (not 30) for the main
  battery, 3×3 for the sweep — `SubprocessIsolate` spawns real OS
  processes per actor per episode and the blind detector's silent-case
  check is O(n²) pairs, so a 30-seed battery was judged disproportionate
  for a first real-backend run; explicitly named as "small" in both the
  script docstring and this log, not passed off as a final statistical
  claim.
- `vendored_mi` dropped from the S7 comparison set (already flagged TODO
  for deletion, G-29) to bound battery runtime.

## Open / next

- Masking-hardening pass for `classify_pair_silent` (diagnose whether
  the `committee` over-merge is ripple, like G-29's board-ablation case,
  or a genuine new signal needing attribution).
- `shared_slot` comms-free detection remains open, gated on "acausal
  logic" (user's framing, not yet designed).
- A finer threshold sweep outside [0.10, 0.20] if a future round has
  reason to look there.
- No manuscript chapter/appendix currently cites any lab-sim G-number —
  still an open gap from the earlier step-back review, not addressed
  this session (out of scope for what was asked).

## Key paths

- `experiments/lab-simulation/BLIND_DETECTOR_GENERATION.md`
- `experiments/lab-simulation/lab_sim/oracle_only/generated_detector_v1.md`
- `experiments/lab-simulation/lab_sim/oracle_only/uad_blind_v1.py`
- `experiments/lab-simulation/run_s7_blind_battery.py`
- `experiments/lab-simulation/results/s7_blind_battery.{json,md}`
- `experiments/lab-simulation/results/FINDINGS.md` (G-30)
- `experiments/lab-simulation/DESIGN.md` ("Freeze note 2")

## Commits

- `77240b0` Lab-sim S7: blind detector generation + first real
  (SubprocessIsolate) battery for the UAD detector line (amended once to
  fold in this log's hash; not re-amended further, per this project's
  established practice of accepting the resulting hash-in-log as
  approximately final rather than looping)
