# 2026-10-24 — Bare vs record-carrying state (frame graphs)

kind: new-work
uptake: local

## Trigger
The user noted that encoding history or route bits into the state escapes state–cycle, but then the state is no longer "state only" as instrumental-convergence arguments assume. They asked to model the two kinds of state separately with edges for each, and to discuss how far existing reward functions encode the trajectory (speculation: LLM training does, which might help long runs).
Prompts: paraphrase-only

## Done
- content: New `formal/AlignmentProofSpine/FrameHistoryState.lean`:
  - `state_utility_lifts_to_records`, strict by `record_utility_not_state`;
  - `route_exact_on_records`: every edge reward is a difference of record values;
  - `round_trip_value_on_records`: the `stateCycleIncompat` round trip gets value 1 on records;
  - `unrecorded_route_not_representable`: the escape needs the record to see the route.
  Imported in the root module; module tables updated in `AlignmentProofSpine.lean` and `formal/README.md`.
- content: `FrameMorphisms`:
  - new node `hstate` with carrier `augmentedStateHistory`;
  - `state → hstate` specialize (`readAtRecordEnd`);
  - `hist → hstate` and `route → hstate` encode, replacing `→ state`;
  - `morphism_tgt_carriers` docstring updated.
- content: DOT **a**/**b**:
  - `hstate` node and its three edges;
  - state–cycle label "(state carries no record)", also in **c**;
  - **b** needs `constraint=false` on `hist → hstate` because Graphviz `dot` crashes with "trouble in init_rank" without it.
  - SVGs and **x** regenerated.
- content: Relations note:
  - Encodings section gets a paragraph on the two kinds of state, plus a calibrated reading of existing reward functions (token-level state is a full record within an episode; outcome rewards ignore the route; judges, PRMs and format/CoT terms read only the transcript; compaction makes the record lossy; policy-side record ≠ reward-side record);
  - inventory and registry rows;
  - new "Bare and record-carrying state (Lean)" table.
- content: Site:
  - new lens card `record-carrying-state`;
  - state-utility, history-value and cycle-residue cards point to it;
  - `state → hstate` and `route → hstate` map edges link to `FrameHistoryState`.
- bookkeeping: Verification:
  - `lake build AlignmentProofSpine` → "Build completed successfully (2271 jobs).";
  - `#print axioms`: new theorems ⊆ `[propext, Quot.sound]` or none;
  - `./formal/check.sh --no-build` → "Axiom budget check passed (48 theorems, no drift).";
  - `python3 scripts/check_frame_graph.py` → "Frame graph check passed (19 compose, 8 incompatible, 18 morphism, 3 limit/strengthens edges match Lean).";
  - `npm run check:concepts`: lens syncs up to date; `build-search-index --check` out of date (pre-existing, as on 2026-10-23).

- content (second request: write up the finding, check Turner, add the hstate–correction edge):
  - New `drafts/state-utility-in-practice.md`: bare vs record state, correction trilemma on records, instrumental convergence after checking Turner, table of what current reward terms read, policy-side vs reward-side record, test ideas, related work.
  - **Correction from Turner check:** the earlier claim that records break the instrumental-convergence premise was wrong. Turner et al. 2021 Def. 3.5 is state-based, but Turner and Tadepalli 2022 App. A count over any outcome set, "or a trajectory". Records change what a chosen utility can express, not the count. Card, note and this log corrected.
  - `FrameHistoryState`: `CorrRecord`, `state_accepts_only_ties` (bare-state rigidity), `record_accepts_compensated_correction`, `hstateCorrectionIncompat` (`H`: utility ignores the channel bit; protect ⇔ seek; boundary: utility values the kept channel), registry `incompatExt`.
  - DOT **a**/**b** red edge `hstate – correction`; `check_frame_graph.py` reads `incompatExt`; site edge link and card text; relations note rows; the note's reward-practice paragraph moved to the write-up.
  - Verification: `lake build AlignmentProofSpine` → "Build completed successfully (2271 jobs)."; axioms ⊆ `[propext, Classical.choice, Quot.sound]`; `check_frame_graph.py` → "Frame graph check passed (19 compose, 9 incompatible, 18 morphism, 3 limit/strengthens edges match Lean)."; `sync-lenses --check`, `sync-lens-graph --check` up to date.

## Decisions
- Kept `state` for the bare state (the instrumental-convergence premise) and added `hstate`; did not rename `state`.
- `hstate`–correction drawn red now (registry `incompatExt`, no kind); its kind is set in the red-edge split.

## Open / next
- Superseded by `2026-10-25-frame-edge-classes.md` (red-edge split done; write-up open items listed there and in the write-up).

## Key paths
- `formal/AlignmentProofSpine/FrameHistoryState.lean`
- `drafts/alignment-frames-relations.dot`
- `site/scripts/lib/lenses-data.mjs`
- `drafts/state-utility-in-practice.md`
