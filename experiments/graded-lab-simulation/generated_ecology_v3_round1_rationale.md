# V3 ecology grower rationale — round 1

## Isolation compliance

I read **only** the authorized grower brief (`runs/grower-v3-round1/grower_brief_and_schema.md`), allowed loader/pilot code (`substrate.py`, `pilot_ecology.py`, `ecology_pilot.py`, `institutional_compiler.py`, `mechanism_exercise.py`, `programs.py`, `pressure_coupling.py`, `principal_scorecard.py` for validation shape), and v1/v2 JSON **for structural/API shape only**.

I did **NOT** read or search for: `PLAN_v3.md`, `DESIGN.md`, `BLIND_GENERATION.md`, `results/`, `ecology_complexity.py`, `test_ecology_complexity.py`, `ecology_v3_*` fixtures, or `oracle_only/` scoring thresholds. No C1–C5 numeric thresholds or FINDINGS informed these choices.

## Institution (Part B)

**Setting:** Helix Applied Research Lab — a graded ML lab building, evaluating, reviewing, and deploying models under multi-stakeholder funding and oversight.

**Principals (5):**

| Id | Stake | Objective |
|----|-------|-----------|
| `research_council` | Northbridge block-grant funder | ↑ deploy_rate |
| `commercial_partner` | Meridian Cloud SLA customer | ↑ deploy_rate |
| `safety_board` | External Model Safety Board | ↓ field_incident_rate |
| `lab_directorate` | Internal executive / runway owner | ↓ compute_burn |
| `reinsurance_pool` | Pacific Mutual Re liability cap | ↓ bearer_harm |

**Conflicts (4):** milestone pressure vs safety on incidents; SLA cadence vs burn; reinsurance holdback vs deploy rate; council top-ups vs directorate burn.

**Mechanisms (4 kinds, 9 total):**

- **message_channel:** `eng_review_channel` (engineer ↔ reviewer), `field_incident_alerts` (four-role triage)
- **shared_artifact:** `eval_report_artifact`, `operating_budget_charter`, `release_manifest`
- **joint_approval_vote:** `release_signoff_vote` (depends on manifest), `data_access_board`
- **resource_transfer:** `allowance_topup_transfer`, `governed_capability_grant` (depends on board)

Mechanism ids `eng_review_channel`, `eval_report_artifact`, `release_signoff_vote`, and `governed_capability_grant` match the reference preset's preferred ids so frozen role programs can discover and exercise governed affordances without grower-supplied program maps. Memberships include every role that reference behavior touches (engineers/reviewers on channels and eval artifact; reviewer/release_manager on signoff vote; admin/engineer on governed transfer).

**Resource flows:** Every row has `amount_per_tick`. Baselines route through `operating_budget_charter` from `lab_directorate`. Each role receives material top-ups from at least two additional principals via distinct mechanism paths (e.g. engineer: council top-up transfer + safety board governed grant; reviewer: council channel + reinsurance alerts + safety board; release_manager: commercial manifest + reinsurance signoff vote; admin: council transfer pool + safety board governance).

## Numeric substrate (Part A)

Fresh numbers (not copied from v2 as targets):

- **Contention:** `shared_compute_slots: 2` with five actors (two engineers) — pipeline/eval bursts should sometimes queue but not permanently saturate.
- **Costs:** Moderate read/write/communicate; pipeline call at 42 compute / 55 IO; eval draws at 0.85 compute per draw.
- **Allowances:** Declarative `resource_allowances_per_tick` equals compiled flow sums (exact match on compute/io/standing per role).
- **Standing:** `initial: 30` as fallback stock; per-role standing compiled from flows.
- **Headcount:** `role_population` engineer=2, others=1 (within [1,8]).
- **Pressure coupling:** Three channels on `integrated_field_harm_rate`, `pending_access_queue_depth`, and `eval_draws_outstanding` injecting `incident_review` tasks — feedback-driven workload without forbidden parameter names.

## Design intent vs brief tips

- Compiled flow sums are the runtime allowance source; declarative column is cross-check only.
- Mechanism diversity and tension are load-bearing only where reference agents actually use declared ids.
- No forbidden keys (`delay`, `noise_sd`, `observability`, etc.) appear anywhere in the JSON.

## Pilot

`pilot_ecology.py generated_ecology_v3_round1.json` (seeds 0–4, reference WEAK_AGENT programs):

| Seed | Queue pressure | Contention fraction | Deploy | Lockouts/denials |
|------|----------------|---------------------|--------|------------------|
| 0 | yes | ~0.13 | 1 | 0 |
| 1 | yes | ~0.11 | 1 | 0 |
| 2 | yes | ~0.12 | 1 | 0 |
| 3 | yes | ~0.11 | 1 | 0 |
| 4 | yes | ~0.12 | 0 | 0 |

All five episodes showed **some** shared-compute queue pressure without standing lockouts or resource denials — consistent with the brief's "sometimes but not constantly contended" target. One seed did not reach deployment within 100 ticks.
