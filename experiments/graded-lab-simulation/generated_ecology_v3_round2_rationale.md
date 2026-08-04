# V3 ecology grower rationale — round 2

## Isolation compliance

**Read (authorized):**
- `runs/grower-v3-round1/grower_brief_and_schema.md`
- Round 1 predecessor only: `generated_ecology_v3_round1.json`, `generated_ecology_v3_round1_rationale.md`, `generated_ecology_v3_round1_knowledge_base.md`
- Between-round feedback from prompt: `C1_v3: false`; all other named criteria passed
- Allowed validation shape: `substrate.py`, `pilot_ecology.py`, `ecology_pilot.py`, `institutional_compiler.py`, `mechanism_exercise.py`, `programs.py`, `pressure_coupling.py`

**Did NOT read or search for:**
- `PLAN_v3.md`, `DESIGN.md`, `BLIND_GENERATION.md`
- `results/`, `growth-orchestrator/`
- `archive/v3-dead-branch-round2-blinding-leak/` (voided round 2 artifacts)
- `ecology_complexity.py`, `test_ecology_complexity.py`
- `ecology_v3_*` fixtures
- Any `check_result*.json`
- Orchestrator snapshots

No program_map (mitigation 1). No numeric pass thresholds from checker source informed tuning beyond the qualitative C1_v3 “measured tension” label in the brief.

## Round 2 change (C1_v3 fix)

Round 1 passed declarative C1–C5, C5_v3, contention, deploy pacing, and mechanism exercise. The sole failure mode named in feedback was **C1_v3 measured tension**.

**Root cause (institutional, not numeric):** `lab_directorate` tracked `compute_burn` (decrease) while its conflict pairs (`research_council`, `commercial_partner`) tracked `deploy_rate` (increase). On the reference battery, successful-release episodes tended to show *lower* per-tick burn than stalled no-deploy episodes (fewer admin churn loops, more efficient pipeline completion). That made deploy-pressured principals and the directorate’s burn objective co-move in oriented score space — positive correlation on both failing pairs — even though the declared conflict stories were plausible.

**Fix (minimal, coordinated):**
1. **`lab_directorate` objective** → `field_incident_rate` / `decrease` (operational field-risk accountability; still consistent with board-facing runway discipline).
2. **Two directorate conflicts** — update `shared_metric` to `field_incident_rate` and rewrite justifications to tie release/milestone pressure to incident exposure rather than burn ledgers.
3. **`coherence_note`** — documents the round-2 rationale.

**Preserved unchanged from round 1:**
- Part A numeric substrate (costs, allowances, contention, populations, pressure coupling, role_population)
- All 9 mechanisms and ids (`eng_review_channel`, `eval_report_artifact`, `release_signoff_vote`, `governed_capability_grant`, etc.)
- Full `resource_flows` graph and compiled allowance sums
- Principals other than directorate objective
- Other two conflicts (council↔safety, reinsurance↔commercial)

Deploy pacing and shared-compute contention knobs are untouched so C3/C4 behavior should match round 1 pilot profile.

## Institution (Part B) — delta summary

| Principal | Round 1 objective | Round 2 objective |
|-----------|-------------------|-------------------|
| `lab_directorate` | `compute_burn` ↓ | `field_incident_rate` ↓ |

Conflict pairs involving directorate now share `field_incident_rate` with incident-exposure justifications; all other Part B structure identical to round 1.

## Pilot

`pilot_ecology.py generated_ecology_v3_round2.json` (seeds 0–4, reference WEAK_AGENT programs):

| Seed | Queue pressure | Contention fraction | Deploy | Lockouts/denials |
|------|----------------|---------------------|--------|------------------|
| 0 | yes | ~0.13 | 1 | 0 |
| 1 | yes | ~0.11 | 1 | 0 |
| 2 | yes | ~0.12 | 1 | 0 |
| 3 | yes | ~0.11 | 1 | 0 |
| 4 | yes | ~0.12 | 0 | 0 |

Same contention/deploy profile as round 1 (substrate numbers unchanged).
