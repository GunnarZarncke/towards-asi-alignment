# 2026-09-23 — PRA diagram vs Lean

## Trigger
User asked to review `lean_checked_bayesian_pra_diagram.py` against the actual Lean spine and fix inconsistencies.

## Done
- Relabeled every box: `Market n` plus the Evidence.lean cert → predicate (or explicit “no cert / not a bundle leaf”).
- Added the missing `FilterCert` leaf (required by `CoherentCertificateBundle`; no market).
- Rewired edges to `Evidence.lean` adapters, `Core.lean` `MB*` directions, and `metadata/assurance-model.yml`.
- Layout pass: plain-text diamonds (edges leave vertices); Yes down / No down-right; more `nodesep`/`ranksep`; polyline routing.
- Restored spine edges via Lean hubs `AccessRobust`, `CorrectionIntegrity`, and `CoherentCertificateBundle` (all bundle leaves now have a path).
- Split types: left is an event tree; right is Lean AND into Certified plus PRA composition into \(f_M\). Join node `P(ACCEPT | hazardous)` so \(f_M\) and \(f_U\) parameterize the ACCEPT draw.
- Broke the `Market 15 → 18 → f_M` pipeline. \(f_M\) now has parents: bundle \(P(\mathrm{AND\ leaves})\) plus residuals 10, 13, 15, 16, 18. Market 18 is one residual, not the source.
- Split into two figures (event tree / assurance). Dropped the key-quantity and interpretation boxes; captions belong in the host document. \(f_M\) is the interface: assurance outputs it, the event tree takes it as an input.
- Outputs: `lean_checked_bayesian_pra_event_tree.png`, `lean_checked_bayesian_pra_assurance.png`. Removed the combined PNG.
- Event tree: one shared **No catastrophe** sink (not-hazardous and controls-hold). Dashed assurance edges labeled: warrant vs common-cause.
- Converted both figures from Python to plain Graphviz (`.dot`) plus `render_pra_diagrams.sh`. Deleted `lean_checked_bayesian_pra_diagram.py`.
- Event tree: scope gates for `f_M,multi` (Market 11, represented branch) and `c_novel` (Market 17, consequence branch). TODO in `metadata/TODO.md` to wire through manifest, assurance `.dot`, prose, and site demo.

## Decisions
- Bare `M<n>` is forbidden here: Market 8 is MB7a, Market 10 is MB7c, Market 13 is MB10. The old “M10 Adversarial robustness” label was the MB10/Market-10 mix-up.
- Market 5 is auditor independence (`PositiveMeasuredPathCertificate`), not “correction legitimacy” (that is MB4 / Market 4).
- Markets 4, 5, and 16 are complementary PRA obligations; Lean gives three routes onto `CorrectionIntegrity`. `MB6b` points basin → integrity, not Market 4 → 16.
- Market 15 composes the bundle leaves (1–6, 8–9, 12, `FilterCert`). Markets 10, 11, 13, 16, 17 are not bundle fields.
- Market 18 is the `SafeIn` stub, not unary `Safe` and not MB11. Market 14 is constructibility, not a generic `o` and not MB11.
- `f_M` stays a PRA parameter: a mix of the AND-stack and residual rates, not a Lean object and not Market 18. Market YES is not a Lean constructor. MB8 is retired and absent.
- Do not multiply market prices into \(f_M\). Market 7 reaches \(f_M\) only via Market 16.

## Open / next
- Catalog still maps Market 9 → `primaryBridge: MB7b` while Evidence/assurance-model attach Market 9 to `HiddenRouteBound` and leave `FilterCert` unmarketed. Diagram follows Lean + the manifest.
- Bundle fan-in still has some long diagonals (ten leaves → one hub).

## Key paths
- `drafts/plans/predictions/lean_checked_bayesian_pra_event_tree.dot`
- `drafts/plans/predictions/lean_checked_bayesian_pra_assurance.dot`
- `drafts/plans/predictions/render_pra_diagrams.sh`
- `drafts/plans/predictions/lean_checked_bayesian_pra_event_tree.png`
- `drafts/plans/predictions/lean_checked_bayesian_pra_assurance.png`
- `formal/AlignmentProofSpine/Evidence.lean`
- `formal/AlignmentProofSpine/Core.lean`
- `metadata/assurance-model.yml`

## Commits
- `c853b397` — PRA Graphviz sources + render script (event tree / assurance `.dot`, PNGs; removed Python generator). `metadata/TODO.md` scope-parameter follow-up left unstaged.
