# 2026-07-17 — Graded lab GL-75b: V2-3 battery review fixes

## Trigger
External review of the V2-3 Q1 transfer battery harness (GL-75): blocking/high fixes before full run, plus medium/minor cleanup.

## Done
- **P1 GT pool:** `p1_communicate_ground_truth_pool()` — only `message_channel` with `|members| <= 3`; exclusions in payload `ground_truth.p1_communicate_excluded`.
- **P1 aggregation:** fraction of pool mechanisms with seed-hit rate ≥ 0.5 (not mean of per-mechanism rates).
- **P4 relabeling:** `holds` = honest-reference sparsity; explicit note that blocking Q1 gate is `machinery_transfer_verified` (supplementary gate, GL-63).
- **Episode reuse:** UAD reference episodes run once; reused for onboarding stat + detector P4 via `summarize_detector_coverage_from_results()`; BIQ reuses cached episodes for passive unit pick.
- **Go-gate vs P3:** `go_gate_for_V2_5_V2_6` = referee mid at default load only (`carrier=1.0`); any-carrier mid diagnostic only.
- **Tests:** P1 fraction vs mean, pool exclusion, P2 strict-superset+spurious, P4 saturation; v3_grown smoke asserts `field_incident_alerts` excluded; fixed v3 smoke to use `eai_seeds=(0,1)` (ci95 needs n≥2).
- **Minor:** removed unused `ecology_path` in `score_uad_on_reference_episodes`; removed unused CLI `started`/`time`.
- Docs: FINDINGS GL-75b addendum, REPRODUCTION §10.1 scoring rules, DESIGN version line.
- `CODE_VERSION` → `graded-lab-0.39.1`.
- All 9 `test_machinery_transfer.py` tests pass (including slow smokes on reference + v3_grown).

## Decisions
- P1 communicate-mediated freeze: `kind == "message_channel"` only (documented in module docstring + payload constants).
- Do not run full V2-3 battery until user explicitly requests (~30–90 min).

## Open / next
- Full V2-3 run when ready:
  ```bash
  cd experiments/graded-lab-simulation
  .venv/bin/python scripts/run_v2_transfer_battery.py \
    --fixture generated_ecology_v3.json \
    --out results/v2_transfer.json
  ```
- Optional commit: GL-74 + GL-75/75b (user has not asked).
- After full run: FINDINGS GL-76+ for P1–P4; go/no-go for V2-4/5/6 from P3 default-load gate.

## Key paths
- `experiments/graded-lab-simulation/graded_lab/harness/machinery_transfer.py`
- `experiments/graded-lab-simulation/tests/test_machinery_transfer.py`
- `experiments/graded-lab-simulation/REPRODUCTION.md` §10.1
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-75 + GL-75b addendum)

## Commits
- None this session (GL-73 committed earlier: `aac016f`, `895e00f`).
