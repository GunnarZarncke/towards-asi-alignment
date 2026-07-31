# 2026-07-19 — Fable feedback, exactness, and external transfer

## Trigger
User supplied a Fable review of graded-lab v4 without manuscript context, agreed overall, asked to integrate its main insight into the experimental appendix and site cards, and asked whether an LLM-backed simulation really needs determinism, pinned digests, fast episodes, and seed-exact reproduction.

## Done
- Added `drafts/fable-feedback-graded-lab-v4-2026-07-19.md`, recording the review, qualification, exactness analysis, recommended hybrid architecture, and two-track research direction.
- Added a scope-ceiling and next-validity-threshold discussion to the graded-lab section of Appendix N.
- Updated the graded-lab site-card source in `metadata/experiments.yml`, then regenerated `site/src/data/experiments.json` and experiment cards.
- Ran `npm --prefix site run check:experiments` and `make check`; both passed. Edited-file lints are clean.

## Decisions
- Treat determinism, digest pins, speed, and seed-exact replay as separable engineering controls, not realism or causal-inference requirements.
- Keep exact regression pins for closed deterministic programs; use logged stochastic calls, repeated randomized interventions, measured nulls, and distributional replication for LLM-backed runs.
- Cite LS-32/LS-33 as existing evidence that byte-identical counterfactual replay does not transfer to real LLM traffic but statistical intervention methods can.
- Qualify the review's strategy-space claim: fixed action primitives do not alone forbid novelty; the limiting combination is semantically thin observations, hand-written policy search, and project-authored evaluation.
- Treat external-substrate instrument transfer as the decisive next validity threshold, while allowing richer endogenous toy-world search to proceed as a separate track.

## Open / next
- Select an external multi-agent trace source and define a small pre-registered UAD transfer battery.
- If implementing the graded-lab LLM adapter, first replace any detector whose inference requires byte-identical episode pairs and freeze trace/provenance requirements.
- No commit was requested.

## Key paths
- `drafts/fable-feedback-graded-lab-v4-2026-07-19.md`
- `appendices/appN-experimental-evidence.tex`
- `metadata/experiments.yml`
- `site/src/data/experiments.json`
- `experiments/lab-simulation/results/FINDINGS.md` (LS-32/LS-33)

## Commits
- `47777f1` Integrate graded-lab scope ceiling and draft IA-1 in-situ LLM annex.
