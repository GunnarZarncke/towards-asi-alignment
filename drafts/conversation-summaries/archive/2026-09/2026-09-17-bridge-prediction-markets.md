# 2026-09-17 — Bridge prediction markets

## Trigger
User asked to read `drafts/AI_Alignment_Prediction_Market_Resolution_Criteria.docx`, create a plan in `drafts/plans/` for implementing prediction markets on the bridges, and review whether the proposal is complete, needs amendment, or adds to modeling.

## Done
- Extracted the 14 2027 binary criteria plus the common qualification rule from the docx (Read cannot open `.docx`).
- Mapped each section to live `MB*` / constructibility objects; noted MB8 correctly omitted.
- Wrote [`drafts/plans/bridge-prediction-markets.md`](../plans/bridge-prediction-markets.md): mapping, completeness gaps, required amendments, absorb vs leave-as-contract, P0–P4, author Qs.
- HANDOFF, INDEX, `metadata/TODO.md` (Outreach + Cite/Wait LI pointer), `field.md` related-artifacts link.

## Decisions
- Treat the proposal as a **contract layer**, not a new spine ontology and not Lean discharge.
- §10 is the one contract that already has Lean shape (MB7c composition).
- §14 is constructibility/governance, **not** MB11.
- Specific percentages / $100k / 2027 date stay contract-only; do not import into `RiskGap` or manuscript.
- Ordinary prediction markets ≠ logical-induction Cite/Wait item.

## Open / next
- Superseded for P0b by `2026-09-18-bridge-markets-mb6-binary.md` (binary YES/NO; MB6 \(g_{\mathrm{CCI}}\)).

## Key paths
- `drafts/plans/bridge-prediction-markets.md`
- `drafts/AI_Alignment_Prediction_Market_Resolution_Criteria.docx`
- `reference/field-agendas/data/bridges.yml`
- `docs/METHODOLOGY.md`

## Commits
- none
