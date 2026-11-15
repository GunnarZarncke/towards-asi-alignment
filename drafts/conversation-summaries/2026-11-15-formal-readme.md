# 2026-11-15 — Formal README orientation

kind: correction
uptake: local

## Trigger
User: `formal/README.md` is outdated; new proofs should be reflected; bridge and coined glossary terms should be explained or expanded unless Lean keeps the short name.
Prompts: paraphrase

## Done
- content: Rewrote `formal/README.md`. Vocabulary table for `MB*` bridges and short names (`CCI`, `BIQ`, `UAD`, `RiskGap`, bearer map, value bundle). ELK section lists the finite proofs past reporter non-identifiability (crisp counterexample, search, operator labels, ontology mismatch, cost crossover). Alignment-criteria section covers `FrameIncompatibility`, `FrameDecision`, `FrameHistoryState`, `FrameCorrector`, `FrameDisclosure`, `FrameLimits`, `FrameLockIn`.
- content: One bridge definition. `BridgeAssumptions` explains why `MB2`, `MB4a`, `MB10`, and `MB11` are stated later (their statements need definitions `Core.lean` does not have) and why `MB8` stays out. Short names expanded: `CCI`, `RiskGap`, `DeploymentMass`, `SuccessorSafe`, `U_H` / `U_S`.

## Decisions
- Lean identifiers stay short (`MB4`, `CCI`). The expansion sits beside the first use.
- `MB8` is described as retired from `BridgeAssumptions`, with the axiom kept for the chokepoint comparison. The word "gravestone" is not used.

## Open / next
- Shannon mutual information in `Finite/ShannonMI.lean` is still not connected to `TraceBIQ.lean`. That remains the open item in `drafts/plans/spine/spine.md`.

## Key paths
- `formal/README.md`
- `formal/AlignmentProofSpine/Field/Finite/ELKIdentifiability.lean`
- `formal/AlignmentProofSpine/FrameDecision.lean`
- `formal/AlignmentProofSpine/FrameDisclosure.lean`

## Left unstaged (other work)
- Commit-hash backfill on older session logs (`2026-11-04-book-link-root-relative.md`, `2026-11-04-llms-sync-todo-compaction.md`, `2026-11-05-field-v2-lenses-panel.md`, `2026-11-09-offline-cache-analytics.md`, `2026-11-10-compendium-chapter-cites.md`).
- `drafts/plans/field/field.md` path to `outreach/lw-wiki-tags.md`; `metadata/TODO.md` wiki-tag line.
- Untracked `reports/`, `research_notes/`, and `drafts/project/self-audit/edit-attribution/bar-updates.jsonl.lock`.

## Commits
- `399626dacd` Rewrite the Lean spine README around the checked proofs.
