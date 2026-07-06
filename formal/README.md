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
  in `Core.BridgeAssumptions`, a tenth bridge `MB10` (successor forgeability;
  declared in `AlignmentProofSpine.Forgeability` and threaded explicitly rather
  than packaged, since it needs the numeric risk leaf), plus the
  model-selection convention `S07`. They are **never hidden** inside definitions.
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
`propext` / `Quot.sound` (or abstract carriers). `risk_bound_from_cci_slack`
is the narrow arithmetic leaf deriving `Risk A ≤ δ` from
`Control A ≤ CCI A + δ` via `P13` (no bare `hrisk` hypothesis).
`NumericRiskLeaf` records whether that scalar leaf came directly, from vector CCI
support, from a BIQ-derived slack certificate, or from a Markov-blanket/B-IQ
profile. The vector-CCI path no longer needs a bare assumed floor: the ch26
scalar projection `CCI_λ` is computed from the certificate
(`CCICertificate.lambdaProjection`) and the pass thresholds induce a floor
(`CCIThresholds.lambdaFloor`), with only measurement alignment
(`CCICertificateMeasures`) left bridge-shaped. Trace-computed blanket profiles
feed the same leaf via `traceDerivedCCISlack` / `trace_derived_risk_bound`.
`certified_class_safety_spine_derived` packages that risk leaf together with
`Certified`, `SatisfiesInvariants`, and `LayeredAlignedDef` into a
`CertifiedSafetyCase`, so the non-arithmetic evidence is no longer advertised
as proving the numeric inequality.
`certified_class_safety_from_bridge_record` takes an explicit
`BridgeAssumptions` record; `certified_class_safety_from_spine_and_bridges` is
the corollary obtained from `standardBridges`.
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
| `AlignmentProofSpine/Defeaters.lean` | systematic defeater ledger for all of `MB1`–`MB9`: named failure-mode signal predicates (`LockedInBadBasin`, `JudgeManipulated`, `LegitimacyTheater`, `EstimatorNonstationary`-style, etc., each traced to an A-ID/U-ID in `metadata/assumptions-ledger.md`), finite toy models proving the antecedent-signal-not-consequent shape is logically consistent for `MB1`, `MB4`, `MB6b`, `MB8`, and a reduction of `MB7b`–`MB7d`'s defeater to `Chokepoint.SteerableAt` | crosswalk to assumptions/uncertainty ledgers |
| `AlignmentProofSpine/Mathlib.lean` | shared Mathlib lemmas (e.g. finite-cardinality pigeonhole for `P34`) | foundations |
| `AlignmentProofSpine/Boundaries.lean` | `P05`–`P09`, `P36`, access-equivalence and K-equivalence non-identifiability, CID abstraction-relative incentive separation, smoothing-margin arithmetic | 6–7, 10, 36 |
| `AlignmentProofSpine/Capability.lean` | `P10`–`P13`, `P32`, `P43`, Markov-blanket/B-IQ profiles, hidden-BIQ certificate, slow-plotting accumulation (B-IQ / control–correction arithmetic), ch13 weighted collective competence (`weightedCollectiveCompetence`, `P12_coordination_bottleneck_partial`, `P12_seven_loss_bottleneck`), θ-floor risk leaf (`risk_bound_from_threshold_certified_cci`) | 11–14, 33, 36 |
| `AlignmentProofSpine/CooperationGraph.lean` | **`UADDiscoveryAudit`**, **`UnitScore`**, **`MetaPriorEvidence`**, `metaPriorMismatch` derived from `P_meta` diagonal mass, **`InferentialDetectionCertificate`**, **`DerivedCoopGraph`**, **`DerivedInferentialGraph`**, `causalMutualModelOf` / `inferentialProfileOf` / `inferentialPairOf` (opaque evidence emitters), `inferentialCouplingScore`, `auditMutualModelWithInferential`, `uad_audit_yields_inferential_graph`, `severed_causal_reach_positive_effective_reach`, **`P33`** | 13, 33, 35 |
| `AlignmentProofSpine/Bundles.lean` | `P14`, `P16`, `P19`–`P22a` (proofs), `P15`/`P17`/`P18`/`P22b` (counterexamples), scalar CIRL as one-dimensional bundle inference, cooperative reward inference / bundle-preservation separation, syntactic-tiling/import-preservation alias | 15–23, 30 |
| `AlignmentProofSpine/Correction.lean` | `P23`, `P24`, `P25`, `P26`, scalar **`CCI`**, vector/status **`CCICertificate`** with derived ch26 scalar projection (`CCICertificate.lambdaProjection`, `CCIThresholds.lambdaFloor`, `CCI_ge_threshold_floor`), handle-controlled **`CorrectionPath`**, shutdown/interruptibility/corrigibility, impact, quantilization, debate, amplification, and latent-readout separations | 25–29, 41–43 |
| `AlignmentProofSpine/Field/*.lean` | **Field-agenda subsumptions**: shared-domain special-case / projection theorems with explicit interface conditions, non-converse separations, shared status ledger, finite Mathlib-backed helpers (`Finite/MDP`, `Finite/Probability`, `Finite/PMF`, `Finite/ShannonMI`, `Finite/Weights`, `Finite/Reachability`, `Finite/Contraction`, `Finite/TraceBIQ`), cited imported field theorem handles, and agenda modules for CIRL, shutdown, interruptibility, Christiano corrigibility, ELK, debate, impact, and quantilization. Recent finite derivations include assistance-belief defer optimality, finite-horizon AUP attainable-utility preservation, PMF quantilizer support soundness, quantilizer base-rate fragments, trace-computed vector B-IQ / output-capability appearance bounds with a tight information-shaped ceiling `⌈log₂ min(m,|𝒜|)⌉` (no channel-count factor, alphabet clip `|𝒜|` not `|𝒜|²`), attended-harm / extinction certificates, a concentration bridge with tight worst-case fallback for supplied blanket partitions, and a **real-valued (noncomputable) Shannon entropy/mutual-information development** (`Finite/ShannonMI`) proving `mutualInformation_le_log_min_card` — the general Shannon-theoretic fact (`MI ≤ log min(m,n)`, via Mathlib's concave-Jensen inequality applied to `Real.log`) underneath the N-8 empirical finding that the appearance *ceiling* (not the counting *score*) is a sound MI bound; not yet wired to `TraceBIQ`'s decidable rational pipeline (`metadata/TODO.md`). Debate/ELK remain later targets for native protocol/reporter theorem matching. | crosswalk appendix |
| `AlignmentProofSpine/FieldSubsumptions.lean` | compatibility re-export for the field-agenda headline theorem names | crosswalk appendix |
| `AlignmentProofSpine/Successors.lean` | `P27`, `P28`, `P29`, **`SuccessorSafeChain`**, **`SuccessorMeasurandChain`**, risk bound propagation; ch48 audit links are the explicit hypothesis record `SuccessorAuditLinks` (no global linking axioms), and safe chains reduce to measurand chains via `SuccessorSafeChain.toMeasurandChain` | 28–31 |
| `AlignmentProofSpine/Forgeability.lean` | ch08/ch31/ch48 successor-forgeability gap made a checked finite counterexample (`forgeability_gap`); bridge `MB10` (conserved-property signature not forged), declared here rather than in `Core.BridgeAssumptions` because it needs the numeric risk leaf, threaded explicitly like `SuccessorAuditLinks`; `true_harm_bound_of_successor_safe_step` shows what `MB10` buys on top of the existing risk-propagation machinery | 8, 31, 43, 48 |
| `AlignmentProofSpine/Adversarial.lean` | `P31`, `P34`, `P36R`, `P37` (`P33` in `CooperationGraph`) | 32–37 |
| `AlignmentProofSpine/Philosophy.lean` | `P41`, `P42`, `P44`, `P45` | 41–44 |
| `AlignmentProofSpine/Certification.lean` | `P01`, `P02`, `P30`, `P35`, finite-support `P40`, direct/bridge-derived layer evidence records, grounding required by `LayeredAlignedDef`, **`risk_bound_from_cci_slack`** (numeric risk leaf), **`certified_class_safety_from_bridge_record`** and **`certified_class_safety_spine_derived`** (`CertifiedSafetyCase` package) | 1–5, 37–38, 42, 48 |
| `AlignmentProofSpine/WorkedInstance.lean` | worked instances on **real committed data** from the same pinned generator (`synthesize_rows(300, ..., seed=5)` at git `408444b`): 26-row windows of `sample_capture_theater.jsonl` and `sample_honest_baseline.jsonl` packaged as `DiscreteTrace`/`EnvBlanket`, `decide`d trace-computed diversity/capacity/ceiling numbers, and `CCICertificate`s whose `manipulation` coordinate is *computed* from the real `judge_captured` column (not asserted) against thresholds fixed before either count was computed — the capture-theater certificate honestly **fails** (`workedCert_fails`, `26 > maxManipulation = 1`) and the honest-baseline certificate **passes** the identical thresholds (`honestCert_passes`, count `0`), yielding an actual `NumericRiskLeaf A 6`/`Risk A ≤ 6` (`honest_instance_risk_bound`; bound weak because the pre-registered thresholds are loose — reported at face value, not sharpened through placeholder coordinates); the single differing real coordinate flips the verdict, so the gate *discriminates*; fixture provenance pinned by `experiments/embedded-simulation/tests/contract/test_worked_instance_fixtures.py`; see the module docstring for the earlier (fixed) mistranscription-plus-reverse-engineered-thresholds version | 11, 26, 43, 46 |
| `AlignmentProofSpine.lean` | root module re-exporting all of the above | — |
| `scripts/check_axiom_budget.py` + `axiom-ledger.json` | tooling, not a proof module: mechanically diffs `#print axioms` on 17 headline theorems against the checked-in ledger and generates Appendix G's axiom-budget table (`metadata/axiom-budget-index.tex`) | appi:sec:axiom-budget |

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
  governance, or future theory (`MB1`–`MB10`, declared as `axiom`; `MB1`–`MB9`
  packaged in `BridgeAssumptions`, `MB10` threaded explicitly).
* **imported field theorem** — a source-cited external result or protocol
  assumption (`Field.Imported`) used to state what the external agenda proves
  under its own assumptions. These are distinct from `MB*` book bridges.

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
* **`Risk`** is `Control − CCI` (`RiskGap`). Certification uses `Control ≤ CCI + δ`
  as the numeric scalar-projection leaf. `CCICertificate` / `CCIThresholds` encode
  the manuscript's vector/status certificate, and `CCIVectorSupportsScalarSlack`
  records the bridge-shaped handoff from a passed vector certificate to that scalar leaf.
  Handle-controlled path: `CorrectionPath` / `SystemCorrectionPath` over `CorrectionChainLink`,
  now grounded in a correcting agent's controlled handles. The richer manuscript
  $C_{\mathrm{raw}}$ is represented as a certificate coordinate; the old weakest-link
  scalar remains inside `CCI` for existing arithmetic lemmas.
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
