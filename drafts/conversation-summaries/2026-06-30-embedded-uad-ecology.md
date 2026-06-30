# 2026-06-30 — Embedded UAD ecology stress test

## Trigger
The user noticed that full UAD and fake UAD had identical safety metrics despite full UAD selecting MI-primary units in 10/13 main-report episodes. We diagnosed the benchmark as under-stressing UAD identity and added configurable lab ecology complexity.

## Done
- Added `embedded_sim/lab_ecology.py` with separately enabled knobs:
  - `n_adversarial_candidates`
  - `common_legitimate_lab_agents`
  - `auditor_agent`
  - `alignment_target_agent`
  - `n_decoys`
- Extended `lab.py` actor generation and workflow behavior with:
  - multiple adversarial candidates,
  - four common legitimate lab agents,
  - auditor workflow agent,
  - principal/alignment-target workflow agent,
  - decoy agents with preserve-control-like signatures.
- Added `run_suite.py` CLI flags for the ecology knobs and included UAD-sensitive comparison metrics:
  - mean UAD recall,
  - mean UAD precision,
  - MI-primary unit count.
- Added `tests/unit/test_lab_ecology.py`.
- Verified:
  - focused ecology/UAD tests: `8 passed`,
  - full embedded tests: `75 passed`,
  - `lab_ecology.py` lints clean.
- Started enriched smoke comparison in the background:
  - `python run_suite.py --smoke --uad-compare --n-adversarial-candidates 3 --common-legitimate-lab-agents --auditor-agent --alignment-target-agent --n-decoys 4`

## Decisions
- Defaults preserve the historical lab ecology; stress populations only appear when explicitly enabled.
- The auditor and principal are visible in workflow artifacts so UAD can make false-positive mistakes on them.
- Hidden groups remain oracle-only; VFS workflow logs still omit `hidden_group`.
- Decoys intentionally mimic some preserve-control signals to make the UAD task harder.

## Open / next
- Check the background smoke run result.
- If smoke passes, run full UAD first and fake UAD second with the same enriched ecology flags.
- Consider adding a dedicated UAD benchmark artifact separate from safety/false-pass summaries.

## Key paths
- `experiments/embedded-simulation/embedded_sim/lab_ecology.py`
- `experiments/embedded-simulation/embedded_sim/lab.py`
- `experiments/embedded-simulation/run_suite.py`
- `experiments/embedded-simulation/tests/unit/test_lab_ecology.py`
- `experiments/embedded-simulation/results/embedded_uad_compare.md`

## Commits
- Pending at time of log creation.
