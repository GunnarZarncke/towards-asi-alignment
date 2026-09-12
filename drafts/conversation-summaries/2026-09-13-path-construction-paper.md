# 2026-09-13 — Path construction spin-out

## Trigger
A conversation questioned the v2 unification of CEV with outer alignment: the CEV principal is future better humans, not present controllers. The load-bearing residue was construction: TSA models a required end state, not constraints on incremental steps from the current flawed correction system, nor whether that sequence is realizable. User asked for a short dense LaTeX spin-out as a base for later v2 Construct chapters, and an extension of the Construct 2.0 plan.

## Done
- Added [`papers/path-construction/`](../../papers/path-construction/): `path-construction.tex`, `.bib`, `build.sh`, built PDF (7 pp.).
- Listed the paper in [`papers/README.md`](../../papers/README.md).
- Extended [`drafts/plans/construct.md`](../plans/construct.md): third object (path construction); Family E; checklist; P0/P4.
- Noted Family E in [`metadata/TODO.md`](../../metadata/TODO.md) Construct row. No Lean `PathRealizable` in v1.

## Decisions
- Destination realizability (`ConstructionCrux` / \(\exists A\)) and path realizability are independent open cruxes. Near-term construction lives in the path-without-destination cell.
- Joint state is \((G,A)\). Successor constraints on \(A\), \(U_H\) as a node invariant, and pivotal-process basins are nearby and the wrong object.
- Edge family \(\mathcal{E}\): authorization, non-foreclosure, power match, bounded irreversibility, local improvement on a pre-frozen \(\Phi\), channel live (necessary, not sufficient). Partial nodes that fail some cruxes are the normal case.
- CEV remains one named \(G^\star\), not the unique intended principal.
- No v1 manuscript chapter; no Lean axiom. Family E unblocks only when a named host can fail a path claim.

## Open / next
- Describe \(G_0\) as an instance (who holds which correction authority), or record that specify-side debt as blocking well-posedness.
- Freeze a first \(\Phi\) independently of any exhibited path.
- If later typed in Lean, `PathRealizable` stays uninterpreted next to `ConstructionCrux`.
- Constructibility of taking the steps remains Family D, not this paper.
- Left uncommitted (prior or adjacent drafts): maintained-blanket import, containment-verification news card, `drafts/alignment-problem-alternative-decomposition.md`, alignment-under-selection edits, site/field-news leftovers.

## Key paths
- `papers/path-construction/path-construction.tex`
- `drafts/plans/construct.md` (Family E)
- `formal/AlignmentProofSpine/AlignmentConstruction.lean` (destination crux only)

## Commits
- none
