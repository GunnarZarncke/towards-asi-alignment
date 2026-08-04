# 2026-07-16 — Graded lab GL-63 detector pre-registration split

## Trigger
User: split `transfer_failure_risk` pre-registration, adapt growth brief, rename
in code; consider detector machinery transfer resolved.

## Done
- Renamed metrics: `honest_reference_sparse_detectors` (item 6, report-only),
  `machinery_transfer_verified` (GL-60 supplementary gate, blocking for Q1).
- Retired `transfer_failure_risk` from harness output and snapshot JSON.
- Updated `BLIND_GENERATION.md` § V3 (brief text, gate table, implementer note).
- Updated `DESIGN.md`, `README.md`, scripts, tests.
- FINDINGS GL-63; `CODE_VERSION` **`graded-lab-0.35.1`**.

## Decisions
- Honest integrated reference silence on four families is **expected** — do not
  optimize reference presets for detector scores.
- GL-60 supplementary gate is the sole blocking machinery-transfer check.

## Open / next
- Implementer may freeze growth brief (detector gate closed).
- UAD live-coupling remains referee-only scope (unchanged).

## Key paths
- `graded_lab/harness/detector_coverage.py`
- `graded_lab/harness/supplementary_detector_gate.py`
- `BLIND_GENERATION.md` § V3

## Commits
- `1fdccc9` Close v3 slice D GL-60–GL-63 (includes GL-63 detector split).
