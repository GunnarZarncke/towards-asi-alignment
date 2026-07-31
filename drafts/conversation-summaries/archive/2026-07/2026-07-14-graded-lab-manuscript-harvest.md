# 2026-07-14 — Graded lab manuscript harvest: four backlog findings written into chapters

## Trigger

User: "Harvest! Now add the findings to the book chapters as defined." —
referring to the 4-item manuscript-integration backlog registered in
`experiments/graded-lab-simulation/PLAN.md` (ch07, ch11, ch33,
ch34/ch36/ch40), most recently updated after G-23/G-24 in the previous
session.

## Done

Added one short, sourced, hedged paragraph to each of four chapters, at
the point in the existing text that already made the relevant abstract
claim (surgical, not a rewrite):

- **`ch07-finding-boundary.tex`** — after the existing testbed-lesson
  paragraph on ripples/false-merges: `signal_handoff_pair` (G-11,
  write/read-only coordination invisible to passive discovery and to
  passive-seeded intervention; recovered only by a standalone all-pairs
  dependency-score probe) and `three_way_nod` (G-12, the same probe
  recovers the barrier but over-merges a resource-bound bystander
  through shared queue contention).
- **`ch11-capability-without-task-ontology.tex`** §"Why This Is
  Task-Agnostic but Not Ontology-Free" — the `I_ctrl` outcome-vector
  scoping bug (G-13/G-14): an outcome vector inherited from an earlier
  diagnostic silently re-imported a task ontology, making a
  contention-driving bystander look identical to the actual task driver
  until the vector was widened.
- **`ch33-certification-without-construction.tex`** §"Adversarial
  Certification" — toy-simulation's `belowThreshold`-on-passive-only /
  `light_handles`-suffices instrumentation-cost-curve result.
- **`ch34-selection-environment.tex`** §"A Minimal Model of
  Socio-Technical Selection" — the G-23 selection-battery result
  (deployment mass shifted toward higher-throughput, away from the sole
  correction-preserving-tagged program, with severity falling), stated
  with the G-24 caveats inline (confounded tag, single narrow handle)
  rather than as an unqualified confirmation.

`ch36`/`ch40` deliberately left untouched: G-23 supplies no parasite or
goal-laundering signature (per G-24's finding), so no addition was made;
checked both chapters for any premature claim already citing this line
and found none.

Verified `make check` (structure + citation + bibliography-summary) and
a full `./build.sh` (1332pp) both clean after the edits. No new bib keys
needed — `zarncke2025uad`/`zarncke2025biq` already existed and are
reused for the same self-citation purpose elsewhere in these chapters.

Updated `PLAN.md`'s manuscript-integration-backlog section to record
exactly where and how each item was written in, so it is not re-derived
from scratch later.

## Decisions

- Treat each addition as a scope-limited empirical anchor with its
  caveats stated in the same sentence, not a separate hedge elsewhere —
  matches the chapters' existing hedging style.
- No edits to `ch36`/`ch40` — absence of evidence is not itself a
  manuscript sentence worth adding.

## Open / next

- Phase 8a/8b/8c (from G-24) remain pre-registered, not run; if run,
  the ch34 paragraph should be revisited (it explicitly names the
  confounded-tag and narrow-handle caveats it would address).
- Phase-7-gate language fix in `PLAN.md`'s roadmap table (G-24 concern
  4) is still named but not applied.

## Key paths

- `chapters/ch07-finding-boundary.tex`
- `chapters/ch11-capability-without-task-ontology.tex`
- `chapters/ch33-certification-without-construction.tex`
- `chapters/ch34-selection-environment.tex`
- `experiments/graded-lab-simulation/PLAN.md` — backlog section updated

## Commits

- Not committed this session; user has not yet asked.
