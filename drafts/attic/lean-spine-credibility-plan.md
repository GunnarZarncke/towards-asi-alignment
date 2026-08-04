# Plan: Lean spine credibility — non-trivial certification, grounded tolerance, consistency model, Löbian contrast

**Status (2026-07-20):** P1–P4 **done**. P1: headline `risk_gap_bound_from_trace_profile` + `honest_instance_risk_bound` rewired. P2: `ToyDeploymentGate.lean`. P3: `SpineModel.lean` + `check_spine_model.py`. P4: `Field/Finite/LobTiling.lean`, a conditional Löb derivation, self-certifying tiling obstruction, and successor-audit contrast.

## Problem summary

The recent Lean changes **fixed structural honesty** (anti-capture representable, labeled bridges, `Safe` wired through `MB11`, `Risk`→`RiskGap`, field rederivations). A hostile reader who opens the spine today still hits four predictable objections:

1. **Headline certification is still definitional rearrangement.** `P13` / `risk_gap_bound_from_cci_slack` and the `certified_class_safety_*` assembly theorems conclude `RiskGap A ≤ δ` from a hypothesis that is already `Control A ≤ CCI A + δ` (or its vector-shaped equivalent). The proof is `unfold; omega`. Strategic advice item 4 asked for either honest pruning *or* at least one certification theorem whose proof term uses non-trivial structure.
2. **`WithinDeploymentRiskTolerance` is a named empty box.** Foregrounding it in prose helps authors; skeptics still see an ungrounded axiom with no example of what discharging it looks like on real or toy data.
3. **No published consistency witness.** The axiom budget guard tracks *which* axioms headline theorems depend on, but the repo does not exhibit a model showing the axiom set is satisfiable — that safety is not a theorem of the scaffolding alone — or that each labeled bridge is **independently** load-bearing (not redundant, not vacuously true, not collapsible into one another).
4. **Successor chapter vs. Löbian tiling is prose-only engagement.** ch30 cites Yudkowsky tiling and states import-preserving transport; `Bundles.lean` has the semantic/import counterexample. There is no Lean engagement with the Löbian / proof-theoretic obstruction (Yudkowsky–Herreshoff, Fallenstein–Soares) that alignment researchers expect on successor/self-modification topics.

These are **credibility and framing** gaps, not gaps in the book's conditional thesis. Closing them does not require proving deployment safety or discharging every `MB*` bridge.

## Design decisions

- **Rent test (carry forward):** every new Lean object must have ≥2 consumers in the proof tree, or be applied through a lemma whose structure is used — or it is a constant in costume. No speculative `FailureProbability : System → Rat`, no moduli without a per-step producer.
- **Non-trivial certification ≠ fancier arithmetic.** The fix is to promote a theorem whose *hypotheses* are trace- or certificate-level facts that are not restatements of the conclusion, so intermediate lemmas (Shannon MI, log-ceiling monotonicity, vector gate → scalar floor) must appear in the proof term.
- **Ground tolerance by example, not by axiom.** Do not add `WithinDeploymentRiskTolerance toyA δ` as a new axiom. Exhibit a decidable `EpisodeBatteryGate` (or similar) on committed battery output; docstring-explicit that discharging the global tolerance for a real deployment still requires a governance judgment that *this* battery at *this* threshold is the acceptance criterion.
- **Consistency model is signature + instance, not meta-proof.** Lean cannot prove its own global consistency from inside. The acceptable artifact is a `SpineModel` structure whose fields mirror the axiom statements, plus one trivial instance, one non-degenerate instance (`RiskGap > 0`, `¬ Safe` possible), and a **bridge-independence family** — one exhibited countermodel per labeled bridge showing that bridge is independently load-bearing — mechanically checked against the live axiom set and the axiom-budget ledger.
- **Löbian work stays in `Field/Finite/`, not on opaque `System`.** Same pattern as `BellmanQ.lean` / `ShutdownIncentives.lean`: real derivation where possible; one labeled hypothesis for the genuinely hard step (diagonalization / fixed point); explicit contrast theorem showing `SuccessorAuditLinks` avoids the Löbian hypothesis by using measured inequalities instead of internal provability.

## Priority order

Recommended execution order: **P4 → P1 → P2 → P3** (Löbian contrast first for credibility-per-hour; P3 is mechanical but tedious).

### P1 — Non-omega headline certification theorem

**Goal:** One certification-path theorem that a reviewer can inspect and see non-definitional work — without changing what the framework claims.

**Approach:**

1. **Identify existing derivational content** (already in repo, not on the headline path):
   - `Field/Finite/ShannonMI.lean` — real entropy / MI bounds.
   - `Field/Finite/TraceBIQ.lean` — `traceMarkovBlanketBIQProfile`, `traceActionCapacityBits`, `traceControlDiversity`, `traceDerivedCCISlack`, `trace_derived_risk_bound` (currently ends in `P13` once `hslack : traceActionCapacityBits t B ≤ CCI A + δ` is assumed).
   - `WorkedInstance.lean` — `decide`d certificate pass/fail on committed fixture data.

2. **Add a composed theorem** (working name: `risk_gap_bound_from_trace_profile` or promote `trace_derived_risk_bound` + a new upstream lemma):
   - **Hypotheses:** a `DiscreteTrace`, `EnvBlanket`, `TraceBIQParams`, passing `TraceBIQProfileCertificate`, system equalities linking `Control`/`CactSys` to trace-computed measurands, passing `CCICertificatePasses` (or trace-derived slack facts), and **not** a bare `Control A ≤ CCI A + δ` as the only input.
   - **Proof must use:** at least one of `ShannonMI` capacity bound, `log2CeilBits_mono` / trace counting lemmas, and the vector-gate → scalar-floor chain (`CCIVectorSupportsScalarSlack.fromThresholdFloor` or trace analogue) before the final `P13` subtraction.
   - **Acceptance test:** deleting the MI or ceiling lemma breaks the proof; `#print axioms` footprint unchanged or narrower than current assembly theorems.

3. **Rewire presentation, not mathematics:**
   - Make this theorem the one `certified_class_safety_from_*` cites in docstrings and Appendix G's "headline certification" paragraph.
   - Add to `formal/scripts/check_axiom_budget.py` ledger if it becomes a headline theorem.
   - Optionally add a `WorkedInstance` corollary instantiating the composed theorem on the honest-baseline fixture (parallel to `honest_instance_risk_bound`).

**What does *not* count as success:**

- Longer chains of `omega` or induction that only propagate an inequality already assumed per step (`Successors.lean` style).
- Renaming `risk_gap_bound_from_cci_slack` without changing hypothesis shape.

**Size:** ~1 session (mostly rewiring; MI/trace machinery exists).

**Verification:** `lake build`; inspect proof term or `#check` that key lemmas appear; `check_axiom_budget.py`; `make check`.

---

### P2 — Ground `WithinDeploymentRiskTolerance` by example

**Goal:** Show what discharging the tolerance gate *looks like* on committed data, without pretending to prove the global axiom.

**Approach:**

1. **Define a decidable gate structure** in Lean (location TBD — `Certification.lean` companion section or `WorkedInstance.lean` / new `ToyDeploymentGate.lean`):

   ```lean
   structure EpisodeBatteryGate where
     nEpisodes : Nat
     nFailures : Nat
     maxFailures : Nat
   def EpisodeBatteryGate.passes (g : EpisodeBatteryGate) : Prop :=
     g.nFailures ≤ g.maxFailures
   -- instance Decidable (EpisodeBatteryGate.passes g) := ...
   ```

   Docstring: this is the *shape* of a deployment acceptance criterion (pass/fail on a pre-registered battery), not a probability estimate.

2. **Commit literals from an existing battery** — prefer pre-registered frozen validation:
   - Primary source: `experiments/embedded-simulation/results/embedded_frozen_validation.json` (`mode: frozen_validation`, fixed thresholds in `frozen_capture_rules`, validation seeds `[21, 22]`).
   - **Read `NEGATIVE_RESULTS.md` and the JSON first.** If the frozen battery fails or is ambiguous for the scenario chosen, publish that result — do not shop for a passing arm.
   - Alternative: lab-simulation episode battery if embedded output does not yield a clean pass/fail count without new parsing code.

3. **Prove `EpisodeBatteryGate.passes` by `decide`** on the committed `(nFailures, maxFailures)` pair; docstring cites source file path, git hash, scenario name, and threshold provenance.

4. **Do not axiomatize** `WithinDeploymentRiskTolerance A δ` for a toy system. Instead:
   - Add a theorem `toy_battery_gate_passes : EpisodeBatteryGate.passes toyGate` (pure data).
   - Prose in `formal/README.md`, `metadata/assumptions-ledger.md`, and optionally ch42/appG: the gap between `EpisodeBatteryGate.passes` and `WithinDeploymentRiskTolerance A δ` is exactly the governance judgment that this battery at this threshold is the deployment's acceptance criterion — same epistemic class as θ thresholds and `MB1`.

5. **Optional stretch:** a `CertifiedSafetyCase` + `EpisodeBatteryGate.passes` + explicit `WithinDeploymentRiskTolerance` hypothesis yields `Safe` via `P30_safe_of_case` — shows the *composition* without discharging the tolerance axiom.

**Size:** ~0.5–1 session (data selection + one small Lean module + prose).

**Verification:** `decide` proof succeeds; docstring traceability to JSON; no new axioms beyond existing `WithinDeploymentRiskTolerance` / `MB11`.

---

### P3 — Consistency model + bridge-independence family

**Goal:** Publish evidence that (a) the spine's axiom set is consistent, (b) `Safe` is not built into the scaffolding, and (c) **every labeled bridge is independently load-bearing** — each does empirical work the others do not substitute for.

**Bridge inventory (canonical checklist):**

| ID | Source | Typical consumer (for `#print axioms` link) |
|----|--------|---------------------------------------------|
| `MB1`–`MB9` | `Core.lean` / `BridgeAssumptions` | `certified_class_safety_from_spine_and_bridges`, layer-derivation paths |
| `MB4a` | `Correction.lean` | `CorrectionIntegrity_implies_*`, capture vs. legitimacy theorems |
| `MB10` | `Forgeability.lean` | `MB10_conserved_property_signature_not_forged` consumers, risk→true-harm corollary |
| `MB11` | `Certification.lean` | `P30_safe_of_case`, `safe_from_spine_inputs` |
| `S10` | `Capability.lean` | B-IQ measurand coherence chain (`IctrlSys_le_Cact`, …) |
| `WithinDeploymentRiskTolerance` | `Certification.lean` | paired with `MB11` (tolerance without case, or case without tolerance) |

Book assumptions `A-001`–`A-014` stay out of the finite toy unless a bridge maps 1:1; this plan targets **Lean bridge fields only**.

**Definition — independently load-bearing (operational):**

For bridge `B : Antecedent → Consequent` (or `∀ …, Antecedent → Consequent`), exhibit a toy `SpineModel` variant `m` such that:

1. **Scaffolding is live:** carriers and measurands are defined consistently (not all `Unit` / `0` / `True` unless that variant is explicitly the trivial instance).
2. **Antecedent reachable:** in `m`, the antecedent of `B` holds for some witness system(s) — the bridge is not vacuously inapplicable.
3. **Bridge falsifiable:** with the same witness, the consequent of `B` fails *or* a named spine conclusion that `#print axioms` shows depends on `B` fails when `B`'s field is withheld / replaced by a counterexample proof.
4. **Non-redundancy:** the blocked conclusion is one the axiom-budget ledger attributes to `B` specifically (not already blocked by failing a different bridge in the same model).

Collectively: **no bridge is entailed by scaffolding alone**, and **no bridge is entailed by the conjunction of the others** — at least not for the conclusions the spine actually exports.

**Approach:**

1. **`SpineModel` structure** (new file: `formal/AlignmentProofSpine/SpineModel.lean` or `Field/Finite/SpineModel.lean`):
   - Parameters: finite toy carriers (`System := Fin n`, small handle/access types) or a parameterized signature matching `Core.lean`.
   - Fields: one field per load-bearing axiom in the checklist above, plus enough measurand definitions that `RiskGap`, `CCI`, `Safe`, layer predicates, and bridge antecedents are interpretable.
   - Docstring: consistency / independence witnesses only — not a claim about any real deployment.

2. **Instance A — trivial model (consistency only):**
   - `System := Unit`; all `Int` measurands `:= 0`; all `Prop` predicates `:= True`.
   - All bridge fields: `intro; trivial` / `omega`.
   - Theorem: `spine_axioms_consistent : Nonempty SpineModel`.

3. **Instance B — non-degenerate base model:**
   - At least two systems with `RiskGap A > 0` and `¬ Safe A` while Instance A's axioms are satisfied *as a structure* but with non-constant interpretation.
   - Theorem: `spine_axioms_nontrivial : ∃ m : SpineModel, ∃ A, RiskGap A > 0 ∧ ¬ Safe A`.
   - Shows safety is not built into scaffolding.

4. **Instance family C — one independence witness per bridge (required for hostile review):**

   For each `B` in the checklist, prove a theorem `bridge_B_independently_load_bearing` (namespaced, e.g. `SpineModel.MB3_independent`) stating schematically:

   ```lean
   -- pattern; exact statement tuned per bridge shape
   theorem MB3_independently_load_bearing :
     ∃ (m : SpineModel), ∃ A B : System,
       m.MB3_antecedent A B ∧        -- bridge input situation reachable
       ¬ m.MB3_consequent A B ∧      -- bridge conclusion fails in this model
       ¬ m.derived_layer_goal A      -- named export that needs MB3 also fails
   ```

   **Reuse before rebuilding:** `Defeaters.lean` already has finite toys for `MB1`, `MB4`, `MB6b`, `MB8`; `Forgeability.lean` has `forgeability_gap` for the `MB10` gap; `Correction.lean` has capture theorems for the `MB4a` / anti-capture direction. P3 should **lift or alias** these into the `SpineModel` checklist rather than duplicate — add missing toys for bridges without one:

   | Bridge | Existing partial work | Likely new toy focus |
   |--------|----------------------|----------------------|
   | `MB1` | `MB1_defeater_toy_nonstationary_shift` | lift; link to estimator-soundness export |
   | `MB2` | signal only | behavioural sample too poor to identify bundle |
   | `MB3` | signal only | bearer map agrees on probe, diverges off-sample |
   | `MB4` | `MB4_defeater_toy_manipulated_judge` | lift |
   | `MB4a` | `capture_defeats_correction_integrity` | measured path captured while abstract layer would need `MB4a` |
   | `MB5` | signal only | ontology shift not audited on successor channels |
   | `MB6a` | signal only | confounded percolation evidence |
   | `MB6b` | `MB6b_defeater_toy_lock_in` | lift |
   | `MB7a`–`MB7d` | chokepoint / `SteerableAt` | access/filter/detector gamed while antecedent-shaped inputs hold |
   | `MB8` | `MB8_defeater_toy_legitimacy_theater` | lift |
   | `MB9` | signal only | grounding cert conservative on wrong ontology slice |
   | `MB10` | `forgeability_gap` | forged signature passes measured risk, fails true harm |
   | `MB11` | — | `CertifiedSafetyCase` + tolerance, but `Safe` blocked when `MB11` withheld |
   | `S10` | — | measurands violate blanket coherence while other fields hold |
   | `WithinDeploymentRiskTolerance` | — | case without tolerance (or tolerance without case) blocks `Safe` |

   **Collective theorem (recommended export):**

   ```lean
   theorem all_bridges_independently_load_bearing :
     MB1_independent ∧ MB2_independent ∧ … ∧ MB11_independent ∧
     MB4a_independent ∧ S10_independent ∧ tolerance_independent
   ```

   Appendix G gets a compact table: bridge ID → independence theorem → blocked export → existing defeater toy (if any).

5. **Mechanical drift guards:**
   - `check_spine_model.py` (or extend `check_axiom_budget.py`): (i) diff `SpineModel` fields against pretty-printed axiom statements; (ii) verify the checklist has exactly one `*_independent` theorem per bridge ID in `BridgeAssumptions` + `{MB4a, MB10, MB11, S10, WithinDeploymentRiskTolerance}`; (iii) fail CI if a new `MB*` axiom lands without a matching independence witness.
   - Regenerate or add Appendix G subsection (`appi:sec:spine-model` or paragraph under axiom budget) with the independence table.

**Minimal acceptable bar:** Instance A only — consistency, no independence (time-constrained fallback; document as incomplete).

**Credibility bar (this plan's target):** Instance A + B + full Instance C family + drift script + axiom-budget cross-links per bridge.

**Size:** ~2 sessions (Instance A/B ~0.5 session; C family ~1–1.5 sessions given partial reuse from `Defeaters.lean`; MB2/MB3/MB5/MB6a/MB7*/MB9/S10/tolerance toys are the main new work).

**Verification:** `lake build`; every `*_independent` theorem typechecks; `check_spine_model.py` passes; for each bridge, `#print axioms` on the cited blocked export includes that bridge and not only scaffolding; `make check`.

---

### P4 — Löbian / tiling contrast in `Field/Finite/`

**Implemented (2026-07-20):** `LobTiling.lean` provides `HBLConditions`, named `LobFixedPoint`, the derived `lob_rule_from_fixed_point`, `self_certifying_tiling_obstruction`, and `audited_successor_risk_bound_without_provability`. The fixed point is an explicit field-scope hypothesis; no claim is made that the book spine or a real agent satisfies it. Ch30, Appendix G, the formal README, and the assumptions ledger point to the distinction.

**Goal:** Pre-empt the "successor chapter substitutes an engineering inequality for the Löbian obstruction" objection with a formal contrast, not just citations.

**Approach:**

1. **New module:** `formal/AlignmentProofSpine/Field/Finite/LobTiling.lean`.

2. **Layer 1 — abstract provability (finite / modal idiom):**
   - `Formula` inductive type (or `Nat` codes if keeping the spine's integer style).
   - `Prov : Formula → Prop` (or `Formula → Formula` for modal reading).
   - Structure `HBLConditions` (or named record): Hilbert–Bernays–Löb conditions (necessitation, distribution, internal necessitation) as explicit hypotheses — **not** asserted for the real spine.

3. **Layer 2 — labeled hard step:**
   - Hypothesis or axiom `Diagonalization` / `LobFixedPoint` (existence of the Löb sentence): statement-bearing, docstring cites Gödel diagonal lemma; same honesty pattern as `OA2016_offpolicy_qlearning_convergence` in `BellmanQ.lean`.
   - **Derive Löb's theorem** from HBL + fixed point (~5 lemmas of modal reasoning). This is real work and belongs in the axiom ledger only if exported as a headline theorem.

4. **Layer 3 — tiling obstruction (miniature):**
   - Define `ProvableSuccessorSafe (agent : …) (successor : …) : Prop` as "agent's proof system proves `Safe successor`".
   - Theorem sketch: under HBL + fixed point + a soundness-expressibility hypothesis, a policy "accept successor only if `ProvableSuccessorSafe self successor`" cannot accept an equally-strong successor without proving own soundness (Löb collapses the needed implication). Keep the statement minimal and faithful to Yudkowsky–Herreshoff / Fallenstein–Soares — cite in docstring and `Field/Imported.lean`.

5. **Layer 4 — contrast with spine successor chain:**
   - Theorem: `SuccessorAuditLinks` / `SuccessorMeasurandLink` **does not** assume `Prov` or HBL — it requires measured inequalities (`CCI` monotone, `Control` antitone along audited steps).
   - Docstring states the trade explicitly: the spine avoids the Löbian regress by replacing internal provability with empirical audit links; the open cost is "who validates the audit at step *n*?" (measurement/governance), not "who proves proof of proof?"
   - Wire via `Field/Shutdown.lean` or a new `Field/SuccessorObstructions.lean` re-export; add row to `FieldResultRecord` table.

6. **Manuscript sync (prose only, surgical):**
   - ch30 §tiling: one `\leanspine{}` pointer to the contrast theorem.
   - `appendices/appG-lean-proof-spine.tex`: short "Rederived in Lean" paragraph + bridge crosswalk note if applicable.
   - `metadata/assumptions-ledger.md`: record diagonalization as field-scope hypothesis, not spine bridge.

**Link to existing content:** `Bundles.lean` already proves `syntactic_tiling_not_import_preserving` (semantic ≠ import-preserving transport). P4 adds the **proof-theoretic** flank; together they cover both ways naive tiling fails.

**Size:** ~1 focused session (Lean) + small prose pass.

**Verification:** `lake build`; `#print axioms` on exported theorems shows only HBL/fixed-point hypotheses, no spine `MB*`; field module imports cleanly.

---

## Cross-cutting presentation (after P1–P4 land)

These are not separate implementation tracks but acceptance criteria for the batch:

- **Appendix G / `formal/README.md`:** Lead with what is **proved** (separations, defeaters, trace instance, Löbian contrast, consistency + **bridge-independence** instances) before the bridge list — addresses hostile-review §3 and `metadata/TODO.md` "Separate bridge axioms from book assumptions."
- **Headline theorem list:** Consider demoting `certified_class_safety_from_spine_and_bridges` in reader-facing tables below `trace_derived_risk_bound` / worked-instance theorems — assembly labeled, derivation promoted.
- **Dependency graphs:** Add P4 / consistency model nodes to `context/lean_proof_graphs/*.dot` when those modules exist.

## Backlog (out of scope for this plan)

- **Unweight `CCI`'s primary path** — see `drafts/lean-risk-spine-typing-plan.md` backlog; separate session, large blast radius.
- **Prune unused fields from `CertifiedSafetyCase`** — only if P1 promotion makes the packaging redundant; do not prune without a reviewer-facing story.
- **Full probabilistic tail bounds** for `MB1` — only when an estimator-soundness bridge needs them.
- **Prove Gödel diagonalization in Lean** — out of scope; labeled hypothesis only.
- **Solve Löbian tiling for real agents** — out of scope; contrast + citation only.

## Non-goals

- Proving `WithinDeploymentRiskTolerance` for abstract `System` or real deployments.
- Renaming the artifact from "proof spine" globally (optional follow-up; this plan improves what the spine *shows*, not necessarily its marketing name).
- New quantitative failure-probability or value-loss types.
- Changing `MB11` from axiom to theorem.

## Success criteria (batch)

| Item | Done when |
|------|-----------|
| P1 | At least one headline certification theorem whose proof uses Shannon/trace/vector-floor lemmas; hostile "omega only" objection answered for that theorem |
| P2 | Decidable `EpisodeBatteryGate` with `decide` proof on committed JSON literals; prose names governance gap to `WithinDeploymentRiskTolerance` |
| P3 | `Nonempty SpineModel` + non-degenerate instance + **one `*_independent` theorem per bridge** (`MB1`–`MB9`, `MB4a`, `MB10`, `MB11`, `S10`, tolerance); drift script enforces checklist completeness |
| P4 | Löb derived from labeled HBL + fixed point; contrast theorem vs. `SuccessorAuditLinks`; ch30/appG pointer |
| Batch | `lake build`, `check_axiom_budget.py`, `make check` green; conversation log + INDEX row |

## Key paths (existing)

- `formal/AlignmentProofSpine/Certification.lean` — assembly, `MB11`, tolerance axiom
- `formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean` — trace→risk leaf (`trace_derived_risk_bound`)
- `formal/AlignmentProofSpine/Field/Finite/ShannonMI.lean` — MI bounds
- `formal/AlignmentProofSpine/WorkedInstance.lean` — real fixture discrimination
- `formal/AlignmentProofSpine/Successors.lean` — `SuccessorAuditLinks` (contrast target for P4)
- `formal/AlignmentProofSpine/Bundles.lean` — syntactic vs import-preserving tiling
- `experiments/embedded-simulation/results/embedded_frozen_validation.json` — P2 data candidate
- `formal/AlignmentProofSpine/Defeaters.lean` — partial bridge defeater toys to lift into P3
- `formal/AlignmentProofSpine/Forgeability.lean` — `MB10` / `forgeability_gap`
- `formal/scripts/check_axiom_budget.py`, `formal/axiom-ledger.json` — extend for P1/P3; cross-link each bridge to its independence theorem and blocked export
- `review/strategic-advice-2026-06-28.md` item 4 — originating concern for P1/P3

## Relation to prior plan

| Prior (`lean-risk-spine-typing-plan.md`) | This plan |
|------------------------------------------|-----------|
| P4 toy tolerance instantiation | **P2** here — expanded with explicit non-axiom pattern and frozen-validation source |
| Backlog: unweight `CCI` | Still backlog — not blocked by P1–P4 |
| P1 vector-primacy refactor | Still backlog — P1 *here* is a different P1 (non-omega certification) |

Use distinct names in session logs: "typing plan P4" vs "credibility plan P2" to avoid confusion.
