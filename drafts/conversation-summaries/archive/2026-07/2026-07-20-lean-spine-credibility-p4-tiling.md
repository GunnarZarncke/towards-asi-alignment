# 2026-07-20 — Lean spine credibility P4: Löbian tiling contrast

## Trigger

User asked to prove tiling, integrate it into the book, and review whether the completed credibility-plan work fits together.

## Done

- Added `formal/AlignmentProofSpine/Field/Finite/LobTiling.lean`.
  - `HBLConditions`: explicit necessitation, distribution, and internal-necessitation closures.
  - `LobFixedPoint`: an explicitly supplied diagonal-lemma instance.
  - `lob_rule_from_fixed_point`: derives the Löb rule from those inputs plus a reflection implication.
  - `self_certifying_tiling_obstruction`: a diagonal successor cannot be accepted solely by reflecting the same proof system's proof of its safety.
  - `audited_successor_risk_bound_without_provability`: contrasts the book's external, measured successor-audit path with internal provability/reflection.
- Re-exported the module through `Field.lean` and documented it in `formal/README.md` and the root module.
- Added surgical pointers in ch30 and formal statement/proof summaries in Appendix G.
- Added the missing Appendix G table for the P3 consistency/local bridge-separation witnesses.
- Corrected the axiom-ledger gloss for the P1 trace theorem: raw Unicode theta was invalid in the generated LaTeX table; it now uses ASCII `theta`.

## Review

- P1–P4 now form a coherent evidence ladder: trace certification (P1), a concrete battery-gate shape without false deployment discharge (P2), satisfiability plus local non-implication witnesses (P3), and the proof-theoretic limit of self-certification versus an external-audit alternative (P4).
- The P4 claims are consistently conditional. `HBLConditions` and `LobFixedPoint` are field-scope inputs, not MB bridges, axioms about the spine, or properties attributed to real agents.
- Corrected one stale root-module documentation claim of a collective `all_bridges_independently_load_bearing` theorem; only the individual witnesses exist.
- P3's theorem names overstate their formal strength slightly: current witnesses show **local** antecedent/consequent separations, not that one bridge is independent of the conjunction of all others. Appendix G now says this explicitly. A genuine joint-independence model remains open.

## Verification

- `lake build`: success (2253 jobs).
- `python3 formal/scripts/check_spine_model.py`: pass (18 witnesses, 2 consistency exports).
- `python3 formal/scripts/check_axiom_budget.py`: pass (38 headline theorems).
- `make check`: pass.
- `./build.sh`: pass; regenerated `dist/pdf/towards-superintelligence-alignment.pdf`.
- `#print axioms`: `lob_rule_from_fixed_point` and `self_certifying_tiling_obstruction` have no axioms; the audit contrast has only the pre-existing abstract spine carriers, no MB bridge or provability assumption.

## Open / next

- Upgrade P3 from local separation witnesses to a genuine family of models satisfying every other bridge while falsifying the selected bridge.
- P4 deliberately does not prove a Gödel diagonal lemma for coded arithmetic or solve reflective stability/tiling for real agents.

## Commits

- `ea05db30` — Lean spine credibility P1–P4 (this session)

## Key paths

- `formal/AlignmentProofSpine/Field/Finite/LobTiling.lean`
- `chapters/ch30-successor-central-test.tex`
- `appendices/appG-lean-proof-spine.tex`
- `formal/README.md`, `metadata/assumptions-ledger.md`
- `formal/axiom-ledger.json`, `metadata/axiom-budget-index.tex`
