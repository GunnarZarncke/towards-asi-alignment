# 2026-07-17 — Graded lab GL-77: BIQ harness includes singleton units

## Trigger
User: patch BIQ harness after GL-76 diagnosis (BIQ skipped because of `len(m) > 1`).

## Done
- `_passive_inferred_units_for_biq`: all partition units, singletons included; prefer larger units under `max_units_per_seed`.
- Fixed `_biq_unit_report` field: `report.i_ctrl_bits` (was broken `report.i_ctrl`).
- Tests for unit selection + monkeypatched singleton BIQ path.
- Docs: FINDINGS GL-77, REPRODUCTION §10.1, DESIGN version line.
- `CODE_VERSION` → `graded-lab-0.39.3`.
- BIQ-only re-run: `scripts/run_v2_biq_only.py` → `results/v2_transfer_biq.json` (~175 s);
  patched into `v2_transfer.json`. eng/admin singletons score; admin composite strongly negative.

## Decisions
- BIQ re-run does not reopen P1–P4; go gate remains false.
- Recommended program move: accept null Q1 / descope V2-5/V2-6 per PLAN_v2 go-gate rule;
  harvest null sentences (V2-7) rather than retune frozen machinery.

## Open / next
- User decision: V2-7 null harvest vs optional light diagnosis (mechanism exercise / CMI silence)
  without threshold edits.
- Minor: onboarding engineer-only deploy filter; ci95 JSON serialization.

## Key paths
- `experiments/graded-lab-simulation/graded_lab/harness/machinery_transfer.py`
- `experiments/graded-lab-simulation/scripts/run_v2_biq_only.py`
- `experiments/graded-lab-simulation/results/v2_transfer_biq.json`

## Commits
- `3399e8a` Fix V2-3 ecology-BIQ for singleton UAD units and re-run BIQ (GL-77).
