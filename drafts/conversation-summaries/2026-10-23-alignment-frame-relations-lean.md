# 2026-10-23 — Alignment-frame relations graph in Lean

kind: new-work
uptake: local

## Trigger
User asked for typed nodes on the frame-relations graph, then for a Lean representation from which variant **c** can be derived (or an account of why not), then compose paths/slots and carriers/maps, then proofs for the incompatible (red) edges.
Prompts: paraphrase only (no prompt id recorded).

## Done
- content: `drafts/alignment-frames-relations.md` — node registry `(role, object-kind, assessment-kind)`; sections *Formal layer (Lean)*, compose paths, carriers and maps, *Incompatibilities (Lean)*; state–correction prose narrowed to updates that lower the chosen outcome.
- content: `formal/AlignmentProofSpine/FrameRelations.lean` (interfaces, variant **c** classifier, `variantC_all_derived`), `FrameComposePaths.lean` (8 paths partitioning 19 compose slots), `FrameMorphisms.lean` (carrier tags and `mapId` registry for graph **a**/**b** specialize/project/encode), `FrameIncompatibility.lean` (all 8 red edges as `Incompatibility` instances; `no_finite_weights_represent_floor`; `gradient_closed_walk_zero`; `registry_matches_proofs`).
- content: DOT **a**/**b**/**c** state–correction label changed to "fixed U rejects updates that lower its chosen outcome"; SVGs regenerated.
- content: robust–correction re-proved as a quantifier conflict (corrections counted as disturbances cannot reach a target outside `K`; `robust_with_correction_iff_closed`, `robust_correction_target_meets_K`); captured-set version moved to `FrameLockIn.lean` as the lock-in illustration with `robust_invariance_sign_blind`; DOT label "if corrections count as disturbances and aim outside the set"; md prose rewritten.
- bookkeeping: root module imports and module table; `formal/README.md` module map row.
- content: DOT node ids renamed for disambiguation (`criteria_vector`, `weighted_scalar`, `au_penalty`, `au_floor`, `cci_cert`, `coord_floor`, `preserve_tuple`); human-visible two-line labels on all nodes in **a**/**b**/**c**; registry tables in md synced; SVGs regenerated.
- bookkeeping: verification — `lake build AlignmentProofSpine` → "Build completed successfully (2269 jobs)."; `./formal/check.sh --no-build` → "Axiom budget check passed (48 theorems, no drift)."; `#print axioms` on each incompatibility instance shows only `propext`, `Quot.sound`, `Classical.choice`.

## Decisions
- Compose edges are not derivable from interface types; variant **c** greens are a named correction-centered reading (`ComposeSlot`), checked rather than inferred.
- Incompatibility template uses `liveInH` (one frame accepted inside `H`) instead of per-frame non-vacuity: a fixed-utility evaluator rejects every update in its conflict class.
- vector–cci_vec is a non-entailment under Pareto (`pareto_does_not_entail_floor`); red only after scalarization (`viaProjection`).

## Open / next
- robust–correction: the split into adversarial vs correction inputs is only coherent if the system cannot relabel corrections as attacks; that links to the `MB4a` anti-capture condition but is not formalized here.
- Morphisms are `mapId` keys only; no actual map definitions or commuting squares yet. `limit`/`strengthen` edges are not registered.
- Summand edges still rest on node pairing plus the closed-walk lemma; no general direct-sum decomposition.
- Spinout PDF (`papers/alignment-frames/`) not updated for any of this.

## Key paths
- `drafts/alignment-frames-relations.md`
- `formal/AlignmentProofSpine/FrameIncompatibility.lean`

## Commits
- (this session) frame relations Lean + graphs + `alignment-frames-relations.md`; spinout paper/md left unstaged.
