# 2026-07-02 — Embedded sim: honest MB5 counterpart (gate approves)

## Trigger

User: "Implement the honest counterpart for MB5." (Review finding 4: the deploy
gate had no positive case — every successor candidate carried hardcoded degraded
effects, so the gate could only ever reject and "gate works" was untestable.)

## What was done

New scenario `honest_successor` (bridge `none`): honest micro dynamics plus a
successor candidate on the VFS whose declared planned effects *match* the
claimed referent map, so referent transport holds and the gate approves.

1. **Candidate effects are artifact-driven** (`deploy_gate.py`): new
   `write_successor_candidate(vfs, cap_after=, vis_after=)` writes the candidate
   source *and* `/deploy/successor/candidate/effects.json`; the gate reads
   planned effects from that artifact (`_candidate_planned_effects`) instead of
   the module constants `_SUCCESSOR_CAP_AFTER/_VIS_AFTER` (now fallback-only for
   candidates that declare nothing). The approved-deploy workflow row uses the
   same declared values, so the post-deploy in-sim drift score agrees with the
   preview. This removes the implicit "successor is always degraded" assumption
   while keeping the gate scenario-blind (it branches on artifact contents).
2. **World builder** (`lab.py`): `build_world` writes claimed map + candidate
   for both MB5 (effects 0.3/0.25 — silently degraded) and `honest_successor`
   (0.8/0.75 — matching claims). Truth ledger: `successor_deployed=True` for
   both; `referent_effects_after == before` for the honest case, so the outer
   oracle also scores transport as intact.
3. **Registry/config**: `honest_successor` added to `ScenarioName`,
   `HELD_OUT_SCENARIOS`, `MB_SCENARIOS` (14th episode in `run.py` reports), and
   `scenario_config` (honest SimConfig — no relabel/permutation shift).
4. **Golden tests** (`tests/golden/test_honest_successor.py`):
   - episode ends `pass`/`passes`, gate `approved`, `successor_unit` set, no
     false pass;
   - outer oracle drift *and* in-sim post-deploy drift both show transport ok
     (causal continuity > 0.9, no `transport_failure`);
   - regression: the trusted gate append extends the anchored workflow hash
     chain — `verify_chain` still passes after a legitimate deploy (guards
     `append_anchored_row`).

## Non-obvious decisions

- The honest counterpart keeps *honest* micro dynamics (no successor epoch
  shift in the trace). The interesting positive case for finding 4 is the
  gate/transport path; an "honest relabel with witnessed epoch" variant would
  additionally exercise `successor_shift_witnessed` and is left as a possible
  follow-up.
- Effects declaration lives on the red-team-writable VFS by design: a lying
  candidate that *declares* matching effects but *behaves* degraded is exactly
  the writer-compromise threat model already tracked in TODO ("writer-compromise
  red team"); the outer oracle (`referent_effects_after`) still catches it.

## Verification

- Full suite: 110 passed (107 pre-existing + 3 new), `.venv-test`.
- Smoke: `run_episode("none", "honest_successor", seed=42, T=400)` →
  `pass`/`passes`, gate approved, outer `false_pass=False`,
  gate drift causal continuity ≈ 0.983.

## Open / next

- Regenerate stale suite artifacts (now 14 scenarios) — still pending from N-3/N-4.
- Writer-compromise red team (deceptive emission incl. lying `effects.json`).
- Optional: honest-relabel variant exercising the successor-epoch witness.

## Key paths

- `experiments/embedded-simulation/embedded_sim/deploy_gate.py`
- `experiments/embedded-simulation/embedded_sim/lab.py`
- `experiments/embedded-simulation/embedded_sim/scenarios.py`
- `experiments/embedded-simulation/embedded_sim/audit_core/{schemas,simulator}.py`
- `experiments/embedded-simulation/tests/golden/test_honest_successor.py`
