# 2026-11-10 — V2 target composition and incremental construction

kind: feedback
uptake: status

## Trigger

The user tentatively chose correction-first as TSA's running reference while widening TSA 2.0 toward construction, then asked how the alignment-criteria constraints interact with incremental construction and requested that the v2 plan be updated.
Prompts: paraphrase-only

## Done

- content: Updated `drafts/plans/construct/construct.md`: correction-first is now a worked reference rather than an architecture-wide conclusion; v2 will compare correction-, rights-, capability-, and procedure-first compositions using the forced design order from the alignment-criteria paper.
- content: Added the incremental-construction split between destination composition \(P^\star\), path constraints \(\mathcal{E}\), and independently specified recovery envelope \(K_{\mathrm{path}}\). The forced order applies per frozen episode; intermediate nodes need not realize the destination.
- content: Updated `drafts/plans/construct/embedded-v2.md`: stability has no sign; \(D_{\mathrm{joint}}\) is independently justified and cannot be defined as whatever persists; viability establishes persistence or recoverability, not improvement, legitimacy, or target choice.
- bookkeeping: Updated the canonical Construct TODO, construct checklist, phase description, handoff, and session index. No manuscript or Lean changes.

## Decisions

- Tentative: TSA 2.0 is a broader construction-focused architecture with correction-first as its running reference and worked example.
- Path-level correction safeguards do not by themselves establish correction-first as the final normative composition.
- A legitimate process may revise \(P_t\) between episodes, but the episode target, criteria, and envelope are frozen before judging the intervention.

## Open / next

- Compare the four candidate compositions and decide whether correction-first remains TSA 2.0's selected composition or only its reference case.
- Choose the running example; the matched-endpoint learning-versus-rewiring case is the leading candidate.
- Manuscript edits remain behind the existing 2.0 gate; construction chapters remain behind fail/refuse evidence.

## Key paths

- `drafts/plans/construct/construct.md`
- `drafts/plans/construct/embedded-v2.md`
- `papers/alignment-criteria/alignment-criteria.tex`

## Commits

- `0bd5f86c9f` Revise TSA v2 target composition plan.
