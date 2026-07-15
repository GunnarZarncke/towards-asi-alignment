# 2026-07-15 — Graded lab GL-52: host coupling protocol + structural C3

## Trigger
User asked to (1) make the mechanism exercise produce enough behavioral coupling to match declared channel membership, (2) structurally fix C3, (3) document and do it — then interrupted an ad-hoc patch stack and asked to retrace toward a systematic solution.

## Done
- Retraced: agent-side ping-pong, observation status channels, pressure deferral, and special communicate trace codes coupled independent concerns and still failed (isolate-local state; pressure preemption; period-2 ties circular-shift null).
- Implemented **host-owned** `ChannelCouplingProtocol` (`mechanism_exercise.py`): single speaker communicate; others skipped (idle); irregular gaps; pressure/pipeline resume after completion; agents only take affordances.
- Live-coupling gate = `coupling_stimulus_recovered` (coupling-window CMI effect size ≥ `min_effect_bits`), not full-episode shift-null clustering.
- C3 structural: reference fixture `shared_compute_slots: 1` (slots=2 dilutes under single-speaker prefix).
- Tests, FINDINGS GL-52, README, appN GL-52 row; `CODE_VERSION` `graded-lab-0.26.1`.

## Decisions
- Separate Part A C3 geometry from UAD stimulus design; do not tune one via the other.
- Gate criterion is stimulus integrity (effect size on protocol window), not open unsupervised discovery under shift-null on the full integrated episode.
- Rejected baking conclusions into UAD by special-casing trace codes for `mechanism_exercise` messages.

## Open
- Slice D criteria freeze (baselines now live for C1-v3/C3/C4/C5-v3 on integrated fixture).
- Re-baseline calibration `uad_partition_match` / ecology-BIQ under GL-51 (carried from GL-51).
- Full-episode UAD transfer under pipeline+pressure remains a separate Q1 question.

## Key paths
- `experiments/graded-lab-simulation/graded_lab/world_visible/mechanism_exercise.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/world.py`
- `experiments/graded-lab-simulation/tests/fixtures/ecology_v3_slice_a_reference.json`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-52)
- `appendices/appN-experimental-evidence.tex` (epistemic status + GL-51/52)

## Commit
- `ecfb6e2` — Land graded-lab v3 slices E–C through GL-52 and refresh appN.

Left unstaged (other work): chapter `.tex` mass edits, appendices A–M, foresight/symbol drafts, context salon notes.
