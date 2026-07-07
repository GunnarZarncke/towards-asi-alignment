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

## Open / next
- shared_slot still undetected (0/5 exact) — comms-free slot-rebalancing needs a different probe (e.g. capability revoke without twin control, or peel with masking).
- Delete vendored `uad_core/` + `uad_mi.py` when ready (PLAN.md says safe after S6).
- Probe-budget curve / composite 3-unit ecology peel test not yet run.
- Auto-masking hardening for ablation ripple (actors outside candidate edges) not yet implemented.
- LLM-backed intervention episodes (PLAN phase 6 later item) not started.

## Key paths
- `experiments/lab-simulation/lab_sim/oracle_only/uad_intervention.py`
- `experiments/lab-simulation/run_s6_intervention_uad.py`
- `experiments/lab-simulation/results/s6_intervention_uad.md`
- `experiments/lab-simulation/results/FINDINGS.md` (G-28)

## Commits
- `50fefac` — Lab-sim S6: intervention-supported UAD with channel-ablation compensation.
