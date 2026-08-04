# 2026-07-15 — Graded lab PLAN_v3 slice B completion

## Trigger
User: "finish slice B" — close the four-item build-order checklist after slices F and E.

## Done
- `mechanism_exercise.py`: governed primitive builder, C5-v3 check, UAD live-coupling ground truth.
- `governed_*` programs + `V3_MECHANISM_REFERENCE` agent type.
- Affordable set + episode loop surface governed channel/artifact/transfer/vote primitives.
- `ecology_complexity.py`: mechanism-reference battery + `c5_v3_mechanisms_exercised` on v3 check.
- `tests/test_slice_b_completion.py` (4 tests): exercise gate, C5-v3, UAD coupling, ACL overhead.
- `CODE_VERSION` → `graded-lab-0.24.0`; FINDINGS GL-48; PLAN_v3 + DESIGN.md updated.

## Decisions
- Governed channel communicate repeats each tick (not one-shot) so passive UAD co-activity can recover the eng–rev channel unit.
- C3/C4 reference battery unchanged (WEAK_AGENT); C5-v3 uses separate mechanism-reference episodes.
- ACL overhead gate: noop v1 vs v3 episode wall-clock, must be < 10%.

## Open / next
- Slice C (principal scorecard + measured tension).
- Commit when user asks.

## Key paths
- `experiments/graded-lab-simulation/graded_lab/world_visible/mechanism_exercise.py`
- `experiments/graded-lab-simulation/tests/test_slice_b_completion.py`
- `experiments/graded-lab-simulation/PLAN_v3.md` § Slice B

## Commits
- (none yet — uncommitted)
