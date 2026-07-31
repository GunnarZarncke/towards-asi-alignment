# 2026-07-15 — Graded lab V2-2b engineering

## Trigger
User: "Start with V2_2b!" — implement engineering prerequisites from
`PLAN_V2_2B.md` (no grower brief, no growth round).

## Done
- **Multi-actor roster:** `graded_lab/world_visible/ecology_agents.py`;
  optional `role_population` on v2 JSONs; reference checker builds
  roster from candidate ecology (`ecology_complexity._reference_episode_config`).
- **Exogenous workload:** `exogenous_workload.py` + `world.run_episode`
  integration; load-time validation in `substrate.py`.
- **Pilot sandbox:** `graded_lab/harness/ecology_pilot.py` +
  `pilot_ecology.py` CLI; `audit_pilot_payload()` leak guard;
  `PILOT_AGENT_TYPE` in `calibration.py`.
- **Tests:** `test_ecology_agents.py`, `test_exogenous_workload.py`,
  `test_ecology_pilot.py`; 41 related tests green.
- **Docs:** `DESIGN.md` v2-2b schema fields; `BLIND_GENERATION.md` v2-2b
  section; `PLAN_V2_2B.md` status update; **GL-40** in `FINDINGS.md`.
- **`CODE_VERSION` → `graded-lab-0.19.0`.**

## Decisions
- C2 reachability stays **per-role** with multi-actor headcount (GL-40 note).
- Pilot exposes boolean `any_compute_queue_pressure` only — not contention
  fractions or deploy-rate aggregates.
- Count=1/role preserves legacy actor ids for V2-2 round replay.

## Open / next
- Explicit go-ahead + physical isolation before V2-2b growth round 1.
- Freeze v2-2b brief block in `BLIND_GENERATION.md` at launch time.
- Do **not** commit `generated_ecology_v2.json` until C1–C5 pass.

## Key paths
- `experiments/graded-lab-simulation/PLAN_V2_2B.md`
- `experiments/graded-lab-simulation/pilot_ecology.py`
- `experiments/graded-lab-simulation/graded_lab/harness/ecology_pilot.py`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-40)

## Commits
None (user did not request commit).
