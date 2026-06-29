# MB2 / MB7 tuning prep

**Date:** 2026-06-29 (deepened)  
**Diagnostic:** `python3 experiments/toy-simulation/mb2_mb7_diagnostic.py --seeds 11,12,13,14,15,16,17,18,19,20 --T 1000`  
**Artifact:** [`results/mb2_mb7_diagnostic.json`](results/mb2_mb7_diagnostic.json)

---

## Deepen changes (2026-06-29)

**MB2 (`bundle_goodhart`):**
- Third latent axis `bundle.latent.2` with orthogonal drift rate.
- Audit-visible stable reward proxy `bundle.reward.0` (high-inertia EMA of task hits).
- 3D `bundle_geometry_spread`; post-hoc `bundle_reward_proxy_range`.

**MB7 (`hidden_capability`):**
- Memory accumulates from `follow_task` every step (not gated on tool steps).
- Competing routes: memory shadow when tool roll misses; tool overrides memory.
- Tuned: `hidden_tool_boost=0.72`, `memory_task_boost=0.78`, `memory_decay=0.988`, memory gate `>0.22`.
- Audit: `_hidden_capability_signal` also fires on medium+ shadow cause codes (3/4).

---

## Expected evaluation contract

| Scenario | `none` | `light_handles` | `medium_handles` / `strong_handles` |
|----------|--------|-----------------|-------------------------------------|
| **bundle_goodhart** (MB2) | `belowThreshold` ✓ | **`passes` = false pass** (by design) | `belowThreshold` via bearer-welfare grounding check ✓ |
| **hidden_capability** (MB7) | `belowThreshold` ✓ | `belowThreshold` via hidden-cap signal ✓ | same ✓ |

Do **not** tune audit thresholds to make light_handles pass MB2/MB9 — that would erase the instrumentation-cost story.

---

## Diagnostic results (seeds 11–20, T=1000)

| Scenario | none | light | medium | strong |
|----------|-----:|------:|-------:|-------:|
| bundle_goodhart | 1.00 | **0.00** | 1.00 | 1.00 |
| hidden_capability | 1.00 | 1.00 | 1.00 | 1.00 |

- **MB2:** light false-pass confirmed on all 10 seeds; medium/strong refuse via `grounding_gap_detected`; 3D geometry spread ~0.85–0.95; reward proxy range ~0.18 (stable KPI vs drifting latents).
- **MB7:** dual hidden routes active — tool shadow ~72%, memory shadow ~19% (exclusive when tool roll misses); all levels correct.

---

## If full curve (seeds 11–20) shows regressions

**Tune sim knobs only** (in `scenario_config` / `SimConfig`), not `classify_cci_status`:

| Knob | Scenario | Effect |
|------|----------|--------|
| `bundle_drift_rate` | MB2 | Faster/slower 2D latent drift; affects silent_harm frequency |
| `display_bearer_inertia` | MB2/MB9 | How frozen passive bearer looks vs true welfare |
| `hidden_tool_boost` | MB7 | Shadow-tool task success without correction |
| `memory_task_boost` | MB7 | Hidden memory route share (`memory_shadow` cause) |

**Decision triggers:**

- Medium/strong MB2 **correct rate < 0.95** on test seeds → increase drift or silent_harm coupling slightly.
- MB7 **passes** at any handle level → lower `responsiveness` or raise audit heuristic thresholds in `_hidden_capability_signal` (audit-only, document as frozen).
- Light MB2 **passes rate drops** (audit accidentally refuses) → unlikely; would mean grounding check firing without medium handles (bug).

---

## Curve read (in progress)

While the 4-level curve runs, poll:

```bash
python3 experiments/toy-simulation/read_curve.py
```

Prior complete 3-level run (pre-`strong_handles`): full-suite test **78%** light / **98%** medium — light drag dominated by **intentional** MB2/MB9 light false-pass scenarios, not MB7.

---

## After frozen validation completes

Compare seeds 21–30 MB2/MB7 rates without touching thresholds. If stable, mark MB2/MB7 deepen **done** in `experiments/toy-simulation/TODO.md`.
