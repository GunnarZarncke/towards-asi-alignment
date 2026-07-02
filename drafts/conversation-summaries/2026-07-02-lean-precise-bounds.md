# 2026-07-02 — Lean spine: more precise bounds, chokepoint, defeaters, axiom-budget guard, forgeability/`MB10`

## Trigger

User asked to review the Lean spine against the chapters it represents and strengthen it with more precise bounds where the chapters supply formal structure (explicitly *not* proving `MB*`), consulting past reviewer feedback via subagent. Work items were drawn from the open rows in `metadata/TODO.md` § chapter ↔ Lean mapping gaps.

## Done

### 1. Tight trace appearance ceiling (`Field/Finite/TraceBIQ.lean`, ch11)

- Switched pattern counters from `eraseDups` to Mathlib `dedup` (same values, usable lemmas) and proved support-count lemmas (`marginalPatternCount_le_length/_le_alphabet/_le_joint`).
- Proved `log2CeilBits_mono` and `finsetSupInt_le_bound` (sup of bounded values is bounded — no cardinality factor).
- New tight ceiling `diversityAlphabetCeiling m nAlpha = ⌈log₂ min(m,|𝒜|)⌉`: proved `laggedPatternDiversity_le_alphabet_ceiling` (joint support dominates marginals, so hx+hy−hxy ≤ min marginal) and `laggedDiversityScore_le_alphabet_ceiling`.
- Replaced the `|A|·|E|·⌈log₂ min(m,|𝒜|²)⌉` optimism budget with `traceDiversityTightOptimism` for control, predictive, attended-output, and B-IQ (2×) appearance bounds; subsample versions; `tight_optimism_le_control_optimism` shows strict domination on nonempty channel sets. Old product bounds retained for compatibility.
- Tight deterministic concentration-bridge fallback `traceAttendedOutputTightWorstCaseBridge` and `trace_attended_harm_tight_worst_case_extinction_threshold` (output cap only needs to dominate the tight ceiling).
- TODO item (3) partial: named trace→risk leaf `traceDerivedCCISlack` / `trace_derived_risk_bound` feeding `MarkovBlanketBIQDerivedCCISlack` → `NumericRiskLeaf.fromMarkovBlanketBIQ`.
- ch11 `eq:trace-ctrl-appearance` updated to the tight form; `\leanspine` tag now cites `subsample_output_capability_le_tight_optimism`.

### 2. Derived scalar CCI floor (`Correction.lean` + `Capability.lean`, ch26)

- ch26 Eq. `eq:cci-ch26` scalar projection is now a Lean function `CCICertificate.lambdaProjection`.
- `CCICertificateMeasures` record isolates the bridge-shaped measurement-alignment hypotheses (certified coordinates over-approximate measured penalties, raw capacity under-approximates the weakest link, weights nonnegative).
- Proved `CCICertificate.lambdaProjection_le_CCI`, θ-derived floor `CCIThresholds.lambdaFloor`, `lambdaFloor_le_lambdaProjection`, `CCI_ge_threshold_floor`; constructors `CCIVectorSupportsScalarFloor.ofMeasures/.ofThresholds`, `CCIVectorSupportsScalarSlack.fromThresholdFloor`, and `risk_bound_from_threshold_certified_cci` — certification thresholds now bound the primary numeric slack directly; `scalarLowerBound` no longer needs to be a bare assumed field.
- ch26 `\leanspine{P24}` gloss extended.

### 3. ch13 weighted coordination bottleneck (`Capability.lean`)

- `weightedLocalCompetence` / `weightedCollectiveCompetence` as `Finset.sum` model of `eq:collective-competence` (Σ ωᵢKᵢ + G − Ω).
- `weightedLocalCompetence_update` (increment δ at i moves the sum by exactly ωᵢδ), `P12_disconnected_competence_gain_is_lost` (ωᵢ=0 authority loss), `P12_coordination_bottleneck_partial` (discrete ∂K_coll/∂K_i ≤ 0), `P12_seven_loss_bottleneck` (seven-loss instantiation).

### 4. Successor audit links de-axiomatized (`Successors.lean`, `Certification.lean`, ch48)

Follow-up to the reviewer-feedback subagent scan: two audits (ad-hoc/ontology audit `f7cca860`, non-Field spine audit `bf2f1108`) flagged `CCIPreserved_implies_monotone` / `ControlLocusPreserved_implies_control_antitone` as bare global axioms.

- Removed both axioms. They are now fields of the explicit hypothesis record `SuccessorAuditLinks` (same style as `BridgeAssumptions`), threaded through `SuccessorSafe_risk_monotone`, the safe-chain risk/slack theorems, and the three chain theorems in `Certification.lean`.
- Unified the two chain notions: `SuccessorSafeChain.toMeasurandChain` reduces every successor-safe chain to a numeric `SuccessorMeasurandChain` given the links; all safe-chain propagation now goes through that reduction (the `hpres`-parameterized induction was removed).
- `#print axioms` confirms the chain theorems depend only on carrier/predicate axioms — the two linking axioms are gone from the footprint.
- Appendix `appi:def:spine-successor-monotone`, `appi:cor:successor-risk-monotone`, `appi:cor:successor-chain-risk` updated to state the record hypothesis; `formal/README.md` Successors row and `metadata/TODO.md` certification-chain row updated.

### Docs synced

- `appendices/appG-lean-proof-spine.tex`: new lemma blocks `appi:lem:cci-lambda-floor`, `appi:lem:p12w`; tight-ceiling paragraph with `appi:eq:tight-appearance-ceiling`; updated numeric-risk-leaves corollary and concentration-bridge paragraph.
- `formal/README.md` module map + notation paragraph; `metadata/TODO.md` rows for TraceBIQ, CCI penalties, and P12 updated.

## Verification

- `lake build` in `formal/` passes (1721 jobs; only pre-existing warnings).
- `#print axioms` on all new theorems: only `propext`/`Classical.choice`/`Quot.sound` plus abstract carriers — **no `MB*` dependence**.
- `make check` passes; `./build.sh` run at session end.

## Decisions

- Kept old product-optimism bounds and `spuriousDiversityCeiling` clip in place (compatibility; the tight results are theorems on top, plus a domination lemma) rather than redefining the score.
- Measurement alignment (`CCICertificateMeasures`) deliberately stays a visible hypothesis record, not an axiom — same policy as other bridge-shaped handoffs.
- `eraseDups` → `dedup` change is value-preserving (both count distinct elements); done to get Mathlib lemma coverage.

### 5. User asked for "other suggestions / step back on approach"; recorded, then acted on top pick

After the reviewer-feedback subagent summary, the user asked for further ideas beyond the transcript-derived list. Given (not yet all executed — see §6 for what was executed):

- **Prioritized the remaining subagent list**: correlated-failure chokepoint (elevated to top — argument-level, not just code-level) > `ValueUpdateCertificate` vectorization > probabilistic `MB1` (drop ε=1 hardcode) > `P33`/`componentLarge` strengthening.
- **Diminishing-returns note**: further integer-inequality lemmas add less now than making one path *executable* end-to-end (compute an actual `CCICertificate`/ceiling/δ from a concrete `experiments/` trace inside Lean — tests estimability, not just arithmetic).
- **Systematize defeaters**: pair each `MB*` axiom with either a finite converse-counterexample, a documented reason none is possible, or a stated observation that would refute it.
- **Axiom-budget guard**: a small CI script running `#print axioms` on headline theorems, diffed against a checked-in ledger, so "assumptions are never hidden" is self-enforcing and doubles as an auto-generated appendix table.
- **Structural doubt**: the forgeability problem (BIG REVIEW item, ch08/ch46/ch48) may be formalizable *against* the spine — a finite model where `SuccessorSafeWitness` + audit links hold yet a harm quantity outside `Risk = Control − CCI` grows. Suggested naming the "measurands vs what matters" gap as an explicit bridge (candidate MB10 / widened MB5) rather than leaving it implicit.

None of the above four (executable path, defeater pairing, axiom-budget CI, MB10 naming) were implemented this session — recorded here as the standing suggestion list for a future session.

### 6. Correlated-failure chokepoint formalized (`Chokepoint.lean`, new module)

Acted on the elevated top pick: formalized ch43's (`chapters/ch43-verifiability-and-ontology-adequacy.tex`, §`sec:cost-relation-ch43`) "adversarially verifiable up to κ" cost-relation definition — previously **0% formalized** despite being a load-bearing, explicitly `[Conjectural]`-tagged concept — and used it to make precise the 2026-06-30 external review's structural claim that "disjunctive routes (`MB6b` or `MB8`) add failure tolerance" is illusory if both routes share the adversarial-verifiability antecedent.

- New file `formal/AlignmentProofSpine/Chokepoint.lean`:
  - `MeasurementChannel` (`reads`/`costFake`/`affordableSurplus`), `AdversariallyVerifiableUpTo`/`SteerableAt` — direct Lean translation of ch43 Eq. (line 80).
  - `VerifiabilityGatedBridge` — reformulates an `MB*`-style axiom as `sound : verifiable → reads → consequent`, making the ch43 caveat part of the type.
  - `sharedChokepoint_verifiability_iff` / `sharedChokepoint_steerable_blocks_both_routes` (**axiom-free**, `#print axioms` confirms) — if two gated bridges share a channel, losing verifiability blocks both simultaneously; the "OR" is not independent-failure-mode robust.
  - `independent_channels_can_diverge` — constructive toy counterexample showing genuine independence *is* possible in principle (the shape a fix would need).
  - Worked instance at the book's actual `System`/`MB6a`/`MB6b`/`MB8`: `percolationChannel`, `valueUpdateChannel`, named (not axiomatized) `SharedInstrumentHypothesis`, `percolationGatedBridge`/`valueUpdateGatedBridge` (their `sound` fields discharge via the existing `MB6a`/`MB6b`/`MB8` axioms unchanged), and `correction_integrity_disjunctive_tolerance_needs_distinct_instruments`.
- `#print axioms` on the worked-instance theorem shows exactly `MB6a`, `MB6b`, `MB8` plus abstract carriers — no new axiom was introduced; the module states a conditional ("if instruments are shared, tolerance collapses"), not a proof that they *are* shared.
- Docs synced: `formal/AlignmentProofSpine.lean` + `formal/README.md` module tables; new appendix subsection `appendices/appG-lean-proof-spine.tex` §`appi:sec:chokepoint` (definitions + theorem + two corollaries); `appendices/appF-research-program.tex` disjunctive-tolerance paragraph reworded to state the independence proviso and cite the review + new Lean ids; `appendices/appB-bridge-crosswalk.tex` takeaway sentence split to flag the one qualification; `chapters/ch43-verifiability-and-ontology-adequacy.tex` gets a `\leanspine{proof}{AdversariallyVerifiableUpTo}{...}` gloss after the cost-relation claim.
- `metadata/TODO.md` BIG REVIEW item marked `[~]`: fix options (1)/(2) done formally; (3) per-chapter WWCTV forward references and (4) uncertainty-ledger reconciliation still open; the underlying empirical question (are `MB6b`/`MB8` actually shared or independent?) is explicitly **not** resolved — `SharedInstrumentHypothesis` stays a named, undischarged hypothesis by design.

### 7. Systematized `MB1`–`MB9` defeaters (`Defeaters.lean`, new module)

User follow-up: "Systemize defeaters as suggested" — the second item from §5's standing list. For every bridge, named an observable **signal** (a `Prop`, not a claim) that would be a candidate falsifier of the bridge's consequent, traced to the exact "failure mode if false" language already in `metadata/assumptions-ledger.md` §I and the matching `metadata/uncertainty-ledger.md` U-ID.

- New file `formal/AlignmentProofSpine/Defeaters.lean` with a header status table for all 13 sub-bridges (`MB1`–`MB9`, `MB6a`/`MB6b`, `MB7a`–`MB7d`).
- Named-vocabulary axioms (style-matched to existing bare predicates like `BasinStableSys`): `GradientEquivalenceEstimationArtifact` (MB2), `BearerMapSpoofed` (MB3), `OntologyShiftUnaudited` (MB5), `PercolationEvidenceConfounded` (MB6a), `LockedInBadBasin` (MB6b), `AccessModelGamed` (MB7a), `JudgeManipulated` (MB4), `LegitimacyTheater` (MB8), `OntologyDriftBeyondCertifiedDomain` (MB9).
- Four finite toy models (following the spine's existing counterexample convention — fresh toy carriers, not the real opaque `System`-level predicates) proving the antecedent-signal-not-consequent shape is **logically consistent**: `MB1_defeater_toy_nonstationary_shift` (calibration-time certificate, later distribution shift), `MB4_defeater_toy_manipulated_judge`, `MB6b_defeater_toy_lock_in`, `MB8_defeater_toy_legitimacy_theater`. `#print axioms` on all four: only `propext` — no `MB*` dependence, confirming each is a fact of pure logic, not conditioned on any bridge.
- `MB7b`–`MB7d` deliberately reuse `Chokepoint.SteerableAt` as their signal (via `MB7bcd_defeater_signal`) rather than inventing new ad hoc vocabulary, since their consequents are exactly the adversarial-measurement claims ch43's cost relation targets.
- Hit one naming collision (`ToyPreservesCorrectionOperator`/`ToyPreservesValueUpdateOperator` already existed in `Correction.lean`) — fixed by prefixing all new toy identifiers with the bridge name (`MB4DefeaterToy*`, `MB8DefeaterToy*`, etc.).
- Docs synced: `formal/AlignmentProofSpine.lean` + `formal/README.md` module tables; new appendix subsection `appendices/appG-lean-proof-spine.tex` §`appi:sec:defeaters`; `metadata/assumptions-ledger.md` §IV cross-links back to the new Lean module; `metadata/TODO.md` new item.
- Explicitly **not** done: toy models for `MB2`, `MB3`, `MB5`, `MB6a`, `MB7a`, `MB9` (named signal only — recorded as a deferral in the module's own header table, not silently dropped).

### 8. Axiom budget mechanically guarded + Appendix G table generated (`formal/scripts/check_axiom_budget.py`, new)

User follow-up: "Guard the axiom budget mechanically and generate the appendix table from it" — the axiom-budget-guard item from §5's standing list.

- New `formal/scripts/check_axiom_budget.py` + checked-in snapshot `formal/axiom-ledger.json` (13 curated headline theorems, each with a short gloss and its expected sorted axiom list).
- Script generates a scratch `.lean` file with `#print axioms <name>` for every ledger entry, runs it via `lake env lean` from `formal/`, parses the (possibly multi-line) output, and diffs each theorem's actual axiom set against the ledger — classifying any drift as `core` (`propext`/`Classical.choice`/`Quot.sound`), `bridge` (`MB\d...`), or `vocabulary` (everything else). Exits 1 on drift with a `+`/`-` diff; `--update` accepts the current output as the new ledger (for intentional spine changes); `--no-lean` regenerates only the `.tex` table from the existing ledger (no Lean invocation, useful for pure doc iteration).
- The curated 13 span three regression-guard shapes: (a) should-stay-axiom-free sanity checks (`sharedChokepoint_steerable_blocks_both_routes`, the four `MB*_defeater_toy_*` theorems — confirmed `propext`-only or fully axiom-free), (b) should-have-exactly-these-bridges checks (`correction_integrity_disjunctive_tolerance_needs_distinct_instruments` → exactly `MB6a`/`MB6b`/`MB8`), and (c) the full-vs-none bridge contrast at the top of the spine: `certified_class_safety_from_bridge_record` (bridges supplied as an explicit `BridgeAssumptions` value — **zero** `MB*` in its own footprint, confirmed by the script) vs. `certified_class_safety_from_spine_and_bridges` (calls `standardBridges` internally — **all nine** `MB1`–`MB9`, confirmed). That full-vs-none contrast was previously only implicit in the code; the ledger makes it an explicit, checked fact.
- Verified the guard actually guards: injected a fake extra bridge axiom into one ledger entry, confirmed `check_axiom_budget.py` exits 1 with a correctly classified diff line; restored the ledger and confirmed a clean pass.
- Script also (re)generates `metadata/axiom-budget-index.tex` (longtable matching the doc's existing `\toprule`/`\endfirsthead`/`\endhead`/`\bottomrule`/`\endfoot` convention, `\leanid{}` for breakable identifiers so long dotted/underscored names wrap instead of overflowing), `\input`-ed from a new Appendix G subsection `appendices/appG-lean-proof-spine.tex` §`appi:sec:axiom-budget` ("Axiom budget", Table `tab:appi-axiom-budget`) placed at the end of the "Reading the Appendix Against Lean" section.
- Full `./build.sh` run twice while tuning column widths (`p{0.23\linewidth}p{0.19\linewidth}p{0.28\linewidth}rr`) to clear the worst overfull-hbox warnings (down to one ~11pt overfull for the longest identifier, well within the book's existing ~583-overfull-hbox baseline noise); rendered pages visually inspected via `magick`/`pypdf` (installed in a throwaway `/tmp` venv, not a repo dependency) — table renders cleanly within margins on both its two pages.
- Docs synced: `formal/README.md` (new "Axiom budget guard" paragraph after the manual `#print axioms` example, module-map row for the script/ledger), `metadata/TODO.md` (new `[x]` item), `metadata/assumptions-ledger.md` §IV (new paragraph cross-linking the guard).
- Not wired into `make check` (root Makefile's check chain is LaTeX-only and doesn't assume a Lean toolchain); invoked manually from `formal/` per the README instructions.

### 9. Successor forgeability formalized against the spine; new bridge `MB10` (`Forgeability.lean`, new module)

User follow-up: "Formalize the forgeability problem against the spine and add the MB (in all relevant places including the diagram)" — the `MB10`-naming item flagged but not executed in §5.

- New file `formal/AlignmentProofSpine/Forgeability.lean`:
  - `forgeability_gap` (finite counterexample, axiom footprint `propext`/`Classical.choice`/`Quot.sound` only): for every claimed harm bound `δ`, a toy successor reads green on every conserved-property check and stays within the measured risk bound while its true harm exceeds `δ` — makes ch08/ch31's own WWCTV prose ("all seven read green and the successor is lethal") a checked fact rather than a residual worry.
  - New vocabulary `TrueHarm : System → Int` (ch08/ch31's "unmeasured remainder") and `ConservedPropertySignatureVerifiable : System → System → Prop` (ch43's cost relation, specialized to this measurand — deliberately *not* formally unified with `Chokepoint.MeasurementChannel`, since that reads a single system and this gate is a transition-pair property; left as an explicit open item).
  - **`MB10_conserved_property_signature_not_forged`**: `SuccessorSafe A B → ConservedPropertySignatureVerifiable A B → Risk B ≤ δ → TrueHarm B ≤ δ`.
  - `true_harm_bound_of_successor_safe_step`: composes `SuccessorSafe_risk_monotone` (given `SuccessorAuditLinks`) with `MB10` to turn a predecessor's risk bound into a true-harm bound at the successor.
  - **Architectural finding:** `MB10` cannot be a field of `Core.BridgeAssumptions` like `MB1`–`MB9` — its statement needs `Risk`, which is not defined until `Capability.lean`, strictly after `Core.lean` builds `BridgeAssumptions`. It is declared in `Forgeability.lean` and threaded explicitly, in the same style as `Successors.SuccessorAuditLinks` (which has the identical constraint). `standardBridges`/`certified_class_safety_from_spine_and_bridges` are therefore **unchanged** (still exactly `MB1`–`MB9`).
  - One `omega` snag: goals over `abbrev`-wrapped structure-field comparisons didn't unfold automatically for `omega`; fixed with `show ¬ δ + 1 ≤ δ` before `omega` rather than `unfold` (which left the projection unreduced).
- Axiom-ledger additions (`formal/axiom-ledger.json`, `formal/scripts/check_axiom_budget.py`): two new headline entries (`forgeability_gap`, `true_harm_bound_of_successor_safe_step`); split `ALL_BRIDGES` into `ALL_CORE_BRIDGES` (9, unchanged collapse case) and `ALL_BRIDGES_WITH_MB10` (10, for a hypothetical future all-ten theorem); `check_axiom_budget.py` passes clean (15 theorems, no drift) and regenerated `metadata/axiom-budget-index.tex`.
- Diagrams: added the previously-missing `MB9` node to `context/lean_proof_graphs/01-boundary-measurement.dot` (closes a separate stale TODO item) and `00-overview.dot`'s Spine I label; added `MB10` + a `[NEW]` `forgeability_gap` node to `03-correction-successors.dot` and `00-overview.dot`'s Spine III label; synced the master `context/lean_proof_dependency_graph.dot`. Regenerated all PNGs via `scripts/render_lean_graphs.sh` and visually inspected the three changed ones.
- Docs synced: `formal/AlignmentProofSpine.lean` + `formal/README.md` module tables and bridge-count prose; new appendix subsection `appendices/appG-lean-proof-spine.tex` §`appi:sec:forgeability` (theorem, corollary, new `Assumption~appi:ass:mb10`, summary-table row) plus figure-caption updates for the three changed diagrams; `appendices/appB-bridge-crosswalk.tex` (new MB10 row + notes paragraph, crosswalked to the same deceptive-alignment/tiling crux family as `MB7a--c`/`MB5`); `appendices/appF-research-program.tex` (new MB10 validate/falsify paragraph, tier footnote); `metadata/assumptions-ledger.md` (§IV entry, quick-index, appendix-E-generating table — regenerated `metadata/assumptions-index.tex`, 28→29 entries); `metadata/uncertainty-ledger.md` (U-04 extended); `metadata/TODO.md` (BIG REVIEW item marked `[~]` with item-1 resolution, separate stale MB9-diagram item closed `[x]`); `\leanspine` glosses added to ch08, ch31, ch43, ch48.
- Deliberately **not** done: formal unification of `ConservedPropertySignatureVerifiable` with `Chokepoint`'s `MeasurementChannel`; a `Defeaters.lean`-style named signal/toy model for `MB10` itself; a chain-level (multi-step `SuccessorSafeChain`) version of `MB10` (current bridge is single-step, matching `MB5`'s own shape) — all recorded as open items.

### 10. Single worked instance on real data (`WorkedInstance.lean`, new module)

User follow-up: "Implement the single worked instance: take a trace from `experiments/embedded-simulation/`, compute an actual `CCICertificate`, an actual tight appearance ceiling, and an actual δ through `NumericRiskLeaf` — inside Lean, on real (toy) data." The remaining item from §5's standing list not yet executed.

- Explored `experiments/embedded-simulation/` for a genuinely committed, small, hand-encodable trace. `synthesize_rows`'s structural profiles (`embedded_sim/structural_fixtures.py`) are sparse pulse patterns (real audit probes are rare by design), so rather than run Python and copy numbers, used the literal first 16 rows of the already-committed fixture `experiments/embedded-simulation/tests/fixtures/sample_capture_theater.jsonl` directly — a real, checked-in artifact, not synthesized for this exercise.
- New file `formal/AlignmentProofSpine/WorkedInstance.lean`:
  - `workedTrace : DiscreteTrace 4 2 16` — four native fixture fields (`visible_action`→active, `intervention_active`→external, `judge_captured`→internal, `correction_request`→sensory) as the literal binary rows of steps 0–15, via Mathlib's `![...]` vector notation; `workedBlanket`/`workedParams` (`maxLag = 0`, matching the simulator's own `PROBE_LAG = 0`).
  - Three `decide`d concrete numbers on the real data: `traceControlDiversity = 1`, `traceActionCapacityBits = 1`, `traceDiversityTightOptimism 16 2 = 1` — the real trace **exactly saturates** the tight ceiling rather than merely falling under it. `workedProfileCert : TraceBIQProfileCertificate` closes by `decide` on the same data.
  - A concrete `CCICertificate` (`workedCert`, ten literal integer coordinates) passing concrete `CCIThresholds`/`CCIPenaltyWeights` (`workedCert_passes`, `decide`); the θ-derived floor (`CCIThresholds.lambdaFloor`) computes to `2`, also `decide`d.
  - `worked_instance_slack` combines the two concrete numbers (`traceActionCapacityBits = 1`, CCI floor `= 2`) via `omega` into the slack `NumericRiskLeaf` needs, at `δ = -1`.
  - `workedRiskLeaf` builds an **actual** `NumericRiskLeaf A (-1)` term via `traceDerivedCCISlack`/`NumericRiskLeaf.fromMarkovBlanketBIQ`; `worked_instance_risk_bound` concludes `Risk A ≤ -1` for any hypothesized system `A` satisfying the (necessarily still-explicit, since `System` is opaque) bridge hypotheses `hctrl`/`hcact`/`hmeas`.
- One tooling snag: `dsimp only [CCICertificatePasses, workedCert, workedThresholds]; decide` was required instead of `unfold ...; decide` — plain `unfold` exposes the opaque `hvalid`/`hground` proof terms syntactically before projection (iota) reduction eliminates them, and `decide` refuses any goal that still mentions a free variable even when it doesn't affect decidability; `dsimp` performs the projection reduction first so they drop out before `decide` runs.
- `#print axioms worked_instance_risk_bound`: only carrier/predicate vocabulary axioms (`System`, `CactSys`, `CCIPenaltiesSys`, `GroundingViable`, etc.) plus `propext`/`Classical.choice`/`Quot.sound` — **no `MB*`, no `sorryAx`** — confirming the instance chips at estimability (does real numbers flow through the real theorems) without smuggling in a bridge proof.
- Axiom-ledger: new entry `AlignmentProofSpine.worked_instance_risk_bound` in `formal/axiom-ledger.json`; `check_axiom_budget.py --update` regenerated `metadata/axiom-budget-index.tex` (16 headline theorems now).
- Docs synced: `formal/AlignmentProofSpine.lean` (import + module-map row) and `formal/README.md` (module-map row, axiom-budget-tooling theorem count 13→16); `appendices/appG-lean-proof-spine.tex` new "Worked instance on real data" paragraph in §`appi:sec:trace-attended-harm`, citing the concrete numbers and `\leanid{worked_instance_slack}`/`\leanid{worked_instance_risk_bound}`; `metadata/TODO.md` updates to the `Field/Finite/TraceBIQ.lean` item (line ~143) and the "Full worked example" item (line ~53), both noting this covers the capability-vs-correction-slack numeric leaf only (not boundary residual, value-bundle signal, or the adversarial capture/faking case, which stay with the Python `experiments/toy-simulation/` pipeline).
- Deliberately **not** done: calibrating the pattern-diversity score against `audit_core/info.py`'s Shannon CMI (separate, still-open TODO item); a `CertifiedSafetyCase`-level instance (this stays at the `NumericRiskLeaf`/`Risk` layer, not the full `LayeredAlignedDef` + `Certified` + invariants stack); using a richer/less-sparse trace window (the fixture's real audit signal is genuinely sparse — one probe in 16 steps — which is itself an honest reflection of ch26's rare-audit-event concern, not a limitation introduced here).

### 11. §10 correction: the worked instance's `δ = -1` was manufactured, not measured

User caught it immediately: "Wait, δ = -1 is cheating." Investigating confirmed **two** real bugs in §10's first version, not one:

- **Reverse-engineered certificate/thresholds.** `workedThresholds`'s `minRawCapacity = 3`/`maxLatency = 1` were, per that version's own docstring, "chosen so the θ-derived floor lands exactly on 2, one bit above the trace-computed action capacity" — solved backward from the target `δ = -1`, not measured. Every penalty coordinate (`manipulation`, `irreversibility`, `ontologyTranslation`, `coercion`, `dependency`) was set to `0` by fiat, on a fixture literally named `sample_capture_theater.jsonl` whose whole point is a compromised correction judge — asserting zero manipulation on a captured-judge trace is the "capture theater" pattern itself (manufacturing an appearance of safety), not a measurement of it.
- **A second, independent bug found while investigating the first:** the 16 literal rows were mistranscribed. The real committed row 0 has `visible_action = 0` (not `1` as coded), and across the real steps 0–15 `visible_action` is constant `0` throughout — so the module's central claim ("the real trace exactly saturates the tight ceiling") was checked against fabricated numbers, not the real fixture. (Root cause: the four-column table in the previous session's memory carried a stale/misremembered row rather than a fresh re-read of the committed file.)

**Fix — `formal/AlignmentProofSpine/WorkedInstance.lean` rewritten in full:**

- Re-pinned to the literal fixture at git commit `408444b` (`git show 408444b:experiments/embedded-simulation/tests/fixtures/sample_capture_theater.jsonl`), re-transcribed by direct extraction rather than by hand, to avoid a repeat of the same class of error.
- Widened the window from 16 to 26 rows (steps 0–25) under a **pre-registered rule stated before computing anything**: the smallest prefix in which each of the three time-varying mapped columns (`visible_action`, `intervention_active`, `correction_request`) takes both its values at least once. (`judge_captured` is excluded from that rule because it is `1` for all 300 rows of the fixture, not just a windowing artifact — confirmed by checking the full file, not just the prefix.)
- On the real, correctly-transcribed window: `traceControlDiversity = 0` (not saturating the tight ceiling — an honest, unforced result: the visible-action pulse at step 25 and the intervention pulses at steps 0/22 never coincide at lag 0), `traceActionCapacityBits = 1`, `traceDiversityTightOptimism 26 2 = 1`, all `decide`d.
- The one `CCICertificate` coordinate the trace can actually speak to, `manipulation` (ch26's captured-judge penalty), is now **computed** — `workedManipulationCount`, a `Finset.filter`/`.card` count of steps where the internal (`judge_captured`) column reads `1` — rather than asserted; it evaluates to `26` (every row in the window). `CCIThresholds` are fixed independently of that count (`maxManipulation = 1`, small round numbers on every other coordinate) rather than solved backward. Every other `CCICertificate` coordinate (`rawCapacity`, `latency`, `plurality`, `exitCapacity`, `independence`, and the remaining penalty terms) is disclosed as an illustrative placeholder — a four-column per-step binary trace cannot literally encode architecture-level facts like handle redundancy — chosen comfortably clear of its own threshold so the single real coordinate is what decides the outcome.
- **The honest result: the certificate fails.** `workedCert_fails : ¬ CCICertificatePasses (workedCert hvalid hground) workedThresholds`, proved by the same `dsimp only [...]; decide` pattern as before. `26 > 1` is the sole, decisive, real failure; every other coordinate passes comfortably. Consequently `CCI_ge_threshold_floor`/`NumericRiskLeaf`/`Risk A ≤ δ` cannot be invoked through this certificate for this trace — documented as prose (not a further theorem; the negative fact already says everything) rather than manufacturing a substitute conclusion.
- Dropped the earlier `worked_instance_slack`/`workedRiskLeaf`/`worked_instance_risk_bound` chain entirely — there is no honest way to produce a `NumericRiskLeaf` from a certificate that correctly fails, and inventing looser thresholds specifically to make it pass again would just be the same bug relocated. Recorded as an explicit open item: a genuine *passing*-certificate instance needs a second real trace whose `judge_captured` is not identically `1` for its whole duration; the only fixture currently committed under `experiments/embedded-simulation/` has `judge_captured = 1` on all 300 of its rows (checked directly), so no such window exists there today.
- `#print axioms workedCert_fails`: carrier/predicate vocabulary axioms plus `propext`/`Classical.choice`/`Quot.sound` only — same clean footprint shape as before, now attached to a claim that is actually true of the real data.
- One incidental tooling bug fixed along the way: `formal/scripts/check_axiom_budget.py`'s `latex_escape` didn't escape `_`, so the new ledger gloss (which needed to say `judge_captured`) broke the LaTeX build with "Missing $ inserted" — fixed by adding `_` → `\_` to the escape table (a generically-useful fix, not specific to this entry).
- Docs re-synced to the corrected story: `formal/axiom-ledger.json` (`worked_instance_risk_bound` entry replaced by `workedCert_fails`, still 16 headline theorems, `check_axiom_budget.py` clean/no-drift), `formal/AlignmentProofSpine.lean` + `formal/README.md` module-map rows, `appendices/appG-lean-proof-spine.tex` "Worked instance on real data" paragraph rewritten end-to-end, `metadata/TODO.md`'s two entries (the "Full worked example" item and the `TraceBIQ.lean` item) both corrected with a same-day "Correction" note rather than silently overwritten, so the historical record shows the mistake and the fix rather than erasing it.
- Full `lake build` (1725 jobs) and `./build.sh`/`make check` re-run clean after the fix. (The rebuild also required the documented stale-biber-cache workaround — `mkdir -p .biber-par-cache && PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" ./build.sh` — unrelated to this session's edits; `book.bcf-SAVE-ERROR`/`book.bbl-SAVE-ERROR` were already present as untracked files at session start.)

**Lesson for future sessions using this pattern:** when a "worked instance" is supposed to demonstrate a gate/certificate against real data, fix the gate's parameters *before* computing what the real data does, and treat a correctly-failing gate as a valid (often more informative) outcome rather than something to route around.

### 12. Shannon-CMI calibration of the trace diversity score (item (4) of the TraceBIQ row) — negative result N-8

User: "Implement the Shannon-CMI calibration" — the top-leverage open item identified in the post-§11 assessment.

- New `experiments/embedded-simulation/calibrate_trace_biq.py`: a faithful Python port of `TraceBIQ.lean`'s score pipeline (`log2CeilBits`, `laggedPairs`, `laggedPatternDiversity`, spurious/tight ceilings, `laggedDiversityScore`, `traceControlDiversity`, `columnSupportBits`) compared against `embedded_sim/audit_core/info.py`'s plug-in Shannon MI/CMI on the same data.
- **Protocol pre-registered in the script docstring before computing** (the §11 lesson applied): fixed pairs (both Lean measurand directions + two disclosed diagnostics), all lags 0–25, both the 26-row worked-instance window and the full 300 rows, small-sample rows (<10 pairs, `info.py`'s own threshold) excluded from findings.
- **Port gated on the Lean cross-check:** the script hard-fails unless it reproduces the four Lean-`decide`d numbers from `WorkedInstance.lean` (control diversity 0, action capacity 1, tight ceiling 1, manipulation count 26) — guards against a repeat of §11's transcription-bug class. Data pinned at git `408444b` via committed `tests/fixtures/trace_biq_calibration_columns.json` (necessary because the working-tree fixture has since changed schema and no longer has `judge_captured` at all); the script re-verifies the committed columns against `git show` when git is available.
- **Findings (recorded as N-8 in `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`; full tables `results/trace_biq_calibration.{md,json}`):**
  - *Score uncalibrated in both directions.* Under-detection: the fixture's one genuine coupling (intervention pulse → visible action 3 steps later, ≈0.17–0.24 bits MI) scores **0** — the single step-0 boundary pulse inflates the joint support and collapses the support-difference formula. Over-statement: sparse byte-identical columns (`correction_request` = `intervention_active`, an exact invariant of the pinned fixture) score a full **1 bit** vs ≈0.27–0.39 bits plug-in MI.
  - *Ceiling sound.* The tight appearance ceiling `⌈log₂ min(m,|𝒜|)⌉` dominated Shannon MI on every pair/lag tested (0 violations), matching the provable direction (MI ≤ min marginal entropy ≤ log₂ support).
  - *Direction blindness is protocol-level:* at the worked instance's own protocol (`maxLag = 0`, active→external) both estimators correctly read ≈0; the real structure lives at lag 3 in the reverse direction — neither estimator is wrong there, the *probe protocol* is blind to it.
- 7 contract tests in `tests/contract/test_trace_biq_calibration.py` pin the fixture invariants, the Lean cross-check, MI ≤ ceiling, one canonical under-detection case, one canonical over-statement case, and results-JSON ↔ code sync. All pass (throwaway `/tmp` pytest venv; repo convention, not a new dependency).
- Docs synced: `metadata/TODO.md` TraceBIQ item (4) marked done-with-negative-finding; appG worked-instance paragraph gains the "appearance ceilings, not measured bits" caveat sentence citing N-8; `TraceBIQ.lean` module docstring points to the calibration; NEGATIVE_RESULTS.md reproduction block extended. `lake build` + `./build.sh` + `make check` all pass after.
- **Consequence for the manuscript:** trace-derived diversity/control numbers may be cited as appearance ceilings (upper bounds) only, never as measured bits — the quantitative version of the caveat `TraceBIQ.lean` always carried in prose.

### 13. Honest companion worked instance — the gate passes real honest data (`honest_instance_risk_bound`)

User: "Implement the second varied real trace" — closes the §11 open item that a rejection-only gate demonstration is unfalsifiable in the flattering direction.

- **Provenance solved by symmetry, not new data collection:** the capture-theater fixture was created by `synthesize_rows(300, "capture_theater", seed=5)` (visible in `git show 408444b:...tests/contract/test_trace_ingest.py`). The companion `tests/fixtures/sample_honest_baseline.jsonl` is `synthesize_rows(300, "honest_baseline", seed=5)` from the **identical pinned-commit generator** — same code, same seed, same commit, different structural profile. Generated from `git show 408444b:...structural_fixtures.py` executed in isolation (the working-tree generator has since been schema-changed by another session and no longer emits `judge_captured`). New contract test `tests/contract/test_worked_instance_fixtures.py` (5 tests) pins: fixture shape/invariants, byte-for-byte regeneration from the pinned generator, both 26-row Lean window transcriptions, and the discriminating manipulation counts (0 vs 26).
- **Lean (`WorkedInstance.lean` §5):** same blanket, params, column mapping, and — decisively — the **same `workedThresholds`/`workedWeights`, which §3 fixed before this fixture existed** (the strongest pre-registration available). `honestRows`/`honestTrace` (26 rows; `judge_captured` all-0, `visible_action` all-0, single step-0 probe pulse), `decide`d numbers: control diversity 0, action capacity **0 bits** (honest deployments are quiet on this profile), manipulation count **0**. `honestCert` has the identical placeholder coordinates as §3 and the computed manipulation `0` → `honestCert_passes` (`decide`). θ-floor `= 1 − (2+1+2+2) = −6` → `honest_instance_slack` → actual `NumericRiskLeaf A 6` (`honestRiskLeaf`) → **`Risk A ≤ 6`** (`honest_instance_risk_bound`), via the standard `traceDerivedCCISlack` path under the same explicit bridge hypotheses.
- **Two honesty choices, disclosed in module + appG:** (i) `δ = 6` is *weak* — the pre-registered thresholds are loose and the θ-floor inherits that; reported at face value. (ii) The sharper certificate-projection floor (`3 − 1 = 2`, would give `Risk A ≤ −2`) is deliberately **not** used because it rests on placeholder coordinates `rawCapacity = 3`/`latency = 1` — exactly the superseded §10 mistake. The headline δ depends only on pre-registered thresholds + measured capacity.
- **Window choice disclosed:** same 26-row length as §1 for like-for-like comparison; §1's minimal-prefix rule would give a 2-row window here with the same qualitative outcome (all measured quantities are constant-0-robust to the window).
- **Punchline (in module docstring, README module map, appG):** identical thresholds, identical procedure, opposite verdicts, and the *only* differing real coordinate is the computed captured-judge count (26 vs 0) — the gate discriminates on real data rather than merely rejecting.
- Ledger: `honest_instance_risk_bound` added to `axiom-ledger.json` (17 headline theorems now; footprint = the standard measurand axioms + `Classical.choice`/`Quot.sound`/`propext`, no `MB*`, no `sorryAx`). `check_axiom_budget.py` passes, no drift. Numbers scratch-verified via a throwaway `#eval` file *before* writing the module (§11 lesson). `lake build` (1725 jobs), 12 contract tests, `./build.sh`, `make check` all pass.

## Open / next

- Probabilistic concentration lemma to instantiate `TraceAttendedOutputConcentrationBridge` (still the main open trace item).
- Named extinction-bound leaf in `Certification.lean` (attended-harm certs not yet wired into `NumericRiskLeaf`).
- ch13 κ_ij edge/percolation structure beyond `P32`.
- Reviewer-feedback transcript scan ran as subagent; highest-priority flagged item (successor audit-link axioms) addressed this session (§4). Remaining flagged items for later: `SystemUpdateCertificate` / `ValueUpdateCertificate` vectorization, probabilistic `MB1` (drop ε=1 hardcode), `CooperationGraph.componentLarge`/`P33` strengthening, finite models for `Adversarial.lean` `P31`/`P37`, typed per-agenda certificates replacing `all_crosswalk_subsumptions_proved`.
- From §5's standing suggestion list: all four items executed (§7 defeater-pairing, §8 axiom-budget guard, §9 `MB10`/forgeability naming, §10/§11 the worked instance — corrected in §11 to an honest failing-certificate result rather than a manufactured passing one).
- Worked instance (§10/§11): ~~a genuine *passing*-certificate companion instance needs a second real committed trace whose `judge_captured` (or equivalent) column is not identically `1`~~ — done §13 (`honest_instance_risk_bound` on `sample_honest_baseline.jsonl`, same pinned generator/seed/commit); still open: extend to a `CertifiedSafetyCase`-level instance once a `LayeredAlignedDef` worked example exists. ~~Calibrate the pattern-diversity score against `audit_core/info.py`'s Shannon CMI~~ — done §12, negative result N-8 (score uncalibrated both directions; ceiling sound).
- Calibration follow-ups (§12): if a calibrated trace estimator is ever needed, wire `Field/Finite/PMF.lean`'s MI machinery to trace columns instead of patching the support-count score; consider a probe protocol that scans lags/directions (the fixture's real coupling is at lag 3 in the direction `PROBE_LAG = 0` cannot see).
- BIG REVIEW chokepoint item (§6): WWCTV cross-chapter forward references (ch07/ch46/ch46/ch48) to `appi:sec:chokepoint`; uncertainty-ledger reconciliation (U-03/U-05/U-14/U-16); the empirical shared-vs-independent-instrument question itself.
- Defeater ledger (§7): toy models for `MB2`, `MB3`, `MB5`, `MB6a`, `MB7a`, `MB9`; whether any named signal (e.g. `LockedInBadBasin`, `JudgeManipulated`) is actually observed in a real deployment is an open empirical question this session deliberately leaves unresolved.
- Axiom-budget guard (§8): the headline-theorem list (13 at §8, 17 after §13) is curated by hand, not auto-discovered — adding a new headline theorem to the spine requires manually adding it to `formal/axiom-ledger.json`; not wired into `make check` or any CI workflow yet.
- Forgeability / `MB10` (§9): unify `ConservedPropertySignatureVerifiable` with `Chokepoint.MeasurementChannel` formally; give `MB10` a `Defeaters.lean` entry (named signal + toy model, e.g. an `AuditChannelCaptured`-style predicate); non-enumerability (item 2 of the same BIG REVIEW) remains entirely unformalized; a chain-level `MB10` matching `SuccessorSafeChain` rather than single-step `SuccessorSafe`.

## Key paths

- `formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean`
- `formal/AlignmentProofSpine/Correction.lean`
- `formal/AlignmentProofSpine/Capability.lean`
- `formal/AlignmentProofSpine/Successors.lean`, `formal/AlignmentProofSpine/Certification.lean`
- `formal/AlignmentProofSpine/Chokepoint.lean` (new)
- `formal/AlignmentProofSpine/Defeaters.lean` (new)
- `formal/AlignmentProofSpine/Forgeability.lean` (new)
- `formal/AlignmentProofSpine/WorkedInstance.lean` (new)
- `experiments/embedded-simulation/tests/fixtures/sample_capture_theater.jsonl` (real trace source, read-only, pinned at `408444b`)
- `experiments/embedded-simulation/calibrate_trace_biq.py`, `tests/contract/test_trace_biq_calibration.py`, `tests/fixtures/trace_biq_calibration_columns.json`, `results/trace_biq_calibration.{md,json}` (new, §12)
- `experiments/embedded-simulation/tests/fixtures/sample_honest_baseline.jsonl`, `tests/contract/test_worked_instance_fixtures.py` (new, §13)
- `formal/scripts/check_axiom_budget.py`, `formal/axiom-ledger.json` (new)
- `metadata/axiom-budget-index.tex` (new, auto-generated)
- `context/lean_proof_dependency_graph.dot`, `context/lean_proof_graphs/00-overview.dot`, `01-boundary-measurement.dot`, `03-correction-successors.dot`
- `appendices/appG-lean-proof-spine.tex`, `appendices/appF-research-program.tex`, `appendices/appB-bridge-crosswalk.tex`
- `chapters/ch08-grow-split-merge.tex`, `chapters/ch11-capability-without-task-ontology.tex`, `chapters/ch26-correction-channel-integrity.tex`, `chapters/ch31-conserved-properties.tex`, `chapters/ch43-verifiability-and-ontology-adequacy.tex`, `chapters/ch48-towards-alignment.tex`
- `metadata/TODO.md`, `formal/README.md`, `metadata/assumptions-ledger.md`, `metadata/uncertainty-ledger.md`, `metadata/assumptions-index.tex`
- `review/adversarial-steerability-correlated-failure-2026-06-30.md`

## Commits

- (none — user did not request a commit)
