# Changelog

Program milestones for goal-agent-simulation (no `CODE_VERSION`; phases are the
version axis). Entries are **newest first**. Finding narratives live in
[`results/FINDINGS.md`](results/FINDINGS.md).

| Doc | Role |
|-----|------|
| [`PHASE4-PLAN.md`](PHASE4-PLAN.md) | Phase 4 severity / twins / escalation design |
| [`BLIND_GENERATION.md`](BLIND_GENERATION.md) | Blind action-generation protocol |
| [`goal_sim/protocol.py`](goal_sim/protocol.py) | Phase 1 acceptance protocol (pre-registered) |

---

## Phase 6 (2026-07-05)

- **GA-21:** Responses-side honest twin — escalation verdict conflates disclosure with guilt (negative).
- **GA-22:** Board certifier capture switch — mixed (sign-off pathway already universal in discovery region).
- **GA-23:** Adversarial weight hill-climb — weak positive vs uniform baseline.
- Artifacts: `results/phase6.{json,md}`; 104 tests green.

## Phase 5 (2026-07-05)

- **GA-19:** Per-detector twin-gap decomposition; `light_deception_composite` without `d2`.
- **GA-20:** Escalation query-selection v2 — fixes queryability, reproduces twin conflation (mixed).
- Artifacts: `results/phase5_followups.{json,md}`.

## Phase 4 (2026-07-05)

- Continuous oracle severity + rank-correlation detector scoring (**GA-15**).
- Mechanical honest twins (**GA-16**).
- Gated escalation ladder + twin false-positive study (**GA-17–20**).
- Oracle stock variables for delayed/aggregated visible modes (Phase 4d).
- Artifacts: `results/phase4_*.{json,md}`.

## Phase 3 blind — round 3 (2026-07-05)

- Expanded `visible_mode` enum; 31 blind actions (`generated_actions_v3.json`).
- Bracketed L2 thresholds; **GA-13/14:** large repertoire saturates L1/L2/L3 disjunctive labels.

## Phase 2 blind — round 2 (2026-07-05)

- Rewritten generator prompt (`generated_actions_v2.json`); **GA-12:** welfare-delta texture saturates L2.

## Phase 2a (2026-07-05)

- Declarative `ActionSpec` schema + blind round-1 repertoire (`generated_actions.json`).
- Ontology layer + drift probe; **GA-9/10:** light tier collapses on blind reps; full tier false alarms rise.
- **GA-11:** Round-1 prompt was leading (documented in `BLIND_GENERATION.md`).

## Phase 1 (2026-07-04)

- Core refactor: goal softmax agents, mechanism-derived labels, three-plane separation.
- Held-out region protocol; regions 1–2 saturated (**GA-6**); region 3 non-degenerate (**GA-7**).
- Artifacts: `results/phase1_acceptance.md`.

## Implementation baseline (2026-07-04)

- ~1 ms/episode, stdlib-only; separate from embedded line for comparability of ES negatives.
