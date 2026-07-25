# Plan: RiskGap unit hygiene, vector-gate primacy, and foregrounding the existing MB11 acceptance gate

**Status (2026-07-20):** P1's rename half, P2, and P3's prose are **done** (commit pending). P1's vector-primacy-refactor half turned out to require unweighting `CCI` itself, not just `Certification.lean` — see "Finding" below — and is deferred to backlog per explicit user decision, not attempted this session.

## Problem summary

1. `Risk A := Control A − CCI A` names a conclusion ("risk") on a bare subtraction — the "primary numeric risk bound" is a renaming, not a derivation (hostile-review point).
2. `CCICertificate.lambdaProjection` sums heterogeneous-unit coordinates (capacity in bits/window, manipulation as a count, latency as a time, translation loss as a score) into one `Int` via unstated λ exchange rates. This is where "fake arithmetic" actually bites, once inspected.
3. `CCICertificatePasses` (componentwise threshold gate, no summation) is already the honest vector-bound pattern and already the one the WorkedInstance exercises with real fixture data — but it is not the primary path into `RiskGap`/`Risk`; the scalar projection is.
4. Nothing in the spine outputs a probability of failure or an expected value loss — the quantities are all information/capacity-theoretic (bits/window) or raw counts. That translation is the actual thing a reader will ask for, and it is currently absent, not faked — it should stay absent and be named, not retrofitted with unsupported arithmetic.

## Design decisions carried forward from the thread

- No pricing/exchange-rate axiom for λ weights. Instead, **demote scalar `CCI`/`lambdaProjection` to an illustrative secondary path**; promote the vector gate (`CCICertificatePasses`) to the primary certification object.
- `RiskGap`'s capacity coordinate (`Control` vs. `rawCapacity`) is the only place a *subtraction* is dimensionally sound (both bits/window) — keep that. **Fully rename `Risk` → `RiskGap`, everywhere, no deprecated alias.** Two names for one subtraction is exactly the confusion the original critique flagged; adapt every reference (Lean, `.tex`, metadata) rather than keep a compatibility shim.
- Reject function-valued bounds (moduli, `BoundingScheme`, envelope functions) for now: no upstream producer in the proof tree has more than one instance to apply them to (single `FilterFamily`, no per-step gain producer). Record the generalization in commentary only ("rent test": a function-valued bridge input must be applied at ≥2 distinct arguments or composed through a lemma that uses its structure, or it's a constant in costume).
- Reject constraint-set reification: `CCICertificatePasses` already *is* the constraint set; a reflected/first-class version has no proof-tree consumer today.
- **Failure-probability / value-loss: no new quantitative bridge.** An earlier draft of this plan proposed `FailureProbability : System → Rat` plus a monotone-dependence axiom — this fails the same rent test used to reject moduli (no upstream producer for a real-deployment probability). The framework already has the honest answer: `WithinDeploymentRiskTolerance : System → Int → Prop` + `MB11_safety_case_adequacy` (`formal/AlignmentProofSpine/Certification.lean`), a **Prop-valued acceptance gate** reaching `Safe A`, docstring-explicit that "nothing in this development pretends to prove it." Use that, don't invent a number. The toy-ecology angle survives in weakened form: an episode-battery pass/fail rate can instantiate a *decidable* `WithinDeploymentRiskTolerance` for a toy system, still a gate, no invented probability.

## Finding that changed scope mid-implementation (2026-07-20)

`CCI` is **not** merely projected-to by a weighted certificate scalar; `CCI` itself is *defined* at the `System` level as the weighted quantity:

```965:968:formal/AlignmentProofSpine/Correction.lean
noncomputable def CCI (A : System) : Int :=
  (SystemCorrectionPath A).weakestLink -
  CCIPenaltySum (CCIPenaltyWeightsSys A) (CCIPenaltiesSys A)
```

This is ch46's own equation (`eq:cci-ch46`), and `CCICertificateMeasures.weights_eq` forces the certificate's `lambdaProjection` to use the *same* weights, so certificate and system-level pricing agree by construction — no inconsistency, but the pricing commitment itself is real and is inherited by every consumer of `CCI` (`RiskGap`, `MB6b`, `MB7c`, `S10`, every chapter/appG citation), not just by `Certification.lean`'s scalar route. Making the vector gate (`CCICertificatePasses`) the *primary* certification quantity — as P1 originally proposed — would therefore require introducing a new, unweighted System-level quantity and rewiring every bridge that currently reads `CCI`, not a local `Certification.lean` change. Given that blast radius, this was moved to backlog (below) rather than attempted in this session; user confirmed "stop here" when asked.

## Priority order

### P1 — Full `Risk` → `RiskGap` rename (Certification.lean, Capability.lean, Successors.lean, Forgeability.lean, TraceBIQ.lean, WorkedInstance.lean) — **done**
- **Full rename, no alias**, across `formal/**/*.lean`, `appendices/appG-lean-proof-spine.tex`, `appendices/appD-worked-example.tex`, `chapters/ch33-certification-without-construction.tex`, `chapters/ch42-safety-case.tex`, `chapters/ch48-towards-alignment.tex`, `formal/README.md`, `metadata/assumptions-ledger.md`, `formal/axiom-ledger.json`. Deleted `Risk`, `Risk_eq_RiskGap`, and the duplicate `Risk`-named theorems that existed only to restate the `RiskGap` versions under the old name (`risk_bound_successor_safe_step`, `risk_bound_along_successor_measurand_chain`, `risk_bound_along_successor_safe_chain`, `risk_le_delta_of_cci_slack`). Renamed the remaining non-duplicate `risk_*` theorems to `risk_gap_*` for consistency (`risk_gap_bound_from_cci_slack`, `risk_gap_bound_from_vector_supported_slack`, `risk_gap_bound_from_threshold_certified_cci`, `risk_gap_le_delta_of_witness`, `risk_gap_bound_from_biq_ceiling`, `BIQCapacityCertificate.risk_gap_bound`, `risk_gap_bound_from_hidden_biq_certificate`).
- Also fixed the same "two names for one subtraction" pattern in the manuscript prose itself: `chapters/ch33-certification-without-construction.tex` had the identical `\mathrm{Risk}(A) = \mathrm{RiskGap}(A)` redundant equation (`eq:risk`), removed along with its 3 `appG` citations.
- `formal/LeanProofSpineImplementationBrief.md` intentionally **not** touched: it is a superseded Lean-3-syntax design brief (`constant Risk : System → Int`), not synced with the current implementation, and rewriting historical planning docs is out of scope.
- Verification: `lake build` (2250/2250, clean except two pre-existing unrelated warnings), `python3 scripts/check_axiom_budget.py` (37 theorems, no drift — one ledger entry name updated to match the rename), `make check` (structure/citations/bib-summaries all pass).
- **Not done** (see Finding above, moved to backlog): making `CCICertificatePasses` the primary path that bypasses weighted `CCI` for the capacity coordinate. What *is* already true and unchanged: `CCICertificatePasses` never sums cert coordinates against each other (each checked against its own threshold independently), and it is a required hypothesis of every route to the weighted floor — it just doesn't yet replace `CCI` as the thing `RiskGap` is computed from.

### P2 — Threshold-provenance note (prose only, no Lean) — **done**
- Added to `formal/README.md`: `CCIThresholds` (`θ`) is a deployment-specific empirical/policy input with its own measurement-protocol crux, same epistemic class as `MB1`'s estimator soundness, not something the arithmetic discharges.

### P3 — Foreground `MB11`/`WithinDeploymentRiskTolerance` as the answer to "what do you actually get" (prose only) — **done** (Lean wiring deferred with the P1 vector-primacy half)
- No new bridge, no new quantitative type added. `MB11_safety_case_adequacy` + `WithinDeploymentRiskTolerance` (already in `Certification.lean`) is the honest Prop-valued gate that reaches `Safe A`.
- Prose added to `formal/README.md` and `metadata/assumptions-ledger.md`: the framework's answer to "probability of failure / quantified value loss" is a Prop-valued acceptance gate (`Safe`, reached only through `MB11` + a named, ungrounded tolerance judgment), not a number — a deliberate epistemic choice, not a gap to be closed by more arithmetic.
- Lean wiring (making the vector-gate flow into `MB11`'s hypothesis) is deferred along with the vector-primacy refactor above, since there is currently no separate vector-gate `CertifiedSafetyCase` variant to wire in.

### P4 — Toy instantiation of `WithinDeploymentRiskTolerance` (optional, larger, separate task)
- Wire one existing embedded-simulation or lab-simulation episode-battery statistic (fraction of episodes where a detector/certificate fails, compared against a pre-registered threshold) as a *decidable* instance of `WithinDeploymentRiskTolerance` for a toy system — still a gate (pass/fail), not an invented probability number.
- Only attempt after P3 lands and only if there's a clean existing battery output to point at without new experiment code.

## Backlog (not prioritized, needs further discussion before starting)

- **Unweight `CCI`'s primary path (was P1's vector-primacy refactor; deferred 2026-07-20 — see Finding above).** Introduce a new, unweighted System-level quantity (e.g. `rawCapacityFloor : System → Int`, sourced from `CCICertificate.rawCapacity`/`θ.minRawCapacity` directly, no λ) and give `RiskGap`/`NumericRiskLeaf`/`CertifiedSafetyCase` an alternative construction path through it instead of through weighted `CCI`. Requires touching `Correction.lean`'s `CCI` consumers (`MB6b`, `MB7c`, `S10`) and re-deriving which of `MB6b`/`MB7c` still typecheck against the new quantity — size this properly (likely its own session) before starting; do not fold into a "quick" pass.
- Phantom unit types (`Qty (u : Unit)`) for `Control`/`CCI`/coordinates — useful if/when more unit-mixing bugs turn up; deferred because P1's vector-primacy refactor removes the one unit-mixing case found so far without needing new types.
- Gate × payload generalization beyond `CCICertificate` (e.g., applying the same pattern to `BoundaryMarginCertificate` or other certificates) — revisit once P1 is done and the pattern is proven out once.
- Rate-indexed "capability gain doesn't outrun control" lemma in `Successors.lean` — blocked on a per-step gain producer; no current source. Note only, no Lean object, until such a producer exists (e.g., a TraceBIQ-style per-window capability delta).
- Multi-resolution `FilterFamily` ordering (would unblock moduli-style MB7b bounds) — out of scope unless the multi-resolution UAD prose gets formalized separately.
- Value-loss (expected harm in utility units) version of the failure bridge — blocked on a `System`-level utility function that does not exist; do not add speculatively.
- Full re-audit of which appG/chapter prose cites scalar `CCI`/`Risk` by name and needs updating once P1's primary path changes (mechanical but must be complete, not partial, to avoid drift between Lean and prose).

## Non-goals

- No probabilistic tail-bound machinery (`Finite/PMF`-based confidence bounds) added speculatively; only if/when a real estimator-soundness bridge (MB1) needs it.
- No new abstraction (`BoundingScheme`, moduli, constraint-set reflection) without a concrete second instance already in hand at design time.
