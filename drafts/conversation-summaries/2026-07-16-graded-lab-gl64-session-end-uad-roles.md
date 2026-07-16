# 2026-07-16 — Graded lab session end: GL-60–63 commit + UAD roles direction

## Trigger
User asked to end the session and commit graded-lab changes after agreeing on
preferred shape for replacing `ChannelCouplingProtocol` with supplementary
in-ecology comms/scribe roles (implementer-only fixture, not grower-visible).

## Done
- Committed **GL-60–GL-63** graded-lab line (`graded-lab-0.35.1`):
  - GL-60: supplementary detector fixtures + gate (`machinery_transfer_verified`)
  - GL-61: human decision — Part B retarget path (docs)
  - GL-62: ecology-governed Part B presets when host merge off; C5 without coupling
  - GL-63: split detector pre-registration (`honest_reference_sparse_detectors` vs
    `machinery_transfer_verified`; retired `transfer_failure_risk`)
- C3/C4 @ T=200 validated on integrated reference (prior session).

## Decisions
- **`ChannelCouplingProtocol` is the wrong hack** for UAD claims — host-owned
  ticks, not in-ecology institutional traffic.
- **Acceptable hack (GL-60 class):** implementer-only supplementary fixture with
  1–2 comms/scribe actors (extended `role_population` and/or fixture-only roles),
  real `communicate`/`write` on declared mechanisms; pre-registered UAD gate;
  **not** on grower surface or C1–C5 reference batteries.
- **GL-64 direction (next):** move exercise targets to `RuntimeEcology.exercise_targets`,
  always resolve at compile; `channel_coupling_rounds=0` when off; unify preset path.
- **GL-65 direction (after GL-64 or parallel):** supplementary UAD fixture with
  organic channel traffic; retire protocol from claim path once gate passes.
- Growth brief remains **DRAFT** — not frozen this session.

## Open / next
1. Implement GL-64 (`exercise_targets` on `RuntimeEcology`, drop dual paths).
2. Design + implement GL-65 supplementary UAD comms/scribe fixture + gate.
3. Document `ChannelCouplingProtocol` as referee-only / legacy until GL-65 passes.
4. Freeze growth brief when user signs off (Part B + detector gates documented closed).

## Left uncommitted (other workstreams)
- Chapter/appendix `\begin{epistemicstatus}` blocks (many `.tex` files)
- `hostile-review.md`, symbol-formula graph drafts, context notes, salon slides
- Generated artifacts: `generated_ecology_v2.json`, `pipeline_supplementary_orphan_eval.json`

## Key paths
- `experiments/graded-lab-simulation/graded_lab/world_visible/mechanism_exercise.py`
- `experiments/graded-lab-simulation/graded_lab/harness/supplementary_detector_gate.py`
- `experiments/graded-lab-simulation/tests/fixtures/ecology_v3_supplementary_detector_suite.json`
- `experiments/graded-lab-simulation/BLIND_GENERATION.md` § V3

## Commits
- (filled in after commit)
