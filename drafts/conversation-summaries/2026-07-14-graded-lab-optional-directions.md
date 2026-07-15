# 2026-07-14 — Graded lab optional directions (parity, 8c diagnosis, 8d)

## Trigger
User asked to work on optional next graded-lab directions until hitting a
surprise or roadblock (subprocess parity, 8c mechanism diagnosis,
`programmatic_budget_aware` member, etc.).

## Done
- **Subprocess parity formalized:** `verify_phase8_isolate_parity.py` — all 7
  member program maps + 4×2 selection loop PASS mock vs subprocess;
  `run_phase8_selection.py --subprocess` flag; smoke subprocess run OK
  (GL-30).
- **8c mechanism diagnosis:** `diagnose_phase8c_carryover.py` →
  `results/phase8c_diagnosis.json` — 0 ep0 mismatches, 9 ep1 diffs, first
  w_thr divergence at gen 1 (GL-28).
- **Phase 8d pre-registered and run:** DESIGN.md "Phase 8d";
  `BUDGET_AWARE_MEMBER_TEMPLATES`, `sample_budget_aware_population()`,
  `run_phase8d_budget_aware.py` → `results/phase8d_budget_aware.json`
  (GL-29).
- `CODE_VERSION` `graded-lab-0.16.0` → `graded-lab-0.17.0`; new test
  `test_sample_budget_aware_population_replaces_weak_2step`; `PLAN.md`
  roadmap row updated; FINDINGS GL-28/29/30 recorded.

## Decisions
- **Roadblock on 8d preservation tradeoff:** swapping `weak_2step` for
  `weak_budget_aware` also flips `correction_preserving` False→True, so
  preservation-mass endpoint (~0.99) is an accounting confound — not
  interpretable as the tradeoff GL-24 named. Deploy-rate null (+0.042)
  confirms GL-17 at selection scale.
- Did **not** implement referee-visible throughput selection — underspecified,
  needs pre-registration.
- Did **not** re-run larger 8a battery — needs new pre-registration.

## Open / next
- Meaningful budget-aware tradeoff: either tag parity
  (`correction_preserving=False`) or new ecology protocol at
  `carrier_load_scale=2.0` (pre-register as 8d-revised or 8e).
- Referee-visible throughput fitness (pre-register in DESIGN.md first).
- Manuscript harvest for GL-28/29/30 if desired (ch34 only if user asks).
- Commit when authorized.

## Key paths
- `experiments/graded-lab-simulation/verify_phase8_isolate_parity.py`
- `experiments/graded-lab-simulation/diagnose_phase8c_carryover.py`
- `experiments/graded-lab-simulation/run_phase8d_budget_aware.py`
- `experiments/graded-lab-simulation/results/phase8{c,d}_*.json`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-28–GL-30)

## Commits
- `ed21adb` Graded lab optional directions: parity, 8c diagnosis, Phase 8d.
