# 2026-07-02 — Lean spine: more precise bounds (trace ceiling, CCI θ-floor, ch13 weighted bottleneck)

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

## Open / next

- Probabilistic concentration lemma to instantiate `TraceAttendedOutputConcentrationBridge` (still the main open trace item).
- Named extinction-bound leaf in `Certification.lean` (attended-harm certs not yet wired into `NumericRiskLeaf`).
- ch13 κ_ij edge/percolation structure beyond `P32`.
- Reviewer-feedback transcript scan ran as subagent; highest-priority flagged item (successor audit-link axioms) addressed this session (§4). Remaining flagged items for later: `SystemUpdateCertificate` / `ValueUpdateCertificate` vectorization, probabilistic `MB1` (drop ε=1 hardcode), `CooperationGraph.componentLarge`/`P33` strengthening, finite models for `Adversarial.lean` `P31`/`P37`, typed per-agenda certificates replacing `all_crosswalk_subsumptions_proved`.
- From §5's standing suggestion list (§7 executed defeater-pairing, §8 executed the axiom-budget guard; still not executed): an executable end-to-end instance computing a real `CCICertificate`/ceiling/δ from an `experiments/` trace; naming the "measurands vs what matters" gap as an explicit bridge.
- BIG REVIEW chokepoint item (§6): WWCTV cross-chapter forward references (ch07/ch46/ch46/ch48) to `appi:sec:chokepoint`; uncertainty-ledger reconciliation (U-03/U-05/U-14/U-16); the empirical shared-vs-independent-instrument question itself.
- Defeater ledger (§7): toy models for `MB2`, `MB3`, `MB5`, `MB6a`, `MB7a`, `MB9`; whether any named signal (e.g. `LockedInBadBasin`, `JudgeManipulated`) is actually observed in a real deployment is an open empirical question this session deliberately leaves unresolved.
- Axiom-budget guard (§8): the 13-theorem list is curated by hand, not auto-discovered — adding a new headline theorem to the spine requires manually adding it to `formal/axiom-ledger.json`; not wired into `make check` or any CI workflow yet.

## Key paths

- `formal/AlignmentProofSpine/Field/Finite/TraceBIQ.lean`
- `formal/AlignmentProofSpine/Correction.lean`
- `formal/AlignmentProofSpine/Capability.lean`
- `formal/AlignmentProofSpine/Successors.lean`, `formal/AlignmentProofSpine/Certification.lean`
- `formal/AlignmentProofSpine/Chokepoint.lean` (new)
- `formal/AlignmentProofSpine/Defeaters.lean` (new)
- `formal/scripts/check_axiom_budget.py`, `formal/axiom-ledger.json` (new)
- `metadata/axiom-budget-index.tex` (new, auto-generated)
- `appendices/appG-lean-proof-spine.tex`, `appendices/appF-research-program.tex`, `appendices/appB-bridge-crosswalk.tex`
- `chapters/ch11-capability-without-task-ontology.tex`, `chapters/ch26-correction-channel-integrity.tex`, `chapters/ch43-verifiability-and-ontology-adequacy.tex`
- `metadata/TODO.md`, `formal/README.md`, `metadata/assumptions-ledger.md`, `metadata/uncertainty-ledger.md`
- `review/adversarial-steerability-correlated-failure-2026-06-30.md`

## Commits

- (none — user did not request a commit)
