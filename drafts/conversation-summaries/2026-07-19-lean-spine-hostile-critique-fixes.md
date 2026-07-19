# 2026-07-19 — Lean spine: hostile-critique fixes + field rederivations

## Trigger

User shared a hostile critique of the Lean spine (unlabeled anti-capture axiom, unlabeled B-IQ axioms, record-packing "theorems", opaque imported handles) and asked: fix the obvious cases; derive Thornley's incomplete-preference machinery, Soares et al.'s incentive theorems, and Orseau–Armstrong's convergence results in Lean; replace record-packing hacks with a bridge axiom carving out open research; stop at the edge of the formalizable.

## Done

- **Anti-capture (`Correction.lean`).** `CorrectionPath` is now data-only (corrector, handles, capacities); all legitimacy conditions (controls/reaches/persists/**notCaptured** + agent/human-coincidence) moved to a new `Prop` structure `CorrectionPathLegitimate`, supplied only by the new labeled bridge **`MB4a_measured_path_legitimacy`** (`CorrectionIntegrity A → CorrectionPathLegitimate (SystemCorrectionPath A)`). Capture is now representable: new theorems `capture_invalidates_reference`, `capture_makes_cci_captured_or_invalid` (no bridge needed), `capture_defeats_correction_integrity`, `capture_blocks_valid_certificate`. The three formerly unlabeled `CorrectionIntegrity_implies_*` axioms became theorems from `MB4a`; the nonempty-links one is provable outright.
- **B-IQ arithmetic (`Capability.lean`).** Four unlabeled axioms consolidated into one labeled measurement convention **`S10_blanket_measurand_coherence`**; the four originals re-proven as theorems from it.
- **Record packing (`Certification.lean`).** Evidence structures (`CertifiedSafetyCase` etc.) demoted from `Type` to `Prop`; assembly theorems' docstrings now say "bookkeeping, not derivation". New axiom `WithinDeploymentRiskTolerance` plus new bridge **`MB11_safety_case_adequacy`** (`CertifiedSafetyCase A δ → WithinDeploymentRiskTolerance A δ → Safe A`), consumed by `P30_safe_of_case` — the safety-case→Safe gap is a named axiom, not an implied conclusion.
- **Thornley IPP (`Field/Finite/IncompletePreferences.lean`, new).** POST preferences as a provably incomplete preorder (`POSTPref_not_total`), incomparability ≠ indifference (sweetening-insensitivity), Timestep Dominance; proved `td_never_pays_to_shift_shutdown_time` and `pure_timing_shift_neither_dominates`, contrasted with EU-maximizer manipulation incentives.
- **Soares et al. (`Field/Finite/ShutdownIncentives.lean`, new).** Two-branch button model; incentive identity `button_eu_gap`; `prevention_incentive` / `seeking_incentive` / `button_incentive_iff_payoff_gap`; utility indifference works locally (`indifference_removes_button_incentive`) but is a knife-edge (`indifference_is_knife_edge`) and buys no corrigibility (`indifferent_agent_wont_pay_to_preserve_button`, `indifferent_agent_weakly_prefers_disabling_button`).
- **Orseau–Armstrong (`Field/Finite/BellmanQ.lean`, new).** Finite-horizon deterministic MDP; `bellmanQ`, `BellmanConsistent` uniqueness, value-iteration optimality, the off-policy point `bellman_target_schedule_invariant`; the stochastic-approximation step is the **statement-bearing** axiom `OA2016_offpolicy_qlearning_convergence` (replacing the opaque `True`-typed handle); derived `oa_learned_q_interruption_invariant` and `oa_interrupted_learner_greedy_optimal`.
- **Wiring.** `Field/Shutdown.lean` and `Field/Interruptibility.lean` re-export the new results via `alias` and record them in the `FieldResultRecord` tables; `Field/Imported.lean` docstrings mark the old opaque handles as legacy/superseded; `ThornleyShutdownability` docstring clarifies it is the one-bit interface, not the IPP.
- **Docs/ledgers.** `formal/README.md` (bridges, module map, 17→27 headline theorems), `formal/AlignmentProofSpine.lean` docstring, `formal/axiom-ledger.json` (+10 headline theorems), `check_axiom_budget.py` TEX_HEADER, `appendices/appG-lean-proof-spine.tex` (MB4a/MB11/S10 assumption blocks, bridge table rows, "Rederived in Lean" paragraphs for both agendas), `chapters/ch26-correction-channel-integrity.tex` leanspine gloss, `metadata/assumptions-ledger.md` (§III S01–S10, §IV MB4a/MB11 narrative + bridge table + appendix-index rows for S10/MB4a/MB11; regenerated `metadata/assumptions-index.tex`). (`hostile-review.md` was *not* touched by this session; its working-tree changes are from the same-day honest-meta-language/subsumption session.)

## Verification

- `lake build`: success (2243 jobs; only pre-existing `TraceBIQ` unused-variable warning).
- `formal/scripts/check_axiom_budget.py`: passed, 27 theorems, no drift; regenerated `metadata/axiom-budget-index.tex`.
- `make check`: structure, citation (215 keys), and bibliography-summary (413) checks all pass; chapter labels for new index rows (`ch:capability-without-task-ontology`, `ch:correction-channel-integrity`, `ch:safety-case`) verified.

## Decisions

- `MB4a` is threaded explicitly (like `MB10`, `MB11`) rather than packaged in `Core.BridgeAssumptions`, because its statement needs `Correction.lean` definitions.
- `MB11` maps to claim **C-001** in the crosswalk table (deployment-level safety), not an A-ID.
- Field rederivations live under `Field/Finite/` as finite integer models — honest about scope: no dynamic-choice/sequential-planning arguments for Thornley, no stochastic learning theory for OA (that is exactly what `OA2016_offpolicy_qlearning_convergence` carves out).
- Assembly/record structures stay (the manuscript cites them) but are labeled as packaging; the substance is in what consumes them (`MB11`).

## Open / next

- Thornley dynamic-choice layer (sequential IPP arguments, resolute choice) not formalized — prose-only.
- OA stochastic-approximation convergence remains an axiom by design; a finite-state probabilistic model could shrink it further but needs measure-theoretic machinery beyond the spine's integer idiom.
- `appB-bridge-crosswalk.tex` and `appF-research-program.tex` do not yet have dedicated MB4a/MB11 validate/falsify paragraphs (appG has the assumption blocks; crosswalk table in appG updated). Consider a follow-up pass mirroring the MB10 treatment (see TODO entry for MB10, 2026-07-02).
- Lean dependency graphs (`context/lean_proof_graphs/*.dot`) do not yet show MB4a/MB11/S10 nodes.

## Key paths

- `formal/AlignmentProofSpine/Correction.lean`, `Certification.lean`, `Capability.lean`
- `formal/AlignmentProofSpine/Field/Finite/{IncompletePreferences,ShutdownIncentives,BellmanQ}.lean`
- `formal/AlignmentProofSpine/Field/{Shutdown,Interruptibility,Imported}.lean`
- `appendices/appG-lean-proof-spine.tex`, `metadata/assumptions-ledger.md`, `formal/axiom-ledger.json`, `formal/README.md`

## Commits

- None (working tree only; user did not request a commit).
