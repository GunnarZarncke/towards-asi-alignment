# Bridge prediction markets (drafts)

Working contracts and source material for 2027 bridge markets — not manuscript canon.

## Live artifacts

| File | Role |
|------|------|
| [`bridge-prediction-market-criteria.md`](bridge-prediction-market-criteria.md) | Working resolution criteria (`0.4-working`) |
| [`bridge-predictions-prior-tests.md`](bridge-predictions-prior-tests.md) | Prior-art / prior-test snapshot (2026-09-19); the appendix boxes now carry a "Closest existing work" lead instead of quoting this file |
| [`resolution-gap-analysis.md`](resolution-gap-analysis.md) | Phase 2b gaps, CIRIS context, smallest next experiment |
| [`resolution-advisors.md`](resolution-advisors.md) | Proposed advisors and desk/panel protocols for other platforms. Not linked from the manuscript or the site |
| [`metaculus-question-template.md`](metaculus-question-template.md) | Create-form fields, the limits that apply, and how to lay them out in TeX and on the site |
| [`CIRIS_TSA_Combined_Experiment_Proposal.pdf`](CIRIS_TSA_Combined_Experiment_Proposal.pdf) | CIRIS×TSA experiment proposal (architecture only in the gap analysis) |
| [`AI_Alignment_Prediction_Market_Resolution_Criteria.docx`](AI_Alignment_Prediction_Market_Resolution_Criteria.docx) | Source export (no tracked changes) |

## Plans (checklists)

- [`../plans/predictions/bridge-prediction-markets.md`](../plans/predictions/bridge-prediction-markets.md) — instrument plan, mapping, phasing
- [`../plans/predictions/prediction-interface.md`](../plans/predictions/prediction-interface.md) — integration across appendix, site, Lean
- [`../plans/predictions/assurance-risk-modelling.md`](../plans/predictions/assurance-risk-modelling.md) — PRA layer; Phases 0–3 shipped
- [`../plans/predictions/eval-registry-split.md`](../plans/predictions/eval-registry-split.md) — sibling claims registry `ai-safety-claims` (scaffolded locally); appendix/site shrink to pointers later
- [`../plans/predictions/chapter-gaps-from-contracts.md`](../plans/predictions/chapter-gaps-from-contracts.md) — chapter gaps the Market 1/4 contracts exposed, with suggested resolutions

## Shipped (do not re-derive from drafts)

- Manuscript: `appendices/appP-bridge-predictions.tex` (print H)
- Site: `/predictions/` hub + `prediction` cards from `metadata/predictions.yml`; `/predictions/safety-case/` odds demo
- Manifest: `metadata/safety-case-model.yml` (shared node IDs; Markets 19–20 draft metadata)
- Lean: `formal/AlignmentProofSpine/Evidence.lean` (v1 certificate adapters)

Superseded improvement drafts (v0, incentives, Lean-improvements) are in [`../attic/`](../attic/). Open listing questions (Q1/Q2/Q6) live only in the instrument plan — not in this folder.
