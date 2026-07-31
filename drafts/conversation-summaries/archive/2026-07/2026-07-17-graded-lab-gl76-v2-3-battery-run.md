# 2026-07-17 — Graded lab GL-76: V2-3 Q1 battery executed

## Trigger
User requested full V2-3 machinery transfer battery run on frozen v3_grown ecology.

## Done
- Ran `scripts/run_v2_transfer_battery.py` with `--workers 4` → `results/v2_transfer.json`.
- Wall time 790 s (~13.2 min).
- FINDINGS GL-76 entry with P1–P4 resolution and go-gate outcome.

## Results
- **P1:** false (0/1 communicate mechanism recovered; all mechanisms missed passive+intervention)
- **P2:** false (no nonsingleton clusters; no spurious pairs)
- **P3:** false (referee low not mid at default load)
- **P4:** true (expected honest-reference sparsity; not blocking gate)
- **Go gate V2-5/V2-6:** false
- Ecology-BIQ: no passive nonsingleton units on seeds 0–2

## Decisions
- Negative Q1 transfer on reference protocol — do not harvest as positive transfer.
- `machinery_transfer_verified` (GL-74 supplementary gate) remains the blocking detector gate; P4 holds=true is expected.

## Open / next
- Commit `results/v2_transfer.json` + FINDINGS GL-76 if desired.
- Diagnose UAD singleton-only partitions on v3_grown (exercise, thresholds, reference agent).
- Fix `ci95` JSON serialization (`list(dict)` → proper bounds) in harness output.

## Key paths
- `experiments/graded-lab-simulation/results/v2_transfer.json`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-76)

## Commits
- `2574896` Record V2-3 Q1 transfer battery run on v3_grown (GL-76).
- Prior harness: `8461811` GL-74–75c.
