# Graded lab V2-2b planning + cross-line blind-generation methodology doc

**Date:** 2026-07-15
**Trigger:** Follow-up discussion after V2-2 closure (GL-38, C3 4-round
failure): why C1/C2/C4/C5 converged under blind pass/fail growth while
C3 never did, whether richer feedback would have helped, and whether the
C-criteria themselves should have been chosen differently. User asked
for a V2-2b plan (multi-actor roles, exogenous workload, sandbox) and a
new procedure doc capturing lessons scattered across sessions/AGENTS.md.
**Explicitly: planning only, no implementation started.**

## What was done (all documentation)

1. **Diagnosis walkthrough** (chat only, then written into GL-39):
   C3 differs from C1/C2/C5 (declarative-state checks, decidable from
   the grower's own JSON) and from C4 (diagnosable by hand-derived
   invariants without running the sim) on three axes — emergent,
   depends on an unstated world fact (roster cardinality), and has no
   leak-safe gradient (grid search confirmed a step function, no
   interior band without hitting `slots=1`).
2. **Rejected fix:** disclosing "too saturated/too sparse" contention
   feedback — shown to be a coarsened readout of the checker's own
   threshold, same leak class as a raw number. Flagged C2's existing
   failing-roles disclosure as already over this line, not a safe
   precedent to extend.
3. **General principle distilled:** "blind the measurement, never the
   phenomenon" — real blinding regimes (trials, peer review, audits)
   blind the rubric, not the evaluated party's own system running. V2-2
   blinded both; the sandbox fix (item 5 below) targets exactly this gap.
4. **`experiments/graded-lab-simulation/PLAN_V2_2B.md`** (new) — planning
   doc for a follow-on growth attempt: (a) multi-actor-per-role schema,
   (b) exogenous stochastic workload mechanism, (c) generator-side
   non-scoring pilot sandbox exposing only sensor-plausible outcome
   fields (modeled on `embedded-simulation/audit_projection.py`'s
   plane-enforcement discipline, applied to the generator instead of
   the auditor). C1–C5 targets and thresholds explicitly unchanged.
   Lists 6 engineering prerequisites, none started.
5. **`experiments/BLIND_GENERATION_METHODOLOGY.md`** (new) — cross-line
   (not graded-lab-specific) lesson catalogue: 9 lessons (blind the
   measurement not the phenomenon; coarsened feedback is still a leak;
   world-fact vs. rubric-fact disclosure test; parameter ownership
   between generator and implementer; validate criteria against a live
   baseline before freezing; filter-vs-generator criterion shapes;
   misdiagnosis under opaque feedback is predictable, not a generator
   failure; archive-don't-discard contaminated rounds; progress logging
   /honest negatives) plus a 7-item pre-registration checklist. Draws on
   goal-agent-simulation's and lab-simulation's existing
   `BLIND_GENERATION.md` files and embedded-simulation's projection
   plane as prior art.
6. **`results/FINDINGS.md` GL-39** — records the diagnosis and plan
   as planning-only, no code/brief/round started.
7. **`PLAN_v2.md`** — added a V2-2b row (planning only) and document-map
   pointers to both new files.
8. **`experiments/README.md`** — added a pointer to the new
   methodology doc.

## Non-obvious decisions

- Did not touch C1–C5's mechanical definitions or thresholds — the plan
  changes the substrate's capacity to satisfy C3 and the grower's
  ability to observe progress toward it, not the target itself.
- Did not retroactively re-score or re-open V2-2's four closed rounds.
- Explicitly rejected extending C2's failing-roles disclosure as a
  precedent, rather than treating "we already do this for C2" as
  justification.
- The methodology doc is deliberately placed at `experiments/` top level
  (not inside `graded-lab-simulation/`) since it draws on and applies to
  all blind-generation lines, not just this one.

## Open / next steps

- V2-2b is not started. Before any brief is sent: multi-actor schema +
  regression test against v1/v2 digest pins, workload-mechanism
  interface design, pilot-runner field-leak audit, `BLIND_GENERATION.md`
  v2-2b section, and a pre-registered FINDINGS entry — all listed in
  `PLAN_V2_2B.md` §"Open engineering work."
- User has not yet said whether to proceed with V2-2b implementation.

## Key paths

- `experiments/graded-lab-simulation/PLAN_V2_2B.md`
- `experiments/BLIND_GENERATION_METHODOLOGY.md`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-39)
- `experiments/graded-lab-simulation/PLAN_v2.md`

No commits this session.
