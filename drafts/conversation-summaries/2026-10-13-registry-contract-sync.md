# 2026-10-13 — Registry contract sync from TSA (markets 2–3, 5–18)

kind: new-work
uptake: status

## Trigger
User: bring ai-safety-claims markets in sync with TSA like Market 4; skip Market 1 (in progress) and Market 4 (already aligned).
Prompts: paraphrase-only

## Done
- content: **`ai-safety-claims`** — bumped frozen contracts for catalog 2–3, 5–13, 15–18: `question` + `background` from Appendix P `predictionbackground` / `predictions.yml` `longTitle`; `yesRequires`, bars, checks unchanged; superseded `contract-v*.yaml` removed; sketches on 8/11/12 retargeted to new contract versions.
- content: **`metadata/predictions.yml`** — `contractVersion` pins updated to match registry.
- content: **`appendices/appP-bridge-predictions.tex`** — `\claimspage{…}{K}` version bumps for those markets.
- housekeeping: **`scripts/sync_registry_contracts_from_tsa.py`** — repeatable sync (registry sibling path; deletes prior contract file).
- gate: `ai-safety-claims` `.venv/bin/python3 -m validator build && check && test` → ok (17 outcome files; m01/m04 scenarios).
- gate: `cd site && npm run sync:predictions` → `sync-predictions: wrote 20 cards and predictions.json`.

## Decisions
- Listing-text-only bump: no bar changes; same pattern as Market 4 split (narrative in `background`, bars in `yesRequires`).
- Markets **1** and **4** untouched in this pass.

## Follow-up (same day)
- content: Market **1** registry edit (`output`, `per-system-output` human check, `certificate` column gloss) synced back to TSA: Appendix P authbar, `bridge-prediction-market-criteria.md` §1, `metaculus-all-markets.md`; `sync:predictions` refreshed market-01 card. Still **contract v2** (no version bump).

## Open / next
- Commit and push **`ai-safety-claims`** (contracts, outcomes, sketches, `registry.json`).
- Refresh `drafts/predictions/metaculus-all-markets.md` if listing.

## Key paths
- `../ai-safety-claims/market-contracts/`
- `scripts/sync_registry_contracts_from_tsa.py`
- `metadata/predictions.yml`, `appendices/appP-bridge-predictions.tex`

## Commits
- none (user did not ask)
