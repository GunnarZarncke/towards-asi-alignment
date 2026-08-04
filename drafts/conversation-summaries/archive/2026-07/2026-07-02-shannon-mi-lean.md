# 2026-07-02 — Real Shannon entropy/mutual-information proved in Lean (`ShannonMI.lean`)

## Trigger

Continuation of the day's Lean-precise-bounds thread. User asked to plan next steps for strengthening the measurement protocol; a `CreatePlan` cycle produced a Python-first plan (bootstrap CIs, lag/direction probe scan, population-calibrated thresholds — see `.cursor/plans/strengthen_measurement_protocol_940d8c38.plan.md`, left untouched for later). User then redirected: "Because the experiments are blocked by parallel work, let's take a shot at formalizing in Lean first (leave the plan as is for later)." This session is that Lean-side shot, done in Agent mode (not re-planned, per the user's explicit "take a shot" framing).

## Done

**New module `formal/AlignmentProofSpine/Field/Finite/ShannonMI.lean`** — a real-valued (`noncomputable`) Shannon entropy/mutual-information development, proved from Mathlib's convexity API rather than assumed or only checked empirically:

- Surveyed Mathlib first (no wasted effort assuming infrastructure that doesn't exist): no general finite Shannon entropy/MI anywhere (only `Analysis/SpecialFunctions/BinaryEntropy.lean`'s single-Bernoulli-parameter `binEntropy`, and a measure-theoretic KL-divergence framework in `InformationTheory/KullbackLeibler/` too heavy for finite discrete data). Found the right building blocks instead: `Real.negMulLog` (`x ↦ -x log x`, `Analysis/SpecialFunctions/Log/NegMulLog.lean`, including the algebraically crucial `negMulLog_mul`), `strictConcaveOn_log_Ioi`, and `ConcaveOn.le_map_sum` (finite Jensen's inequality).
- `shannonEntropy p := ∑ a, Real.negMulLog (p a)`; `shannonEntropy_nonneg`.
- **`shannonEntropy_le_log_card`**: maximum-entropy bound `H(p) ≤ log (Fintype.card α)`, via one Jensen application (weights `p`, points `1/p(a)` on the support).
- `jointEntropy`, `marginalX`, `marginalY`, and the harder **`shannonEntropy_marginalY_le_jointEntropy`** (`H(Y) ≤ H(X,Y)`, i.e. conditional entropy `H(X|Y) ≥ 0` without naming a separate conditional-entropy object): for each `y`, split `p(x,y) = r_y(x) · p_Y(y)` via the per-slice conditional distribution `r_y`, expand `negMulLog(p(x,y))` termwise with `negMulLog_mul`, and show the gap collapses to `p_Y(y) · H(r_y) ≥ 0`. Symmetric `shannonEntropy_marginalX_le_jointEntropy` by transposing `p`.
- `mutualInformation p := H(X) + H(Y) - H(X,Y)`; `mutualInformation_le_shannonEntropy_marginalX/Y`.
- **`mutualInformation_le_log_min_card`**: for any finite joint distribution over alphabets of size `m`, `n`, Shannon MI (nats) `≤ log min(m,n)`. This is the real-Shannon-theoretic fact underneath the N-8 empirical finding (this same day, `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`) that the *appearance ceiling* (not the counting *score*) is a sound Shannon-MI bound — proved for **any** distribution, not just observed with 0 violations on one fixture's pairs/lags.
- Axiom footprint checked before finalizing: `#print axioms` on both headline theorems gives only `propext`, `Classical.choice`, `Quot.sound` — no `sorryAx`, no bespoke axioms.
- Registered in `formal/AlignmentProofSpine/Field.lean` (import list, alphabetically next to `PMF`).

## Decisions

- **Approach chosen after checking feasibility, not assumed.** Full exact rational-arithmetic MI computation (`decide`-checkable numeric bits on trace data) was considered first but rejected as infeasible without building a certified rational log₂-approximation from scratch (Real.log is noncomputable/non-decidable; no Mathlib machinery for that). Chose instead: prove the *general real-valued Shannon-theoretic bound* — tractable via existing Mathlib convexity lemmas, and still a genuine strengthening (the previous state had this fact checked only empirically in Python, not proved).
- **Scope disclosed, not silently left implicit**: the module docstring, `TraceBIQ.lean`'s docstring, `formal/README.md`, `metadata/TODO.md`, and the appG paragraph all say the same thing — this is real-valued/noncomputable and **not yet wired** to `DiscreteTrace`'s decidable rational pipeline. No `decide`-checked numeric MI value on actual trace data exists yet; that wiring (empirical rational PMF from lagged trace pairs → `mutualInformation` → numeric cross-check against `calibrate_trace_biq.py`) is recorded as an open TODO, not attempted this session.
- **TraceBIQ.lean's stale docstring pointer fixed**: it previously said "Real MI estimation lives in `Field/Finite/PMF.lean` when probability data is available" — that was aspirational and wrong (`PMF.lean` only has quantilizer machinery, zero MI content). Corrected to point at the new `ShannonMI.lean` module, with the noncomputable/not-yet-wired caveat attached.
- **Python-first plan explicitly left untouched** per the user's instruction — `.cursor/plans/strengthen_measurement_protocol_940d8c38.plan.md` still exists for a later session, unstarted.
- **Appendix G updated surgically**: one clause added to the existing worked-instance paragraph (§`appi:sec:trace-attended-harm` reference), not a new paragraph — the existing N-8/ceiling sentence now cites the Lean proof rather than only "as theory requires" hand-waving.

## Verification

- `lake env lean` on an iteratively-debugged scratch file first (standard practice for new Lean proofs in this repo), then moved to the permanent module once clean.
- `lake build` (2240 jobs) — full project green, only pre-existing warnings (none new).
- `./build.sh` (with `PAR_GLOBAL_TMPDIR`) — manuscript PDF rebuilds clean with the new appG sentence.
- `make check` — structure/citation/bibliography-summary checks pass.

## Open / next

- **Wire to trace data** (recorded in `metadata/TODO.md`'s TraceBIQ row): build an empirical rational PMF from lagged `DiscreteTrace` column pairs, feed it through `mutualInformation`, and numerically cross-check the resulting bound against `calibrate_trace_biq.py`'s plug-in Shannon-MI estimates on the same pinned fixture data. This would let a future worked instance cite an actual `decide`/`native_decide`-checked MI number, not just the existence proof that one is bounded.
- The Python-first measurement-protocol plan (bootstrap CIs, lag/direction probe scan, population-calibrated thresholds) remains queued, unstarted, at `.cursor/plans/strengthen_measurement_protocol_940d8c38.plan.md`.
- `shannonEntropy`/`mutualInformation` are not added to `formal/axiom-ledger.json`'s curated 17-theorem list — consistent with existing curation practice (the ledger tracks headline risk-bound-chain theorems, not every supporting lemma); revisit if/when this module is wired into a certificate path.

## Key paths

- `formal/AlignmentProofSpine/Field/Finite/ShannonMI.lean` (new)
- `formal/AlignmentProofSpine/Field.lean` (import added)
- `formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean` (docstring pointer fixed)
- `formal/AlignmentProofSpine.lean`, `formal/README.md` (module maps updated)
- `metadata/TODO.md` (TraceBIQ row, Lean-side Shannon MI update)
- `appendices/appG-lean-proof-spine.tex` (one sentence, worked-instance paragraph)
- `.cursor/plans/strengthen_measurement_protocol_940d8c38.plan.md` (untouched, queued)

## Commits

- `2053579` — Prove real Shannon entropy/mutual-information bounds in Lean (ShannonMI.lean).
