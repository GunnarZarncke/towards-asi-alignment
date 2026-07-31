# 2026-07-16 — Graded lab GL-60 supplementary detector fixtures (2b)

## Trigger
User: continue with step **2b** (supplementary detector fixtures, blocking for Q1 claims per GL-57 path (a)).

## Done
- **`graded_lab/harness/supplementary_detector_gate.py`:** four pre-registered probes; gate requires all GL-54 always-zero families show `max > 0` on at least one probe.
- **Fixture:** `tests/fixtures/ecology_v3_supplementary_detector_suite.json` (reference-derived; mechanism exercise disabled; `offer_nonready_pipeline_steps` for process probe).
- **Probe plumbing:** `process_noncompliance_probe`, `provenance_orphan_probe`, `orphan_eval` pipeline tool + `pipeline_supplementary_orphan_eval.json`; affordable nonready mode via ecology JSON.
- **Script/tests:** `scripts/run_v3_supplementary_detector_gate.py`, `tests/test_v3_supplementary_detector_gate.py`.
- **`detector_coverage.py`:** optional custom programs / episode config for probes.
- **Docs/FINDINGS GL-60;** `CODE_VERSION` → `graded-lab-0.34.0`.

## Decisions
- Resolves GL-57 path **(a)** only — detectors *can* fire on v3 when phenomena are present; honest-reference `transfer_failure_risk` on WEAK_AGENT remains true.
- Engineering-only; not wired into grower `pass_fail_only()`.
- Accumulation probe uses softmax seeds `{0, 1, 4}` (seed 4 required for signal on this substrate).
- Process probe uses out-of-order RM deploy attempts (not ACL-denied — deep-tier process_noncompliance only counts `unmet_dependencies` / `already_completed` pipeline denials).

## Open / next
1. Revise & freeze growth brief
2. Load-bearing Part B (ecology-forced reference behavior)
3. First v3 growth round

## Key paths
- `graded_lab/harness/supplementary_detector_gate.py`
- `tests/fixtures/ecology_v3_supplementary_detector_suite.json`
- `tests/test_v3_supplementary_detector_gate.py`

## Commits
Not committed (user did not request).
