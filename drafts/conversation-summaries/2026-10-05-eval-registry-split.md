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

## Follow-up 2 (2026-10-06): review fixes
Prompts: paraphrase ("review the plan … fit for purpose and clear"; then "adapt the plan accordingly; when in doubt choose simplicity")
- content: Plan now keeps Appendix P meaning: `wrapped` attempts let anyone file published work; per-contract `adversarialBudget` and `freezeOrder` copied from the box replace the over-strict default timeline; 60-day filing/adjudication window after resolve-by, tag at its end, annul on missing snapshot (not OTHER); one outcome file per contract version; `dependsOnAttempts` for Markets 10/18/19; governance minimum; admin re-trial step.
- content: First scaffolds are Markets 1 and 4 (Market 14 resolved below).
- bookkeeping: "platform adjudicates" in `bridge-prediction-markets.md` (Q1, Q6, P4, judgment section) and the `predictions.yml` header now say the registry maintainer takes over once hosted. HANDOFF "packs" → contracts.
- Decision (author): Market 14 needs no registry; lists directly on Metaculus, platform adjudicates, YES/NO only (NO = any box condition unmet). Applied: Appendix P box + reading rules, `predictions.yml` longTitle and `outcomes: [YES, NO]`, `sync-predictions.mjs` YES/NO card text.

Continued in `2026-10-06-eval-registry-scaffold.md`.

## Key paths
- `drafts/plans/predictions/eval-registry-split.md`
- `appendices/appP-bridge-predictions.tex` (unchanged)
- `metadata/predictions.yml` (header comment only)

## Commits
- `a205b76ed` Plan ai-safety-claims registry split before Metaculus listing.
