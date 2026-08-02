# `formal/` — Lean proof spine

A compact, **self-contained Lean 4 formalization** of the *logical skeleton* of
the alignment argument in *Towards Superintelligence Alignment*. It implements
the spec in [`LeanProofSpineImplementationBrief.md`](LeanProofSpineImplementationBrief.md)
(conjectured dependency structure in
[`../context/lean_proof_dependency_graph.dot`](../context/lean_proof_dependency_graph.dot);
 book figures in [`../context/lean_proof_graphs/`](../context/lean_proof_graphs/)).

## What this is and is not

The goal is **not** to formalize the empirical content of UAD, value bundles,
B-IQ, attractor basins, or CEV. It formalizes the chain

```
boundary discovery → grounding viability → capability/control/correction quantities
  → value-bundle and bearer-map transport → correction-channel integrity
  → successor stability → adversarial measurement → certified-class safety
```

and makes one distinction explicit and machine-checked:

* **Proved in Lean** — *if* these predicates and inequalities hold, *then* the
  certification conclusion follows.
* **Assumed bridge** (`axiom`) — real systems satisfy these predicates under
  these measurement procedures. These are the nine `MB1`–`MB9` bridges packaged
  in `Core.BridgeAssumptions`, plus three bridges declared outside the record
  because their statements need later definitions (threaded explicitly, same
  pattern): `MB4a` (measured-path legitimacy, **including the anti-capture
  condition** — see `Correction.lean`), `MB10` (successor forgeability,
  `Forgeability.lean`), and `MB11` (safety-case adequacy: certified safety
  case + tolerance → abstract `Safe`, `Certification.lean`). Two measurement
  conventions are also Lean axioms: `S07` (MDL ordering) and `S10`
  (blanket-measurand coherence, replacing four formerly anonymous B-IQ
  inequalities). One imported field theorem is statement-bearing rather than
  an opaque handle: `OA2016_offpolicy_qlearning_convergence`
  (`Field/Finite/BellmanQ.lean`). They are **never hidden** inside definitions.
  Each bridge is mapped to the canonical open problem of the field (IRL
  non-identifiability, ELK, off-switch anti-naturality, ontology identification,
  obfuscated arguments, spec coverage, deceptive alignment / measurement
  gaming, …) in the manuscript appendix
  *Bridges and the Field: A Crosswalk* (`appendices/appB-bridge-crosswalk.tex`).

**Toy vs. target strength.** The current spine is deliberately compact. Many
counterexamples are finite `Bool` separations (one predicate defined as `True`,
another as equality); several “theorems” are definitional; abstract quantities
use integer proxies. The strengthening roadmap lives in `metadata/TODO.md`
(§ Lean proof spine — **chapter ↔ Lean mapping gaps**). Bridges `MB1`–`MB10` are
**out of scope** for Lean completion (empirical / philosophical imports); in-scope
work is aligning **drafted chapter formalism** to spine structure.

Priority: derive certification conclusions from spine inputs (capacity slack,
correction channel, successor invariance) rather than assuming them as bare
hypotheses.

**Open (not yet started):** `Field/Finite/PredictorLoop.lean` — finite model of
closed forecast→deployment→world→score loops implying a discoverable
`System`/boundary fragment (manuscript genesis path in ch10; see
`metadata/TODO.md` chapter↔Lean mapping gaps).

> The book must not say "Lean proves ASI alignment." It may say "Lean proves
> that, *if* these boundary, grounding, bundle, correction, successor, and adversarial
> conditions hold, *then* the certification argument has the advertised logical
> shape. The hard work is showing real systems satisfy the bridge conditions."

## Build

Requires the Lean toolchain via [`elan`](https://github.com/leanprover/elan)
(pinned in `lean-toolchain` to `leanprover/lean4:v4.28.0`). The spine depends on
**Mathlib** (`v4.28.0`) for finite combinatorics, list algebra, and upcoming
field-agenda rederivations. First build downloads Mathlib; use `lake exe cache get`
in `formal/` for precompiled oleans when online.

```bash
cd formal
lake exe cache get   # first time / after Mathlib update (needs network)
lake build
```

Inspect what a theorem ultimately rests on (proofs vs. bridges):

```bash
cd formal
echo 'import AlignmentProofSpine
open AlignmentProofSpine
#print axioms certified_class_safety_from_bridge_record' > /tmp/chk.lean
LEAN_PATH=.lake/build/lib/lean lean --root=. /tmp/chk.lean
```

**Axiom budget guard.** The above check is mechanized for a curated list of
headline theorems in `scripts/check_axiom_budget.py`, which diffs
`#print axioms` output against the checked-in snapshot `axiom-ledger.json`
and regenerates the Appendix G table (`metadata/axiom-budget-index.tex`,
`appi:sec:axiom-budget`) from it:

```bash
cd formal
lake build                              # after any spine change
python3 scripts/check_axiom_budget.py   # fails (exit 1) if a theorem's axiom
                                         # footprint drifted from the ledger
python3 scripts/check_axiom_budget.py --update   # accept an intentional drift
```

This catches, mechanically, exactly the failure mode the "never hidden" claim
above depends on: a refactor that silently makes a theorem depend on a new
`MB*` bridge (or a wider carrier footprint) without anyone noticing.

`P34` (host-capacity aliasing) and the other non-bridge results print only
`propext` / `Quot.sound` (or abstract carriers). `risk_gap_bound_from_cci_slack`
is the narrow arithmetic leaf deriving `RiskGap A ≤ δ` from
`Control A ≤ CCI A + δ` via `P13` (no bare `hrisk` hypothesis).
`NumericRiskLeaf` records whether that scalar leaf came directly, from vector CCI
support, from a BIQ-derived slack certificate, or from a Markov-blanket/B-IQ
profile. The vector-CCI path no longer needs a bare assumed floor: the ch26
scalar projection `CCI_λ` is computed from the certificate
(`CCICertificate.lambdaProjection`) and the pass thresholds induce a floor
(`CCIThresholds.lambdaFloor`), with only measurement alignment
(`CCICertificateMeasures`) left bridge-shaped. Trace-computed blanket profiles feed the same leaf via `traceDerivedCCISlack` /
`trace_derived_risk_bound`. The headline non-definitional certification path is
`FieldFinite.risk_gap_bound_from_trace_profile` (trace profile + passing vector
certificate + θ-floor margin → `risk_gap_bound_from_threshold_certified_cci`;
instantiated on real data by `WorkedInstance.honest_instance_risk_bound`).
`P30_certified_class_safety_derived` packages that risk leaf together with
`Certified`, `SatisfiesInvariants`, and `LayeredAlignedDef` into a
`CertifiedSafetyCase`; its docstring says explicitly that this step is
**assembly, not derivation**. What the record buys is separate:
`MB11_safety_case_adequacy` is the labeled bridge from a safety case plus a
deployment-tolerance judgment to the abstract `Safe` predicate
(`P30_safe_of_case`, `safe_from_spine_inputs`) — the open research step is an
explicit axiom, not an implied conclusion, and the packaged hypotheses are
consumed by it rather than merely stored.
`certified_class_safety_from_bridge_record` takes an explicit
`BridgeAssumptions` record; `certified_class_safety_from_spine_and_bridges` is
the corollary obtained from `standardBridges`.
The anti-capture story is likewise derived rather than presupposed: capture of
any handle on the designated measured path yields `CCICapturedOrInvalid`
unconditionally (`capture_makes_cci_captured_or_invalid`) and refutes
`CorrectionIntegrity` via `MB4a`'s contrapositive
(`capture_defeats_correction_integrity`); the measured path axiom
`SystemCorrectionPath` carries **data only** (corrector, handles, capacities)
and asserts no validity.
The bridge path now splits socio-technical selection into `MB6a`/`MB6b`
(percolation evidence → basin stability → correction integrity) and adversarial
measurement into `MB7a`–`MB7d`, with `MB7d` covering inferential-UAD detector validity.
`MB9` is the grounding-certificate bridge: it turns a conservative value-correction
abstraction certificate into the abstract `GroundingViable` layer.
`MB10` (`AlignmentProofSpine/Forgeability.lean`) is a tenth bridge, not part of
`BridgeAssumptions`: `SuccessorSafe` (all seven ch48 conserved properties) plus a
bounded measured risk does not, on its own, bound a successor's true harm — a
finite counterexample (`forgeability_gap`) makes that concrete — so `MB10` names
the missing condition (the conserved-property audit channel is adversarially
verifiable up to the successor's capability) rather than leaving it implicit.

**Notation.** `ValueUpdateOperator` (`U_H`), `SystemUpdateOperator` (`U_S`),
scalar `CCI` (numeric risk-spine projection), vector/status `CCICertificate`,
handle-controlled `CorrectionPath`,
`SuccessorSafeWitness`.

Manuscript cross-refs: `\leanspine{kind}{node}{gloss}` in `metadata/preamble.tex`.

## Module map

| Module | Proof-spine nodes | Book chapters |
|--------|-------------------|---------------|
| `AlignmentProofSpine/Core.lean` | abstract carriers, access/handle/K-equivalence vocabulary, concrete `Boundary`, grounding predicates and `conservative_abstraction_no_silent_gap`, MDL/graph scaffolding, bridges `MB1`–`MB9` with split `MB6a`/`MB6b`, `MB7a`–`MB7d`, and grounding bridge `MB9`, `BridgeAssumptions` | foundations |
| `AlignmentProofSpine/Chokepoint.lean` | ch43 `AdversariallyVerifiableUpTo`/`SteerableAt` (cost-of-faking-vs-affordable-surplus definition), `VerifiabilityGatedBridge`, `sharedChokepoint_steerable_blocks_both_routes` (shared-channel disjunction gives no independent failure tolerance), `independent_channels_can_diverge` (constructive contrast), worked `MB6a`/`MB6b` vs `MB8` instance (`SharedInstrumentHypothesis`, `correction_integrity_disjunctive_tolerance_needs_distinct_instruments`) | 43, 46 (correlated-failure review 2026-06-30) |
| `AlignmentProofSpine/Defeaters.lean` | systematic defeater ledger for `MB1`–`MB11` (incl. `MB4a`) plus misspec neighborhood signals (`EstimatorNonstationary`, `ModelClassMisspecified`, `GrainOfTruthViolated`, `MeasuredPathCaptured`, `SignatureForgeableAtCapability`, `SafetyCaseScopeExceeded`, …); finite toys for nonstationary/misspec/`MB4`/`MB4a`/`MB6b`/`MB8`/`MB10`/`MB11`; `MB7b`–`MB7d` reduce to `Chokepoint.SteerableAt` | crosswalk to assumptions/uncertainty ledgers |
| `AlignmentProofSpine/Field/Finite/Nonrealizability.lean` | finite nonrealizability / model-class misspec: off-class unsafe counterexample, ambiguity-set transfer, class-certificate ⇏ deployment safety; **no** new `MB*` | field misspec candidate |
| `AlignmentProofSpine/Field/Finite/RegretSafety.lean` | finite regret⇏safety: zero-regret/wrong-loss and prefix-catastrophe counterexamples; conditional loss/exploration transfer to zero harm; **no** new `MB*` | field regret candidate |
| `AlignmentProofSpine/Field/Finite/CompositePathBypass.lean` | green named measured path + composite bypass ⇏ real correction integrity; positive path certificate requires no-bypass (does not reverse `MB4a`) | CIRIS / anti-capture neighborhood |
| `AlignmentProofSpine/FieldInterfaces.lean` | Phase 2 book interfaces (**no** new `MB*`): `EpistemicCoverageEvidence` → `MB9`/`GroundingViable`; `SystemRegretSafetyEvidence` distinct from `RiskGap` (not a safety-case leaf); `PositiveMeasuredPathCertificate` (legitimacy+coverage+no-bypass); finite consumers/separations | field-claim plan |
| `AlignmentProofSpine/Forgeability.lean` (Phase 2 addendum) | `SystemTransition` channel reading of `ConservedPropertySignatureVerifiable` via `Chokepoint.AdversariallyVerifiableUpTo`; `true_harm_bound_of_successor_safe_step_via_chokepoint` | 8, 31, 43, 48 |
| `AlignmentProofSpine/Mathlib.lean` | shared Mathlib lemmas (e.g. finite-cardinality pigeonhole for `P34`) | foundations |
| `AlignmentProofSpine/Boundaries.lean` | `P05`–`P09`, `P36`, access-equivalence and K-equivalence non-identifiability, CID abstraction-relative incentive separation, smoothing-margin arithmetic | 6–7, 10, 36 |
| `AlignmentProofSpine/Capability.lean` | `P10`–`P13`, `P32`, `P43`, Markov-blanket/B-IQ profiles, hidden-BIQ certificate, slow-plotting accumulation (B-IQ / control–correction arithmetic), ch13 weighted collective competence (`weightedCollectiveCompetence`, `P12_coordination_bottleneck_partial`, `P12_seven_loss_bottleneck`), θ-floor risk leaf (`risk_bound_from_threshold_certified_cci`) | 11–14, 33, 36 |
| `AlignmentProofSpine/CooperationGraph.lean` | **`UADDiscoveryAudit`**, **`UnitScore`**, **`MetaPriorEvidence`**, `metaPriorMismatch` derived from `P_meta` diagonal mass, **`InferentialDetectionCertificate`**, **`DerivedCoopGraph`**, **`DerivedInferentialGraph`**, `causalMutualModelOf` / `inferentialProfileOf` / `inferentialPairOf` (opaque evidence emitters), `inferentialCouplingScore`, `auditMutualModelWithInferential`, `uad_audit_yields_inferential_graph`, `severed_causal_reach_positive_effective_reach`, **`P33`** | 13, 33, 35 |
| `AlignmentProofSpine/Bundles.lean` | `P14`, `P16`, `P19`–`P22a` (proofs), `P15`/`P17`/`P18`/`P22b` (counterexamples), scalar CIRL as one-dimensional bundle inference, cooperative reward inference / bundle-preservation separation, syntactic-tiling/import-preservation alias | 15–23, 30 |
| `AlignmentProofSpine/Correction.lean` | `P23`, `P24`, `P25`, `P26`, scalar **`CCI`**, vector/status **`CCICertificate`** with derived ch26 scalar projection (`CCICertificate.lambdaProjection`, `CCIThresholds.lambdaFloor`, `CCI_ge_threshold_floor`), data-only **`CorrectionPath`** with separate validity predicate **`CorrectionPathLegitimate`** and bridge **`MB4a`** (measured-path legitimacy incl. anti-capture), derived anti-capture theorems (`capture_invalidates_reference`, `capture_makes_cci_captured_or_invalid`, `capture_defeats_correction_integrity`), shutdown/interruptibility/corrigibility, impact, quantilization, debate, amplification, and latent-readout separations | 25–29, 41–43 |
| `AlignmentProofSpine/Field/*.lean` | **Field-agenda crosswalk**: shared-domain special-case / projection theorems with explicit interface conditions, non-converse separations, shared status ledger, finite Mathlib-backed helpers (`Finite/MDP`, `Finite/Probability`, `Finite/PMF`, `Finite/ShannonMI`, `Finite/Weights`, `Finite/Reachability`, `Finite/Contraction`, `Finite/TraceBIQ`), cited imported field theorem handles, and agenda modules for CIRL, shutdown, interruptibility, Christiano corrigibility, ELK, debate, impact, and quantilization. Recent finite derivations include assistance-belief defer optimality, finite-horizon AUP attainable-utility preservation, PMF quantilizer support soundness, quantilizer base-rate fragments, trace-computed vector B-IQ / output-capability appearance bounds with a tight information-shaped ceiling `⌈log₂ min(m,|𝒜|)⌉` (no channel-count factor, alphabet clip `|𝒜|` not `|𝒜|²`), attended-harm / extinction certificates, a concentration bridge with tight worst-case fallback for supplied blanket partitions, and a **real-valued (noncomputable) Shannon entropy/mutual-information development** (`Finite/ShannonMI`) proving `mutualInformation_le_log_min_card` — the general Shannon-theoretic fact (`MI ≤ log min(m,n)`, via Mathlib's concave-Jensen inequality applied to `Real.log`) underneath the N-8 empirical finding that the appearance *ceiling* (not the counting *score*) is a sound MI bound; not yet wired to `TraceBIQ`'s decidable rational pipeline (`metadata/TODO.md`). New finite rederivations of the *actual* field machinery: **`Finite/IncompletePreferences`** (Thornley IPP — POST incompleteness, sweetening diagnostic for gaps vs. indifference, timestep dominance, never-pay-to-shift-shutdown-probability, EU-completeness contrast), **`Finite/ShutdownIncentives`** (Soares et al. — the incentive identity, prevention/seeking incentives, neutrality iff `U_S = U_N`, utility indifference works locally / is a knife edge / buys no preservation), **`Finite/BellmanQ`** (Orseau–Armstrong — Bellman-target uniqueness, value-iteration soundness + greedy attainment, schedule invariance of the learned target, with the stochastic-approximation convergence step as the single statement-bearing import `OA2016_offpolicy_qlearning_convergence`), **`Finite/DynamicChoice`** (Thornley dynamic-choice layer — the money-pump objection exhibited on an explicit TD-permissible trade chain, and the resolute-choice escape: every finite decision tree has a plan realizing a TD-maximal reachable outcome), **`Finite/OffSwitchGame`** (Hadfield-Menell et al. off-switch game — deference strictly best under genuine reward uncertainty, rational-human pointwise optimality, and the degradation direction: the incentive vanishes with an uninformative human), **`Finite/QuantilizerMaximin`** (Taylor's characterization — bounded density ratio is sufficient *and* necessary for the worst-case cost guarantee; the quantilizer instance normalizes to the `1/q` bound), **`Finite/DebateGame`** (Irving et al. — native two-prover game on claim trees: min-max value equals truth with a correct judge, constructive honest strategies, and the one-judge-error flip showing the guarantee is conditional on judge integrity), **`Finite/ELKIdentifiability`** (Christiano et al. ELK — the reporter non-identifiability core: translator and simulator agree under *every* behavioral training criterion on-distribution and diverge under tampering; refutes the earlier κ_C-projection framing, which is retained as a labeled interface toy), and **`Finite/AmplificationTree`** (iterated amplification / HCH — leafwise soundness by structural induction, local step validity free for any supervisor, one leaf error flips the root; supersedes the `Bool` toy in `Correction.lean`). A new `Field/Amplification.lean` agenda module carries the amplification records; the ELK/Debate agenda records now separate rederived protocol content from the assumption-labeled interface toys. `FieldSubsumptions.lean`'s former `∀ tag, True` inventory is replaced by the checkable `every_agenda_has_rederived_core` (each agenda tag has at least one finite rederivation record). | crosswalk appendix |
| `AlignmentProofSpine/Field/Finite/LobTiling.lean` | conditional Löb derivation from explicitly supplied HBL closures and a diagonal fixed point; a diagonal successor cannot be accepted by reflecting only the same proof system's proof of its safety; audit-link contrast transports a numeric bound without a provability predicate. The fixed point and closure conditions are field-scope hypotheses, not spine bridges or claims about real agents. | 30–31, appG |
| `AlignmentProofSpine/FieldSubsumptions.lean` | compatibility re-export for the field-agenda headline theorem names | crosswalk appendix |
| `AlignmentProofSpine/Successors.lean` | `P27`, `P28`, `P29`, **`SuccessorSafeChain`**, **`SuccessorMeasurandChain`**, risk bound propagation; ch48 audit links are the explicit hypothesis record `SuccessorAuditLinks` (no global linking axioms), and safe chains reduce to measurand chains via `SuccessorSafeChain.toMeasurandChain` | 28–31 |
| `AlignmentProofSpine/Forgeability.lean` | ch08/ch31/ch48 successor-forgeability gap made a checked finite counterexample (`forgeability_gap`); bridge `MB10` (conserved-property signature not forged), declared here rather than in `Core.BridgeAssumptions` because it needs the numeric risk leaf, threaded explicitly like `SuccessorAuditLinks`; `true_harm_bound_of_successor_safe_step` shows what `MB10` buys on top of the existing risk-propagation machinery | 8, 31, 43, 48 |
| `AlignmentProofSpine/Adversarial.lean` | `P31`, `P34`, `P36R`, `P37` (`P33` in `CooperationGraph`) | 32–37 |
| `AlignmentProofSpine/Philosophy.lean` | `P41`, `P42`, `P44`, `P45` | 41–44 |
| `AlignmentProofSpine/Certification.lean` | `P01`, `P02`, `P30`, `P35`, finite-support `P40`, direct/bridge-derived layer evidence records, grounding required by `LayeredAlignedDef`, **`risk_gap_bound_from_cci_slack`** (numeric risk leaf), **`certified_class_safety_from_bridge_record`** (`CertifiedSafetyCase` assembly, labeled as such), bridge **`MB11`** (safety-case adequacy) with **`P30_safe_of_case`** / **`safe_from_spine_inputs`** deriving abstract `Safe` — `MB11`'s `WithinDeploymentRiskTolerance` is the framework's actual answer to "probability of failure / quantified value loss": a Prop-valued acceptance gate, not a number (nothing here computes a probability or an expected loss; see `CertifiedSafetyCase`'s docstring) | 1–5, 37–38, 42, 48 |
| `AlignmentProofSpine/WorkedInstance.lean` | worked instances on **real committed data** from the same pinned generator (`synthesize_rows(300, ..., seed=5)` at git `408444b`): 26-row windows of `sample_capture_theater.jsonl` and `sample_honest_baseline.jsonl` packaged as `DiscreteTrace`/`EnvBlanket`, `decide`d trace-computed diversity/capacity/ceiling numbers, and `CCICertificate`s whose `manipulation` coordinate is *computed* from the real `judge_captured` column (not asserted) against thresholds fixed before either count was computed — the capture-theater certificate honestly **fails** (`workedCert_fails`, `26 > maxManipulation = 1`) and the honest-baseline certificate **passes** the identical thresholds (`honestCert_passes`, count `0`), yielding an actual `NumericRiskLeaf A 6`/`RiskGap A ≤ 6` (`honest_instance_risk_bound`; bound weak because the pre-registered thresholds are loose — reported at face value, not sharpened through placeholder coordinates); the single differing real coordinate flips the verdict, so the gate *discriminates*; fixture provenance pinned by `experiments/embedded-simulation/tests/contract/test_worked_instance_fixtures.py`; see the module docstring for the earlier (fixed) mistranscription-plus-reverse-engineered-thresholds version | 11, 26, 43, 46 |
| `AlignmentProofSpine/ToyDeploymentGate.lean` | decidable `EpisodeBatteryGate` on frozen-validation battery output (`frozen_validation_battery_gate_passes`: 3/36 false passes ≤ pre-registered max 5); governance gap to `WithinDeploymentRiskTolerance` documented — not a discharge of the global tolerance axiom | 42 |
| `AlignmentProofSpine/SpineModel.lean` | consistency witness (`spine_axioms_consistent`), non-degenerate measurand model (`spine_axioms_nontrivial`), one `*_independently_load_bearing` theorem per labeled bridge (`MB1`–`MB9`, `MB4a`, `MB10`, `MB11`, `S10`, tolerance); checked by `scripts/check_spine_model.py` | appG |
| `AlignmentProofSpine.lean` | root module re-exporting all of the above | — |
| `scripts/check_axiom_budget.py` + `axiom-ledger.json` | tooling, not a proof module: mechanically diffs `#print axioms` on 38 headline theorems against the checked-in ledger and generates Appendix G's axiom-budget table (`metadata/axiom-budget-index.tex`) | appi:sec:axiom-budget |
| `scripts/check_spine_model.py` | verifies the bridge-independence checklist in `SpineModel.lean` (18 independence theorems + 2 consistency exports) | appG |

## Three kinds of result (for the book)

* **proof** — a direct logical/arithmetic theorem (e.g. `P01`, `P10`, `P14`,
  `P27`, `P34`).
* **counterexample** — a compact finite toy model showing one notion does not
  imply another (e.g. `P15`, `P17`, `P18`, `P22b`,
  `cid_incentive_not_abstraction_invariant`,
  `cooperative_reward_inference_not_bundle_preservation`,
  `shutdownability_not_correction_channel_corrigibility`,
  `safe_interruptibility_not_correction_channel_preservation`,
  `low_impact_not_correction_preservation`,
  `correction_preservation_can_require_high_impact`,
  `quantilization_not_trajectory_cci`,
  `act_based_preference_satisfaction_not_stable_corrigibility`,
  `debate_truth_not_correction_preservation`,
  `amplification_not_correction_contraction`,
  `latent_readout_not_correction_uptake`,
  `syntactic_tiling_not_import_preserving`, `forgeability_gap`, `P25`, `P26`,
  `P31`, `P37`, `P41`, `P42`, `P44`).
* **bridge** — an empirical or philosophical condition supplied by measurement,
  governance, or future theory (`MB1`–`MB11` plus `MB4a`, declared as `axiom`;
  `MB1`–`MB9` packaged in `BridgeAssumptions`, `MB4a`/`MB10`/`MB11` threaded
  explicitly).
* **imported field theorem** — a source-cited external result or protocol
  assumption (`Field.Imported`, plus the statement-bearing
  `OA2016_offpolicy_qlearning_convergence` in `Field/Finite/BellmanQ.lean`)
  used to state what the external agenda proves under its own assumptions.
  These are distinct from `MB*` book bridges.

**Community gem (in progress).** The `Field/` module is building a shared
machine-checked finite fragment for CIRL, AUP/relative reachability,
quantilization, shutdown, and interruptibility under explicit interface
conditions. The alignment community has no comparable artifact today. The
manuscript names this as the **field-agenda formalization gem** in Appendix I
(`sec:appi-field-formalization-gem`).

Dependency hygiene: inspect any exported theorem with Lean's `#print axioms`
before describing it as axiom-free. For example, use
`#print axioms AlignmentProofSpine.interrupt_safety_is_correction_projection` or
`#print axioms AlignmentProofSpine.christian_corrigibility_system` in a scratch
Lean file; the former is a local finite proof, while the latter intentionally
depends on `MB4`.

## Notes on deviations from the brief's scaffold

* The Lean 3 `constant` keyword (used in the brief's sketch) was removed in
  Lean 4; abstract carriers are declared with `axiom`, concrete structure with
  `structure`/`def`.
* No `sorry`/`admit` remain. Every `admit` placeholder in the brief's scaffold is
  either proved or, where it depended on empirical content, deliberately routed
  through an explicit `MB*` bridge.
* Counterexamples (brief §8) use finite `Bool`/`Fin` toy models rather than
  abstract `System`, as the brief requires ("do not leave these as abstract
  counterexamples forever").
* `P44` uses the brief's §6 amendment (two disagreeing legitimacy orderings), not
  the inconsistent single-predicate form.
* The host-capacity aliasing theorem `P34` uses Mathlib's
  `Fintype.card_le_of_injective` via `AlignmentProofSpine.Mathlib`.
* **`RiskGap`** is `Control − CCI` — excess influence bandwidth, an
  information/capacity quantity, not a probability or a value-loss estimate.
  There is no separate `Risk` name; renamed from an earlier `Risk := RiskGap`
  alias because two names for one subtraction invited exactly the "primary
  numeric risk bound is a renaming" misreading it now avoids.
  **`CCI` is intrinsically λ-weighted** (`CCI A := weakestLink − CCIPenaltySum`,
  ch46 `eq:cci-ch46`) — this is a manuscript modeling commitment, not a Lean
  artifact: it fixes an exchange rate between heterogeneous penalty units
  (latency as time, manipulation as a count, irreversibility/ontology as loss
  scores) and raw channel capacity (bits/window), applied consistently
  wherever `CCI` is read (`MB6b`, `MB7c`, `S10`, every chapter/appG citation).
  `CCICertificate.lambdaProjection` uses the *same* weights
  (`CCICertificateMeasures.weights_eq` forces this), so certificate and
  system-level pricing agree by construction — there is no inconsistency
  between the two, only the underlying pricing commitment itself, which a
  reader should weigh independently of the arithmetic. `CCICertificatePasses`
  (componentwise threshold gate over `CCICertificate`'s vector coordinates —
  each coordinate checked against its own threshold, no cross-coordinate
  summation at the certificate level) is what the `WorkedInstance` module
  actually exercises on real fixture data, and is the gate a passing
  certificate must clear before the λ-weighted floor is even computed.
  Removing the λ-weighting from the *primary* certification path (an
  unweighted raw-capacity quantity, independent of `CCI`) would require
  introducing a new System-level quantity and rewiring every bridge that
  reads `CCI` — scoped as a separate, larger backlog item (see
  `drafts/lean-risk-spine-typing-plan.md`), not attempted here.
  `CCIVectorSupportsScalarSlack` records the bridge-shaped handoff from a
  passed vector certificate to the scalar leaf; `Control ≤ CCI + δ` is the
  numeric leaf `NumericRiskLeaf` consumes. `CCIThresholds` (`θ`) itself is a
  deployment-specific empirical/policy input — what tolerance is measured and
  accepted is not something the arithmetic discharges, the same epistemic
  class as `MB1`'s estimator soundness.
  Handle-controlled path: `CorrectionPath` / `SystemCorrectionPath` over `CorrectionChainLink`,
  now grounded in a correcting agent's controlled handles. The richer manuscript
  $C_{\mathrm{raw}}$ is represented as a certificate coordinate; the old weakest-link
  scalar remains inside `CCI` for existing arithmetic lemmas.
* **What you actually get is a gate, not a number.** Neither `RiskGap` nor the
  vector certificate produces a probability of failure or an expected value
  loss — nothing in this development defines a `System`-level utility function
  or a real-deployment failure-frequency estimator. The framework's honest
  answer to "what does a passing certificate buy" is `MB11_safety_case_adequacy`
  (`Certification.lean`): a `CertifiedSafetyCase` plus a named, ungrounded
  `WithinDeploymentRiskTolerance` judgment reaches the abstract `Safe` Prop —
  an acceptance gate, not a quantified guarantee, and the docstring says so
  explicitly. This is a deliberate epistemic choice, not a gap to be closed
  by inventing a `Rat`-valued risk quantity with no producer.
* **`DeploymentMass`** is environment-relative deployment/control mass (book ch46,
  `eq:deployment-mass-ch46`). Selection uses `SelectionChannel` / `SelectionHandleFor`
  over the same `Handle` type as correction. Revenue and regulatory risk are not
  primitive Lean terms.
* **`SuccessorSafe`** = `Nonempty SuccessorSafeWitness` with the ch48 seven
  conserved-property fields; correction capacity is `CCIPreserved` (vector `\vec{CCI}`
  in prose, including ch46 `U_S` semantics via `rawCapacity` and `ontologyTranslation`).
* Node IDs match `formal/AlignmentProofSpine/*.lean` theorem names (see module map above).
  Full graph: `context/lean_proof_dependency_graph.dot`.
  Book layout: four sub-spines + overview in `context/lean_proof_graphs/` → `figures/lean_proof/` via `scripts/render_lean_graphs.sh` (Lean Proof Spine appendix, Section~\ref{sec:appi-proof-dependency}).
