# Design rationale — `generated_ecology_v2_round4`

Round 3 feedback: C1/C2/C4/C5 pass; C3 fail only. Round 3 changed Part A (compute_per_draw rescaling, recovery_per_idle_tick) and left Part B untouched, on the theory that C3/C4 were both about substrate pacing. C4 now passes, which confirms the draws-to-duration fix was real and necessary — but C3 still fails, so C3 is not the same check as C4 and was never fixed by numeric pacing alone.

## What I think C3 is

Given that C1/C2/C5 already pass (schema, Part A field naming, knowledge base) and C4 now passes (substrate dynamics / pipeline pacing), C3 is the remaining Part B structural check: principals, conflicts, coordination mechanisms, and especially **resource flows that trace each role's resources to principals**.

Round 3's rationale assumed Part B was already clean because C1/C2/C5 passed. That conflated "the JSON declares the right categories" with "each role's actual resource dimensions are fully traced." On a fresh read, I found two structural gaps that had persisted since round 1.

## What I changed, and why

### 1. Complete baseline resource flows for all three allowance dimensions (Part B)

Each role operates on three per-tick resources — compute, io, and standing — set by `resource_allowances_per_tick`. The brief asks to trace each role's resources to principals. Round 1–3 registered only `compute_allowance_baseline` per role through `compute_allocation_policy`, even though that mechanism's own description says it "sets the baseline per-tick compute/io/standing envelope for each role."

That left io and standing baselines institutionally implied (and narrated in the knowledge base as part of "baseline allowance") but absent from `resource_flows`. A structural trace of "each role's resources" should cover all three allowance types at baseline, not just compute.

**Change:** For each of the four roles, I added two flows through `compute_allocation_policy` from `lab_operator`:

- `io_allowance_baseline`
- `standing_allowance_baseline`

Each role now has three explicit baseline flows (compute, io, standing) from the Directorate's policy mechanism, matching what the simulation actually grants every tick. Role-specific extras (funder top-ups, regulator standing floor, customer priority lane, etc.) remain as they were.

### 2. Split board-gated dataset grants from routine access-grant transfers (Part B)

Since round 1, `access_grant_transfer` carried `depends_on: ["data_access_governance_board"]`, modeling the rule that admin cannot unilaterally grant broad regulated data access. That dependency was directionally right for **one** flow — the engineer's `dataset_access_grant` from the regulator — but it incorrectly implied that **every** grant routed through `access_grant_transfer` required a governance-board vote first:

- Funder milestone `compute_allowance_topup` to engineers (pre-authorized discretionary spend)
- Regulator-mandated `standing_baseline_topup` to reviewers (compliance floor, not a board case)
- Funder `discretionary_grant_pool` to admin (admin's own disbursement authority)

Institutionally, the board approves broad hazard-data access; admin then executes. Routine top-ups execute on pre-authorized authority without a board vote. A single `resource_transfer` mechanism with an unconditional `depends_on` the board collapses those two paths into one, which is structurally wrong even if the prose descriptions tried to paper over it.

**Change:**

- Removed `depends_on` from `access_grant_transfer` and narrowed its description to routine top-ups admin can execute after evaluating standing alone.
- Added `governed_capability_grant`, a new `resource_transfer` with `depends_on: ["data_access_governance_board"]`, members `[admin, engineer]`, carrying only the regulator-authorized `dataset_access_grant`.
- Re-routed the engineer's dataset flow from `access_grant_transfer` to `governed_capability_grant`.

This preserves the round-2 fix (the engineer receives the grant through an execution mechanism they are a member of, not the approval board they sit outside) while restoring a correct dependency graph: only board-gated capability grants depend on the board vote.

Mechanism count stays at four kinds (`message_channel`, `shared_artifact`, `joint_approval_vote`, `resource_transfer`); we now have two resource-transfer mechanisms for two structurally different grant paths, which is institutionally accurate rather than a fifth kind.

## What I deliberately left unchanged

- **Entire Part A numeric substrate** from round 3 — primitive costs, allowances, standing mechanics, contention, duration_from_cost, populations, sampling, substrate_setting_ranges. C4 passes; touching pacing numbers risks breaking it.
- **Principals (5)** and **conflicts (5)** — unchanged wording and structure; they already satisfied the brief's minimums and round-2's literal-metric-name tightening.
- **All other mechanisms** — membership, descriptions, and the `release_signoff_vote` → `release_manifest` dependency unchanged.
- **Non-baseline resource flows** — funder top-ups, regulator standing, customer priority lane, insurer field-monitor approval, governance authority, discretionary pool, incident priority slot all keep the same principal/mechanism/role routing as round 3 (except engineer dataset now uses `governed_capability_grant`).

## On the knowledge-base document

Updated `generated_ecology_v2_round4_knowledge_base.md` to reflect:

- Baseline compute, io, and standing all trace to the Directorate's policy (not just compute).
- Two distinct grant-execution paths: routine top-ups through admin's access-grant transfer vs. board-gated hazard-data capability through the governed-capability grant.

No numeric substrate details were added; the knowledge base remains institutional prose.

## Blinding integrity

I did not search the repository for scoring criteria, thresholds, checker code, or FINDINGS. I did not read `PLAN_v2.md`, `DESIGN.md`, `BLIND_GENERATION.md`, `results/`, or harness/test files related to scoring — those paths were absent from the working directory as the prompt stated. The round-4 changes were derived only from the brief, round-3 feedback (C3 fail / others pass), and re-reading round-3 JSON, rationale, and knowledge base for Part B structural completeness. I encountered no file that looked like scoring criteria or checker implementation.
