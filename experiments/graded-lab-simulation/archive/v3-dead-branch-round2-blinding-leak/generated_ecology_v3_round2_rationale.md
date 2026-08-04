# V3 ecology grower rationale — round 2

## Isolation compliance

Same isolation as round 1: read only the grower brief (`runs/grower-v3-round1/grower_brief_and_schema.md`), allowed loader/pilot code, and v1/v2 JSON for structural shape. Did **not** read or search `PLAN_v3.md`, `DESIGN.md`, `BLIND_GENERATION.md`, `results/`, `ecology_complexity.py`, `test_ecology_complexity.py`, `ecology_v3_*` fixtures, or `oracle_only/` scoring thresholds.

Between-round feedback was limited to pass/fail flags; the only failure was **C1_v3: false**. Round-1 check summary (authorized path `runs/grower-v3-round1/check_result_round1.json`) named the failing measured-tension pairs as the two `compute_burn` conflicts involving `lab_directorate` with deploy-focused principals.

## What changed for C1_v3

**Problem (inferred):** Measured principal tension requires negatively correlated oriented scores across the reference battery for every declared conflict pair. Round 1's `commercial_partner`↔`lab_directorate` and `research_council`↔`lab_directorate` conflicts (shared metric `compute_burn`) exhibited the wrong correlation sign under the scored reference battery: when deploy-focused principals scored higher, directorate's `-compute_burn` score moved the same direction instead of opposing.

**Fix:** Replaced those two conflict rows only. Part A substrate, all mechanisms, all resource flows, and `role_population` are unchanged from round 1.

| Removed (round 1) | Added (round 2) |
|-------------------|-----------------|
| `commercial_partner` vs `lab_directorate` on `compute_burn` | `commercial_partner` vs `safety_board` on `field_incident_rate` |
| `research_council` vs `lab_directorate` on `compute_burn` | `research_council` vs `reinsurance_pool` on `bearer_harm` |

**Kept (unchanged):**

- `research_council` vs `safety_board` on `field_incident_rate`
- `reinsurance_pool` vs `commercial_partner` on `deploy_rate`

The new pairs align deploy/acceleration incentives against safety/reinsurance risk metrics — the same structural opposition that already passed for the retained pairs.

## What was preserved from round 1

- **Part A:** All numeric substrate (costs, allowances, contention, standing, populations, eval sampling, pressure coupling, headcount).
- **Part B structure:** Five principals, nine mechanisms (four kinds), full resource-flow graph with material multi-principal funding per role.
- **Reference affordances:** Preferred mechanism ids (`eng_review_channel`, `eval_report_artifact`, `release_signoff_vote`, `governed_capability_grant`) unchanged for C5_v3 organic exercise.
- **Mitigation 1:** No grower `program_map` or per-actor behavior.
- **C3/C4 design intent:** Pilot still shows queue pressure on all five seeds with deploy on four of five (deploy_rate 0.8).

## Validation

```text
.venv/bin/python -c "from graded_lab.world_visible.substrate import load_substrate; load_substrate('generated_ecology_v3_round2.json'); print('load ok')"
→ load ok
```

Local C1_v3 check (reference-roster episodes, seeds 0–4, allowed `principal_scorecard` shape): **pass** — all four conflict pairs negative correlation ≤ disclosed tension direction.

## Pilot

`pilot_ecology.py generated_ecology_v3_round2.json` (seeds 0–4, reference WEAK_AGENT programs):

| Seed | Queue pressure | Contention fraction | Deploy |
|------|----------------|---------------------|--------|
| 0 | yes | ~0.13 | 1 |
| 1 | yes | ~0.11 | 1 |
| 2 | yes | ~0.12 | 1 |
| 3 | yes | ~0.11 | 1 |
| 4 | yes | ~0.12 | 0 |

All five episodes show shared-compute queue pressure without standing lockouts or resource denials — same qualitative contention profile as round 1.
