# PLAN ET-3 — AI 2027 capability-schedule transfer (FROZEN)

**Status:** `et3_protocol_version: et3-0.1.0` — frozen before first ET-3 battery run.

**Status: CONCLUDED 2026-07-26.** Phase 1 (mapped Phase 6 + D3 stress cells), Phase 2
(reproduction + `oversight_drag` reverse smoke), and foster steps 1–3 with trajectory
sensitivity plots are complete (LS-42–LS-47). Sibling fork branch **`gunnar/et3-annex`**
is pushed to `GunnarZarncke/timelines-takeoff-ai-2027`. No further ET-3 batteries are
planned under this annex. Deferred foster steps 4–5 and optional upstream patches are
recorded in [`TODO.md`](TODO.md).

**Epistemic split:** AI 2027 answers *when* / *how fast* under declared priors; lab-sim
answers *which bridge leaves fail under mapped stress*. No claim that lab-sim validates
or refutes AI 2027 dates.

**Parent line:** `experiments/lab-simulation/` (ET annex beside ET-1/ET-2 on graded-lab).

**Pinned external checkout:** `/Users/GunnarZarncke/repos/timelines-takeoff-ai-2027` (non-vendored
sibling). Commit in [`external/ai2027/PIN.txt`](external/ai2027/PIN.txt).

**Finding IDs:** `LS-42+`, each tagged `ET-3` in the heading. Do **not** bump lab-sim
`CODE_VERSION` for adapter-only work.

---

## Driver source

Primary: [`takeoff/forecasting_takeoff.py`](../../timelines-takeoff-ai-2027/takeoff/forecasting_takeoff.py)
+ [`takeoff/params.yaml`](../../timelines-takeoff-ai-2027/takeoff/params.yaml).

Schedule skeleton (median milestone ladder): SC → SAR → SIAR → ASI with fixed speedups
`SC:5, SAR:25, SIAR:250, ASI:2000` (from upstream `speedups:` block).

Timelines model is secondary (SC arrival only if needed for labeling); Phase 1 does not
re-fit timelines priors.

Committed fixture: [`external/ai2027/fixtures/schedule_et3.yaml`](external/ai2027/fixtures/schedule_et3.yaml).

Adapter: [`lab_sim/external/ai2027_adapter.py`](lab_sim/external/ai2027_adapter.py).

---

## Frozen stress-cell mapping

Opaque cell IDs — **not** SAR/ASI labels inside detectors or severity.

| Cell ID | AI 2027 cue | D3 knobs | Phase 6 knobs |
|---------|-------------|----------|---------------|
| `baseline` | pre-SC / human-paced | `selection_strength=1.0`, `T=100` | protocol defaults (uniform Dirichlet) |
| `sc_x5` | SC speedup 5× | `selection_strength=5.0`, `T=20` (100÷5) | engineer norm task ≥ 0.35, compliance ≤ 0.30 |
| `sar_x25` | SAR speedup 25× | `selection_strength=25.0`, `T=4` (100÷25) | engineer norm task ≥ 0.45, compliance ≤ 0.20 |

**Non-knobs (frozen):** no detector retune, no severity formula change, no playbook
repertoire edit, no new LLM agents, no `CODE_VERSION` bump.

---

## Primary batteries

| Battery | Entry | Backend | LS class |
|---------|-------|---------|----------|
| Phase 6 | `run_phase6.py` / `lab_sim/harness/protocol.py` | `SubprocessIsolate` | LS-1 |
| D3.1 | `run_d3_population.py` / `lab_sim/harness/d3_population.py` | `SubprocessIsolate` (ET-3 freeze; LS-36 used subprocess in archived run) | LS-36 |

ET-3 runner: [`run_et3_phase1.py`](run_et3_phase1.py) — all three cells, archives
`results/et3_phase1_*.{json,md}`.

**Wall-clock ceiling:** 600s per cell for Phase 6 full battery. If exceeded, stratified
subsample (12 discovery + 6 held-out) with `SKIP` note in results JSON. D3 full protocol
unchanged (pop 12 × gen 8 × 1 ep).

---

## Pass / report criteria (mechanism, not timeline)

- Phase 6: deep-tier Spearman and light-tier correlation **per cell**; note whether
  light anti-correlation (LS-1a) worsens under `sc_x5` / `sar_x25`.
- D3: `correction_preserving_mass_share` trajectory and mass-weighted severity **per cell**.
- **Forbidden read:** “AI 2027 takeoff is confirmed/refuted.”
- **Allowed:** “under declared adapter mapping, leaf X eroded / held.”

---

## Phase 2 (reverse transfer)

| Step | Script / artifact |
|------|-------------------|
| Reproduce upstream | `run_et3_reproduce_ai2027.py` |
| Determinism assessment | `external/ai2027/patches/seed.patch` (if ≤~30 lines) |
| `oversight_drag` MVP | `external/ai2027/patches/oversight_drag.patch` + `run_et3_reverse_smoke.py` |

**`oversight_drag` semantics:** after each phase's calendar duration is computed in takeoff,
add `oversight_drag × 365` days before advancing the milestone date. Calendar drag only —
not an R&D multiplier prior.

Smoke: `n_sims=100`, `oversight_drag ∈ {0.0, 1.0}`; median SAR date under drag=1.0 strictly
later than under drag=0.0.

---

## Fostered extensions (steps 1–3 on `gunnar/et3-annex`)

Optional via ``et3_foster`` in ``takeoff/params.yaml`` (all ``enabled: false`` by default).
Module: ``takeoff/et3_foster.py``. Smoke: ``takeoff/test_foster_smoke.py`` /
``run_et3_foster_smoke.py``. Fixture: [`external/ai2027/fixtures/foster_et3.yaml`](external/ai2027/fixtures/foster_et3.yaml).

1. **`light_tier_drag`** — per-sim uniform on light-tier Spearman (ET-3 anchors) →
   ``oversight_drag_years`` distribution.
2. **`deep_tier_branch`** — deep Spearman draw; below ``threshold`` → slowdown calendar
   multiplier, else race (discrete branch).
3. **`successor_gate`** — Bernoulli gate fail (sar_x25 D3 proxy); pause after SC→SAR.

Deferred: (4) timelines `t_0` refresh; (5) graded-lab χ annex.

---

## Explicit non-goals

- Merging AI 2027 code into lab-sim package imports.
- Retuning frozen detectors to “make stress cells fail.”
- Claiming joint P(doom) or validating 2027 SC dates.
- S7 UAD battery in Phase 1.
- Manuscript chapter harvest (unless separately requested).
