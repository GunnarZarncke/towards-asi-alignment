# 2026-10-07 — Freeze and copy catalog contracts 2–18 (minus 1, 4, 14)

kind: new-work
uptake: status

## Trigger
User: if ready to freeze, freeze and copy contracts up to 18 (minus 1, 4, 14) and do the needed steps in the sibling repos.
Prompts: paraphrase only (no prompt id).

## Done
- content: `ai-safety-claims` catalog contracts for Markets 2, 3, 5–13, 15–18 copied from book HEAD `888bfa8c4` boxes; Markets 1 and 4 and the new contracts set `status: frozen` as versions (not `resolutionSource`).
- bookkeeping: validator modules + `required-columns.yaml` for each; `python -m validator build` wrote 17 outcome files (all OTHER); `python -m validator test` → m01 YES/NO and m04 scenarios ok; `python -m validator check` → `ok: 17 outcome files and ui/index.html match the validator`.
- bookkeeping: README/GOVERNANCE/common-v1/ui banner; workbench README notes Inspect still only Markets 1 and 4.
- content: Appendix H pointers for those markets; `predictions.yml` `registryContractPublished` on 1–13 and 15–18.
- bookkeeping: `cd site && npm run sync:predictions` → `wrote 20 cards and predictions.json`.

## Decisions
- Freeze means frozen *contract versions*, not listing freeze. `resolutionSource` stays false; no `snapshot-0` tag (independent host still required).
- Markets 19–21 uncopied. Market 14 stays off-registry.
- Default-budget contracts do not require `adversarial-route.yaml`.

## Open / next
- Commit and push `ai-safety-claims` and `ai-safety-claims-workbench` (not done here).
- Independent host, then `snapshot-0`, then Metaculus.
- Inspect templates for the newly copied markets, if wanted.

## Key paths
- `../ai-safety-claims/market-contracts/`
- `appendices/appP-bridge-predictions.tex`

## Commits
- none
