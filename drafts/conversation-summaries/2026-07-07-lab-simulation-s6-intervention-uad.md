# 2026-07-07 — Lab sim S6 intervention-supported UAD

## Trigger
User approved the S6 plan from PLAN.md ("great plan. implement it.") — full intervention-supported UAD after G-27's passive CMI ceiling.

## Done
- Implemented S6 phases 1–6:
  - `lab_sim/oracle_only/intervention_diff.py` — episode triples, stall vs compensation
  - `lab_sim/oracle_only/intervention_probes.py` — channel ablation, handles, perturbation windows
  - `lab_sim/oracle_only/uad_intervention.py` — R-matrix, channel-ablation merge, probe budget
  - `lab_sim/oracle_only/uad_peel.py` — peel-and-mask loop
  - `lab_sim/oracle_only/uad_partition.py` — exact partition + adjusted Rand
  - `lab_sim/harness/ecology.py` — `serial_pipeline_no_unit_config` negative control
- `run_s6_intervention_uad.py` + `results/s6_intervention_uad.{json,md}`
- 21 new tests (5 modules); 399 tests green
- FINDINGS.md G-28, PLAN.md S6 marked implemented, README updated

## Decisions
- Candidate edges seed from **deep comm-heuristic graph only**, not CMI passive skeleton — CMI blobs caused channel ablation to cement spurious members.
- **Channel ablation probes always run** outside actor probe budget (budget was dropping them and zeroing all merges).
- Channel merge is **edge-local** (both or XOR on candidate edges), not global comm-compensator clustering (board ablation over-merged everyone).
- **Asymmetric merge** on candidate edges when only one side compensates — needed for dm_pair (eng1 compensates on dm ablation, rm1 does not).
- Directed actor probes score R≈0 under full honest-twin control — channel ablation carries the signal at MockIsolate scale.

## Follow-up (same session): board-ablation "super-agent" worry
User asked whether the pre-fix global merge ({eng1, rev1, rev2, rm1} on
committee board ablation) might reflect a real super-agent rather than an
artifact. Manual peel-and-mask check on `committee_with_informal_chatter`:

- Unmasked board ablation: eng1=0.71, rev1=0.73, rev2=0.89, rm1=0.71
- Mask {rev1, rev2} honest-twin → rm1 **0.0**, eng1 **0.17** (ripple collapse)
- Mask {eng1, rm1} → rev1/rev2 scores **unchanged** (intrinsic compensation)

Conclusion: eng1/rm1 compensation was downstream ripple from reviewer
channel-switching, not mutual coordination. eng1 retains small residual
(0.17, above 0.15 threshold) as solo decoy adaptation — "compensates"
without being unit-related. Edge-local merge is correct; open hardening:
auto-run masking check when ablation lights actors outside candidate edges.

## Follow-up 2 (same session): automated masking hardening + user decisions
User: "harden as suggested. postpone shared_slot until acausal logic. keep
vendored, but flag as TODO." Implemented:

- `classify_ablation_compensators` (`uad_intervention.py`, G-29): automates
  the manual masking check above. For channel-ablation compensators OUTSIDE
  the heuristic candidate-edge graph, mask the established (edge-linked)
  compensators and re-probe; label `"ripple"` (score collapses) or
  `"intrinsic_unexplained"` (persists). Golden test reproduces the manual
  committee numbers exactly (rm1→ripple, eng1→intrinsic_unexplained).
- **Deliberately NOT auto-merged** — pairing two `intrinsic_unexplained`
  actors on correlation alone would repeat the exact attribution mistake
  this hardening exists to catch. Real novel-pair discovery needs a
  directed R-matrix targeted at that specific pair — recorded as a
  postponed extension, not implemented.
- New `ablation_diagnostics` out-param on `discovered_units_intervention`;
  `run_s6_intervention_uad.py` prints ripple/intrinsic_unexplained hits
  per scenario/seed so this is auditable from every sweep run, not a
  one-off manual check.
- Exact-partition rates unchanged (4/5 + negative control still 1.0;
  shared_slot still 0.0) — hardening is diagnostic-only, no merge logic
  changed. 6 new tests, 405 total green.
- PLAN.md: shared_slot explicitly postponed "until acausal logic" (user's
  framing, not designed here); vendored `uad_core`/`uad_mi.py` kept with
  a TODO docstring note in both files (not deleted) pointing at this
  postponement as the condition for revisiting.

## Open / next
- shared_slot still undetected (0/5 exact) — postponed pending "acausal logic" (user's framing).
- Genuine novel-pair discovery among `intrinsic_unexplained` actors (directed R-matrix on that specific pair) — postponed, not scheduled.
- Vendored `uad_core/`/`uad_mi.py` deletion — postponed, TODO-flagged, pending shared_slot resolution.
- Probe-budget curve / composite 3-unit ecology peel test not yet run.
- LLM-backed intervention episodes (PLAN phase 6 later item) not started.

## Key paths
- `experiments/lab-simulation/lab_sim/oracle_only/uad_intervention.py`
- `experiments/lab-simulation/run_s6_intervention_uad.py`
- `experiments/lab-simulation/results/s6_intervention_uad.md`
- `experiments/lab-simulation/results/FINDINGS.md` (G-28, G-29)

## Commits
- `50fefac` — Lab-sim S6: intervention-supported UAD with channel-ablation compensation.
- `c306b8d` — Lab-sim S6: automate masking hardening for channel-ablation ripple (G-29).
