# 2026-07-15 — Graded lab PLAN_v3 slice A hardening (self-review)

## Trigger
User asked "Are we satisfied? Would a critical reviewer be satisfied?" after
slice A (GL-44) was committed. Self-review flagged three fixable gaps:
undocumented gate-calibration discovery process, no negative control, and
substring-matching brittleness in `_ledger_bucket()`. User: "Document. Add
negative-control test. Reduce brittleness. What is the plan for
mechanisms/principals and the behavioral signal?"

## Done
- **`results/FINDINGS.md`**: GL-44 addendum documenting seed-1 exclusion and
  the `carrier_load_scale=1.5` discovery explicitly (both were already frozen
  in fixture metadata before green, but the discovery process was implicit).
- **Negative control** (`test_slice_a_ablation_gate_negative_control_at_default_load`):
  asserts ablation must NOT diverge on all 3 seeds at default `carrier_load_scale=0.0`.
  **Caught a real bug**: the `38`/`2` compute split (chosen earlier this
  session to satisfy the compiler's ±25% cross-check test) was degenerate —
  `compute=2` starves the engineer completely at *any* load, including `0.0`,
  silently invalidating the documented "load=1.5 required" claim.
- **Fixture fix**: re-split engineer compute to `30`/`10` (still sums to
  declared `40`, still passes cross-check). Restored clean load-dependence:
  `L1=0.0` at load `0.0` on all 3 seeds; `L1 ∈ {0.155, 0.617, 0.114}`
  (all ≥ 0.10) at load `1.5`.
- **`institutional_compiler.py`**: replaced substring-matching `_ledger_bucket()`
  with an exact-match `_RESOURCE_TYPE_BUCKETS` registry; unrecognized
  `resource_type` now raises `CompileError` instead of silently contributing
  zero. New test: `test_unrecognized_resource_type_rejected_not_silently_dropped`.
- **`PLAN_v3.md`**: gate table updated (30/10 split rationale), negative-control
  note added, two new anticipated-critic entries ("mechanisms/principals mostly
  decorative" → slice B plan; "behavioral signal is thin" → deferred to slice D).
- Minor cleanup: removed pre-existing unused `EpisodeConfig` import in
  `test_institutional_compiler.py`.
- Verification: `test_institutional_compiler.py` + `test_v3_slice_a_flow_ablation.py`
  8/8 green; full `--profile fast` suite logically 100% pass (speed-guard flagged
  5 pre-existing unrelated UAD tests as wall-clock-slow — machine load, not a
  regression, not investigated further).

## Decisions
- Root-caused the negative-control failure via direct `compile_ecology()` calls
  (not run-episode debugging) — confirmed the compiler was correct (40.0 vs 2.0)
  and the *fixture split* was the degenerate part.
- Kept the gate's engineering-only scope: broadening the behavioral signal
  (multi-actor, AND rule, more fixtures) is deferred to slice D, not slice A —
  widening now would validate the wrong thing (flow wiring, not eventual
  growth criteria).
- Mechanisms/principals enforcement (ACLs, votes, transfers) confirmed as
  slice B's entire scope, wired the same way slice A wired flows.

## Open / next
- Slice B: mechanisms → enforced ACLs/votes (not started).
- Slice D: broaden behavioral signal + re-derive C2-v3 thresholds against
  real batteries (not started).

## Key paths
- `experiments/graded-lab-simulation/graded_lab/world_visible/institutional_compiler.py`
- `experiments/graded-lab-simulation/tests/fixtures/ecology_v3_slice_a_reference.json`
- `experiments/graded-lab-simulation/tests/test_v3_slice_a_flow_ablation.py`
- `experiments/graded-lab-simulation/PLAN_v3.md` (gate table + anticipated critic)
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-44 addendum)

## Commits
- `dc85b05` Harden PLAN_v3 slice A: negative control, exact-match ledger buckets.
