# 2026-11-02 — Chapter 1 stopping rule

kind: correction
uptake: local

## Trigger
User chose revision A for Chapter 1: derive a stopping rule on the support-desk picture, and stop stating later scores and invariant lists as delivered. Add an open item to the 2.0 plan to choose one illustrative example later, possibly that picture carried further or a real system.
Prompts: `d947b68c-41c3-461f-ac7c-f98e99b6ae86`

## Done
- content: `chapters/ch01-wrong-object.tex` — stopping rule (smallest enlargement that changes the predicted failure). Agent draft; author edited wording (thesis, support-desk predictions, "When the Model Is the Right Object" rule paragraph, superintelligence section). Parsimony key claim, similarity formula, and invariant list withdrawn.
- bookkeeping: `metadata/claim-extracts/ch01.jsonl` retargeted. `ch01.075` (the deleted invariant list) removed. `scripts/check_claim_extract.py metadata/claim-extracts/ch01.jsonl` → `ch01.jsonl: 0 error(s)`.
- bookkeeping: `drafts/plans/claim-extract/claim-extract.md` — moving-object and thesis/key-claim decisions updated to the withdrawal.
- bookkeeping: `drafts/plans/construct/construct.md` — illustrative example marked not chosen; checklist item added.

## Decisions
- The support-desk loop is a worked step inside Chapter 1. It is not the running example for 2.0.
- The 2026-10-20 decision that Chapter 1 delivers a chain of admissible transitions is withdrawn. Successor preservation stays in later chapters.

## Open / next
- **Review Chapter 7** against the revised Ch. 1 rule: Ch. 1 defers the score to `ch:finding-boundary`; Ch. 7 should carry \(J(C)\) without contradicting the stopping rule or re-delivering what Ch. 1 now withholds. Blind re-derivation (2026-11-02) called Ch. 7 **working**; that is not a score-alignment pass.
- The boundary-error concept card still says some surrounding parts shape optimization more than the weights. That sentence was withdrawn from Chapter 1.
- 2.0 checklist: choose the illustrative example before multi-frame prose.
- Author copy-edit pass on Ch. 1 (e.g. "we predicts", "usefule") if desired.

## Key paths
- `chapters/ch01-wrong-object.tex`
- `drafts/plans/construct/construct.md`

## Commits
- (this session commit)
