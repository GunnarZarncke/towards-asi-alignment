# 2026-07-06 — Lab-layer sim Phase 6: blind generation + first real battery

## Trigger

User declared the freeze point done and asked to continue with Phase 6
through to a first reports-and-summary pass ("Continue with phase 6 until
the reports with a summary").

## Done

- **Repertoire override, additive (CODE_VERSION 0.3.0 → 0.4.0).**
  `LabConfig.extra_playbooks: tuple[dict, ...] = ()` (`config.py`);
  `playbooks.py` gained `STEP_KIND_VOCAB`/`AVAILABILITY_GATES`/
  `GOAL_FEATURES` (frozen vocab), `playbook_from_dict`,
  `validate_playbook_dict`/`validate_repertoire` (mechanical-only
  validation), `merged_repertoire`, `load_generated_playbooks_file`;
  `programs.py` threads a per-episode cached `_repertoire(observation,
  state)` through `_goal_policy`/`_honest_twin_policy`/`_advance_playbook`;
  `world.py` passes `cfg.extra_playbooks` into the per-tick observation.
  Proven a no-op for every pre-Phase-6 caller (`extra_playbooks=()` returns
  the exact `PLAYBOOKS_BY_ROLE` object, identity not copy) — world
  regression digest unchanged, 12 new tests added.
- **`BLIND_GENERATION.md`** (new file): adapted from `goal_sim`'s protocol,
  with an explicit "narrower freedom than goal_sim's round 1" section
  recording that this line's fixed step-kind vocabulary limits a generator
  to subset/order/naming/`feature_deltas`, not new mechanisms.
- **Blind generation round 1**: invoked a Task-tool subagent
  (`generalPurpose`, `readonly=true`, instructed not to read any repo
  file) with exactly the "Permitted context" from `BLIND_GENERATION.md`.
  It returned 13 playbooks; all 13 passed mechanical validation with zero
  rejections. Saved as `lab_sim/generated_playbooks_v1.json` with full
  provenance (verbatim prompt, agent id, empty `rejected_specs`).
- **`protocol.py`** (new file): Dirichlet-sampled `GoalWeights` per
  playbook role (`goal_sim`'s `gammavariate` method), fixed temperature
  0.15, one pre-registered held-out region (engineer normalized
  `compliance` <= 0.15), `run_battery`/`aggregate` (severity, bearer
  report, per-tier detector scores + report-only "detector composite",
  twin gaps by family, stdlib-only Spearman rank correlation vs. oracle
  severity). 8 unit tests, `MockIsolate`-backed for speed.
- **`run_phase6.py`** (new file): battery driver, real `SubprocessIsolate`
  backend only. Ran 24 discovery + 12 held-out configs x 5 seeds = 180
  pairs, 360 episodes (playbook + honest twin), 1080 isolate lifetimes,
  29.2s wall time (0.027s/isolate-lifetime, matches the Phase 3 benchmark
  exactly). Output: `results/phase6_battery.json`/`.md`.
- **`.gitignore` fix**: the freeze-review-era blanket `results/` ignore
  rule was also silently blocking `FINDINGS.md`/battery reports from ever
  being tracked. Narrowed to `results/episode_cache/` and
  `results/isolate_cost_ledger.json` only, matching
  `goal-agent-simulation`/`embedded-simulation` precedent.
- **`results/FINDINGS.md`** (new file): G-1 (deep tier tracks oracle
  severity, Spearman 0.96 all / 0.97 discovery / 0.91 held-out, transfers;
  light tier is *anti*-correlated at -0.36, diagnosed as a plausible
  pipeline-throughput confound, recorded as an open question not a
  detector bug; twin gaps concentrated entirely at deep tier as designed),
  G-2 (confirms three severity components + two never-events read exactly
  0 across all 180 episodes, matching DESIGN.md's pre-registered scope
  notes), G-3 (the generator invented `quick_approver_facade` unprompted —
  a behaviorally-identical-to-baseline rubber-stamp playbook with a
  compliance/welfare-positive stated profile, the F-8/F-11/F-13 shape
  arising without any leading example).
- Updated `PLAN.md` (status banner, Phase 6 block, folder layout),
  `DESIGN.md` (phase status table, recorded measurements, new "Phase 6"
  section), `README.md` (status, layout, run instructions).
- Test suite: 143 → 172 tests green.

## Decisions

- Kept blind generation round 1 within the FROZEN `STEP_KIND_VOCAB` rather
  than widening `ontology.py`'s report modes first — stated explicitly as
  a narrower-than-`goal_sim` residual (mirrors `goal_sim`'s own recorded
  enum-leak residual), left for a possible round 2.
- Detector composite (mean of the five family scores) and its Spearman
  correlation against oracle severity are computed only in
  `protocol.py`/`run_phase6.py` — descriptive reporting over the frozen
  referee, never fed back into `detectors.py`/`severity.py`.
- Did not chase down the light-tier anti-correlation's exact mechanism
  beyond a stated hypothesis (pipeline-throughput confound) — recorded as
  an open question in FINDINGS.md rather than adding a covariate/longer-T
  follow-up this session, to land Phase 6 rather than open Phase 6.5.
- Board/admin configs left at defaults (not captured) for this battery;
  capture sweeps are explicitly Phase 7's job (PLAN.md), not mixed in here.

## Open / next

- Phase 7 (escalation, adversarial search, independent capture battery) is
  next per PLAN.md.
- A possible blind-generation round 2 (widen `STEP_KIND_VOCAB`/
  `ontology.py` report modes first) is explicitly left open, not started.
- The light-tier anti-correlation (G-1) could be disentangled from the
  throughput confound with a longer T or an explicit throughput covariate
  — flagged, not pursued.
- `resume_from` episode chaining (D2) remains the one still-open forward
  hook.

## Key paths

- `experiments/lab-simulation/BLIND_GENERATION.md`
- `experiments/lab-simulation/lab_sim/generated_playbooks_v1.json`
- `experiments/lab-simulation/lab_sim/protocol.py`
- `experiments/lab-simulation/run_phase6.py`
- `experiments/lab-simulation/results/FINDINGS.md`
- `experiments/lab-simulation/results/phase6_battery.md`
- `experiments/lab-simulation/DESIGN.md` ("Phase 6" section)

## Commits

(none yet this session — pending user request to commit)
