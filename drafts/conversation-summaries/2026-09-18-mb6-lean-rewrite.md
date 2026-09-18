# 2026-09-18 — MB6 Lean rewrite

## Trigger
User asked to do the Lean rewrite of the MB6 object: unsigned `PercolationEvidence → BasinStable → CorrectionIntegrity` has no sign; use signed \(g_{\mathrm{CCI}}\) and shock-robust ∧ \(g_{\mathrm{CCI}}\ge-\varepsilon\) as a correction-supporting basin.

## Done
- Retyped `formal/AlignmentProofSpine/Core.lean`: `CorrectionSelectionGradient`, `BasinShockRobust` (`abbrev BasinStableSys`), `CorrectionSupportingBasin` / `CorrectionSupportingBasinSys`, `MB6a_gradient_estimator_soundness`, `MB6b_correction_supporting_basin`. Frozen `ε` independent of the measured gradient. `PercolationEvidenceSys` kept as graph scaffolding, not the MB6a antecedent.
- Consumers: `BridgeCruxes`, `Certification` (`LayeredAlignedDef`, `BridgeLayerInputs`), `Chokepoint` (channel reads `CorrectionSupportingBasinSys`; `sound` via MB6b only), `Defeaters`, `SpineModel`, `CooperationGraph`.
- Guards: `check_axiom_budget.py` names, `lean_graph_node_aliases.json`, `axiom-ledger.json` + `metadata/axiom-budget-index.tex`. `./formal/check.sh` lake build green; axiom budget accepted after `--update`.
- Prose/sync: App G equations and `LayeredAlignedDef`; App B MB6 paragraph + table; ch42/ch48 `CorrectionSupportingBasinSys`; App D `\leanspine`; `bridges.yml`; MB6 + subsumption cards; assumptions ledger; Implementation Brief sketch; `spine.md` P2 checked; `field.md` Lean-today; markets plan Spine row.
- Site: `sync:concepts`, `sync:bridges`, `sync:field-agendas`, `sync:field-v2`, `sync:lean-spine`, `sync:bridge-graph`.
- Graphs: `context/lean_proof_graphs/{00,04}` and `lean_proof_dependency_graph.dot` labels; `scripts/render_lean_graphs.sh`.

## Decisions
- No `Int ε` in a `structure … : Prop`; pack `∃ ε` with `FrozenGradientTolerance` so ε cannot be cooked after seeing \(g\).
- Unary `LayeredAlignedDef` via `CorrectionSupportingBasinSys`.
- Chokepoint `sound` is MB6b only (MB6a is upstream estimator soundness). Legacy name `percolationChannel` kept.
- `LockedInBadBasin` kept (unsigned stable ∧ bad). Market YES still does not discharge MB*.
- No covering n-tuple.

## Open / next
- Markets lane: remaining author Qs Q1/Q2/Q6/Q8. Do not list markets.
- Spine P2 leftover: Defeaters finite toys for MB2/MB3/MB5/MB6a/MB7a/MB9.
- Optional: `./build.sh` after App G/`\leanspine` edits when next building the PDF.
- Do not commit unless asked.

## Key paths
- `formal/AlignmentProofSpine/Core.lean`
- `appendices/appG-lean-proof-spine.tex`
- `drafts/plans/spine.md`
- `drafts/plans/bridge-prediction-markets.md`

## Commits
- none
