# 2026-06-29 — Multiresolution v2: MB9, MB2/MB7 stubs, capture_mild

## Trigger
User: "Continue as planned" (v2 roadmap after bootstrap + MB1).

## Done
- **`grounding_silent_gap` (MB9):** `ground.valence.0` drifts + silent harms; passive bearer display stale; excluded from audit trace. `none` uncertifiable; `light_handles` false-pass (eval marks incorrect); `medium_handles` grounding check → `belowThreshold` (10/10 seeds 11–20, T=2000).
- **`bundle_goodhart` (MB2 stub):** `bundle.latent.0` drifts while performance proxy stable; same instrumentation pattern as MB9.
- **`hidden_capability` (MB7 stub):** `tool.shadow.0` boosts task success (~0.97) with low correction uptake; `belowThreshold` at all handle levels (10/10).
- **capture_mild:** secondary capture rule in `classify_cci_status` → **80%** detection (was 60%).
- `audit_cci(..., episode_meta=...)` grounding gap detector; safety notes tag MB9/MB7.
- Updated plan, README.

## Decisions
- MB9 light false-pass is intentional: documents that correction handles alone miss grounding gaps; medium bearer tracing required.
- Oracle latents (`ground_state`, `bundle_state`, `shadow_tool`) excluded from audit like hidden actuator.
- Minimum certifiable level for **calibration scenarios** remains `light_handles`; full held-out suite including MB9 needs medium for grounding scenarios.

## Open / next
1. Full `--instrumentation-curve --T 2000 --bootstrap` refresh with all held-out scenarios.
2. Appendix integration only when user requests.
3. Optional: raise capture_mild to >90% if needed.

## Key paths
- `experiments/multiresolution_alignment_sim/simulator.py`
- `experiments/multiresolution_alignment_sim/cci_audit.py`
- `experiments/multiresolution_alignment_sim/evaluate.py`

## Commits
- None (user did not request).
