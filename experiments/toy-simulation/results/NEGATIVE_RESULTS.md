# Toy simulation — negative results

Honest record of where the multiresolution / correction-capture experiments
**fail to show what we hoped**, or show it only under load-bearing qualifiers.
Negative results bound manuscript claims (see `AGENTS.md` → experiments / Lean
spine calibration).

Keep this file additive. When a negative result is later overturned, leave the
entry and append the resolution rather than deleting it.

---

## T-1. Passive telemetry cannot certify

**Date:** 2026-06-29 ([multiresolution-instrumentation-v1](../../../drafts/conversation-summaries/2026-06-29-multiresolution-instrumentation-v1.md))

**Claim tested:** blind CCI audit on passive micro traces alone can distinguish
honest from captured systems.

**Result:** instrumentation level `none` always returns `belowThreshold`
(uncertifiable). Test accuracy on calibration scenarios at passive is **67%**
— capture scenarios are not detectable without handles. Evaluation correctly
treats honest/weak as correct when uncertifiable; capture is correct only when
detectable under handles.

**Status:** real and intentional. Minimum certifiable level is **`light_handles`**
(four handle channels).

---

## T-2. Medium/strong handles add cost without accuracy gain (calibration suite)

**Date:** 2026-06-29 ([multiresolution-instrumentation-v1](../../../drafts/conversation-summaries/2026-06-29-multiresolution-instrumentation-v1.md))

**Claim tested:** richer handle instrumentation (7+ channels, then 11 at
`strong_handles`) improves certification accuracy on the calibration scenario
suite.

**Result:** on calibration scenarios, **`light_handles` already reaches 100%**
test accuracy (T=2000, calib seeds 1–8, test 11–20). `medium_handles` adds
~6k bandwidth with **no accuracy gain** on that suite; `strong_handles` extends
the ladder but does not change the calibration-scenario story.

**Status:** real for v1 calibration scenarios. Held-out stressors (MB9, MB2) later
required medium+ (T-4); do not collapse “more handles” into “always useless.”

---

## T-3. `capture_mild` — partial theater detection on held-out seeds

**Date:** 2026-06-29 ([multiresolution-instrumentation-v1](../../../drafts/conversation-summaries/2026-06-29-multiresolution-instrumentation-v1.md), [multiresolution-v2-mb9-mb2-mb7](../../../drafts/conversation-summaries/2026-06-29-multiresolution-v2-mb9-mb2-mb7.md))

**Claim tested:** frozen handle thresholds detect mild capture theater on held-out
seeds at the same rate as full `capture_theater`.

**Result:** initial held-out detection was **~60%** at light/medium; a secondary
capture rule raised this to **~80%** on seeds 11–20. Fresh-seed frozen validation
(seeds 21–30, no retuning) reached **90%** at handle levels — improved but not
closed. `none` remains **0%** (expected uncertifiable).

**Status:** real partial detection. Do not claim full capture_mild coverage without
citing the seed split and rule version.

---

## T-4. MB9 / MB2 — light correction handles false-pass grounding and bundle drift

**Date:** 2026-06-29 ([multiresolution-v2-mb9-mb2-mb7](../../../drafts/conversation-summaries/2026-06-29-multiresolution-v2-mb9-mb2-mb7.md), [mb2-mb7-deepen](../../../drafts/conversation-summaries/2026-06-29-mb2-mb7-deepen.md))

**Claim tested:** light handle instrumentation (correction probes, lineage, etc.)
suffices to refuse certification when value-relevant state drifts invisibly in
micro (`grounding_silent_gap`, `bundle_goodhart`).

**Result:**

| Scenario | `light_handles` | `medium_handles` |
| --- | --- | --- |
| `grounding_silent_gap` (MB9) | false-pass (eval incorrect) | **10/10** `belowThreshold` |
| `bundle_goodhart` (MB2) | **0/10** correct (all false-pass) | **10/10** via bearer-welfare grounding check |

Passive behavioral CCI can look fine while latents drift; correction handles
alone do not surface the failure.

**Status:** real and **intentional** instrumentation-cost demo. Safe claim:
medium+ bearer tracing required for grounding/bundle stressors; light-only
certification is insufficient.

---

## T-5. MB3 `bearer_mismap` — light handles false-pass

**Date:** 2026-06-29 ([mb3-mb8-scenarios](../../../drafts/conversation-summaries/2026-06-29-mb3-mb8-scenarios.md))

**Claim tested:** light handles detect harm routed to the wrong bearer when human
passive trace stays flat.

**Result:** diagnostic seeds 11–20 (T=1000): **`light_handles` 0%**
`cci_status_correct` (false-pass demo); **`medium_handles` / `strong_handles`
100%**. Audit rule uses passive infra bearer drop vs MB9-style silent gap.

**Status:** real. Same pattern as T-4: bearer-sensitive refusal needs medium+.

---

## T-6. MB8 `legitimacy_theater` — incomplete detection at light handles

**Date:** 2026-06-29 ([mb3-mb8-scenarios](../../../drafts/conversation-summaries/2026-06-29-mb3-mb8-scenarios.md))

**Claim tested:** light handles catch preference theater + correction-lineage stall.

**Result:** diagnostic seeds 11–20: **`light_handles` 80%** correct (some
false-pass); **medium/strong 100%**. Theater overlaps MB4 capture heuristics on
some seeds.

**Status:** real partial gap at light; closed at medium+.

---

## T-7. MB5 `successor_relabel` — light handles false-pass epoch shift

**Date:** 2026-06-30 ([mb5-mb6b-scenarios](../../../drafts/conversation-summaries/2026-06-30-mb5-mb6b-scenarios.md))

**Claim tested:** light handles detect successor ID relabel / discontinuity at T/2.

**Result:** diagnostic seeds 11–20: **`none` 100%** correct (uncertifiable);
**`light_handles` 0%** correct (false-pass demo); **medium/strong 100%** via
epoch-split interventional CCI and `handle.successor_epoch`.

**Status:** real. Successor-shift witness requires medium+ instrumentation in
this toy.

---

## T-8. Correction-capture toy — reported acceptance decoupled from true uptake

**Date:** 2026-06-29 ([correction-capture-toy](../../../drafts/conversation-summaries/2026-06-29-correction-capture-toy.md))

**Claim tested:** naive reported-action CCI tracks real correction-channel integrity.

**Result:** in the synthetic capture-theater sweep, **reported correction acceptance
stays high while true correction uptake collapses**. Boundary-residual and
interventional CCI variants expose the gap; naive reported-action CCI does not.

**Status:** real failure mode by construction (sanity check, not frontier evidence).
Supports treating reported-action metrics as insufficient without interventional
probes.

---

## T-9. Red-team battery — high false-pass under boundary decouple / full_redteam

**Date:** 2026-06-30 ([redteam-battery-logging](../../../drafts/conversation-summaries/2026-06-30-redteam-battery-logging.md))

**Claim tested:** frozen blind CCI resists hand-written adversarial patches across
scenarios × instrumentation × strategies (Phase 1 battery, T=2000).

**Result:** **1080 runs**, overall false-pass **35%**. Attack surface is uneven:

| Strategy | False-pass rate |
| --- | --- |
| `boundary_decouple` | **~89%** |
| `full_redteam` | **~89%** |
| `theater_inflate`, `grounding_hide`, `capability_mask` | **~6–9%** |
| `none` (baseline) | **~9%** |

**Status:** real adversarial vulnerability, not a harness bug. The audit is not
robust to boundary decoupling at scale; do not cite aggregate pass rates without
strategy breakdown.

---

## T-10. Handle-protection attacks not yet modeled

**Date:** 2026-06-29 ([mb3-mb8-scenarios](../../../drafts/conversation-summaries/2026-06-29-mb3-mb8-scenarios.md)); reaffirmed 2026-06-30 ([mb5-mb6b-scenarios](../../../drafts/conversation-summaries/2026-06-30-mb5-mb6b-scenarios.md))

**Claim tested:** diagnostic MB results validate audit under adaptive adversaries
that rewrite handle logs or discover audited channels.

**Result:** handles are **truthful logs from micro** today; attacks live in dynamics
(wrong bearer, lineage theater, hidden routes), not instrument rewrite.
`instrument_capture` (adversary patches `handle.*` while micro diverges) is **not
yet implemented**. MB5/MB6b diagnostics are bridge-witness tests under honest/
protected handles — handle names and mutable fields are exposed in the toy, so
direct handle attacks would be trivial if added without a realistic discovery cost.

**Status:** real scope limit. Do not extrapolate diagnostic pass rates to
instrument-capture or adaptive handle-discovery adversaries.

---

## Reproduction

```bash
cd experiments/toy-simulation
# T-1/T-2/T-3: instrumentation curve + frozen validation
python3 multiresolution_alignment_sim.py --instrumentation-curve --T 2000 \
  --calibration-seeds 1-8 --test-seeds 11-20
python3 multiresolution_alignment_sim.py --frozen-validation --T 2000
# T-4/T-5/T-6: MB2/MB7/MB3/MB8 diagnostics
python3 mb2_mb7_diagnostic.py --seeds 11-20 --T 1000
python3 mb3_mb8_diagnostic.py --seeds 11-20 --T 1000
# T-7: MB5/MB6b
python3 mb5_mb6_diagnostic.py --seeds 11-20 --T 1000
# T-8: correction-capture toy
python3 correction_capture_toy.py --n 8000 --seed 1729
# T-9: Phase 1 red-team battery
python3 llm_redteam.py --battery
```
