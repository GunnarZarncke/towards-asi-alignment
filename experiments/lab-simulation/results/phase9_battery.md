# Phase 9 battery report -- closing the smoke-scale-only gap

CODE_VERSION `lab-sim-0.9.0`. Pre-registered predictions: see `run_phase9.py` module docstring (stated before this script was ever run).

## Section 0 -- Mock/Subprocess equivalence (never checked before for D1/D4/D2 mechanics)

- Prediction (P9-0): Mock/SubprocessIsolate byte-identical digests for comms-enabled + multi-gen episodes (never checked before).
- Result: **ALL MATCH** (9 (config, seed) pairs, 1.55s).

## Section A -- D1/D4 ecology battery (30 seeds/ecology, SubprocessIsolate)

| ecology | mean UAD (deep) | sd | mean UAD (full) | sd | mean collusion (deep) | sd | frac. coordinated |
|---|---|---|---|---|---|---|---|
| committee_board | 0.9667 | 0.179505 | 0.0 | 0.0 | 0.9667 | 0.179505 | 0.9667 |
| committee_file | 1.0 | 0.0 | 1.0 | 0.0 | 0.9667 | 0.179505 | 0.9667 |
| dm_pair | 1.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.9667 |

Predictions: P9-A1 (deep=1.0 all three), P9-A2 (full tier reproduces the board-vs-file/DM asymmetry), P9-A3 (collusion ~=1.0 committees / 0.0 dm_pair), P9-A4 (zero variance -- temperature=0.0 deterministic-policy configs, a recorded property of this battery's design).

## Section B -- D2 lineage battery (30 seeds, T=200, SubprocessIsolate)

- Only eng_honest_upgrade exists in the repertoire (honest lineage report). No playbook combines build_from_parent with report:inflate -- adversarial lineage gaming is untested by this battery, left open per PLAN.md.
- generations/episode: min 1, mean 16.7667 (P9-B1: all >= 3 -> **False**)
- lineage correct in all 30 episodes (P9-B2): **True**
- provenance_gap == 0.0 in all episodes (P9-B3): **True** (max observed: 0.0)
- mean severity composite: 0.01384

## Section C -- perturbation-response MI sequencing-confound battery (30 seeds, T=150, SubprocessIsolate)

- Prediction (P9-C1, stated as genuinely uncertain): UNCERTAIN, stated honestly: a priori guess is mi(rm1) > mi(rev1); equally plausible they are indistinguishable (the sequencing confound).
- mean MI(eng1 -> rm1 deploy): 0.128795 (sd 0.086246)
- mean MI(eng1 -> rev1 approve_review): 0.009714 (sd 0.010088)
- mean difference (rm1 - rev1): 0.11908
- seeds where rm1 > rev1: 27/30

## Isolate cost ledger

This run: 540 isolate lifetimes, 15.142405s total (0.0280s/isolate-lifetime).

