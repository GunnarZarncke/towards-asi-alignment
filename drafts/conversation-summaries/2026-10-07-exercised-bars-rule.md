# 2026-10-07 — Exercised-bars rule and registry decoupling note

kind: new-work
uptake: rule

## Trigger
User (working in sibling repo `ai-safety-claims`): apply the rule that an attempt must exercise every bar before it can count as a NO; adapt the rule in the appendix; record that the manuscript should at some point be decoupled from the registry (independence; the registry may hold non-TSA contracts).
Prompts: paraphrase only (session ran from the registry repo; no prompt id).

## Done
- content: Appendix H reading rules (`appendices/appP-bridge-predictions.tex`, after the qualifying-attempt definition): a bar whose denominator the evaluation design supplies needs at least one scored case, else the attempt is not qualifying (not a NO); an empty denominator from the method's own output is a missed bar.
- bookkeeping: `drafts/plans/predictions/eval-registry-split.md` step 5: decouple fully (registry text authoritative, non-TSA contracts allowed, independent versioning), pointing to `ai-safety-claims/GOVERNANCE.md` § Decoupling from the manuscript.
- bookkeeping: `cd site && npm run sync:predictions` → "sync-predictions: wrote 20 cards and predictions.json"; `make check` → 14 pass rows, no failing check.

## Decisions
- Rule placed once in the reading rules, not repeated in every market's Common rules paragraph.
- Registry side (same session): contracts mark design-supplied denominators with `exercisedBy`; Market 1 false-certificate bars stay without it (zero complete certificates is a NO).

## Open / next
- Whether a real minimum number of fake corrections (Market 4) or correlation-not-control systems (Market 1) is needed: author call in the box first.

## Key paths
- `appendices/appP-bridge-predictions.tex` (reading rules)
- `../ai-safety-claims/shared-rules/common-v1.yaml` (`threeWayRule.exercisedBars`)

## Commits
- none
