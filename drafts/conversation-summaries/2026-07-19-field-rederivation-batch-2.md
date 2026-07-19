# 2026-07-19 — Field rederivation batch 2: ELK, Debate, off-switch, quantilizer maximin, amplification, Thornley dynamic choice

**Trigger.** Follow-on from the hostile-critique session (same day, `2026-07-19-lean-spine-hostile-critique-fixes.md`). After an assessment of the remaining subsumption/projection claims, the user instructed: "Make progress on as suggested. Don't do Christiano's. Do Thornley and we keep Turner's for a later session."

## What was done

Six new finite Lean modules, each replacing an opaque handle or a capacity-identification shortcut with field-native machinery:

1. **`formal/AlignmentProofSpine/Field/Finite/ELKIdentifiability.lean`** — reporter non-identifiability: direct translator vs. human simulator agree pointwise on-distribution, both match human labels, and *no* behavioral criterion (`List Bool → α`, arbitrary result type) over an on-distribution training set separates them (`no_training_criterion_separates`, proved for arbitrary agreeing reporter pairs); they diverge on the tampered scenario (`reporters_diverge_on_tampering`); packaged as `elk_reporter_unidentifiable_from_training`. **Explicitly refutes the earlier κ_C-projection framing** — the docstring and appG now say the difficulty is identifiability, not bandwidth, and relate it to `MB2` as a shared crux.
2. **`.../DebateGame.lean`** — native two-prover game on claim trees (conj/disj over atoms): `debateValue = Claim.eval` with correct judge; constructive honest strategies; `defender_wins_iff_true` / `challenger_wins_iff_false`; one-judge-error flip both directions (`erring_judge_flips_debate`, `erring_judge_rejects_true_claim`). Discharges the "native debate-game matching deferred" note.
3. **`.../OffSwitchGame.lean`** — Hadfield-Menell/Dragan/Abbeel/Russell off-switch theorem in integer-mass form: `defer_strictly_best_under_uncertainty` (both-signs mass ⇒ defer strictly beats act and off); `rational_policy_maximizes_defer` (incentive = human informativeness); `costly_defer_dominated_when_human_uninformative` (Milli–Dragan degradation direction).
4. **`.../QuantilizerMaximin.lean`** — Taylor's characterization both directions: `bounded_ratio_gives_worst_case_bound` (sufficiency) and `unbounded_ratio_admits_adversarial_cost` (necessity via indicator cost); quantilizer instance `quantilizer_cost_le_base` (normalizes to the 1/q bound).
5. **`.../AmplificationTree.lean`** — HCH decomposition trees: `amplification_sound` (leaf-correct ⇒ root-correct, structural induction); `local_steps_always_valid` (local validity free for any supervisor — process checks certify nothing); `single_leaf_error_flips_root` / `local_supervision_without_leaf_truth_unsound`. Supersedes the `Bool` toy `ToyLocalRecursiveSupervision` in `Correction.lean` (kept, docstring marks it legacy).
6. **`.../DynamicChoice.lean`** — Thornley dynamic-choice layer: TD is a strict partial order; `exists_td_maximal` (maximal element of nonempty lists); decision trees + plans + `reachable_realizable`; **`td_resolute_policy_avoids_domination`** (resolute TD choice never ends dominated — the escape from the money pump) and **`naive_stepwise_td_can_be_pumped`** (the Gustafsson-style objection exhibited exactly: X→Y→Z each step TD-permissible both ways, Z strictly dominated by X).

Wiring:

- New agenda module `Field/Amplification.lean` + `FieldAgendaTag.Amplification` + imported meta/handle `Christiano2018_amplification_imported` (key `christiano2018amplifying`).
- ELK/Debate agenda modules rewritten: rederived cores re-exported (`elk_*`, `debate_*` aliases), κ_C-projection theorems kept but relabeled "interface toy (assumption-labeled)" in docstrings, records, and appG. CIRL/Quantilization/Shutdown modules extended with `cirl_offswitch_*`, `quantilizer_maximin_*`/`quantilizer_taylor_cost_bound`, `thornley_money_pump_objection`/`thornley_resolute_choice_unexploitable` aliases + records.
- **`FieldSubsumptions.lean`**: the decorative `subsumptionProvedFor : FieldAgendaTag → Prop := fun _ => True` + `all_crosswalk_subsumptions_proved` (∀ tag, True) was replaced by `hasRederivedCore` / `every_agenda_has_rederived_core` — a `decide`-checked statement that every agenda tag has ≥1 `rederivedFinite` record. (Nothing outside generated graphs referenced the old names.)
- `axiom-ledger.json`: 27 → **37 headline theorems** (new: ELK nonidentifiability, debate iff + judge flip, off-switch pair, maximin pair, amplification leaf error, money pump + resolute escape). All new entries have empty or vocabulary-only (`propext`/`Classical.choice`/`Quot.sound`) footprints — none consume MB* bridges or spine carriers. `check_axiom_budget.py --update` run; no drift.
- Bib: new `hadfieldmenell2017offswitch` (The Off-Switch Game, IJCAI 2017) in `references/external-alignment.bib` + `\bibsummary`.
- `appendices/appG-lean-proof-spine.tex`: new "Rederived in Lean" paragraphs for CIRL (off-switch game), quantilizers (maximin), debate (native game), ELK (nonidentifiability, with the correction of the projection framing); new Amplification subsubsection; status-ledger table rows updated (interface toys labeled as such); the trailing "Debate and ELK remain intentionally weaker" deferral paragraph replaced by a discharge note + the honest inventory statement.
- `formal/README.md` module map + headline count updated; `metadata/TODO.md` item "native Debate and ELK theorem matching" marked done; new batch entry added.

## Verification

- `lake build` clean (2250 jobs; only pre-existing warnings in `PMF.lean`/`TraceBIQ.lean`).
- `python3 scripts/check_axiom_budget.py` passes (37 theorems, no drift).
- `make check` passes (structure, citations 216 keys, bibliography summaries 414/414).

## Non-obvious decisions

- **ELK/Debate reframed from "projection" to "shared crux"/"conditional".** The rederivations do not support the old subsumption reading; the κ_C-identification theorems were kept but explicitly labeled interface toys everywhere (docstrings, records, appG). This is a deliberate weakening of the book-facing claim to what the Lean actually supports.
- **Off-switch game placed under CIRL** (same authors, same assistance-game frame) with its own bib key rather than a new agenda tag.
- **Quantilizer maximin stated cross-multiplied in `Int`** (`D * p.mass a ≤ N * w.mass a`), avoiding rationals; the 1/q reading is in docstrings.
- **DynamicChoice plans are choice *sequences*** (`List Bool`), not functions of the node — avoids needing decidable equality on trees containing functions, and matches the resolute-choice (plan-execution) semantics being formalized. Sophisticated choice is *not* formalized (noted in docstring and TODO).
- **`Correction.lean`'s Bool amplification toy kept** (surgical change): only its docstring now marks it superseded by `AmplificationTree`; the real content lives in the Field layer to keep core-module layering clean.
- User decisions recorded: Christiano's drift-management formalization skipped; Turner power-seeking deferred to a later session.

## Open / next steps

- Turner power-seeking (deferred by user; mechanical but bulky — needs reward-distribution/orbit machinery).
- Sophisticated-choice (backward-induction) variant of the Thornley dynamic layer.
- Probabilistic judge / debater-compute-limited debate model; ELK training-prior (simplicity) argument — both remain with the sources.
- Site Lean-graph nodes and `context/lean_proof_graphs/*.dot` for the new modules (carried over from previous session for MB4a/MB11/S10 too).
- appB/appF validate-falsify paragraphs for MB4a/MB11 (carried over).

## Key paths

- `formal/AlignmentProofSpine/Field/Finite/{ELKIdentifiability,DebateGame,OffSwitchGame,QuantilizerMaximin,AmplificationTree,DynamicChoice}.lean` (new)
- `formal/AlignmentProofSpine/Field/{ELK,Debate,CIRL,Quantilization,Shutdown,Amplification,Common,Imported}.lean`, `Field.lean`, `FieldSubsumptions.lean`, `Correction.lean`
- `formal/axiom-ledger.json`, `metadata/axiom-budget-index.tex` (generated)
- `appendices/appG-lean-proof-spine.tex`, `references/external-alignment.bib`, `references/bibliography-summaries.tex`
- `formal/README.md`, `metadata/TODO.md`

No commits made in this session (user has not asked yet).
