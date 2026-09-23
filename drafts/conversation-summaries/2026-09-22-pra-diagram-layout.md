# 2026-09-22 — PRA diagram layout

## Trigger
User asked to run `lean_checked_bayesian_pra_diagram.py`, inspect the generated graph, and improve layout.

## Done
- Regenerated the figure after a layout rewrite of `drafts/plans/predictions/lean_checked_bayesian_pra_diagram.py`.
- Default render: `drafts/plans/predictions/lean_checked_bayesian_pra.png` (about 4494×2777, no longer a 2880×456 strip).

## Decisions
- Dropped `size`/`ratio=compress` (that forced the unreadable wide strip) and switched to a two-column `dot` layout: compact vertical scenario tree on the left, four-column assurance grid on the right, key/notes under their columns.
- `newrank=false` so the assurance ranks do not stretch the scenario tree.
- Side exits (No / stop / survive) share an `exits` group so they stack to the right of the spine.
- Dropped the `f_M → assurance_result` return edge (it routed around the whole assurance cluster). The diamond now says the result is from `f_M` or `f_U`.
- Dropped the `M1 → M13` dashed cross-cut so the M13 fan-in does not wrap the cluster; M13 still connects to the mechanism nodes.

## Open / next
- Diagram is still a draft-plan artifact; not wired into Appendix H or the site.
- A few long composition edges remain (`M3`/`M6`/`M17` → `M15`).

## Key paths
- `drafts/plans/predictions/lean_checked_bayesian_pra_diagram.py`
- `drafts/plans/predictions/lean_checked_bayesian_pra.png`

## Commits
- none
