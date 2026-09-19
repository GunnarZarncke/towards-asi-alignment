# 2026-09-18 — Bridge prediction markets P0

## Trigger
User asked to do the obvious fixes, suggest an MB6a resolution, push back that MB3 and MB4 should already be in the catalog, suggest how to handle judgment calls, and asked about proposed changes in the docx.

## Done
- Confirmed the docx has **no comments or tracked changes** (python-docx export). Amendments live in working criteria, not in the binary.
- Recast **§3 = MB3** (transport) and **§4 = MB4** (uptake); admission and channel-preservation are probes *inside* those markets, not missing rows.
- Wrote [`drafts/predictions/bridge-prediction-market-criteria.md`](../predictions/bridge-prediction-market-criteria.md) (`0.2-working`): claim-strength, void, judgment stack, glossary, budget table, §1/§4/§6/§7 addenda, **§7a MB6a**.
- Updated [`drafts/plans/bridge-prediction-markets.md`](../plans/bridge-prediction-markets.md): P0 applied; Q3/Q4/Q5/Q7 decided; remaining Q1/Q2/Q6/Q8.

## Decisions
- MB3/MB4 were never missing markets; first-pass review over-split them.
- §7a: frozen coupling/percolation/μ_E predicts persistent **basin vs theater** (`PercolationEvidenceConfounded`). Distinct from §7 (correctability erosion / MB6b).
- Judgment: precision → publication freeze (internal splits only) → two-person desk memo → §3 panel only → void. No lone expert judge.
- §6 adopts the seven conserved properties (map six + add control locus).
- §14 stays constructibility; no 2027 MB11 market.
- Independent binaries get a banner, not delayed parlays.

## Open / next
- Superseded for binary/MB6 by `2026-09-18-bridge-markets-mb6-binary.md`. Remaining listing Qs Q1/Q2/Q6/Q8.

## Key paths
- `drafts/predictions/bridge-prediction-market-criteria.md`
- `drafts/plans/bridge-prediction-markets.md`
- `drafts/AI_Alignment_Prediction_Market_Resolution_Criteria.docx`

## Commits
- none
