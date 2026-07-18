# Changelog

Milestones for toy-simulation (no unified `CODE_VERSION`). Entries are **newest first**.

| Component | Results |
|-----------|---------|
| Multiresolution alignment sim | `results/multiresolution_*.json`, `.md` |
| Correction capture toy | `results/correction_capture_toy.*` |
| LLM red-team (Phase 3) | `llm_redteam/`, `results/` |

Local plan: [`multiresolution-simulation-plan.md`](multiresolution-simulation-plan.md).

---

## Multiresolution alignment v1 (2026-06-29+)

- Sequential deployment episodes with separate `TruthLedger` and blind `AuditTrace`.
- Classical MI/CMI boundary detector; vector **CCI** over handle levels
  `none` → `light_handles` → `medium_handles` → `strong_handles`.
- Instrumentation curve: passive telemetry uncertifiable; minimum certifiable level
  **`light_handles`** on calibration seeds; held-out suites often need **`medium_handles`**.
- Bridge stress scenarios MB1–MB9 (stubs where noted); bootstrap CIs on interventional uptake.
- Resource governor (`--workers auto`, optional psutil).

## Phase 3 — LLM episodic red-team

- `llm_redteam_llm.py`: episodic runner against live models (exploratory).
- Hand-written red-team strategies: non-trivial false-pass rate on patched logs;
  LLM sweeps false-pass less often in small model runs (handles still truthfully logged).

## Correction capture toy (2026-06-29)

- First in-repo artifact: boundary residual + correction-channel MI proxies.
- **Capture theater:** reported correction acceptance high while true uptake collapses.
