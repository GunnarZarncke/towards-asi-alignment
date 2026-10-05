# 2026-10-05 — Eval registry split

kind: new-work
uptake: status

## Trigger
Plan the split: third-party registry (sibling repo at first), appendix and site restructure, per-market registry contents, and whether Hugging Face or another registry already does this.
Prompts: paraphrase (no prompt id in this session)

## Done
- content: Plan at `drafts/plans/predictions/eval-registry-split.md`.
- bookkeeping: Pointers in `drafts/predictions/README.md`, `bridge-prediction-markets.md`, `assurance-risk-modelling.md` Phase 4, HANDOFF, INDEX.

## Decisions
- Metaculus resolves `status/market-NN.json` at a git tag (Zenodo fallback), not the literature and not a Hugging Face leaderboard.
- Scientific bars move into versioned packs in the sibling repo. Appendix keeps the property, the three-way rule, and closest existing work.
- TSA may submit; TSA does not merge adjudication after transfer.
- Do not rewrite Appendix P until a host org owns the repo.

## Open / next
- Scaffold **`ai-safety-claims`** (schemas, validator, Market 14 and Market 1 contracts, challenge-runs fixture) only when asked.
- Ask Plex (first) to take the org before any listing URL is frozen.

## Follow-up (2026-10-06)
- Renamed repo to `ai-safety-claims`; replaced “pack” with **market contract**; renamed folders (`market-contracts/`, `submitted-attempts/`, `score-table.csv`, `market-outcomes/`, `challenge-runs/`); defined attempt-id format; documented adversarial/hidden timeline and three roles.

## Key paths
- `drafts/plans/predictions/eval-registry-split.md`
- `appendices/appP-bridge-predictions.tex` (unchanged)
- `metadata/predictions.yml` (unchanged)

## Commits
- (this session)
