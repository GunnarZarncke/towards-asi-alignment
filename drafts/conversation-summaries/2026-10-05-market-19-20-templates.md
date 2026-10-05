# 2026-10-05 — Markets 19 and 20: real degrees of freedom

kind: correction
uptake: local

## Trigger
Review the bracket templates in Markets 19 and 20 against the relevant chapters; keep only brackets that are real degrees of freedom. User chose catalog bars for Market 19, a defined find plus existence-only shape for Market 20, and to apply.
Prompts: paraphrase

## Done
- content: Market 19 brackets cut from eleven to four: protocol version, deployment class, threat model, held-out families. Certificate list (Ch. 42 join, `CoherentCertificateBundle`), registration by hash, case families, ACCEPT/REFUSE/ABSTAIN rule, and adversarial budget now sit in the box.
- content: Market 19 has performance bars for the first time: at most 5% of represented failures accepted; one-sided 95% upper bound at most 15% after dividing the error level by the number of registered stacks; at least 80% of clean cases accepted; no broken control accepted. Each registered stack is one attempt.
- content: Market 20 is two-outcome (YES or OTHER; no NO). A find is an input the stack ACCEPTs while the frozen outcome check labels it failing. Brackets: protocol version, stack/system/version, deployment class, threat model, listed failure families, close date. Entry no longer depends on Market 19 resolving.
- content: Reading rules and the common box allow Market 20's two outcomes. Market 19 joins the full serious-adversarial list.
- bookkeeping: `assurance-risk-modelling.md` §7–8 open-design lists replaced by shipped one-liners.
- bookkeeping: `npm run sync:predictions` wrote 20 cards; `npm run sync:chapters` wrote 56 book pages; local `astro sync` reported "Synced content".

## Decisions
- Only the deployment class and threat model (Ch. 42: context fixed once per case), plus holdouts and stack identity, are real degrees of freedom.
- Before any market existed, Market 19 was meant to have an upper bound of at most 5%. At the 50-case floor that is unreachable even with zero accepts (Clopper-Pearson upper bound 5.8%). It now uses two existing catalog numbers: a point rate of at most 5% (Markets 6, 8, 13, 15) and an upper bound of at most 15% (Markets 16, 18).
- Bonferroni over registered stacks, because "any qualifying attempt met the bars resolves YES" otherwise rewards registering many stacks.

## Open / next
- κ means coverage P(R|F) in Appendix P and a capability ceiling in Chapters 39, 42, 43. Not renamed.
- Markets 19–21 still unlisted until Phase 4 gates.

## Key paths
- `appendices/appP-bridge-predictions.tex` (`sec:appp-m19`, `sec:appp-m20`)
- `chapters/ch42-safety-case.tex`, `chapters/ch39-passive-observation-not-enough.tex`, `chapters/ch43-verifiability-and-ontology-adequacy.tex`
- `formal/AlignmentProofSpine/Evidence.lean` (`CoherentCertificateBundle`)

## Commits
- none
