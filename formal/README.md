# `formal/` — Lean dependency spine

A self-contained Lean 4 check of the *logical skeleton* of *Towards Superintelligence Alignment*. It shows which conclusions follow when the stated predicates hold, and it labels the steps it does not prove. It does not establish that any real system is aligned.



Conjectured graph: [`../context/lean_proof_dependency_graph.dot`](../context/lean_proof_dependency_graph.dot). Figures: [`../context/lean_proof_graphs/`](../context/lean_proof_graphs/).

Many counterexamples are finite `Bool` or `Fin` separations. Several named results are definitional. Abstract quantities often use integer proxies.

## Vocabulary


A **bridge** is an empirical or philosophical condition a later certificate relies on and the development does not prove. Lean declares it as an `axiom`. Reader-facing assumption boxes `A-001`–`A-014` are a different list. Appendix B (`appendices/appB-bridge-crosswalk.tex`) maps both onto standing problems in the field. A `*Crux` `Prop` (`BridgeCruxes.lean`, `MB2Identifiability.lean`, `MB4CorrectionIntegrity.lean`) is that same hypothesis packaged so a theorem can take it as an argument.

| Lean name | What has to be true, and is not proved here |
|-----------|-----------------------------------------------|
| `MB1_estimator_soundness` | A measured boundary certificate warrants the abstract boundary (the agent–environment cut). |
| `MB2Crux` | Evidence identifies value-bundle geometry. Not a field of `BridgeAssumptions`; a finite chain `MB2a` / `MB2b` / `MB2c` in `MB2Identifiability.lean`. A **value bundle** is a low-dimensional control direction (care, truth, autonomy, …), not a scalar reward. |
| `MB3_bearer_import` | A preserved **bearer map** — who or what the values apply to — makes transport more than keeping the words. |
| `MB4_correction_integrity` | **Correction-channel integrity** means later behavior tracks the correction operator: uptake and persistence, not only a legitimate reference. The **correction channel** is the path by which a correcting agent, through handles it controls, changes the system's later behavior. |
| `MB4a_measured_path_legitimacy` | Integrity implies the designated measured path is legitimate, including that the target has not captured the corrector's handles. Capture refutes integrity (`capture_defeats_correction_integrity`). Declared in `Correction.lean` because it needs `CorrectionPath`. |
| `MB5_ontology_shift_successor_audit` | Full transport plus bearer transport through a change of world-model yields successor safety. |
| `MB6a_gradient_estimator_soundness` | Coupling evidence identifies the correction-selection gradient. |
| `MB6b_correction_supporting_basin` | A shock-robust basin whose gradient is not too negative supports correction integrity. `BasinShockRobust` is a separate predicate and is not this antecedent. |
| `MB7a_access_model_soundness` | An adequate access model makes boundary discovery robust when the system tries to hide structure. |
| `MB7b_filter_family_coverage` | That access, plus adequate resolution, bounds hidden productive **boundary-information quality** (`HiddenBIQBoundedSys`). BIQ here is control relevant to the boundary that monitors do not see. The experiment lines use the same abbreviation for a different score (glossary). |
| `MB7c_hidden_biq_to_adversarial_robustness` | Bounded hidden BIQ plus correction integrity supports oversight that stays informative when the system optimizes against the measurement (**adversarial verifiability**: faking the signal costs more than the system can afford). |
| `MB7d_inferential_uad_detector_soundness` | An **unsupervised agent discovery** detector (inferring which variables form one acting unit, without a hand-labeled roster) warrants measurements of **inferential coupling**: coordination that remains after ordinary message channels are cut. |
| `MB8_cev_process_convergence` | Retired from the live record `BridgeAssumptions`. The axiom remains so one worked comparison with `MB6b` can still name it (`Chokepoint.lean`). Coherent extrapolated volition is an alignment *target* in `AlignmentConstruction.lean`, not a second route to correction. |
| `MB9_grounding_certificate_soundness` | A certified conservative abstraction warrants **grounding viability**: a value-relevant change moves the checked abstraction or raises its uncertainty. |
| `MB10_conserved_property_signature_not_forged` | A green checklist of **conserved properties** (what a successor must inherit) bounds true harm only if that checklist was adversarially verifiable up to the successor's capability. Without it, `forgeability_gap` is a finite counterexample. Declared in `Forgeability.lean` because it needs `RiskGap`. |
| `MB11_safety_case_adequacy` | A certified safety case plus `WithinDeploymentRiskTolerance` warrants the abstract predicate `Safe`. That tolerance is an acceptance judgment, not a computed probability. |
| `S07_mdl_positive_gain_preferred` | Minimum-description-length convention: a positive description-length gain means the first model is preferred. |
| `S10_blanket_measurand_coherence` | Measured predictive information does not exceed sensory capacity, measured control information does not exceed action capacity, and the memory and surprise penalties are nonnegative. |

`BridgeAssumptions` is a structure in `Core.lean`, filled by `standardBridges` from the axioms. A field of that structure can only mention predicates `Core.lean` already defines, so it holds `MB1`, `MB3`, `MB4`, `MB5`, `MB6a`, `MB6b`, `MB7a`–`MB7d`, and `MB9`.

Four hypotheses are stated in later files because the statement uses a definition `Core.lean` does not have yet:

* `MB2Crux` uses the finite value-bundle models (`MB2Identifiability.lean`).
* `MB4a_measured_path_legitimacy` uses `CorrectionPath` (`Correction.lean`).
* `MB10_conserved_property_signature_not_forged` uses `RiskGap` (`Forgeability.lean`, after `Capability.lean`).
* `MB11_safety_case_adequacy` uses `CertifiedSafetyCase` (`Certification.lean`).

A theorem that needs one of these takes it as an argument, so `#print axioms` still shows the dependency. `MB8_cev_process_convergence` is out of the structure for a different reason: the live certification path uses the alignment target in `AlignmentConstruction.lean`. The axiom remains so the comparison in `Chokepoint.lean` can still name it.

### Other short names in the code

**`CCI` — correction-channel integrity.** This asks whether the correction channel still works under pressure: the correcting agent still sees enough, still acts in time, and the system's later behavior still follows the correction. The scalar subtracts a weighted penalty sum (latency, manipulation, irreversibility, ontology translation) from the weakest link on that path. `RiskGap` reads this scalar. `CCICertificate` is the vector of the underlying measurements. Its scalar projection ignores five process coordinates — coercion, dependency, plurality, exit capacity, and independence — so a certificate can clear the scalar floor while those coordinates fail (`scalar_floor_blind_to_process`). The exchange rate the weights impose is under [The scalar prices heterogeneous units](#the-scalar-prices-heterogeneous-units).

**`RiskGap`.** `Control A` is the system's measured control information, how much it can do through its actuators (`Control A := IctrlSys A`, and `S10` requires that this not exceed action-channel capacity). `RiskGap A` is `Control A - CCI A`: control the correction channel does not cover. The certification path treats the quantity as information. A bound on it is an input to the safety case; the step from that case to the predicate `Safe` is the acceptance judgment `MB11`.

**`DeploymentMass`.** `DeploymentMass E A` is deployment leverage, μ_E(A) in the book: how much of environment E runs on system A. The environment is the institutions, markets, and protocols that copy, fund, integrate, and replace systems. A selection handle is a lever in that environment — procurement, compute allocation, authorization, release of a successor — and the number adds capacity over the handles that reach A. Correction uses the same `Handle` type in the other direction: correction asks whether a legitimate agent can change the system, and deployment leverage asks whether the environment is spreading it. Revenue, benchmark scores, and regulatory findings are not Lean terms. They enter only when they change which handles are used.

**`SuccessorSafe`.** `SuccessorSafe A B` means some `SuccessorSafeWitness` records that successor B still carries seven properties of A: the boundary still closes, memory lineage continues, value-bundle geometry is preserved, the bearer map is preserved, penalised correction-channel integrity is preserved, the transparency policy is preserved, and the control locus is continuous. Copying behavior while dropping one of these fails the predicate. `MB10` is the further claim that a green reading of this list bounds the successor's true harm, and that claim is unproved.

**`U_H`, `U_S`.** `ValueUpdateOperator` (`U_H`) is the schematic update of the legitimate value state, V_{t+1} = U_H(V_t, E_t, D_t), from evidence and deliberation. The type is opaque: certification uses `ValueUpdateEnvelope` and does not claim to have isolated a separable human-update mechanism. `SystemUpdateOperator` (`U_S`) is the system's own update when a correction arrives, (Θ_{t+1}, Z_{t+1}) = U_S(Θ_t, Z_t, C_t, E_t): parameters and the checked abstraction change. Successor and certification audits read that update through the vector certificate, in `rawCapacity` and `ontologyTranslation`, rather than through a separate preserved-operator field.

Glossary: [`appendices/appE-glossary.tex`](../appendices/appE-glossary.tex).


## Three buckets

Read `#print axioms` before citing a theorem.

| Bucket | Lean shape | What a reader should take from it |
|--------|------------|-------------------------------------|
| **Proved** | `theorem` / `def` | Machine-checked logic, arithmetic, or a finite rederivation. Often only `propext` / `Quot.sound`, or trust in the compiler when the proof is `native_decide`. |
| **Bridge** | `axiom MB*`, plus `S07`, `S10`, `WithinDeploymentRiskTolerance` | An axiom from Vocabulary. Never hidden inside a definition. |
| **Import placeholder** | opaque `Prop` in `Field.Imported` | A literature bookmark. Not the content of the finite rederivations. One exception is statement-bearing: `OA2016_offpolicy_qlearning_convergence` in `Field/Finite/BellmanQ.lean` (off-policy Q-learning convergence). |

`Field/Finite/DebateGame.lean` proves the deterministic claim-tree core (soundness and completeness given a correct judge; one judge error flips the outcome). `Irving2018_debate_truth_protocol_imported` is an opaque placeholder for the paper's bounded-judge, obfuscated-argument, and probabilistic-judge content. The game theorems do not rest on it.

Four labels for the book, matching the brief:

* **proof** — logical or arithmetic theorem (`P01`, `P10`, `P14`, `P27`, `P34`, the decision-problem squares below).
* **counterexample** — finite toy showing one notion does not imply another (`P15`, `P17`, `P18`, `P22b`, `forgeability_gap`, the separations in `Correction.lean` and `FrameIncompatibility.lean`).
* **bridge** — an axiom from Vocabulary.
* **imported field theorem** — a source-cited external result (`Field.Imported`, plus `OA2016_offpolicy_qlearning_convergence`). Distinct from the book's bridges.

## What the certification path checks

`P34_capacity_below_entropy_aliasing` (fewer signal classes than attack classes, so no detector is injective) and the other non-bridge results print only `propext` / `Quot.sound`, or abstract carriers.

`risk_gap_bound_from_cci_slack` derives `RiskGap A ≤ δ` from `Control A ≤ CCI A + δ` via `P13`. `NumericRiskLeaf` records whether that leaf came directly, from the vector certificate, from an `S10` slack certificate, or from a Markov-blanket profile (the boundary's sensory and active channels). The vector path does not assume a bare floor: `CCICertificate.lambdaProjection` computes the chapter-26 scalar from the certificate, and `CCIThresholds.lambdaFloor` induces a floor. `CCICertificateMeasures` (the certificate was actually measuring this system) stays bridge-shaped. Trace-computed blanket profiles feed the same leaf via `traceDerivedCCISlack` / `trace_derived_risk_bound`.

The headline non-definitional path is `FieldFinite.risk_gap_bound_from_trace_profile`: a trace profile, a passing vector certificate, and margin over the threshold floor yield `risk_gap_bound_from_threshold_certified_cci`. `WorkedInstance.honest_instance_risk_bound` instantiates it on committed data.

`P30_certified_class_safety_derived` packages that leaf with derived `Certified` (a coherent bundle of per-system certificates is inhabited; `Evidence.lean`), derived `SatisfiesInvariants`, and `LayeredAlignedDef`, into a `CertifiedSafetyCase`. The module says this step is assembly. `MB11_safety_case_adequacy` is the labeled bridge from that case plus `WithinDeploymentRiskTolerance` to `Safe` (`P30_safe_of_case`, `safe_from_spine_inputs`). `certified_class_safety_from_bridge_record` takes an explicit `BridgeAssumptions`; `certified_class_safety_from_spine_and_bridges` is the corollary from `standardBridges`.

Capture of any handle on the designated measured path yields `CCICapturedOrInvalid` (`capture_makes_cci_captured_or_invalid`) and refutes `CorrectionIntegrity`. `SystemCorrectionPath` carries data only (corrector, handles, capacities).

`MB9` turns a conservative value-correction abstraction certificate into `GroundingViable`.

## Finite rederivations of published arguments

`Field/` checks finite fragments of existing arguments under explicit interface conditions, plus separations (the field claim does not yield the book's predicate). `every_agenda_has_rederived_core` requires each agenda tag to have at least one such record. The manuscript calls this the field-agenda formalization (Appendix I, `sec:appi-field-formalization-gem`).

| Module | What is proved |
|--------|----------------|
| `Finite/IncompletePreferences.lean` | Thornley: partial preferences can refuse to rank a pair (POST incompleteness), a sweetening test separates a gap from indifference, timestep dominance, an agent with these preferences does not pay to shift shutdown probability. Contrast with expected-utility completeness. |
| `Finite/DynamicChoice.lean` | Thornley: an explicit money-pump on a timestep-dominance-permissible trade chain, and the resolute-choice escape (every finite tree has a plan realizing a maximal reachable outcome). |
| `Finite/ShutdownIncentives.lean` | Soares et al.: the incentive identity, prevention and seeking incentives, neutrality iff the shutdown utility equals the no-shutdown utility, utility indifference is local and buys no preservation (`soares_prevention_incentive`, `soares_indifference_knife_edge`). |
| `Finite/BellmanQ.lean` | Orseau–Armstrong: Bellman-target uniqueness, value iteration and greedy attainment, schedule invariance of the learned target. Stochastic-approximation convergence is the one imported axiom `OA2016_offpolicy_qlearning_convergence`. |
| `Finite/OffSwitchGame.lean` | Hadfield-Menell et al.: under genuine reward uncertainty, deferring to the human is strictly best; the incentive vanishes when the human is uninformative. |
| `Field/CIRL.lean` | Cooperative inverse reinforcement learning: a scalar assistance game is the one-coordinate case of a value-bundle game (`scalar_assistance_game_is_bundle_game_k1`). Deferring is optimal under reward uncertainty. The scalar case does not yield bundle preservation (`cirl_separation_profiles`). |
| `Field/Impact.lean` | Attainable utility preservation: over a finite horizon, the value of auxiliary actions is kept (`aup_horizon_attainable_utility_preserves_previous_value`). That need not keep every tracked option. A low-impact penalty is separated from correction-channel integrity. |
| `Finite/QuantilizerMaximin.lean` | Taylor: a bounded density ratio is sufficient and necessary for the worst-case cost guarantee. |
| `Finite/DebateGame.lean` | Irving et al.: on claim trees, the min-max value equals the truth when the judge is correct; one judge error flips the outcome (`debate_defender_wins_iff_true`, `debate_judge_error_flips_outcome`). |
| `Finite/AmplificationTree.lean` | Iterated amplification: leafwise soundness by induction; one leaf error flips the root (`amplification_leaf_error_amplified`). |
| `Finite/ELKIdentifiability.lean` | Eliciting latent knowledge (Christiano, Cotra, Xu). See the next subsection. |
| `Finite/ShannonMI.lean` | Real-valued Shannon mutual information: `mutualInformation_le_log_min_card` (`MI ≤ log min(m, n)`). This is the bound behind the appearance *ceiling* in the trace code. It is noncomputable and not yet connected to `TraceBIQ.lean`'s decidable rational pipeline. |
| `Finite/TraceBIQ.lean` | Trace-computed vector boundary-information quality and output-capability appearance, with ceiling `⌈log₂ min(m, \|𝒜\|)⌉`. Also attended-harm certificates and a concentration bound with a worst-case fallback (`trace_attended_harm_certificate_below_extinction`, `concentration_bridge_harm_below_extinction`). |
| `Finite/Nonrealizability.lean` | Off-class unsafe behavior, ambiguity-set transfer, a class certificate does not yield deployment safety. No new bridge. |
| `Finite/RegretSafety.lean` | Zero regret on the wrong loss, and a prefix catastrophe, are not safety. A conditional transfer from loss and exploration to zero harm. No new bridge. |
| `Finite/CompositePathBypass.lean` | A green named path plus a composite bypass does not yield correction integrity. |
| `Finite/LobTiling.lean` | Conditional Löb from supplied provability closures: a diagonal successor is not accepted by reflecting only the same system's proof of its safety. An audit link can transport a numeric bound with no provability predicate. The fixed point and the closures are field hypotheses, not book bridges. |

### Eliciting latent knowledge

`ELKIdentifiability.lean` (aliases in `Field/ELK.lean`):

* On confident rows (observation already matches the latent), the direct translator and the human simulator agree, and every function of their answer lists agrees (`no_training_criterion_separates`). They diverge on a tampered row. Together: `elk_reporter_nonidentifiability`.
* A human label that disagrees with the latent makes zero-one loss prefer the simulator (`human_mistake_prefers_simulator`).
* On the tampered row the simulator is unambiguously wrong and the observation still looks good (`human_simulator_is_crisp_counterexample`). Search that trusts the observation accepts that row; search that requires the translator rejects it.
* Inside a human model, no training criterion separates model-internal inference from the translator. Outside the model they diverge (`no_operator_training_criterion_separates`, `outside_human_model_diverges`).
* A model with no latent node yields observation labels, so the same non-separation applies (`ontology_mismatch_training_does_not_separate`).
* `cost_crossover_complexity`: at size 8, a `log₂` cost is below a linear cost. That witnesses the report's slower-growth comparison. It does not simulate the report's example.

`elk_readout_is_correction_projection` is an older interface toy. It assumes the readout-bandwidth identification it appears to derive, and it is not an `ELKIdentifiability` theorem.

## Alignment criteria

`Frame*.lean` is a separate development from the certification spine. It does not add bridges. It is the machine-checked side of *Combining Alignment Criteria* (`papers/alignment-criteria/`); the relation graphs live in `drafts/alignment-frames-relations.md`. Headline names are in `axiom-ledger.json` under `FrameRelations`.

An alignment criterion here is a way of scoring or constraining outcomes (a scalar reward, a floor, a Pareto order, a correction constraint, a shutdown bit). The proofs say when two criteria cannot be met together, and when a map between decision problems preserves the choice.

| Module | What is proved |
|--------|----------------|
| `FrameIncompatibility.lean` | Red edges as `Incompatibility` proofs, in four classes (`IncompatClass`): the carrier cannot hold the distinction (`representability`); both criteria choose on the same menu and disagree (`choiceConflict`); one accepts only the part of the other that changes nothing it cares about (`rigidity`); the total is fixed (`sharedResource`). No finite positive weights represent a floor (`no_finite_weights_represent_floor`), with the same fact pulled back to deontic bans, non-observability, and a correction-channel-integrity floor. Pareto does not entail a floor; a coordinate that *is* the floor does (`pareto_with_floor_coordinate_meets_floor`). `registry_matches_proofs` ties the edge list to the proofs. Closed walks of a gradient sum to zero (`gradient_closed_walk_zero`). |
| `FrameDecision.lean` | The scores cluster as decision problems: an objective pulls back along a map, and choosing commutes (`argmax_pullback` and the squares in the module docstring). Counting beside those ∀ results, in the style of Turner's power-seeking orbits: `copies_count_le`, `correction_avoided_card_fold`, and the decided examples `turner_corrigible_quarter`, `option_preserving_correction_half`. |
| `FrameHistoryState.lean` | A reward that sees the whole record can price a route exactly (`route_exact_on_records`). A utility of the current state alone cannot represent that route (`unrecorded_route_not_representable`). A record that ignores whether the channel was kept is the Soares button model (`channel_blind_record_is_button`). |
| `FrameCorrector.lean` | A correction is pending; the agent may accept, contest, disable the channel, or manipulate the corrector. Under a constraint that requires the channel and forbids influence, the corrector decides for every utility (`corrector_decides_under_constraint`), and contesting through the channel is the remaining outlet. A constraint that does not measure influence cannot tell contest from manipulation (`blind_constraint_cannot_separate`). |
| `FrameDisclosure.lean` | A verified report that pays at least the gap's gain beats using the gap at every detection rate, including zero (`verified_report_beats_use`). A penalty never reaches an undetected gap (`penalty_cannot_reach_undetected`). Setting the disclosure penalty equal to the expected penalty for concealing makes disclosure optimal and leaves the incentive not to fail unchanged (`matched_amnesty_keeps_deterrence`); a further discount costs that much deterrence. Finite form of Kaplow and Shavell. |
| `FrameLimits.lean` | Robust viability (the set stays good for every disturbance in a class) is strictly stronger than viability at one disturbance (`viable_not_robust`). A quantilizer's support becomes the argmax set in the stated limit (`quantilizer_limit_is_argmax`). A forced halt converges (`forced_halt_converges`). |
| `FrameLockIn.lean` | Robust invariance of a captured set does not see the sign of the drift (`robust_invariance_sign_blind`): a stable basin can be a stable bad one. |
| `FrameRelations.lean`, `FrameComposePaths.lean`, `FrameMorphisms.lean` | Which edges are derived, which compose-paths partition the slots, and which maps have a declared source and target carrier. |

## Instances on recorded data

`WorkedInstance.lean` uses committed rows from one pinned generator (`synthesize_rows(300, …, seed=5)` at git `408444b`): windows of `sample_capture_theater.jsonl` and `sample_honest_baseline.jsonl`. Thresholds were fixed before either manipulation count was computed. The capture-theater certificate fails (`workedCert_fails`, count 26 against `maxManipulation = 1`). The honest-baseline certificate passes the same thresholds (`honestCert_passes`, count 0) and yields `RiskGap A ≤ 6` (`honest_instance_risk_bound`). The bound is weak because those pre-registered thresholds are loose. Provenance: `experiments/embedded-simulation/tests/contract/test_worked_instance_fixtures.py`.

`BacktestC2Instance.lean` pins a tool-scout host log (`experiments/backtest/fixtures/c2-tool-scout-v1.json`) as a path audit: the named path is green, and the bypass count computed from `composite_log` exceeds `maxWorldEffectsAfterDefer = 0`, so the log is not correction integrity (`c2_pinned_green_named_with_bypass_not_integrity`). The proof is `native_decide`, so `#print axioms` also lists `Lean.ofReduceBool` and `Lean.trustCompiler`. Floats and correction-channel-integrity slots are refused. This is not `Safe` and not `MB11`.

`ToyDeploymentGate.lean`: a decidable gate on a frozen validation battery (`frozen_validation_battery_gate_passes`, 3/36 false passes against a pre-registered maximum of 5). A passing gate is a candidate shape for `WithinDeploymentRiskTolerance`. It does not discharge that axiom.

`SpineModel.lean`: the bridge axioms are jointly consistent (`spine_axioms_consistent`), the measurand model is non-degenerate, and each labeled hypothesis is independently load-bearing. `scripts/check_spine_model.py` checks that list.

## The scalar prices heterogeneous units

`CCI A` subtracts a weighted penalty sum from the weakest link on the correction path (chapter 46). The weights fix an exchange rate between latency, a manipulation count, irreversibility and ontology scores, and raw channel capacity. `CCICertificate.lambdaProjection` uses the same weights (`CCICertificateMeasures.weights_eq`). `CCICertificatePasses` checks each coordinate against its own threshold; the worked instance exercises that gate. `CCIThresholds` is a deployment input, in the same epistemic class as `MB1`: the arithmetic does not decide what tolerance to accept. `CCIVectorSupportsScalarSlack` is the bridge-shaped handoff from a passed vector certificate to the scalar leaf.

## Build

Toolchain: [`elan`](https://github.com/leanprover/elan), pinned in `lean-toolchain` to `leanprover/lean4:v4.28.0`. Mathlib `v4.28.0`. First build downloads Mathlib; `lake exe cache get` in `formal/` fetches precompiled oleans when online.

```bash
make lean                 # from repo root: cache + lake build + python guards
# or: ./formal/check.sh
```

`check.sh` runs `lake exe cache get` (needs network) then `lake build`, unless `--no-build`. GitHub Actions uses `./formal/check.sh --no-build` after `lean-action`.

Inspect what a theorem rests on:

```bash
cd formal
echo 'import AlignmentProofSpine
open AlignmentProofSpine
#print axioms certified_class_safety_from_bridge_record' > /tmp/chk.lean
LEAN_PATH=.lake/build/lib/lean lean --root=. /tmp/chk.lean
```

`scripts/check_axiom_budget.py` diffs `#print axioms` for the headline theorems against `axiom-ledger.json` and regenerates the Appendix G table (`metadata/axiom-budget-index.tex`). An intentional drift is accepted with `--update`.

```bash
./formal/check.sh
./formal/check.sh --no-build
python3 formal/scripts/check_axiom_budget.py --update
```

`formal/playgrounds/` holds short snippets for the companion site. They compile alone and are not part of `lake build`.

Manuscript cross-references: `\leanspine{kind}{node}{gloss}` in `metadata/preamble.tex`.

## Module index

| Module | Role |
|--------|------|
| `Core.lean` | Carriers, handles, boundary and grounding predicates, `MB1`–`MB9` except the ones declared later, `BridgeAssumptions`, `S07`. |
| `MB2Identifiability.lean` | Finite value-bundle chain; `bundle_aligned_from_mb2_chain`. Chapters 15–21. |
| `MB4CorrectionIntegrity.lean` | Legitimacy, uptake, and persistence; `preserves_correction_from_mb4_chain`. Chapters 25–26. |
| `BridgeCruxes.lean` | Core hypotheses as `Prop`s; `certified_class_safety_from_core_cruxes`. |
| `AlignmentConstruction.lean` | `AlignmentTarget`, constitutions (`cevConstitution`, `caiConstitution`, …), `Realizes`, `ConstructionCrux`. Target realization is this interface, not an `MB*` axiom. |
| `AlignmentRegime.lean` | Uninterpreted `DeploymentOk`. A pause does not yield the toy certificate (`fin_pause_ok_not_certified`). No arrow to `Safe`. |
| `Boundaries.lean` | `P05`–`P09`, `P36`. Access-equivalence and knowledge-equivalence do not identify the hidden state. |
| `Capability.lean` | `P10`–`P13`, `P32`, `P43`, blanket profiles, hidden-BIQ certificate, collective-competence bottleneck `P12`, `RiskGap`, `S10`. |
| `CooperationGraph.lean` | Unsupervised agent-discovery audit to a derived graph; inferential-coupling score; `P33`. |
| `Bundles.lean` | Value-bundle transport. Proofs `P14`, `P16`, `P19`–`P22a`. Counterexamples `P15`, `P17`, `P18`, `P22b`. |
| `Correction.lean` | Scalar `CCI`, `CCICertificate`, `CorrectionPath`, `MB4a`, capture theorems, separations (shutdown, interruptibility, impact, quantilization, debate, amplification, latent readout do not yield correction-channel integrity). |
| `Successors.lean` | `P27`–`P29`. Safe chains reduce to measurand chains via `SuccessorSafeChain.toMeasurandChain`. Audit links are the hypothesis record `SuccessorAuditLinks`. |
| `Forgeability.lean` | `forgeability_gap`, `MB10`, `true_harm_bound_of_successor_safe_step`. |
| `Chokepoint.lean` | `AdversariallyVerifiableUpTo`, `SteerableAt`. A shared verification channel gives no independent failure tolerance (`sharedChokepoint_steerable_blocks_both_routes`); independent channels can diverge. |
| `Defeaters.lean` | Per-hypothesis ways the antecedent fails, with finite toys for several of them. |
| `FieldInterfaces.lean` | Book-facing interfaces: coverage evidence into `MB9`; regret evidence is not `RiskGap`; a positive measured-path certificate needs legitimacy, coverage, and no bypass. |
| `Evidence.lean` | Per-system certificates and eval-soundness adapters. `CoherentCertificateBundle`. Derived `Certified`. `SafeIn` does not retarget `MB11`. |
| `Certification.lean` | `P01`, `P02`, `P30`, `P35`, `P40`, the risk leaf, `MB11`, `AlignmentDeployment`. |
| `Adversarial.lean` | `P31`, `P34`, `P36R`, `P37`. |
| `Philosophy.lean` | `P41`, `P42`, `P44`, `P45`. |
| `Field.lean`, `Field/*.lean`, `FieldSubsumptions.lean` | Agenda wrappers and the re-export of headline names. Finite proofs: section above. |
| `WorkedInstance.lean`, `BacktestC2Instance.lean`, `ToyDeploymentGate.lean`, `SpineModel.lean` | Data instances and the consistency checklist. |
| `Frame*.lean` | Alignment criteria. Section above. |
| `AlignmentProofSpine.lean` | Root re-export. |
| `Mathlib.lean` | Shared lemmas, including the finite pigeonhole used by `P34`. |

## Deviations from the brief

* Lean 4 has no `constant`. Abstract carriers are `axiom`; concrete structure is `structure` or `def`.
* No `sorry` or `admit`. Where the brief's placeholder needed empirical content, the development uses an explicit bridge.
* Counterexamples use finite `Bool` / `Fin` models, as the brief requires.
* `P44` uses two disagreeing legitimacy orderings, per the brief's amendment.
* Brief nodes `P38` / `P39` (a tripwire failure decertifies) are absent. `P40_unsupported_leaf_blocks_root` stands without them.
* `P34` uses Mathlib's `Fintype.card_le_of_injective` via `Mathlib.lean`.
* Node ids match theorem names in `AlignmentProofSpine/*.lean`.
