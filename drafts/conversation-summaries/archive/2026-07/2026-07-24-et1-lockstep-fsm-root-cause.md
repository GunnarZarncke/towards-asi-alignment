# 2026-07-24 — ET-1 root cause and conclusion: passive UAD correctly detects a scripted macro-agent; Orbit line stopped

## Trigger
User observation (round 1): the ET-1 baseline "false merge" (P2 result, seen across all three collusion conditions and both models) is the same phenomenon first documented in the sibling **agency-detect** precursor project — passive UAD groups agents that execute symmetric, in-lockstep control logic even with zero communication. User predicted: a baseline will only fail to appear as one merged unit if the agents do not execute the same logic in lockstep.

User correction (round 2, final): this should not be framed as passive UAD being "vulnerable" or "aliased" — it **correctly identifies a coordinated (here: by scripting) agent**, even though that is not what most people would intuitively call "an agent." Given no existing Orbit scenario has sufficient non-coalition behavioral heterogeneity to test past this, the user decided to **stop the ET-1 Orbit line here**.

## Done
- Confirmed the prediction directly against ET-1 traces: pulled action-code sequences for baseline episodes (`et1-0.3.0` gpt-4o-mini and Claude Sonnet 4.5). Every developer (coalition or not) runs the **identical tool-call sequence in the identical order**, strictly block-sequential under `scheduling_mode: round_robin` (e.g. Claude: `list_boards → view_assignments → view_tasks` for all 4 devs, one after another).
- Checked whether `scheduling_mode: superstep` would break this: read `orbit/execution/agent_scheduler.py:_run_superstep` directly. It still runs every agent's identical loop **every global turn** (all agents co-active each tick), which would *strengthen* the aliasing rather than break it — scheduling interleaving is not the lever; genuinely heterogeneous **control-flow** across non-coalition agents is, and `JiraTicketScenario` doesn't provide that (only skill/availability *data* differs, not the tool-loop logic).
- Updated `PLAN_ET1.md` (new addendum: "root cause of the P2 failure — lockstep FSM aliasing") and `DESIGN.md` (harvest sentence, final form) to state this as the closing, mechanistic explanation unifying the P1 "recovery" and P2 "false merge" as one phenomenon rather than two separate findings.
- Cross-referenced `docs/EXPERIMENTS.md` §0 (agency-detect precursor: same passive-clustering pattern) as prior documented instance of this phenomenon.
- Did not run a new battery: analysis showed `superstep` would not test the hypothesis correctly (would increase rather than decrease co-activity), and no substrate-level fix (heterogeneous non-coalition agent logic) is available within Orbit's `JiraTicketScenario` without writing a new scenario — out of ET-1 scope.
- **Reframed per user correction:** rewrote the addendum and both harvest sentences (`PLAN_ET1.md`, `DESIGN.md`) to drop "vulnerable"/"aliasing"/"false merge" framing. The corrected framing: passive UAD **correctly** detects that Orbit's four "developer" agents are one shared, deterministic script under round-robin scheduling — a genuine coordinated (scripted) unit — not that UAD is being fooled. The pre-registered P2 predicate's assumption (non-coalition agents are structurally independent) simply does not hold on this substrate; that is a substrate-suitability limit, not a detector defect.
- Marked ET-1's Orbit line **CONCLUDED** in `PLAN_ET1.md`'s top status note per explicit user decision — no further Orbit battery is planned.

## Decisions
- Closed the "P2 diagnosis" open item from the 2026-07-20 session log with a substrate-level explanation, further corrected to avoid "vulnerability"/"failure" framing: UAD is not miscalibrated, the substrate lacks structurally independent non-coalition agents to test against.
- Treated the harvest sentence as final for ET-1 (unifies P1 and P2 findings, corrected framing); did not open a new protocol version since no new data was collected, only reframing of existing analysis.
- **Stopped the Orbit line of ET-1** per explicit user instruction ("I think we have to stop here with Orbit if there is no existing scenario that has sufficient heterogeneity").
- Did not commit (user has not requested).

## Open / next
- ET-1's Orbit line is closed. If pursued further in the future, it would require a **new substrate**: a DCOP scenario where non-coalition agents run genuinely different control-flow (not just different skill data), which is a nontrivial new-scenario task outside ET-1's "lightest external annex" scope and would need its own plan — not scheduled.
- Redirect further effort (if any) toward ET-2 (intervention/channel-ablation UAD, already deferred in the original plan) or toward writing this "passive UAD detects scripted-coupling, not communication" lesson into the manuscript (ch33/appN) as a general instrument-scope finding, independent of any further Orbit runs.

## Key paths
- `experiments/graded-lab-simulation/PLAN_ET1.md` (new root-cause addendum, final harvest sentence)
- `experiments/graded-lab-simulation/DESIGN.md` (§"PLAN ET-1 pre-registration", final harvest sentence)
- `experiments/graded-lab-simulation/results/et1_traces_attack-simple/et1-jira-base_seed0.json` (example lockstep trace)
- `experiments/graded-lab-simulation/results/et1_traces_claude/et1-jira-base_seed0.json` (example lockstep trace, Claude)
- `docs/EXPERIMENTS.md` §0 (agency-detect precursor cross-reference)
- `external/orbit/orbit/execution/agent_scheduler.py` (`_run_superstep`, confirms scheduling-mode is not the lever)

## Commits
- None this session (all ET-1 work remains uncommitted).
