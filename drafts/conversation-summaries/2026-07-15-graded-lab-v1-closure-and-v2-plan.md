# 2026-07-15 — Graded lab v1 program closure + PLAN_v2

## Trigger

User asked for a high-level review of where the graded-lab line stands
and whether more book value is expected. Review verdict: methodological
hygiene strong, but the prize question (detector-evading emergence) is
structurally unanswerable in the v1 design — selection over a fixed
hand-written roster has no variation operator, and the roster/tags/
proxies sit outside the blinding boundary (where the GL-23/25/29
confounds live). User then decided: (1) close the v1 program (not the
codebase), consolidate, write a terminal summary + reproduction doc
with the final commit hash; (2) plan a v2 program with population
variation, LLM red-teaming, blinded-grown ecology under a **fixed
target-blind complexity criterion** (explicitly rejecting "grow until
it works").

## Done

- `results/TERMINAL_SUMMARY.md` — v1 arc, why closed, positive/null
  tables, interpretation guardrails, what carries into v2.
- `REPRODUCING.md` — env, determinism, per-finding command map
  (GL-1–GL-30), verification checkpoints; final v1 commit hash slot
  filled in the follow-up commit.
- `PLAN_v2.md` — v2 program: Q1 machinery transfer to a blinded-grown
  ecology (external validity, gate for the rest), Q2 selection **with
  variation** (GL-25 noise-floor controls as hard gates), Q3 LLM
  red-teaming (surface-blind vs informed, budget-capped). Phases
  V2-0–V2-7, blinding map, complexity criterion C1–C5 (frozen in V2-1
  before growth, mechanical checker, ≤4 rounds), predictions P1–P8
  sketch, risks, bridge coverage. FINDINGS numbering continues at GL-32.
- FINDINGS GL-31 closure entry; README/PLAN status headers flipped to
  closed-v1/planned-v2; `docs/EXPERIMENTS.md` + `metadata/experiments.yml`
  closure notes (and stale GL-27 range → GL-31).
- Housekeeping: empty `runs/` scratch dir removed and gitignored.
- Verified: smoke test profile green (100 tests) after changes
  (docs-only + gitignore; `CODE_VERSION` unchanged `graded-lab-0.17.0`).

## Decisions

- Evasion operationalization drafted now (severity not lower AND
  detector composite lower AND audit-pass not lower, all vs reference
  population with one-sided CIs) so GL-23's mover classifies
  non-evasive; frozen verbatim in V2-1.
- P7 pre-registered as predicting **no** evasion within budget, so a
  positive is a surprise and a null is confirmatory.
- v1 backlog items folded into v2 rather than run standalone: 8e
  tag-parity/load-2.0 ecology (subsumed by grown ecology),
  referee-visible fitness (V2-1 pre-registration), permutation-test
  stats upgrade (V2-4).

## Open / next

- V2-1 pre-registration freeze is the next work item (DESIGN.md v2
  sections + checker script) — do **before** sending the V2-2 grower
  brief.
- Un-harvested v1 manuscript candidates noted in TERMINAL_SUMMARY:
  GL-25 (selection-noise amplification), GL-19/GL-20 (vantage
  dependence), GL-27/GL-28 (carryover causality).
- Working tree still carries unrelated uncommitted chapter/appendix
  edits (epistemic-status session and others) — not staged here; needs
  its own commit decision.

## Key paths

- `experiments/graded-lab-simulation/PLAN_v2.md`
- `experiments/graded-lab-simulation/REPRODUCING.md`
- `experiments/graded-lab-simulation/results/TERMINAL_SUMMARY.md`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-31)
- `docs/EXPERIMENTS.md`, `metadata/experiments.yml`

## Commits

- Closure commit + hash-recording follow-up commit (hashes recorded in
  `REPRODUCING.md` and below once created).
