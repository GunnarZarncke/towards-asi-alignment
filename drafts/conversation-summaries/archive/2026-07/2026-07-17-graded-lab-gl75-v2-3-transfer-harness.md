# 2026-07-17 — Graded lab GL-75: V2-3 Q1 transfer battery harness

## Trigger
User: develop V2-3 Q1 transfer battery but don't run yet.

## Done
- `graded_lab/harness/machinery_transfer.py` — full orchestration + P1–P4 evaluators.
- `scripts/run_v2_transfer_battery.py` — `--smoke`, `--no-biq`, `--fixture`.
- `tests/test_machinery_transfer.py` — fast unit tests + slow smoke on reference fixture (green).
- FINDINGS GL-75; REPRODUCTION §10.1; PLAN_v2 V2-3 row → harness implemented.
- `CODE_VERSION` → `graded-lab-0.39.0`.

## Decisions
- Target ecology default: `generated_ecology_v3.json` / `v3_grown`.
- C5 ground truth: all mechanism kinds via role-expanded `members_ground_truth`.
- EAI sweep uses ecology-aware `_reference_episode_config` + `SubstrateSettings` overlay.
- Full battery not executed; smoke test on reference fixture only validates wiring.

## Open / next
- Run full battery → `results/v2_transfer.json`; resolve P1–P4 in FINDINGS GL-76+.
- Go/no-go for V2-4/5/6 from P3 referee mid band.
- Commit GL-74 + GL-75 together or separately.

## Key paths
- `graded_lab/harness/machinery_transfer.py`
- `scripts/run_v2_transfer_battery.py`

## Commits
- (pending)
