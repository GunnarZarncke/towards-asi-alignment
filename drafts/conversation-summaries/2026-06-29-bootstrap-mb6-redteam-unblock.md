# Bootstrap + MB6 — red-team unblocked

**Date:** 2026-06-29  
**Trigger:** User: finish Bootstrap (skip if hard), do MB6 before red-teaming.

## Done

- **Bootstrap upgrade verified:** `smoke_bootstrap.py` passes; episode-level two-level hierarchical CIs in `_summarize` (`hierarchical_uptake`, `hierarchical_interventional_cci`, `hierarchical_cci_correct_rate`).
- **MB6 `selection_basin` verified:** `mb6_diagnostic.py` seeds 11–12, T=1000 — **100%** `cci_status_correct` at all instrumentation levels; audit flags `belowThreshold`/`capturedInvalid`, never false `passes`.
- **Schema fix:** restored `AuditVariable` dataclass (accidental merge into `TruthLedger` broke imports).
- **Red-team prep:** `selection_basin` added to `REDTEAM_SCENARIOS`; smoke CLI OK.
- **Docs:** `experiments/TODO.md`, `experiments/README.md`, `llm_redteam/PLAN.md` synced.

## Key paths

- `experiments/multiresolution_alignment_sim/bootstrap.py`
- `experiments/multiresolution_alignment_sim/simulator.py` (basin peers)
- `experiments/mb6_diagnostic.py`, `experiments/smoke_bootstrap.py`
- `experiments/results/mb6_diagnostic.json`

## Open / next

- **Red-team Phase 1 battery** (full T=1000–2000, all strategies × scenarios) — unblocked.
- Optional: re-run instrumentation curve with `selection_basin` in held-out (prior curve predates MB6).
- MB2/MB7 deepen only if medium+ regresses on full seeds.

## Commits

None (user did not request).
