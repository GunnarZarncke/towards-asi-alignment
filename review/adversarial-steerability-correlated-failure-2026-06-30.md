# Reviewer Feedback — Correlated Steerability Failure & Operationalization Deferral

Recorded 2026-06-30. External reviewer feedback (claim-strength / structural, not a localized bug report). Preserved verbatim structure from the review output format in `REVIEWING_FOR_AGENTS.md`.

---

## High-Severity Issues

### Correlated failure across the whole apparatus (claim-strength, not a bug)

- **Path:** ch07 §WWCTV, ch46 §WWCTV, ch46 §WWCTV, ch48 §WWCTV, cross-ref `appendices/appB-bridge-crosswalk.tex` §takeaway.
- **Problem:** Every chapter's strongest self-objection is the same one: the measurand is steerable. Ch7 — "the boundary residual is not merely noisy but steerable; a system that models the observer shapes its own residual." Ch37 — "a system launders goals with the index reading zero; the detector's features are the launderer's constraints, not its tell." Ch19b and ch46 say the structurally identical thing. So boundary residual, bundle probes, the laundering index, and successor closure don't fail independently — they share the antecedent (adversarial verifiability), which the bridge appendix itself concedes "positively correlate the bridges."
- **Why it matters:** The appendix claims disjunctive routes (MB6b or MB8) "add failure tolerance." If the disjuncts share the steerability antecedent, that tolerance is largely illusory — the chokepoint failure takes the whole chain down together. The framework's honesty about each local failure obscures that the failures are one failure.
- **Acknowledged by author:** Partially. Each local case is flagged; the correlation across them is not drawn out as a single load-bearing risk.
- **Suggested fix:** State explicitly that the bridges are conjunctive-through-a-shared-chokepoint, and weaken the "disjunctive routes add failure tolerance" language accordingly, or show the disjuncts have independent antecedents.

**Related prose (added 2026-06-28, now under review):**

- `appendices/appB-bridge-crosswalk.tex` takeaway — shared antecedents positively correlate bridges; disjunctive routes (MB6b ∨ MB8) add failure tolerance.
- `appendices/appF-research-program.tex` §`sec:research-dependency-order` — "Disjunctive routes add failure tolerance" paragraph.

**WWCTV loci to reconcile:**

| Measurand / layer | Chapter | WWCTV objection shape |
|-------------------|---------|------------------------|
| Boundary residual \(J\) (from \(R, P, \Omega\)) | ch07 | Observer-modeling steers the residual |
| Bundle probes / Goodhart geometry | ch46 | Probes are optimization constraints |
| Successor closure / conserved-property score | ch46 | Forgeable under adversarial predecessor |
| Goal-laundering index GLI (\(d_G, d_\Phi\), CCI, \(D_{\text{succ}}\)) | ch48 | Detector features are launderer's constraints |

**Shared antecedent:** adversarial verifiability / measurand steerability (ch47 vocabulary); see also U-03, U-05, U-14, U-16 in `metadata/uncertainty-ledger.md`.

---

## Medium-Severity Issues

### Operationalization-by-deferral ("turtles")

- **Path:** ch48 §Laundering Index (GLI built from \(d_G\), \(d_\Phi\), CCI, \(D_{\text{succ}}\)), ch07 §Boundary Residual (\(J\) built from \(R\), \(P\), \(\Omega\)).
- **Problem:** Each composite quantity is defined in terms of sub-distances that are themselves defined in other chapters, and the chain bottoms out — in the Lean spine — in `Int` proxies and `Toy… := True` predicates. No layer is yet a measured number.
- **Acknowledged by author:** Yes, repeatedly (the spine README, the MB-bridge isolation).
- **Suggested fix:** A single table mapping each composite index to the concrete estimator and dataset that would instantiate it (the `experiments/toy-simulation/` harness is the natural home; the `mb*_diagnostic.py` scripts already gesture at this).

**Composite indices needing an estimator ↔ dataset row:**

| Composite | Sub-components (deferred to) | Candidate experiment hook |
|-----------|------------------------------|----------------------------|
| Boundary residual \(J\) | \(R\), \(P\), \(\Omega\) (ch06–07, ch09) | `correction_capture_toy.py`; multiresolution `boundary_alias` |
| GLI | \(d_G\), \(d_\Phi\), CCI, \(D_{\text{succ}}\) (ch46, ch46, ch48) | ch48 not yet in sim; CCI from `cci_audit.py` |
| CCI (vector / scalar) | Penalties \(L,M,R,\Omega\) (ch46) | multiresolution audit path |
| Conserved-property / successor score | Seven properties (ch48) | `mb5_mb6_diagnostic.py`, `successor_relabel` |
| Bundle-geometry probes | ch16–19b catalogue | `bundle_goodhart` scenario |

---

## Claim-Strength / Bridge Issues

- The 2026-06-28 composition argument (appH §`sec:research-dependency-order`, crosswalk takeaway) may have **overstated** disjunctive failure tolerance relative to the shared steerability chokepoint. Reviewer accepts positive correlation via shared antecedents but rejects the implication that MB6b ∨ MB8 yields robustness when both disjuncts (and the conjunctive spine) fail under the same adversarial-measurement attack.
- **Decision needed:** downgrade disjunctive-tolerance prose *or* demonstrate independent antecedents for at least one disjunct (e.g. MB8 legitimacy theater vs MB6b basin lock-in under instrument capture).

---

## Evidence / Source Gaps

- No single manuscript table links composite indices → estimators → datasets → toy-sim scenario / diagnostic script.
- Lean spine intentionally stops at bridges; reviewer asks for a **manuscript-facing** instantiation map, not only formal/README disclaimers.

---

## Residual Risk

Until the shared chokepoint is named as a single load-bearing failure mode (not N independent WWCTV caveats), readers may underestimate correlated collapse of the safety-case graph under adversarial optimization. Until the instantiation table exists, composite scores remain definitionally coherent but empirically unfalsifiable in practice.

---

## Tracking

- **TODOs:** `metadata/TODO.md` — BIG REVIEW (correlated steerability chokepoint); measurand instantiation table.
- **Experiments:** `experiments/toy-simulation/TODO.md` — composite-index ↔ estimator matrix.
- **Prior session:** ``drafts/conversation-summaries/RECOVERY.md` (session `2026-06-28-research-order-composition-argument.md`)` (source of the now-questioned disjunctive-tolerance language).
