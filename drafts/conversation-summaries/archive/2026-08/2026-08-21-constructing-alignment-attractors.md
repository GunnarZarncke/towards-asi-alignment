# 2026-08-21 — Constructing alignment attractors paper

## Trigger
User asked for a critical review of a draft, then to extend the symmetry-breaking concept into an extension of `alignment-under-selection`. After a structure proposal, they asked to create the new paper in a new folder.

## Done
- Wrote `papers/constructing-alignment-attractors/` (tex, bib, `build.sh`); PDF builds (11 pages after lit pass).
- Indexed in `papers/README.md`. 
- Companion relation: evaluate attractors (paper 1) vs explicit symmetry-breaking construction (paper 2).
- Integrated Kulveit/Douglas *Artificial Self* as identity crystallization (reconstructive \(Q\), timing window, coherence ≠ \(D\)).
- Added constructor-level first-mover/other-modeling as a different, already-studied game (short note under unipolar rewrites; not re-derived).
- Selected literature pass from `deep-research_constructing_alignment.md`: reworded PD lemma as payoff redesign; added Maskin, Sandholm, Newton–Ma, Chassang, Harris, Blanchini, Soares/AI Control, Frank/Wechsler, Acemoglu–Robinson; new failure mode *Enforcement collapse*.

## Decisions
- Construction criterion requires \(D\) fixed independently of the intervention (anti-baked-conclusion).

## Open / next
- Author pass on density and the intervention table.

## Key paths
- `papers/constructing-alignment-attractors/constructing-alignment-attractors.tex`
- `papers/alignment-under-selection/alignment-under-selection.tex`

## Commits
- `cd866f9e` Add identity crystallization to Constructing Alignment Attractors.
- `898df416` Extend Constructing Alignment Attractors with lit pass and race note.
