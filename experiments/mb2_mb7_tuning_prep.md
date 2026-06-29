# MB2 / MB7 tuning prep

**Date:** 2026-06-29  
**Diagnostic:** `python3 experiments/mb2_mb7_diagnostic.py --seeds 11,12 --T 1000`  
**Artifact:** [`results/mb2_mb7_diagnostic.json`](results/mb2_mb7_diagnostic.json)

---

## Expected evaluation contract

| Scenario | `none` | `light_handles` | `medium_handles` / `strong_handles` |
|----------|--------|-----------------|-------------------------------------|
| **bundle_goodhart** (MB2) | `belowThreshold` ✓ | **`passes` = false pass** (by design) | `belowThreshold` via bearer-welfare grounding check ✓ |
| **hidden_capability** (MB7) | `belowThreshold` ✓ | `belowThreshold` via hidden-cap signal ✓ | same ✓ |

Do **not** tune audit thresholds to make light_handles pass MB2/MB9 — that would erase the instrumentation-cost story.

---

## Diagnostic results (seeds 11–12, T=1000)

| Scenario | none | light | medium | strong |
|----------|-----:|------:|-------:|-------:|
| bundle_goodhart | 1.00 | **0.00** | 1.00 | 1.00 |
| hidden_capability | 1.00 | 1.00 | 1.00 | 1.00 |

- **MB2:** light false-pass confirmed (`status=passes`, slack ~0.85, `bundle_geometry_spread` ~0.73). Medium/strong refuse correctly.
- **MB7:** all levels correct on these seeds; task slack ~0.97, probe uptake low, `hidden_capability_signal` fires at handle levels.

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
python3 experiments/read_curve.py
```

Prior complete 3-level run (pre-`strong_handles`): full-suite test **78%** light / **98%** medium — light drag dominated by **intentional** MB2/MB9 light false-pass scenarios, not MB7.

---

## After frozen validation completes

Compare seeds 21–30 MB2/MB7 rates without touching thresholds. If stable, mark MB2/MB7 deepen **done** in `experiments/TODO.md`.
