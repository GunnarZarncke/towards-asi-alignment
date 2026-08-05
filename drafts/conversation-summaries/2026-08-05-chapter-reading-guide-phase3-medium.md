# 2026-08-05 — Chapter reading guide Phase 3 (medium audit)

## Trigger
Audit the remaining two- and three-edge chapters after the easy rollout; ch09 had already been audited in Phase 2.

## Verdict
- **Add `readingguide`: ch38 only.** Its opening continues ch37's Alignment Attractor frame, but assumes without reintroducing ch02's artificial-civilizational control loop. The new one-item box supplies that object and names the two basin definitions plus pivotal process.
- **Omit:** ch09, ch11, ch17, ch24, ch31, ch34, ch40, ch47, ch48. Their direct prerequisites are locally reintroduced, bridged by the previous closing, introduced later when used, or are forward references in manuscript order.

## Graph caveat
The informal dependency DAG can contain logical/conceptual edges from a later chapter to an earlier chapter (for example `ch38 → ch34`). They are not valid entry prerequisites in PDF order. Treat every edge as an audit prompt; do not convert it mechanically into a `readingguide` item.

## Verification
- Regenerated chapter reading checklists and synced chapter site content.
- `make check` passed: structure, citations, bibliography summaries.

## Open / next
- **Phase 4:** high-fan-in and synthesis audit: ch16, ch22, ch26, ch33, ch42, ch44.
