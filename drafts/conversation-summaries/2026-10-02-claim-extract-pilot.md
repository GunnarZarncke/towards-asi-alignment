# 2026-10-02 — Claim-extract pilot (Ch. 42)

kind: new-work
uptake: local

## Trigger
User wants every chapter argument checked as far as possible: each load-bearing sentence rendered as a formal line (implication, strength qualifier, Lean referent). Pick the easiest chapter, sketch, write a draft for the first 2-3 sections, discuss findings.
Prompts: none resolved (paraphrase-only)

## Done
- content: `metadata/claim-extracts/ch42.jsonl` — records for Ch. 42 through the Summary (lines 27-332); every section except the references.
- content: `drafts/plans/claim-extract/claim-extract.md` — findings grouped into prose repairs, spine questions, source checks; discussion; open questions Q1-Q7.
- bookkeeping: `metadata/claim-extracts/README.md` (schema, stop rule); `scripts/check_claim_extract.py` (quote-vs-tex and Lean-symbol-vs-`formal/` check; run result: `ch42.jsonl: 0 error(s)`).

## Decisions
- Ch. 42 chosen: already an argument tree, maps to `Certification.lean`.
- JSONL sidecar, light typed logic (not Lean statements), user choice.
- `lean.status` is the extractor's reading, not a Lean build; not a verification claim.

## Open / next
- Author decisions on findings (chat summary): root variants (`SafeFor` vs package vs `Safe`), `D`/`T` absent from Lean, table bridge placement (MB4, MB7a), `P40` isolated, `SatisfiesInvariants` redundant.
- Plan open questions Q1-Q7 await author answers.
- Decide whether to extend to a second chapter or write an extraction prompt/spec first.

## Key paths
- `metadata/claim-extracts/`, `scripts/check_claim_extract.py`, `formal/AlignmentProofSpine/Certification.lean`
