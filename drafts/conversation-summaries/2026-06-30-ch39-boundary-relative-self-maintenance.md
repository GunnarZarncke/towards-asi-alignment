# 2026-06-30 — ch39 boundary-relative self-maintenance

## Trigger
User asked to add the Pando Problem / boundary-shaping point to ch39 after discussing correlated steerability and the shift from "read truth" to "bound faking."

## Done
- `chapters/ch39-safety-case.tex`: added a new `\paragraph{Boundary-relative self-maintenance.}` under Verifiability Labels.
- The new paragraph states that instrumental convergence is boundary-relative: a system maintains the control boundary whose continuation supplies memory, access, capability, and update gradients.
- Cites `kulveit2025pando` for AI individuality / boundary ambiguity, and reframes human-inclusion as a substitution-cost question: what would it cost to fake a human-inclusive boundary while making human judgment causally superfluous?
- Added a summary bullet clarifying that boundary shaping helps only when human correction, legitimacy, and grounding are constitutive of the maintained process.
- Updated the ch39 Chapter References sentence to include AI individuality and boundary ambiguity.
- Verified with `make check` (structure, citations, bibliography summaries all pass).

## Decisions
- Used the existing `kulveit2025pando` bib key rather than adding AXRP / hierarchical-agency references in this pass, because the user specifically confirmed the Pando Problem.
- Placed the material in ch39 rather than ch39b because the requested change is safety-case discipline: what a certification case must state about the operative boundary and substitution/faking cost.

## Open / next
- Optional future pass: add AXRP / Kulveit hierarchical-agency references if the text later needs the stronger "humans become instrumentally less useful" citation.
- Reconcile with the open BIG REVIEW on correlated steerability: ch39 now has the boundary-relative self-maintenance caveat, but appH/crosswalk disjunctive-tolerance language still needs qualification.

## Key paths
- `chapters/ch39-safety-case.tex`
- `references/dynamical-systems.bib` (`kulveit2025pando`)
- `metadata/TODO.md` (correlated steerability BIG REVIEW)

## Commits
- (none)
