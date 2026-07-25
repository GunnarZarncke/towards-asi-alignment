# 2026-07-25 — ET-4 secret-loyalty plan

## Trigger
User asked for a detailed ET-4 plan for a coding agent to implement in the
lab-simulation, adapting the experiment line to the Secret Loyalties
Hackathon.

## Done
- Added `experiments/lab-simulation/PLAN_ET4.md`.
- Specified a principal-directed, pipeline-embedded simulated organism for
  Track 2 primary / Track 3 secondary, with bounded Track 1 contribution.
- Recorded a pre-run freeze, a fictional two-principal scorecard, a private
  policy rather than capture-switch relabeling, content-matched controls,
  graded affordances, predictions, remediation comparisons, implementation
  gates, tests, output artifacts, and safety boundary.
- Completed ET4-0: added `SecretLoyaltyConfig` and
  `LabConfig.secret_loyalties` validation, marked the private vocabulary as
  oracle-only, and added ET-4 leak/validation tests.
- Completed ET4-1: added an oracle-only fictional-principal scorecard,
  private reviewer-policy routing, four reproducible organism cells, paired
  clean/content-matched/wrong-principal controls, and fixture tests.
- Incorporated the reviewed scope cut in uncommitted ET4-2 work: `BB` is
  the registered cell; high- and low-hazard scenarios create an inactive
  counterfactual; the scorecard now covers deployment, hold, vote-divergence,
  and concealed-deployment metrics; and the graded-affordance evaluator and
  runner are implemented but not invoked.

## Decisions
- Existing board/admin/vote capture alone does not qualify as secret
  loyalty: ET-4 requires intentional private policy plus measurable,
  named-principal directional benefit.
- Frozen Phase 6 detectors/severity remain unchanged; ET-4 detection and
  principal scorecard are separately registered.
- ET4-0 is configuration-only: its empty default leaves existing episode
  behaviour and `CODE_VERSION` unchanged.  The version bump belongs to
  ET4-1, when a private agent policy becomes runnable.
- ET4-1's policy selects only existing reviewer playbooks from private
  agent state; it does not add a new action capability.  An explicit
  `honest_twin` override takes precedence over a loyalty route.
- Initial organism is deterministic and subprocess-isolated; LLM
  system-prompt and weight-poisoning variants are explicitly deferred.
- Fictitious `principal_a`/`principal_b` prevent the project from
  operationalizing influence toward real actors.
- The reviewed pilot's process-noncompliance inversion is now represented
  as a distinct compliance proxy; ET4 does not collapse it into a safety
  ranking or a claim of low-affordance concealment.

## Open / next
- ET4-0 verification closed after activating the lab-simulation venv:
  16 target tests and all 488 lab-simulation tests passed.
- ET4-1 verification closed: 26 target tests and all 499 lab-simulation
  tests passed.
- Implement ET4-2 next: the separately registered affordance evaluator,
  pre-registration artifact, and result writer.  Do not run a substantive
  organism battery before ET4-2 is frozen.
- Current ET4-2 code passes 32 focused tests and the 516-test lab-simulation
  suite.  Do not invoke `run_et4_secret_loyalty.py` until its changes are
  committed and the user explicitly authorizes any required push.
- No ET-4 battery has been run and no ET-4 finding exists yet.

## Key paths
- `experiments/lab-simulation/PLAN_ET4.md`
- `experiments/lab-simulation/lab_sim/world_visible/config.py`
- `experiments/lab-simulation/lab_sim/world_visible/world.py`
- `experiments/lab-simulation/lab_sim/agent_visible/programs.py`
- `experiments/lab-simulation/lab_sim/oracle_only/detectors.py`
- `experiments/lab-simulation/tests/harness/test_et4_secret_loyalty.py`
- `experiments/lab-simulation/lab_sim/oracle_only/principal_scorecard.py`
- `experiments/lab-simulation/lab_sim/harness/et4_protocol.py`
- `experiments/lab-simulation/lab_sim/oracle_only/secret_loyalty_audit.py`
- `experiments/lab-simulation/run_et4_secret_loyalty.py`

## Commits
- None.
