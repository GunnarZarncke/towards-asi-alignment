# 2026-08-28 — Witness Phase 4

## Trigger
User asked to implement the next Witness phase (`witness-next.md` Slices A–C).

## Done
- Froze [`drafts/plans/witness-phase4.md`](../plans/witness-phase4.md).
- **W-7:** refuse WVS/ESS/LHCV-host; optional HH/PKU not run.
- **W-8:** `formal/AlignmentProofSpine/WitnessC2Instance.lean` pins C2 JSON; thresholds first; CCI floats refused; `#print axioms` on the pinned theorem.
- **W-9–W-11:** H5 JSON trees (FAA Order 2019-03-13, GPLv3 §6, Debian RC #802812) + `check_h5_trees.py`.
- Lake build: `#print axioms` is `propext` + `Lean.ofReduceBool` + `Lean.trustCompiler` on the pinned theorem (native count); no `MB*` / `Safe`.
- Appendix I indexed W-5–W-11. Construct gate **not** opened (analogues, no AI deployment leverage).

## Decisions
- Successor Lean module rather than rewriting `WorkedInstance.lean`.
- Skip optional HH/PKU rather than scrape a figure.
- H5 is Expectation 4 analogue only.

## Open / next
- Phase 5 CIRIS live (not a W-1 gate).
- KernelCI / lore NAK.
- Construct concrete MS still needs a stop **with deployment leverage**.
- Optional: rebuild PDF; `site/scripts/sync-experiments.mjs` if experiments.json must match YAML.

## Key paths
- `drafts/plans/witness-phase4.md`
- `experiments/witness/results/FINDINGS.md`
- `formal/AlignmentProofSpine/WitnessC2Instance.lean`

## Commits
- `6c7396f1` Record Witness W-5–W-11 and freeze the same-unit Moral Machine protocol.
