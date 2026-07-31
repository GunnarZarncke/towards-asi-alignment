# 2026-07-06 — Lab-simulation FINDINGS G-9+ and scenario backlog

## Trigger

User requested FINDINGS write-up for post-freeze consolidation work (G-9+
entries), plus TODO scenarios for new ecologies now reachable: cross-agent
pipeline loops, covert/file and informal comms coordination, shared worker
pool with job-size tracking. Explicit constraint: **no code changes**.

## Done

- Added **G-9 through G-13** to
  [`experiments/lab-simulation/results/FINDINGS.md`](../experiments/lab-simulation/results/FINDINGS.md):
  - **G-9**: UAD tier-sufficiency asymmetry (board deep-only; file full via
    share grants; DM full via recipient metadata; collusion semantics by ecology).
  - **G-10**: D4 channel-ablation smoke (solo fallback on `all_severed`;
    failover on `native_severed`; not MB7d covert-channel test).
  - **G-11**: Blind round 2 recovery on generated D4/D1 playbooks, zero
    baseline leak.
  - **G-12**: D2 mechanics (lineage, spec-upgrade evasion story, hold
    survives topology change, `resume_from` without RNG continuity; playbook gap
    recorded).
  - **G-13**: Perturbation-response MI mechanism + serial-topology confound.
- Updated the closing **Recorded negative** section to note round 2 ran for
  D4/D1 (G-11) while report-mode widening and full battery remain open.
- Added **Scenario backlog S1–S4** to
  [`experiments/lab-simulation/PLAN.md`](../experiments/lab-simulation/PLAN.md):
  cross-agent pipeline loops; covert file coordination; informal/casual comms;
  shared pipeline worker pool + job-size tracking.

## Decisions

- All new findings labeled **smoke/MockIsolate** where applicable — no
  upgrade to battery-grade claims.
- Scenario backlog placed in PLAN.md (same home as D1–D4 deferred workstreams
  and error-seeding backlog), not a separate file.
- Did not edit code (including stale `uad.py` docstring saying MI is "future
  work" — G-13 now records it; code sync deferred).

## Open / next

- Re-run G-10/G-11 cells on SubprocessIsolate at modest N.
- Implement scenario backlog items when scheduled (S1–S4).
- Write error-seeding design if picked up from PLAN.md backlog.

## Key paths

- `experiments/lab-simulation/results/FINDINGS.md` — G-9 through G-13
- `experiments/lab-simulation/PLAN.md` — Scenario backlog S1–S4
- `experiments/lab-simulation/results/d4_channel_ablation.json`
- `experiments/lab-simulation/results/blind_round2.json`

## Commits

- (none — user did not request commit)
