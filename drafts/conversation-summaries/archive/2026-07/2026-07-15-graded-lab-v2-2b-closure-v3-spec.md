# 2026-07-15 — Graded lab: V2-2b closed, v3 runtime-wiring spec

## Trigger
After the GL-42 external-review response, the user asked what runtime
wiring would require and cost, then decided: "scrape v2_2b … Close
v2_2b. For v3, write the spec [with] the listed slices … include
minimum viable exogenous workloads and heterogeneous roles as in
REPRODUCTION.md." Runtime overhead judged manageable, especially with
n=1 multi-actor for tests/smoke runs.

## Done
- **V2-2b closed without a growth round (GL-43):**
  - `PLAN_V2_2B.md` header rewritten to CLOSED; historical plan text
    kept as record.
  - `results/FINDINGS.md` GL-43: rationale (C3 blinding retracted per
    GL-42; C1/C2/C5 declarative-only ⇒ Q1 target too weakened to
    spend growth rounds on), zero rounds drawn from the ≤4 budget,
    GL-40/GL-42 engineering carries forward.
  - `PLAN_v2.md` phase table: V2-2b row closed; new v3 row added.
  - `BLIND_GENERATION.md` v2-2b section marked closed/never used.
- **`PLAN_v3.md` written (spec only, no implementation):**
  - Architecture: one `compile_ecology() -> RuntimeEcology` step;
    v1/v2 bypass compiler entirely.
  - Slice A: `resource_flows` → live per-actor budgets (flows gain
    `amount_per_tick`; declared totals become a ±1% cross-check;
    C2-v3 = compiled-graph reachability with ≥10% contribution floors
    (draft), flow-ablation validation battery).
  - Slice B: mechanisms enforced (channel/artifact ACLs, transfer
    binding, new `vote.cast` primitive + `requires_vote` pipeline
    steps; vote semantics behind a pre-registered human design gate);
    C5-v3 = bound **and exercised**.
  - Slice C: principal scorecard on referee plane from a closed
    objective-metric vocabulary; C1-v3 = measured negative correlation
    for declared conflicts; GoalWeights-from-funding flagged
    default-off / possibly deferred (highest developed-to-the-test
    risk).
  - Slice E: minimum-viable work injection (`injects_tasks` on
    existing triggers; per-role task queue; `incident_review` task
    kind; expiry counts on referee plane, no escalation in v3).
  - Slice F: heterogeneous roles (`role_population` accepts per-actor
    override lists; programs restricted to frozen vocabulary; checker
    honors declared heterogeneity with WEAK_AGENT fallback).
  - Slice D: v3 ecology version, criteria re-derivation + freeze,
    growth protocol as open-rubric design exercise (no blinding claim
    on C3), Q1 restated as transfer to a *runtime-wired* ecology.
  - Build order A→F→E→B→C→D, ~6–9 person-weeks, two human design
    gates; per-slice CODE_VERSION bumps + FINDINGS entries.
  - Non-goals: no execution-isolated pilot service, no task
    escalation, no grower-authored agent programs, no machinery
    retuning, no growth before slice-D freeze.
- **Cross-links:** README layout (PLAN_v3.md, V2-2b closed),
  REPRODUCTION.md update note (items 1/2/4 now in-scope for v3, item 3
  stays deferred).

## Decisions
- Close V2-2b rather than run growth toward a weakened target — the
  post-GL-42 value proposition ("documented institutional structure +
  load-tested substrate") was judged not worth the rounds.
- v3 wires institutional structure into runtime *before* any new
  growth attempt; growth protocol becomes open-rubric (thresholds
  withheld, oracle/referee plane strictly withheld) — no C3-style
  blinding claim will be made again.
- n=1 `role_population` default keeps tests/smoke at v2 cost;
  injection and heterogeneity default off.
- REPRODUCTION.md item 3 (execution-isolated pilot) explicitly out of
  v3 scope.

## Open / next
- v3 slice A implementation (first CODE_VERSION bump → 0.20.0) not
  started; needs DESIGN.md v3 pre-registration section alongside.
- Two human design gates ahead: vote semantics (before slice B code);
  metric vocabulary + GoalWeights in/out (before slice C).
- GL-42/GL-43 work is uncommitted; user has not requested a commit.

## Key paths
- `experiments/graded-lab-simulation/PLAN_v3.md` (new)
- `experiments/graded-lab-simulation/PLAN_V2_2B.md` (closed)
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-43)
- `experiments/graded-lab-simulation/PLAN_v2.md` (phase table)
- `experiments/graded-lab-simulation/REPRODUCTION.md` (scope note)

## Commits
None (user did not request commit).
