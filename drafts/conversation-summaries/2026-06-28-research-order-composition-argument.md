# 2026-06-28 — Research-order / composition argument into appH + crosswalk

## Trigger
Reviewer reply (building on the bridges-crosswalk feedback) made three strong points: (1) the book's crispness *relocates* fuzz one level down into predicates but makes its location legible — crispness conditional on the chosen frame; (2) the selection/basin layer (MB6) was the reviewer's own omission and is the book's *most* differentiated, *least* validated area, with value lock-in as a direct counterexample to MB6b; (3) composition matters — shared antecedents correlate bridges, disjunctive routes (MB6b∨MB8) add failure tolerance, the conjunctive spine is capped by its weakest necessary link, and the dependency graph gives a research ordering + a "blast radius" query the Lean spine can answer. User asked to include the argument and especially derive the research agenda **organically in the implied dependency order**.

## Done
- `appendices/appH-research-program.tex`:
  - Reframed intro: dropped "order is logical dependency, not priority"; now states the bridges compose and the composition prescribes priority + sequence; per-bridge items are presented in dependency order.
  - New leading section **Dependency order, composition, and research priority** (`sec:research-dependency-order`): four paragraphs (shared antecedents → positive correlation; disjunctive routes → failure tolerance; conjunctive weakest-link ceiling; composition → order + Lean blast-radius query), plus a **Priority tiers** subsection (Tier 0 enabling: MB1/MB2/MB9; Tier 1 gating hard bridges: MB4/MB7a–c; Tier 2 transport+successor: MB3/MB5; Tier 3 selection: MB6a/MB6b/MB7d), with MB8 noted as a disjunctive backstop.
  - Added `\label`s `sec:bridge-empirical` and `sec:master-crux`; wired `\ref`s.
  - Enriched the MB6a–b item with the multipolar-literature context and the value-lock-in counterexample (`\autocite{critch2021multipolar,critch2020ai,christiano2019failure}`).
- `appendices/appBridge-crosswalk.tex` takeaway:
  - New **Crispness, and where it lives** paragraph (MB4 example: fuzz pools in `CorrectionIntegrity`, not the arrow; crisp-and-locatable >> fuzzy-and-everywhere; conditional on the System/bundle/bearer/correction frame).
  - Strengthened the MB6 "Added" bullet (field's narrative neglect is diagnostic; value lock-in counters MB6b) with the same citations.
  - Added a sentence to "The actual bet" linking composition-as-research-object to appH §`sec:research-dependency-order`.
- `metadata/TODO.md`: added TODO to propagate `MB9` into appI/appH per-bridge/appE (range strings still say MB1–MB8; no `appi:ass:mb9` block yet).
- Build green: `./build.sh` exit 0, no undefined refs/citations; `make check` passes (132 cited keys). New section is appendix I.1 (research program shifted H→I after the crosswalk insertion).

## Decisions
- Kept the per-bridge subsections physically in MB-number order (already ≈ dependency order: MB1→MB2/3→MB4→MB5→MB6→MB7→MB8) and made the ordering *explicit + tiered* in the new lead section rather than physically shuffling 13 paragraphs — surgical, and satisfies "derive in the implied order."
- Referenced grounding (MB9) by chapter home (ch03) in appH instead of `appi:ass:mb9`, which does not yet exist — flagged as a TODO rather than expanding scope to fix appI/appE here.
- Cited only bib keys that exist (critch2021multipolar, critch2020ai, christiano2019failure). Hendrycks evolutionary-pressure, gradual-disempowerment (Kulveit et al.), and value lock-in (Ord/MacAskill) have no keys; described in prose without `\cite`.

## Open / next
- MB9 propagation (new TODO) — appI assumption block + appH Tier-0 item + appE/appI/appH "MB1–MB8" → "MB1–MB9".
- Optional: actually run the Lean blast-radius experiment (delete each hard bridge axiom, record which theorems go grey) and tabulate per-bridge blast radius in appH — the reviewer's most generative suggestion.
- Optional: add bib entries for Hendrycks natural-selection, gradual disempowerment, value lock-in; then cite in the MB6 discussions.

## Key paths
- `appendices/appH-research-program.tex` (§`sec:research-dependency-order`), `appendices/appBridge-crosswalk.tex` (takeaway)
- `metadata/assumptions-ledger.md` §IV, `formal/AlignmentProofSpine/Core.lean` (MB axioms), `context/lean_proof_dependency_graph.dot` (graph for blast-radius)

## Commits
- (none this session)
