# 2026-10-23 — Lens review fixes (Lean frames + lens cards)

kind: correction
uptake: gate

## Trigger
User asked for a review of the lens formulation (cards and Lean), then: "apply the fixes and add the missing parts that are clear. report back with what is still open."
Prompts: paraphrase-only

## Done
- content: `FrameRelations.lean` — module table rewritten to say what is registry vs proof; `roleCompose_trivial` (the role gate admits every pair) and `roleCompose_necessary_slot` now follows from it; superseded triangle lemma removed (closed-walk lemma covers it); `native_decide` → `decide`.
- content: `FrameIncompatibility.lean` — `floorMenu`, `floorMenu_scalar_violates`, `no_finite_weights_pullback`; per-edge ∀-weight theorems `deontic_no_finite_weights`, `nonobs_no_finite_weights`, `cci_no_finite_weights`; `provedIncompat` now carries the `Incompatibility` instances (`ProvedIncompat`), `registry_matches_proofs` by `rfl`.
- content: `FrameMorphisms.lean` — map ids `restrict.fixedWeightOrder` (specialize) and `scalarize.chosenWeights` (project) replace the swapped names; 6 missing `mapSignatures`; `morphism_src_carriers`, `morphism_tgt_carriers`, `morphism_signatures_complete`; `decide`.
- content: `FrameComposePaths.lean` `decide`; `FrameLockIn.lean` docstring no longer calls a trajectory predicate robust invariance.
- content: `scripts/check_frame_graph.py` (DOT **a**/**b**/**c** vs Lean compose, red, and morphism registries), wired into `scripts/check.sh`.
- content: ai_power–human_power DOT label "when the option pool does not grow" (**a**/**b**/**c**); SVGs regenerated, **x** via `render_alignment_frames_x.py`.
- content: `drafts/alignment-frames-relations.md` Lean sections synced (registry vs proof, pullbacks, renamed maps, state–correction `A₂` unused).
- content: `lenses-data.mjs` — `(U)` rendering bug; 9 LessWrong links fixed (404s and label mismatches); hist/route/exact quotes now verbatim from the frames draft; weighted-scalar, criteria-vector, state-utility, proof card claims calibrated; Lean line anchors resolved from source at sync time; limit/strengthens edges no longer link to unrelated Lean; summand edges link `gradient_closed_walk_zero`. Overview and `FieldLensGraph` copy updated.
- content: Follow-up (user: "the site should follow the graph a"): removed lens cards `correction-certificate`, `coordinate-floor`, `scalar-risk-gap`, `deployment-preserve-tuple` (not on graph **a**) and the card sentences pointing at **b**-only edges (approval, proof, control, safety case, viability, criteria vector, weighted scalar); concept CCI `related` and redirects resynced. 25 lens cards + overview, all on the map.
- content: Second follow-up (user: criteria–CCI status, state–correction model, remove Hallgren quote, real-weights sentence, prove limit/strengthens):
  - `FrameIncompatibility`: `vectorCCIIncompat` is now its own instance (task-only Pareto vs CCI floor, `H` = every admissible option task-dominated; kind `paretoExcludesFloor`); `pareto_with_floor_coordinate_meets_floor` proves compatibility when the CCI coordinate is in the vector. Real-weight sentence on `no_finite_weights_represent_floor`.
  - New `FrameLimits.lean`: `robust_strengthens_viable`, `robust_trajectory_stays`, `viable_not_robust`; `quantilizer_limit_is_argmax`, `quantilizer_never_argmax_without_base_mass`; `forced_halt_converges`, `forced_halt_depends_on_time`; `limitEdges` registry, checked by `check_frame_graph.py`.
  - DOT **b**/**c** criteria_vector–cci_cert label "when every admissible option is task-dominated"; SVGs regenerated. Relations note, module tables updated.
  - Site: Hallgren quote replaced (relations-note sentence); quantilizer, robust, CEV, criteria-vector, weighted-scalar cards cite the new theorems; limit/strengthens edges link to `FrameLimits`; parallel edges (`cev→state`, `route→cycle`) keep separate links (`injectEdgeLinks` accepts per-title arrays).
  - Verification: `lake build AlignmentProofSpine` → "Build completed successfully (2270 jobs)."; new theorems' axioms ⊆ `[propext, Classical.choice, Quot.sound]`; `check_frame_graph.py` → "... 17 morphism, 3 limit/strengthens edges match Lean)."; `./scripts/check.sh` only markdown-link failures (untracked files, incl. this session's new ones until committed).
- bookkeeping: stale "variant b" line in `2026-10-23-lens-cards.md` corrected.
- bookkeeping: verification —
  - `lake build AlignmentProofSpine` → "Build completed successfully (2269 jobs)."
  - `./formal/check.sh --no-build` → "Axiom budget check passed (48 theorems, no drift)."
  - `#print axioms`: `variantC_all_derived`, `paths_partition_slots`, `morphism_*` "does not depend on any axioms"; pullback theorems and `registry_matches_proofs` → `[propext, Classical.choice, Quot.sound]`.
  - `python3 scripts/check_frame_graph.py` → "Frame graph check passed (19 compose, 8 incompatible, 17 morphism edges match Lean)."
  - `./scripts/check.sh`: all pass except markdown links ("15 broken relative link(s)", all to untracked frames drafts / other sessions' files).
  - `npm run check:concepts`: lens checks pass; `build-search-index --check` reports out of date even right after a rebuild (gitignored output; not investigated).

## Decisions
- Kept `RoleCompose` as a hook with an honest triviality theorem rather than deleting it.
- Did not change graph colours or the `Incompatibility` template in this session.
- **User decision (end of session):** split the red "incompatible" edges into distinct kinds. state–correction is *rigidity*, not a conflict between frames: a fixed maximizer accepts only corrections within U's ties (one-sided ΔU ≤ 0 at the optimum, not zero-sum with V). Separately, state utility is conservative on loops, so correct-then-restore has zero value: the correction-as-process part sits in the cycle/history summand (link to state–cycle).

## Open / next
- Role gate: give `RoleCompose` a real exclusion or delete it.
- **Next: split red edges by kind** (decided). Kinds and edges:
  - choice conflict (both frames choose on one menu; disjoint in `H`): deontic/au_floor/cci_cert–weighted_scalar, criteria_vector–cci_cert, robust–correction. Keep `Incompatibility`; consider orienting `liveInH` as `∃ x, H x ∧ A₂ x`.
  - shared resource (zero-sum by the conservation assumption in `H`): ai_power–human_power.
  - representability (one object cannot carry the other's distinction; escape by encode/augmented state): state–cycle. New structure, no situation class.
  - rigidity (one frame accepts only the degenerate part of what the other requires): state–correction. Theorems: fixed U accepts a correction only within U's ties; utility indifference as boundary (enlarges ties) and its cost (indifferent to channel preservation).
  - Then: per-kind DOT colour/style in **a**/**b**/**c**, `check_frame_graph.py` per kind, map legend and overview text, state-utility / exact / cycle / human-power cards, relations note.
- state–correction model: corrector utility V plus `Legit` predicate (MB4a hook); folds into the rigidity kind above.
- Roles across specialize edges (approval protocol → route target; corrig → correction). Proposed: rename specialize/encode at type level to embeddings of carriers; roles attach to uses.
- Real-valued weights (expected, not proven); actual `mapId` functions; general route = exact ⊕ cycle.
- Lean anchors point at `blob/main`; correct only once these Lean edits are pushed. Options: SHA-pinned permalinks at sync (shared with `spine-source-index.mjs`), or decl pages on the site.
- `metadata/axiom-ledger.json` has no Frame theorems (ledger scope unchanged).

## Key paths
- `formal/AlignmentProofSpine/FrameIncompatibility.lean`
- `scripts/check_frame_graph.py`
- `site/scripts/lib/lenses-data.mjs`

## Commits
- Lens review fixes: Lean frame modules, FrameLimits, graph check, DOT labels, lens cards (this commit).
